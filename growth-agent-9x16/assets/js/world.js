// Instagram Growth Agent reel: the 3D world. Everything is a pure function of time t (seconds), rendered on HyperFrames'
// hf-seek. Story (Option A, "inside the phone"): a phone spins in and lands, Claude bursts out of its screen and the
// follower count rolls 339 -> 2,400 on a 3D odometer while follows stream past the lens; one post is just a post, then
// the page grows (the grid rises out of the screen); five app icons, the fifth one dark; the camera dives through the
// screen into the phone, where each move is a room (the niche radar, the shot board, the script desk, the comment room);
// the lights go out for move five, a lab where the last reel is studied, broken apart and rebuilt as v2; then back out
// through the screen for the bonus (a gift box, the course card, an odometer to 16,000+) and the CTA (AGENT typed into the
// comments, a swarm of AGENT comments, the DM). Cue times come from the voice (window.GA_T, written by build/generate.py).
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";

const T = window.GA_T;
const L = T.l, E = T.e;
const W = 1080, H = 1920;
const IN_Z = -100;                                   // the world inside the phone sits this far down -z

const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, powerPreference: "high-performance" });
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.NeutralToneMapping;
renderer.toneMappingExposure = 1.0;

const scene = new THREE.Scene();
const BG_OUT = new THREE.Color(0xf2e8dc), BG_IN = new THREE.Color(0xf4ddcc), BG_DARK = new THREE.Color(0x0b0710);
scene.background = BG_OUT.clone();
scene.fog = new THREE.Fog(0xf2e8dc, 7, 24);
const camera = new THREE.PerspectiveCamera(40, W / H, .05, 200);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), .04).texture;
scene.environmentIntensity = .55;

// ---------------------------------------------------------------- post: bloom on the glow only, then grain / vignette / chroma
const rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });
const composer = new EffectComposer(renderer, rt);
composer.setPixelRatio(1);
composer.setSize(W, H);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), .35, .5, 1.05);
composer.addPass(bloom);
composer.addPass(new OutputPass());
const grade = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uGrain: { value: .035 }, uVig: { value: .3 }, uChroma: { value: 0 },
    uTint: { value: new THREE.Vector3(1, 1, 1) } },
  vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }",
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime, uGrain, uVig, uChroma; uniform vec3 uTint; varying vec2 vUv;
    float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
    void main(){
      vec2 c = vUv - .5; vec2 off = c * uChroma * .02;
      vec3 col = vec3(texture2D(tDiffuse, vUv + off).r, texture2D(tDiffuse, vUv).g, texture2D(tDiffuse, vUv - off).b);
      col *= uTint;
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
const backOut = (k, c = 1.7) => (k <= 0 ? 0 : 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2));
const win = (t, a, b) => clamp((t - a) / (b - a));
const pulse = (t, at, up = .08, down = .35) => (t < at ? 0 : t < at + up ? (t - at) / up : Math.max(0, 1 - (t - at - up) / down));
const between = (t, a, b) => t >= a && t < b;
const rb = (w, h, d, r = .06, seg = 3) => new RoundedBoxGeometry(w, h, d, seg, Math.min(r, w / 2 - .001, h / 2 - .001, d / 2 - .001));
const std = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: .55, metalness: 0, ...o });
const phys = (color, o = {}) => new THREE.MeshPhysicalMaterial({ color, roughness: .3, metalness: 0, ...o });
const glow = (color, k = 3, o = {}) => new THREE.MeshBasicMaterial({ color: new THREE.Color(color).multiplyScalar(k), toneMapped: false, ...o });
function mesh(geo, m, cast = true, recv = true) { const x = new THREE.Mesh(geo, m); x.castShadow = cast; x.receiveShadow = recv; return x; }
function hash(i) { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); }
function grp(parent, x = 0, y = 0, z = 0) { const g = new THREE.Group(); g.position.set(x, y, z); if (parent) parent.add(g); return g; }
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const at = (o, x, y, z) => { o.position.set(x, y, z); return o; };
const lerpV = (a, b, k) => a.map((x, i) => lerp(x, b[i], k));
const I = (x, y, z) => [x, y, z + IN_Z];             // a point inside the phone, as an array
function show(o, k) { o.visible = k > .002; o.scale.setScalar(Math.max(.001, k)); }
function canvasTex(w, h, draw) {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  const g = c.getContext("2d"); draw(g, w, h);
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8; return tx;
}
function rr(g, x, y, w, h, r) { g.beginPath(); g.roundRect(x, y, w, h, r); }
function roundedPlane(w, h, r) {
  const s = new THREE.Shape(), x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r); s.lineTo(x + w, y + h - r);
  s.quadraticCurveTo(x + w, y + h, x + w - r, y + h); s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r);
  s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
  const g = new THREE.ShapeGeometry(s, 10), p = g.attributes.position, uv = g.attributes.uv;
  for (let i = 0; i < p.count; i++) uv.setXY(i, (p.getX(i) - x) / w, (p.getY(i) - y) / h);
  return g;
}
const glowTex = canvasTex(128, 128, (g, w) => {
  const gr = g.createRadialGradient(w / 2, w / 2, 0, w / 2, w / 2, w / 2);
  gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(.35, "rgba(255,255,255,.5)"); gr.addColorStop(1, "rgba(255,255,255,0)");
  g.fillStyle = gr; g.fillRect(0, 0, w, w);
});
glowTex.colorSpace = THREE.NoColorSpace;
const add = (c, k = 1, o = {}) => new THREE.MeshBasicMaterial({ color: new THREE.Color(c).multiplyScalar(k), transparent: true, depthWrite: false,
  blending: THREE.AdditiveBlending, toneMapped: false, ...o });
function halo(size, color, k = .4) { return new THREE.Mesh(new THREE.PlaneGeometry(size, size), add(color, k, { map: glowTex })); }
const faceMat = (k = 1, o = {}) => new THREE.MeshBasicMaterial({ transparent: true, toneMapped: false, color: new THREE.Color(k, k, k), ...o });
// a flat card: a face showing a canvas texture on a thin glossy rounded slab
function card(w, h, k = 1, back = 0xfffaf5, r = .045) {
  const g = new THREE.Group();
  const face = new THREE.Mesh(new THREE.PlaneGeometry(w, h), faceMat(k)); face.position.z = .014; g.add(face);
  if (back !== null) g.add(mesh(rb(w + .012, h + .012, .025, Math.min(r, h / 2), 2), phys(back, { roughness: .35, clearcoat: 1 }), true, false));
  g.userData.face = face;
  return g;
}

// palette
const CREAM = 0xfaf4ec, TERRA = 0xd97757, CORAL_L = 0xf0a07c, PEACH = 0xf6c9a8, INK = 0x1d1418, GREEN = 0x2fbf71, GOLD = 0xffbf47,
  ROSE = 0xe9a2a0, SAND = 0xe8cfb6, LILAC = 0xb9a4f0;

// ---------------------------------------------------------------- lights
const hemi = new THREE.HemisphereLight(0xfff3e6, 0xd4b39c, 1.15); scene.add(hemi);
const key = new THREE.DirectionalLight(0xfff0e0, 2.3);
key.castShadow = true; key.shadow.mapSize.set(2048, 2048); key.shadow.radius = 5; key.shadow.bias = -.0004; key.shadow.normalBias = .02;
Object.assign(key.shadow.camera, { left: -3.2, right: 3.2, top: 3.2, bottom: -3.2, near: .5, far: 22 });
scene.add(key, key.target);
const fill = new THREE.DirectionalLight(0xffd6c2, .55); fill.position.set(4, 2, 3); scene.add(fill);
const spot = new THREE.SpotLight(0xffe7d2, 0, 14, .36, .55, 1.1);            // move five's one light
spot.castShadow = true; spot.shadow.mapSize.set(1024, 1024); spot.shadow.bias = -.0004; scene.add(spot, spot.target);
const coralLight = new THREE.PointLight(TERRA, 0, 4, 1.5); scene.add(coralLight);   // follows Claude
const fx = new THREE.PointLight(0xffe8d6, 0, 6, 1.4); scene.add(fx);                // flashes
let toneKey = 1;                                       // lighting mood: 1 day, 0 the dark lab

// ---------------------------------------------------------------- the outside: a cream infinity studio and the phone
const outside = grp(scene);
const floorO = mesh(new THREE.PlaneGeometry(90, 90), std(0xefe2d3, { roughness: .95 }), false, true); floorO.rotation.x = -Math.PI / 2; outside.add(floorO);
const PW = .78, PHH = 1.6, PD = .085, SCW = PW - .066, SCH = PHH - .066;
const phone = grp(outside, 0, 1.15, 0);
const phoneM = phys(0xd3a088, { metalness: .8, roughness: .28, clearcoat: .7, clearcoatRoughness: .2 });
phone.add(mesh(rb(PW, PHH, PD, .12, 5), phoneM));
phone.add(at(mesh(roundedPlane(PW - .024, PHH - .024, .11), std(0x0a090b, { roughness: .12 }), false, false), 0, 0, PD / 2 + .0006));
const SCR = document.createElement("canvas"); SCR.width = 720; SCR.height = 1552;
const screenTex = new THREE.CanvasTexture(SCR); screenTex.colorSpace = THREE.SRGBColorSpace; screenTex.anisotropy = 8;
const screenM = new THREE.MeshBasicMaterial({ map: screenTex, toneMapped: false });
const screen = new THREE.Mesh(roundedPlane(SCW, SCH, .088), screenM); screen.position.z = PD / 2 + .0015; phone.add(screen);
phone.add(at(mesh(rb(.2, .056, .004, .028, 2), std(0x050505, { roughness: .2 }), false, false), 0, SCH / 2 - .055, PD / 2 + .004));
for (const [x, y, h] of [[PW / 2 + .004, .32, .2], [-PW / 2 - .004, .42, .1], [-PW / 2 - .004, .24, .15]]) phone.add(at(mesh(rb(.012, h, .03, .006, 2), phoneM), x, y, 0));
const glare = new THREE.Mesh(roundedPlane(SCW, SCH, .088), new THREE.MeshBasicMaterial({ transparent: true, depthWrite: false, toneMapped: false, opacity: .5 }));
glare.position.z = PD / 2 + .0025; phone.add(glare);
const screenGlow = halo(2.6, 0xffd9c2, .0); screenGlow.position.z = -.08; phone.add(screenGlow);
// screen px -> phone-local position (the canvas is SCW x SCH)
const spx = (x, y) => V((x / 720 - .5) * SCW, (.5 - y / 1552) * SCH, PD / 2 + .002);

// ---------------------------------------------------------------- Claude: the coral spark with a face and an AGENT badge
const CL_R = .2;
const clMat = phys(TERRA, { roughness: .38, clearcoat: .8, clearcoatRoughness: .25, emissive: TERRA, emissiveIntensity: .06 });
const inkM = std(0x2a120c, { roughness: .3 });
function rays(parent, n, R, len0, len1, seed, rad = .05) {
  const out = [];
  for (let i = 0; i < n; i++) {
    const arm = i === 0 || i === n / 2;
    const a = i / n * Math.PI * 2 + (arm ? 0 : (hash(i + seed) - .5) * .22);
    const l = arm ? (len0 + len1) / 2 : lerp(len0, len1, hash(i + seed + 17));
    const piv = grp(parent); piv.rotation.z = a - Math.PI / 2; piv.position.z = -.03;
    const r = mesh(new THREE.CapsuleGeometry(rad, l, 4, 10), clMat, true, false); r.position.y = R * .55 + l / 2; piv.add(r);
    out.push({ piv, r, base: a - Math.PI / 2, l });
  }
  return out;
}
const FACES = [];                                    // [mesh, texture key], handed out once the fonts are in
const face = (m, k) => { FACES.push([m, k]); return m; };
function claudeBuild() {
  const root = grp(scene);
  const body = grp(root);
  const core = mesh(new THREE.SphereGeometry(CL_R, 40, 28), clMat); core.scale.z = .72; body.add(core);
  const rs = rays(body, 12, CL_R, .2, .34, 3, .041);
  const h0 = halo(1.9, CORAL_L, .22); h0.position.z = -.14; body.add(h0);
  const fc = grp(body, 0, 0, CL_R * .72 - .01);
  const eyes = [];
  for (const s of [-1, 1]) {
    const open = mesh(new THREE.SphereGeometry(.03, 16, 12), inkM, false, false); open.scale.set(.85, 1.35, .5); open.position.set(s * .066, .035, 0); fc.add(open);
    const hl = mesh(new THREE.SphereGeometry(.0095, 8, 6), glow(0xffffff, 1.4), false, false); hl.position.set(.011, .013, .022); open.add(hl);
    const shut = mesh(new THREE.TorusGeometry(.03, .008, 6, 14, Math.PI), inkM, false, false); shut.position.set(s * .066, .028, .006); fc.add(shut);
    eyes.push({ open, shut });
  }
  const smile = mesh(new THREE.TorusGeometry(.04, .009, 6, 16, Math.PI), inkM, false, false); smile.rotation.z = Math.PI; smile.position.set(0, -.035, .008); fc.add(smile);
  const mouthO = mesh(new THREE.SphereGeometry(.034, 14, 10), std(0x3a0f0a, { roughness: .5 }), false, false); mouthO.scale.set(1, .6, .3); mouthO.position.set(0, -.05, .004); fc.add(mouthO);
  for (const s of [-1, 1]) { const ch = new THREE.Mesh(new THREE.CircleGeometry(.026, 16), add(0xff7a90, .32)); ch.position.set(s * .118, -.022, -.004); fc.add(ch); }
  for (const s of [-1, 1]) {
    const st = mesh(new THREE.CylinderGeometry(.0055, .0055, .2, 6), std(CREAM, { roughness: .6 }), false, false);
    st.position.set(s * .065, -.2, .135); st.rotation.z = s * .32; st.rotation.x = .12; body.add(st);
  }
  const badge = card(.17, .1, 1.05, 0xfffaf5, .02); badge.position.set(0, -.33, .14); badge.rotation.x = -.08; body.add(badge);
  face(badge.userData.face, "badge");
  root.scale.setScalar(.001); root.visible = false;
  return { root, body, rs, eyes, smile, mouthO, halo: h0 };
}
const cl = claudeBuild();

// ---------------------------------------------------------------- the 3D odometer (339 -> 2,400 and 0 -> 16,000+)
// each drum is a cylinder lying on its side; its texture strip holds 0-9 and a blank (slot 10), and turning the drum is
// shifting the strip, so a number rolls the way a mechanical counter does
const DRUMS = [];
function odometer(parent, n, commaAt, plus) {
  const g = grp(parent);
  const R = .125, HD = .17, SP = .195;
  const wd = n * SP + (plus ? .16 : 0) + .16;
  g.add(at(mesh(rb(wd, .38, .2, .1, 4), std(INK, { roughness: .35, metalness: .2 })), plus ? .08 : 0, 0, -.07));
  const drums = [];
  const capM = std(0xf1e6da, { roughness: .4 });
  for (let i = 0; i < n; i++) {
    const side = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .35 });
    const d = mesh(new THREE.CylinderGeometry(R, R, HD, 48, 1, false).rotateZ(Math.PI / 2), [side, capM, capM], true, false);
    d.position.x = (i - (n - 1) / 2) * SP; g.add(d);
    drums.push(side); DRUMS.push(side);
  }
  const maskM = std(INK, { roughness: .35, metalness: .2 });
  for (const s of [-1, 1]) g.add(at(mesh(rb(n * SP + .04, .12, .03, .012, 2), maskM, false, false), 0, s * .108, R + .012));
  const comma = card(.05, .09, 1, null); comma.position.set((commaAt - .5 - (n - 1) / 2) * SP, -.025, R + .03); g.add(comma); face(comma.userData.face, "comma");
  let pl = null;
  if (plus) { pl = card(.13, .13, 1, null); pl.position.set(((n - 1) / 2) * SP + .19, 0, .1); g.add(pl); face(pl.userData.face, "plus"); }
  const label = card(.62, .1, 1, null); label.position.set(plus ? .08 : 0, -.29, .02); g.add(label);
  return { g, drums, n, comma, plus: pl, label, commaAt };
}
// v: the value (float); the drums roll continuously, leading zeros blank
function setOdo(o, v) {
  v = Math.max(0, v);
  for (let i = 0; i < o.n; i++) {
    const p = o.n - 1 - i;                             // place: 0 = units
    const P = Math.pow(10, p);
    let s;
    if (p > 0 && v < P) s = 10;
    else {
      const d = Math.floor(v / P) % 10;
      const roll = p === 0 ? v % 1 : clamp((v % P) - (P - 1));
      s = d + roll;
    }
    const tx = o.drums[i].map;
    if (tx) tx.offset.x = (s + 1.5) / 11;
  }
  o.comma.visible = v >= Math.pow(10, o.n - o.commaAt);
}

// ---------------------------------------------------------------- outside props
// odometer 1: the followers
const odo1 = odometer(outside, 4, 1, false); odo1.g.position.set(0, 2.3, .28); face(odo1.label.userData.face, "lblFollowers");
// "+1 follower" pills streaming out of the screen past the lens
const PILLS = [];
for (let i = 0; i < 26; i++) {
  const c = card(.4, .105, 1, 0xfffaf5, .05); outside.add(c); face(c.userData.face, "pill" + (i % 3)); c.visible = false;
  const t0 = 2.55 + i * .13 + hash(i + 2) * .06;
  PILLS.push({ c, t0, sx: (hash(i) - .5) * .5, sy: .45 + hash(i + 9) * 1.2, dx: (hash(i + 4) - .5) * 1.5, dy: (hash(i + 6) - .3) * .9 });
}
// confetti: one instanced burst per moment
const CONF_N = 150;
function confetti(parent) {
  const geo = new THREE.PlaneGeometry(.035, .055);
  const m = new THREE.InstancedMesh(geo, new THREE.MeshStandardMaterial({ side: THREE.DoubleSide, roughness: .5 }), CONF_N);
  const cols = [TERRA, CORAL_L, GOLD, CREAM, GREEN, PEACH, LILAC];
  for (let i = 0; i < CONF_N; i++) m.setColorAt(i, new THREE.Color(cols[i % cols.length]));
  m.instanceColor.needsUpdate = true; m.frustumCulled = false; parent.add(m);
  return m;
}
const confA = confetti(outside), confB = confetti(outside);
const tM = new THREE.Matrix4(), tP = new THREE.Vector3(), tQ = new THREE.Quaternion(), tS = new THREE.Vector3(), tE = new THREE.Euler();
const ZERO = new THREE.Matrix4().makeScale(0, 0, 0);
function burst(m, t, t0, o, spread = 1) {
  const dt = t - t0;
  if (dt < 0 || dt > 2.2) { m.visible = false; return; }
  m.visible = true;
  for (let i = 0; i < CONF_N; i++) {
    const a = hash(i * 3.1) * Math.PI * 2, up = .9 + hash(i + 7) * 1.6, sp = (.6 + hash(i + 2) * 1.4) * spread;
    tP.set(o.x + Math.cos(a) * sp * dt, o.y + up * dt - 1.6 * dt * dt, o.z + Math.sin(a) * sp * dt * .8 + .3 * dt);
    tE.set(dt * (4 + hash(i) * 8), dt * (3 + hash(i + 1) * 6), i); tQ.setFromEuler(tE);
    tS.setScalar(Math.max(0, 1 - win(dt, 1.4, 2.2)));
    m.setMatrixAt(i, tM.compose(tP, tQ, tS));
  }
  m.instanceMatrix.needsUpdate = true;
}
// Claude's burst out of the screen: a shockwave ring
const shock = new THREE.Mesh(new THREE.RingGeometry(.3, .36, 64), add(CORAL_L, 1.4, { side: THREE.DoubleSide })); outside.add(shock);
// the post: a reel card that slides out, gets stamped "just posting" and is dropped
const reel = card(.46, .78, 1, 0xfffaf5, .05); outside.add(reel); face(reel.userData.face, "reel");
// the page grows: the grid's nine tiles rise out of the screen
const TILE_COL = [TERRA, PEACH, INK, CORAL_L, SAND, TERRA, ROSE, INK, CORAL_L];
const TILE_H = [.16, .26, .2, .3, .42, .34, .38, .56, .74];
const tiles = TILE_COL.map((c, i) => {
  const r = Math.floor(i / 3), k = i % 3;
  const p = spx(126 + k * 234, 958 + r * 234);
  const m = mesh(rb(.218, .218, 1, .03, 3), std(c, { roughness: .5 })); m.geometry.translate(0, 0, .5);
  m.position.copy(p); phone.add(m); m.visible = false;
  return { m, r, k };
});
const arrowShape = new THREE.Shape();
arrowShape.moveTo(-.03, -.5); arrowShape.lineTo(.03, -.5); arrowShape.lineTo(.03, .32); arrowShape.lineTo(.1, .32); arrowShape.lineTo(0, .5);
arrowShape.lineTo(-.1, .32); arrowShape.lineTo(-.03, .32); arrowShape.closePath();
const arrow = mesh(new THREE.ExtrudeGeometry(arrowShape, { depth: .04, bevelEnabled: true, bevelSize: .012, bevelThickness: .012, bevelSegments: 2 }),
  phys(GREEN, { roughness: .3, clearcoat: 1, emissive: GREEN, emissiveIntensity: .15 }));
phone.add(arrow); arrow.visible = false;
// five app icons, the fifth one dark with a "?"
const ICONS = Array.from({ length: 5 }, (_, i) => {
  const g = grp(outside);
  g.add(mesh(rb(.26, .26, .08, .07, 4), phys(i === 4 ? INK : 0xfffaf5, { roughness: .3, clearcoat: 1 })));
  const f = new THREE.Mesh(roundedPlane(.235, .235, .06), faceMat(1)); f.position.z = .0405; g.add(f); face(f, "icon" + i);
  const h = halo(.9, TERRA, 0); h.position.z = -.08; g.add(h);
  g.userData = { f, h }; g.visible = false;
  return g;
});
// the bonus: a gift box, the course card, odometer 2 (downloads)
const gift = grp(outside);
const giftM = phys(TERRA, { roughness: .4, clearcoat: .8 }), ribM = phys(CREAM, { roughness: .35, clearcoat: 1 });
gift.add(at(mesh(rb(.5, .38, .5, .04, 3), giftM), 0, 0, 0));
gift.add(at(mesh(new THREE.BoxGeometry(.09, .385, .505), ribM), 0, 0, 0));
gift.add(at(mesh(new THREE.BoxGeometry(.505, .385, .09), ribM), 0, 0, 0));
const lid = grp(gift, 0, .2, 0);
lid.add(mesh(rb(.56, .1, .56, .03, 3), giftM));
lid.add(at(mesh(new THREE.BoxGeometry(.095, .105, .565), ribM), 0, 0, 0));
lid.add(at(mesh(new THREE.BoxGeometry(.565, .105, .095), ribM), 0, 0, 0));
for (const s of [-1, 1]) { const bow = mesh(new THREE.TorusGeometry(.07, .025, 10, 24), ribM); bow.position.set(s * .07, .1, 0); bow.rotation.set(0, s * .5, s * .6); lid.add(bow); }
gift.visible = false;
const course = card(.92, .62, 1, 0xfffaf5, .05); outside.add(course); face(course.userData.face, "course"); course.visible = false;
const freeStamp = card(.32, .12, 1, null); course.add(freeStamp); freeStamp.position.set(.3, .25, .04); freeStamp.rotation.z = -.2; face(freeStamp.userData.face, "free");
const odo2 = odometer(outside, 5, 2, true); odo2.g.position.set(-.05, 1.5, .85); odo2.g.visible = false; face(odo2.label.userData.face, "lblDownloads");
// the CTA: a swarm of AGENT comments and the DM
const SWARM = Array.from({ length: 20 }, (_, i) => {
  const c = card(.5, .12, 1, 0xfffaf5, .06); outside.add(c); face(c.userData.face, "ag" + (i % 6)); c.visible = false;
  const side = i % 2 ? 1 : -1;
  return { c, t0: T.agentcta + .05 + i * .11, x: side * (.55 + hash(i + 3) * .4), z: .15 + hash(i + 8) * .8, sp: .35 + hash(i + 1) * .3 };
});
const dm = card(.78, .2, 1, 0xfffaf5, .07); outside.add(dm); face(dm.userData.face, "dm"); dm.visible = false;

// ---------------------------------------------------------------- the inside of the phone: warm clay rooms, one per move
const inside = grp(scene, 0, 0, IN_Z);
const floorI = mesh(new THREE.PlaneGeometry(120, 120), std(0xf0d6c3, { roughness: .9 }), false, true); floorI.rotation.x = -Math.PI / 2; inside.add(floorI);
// floating UI shapes on both sides of the path: hearts, pills, toggles, play buttons, tiles (parallax as the camera flies)
const heart = new THREE.Shape();
heart.moveTo(0, -.5); heart.bezierCurveTo(-.15, -.35, -.55, -.05, -.5, .2); heart.bezierCurveTo(-.45, .5, -.08, .52, 0, .25);
heart.bezierCurveTo(.08, .52, .45, .5, .5, .2); heart.bezierCurveTo(.55, -.05, .15, -.35, 0, -.5);
const heartGeo = new THREE.ExtrudeGeometry(heart, { depth: .18, bevelEnabled: true, bevelSize: .06, bevelThickness: .06, bevelSegments: 4, curveSegments: 18 }).center();
const play = new THREE.Shape(); play.moveTo(-.3, -.35); play.lineTo(.4, 0); play.lineTo(-.3, .35); play.closePath();
const playGeo = new THREE.ExtrudeGeometry(play, { depth: .12, bevelEnabled: true, bevelSize: .06, bevelThickness: .05, bevelSegments: 3 }).center();
const DECO = [];
{
  const geos = [heartGeo, new THREE.CapsuleGeometry(.18, .5, 6, 16).rotateZ(Math.PI / 2), playGeo, rb(.5, .5, .16, .12, 4), new THREE.TorusGeometry(.26, .09, 14, 32),
    new THREE.SphereGeometry(.24, 24, 16)];
  const cols = [TERRA, CREAM, CORAL_L, PEACH, ROSE, 0xffffff, SAND, LILAC];
  for (let i = 0; i < 64; i++) {
    const side = i % 2 ? 1 : -1;
    const m = mesh(geos[i % geos.length], phys(cols[(i * 3) % cols.length], { roughness: .45, clearcoat: .5 }), false, false);
    const s = .55 + hash(i + 11) * .9;
    m.scale.setScalar(s);
    const z = 6 - i * .62 - hash(i) * .5;
    m.position.set(side * (5.4 + hash(i + 5) * 4), .5 + hash(i + 7) * 4, z);
    m.rotation.set(hash(i + 1) * 3, hash(i + 2) * 3, hash(i + 3) * 3);
    inside.add(m);
    DECO.push({ m, y: m.position.y, ph: hash(i + 13) * 6, rs: (hash(i + 21) - .5) * .8 });
  }
}
// an arch behind each room, so the rooms read as rooms
const ROOMS = [V(0, 0, 0), V(-3.5, 0, -5), V(3.5, 0, -9), V(0, 0, -14)];
ROOMS.forEach((p, i) => {
  const a = mesh(new THREE.TorusGeometry(2.3, .13, 16, 64, Math.PI), phys([TERRA, CORAL_L, TERRA, PEACH][i], { roughness: .4, clearcoat: .6 }));
  a.position.set(p.x, 0, p.z - 1.6); inside.add(a);
});
// move 1: the niche radar
const radar = grp(inside, 0, 0, 0);
radar.add(at(mesh(new THREE.CylinderGeometry(1.38, 1.45, .07, 72), std(0xfff7ef, { roughness: .5 })), 0, .035, 0));
for (const r of [.45, .9, 1.3]) { const ring = mesh(new THREE.TorusGeometry(r, .009, 6, 96), std(TERRA, { roughness: .5 }), false, false); ring.rotation.x = -Math.PI / 2; ring.position.y = .072; radar.add(ring); }
for (const a of [0, Math.PI / 2]) { const ln = mesh(new THREE.BoxGeometry(2.6, .004, .012), std(TERRA), false, false); ln.position.y = .072; ln.rotation.y = a; radar.add(ln); }
const sweepG = grp(radar, 0, .075, 0);
const sweep = new THREE.Mesh(new THREE.CircleGeometry(1.32, 48, 0, .85), add(TERRA, .55, { side: THREE.DoubleSide })); sweep.rotation.x = -Math.PI / 2; sweepG.add(sweep);
const sweepEdge = mesh(new THREE.BoxGeometry(1.32, .01, .016), glow(TERRA, 1.6), false, false); sweepEdge.position.x = .66; sweepG.add(sweepEdge);
const TRENDS = [[-.3, .5, -.15], [.42, .02, .15], [-.12, -.55, -.05]].map(([x, z, ry], i) => {
  const c = card(.82, .25, 1, 0xfffaf5, .05); c.position.set(x, .46, z); c.rotation.set(-.38, ry, 0); radar.add(c); face(c.userData.face, "trend" + i); c.visible = false;
  return c;
});
const hotBar = mesh(rb(.14, 1, .14, .05, 3), phys(TERRA, { roughness: .35, clearcoat: 1, emissive: TERRA, emissiveIntensity: .35 })); hotBar.geometry.translate(0, .5, 0);
hotBar.position.set(-.3, .07, .32); radar.add(hotBar);
const hotBadge = card(.52, .14, 1, null); hotBadge.position.set(-.3, 1.3, .38); radar.add(hotBadge); face(hotBadge.userData.face, "hot");
const FLAME = Array.from({ length: 14 }, (_, i) => { const h = halo(.16 + hash(i) * .12, i % 2 ? GOLD : TERRA, .9); radar.add(h); return h; });
const radarTitle = card(.9, .13, 1, null); radarTitle.position.set(.05, 1.0, -.9); radar.add(radarTitle); face(radarTitle.userData.face, "radarTitle");
// move 2: the shot board, four vertical frames snap in, then the palette
const boardG = grp(inside, -3.5, 1.2, -5);
boardG.add(at(mesh(rb(1.08, 1.62, .06, .06, 3), phys(0xfffaf5, { roughness: .45, clearcoat: .5 })), 0, -.06, -.04));
const boardHead = card(.9, .1, 1, null); boardHead.position.set(0, .64, .0); boardG.add(boardHead); face(boardHead.userData.face, "boardHead");
const FRAMES = Array.from({ length: 4 }, (_, i) => {
  const c = card(.36, .62, 1, 0xfffaf5, .03); boardG.add(c); face(c.userData.face, "frame" + i); c.visible = false; return c;
});
const SWATCH = [TERRA, CORAL_L, CREAM, INK, GOLD].map((col, i) => {
  const m = mesh(new THREE.CylinderGeometry(.075, .075, .03, 32).rotateX(Math.PI / 2), phys(col, { roughness: .35, clearcoat: 1 }));
  m.position.set(-.4 + i * .2, -1.0, .1); boardG.add(m); m.visible = false; return m;
});
// move 3: the script desk; the page types itself, the keys spell AGENT, the caption pops
const deskG = grp(inside, 3.5, 1.1, -9); deskG.rotation.y = -.12;
const page = card(1.0, 1.2, 1, 0xfffaf5, .04); deskG.add(page); face(page.userData.face, "page");
const PLINES = Array.from({ length: 5 }, (_, i) => {
  const w = .84, h = .085;
  const geo = new THREE.PlaneGeometry(w, h); geo.translate(w / 2, 0, 0);
  const m = new THREE.Mesh(geo, faceMat(1)); m.position.set(-.42, .3 - i * .13, .016); page.add(m); face(m, "pl" + i);
  return m;
});
const caret = mesh(new THREE.BoxGeometry(.012, .07, .004), glow(TERRA, 1.2), false, false); page.add(caret);
const capCard = card(.82, .3, 1, 0xfffaf5, .05); capCard.position.set(.5, -.62, .25); capCard.rotation.z = .05; deskG.add(capCard); face(capCard.userData.face, "caption"); capCard.visible = false;
const KEYS = "AGENT".split("").map((ch, i) => {
  const g = grp(deskG, -.44 + i * .19, -.82, .35);
  g.add(mesh(rb(.16, .09, .16, .03, 3), phys(i === 0 ? TERRA : 0xfffaf5, { roughness: .35, clearcoat: 1 })));
  const f = new THREE.Mesh(new THREE.PlaneGeometry(.13, .13), faceMat(1)); f.rotation.x = -Math.PI / 2; f.position.y = .046; g.add(f); face(f, "key" + i);
  g.rotation.x = .5;
  return g;
});
// move 4: the comment room; comments fly in, replies snap beside them
const roomG = grp(inside, 0, 1.45, -14); roomG.scale.setScalar(.72);
const CMS = Array.from({ length: 3 }, (_, i) => {
  const c = card(.98, .2, 1, 0xfffaf5, .06); c.position.set(-.18, .52 - i * .5, 0); roomG.add(c); face(c.userData.face, "cm" + i); c.visible = false;
  const r = card(.78, .17, 1, TERRA, .06); r.position.set(.28, .3 - i * .5, .12); roomG.add(r); face(r.userData.face, "rp" + i); r.visible = false;
  return { c, r };
});
const PLANES = Array.from({ length: 3 }, () => {
  const s = new THREE.Shape(); s.moveTo(0, 0); s.lineTo(-.12, .035); s.lineTo(-.09, 0); s.lineTo(-.12, -.035); s.closePath();
  const m = mesh(new THREE.ShapeGeometry(s), std(0xffffff, { side: THREE.DoubleSide }), false, false); roomG.add(m); m.visible = false; return m;
});
// move 5: the lab, off to the side so no other room is behind it
const LAB = V(10, 0, -20);
const lab = grp(inside, LAB.x, 0, LAB.z);
lab.add(at(mesh(new THREE.CylinderGeometry(.42, .5, .62, 48), phys(0x1b1218, { roughness: .25, clearcoat: 1 })), 0, .31, 0));
const rim = mesh(new THREE.TorusGeometry(.42, .012, 8, 64), glow(TERRA, 2.2), false, false); rim.rotation.x = -Math.PI / 2; rim.position.y = .62; lab.add(rim);
const labFloor = mesh(new THREE.CircleGeometry(3.2, 64), std(0x150d12, { roughness: .35, metalness: .3 }), false, true); labFloor.rotation.x = -Math.PI / 2; labFloor.position.y = .004; lab.add(labFloor);
for (const r of [.9, 1.5, 2.2]) { const ring = new THREE.Mesh(new THREE.RingGeometry(r, r + .012, 96), add(TERRA, .35, { side: THREE.DoubleSide })); ring.rotation.x = -Math.PI / 2; ring.position.y = .01; lab.add(ring); }
const oldReel = card(.5, .88, 1, 0x1a1220, .05); oldReel.position.set(0, 1.12, 0); lab.add(oldReel); face(oldReel.userData.face, "reelOld");
const scanRing = new THREE.Mesh(new THREE.TorusGeometry(.43, .008, 8, 80), add(0xffd9c2, 2.0)); scanRing.rotation.x = Math.PI / 2; lab.add(scanRing);
const scanDisc = new THREE.Mesh(new THREE.CircleGeometry(.43, 64), add(TERRA, .25, { side: THREE.DoubleSide })); scanDisc.rotation.x = -Math.PI / 2; lab.add(scanDisc);
const METRICS = Array.from({ length: 3 }, (_, i) => {
  const c = card(.62, .17, 1, 0x1a1220, .05); c.position.set(-.06, 1.0 - i * .2, .32); c.scale.setScalar(.82); lab.add(c); face(c.userData.face, "met" + i); c.visible = false;
  const bar = mesh(new THREE.BoxGeometry(.4, .022, .01), glow([TERRA, CORAL_L, GOLD][i], 1.5), false, false); bar.geometry.translate(.2, 0, 0); bar.position.set(-.24, -.045, .02); c.add(bar);
  return { c, bar, fill: [.82, .64, .9][i] };
});
const DATA = Array.from({ length: 28 }, (_, i) => { const h = halo(.07, i % 3 ? CORAL_L : 0xffffff, 1.2); lab.add(h); h.visible = false; return h; });
const SH_C = 7, SH_R = 12, SH_N = SH_C * SH_R;
const shards = new THREE.InstancedMesh(new THREE.BoxGeometry(.066, .066, .02), new THREE.MeshStandardMaterial({ roughness: .4, emissive: 0xffffff, emissiveIntensity: .04 }), SH_N);
for (let i = 0; i < SH_N; i++) {
  const r = Math.floor(i / SH_C), k = i % SH_C;
  shards.setColorAt(i, new THREE.Color().setHSL((18 + r * 2 + k) / 360, .62, .42 + (r / SH_R) * .25));
}
shards.instanceColor.needsUpdate = true; shards.frustumCulled = false; lab.add(shards); shards.visible = false;
const newReel = card(.5, .88, 1, TERRA, .05); lab.add(newReel); face(newReel.userData.face, "reelNew"); newReel.visible = false;
const newHalo = halo(2.2, CORAL_L, 0); newHalo.position.z = -.1; newReel.add(newHalo);
const loopG = grp(lab, 0, 1.12, 0);
const loopRing = new THREE.Mesh(new THREE.TorusGeometry(.48, .01, 8, 96), add(CORAL_L, 1.6)); loopG.add(loopRing);
const LOOP = Array.from({ length: 3 }, (_, i) => { const c = card(.3, .088, 1, null); loopG.add(c); face(c.userData.face, "loop" + i); return c; });
loopG.visible = false;
// drifting dust in the light, everywhere (inside the phone and out)
const DUST_N = 160;
const dust = new THREE.InstancedMesh(new THREE.PlaneGeometry(.03, .03), add(0xfff0e0, .5, { map: glowTex }), DUST_N); dust.frustumCulled = false; scene.add(dust);

// ---------------------------------------------------------------- the screen (one canvas, redrawn when its state changes)
let screenKey = "";
const fmt = (n) => Math.round(n).toLocaleString("en-US");
function sparkGlyph(g, x, y, R, c = "#d97757") {
  g.fillStyle = c;
  for (let i = 0; i < 12; i++) {
    const a = i / 12 * Math.PI * 2 + (i % 2) * .05, l = R * (.75 + hash(i + 3) * .3);
    g.save(); g.translate(x, y); g.rotate(a); rr(g, -R * .13, R * .2, R * .26, l, R * .13); g.fill(); g.restore();
  }
  g.beginPath(); g.arc(x, y, R * .42, 0, Math.PI * 2); g.fill();
}
function write(g, s, x, y, size, o = {}) {
  g.font = `${o.i ? "italic " : ""}${o.w || 700} ${size}px ${o.f || "Montserrat"}`; g.fillStyle = o.c || "#1d1418"; g.textAlign = o.a || "left"; g.textBaseline = "middle";
  g.fillText(s, x, y, o.max);
}
function tick(g, x, y, s, c = "#2fbf71", lw = 0) {
  g.strokeStyle = c; g.lineWidth = lw || s * .2; g.lineCap = "round"; g.lineJoin = "round";
  g.beginPath(); g.moveTo(x - s * .45, y); g.lineTo(x - s * .12, y + s * .32); g.lineTo(x + s * .48, y - s * .36); g.stroke();
}
const TILE_GR = [["#d97757", "#f0a07c"], ["#f6c9a8", "#e8cfb6"], ["#1d1418", "#4a2c30"], ["#f0a07c", "#ffd9c2"], ["#e8cfb6", "#d9b79a"],
  ["#c4603f", "#d97757"], ["#e9a2a0", "#f6c9a8"], ["#2a1c22", "#1d1418"], ["#f0a07c", "#d97757"]];
function thumb(g, x, y, w, h, k) {
  const [a, b] = TILE_GR[k % 9], gr = g.createLinearGradient(x, y, x + w, y + h); gr.addColorStop(0, a); gr.addColorStop(1, b);
  g.fillStyle = gr; g.fillRect(x, y, w, h);
  g.fillStyle = "rgba(255,255,255,.75)"; g.beginPath(); const cx = x + w / 2, cy = y + h / 2; g.moveTo(cx - 12, cy - 16); g.lineTo(cx + 16, cy); g.lineTo(cx - 12, cy + 16); g.fill();
}
function drawScreen(k) {
  if (k === screenKey) return;
  screenKey = k;
  const g = SCR.getContext("2d"), w = 720, h = 1552;
  const [kind, a, b] = k.split("|");
  g.fillStyle = "#fffaf5"; g.fillRect(0, 0, w, h);
  write(g, "9:41", 60, 46, 30, { w: 700 });
  g.fillStyle = "#1d1418"; rr(g, 610, 34, 52, 24, 7); g.fill();
  if (kind === "p") {                                     // the profile: followers = a, b = "nogrid" while the tiles stand out
    write(g, "ai.nxtlvl", 48, 150, 46, { w: 800 });
    g.fillStyle = "#3d8bff"; g.beginPath(); g.arc(282, 150, 14, 0, 7); g.fill(); tick(g, 282, 151, 14, "#fff", 4);
    g.fillStyle = "#1d1418"; g.beginPath(); g.arc(150, 330, 102, 0, 7); g.fill();
    write(g, "nxtlvl", 150, 332, 44, { w: 800, c: "#fff", a: "center" });
    g.strokeStyle = "#d97757"; g.lineWidth = 8; g.beginPath(); g.arc(150, 330, 116, 0, 7); g.stroke();
    write(g, a, 470, 312, 72, { w: 800, a: "center" });
    write(g, "followers", 470, 372, 30, { w: 600, c: "#6b5a55", a: "center" });
    write(g, "Nxtlvl AI", 48, 500, 36, { w: 800 });
    ["New AI tool every post. No fluff.", "Free tool list + tutorials", "Open to collabs"].forEach((s, i) => write(g, s, 48, 552 + i * 44, 30, { w: 500, c: "#3a2a2a" }));
    [["Edit profile", 48], ["Share profile", 372]].forEach(([s, x]) => { g.fillStyle = "#efe4d8"; rr(g, x, 700, 300, 70, 16); g.fill(); write(g, s, x + 150, 736, 28, { w: 700, a: "center" }); });
    g.fillStyle = "#1d1418"; g.fillRect(0, 818, w, 2);
    if (b !== "nogrid") for (let i = 0; i < 9; i++) thumb(g, 9 + (i % 3) * 234, 841 + Math.floor(i / 3) * 234, 230, 230, i);
    else { g.fillStyle = "#f4ebe1"; g.fillRect(0, 822, w, 720); }
  } else if (kind === "c") {                              // the comments sheet: a = typed text, b = "sent"; the field sits high
    thumb(g, 0, 80, w, 420, 0);
    g.fillStyle = "rgba(29,20,24,.35)"; g.fillRect(0, 80, w, 420);
    g.fillStyle = "#fffaf5"; rr(g, 0, 380, w, 1180, 40); g.fill();
    g.fillStyle = "#d8cabd"; rr(g, 310, 398, 100, 10, 5); g.fill();
    write(g, "Comments", w / 2, 450, 34, { w: 800, a: "center" });
    const rows = [["creator.sana", "AGENT"], ["tech.aman", "agent pls"], ["neha.edits", "AGENT"], ["j.reels", "AGENT!!"], ["studio.kai", "agent"]];
    if (b === "sent") rows.unshift(["you", "AGENT"]);
    g.fillStyle = "#f1e7dc"; rr(g, 30, 520, 560, 96, 48); g.fill();
    g.fillStyle = "#d97757"; g.beginPath(); g.arc(90, 568, 30, 0, 7); g.fill();
    if (a) write(g, a, 140, 568, 40, { w: 800 }); else write(g, "Add a comment…", 140, 568, 34, { w: 500, c: "#a8968c" });
    g.fillStyle = a ? "#d97757" : "#e1d3c6"; g.beginPath(); g.arc(650, 568, 44, 0, 7); g.fill();
    g.strokeStyle = "#fff"; g.lineWidth = 7; g.lineCap = "round"; g.beginPath(); g.moveTo(632, 568); g.lineTo(668, 568); g.moveTo(654, 552); g.lineTo(670, 568); g.lineTo(654, 584); g.stroke();
    rows.slice(0, 6).forEach(([n, s], i) => {
      const y = 670 + i * 130;
      if (b === "sent" && i === 0) { g.fillStyle = "#fbe7dd"; rr(g, 20, y - 40, w - 40, 120, 24); g.fill(); }
      g.fillStyle = ["#d97757", "#8b6cf6", "#3d8bff", "#2fbf71", "#f0a07c", "#e9a2a0"][(i + (b === "sent" ? 5 : 0)) % 6]; g.beginPath(); g.arc(80, y + 20, 34, 0, 7); g.fill();
      write(g, n, 134, y, 26, { w: 600, c: "#7a6a64" }); write(g, s, 134, y + 42, 34, { w: 800 });
    });
  }
  screenTex.needsUpdate = true;
}

// ---------------------------------------------------------------- textures (drawn once the fonts are in)
const TX = {};
function panel(g, w, h, o = {}) {
  rr(g, 2, 2, w - 4, h - 4, o.r ?? 22); g.fillStyle = o.bg || "#fffaf5"; g.fill();
  if (o.line) { g.strokeStyle = o.line; g.lineWidth = o.lw || 3; g.stroke(); }
}
function avatar(g, x, y, r, c, letter) { g.fillStyle = c; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); write(g, letter, x, y + 2, r * 1.1, { w: 800, c: "#fff", a: "center" }); }
function drawTextures() {
  const ct = (k, w, h, f) => { TX[k] = canvasTex(w, h, f); };
  ct("badge", 256, 150, (g, w, h) => { panel(g, w, h, { r: 18 }); g.fillStyle = "#d97757"; g.fillRect(2, 2, w - 4, 34);
    write(g, "CLAUDE", w / 2, 20, 20, { f: "JBMono", c: "#fff", a: "center" }); write(g, "AGENT", w / 2, 90, 54, { w: 800, a: "center" }); });
  // the odometer strip: 0-9 and a blank, each glyph turned a quarter so it stands upright on the drum
  ct("digits", 11 * 128, 160, (g, w, h) => {
    g.fillStyle = "#fffaf5"; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 10; i++) { g.save(); g.translate(i * 128 + 64, h / 2); g.rotate(Math.PI / 2); write(g, String(i), 0, 6, 132, { w: 800, a: "center" }); g.restore(); }
    g.fillStyle = "rgba(29,20,24,.08)"; for (let i = 0; i <= 11; i++) g.fillRect(i * 128 - 2, 0, 4, h);
  });
  TX.digits.wrapS = THREE.RepeatWrapping;
  ct("comma", 64, 116, (g, w, h) => write(g, ",", w / 2, h / 2 - 20, 130, { w: 800, c: "#fffaf5", a: "center" }));
  ct("plus", 128, 128, (g, w, h) => write(g, "+", w / 2, h / 2 + 4, 140, { w: 800, c: "#f0a07c", a: "center" }));
  ct("lblFollowers", 512, 82, (g, w, h) => write(g, "FOLLOWERS", w / 2, h / 2, 46, { f: "JBMono", c: "#1d1418", a: "center" }));
  ct("lblDownloads", 512, 82, (g, w, h) => write(g, "DOWNLOADS", w / 2, h / 2, 46, { f: "JBMono", c: "#1d1418", a: "center" }));
  ["+1 follower", "+1 follower", "+2 followers"].forEach((s, i) => ct("pill" + i, 400, 105, (g, w, h) => {
    panel(g, w, h, { bg: "#2fbf71", r: 52 });
    g.fillStyle = "#fff"; g.beginPath(); g.arc(56, 42, 15, 0, 7); g.fill(); g.beginPath(); g.ellipse(56, 78, 26, 16, 0, Math.PI, 0); g.fill();
    write(g, s, 96, h / 2 + 2, 42, { w: 800, c: "#fff", max: w - 110 });
  }));
  ct("reel", 460, 780, (g, w, h) => {
    panel(g, w, h, { r: 30 }); thumb(g, 20, 20, w - 40, 600, 0);
    g.fillStyle = "rgba(29,20,24,.7)"; rr(g, 40, 40, 120, 48, 24); g.fill(); write(g, "▶ Reel", 100, 65, 26, { w: 700, c: "#fff", a: "center" });
    write(g, "Posted", 34, 690, 40, { w: 800 }); g.fillStyle = "#e9f8ef"; rr(g, 280, 660, 150, 60, 30); g.fill(); tick(g, 312, 690, 26); write(g, "done", 340, 691, 30, { w: 700, c: "#2fbf71" });
  });
  ct("reelStrike", 460, 780, (g, w, h) => {
    g.drawImage(TX.reel.image, 0, 0); g.fillStyle = "rgba(255,250,245,.45)"; g.fillRect(0, 0, w, h);
    g.save(); g.translate(w / 2, 380); g.rotate(-.18);
    g.strokeStyle = "#e5484d"; g.lineWidth = 9; rr(g, -200, -62, 400, 124, 20); g.stroke();
    write(g, "JUST POSTING", 0, -14, 50, { w: 900, c: "#e5484d", a: "center" }); write(g, "✕  not growing", 0, 38, 32, { w: 700, c: "#e5484d", a: "center" });
    g.restore();
  });
  const ICON = [
    (g, c) => { g.strokeStyle = c; g.lineWidth = 12; for (const r of [26, 52, 78]) { g.beginPath(); g.arc(128, 128, r, -2.4, -.75); g.stroke(); } g.fillStyle = c; g.beginPath(); g.arc(128, 128, 14, 0, 7); g.fill(); },
    (g, c) => { g.strokeStyle = c; g.lineWidth = 12; rr(g, 58, 70, 140, 116, 16); g.stroke(); g.beginPath(); g.moveTo(58, 104); g.lineTo(198, 104); g.stroke(); g.fillStyle = c; g.beginPath(); g.moveTo(112, 124); g.lineTo(150, 146); g.lineTo(112, 168); g.fill(); },
    (g, c) => { g.strokeStyle = c; g.lineWidth = 12; g.lineCap = "round"; for (const [y, l] of [[86, 120], [128, 96], [170, 70]]) { g.beginPath(); g.moveTo(64, y); g.lineTo(64 + l, y); g.stroke(); } g.save(); g.translate(176, 160); g.rotate(-.8); g.fillStyle = c; rr(g, -12, -46, 24, 70, 6); g.fill(); g.restore(); },
    (g, c) => { g.fillStyle = c; rr(g, 52, 62, 152, 104, 30); g.fill(); g.beginPath(); g.moveTo(84, 160); g.lineTo(74, 200); g.lineTo(122, 162); g.fill(); g.fillStyle = "#fffaf5"; for (const x of [92, 128, 164]) { g.beginPath(); g.arc(x, 114, 11, 0, 7); g.fill(); } },
    (g) => { write(g, "?", 128, 136, 170, { w: 900, c: "#f0a07c", a: "center" }); },
  ];
  ICON.forEach((f, i) => ct("icon" + i, 256, 256, (g, w, h) => {
    rr(g, 0, 0, w, h, 56); g.fillStyle = i === 4 ? "#1d1418" : "#fffaf5"; g.fill(); f(g, "#d97757");
    write(g, "0" + (i + 1), 214, 30, 26, { f: "JBMono", c: i === 4 ? "#f0a07c" : "#c9b4a6", a: "center" });
  }));
  ct("radarTitle", 900, 130, (g, w, h) => {
    panel(g, w, h, { bg: "rgba(29,20,24,.92)", r: 64 }); g.fillStyle = "#2fbf71"; g.beginPath(); g.arc(70, h / 2, 14, 0, 7); g.fill();
    write(g, "NICHE RADAR · LAST 24H · SCANNING", 104, h / 2 + 2, 40, { f: "JBMono", c: "#fffaf5" });
  });
  [["AI agents", .92, "#d97757"], ["Claude skills", .7, "#f0a07c"], ["Auto-DM setups", .48, "#e8cfb6"]].forEach(([s, f, c], i) => ct("trend" + i, 660, 200, (g, w, h) => {
    panel(g, w, h, { r: 46, line: i === 0 ? "#d97757" : null, lw: 6 });
    write(g, s, 40, 66, 52, { w: 800, max: 460 });
    g.fillStyle = "#f1e7dc"; rr(g, 40, 118, 470, 30, 15); g.fill(); g.fillStyle = c; rr(g, 40, 118, 470 * f, 30, 15); g.fill();
    write(g, "↑", 590, 100, 90, { w: 800, c: i < 2 ? "#2fbf71" : "#c9b4a6", a: "center" });
  }));
  ct("hot", 520, 140, (g, w, h) => {
    panel(g, w, h, { bg: "#d97757", r: 70 });
    g.fillStyle = "#ffbf47"; g.beginPath(); g.moveTo(70, 112); g.bezierCurveTo(30, 90, 40, 50, 70, 24); g.bezierCurveTo(74, 52, 100, 56, 98, 86); g.bezierCurveTo(98, 104, 86, 112, 70, 112); g.fill();
    write(g, "BLOWING UP", 290, h / 2 + 3, 58, { w: 900, c: "#fff", a: "center" });
  });
  ct("boardHead", 1100, 120, (g, w, h) => write(g, "SHOT LIST · VISUALS", 0, h / 2, 64, { f: "JBMono", c: "#1d1418" }));
  [["HOOK", "#d97757", "text pop"], ["PROOF", "#1d1418", "339 → 2,400"], ["LIST", "#f0a07c", "5 moves"], ["CTA", "#2fbf71", "comment"]].forEach(([s, c, d], i) => ct("frame" + i, 360, 620, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, c); gr.addColorStop(1, i === 1 ? "#4a2c30" : "#fffaf5");
    rr(g, 0, 0, w, h, 26); g.fillStyle = gr; g.fill();
    g.fillStyle = "rgba(255,255,255,.85)"; rr(g, 40, 230, w - 80, 120, 20); g.fill();
    write(g, d, w / 2, 290, 40, { w: 800, a: "center", max: w - 100 });
    write(g, "0" + (i + 1), 34, 50, 34, { f: "JBMono", c: "rgba(255,255,255,.9)" });
    write(g, s, w / 2, 560, 56, { w: 900, c: i === 1 ? "#fffaf5" : "#1d1418", a: "center" });
  }));
  ct("page", 1000, 1200, (g, w, h) => {
    panel(g, w, h, { r: 40 });
    g.fillStyle = "#ff5f57"; g.beginPath(); g.arc(60, 64, 14, 0, 7); g.fill(); g.fillStyle = "#febc2e"; g.beginPath(); g.arc(102, 64, 14, 0, 7); g.fill();
    g.fillStyle = "#28c840"; g.beginPath(); g.arc(144, 64, 14, 0, 7); g.fill();
    write(g, "script.md", 190, 66, 36, { f: "JBMono", c: "#8a7a72" });
    g.fillStyle = "#f1e7dc"; g.fillRect(40, 110, w - 80, 3);
  });
  const PL = [["HOOK:", " I turned Claude into an agent"], ["PROOF:", " 339 → 2,400 followers"], ["LIST:", " five moves, best one last"],
    ["SHOW:", " the room for every move"], ["CTA:", " comment AGENT"]];
  PL.forEach(([a, b], i) => ct("pl" + i, 840, 85, (g, w, h) => {
    write(g, a, 0, h / 2, 46, { f: "JBMono", c: "#d97757" }); const aw = g.measureText(a).width;
    write(g, b, aw, h / 2, 46, { w: 700 });
  }));
  ct("caption", 820, 300, (g, w, h) => {
    panel(g, w, h, { r: 40, line: "#d97757", lw: 6 }); write(g, "CAPTION", 40, 56, 30, { f: "JBMono", c: "#d97757" });
    write(g, "Steal my Claude setup.", 40, 124, 48, { w: 800, max: w - 80 }); write(g, "Comment AGENT below", 40, 184, 44, { w: 600, max: w - 80 });
    write(g, "#reels  #ai  #instagramgrowth", 40, 250, 34, { w: 600, c: "#3d8bff", max: w - 80 });
  });
  "AGENT".split("").forEach((ch, i) => ct("key" + i, 128, 128, (g, w, h) => write(g, ch, w / 2, h / 2 + 4, 92, { w: 800, c: i === 0 ? "#fff" : "#1d1418", a: "center" })));
  [["creator.sana", "how do I set this up??", "#8b6cf6"], ["tech.aman", "need this for my page", "#3d8bff"], ["neha.edits", "AGENT", "#2fbf71"]].forEach(([n, s, c], i) => ct("cm" + i, 980, 200, (g, w, h) => {
    panel(g, w, h, { r: 60 }); avatar(g, 100, h / 2, 54, c, n[0].toUpperCase());
    write(g, "@" + n, 180, 66, 34, { f: "JBMono", c: "#8a7a72" }); write(g, s, 180, 132, 50, { w: 800, max: w - 220 });
  }));
  ["Sent you the steps", "DM'd you the setup", "Check your DMs"].forEach((s, i) => ct("rp" + i, 780, 170, (g, w, h) => {
    panel(g, w, h, { bg: "#d97757", r: 56 }); write(g, "REPLIED", 44, 52, 28, { f: "JBMono", c: "#ffe3d6" });
    write(g, s, 44, 112, 48, { w: 800, c: "#fff", max: w - 150 }); g.fillStyle = "#fff"; g.beginPath(); g.arc(w - 70, h / 2, 40, 0, 7); g.fill(); tick(g, w - 70, h / 2 + 2, 40, "#d97757");
  }));
  ct("reelOld", 500, 880, (g, w, h) => {
    panel(g, w, h, { bg: "#241a22", r: 30 }); thumb(g, 20, 20, w - 40, 700, 7);
    g.fillStyle = "rgba(255,255,255,.12)"; rr(g, 40, 40, 170, 50, 25); g.fill(); write(g, "LAST REEL", 125, 66, 26, { f: "JBMono", c: "#f6ece2", a: "center" });
    write(g, "v1", 40, 800, 64, { w: 800, c: "#f6ece2" }); write(g, "results in", w - 40, 800, 32, { w: 600, c: "#f0a07c", a: "right" });
  });
  ct("reelNew", 500, 880, (g, w, h) => {
    panel(g, w, h, { bg: "#fffaf5", r: 30 }); thumb(g, 20, 20, w - 40, 700, 0);
    g.fillStyle = "rgba(255,255,255,.92)"; rr(g, 60, 300, w - 120, 130, 26); g.fill(); write(g, "NEXT REEL", w / 2, 345, 44, { w: 900, a: "center" });
    write(g, "rewritten", w / 2, 395, 40, { f: "ISerif", w: 400, i: true, c: "#d97757", a: "center" });
    write(g, "v2", 40, 800, 64, { w: 900, c: "#d97757" }); write(g, "↗", w - 60, 800, 70, { w: 800, c: "#2fbf71", a: "center" });
  });
  ["WATCH TIME", "SAVES", "FOLLOWS"].forEach((s, i) => ct("met" + i, 620, 170, (g, w, h) => {
    panel(g, w, h, { bg: "rgba(30,20,28,.95)", r: 40, line: "rgba(240,160,124,.45)", lw: 3 });
    write(g, s, 36, 58, 40, { f: "JBMono", c: "#f6ece2" }); g.fillStyle = "rgba(246,236,226,.12)"; rr(g, 36, 108, w - 72, 26, 13); g.fill();
  }));
  ["POST", "RESULTS", "REWRITE"].forEach((s, i) => ct("loop" + i, 340, 100, (g, w, h) => {
    panel(g, w, h, { bg: i === 2 ? "#d97757" : "#1d1418", r: 50 }); write(g, s, w / 2, h / 2 + 2, 40, { f: "JBMono", c: "#fff", a: "center" });
  }));
  ct("course", 920, 620, (g, w, h) => {
    panel(g, w, h, { r: 40 });
    write(g, "FREE COURSE", 56, 70, 32, { f: "JBMono", c: "#d97757" });
    write(g, "The Proven System", 56, 160, 76, { w: 800, max: w - 100 });
    write(g, "for", 56, 250, 76, { w: 800 }); write(g, "Viral Reels", 190, 254, 92, { f: "ISerif", w: 400, i: true, c: "#d97757" });
    g.fillStyle = "#f1e7dc"; g.fillRect(56, 470, w - 112, 3);
    write(g, "Course by", 56, 530, 32, { w: 500, c: "#8a7a72" }); write(g, "August Alvelund", 216, 530, 32, { w: 800 });
  });
  ct("free", 320, 120, (g, w, h) => {
    rr(g, 6, 6, w - 12, h - 12, 18); g.fillStyle = "rgba(233,248,239,.95)"; g.fill(); g.strokeStyle = "#2fbf71"; g.lineWidth = 8; g.stroke();
    write(g, "FREE", w / 2, h / 2 + 3, 74, { w: 900, c: "#2fbf71", a: "center" });
  });
  [["creator.sana", "AGENT"], ["tech.aman", "agent pls"], ["neha.edits", "AGENT"], ["j.reels", "AGENT!!"], ["studio.kai", "agent"], ["mira.makes", "AGENT"]].forEach(([n, s], i) =>
    ct("ag" + i, 500, 120, (g, w, h) => {
      panel(g, w, h, { r: 60 }); avatar(g, 60, h / 2, 38, ["#8b6cf6", "#3d8bff", "#2fbf71", "#d97757", "#ffbf47", "#e9a2a0"][i], n[0].toUpperCase());
      write(g, "@" + n, 116, 40, 24, { f: "JBMono", c: "#8a7a72" }); write(g, s, 116, 84, 40, { w: 800 });
    }));
  ct("dm", 780, 200, (g, w, h) => {
    panel(g, w, h, { r: 56 }); g.fillStyle = "#1d1418"; g.beginPath(); g.arc(100, h / 2, 60, 0, 7); g.fill();
    sparkGlyph(g, 100, h / 2, 34, "#d97757");
    write(g, "ai.nxtlvl · now", 190, 66, 30, { f: "JBMono", c: "#8a7a72" }); write(g, "My setup + the course", 190, 130, 46, { w: 800, max: w - 300 });
    g.fillStyle = "#2fbf71"; rr(g, w - 120, h / 2 - 30, 92, 60, 30); g.fill(); write(g, "sent", w - 74, h / 2 + 2, 28, { w: 800, c: "#fff", a: "center" });
  });
  // the glass: a soft diagonal sheen across the screen
  glare.material.map = canvasTex(256, 512, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, "rgba(255,255,255,0)"); gr.addColorStop(.42, "rgba(255,255,255,0)");
    gr.addColorStop(.5, "rgba(255,255,255,.22)"); gr.addColorStop(.6, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
  });
  glare.material.needsUpdate = true;
  for (const [m, k] of FACES) { m.material.map = TX[k]; m.material.needsUpdate = true; }
  for (const d of DRUMS) { d.map = TX.digits.clone(); d.map.wrapS = THREE.RepeatWrapping; d.map.needsUpdate = true; d.needsUpdate = true; }
}

// ---------------------------------------------------------------- Claude: where it is, and what it does
const CLK = [                                         // [time, position, scale, blend]
  [0, V(0, 1.15, .06), 0], [T.claude - .02, V(0, 1.15, .08), .05], [T.claude + .28, V(.46, 1.98, .52), .42, .3],
  [L[1] + .1, V(.72, 2.25, .45), .38, .4], [L[2] - .05, V(-.55, 1.78, .7), .36, .35], [T.grows + .1, V(.58, 1.95, .62), .36, .35],
  [L[3] + .05, V(0, 2.12, .55), .34, .3], [T.last - .05, V(.6, 1.98, .7), .34, .3], [T.in0 - .3, V(0, 1.15, .3), .2, .3],
  [T.in0, I(.95, 1.25, .9), .4, .001], [L[5] - .15, I(-2.55, 1.0, -4.3), .4, .25], [L[6] - .15, I(2.62, .95, -8.4), .38, .25],
  [L[7] - .15, I(.78, .72, -13.3), .38, .25], [T.dark0, I(LAB.x + .72, 1.62, LAB.z + .35), .38, .001],
  [T.rewrites - .1, I(LAB.x + .6, 1.75, LAB.z + .45), .38, .3],
  [T.out1, V(.58, 2.05, .8), .36, .001], [L[11] - .1, V(.56, 2.12, .55), .36, .35],
].map((k) => ({ t: k[0], p: Array.isArray(k[1]) ? V(...k[1]) : k[1], s: k[2], d: k[3] || .3 }));
function clAt(t) {
  let i = 0; for (let j = 0; j < CLK.length; j++) if (t >= CLK[j].t) i = j;
  const a = CLK[Math.max(0, i - 1)], b = CLK[i];
  const k = i === 0 ? 1 : easeIO(clamp((t - b.t) / b.d));
  return { p: a.p.clone().lerp(b.p, k), s: lerp(a.s, b.s, k) };
}
function animClaude(t) {
  const { p, s } = clAt(t);
  const bob = Math.sin(t * 2.4) * .025;
  cl.root.position.set(p.x, p.y + bob, p.z);
  show(cl.root, s * (1 + pulse(t, T.claude + .25, .06, .3) * .25 + pulse(t, T.followers, .05, .3) * .15 + pulse(t, T.next, .05, .3) * .15));
  cl.root.lookAt(camera.position.x, camera.position.y, camera.position.z);
  cl.body.rotation.z = Math.sin(t * 1.6) * .12 + (t > L[11] ? Math.sin(t * 9) * .18 : 0);
  cl.rs.forEach((r, i) => { r.piv.rotation.z = r.base + Math.sin(t * 3 + i) * .05; r.r.scale.y = 1 + Math.sin(t * 6 + i * 1.7) * .08; });
  const blink = ((t + .3) % 2.9) < .1;
  const happy = between(t, T.followers, T.followers + 1) || t > L[10];
  cl.eyes.forEach((e) => { e.open.visible = !(blink || happy); e.shut.visible = blink || happy; });
  cl.mouthO.visible = between(t, T.claude, T.claude + .8) || between(t, T.five5, T.five5 + .6) || between(t, T.next, T.next + .6);
  cl.smile.visible = !cl.mouthO.visible;
  const dark = between(t, T.dark0, T.out1);
  coralLight.position.copy(cl.root.position); coralLight.intensity = cl.root.visible ? (dark ? 5 : 1.2) : 0;
  cl.halo.material.color.set(CORAL_L).multiplyScalar(dark ? .45 : .2);
}

// ---------------------------------------------------------------- the outside at work
function animOutside(t) {
  // the phone spins in and lands at .38 s, then floats; it leans back for the dive
  const k = easeOut(win(t, 0, .38));
  const sq = pulse(t, .38, .02, .25);
  phone.position.set(lerp(.55, 0, k), lerp(.8, 1.15, k) + Math.sin(t * 1.3) * .012, lerp(-2.4, 0, k));
  phone.rotation.set(lerp(-.6, 0, k) + Math.sin(t * .9) * .02, lerp(-3.4, 0, k) + Math.sin(t * .7) * .035, lerp(.5, 0, k));
  phone.scale.set(1 + sq * .03, 1 - sq * .04, 1);
  // what the screen shows
  const v1 = lerp(339, 2400, easeIO(win(t, T.twenty - .2, T.followers + .1)));
  if (t < T.in0) drawScreen(`p|${fmt(v1)}|${between(t, T.grows - .05, L[3] + .2) ? "nogrid" : ""}`);
  else if (t < L[11] - .1) drawScreen("p|2,400|");
  else {
    const typed = "AGENT".slice(0, clamp(Math.floor((t - T.agentcta + .06) / .075) + 1, 0, 5));
    drawScreen(`c|${t < T.agentcta - .06 ? "" : typed}|${t > T.agentcta + .5 ? "sent" : ""}`);
  }
  screenGlow.material.color.set(0xffd9c2).multiplyScalar(.12 + pulse(t, T.claude, .05, .5) * .5);
  // Claude's burst: the shockwave
  const sw = win(t, T.claude, T.claude + .55);
  shock.visible = sw > 0 && sw < 1; shock.position.set(0, 1.15, .1 + sw * .3); shock.scale.setScalar(.3 + easeOut(sw) * 3.2);
  shock.material.color.set(CORAL_L).multiplyScalar(1.4 * (1 - sw));
  // odometer 1
  const o1 = backOut(win(t, L[1] - .15, L[1] + .2), 1.8) * (1 - easeIn(win(t, L[2] - .15, L[2] + .05)));
  show(odo1.g, o1 * (1 + pulse(t, T.followers, .05, .3) * .12));
  odo1.g.rotation.y = Math.sin(t * .8) * .1; odo1.g.position.y = 2.3 + Math.sin(t * 1.7) * .015;
  setOdo(odo1, t < T.twenty - .2 ? 339 : v1);
  burst(confA, t, T.followers, V(0, 2.3, .35));
  // the follows streaming past the lens
  PILLS.forEach((p) => {
    const dt = t - p.t0, life = 1.2;
    if (dt < 0 || dt > life || t > L[2]) { p.c.visible = false; return; }
    const k2 = dt / life;
    p.c.visible = true;
    p.c.position.set(p.sx + p.dx * k2 * 1.3, p.sy + p.dy * k2, .1 + easeIn(k2) * 1.9 + k2 * .4);
    p.c.quaternion.copy(camera.quaternion);
    p.c.scale.setScalar(Math.max(.001, backOut(win(dt, 0, .18), 2) * (.7 + k2 * .5)));
  });
  // the post: out of the screen, stamped, dropped
  const ra = L[2] - .05, rk = backOut(win(t, ra, ra + .3), 1.6), fall = easeIn(win(t, T.post + .3, T.post + .65));
  reel.visible = t > ra && t < T.post + .7;
  if (reel.visible) {
    reel.position.set(lerp(0, -.2, rk) - fall * 1.4, lerp(1.15, 1.48, rk) - fall * 1.2, lerp(.05, .55, rk));
    reel.rotation.set(0, lerp(0, .28, rk), fall * 2.2 + pulse(t, T.post, .03, .2) * .08);
    reel.scale.setScalar(Math.max(.001, lerp(.4, .8, rk) * (1 + pulse(t, T.post, .03, .2) * .08)));
    reel.userData.face.material.map = t < T.post ? TX.reel : TX.reelStrike;
  }
  // the page grows: tiles rise out of the grid, the green arrow climbs
  tiles.forEach((tl, i) => {
    const a = T.grows - .05 + (tl.k + (2 - tl.r)) * .07;
    const up = easeOut(win(t, a, a + .35)) * (1 - easeIn(win(t, L[3] + .05, L[3] + .3)));
    tl.m.visible = up > .002;
    tl.m.scale.set(1, 1, Math.max(.001, up * TILE_H[i] * (1 + pulse(t, T.page, .05, .3) * .25)));
  });
  const ar = easeOut(win(t, T.grows + .1, T.grows + .6)) * (1 - easeIn(win(t, L[3] + .05, L[3] + .25)));
  arrow.visible = ar > .002; arrow.position.set(.12, -.45 + ar * .3, .8); arrow.rotation.z = -.55; arrow.scale.setScalar(Math.max(.001, ar * .7));
  // five icons; the fifth leads the dive
  ICONS.forEach((g, i) => {
    const a = L[3] + i * .07, pk = backOut(win(t, a, a + .28), 2);
    const focus = easeIO(win(t, T.last - .05, T.last + .35));
    const dive = easeIn(win(t, T.in0 - .38, T.in0));
    const x0 = (i - 2) * .32, y0 = 1.62 - Math.pow(i - 2, 2) * .035;
    g.visible = t > a && t < T.in0 + .02;
    if (!g.visible) return;
    if (i < 4) {
      g.position.set(x0 * (1 + dive * 2.5), y0 - focus * .08 + dive * (i % 2 ? .6 : -.6), .55 - focus * .25);
      g.scale.setScalar(Math.max(.001, pk * (1 - focus * .25)));
      g.userData.f.material.color.setScalar(1 - focus * .45);
    } else {
      const p0 = V(x0, y0, .55), p1 = V(0, 1.66, .72), p2 = V(0, 1.15, .06);
      const p = p0.clone().lerp(p1, focus).lerp(p2, dive);
      g.position.copy(p);
      g.scale.setScalar(Math.max(.001, pk * (1 + focus * .3 + pulse(t, T.smartest, .05, .3) * .25) * (1 - dive * .7)));
      g.userData.h.material.color.set(TERRA).multiplyScalar(focus * (.5 + .25 * Math.sin(t * 14)));
    }
    g.rotation.set(Math.sin(t * 1.3 + i) * .08, Math.sin(t * 1.1 + i * 2) * .15, 0);
  });
  // the bonus: the gift drops, the lid pops on "free", the course rises; odometer 2 rolls to 16,000
  const gd = backOut(win(t, L[10] - .05, L[10] + .25), 2.2), lidk = easeOut(win(t, T.free - .04, T.free + .45)), gaway = easeIn(win(t, T.sixteen - .45, T.sixteen - .1));
  gift.visible = t > L[10] - .1 && gaway < 1 && t < L[11];
  gift.position.set(0, lerp(2.8, 1.45, gd) - gaway * 1.5, .62); gift.rotation.set(.18, Math.sin(t * 1.2) * .1 - .25, 0);
  gift.scale.setScalar(Math.max(.001, 1 - gaway * .5));
  lid.position.set(lidk * .5, .2 + lidk * 1.3, lidk * .2); lid.rotation.set(-lidk * 1.2, lidk * 2, lidk * .8);
  burst(confB, t, T.free, V(0, 1.45, .7), 1.2);
  const ck = backOut(win(t, T.free + .05, T.free + .45), 1.6) * (1 - easeIn(win(t, L[11] - .2, L[11] + .05)));
  course.visible = ck > .002 && t > L[10]; course.scale.setScalar(Math.max(.001, ck * .64));
  course.position.set(0, lerp(1.3, 1.92, easeOut(win(t, T.free + .05, T.free + .5))), .75); course.rotation.set(-.05, Math.sin(t * .9) * .06, 0);
  show(freeStamp, backOut(win(t, T.course - .1, T.course + .15), 3) * (1 + pulse(t, T.course + .05, .04, .2) * .3));
  const o2 = backOut(win(t, T.sixteen - .3, T.sixteen), 1.8) * (1 - easeIn(win(t, L[11] - .2, L[11] + .05)));
  odo2.g.visible = o2 > .002 && t > L[10]; odo2.g.scale.setScalar(Math.max(.001, o2 * .56 * (1 + pulse(t, T.downloads, .05, .3) * .1)));
  setOdo(odo2, lerp(0, 16000, easeOut(win(t, T.sixteen - .1, T.downloads))));
  // the CTA: the swarm of AGENT comments, the DM
  SWARM.forEach((s, i) => {
    const dt = t - s.t0;
    if (dt < 0) { s.c.visible = false; return; }
    s.c.visible = true;
    s.c.position.set(s.x + Math.sin(dt * 2 + i) * .05, .25 + dt * s.sp, s.z);
    s.c.quaternion.copy(camera.quaternion);
    s.c.scale.setScalar(Math.max(.001, backOut(win(dt, 0, .25), 2) * (1 - win(s.c.position.y, 2.4, 2.9))));
  });
  const dk = backOut(win(t, T.setup - .1, T.setup + .25), 1.8);
  dm.visible = dk > .002; dm.scale.setScalar(Math.max(.001, dk)); dm.position.set(0, lerp(2.0, 1.5, dk), .42); dm.quaternion.copy(camera.quaternion);
}

// ---------------------------------------------------------------- the inside at work
function animInside(t) {
  DECO.forEach((d, i) => { d.m.position.y = d.y + Math.sin(t * .9 + d.ph) * .12; d.m.rotation.y += 0; d.m.rotation.x = d.ph + t * d.rs; d.m.rotation.z = d.ph * .5 + t * d.rs * .6; });
  // move 1: the sweep spins; each trend pops as it passes; the hot one shoots up on "blowing"
  sweepG.rotation.y = -t * 3.2;
  TRENDS.forEach((c, i) => {
    const a = L[4] + .05 + i * .28;
    show(c, backOut(win(t, a, a + .25), 2.2) * (1 + (i === 0 ? pulse(t, T.blowing, .05, .3) * .12 : 0)));
  });
  const hb = easeOut(win(t, T.blowing - .1, T.blowing + .35));
  hotBar.visible = hb > .002; hotBar.scale.set(1, Math.max(.001, hb * 1.1), 1);
  show(hotBadge, backOut(win(t, T.blowing + .05, T.blowing + .3), 2.4));
  hotBadge.quaternion.copy(camera.quaternion);
  FLAME.forEach((f, i) => {
    const ph = ((t * 1.4 + hash(i)) % 1);
    f.visible = hb > .5; f.position.set(-.3 + (hash(i + 3) - .5) * .18, .07 + hb * 1.1 + ph * .4, .32 + (hash(i + 5) - .5) * .1);
    f.scale.setScalar(1 - ph); f.quaternion.copy(camera.quaternion);
  });
  show(radarTitle, backOut(win(t, T.in0 + .05, T.in0 + .3), 2)); radarTitle.quaternion.copy(camera.quaternion);
  // move 2: the frames fly in and snap; the palette pops on "visuals"
  FRAMES.forEach((c, i) => {
    const a = L[5] - .05 + i * .12, k = easeOut(win(t, a, a + .28));
    const home = V(-.21 + (i % 2) * .42, .26 - Math.floor(i / 2) * .68, .02), from = V(home.x * 3 + (i % 2 ? 1.2 : -1.2), home.y + (i % 2 ? 1.5 : -1.2), 1.4);
    c.visible = t > a;
    c.position.copy(from.clone().lerp(home, k));
    c.rotation.set(0, 0, (1 - k) * (i % 2 ? .9 : -.9));
    c.scale.setScalar(Math.max(.001, .6 + .4 * k + pulse(t, a + .28, .03, .15) * .06));
  });
  SWATCH.forEach((m, i) => { const a = T.visuals - .05 + i * .06; show(m, backOut(win(t, a, a + .22), 2.6)); m.rotation.y = 0; });
  show(boardHead, backOut(win(t, L[5] - .2, L[5] + .05), 2));
  // move 3: the lines type in; the keys press; the caption pops on "caption"
  const ty0 = L[6] - .05;
  PLINES.forEach((m, i) => {
    const k = win(t, ty0 + i * .27, ty0 + i * .27 + .3);
    m.visible = k > 0; m.scale.x = Math.max(.001, k); if (m.material.map) { m.material.map.repeat.x = Math.max(.001, k); }
  });
  const cur = clamp(Math.floor((t - ty0) / .27), 0, 4), ck = win(t, ty0 + cur * .27, ty0 + cur * .27 + .3);
  caret.position.set(-.42 + .84 * ck + .01, .3 - cur * .13, .018); caret.visible = Math.floor(t * 4) % 2 === 0 || ck < 1;
  KEYS.forEach((g, i) => {
    const pr = pulse(t, ty0 + i * .25, .04, .14);
    g.position.y = -.82 - pr * .03; g.children[0].material.emissive = new THREE.Color(TERRA); g.children[0].material.emissiveIntensity = pr * .6;
  });
  const cpk = backOut(win(t, T.caption - .08, T.caption + .2), 2);
  capCard.visible = cpk > .002; capCard.scale.setScalar(Math.max(.001, cpk));
  // move 4: comments fly in; replies snap in beside them, a paper plane each
  CMS.forEach(({ c, r }, i) => {
    const a = L[7] - .05 + i * .16, k = backOut(win(t, a, a + .3), 1.8);
    c.visible = t > a; c.position.z = lerp(-2.2, 0, Math.min(1, k)); c.scale.setScalar(Math.max(.001, .7 + .3 * k));
    const b = T.replies - .05 + i * .22, rk = backOut(win(t, b, b + .25), 2);
    r.visible = t > b; r.position.x = lerp(1.6, .3, Math.min(1, rk)); r.scale.setScalar(Math.max(.001, rk));
    const pl = PLANES[i], pk = win(t, b + .05, b + .45);
    pl.visible = pk > 0 && pk < 1; pl.position.set(lerp(.7, -.55, pk), .45 - i * .5 + Math.sin(pk * Math.PI) * .25, .3);
  });
  // move 5: the lab
  const lit = t > T.five5 - .03 ? 1 - .35 * pulse(t, T.five5 + .06, .02, .05) - .3 * pulse(t, T.five5 + .16, .02, .05) : 0;
  spot.intensity = 70 * lit; spot.position.set(LAB.x, 4.2, LAB.z + IN_Z + 1.2); spot.target.position.set(LAB.x, .9, LAB.z + IN_Z);
  oldReel.visible = t < T.rewrites + .02;
  oldReel.rotation.y = Math.sin(t * .8) * .12; oldReel.position.y = 1.12 + Math.sin(t * 1.4) * .01;
  const sc = between(t, T.studies - .1, T.rewrites);
  scanRing.visible = sc; scanDisc.visible = sc;
  const sy = .66 + (.5 - .5 * Math.cos((t - T.studies) * 4.2)) * .94;
  scanRing.position.set(0, sy, 0); scanDisc.position.set(0, sy, 0);
  METRICS.forEach((m, i) => {
    const a = T.studies + .05 + i * .22;
    show(m.c, backOut(win(t, a, a + .25), 2) * (1 - easeIn(win(t, T.rewrites - .1, T.rewrites + .1))));
    m.bar.scale.x = Math.max(.001, easeOut(win(t, a + .15, a + .9)) * m.fill);
  });
  DATA.forEach((d, i) => {
    const ph = ((t - T.studies) * .9 + hash(i)) % 1;
    d.visible = between(t, T.studies + .3, T.rewrites);
    const from = V(-.1 + (hash(i + 2) - .5) * .3, .8 + hash(i + 4) * .7, .05), to = V(.72, 1.62, .35);
    d.position.copy(from.lerp(to, easeIn(ph))); d.scale.setScalar(1 - ph * .6); d.quaternion.copy(camera.quaternion);
  });
  // rewrites: the old reel breaks into tiles that fly apart and come back together as v2
  const ex = easeOut(win(t, T.rewrites, T.rewrites + .3)), co = easeIO(win(t, T.rewrites + .3, T.next - .02));
  shards.visible = between(t, T.rewrites, T.next + .02);
  if (shards.visible) {
    for (let i = 0; i < SH_N; i++) {
      const r = Math.floor(i / SH_C), k = i % SH_C;
      const home = V((k - (SH_C - 1) / 2) * .068, 1.12 + ((SH_R - 1) / 2 - r) * .07, .02);
      const away = home.clone().add(V((hash(i) - .5) * 1.8, (hash(i + 1) - .5) * 1.4, hash(i + 2) * 1.1));
      tP.copy(home.clone().lerp(away, ex * (1 - co)));
      tE.set((hash(i + 3) - .5) * 6 * ex * (1 - co), (hash(i + 4) - .5) * 6 * ex * (1 - co), 0); tQ.setFromEuler(tE);
      tS.setScalar(1);
      shards.setMatrixAt(i, tM.compose(tP, tQ, tS));
    }
    shards.instanceMatrix.needsUpdate = true;
  }
  const nk = backOut(win(t, T.next - .05, T.next + .2), 1.8), launch = easeIn(win(t, T.out1 - .32, T.out1));
  newReel.visible = nk > .002;
  newReel.scale.setScalar(Math.max(.001, nk * (1 + pulse(t, T.next + .15, .05, .3) * .1)));
  newReel.position.set(0, 1.12 + launch * .25, launch * 1.6); newReel.rotation.set(0, Math.sin(t * 1.1) * .08 * (1 - launch), 0);
  newHalo.material.color.set(CORAL_L).multiplyScalar(nk * .28 * (1 + .3 * Math.sin(t * 9)));
  const lk = backOut(win(t, T.next + .05, T.next + .35), 2);
  loopG.visible = lk > .002 && launch < .5; loopG.scale.setScalar(Math.max(.001, lk)); loopG.rotation.set(1.25, 0, 0);
  loopRing.rotation.z = -(t - T.next) * 1.6;
  LOOP.forEach((c, i) => { const a = i / 3 * Math.PI * 2 + (t - T.next) * 1.6 + Math.PI / 2; c.position.set(Math.cos(a) * .48, Math.sin(a) * .48, 0); c.quaternion.copy(loopG.quaternion).invert().multiply(camera.quaternion); });
}

// ---------------------------------------------------------------- camera: one shot list, blended where a cut isn't hard
const SHOTS = [
  { a: 0, b: .42, p: [[.8, 1.75, 3.2], [.5, 1.62, 3.3]], q: [[0, 1.4, 0], [0, 1.42, 0]], fov: 42 },
  { a: .42, b: L[1], p: [[.5, 1.62, 3.3], [-.15, 1.7, 3.55]], q: [[0, 1.42, 0], [.05, 1.5, 0]], fov: 42 },
  { a: L[1], b: L[2] - .1, blend: .4, p: [[-1.05, 1.15, 2.95], [.95, 1.3, 2.9]], q: [[0, 1.95, 0], [0, 2.0, 0]], fov: 44 },
  { a: L[2] - .1, b: T.grows - .12, blend: .3, p: [[.45, 1.55, 2.6], [.25, 1.5, 2.4]], q: [[-.12, 1.35, .3], [-.18, 1.32, .3]], fov: 42 },
  { a: T.grows - .12, b: L[3] - .1, p: [[1.35, .8, 1.6], [1.05, .92, 1.38]], q: [[0, 1.22, .2], [0, 1.32, .2]], fov: 42 },
  { a: L[3] - .1, b: T.in0 - .4, p: [[0, 1.68, 3.05], [0, 1.64, 2.75]], q: [[0, 1.55, 0], [0, 1.52, 0]], fov: 42 },
  { a: T.in0 - .4, b: T.in0, ease: easeIn, p: [[0, 1.64, 2.75], [0, 1.15, .2]], q: [[0, 1.52, 0], [0, 1.15, 0]], fov: [42, 30] },
  { a: T.in0, b: L[5] - .14, ease: easeOut, p: [I(0, 3.0, 3.9), I(.05, 2.2, 2.35)], q: [I(0, .45, -.3), I(-.05, .62, -.1)], fov: 46 },
  { a: L[5] - .14, b: L[6] - .14, blend: .26, p: [I(-3.25, 1.4, -2.1), I(-3.42, 1.32, -2.4)], q: [I(-3.5, 1.28, -5), I(-3.5, 1.25, -5)], fov: 44 },
  { a: L[6] - .14, b: L[7] - .14, blend: .26, p: [I(3.05, 1.45, -6.25), I(3.28, 1.38, -6.5)], q: [I(3.5, 1.3, -9), I(3.5, 1.28, -9)], fov: 44 },
  { a: L[7] - .14, b: T.dark0, blend: .26, p: [I(-.2, 1.55, -11.15), I(0, 1.5, -11.45)], q: [I(0, 1.48, -14), I(0, 1.46, -14)], fov: 44 },
  { a: T.dark0, b: T.rewrites - .1, p: [I(LAB.x + .5, 1.6, LAB.z + 2.9), I(LAB.x + .18, 1.45, LAB.z + 2.0)], q: [I(LAB.x, 1.18, LAB.z), I(LAB.x, 1.2, LAB.z)], fov: 40 },
  { a: T.rewrites - .1, b: T.out1, blend: .3, p: [I(LAB.x - .55, 1.3, LAB.z + 1.95), I(LAB.x - .2, 1.35, LAB.z + 2.25)], q: [I(LAB.x, 1.2, LAB.z), I(LAB.x, 1.25, LAB.z + .3)], fov: 42 },
  { a: T.out1, b: T.out1 + .8, ease: easeOut, p: [[0, 1.5, 1.2], [0, 1.62, 2.95]], q: [[0, 1.5, 0], [0, 1.7, 0]], fov: [34, 42] },
  { a: T.out1 + .8, b: L[11] - .12, p: [[0, 1.62, 2.95], [0, 1.64, 3.2]], q: [[0, 1.7, 0], [0, 1.7, 0]], fov: 42 },
  { a: L[11] - .12, b: T.end, blend: .35, p: [[0, 1.5, 3.45], [0, 1.52, 3.75]], q: [[0, 1.5, 0], [0, 1.52, 0]], fov: 42 },
];
function evalShot(s, t) {
  const k = (s.ease || easeIO)(win(t, s.a, s.b));
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
const HITS = () => [[.38, 1], [T.claude, .9], [T.followers, .6], [T.post, .5], [T.grows, .4], [T.smartest, .4], [T.in0, 1.2], [T.blowing, .5],
  [T.five5, .8], [T.rewrites, .9], [T.next, .5], [T.out1, 1.1], [T.free, .6], [T.downloads, .4], [T.agentcta, .5]];
let HIT_LIST = null;
function hitsAt(t) { HIT_LIST = HIT_LIST || HITS(); return HIT_LIST.reduce((a, [at_, g]) => a + pulse(t, at_, .02, .35) * g, 0); }

// ---------------------------------------------------------------- render
function renderAt(t) {
  const inPhone = between(t, T.in0, T.out1), dark = between(t, T.dark0, T.out1);
  const [p, q, fov] = shot(t);
  const hits = hitsAt(t), hand = dark ? .006 : .01;
  camera.position.set(p[0] + Math.sin(t * 1.9) * hand + Math.sin(t * 91) * .02 * hits, p[1] + Math.cos(t * 1.6) * hand + Math.cos(t * 77) * .02 * hits, p[2]);
  camera.lookAt(q[0], q[1], q[2]);
  camera.rotateZ(Math.sin(t * .7) * .012 + Math.sin(t * 61) * .008 * hits);
  // whip moves between the rooms: a snap of FOV on each
  const snaps = [L[5] - .14, L[6] - .14, L[7] - .14, T.grows - .12, L[3] - .1, L[2] - .1];
  const snap = snaps.reduce((a, c) => a + (t >= c ? (1 - easeOut(win(t, c, c + .3))) * 8 : 0), 0);
  camera.fov = fov + snap + pulse(t, T.in0, .02, .5) * 14 - pulse(t, T.out1, .02, .5) * -10;
  camera.updateProjectionMatrix(); camera.updateMatrixWorld();
  outside.visible = !inPhone; inside.visible = inPhone;
  lab.visible = dark; radar.visible = boardG.visible = deskG.visible = roomG.visible = inPhone && !dark;
  // light and air for each world
  const bg = dark ? BG_DARK : inPhone ? BG_IN : BG_OUT;
  scene.background.copy(bg); scene.fog.color.copy(bg);
  scene.fog.near = dark ? 3 : inPhone ? 5 : 7; scene.fog.far = dark ? 11 : inPhone ? 19 : 24;
  hemi.intensity = dark ? .06 : 1.15; key.intensity = dark ? 0 : 2.3; fill.intensity = dark ? 0 : .55; scene.environmentIntensity = dark ? .12 : .55;
  const focus = V(q[0], 0, q[2]);
  key.target.position.copy(focus); key.position.copy(focus).add(V(-2.2, 5, 3.6)); key.target.updateMatrixWorld();
  if (inPhone) animInside(t);
  if (!inPhone) animOutside(t);
  animClaude(t);
  // dust in the light
  for (let i = 0; i < DUST_N; i++) {
    const ph = hash(i * 1.7) * 50;
    tP.set(p[0] + ((hash(i) * 6 + t * .05 * (hash(i + 2) - .5)) % 6) - 3, p[1] - 1.5 + ((hash(i + 1) * 4 + t * .08 + ph) % 4), p[2] - .5 - hash(i + 3) * 5);
    tS.setScalar(.6 + hash(i + 4) * 1.4);
    dust.setMatrixAt(i, tM.compose(tP, camera.quaternion, tS));
  }
  dust.instanceMatrix.needsUpdate = true;
  dust.material.color.set(dark ? CORAL_L : 0xfff0e0).multiplyScalar(dark ? .55 : .35);
  fx.position.copy(camera.position).add(V(0, .5, -1)); fx.intensity = hits * 4;
  // the grade: warm and clean outside and in, deep in the lab
  const g = grade.uniforms;
  g.uTime.value = Math.round(t * 30) / 30;
  g.uTint.value.set(dark ? 1.04 : 1.0, dark ? .97 : 1.0, dark ? 1.02 : .98);
  g.uGrain.value = dark ? .05 : .03;
  g.uVig.value = dark ? .9 : .28;
  g.uChroma.value = hits * 1.1 + pulse(t, T.in0, .02, .4) * 2 + pulse(t, T.out1, .02, .4) * 2;
  bloom.strength = dark ? .55 : .32; bloom.threshold = dark ? .92 : 1.05;
  composer.render();
}

const ready = (async () => {
  await Promise.all(["800 90px Montserrat", "700 30px Montserrat", "500 30px Montserrat", "900 30px Montserrat", "700 34px JBMono", "italic 400 60px ISerif"].map((f) => document.fonts.load(f)));
  drawTextures();
  drawScreen("p|339|");
  renderer.compile(scene, camera);
  renderAt(window.__hfThreeTime || 0);
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["gaworld"] = ready;
window.addEventListener("hf-seek", (e) => { if (TX.badge) renderAt(e.detail.time); });
