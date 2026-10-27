// Instagram Growth Agent reel: the 3D world. Everything is a pure function of time t (seconds), rendered on HyperFrames'
// hf-seek. Story (Option A, "inside the phone"), built to keep the camera travelling through things:
//   HOOK      an FPV flight down a tunnel of reels, hearts and comments behind Claude, out through the phone's screen
//   FOLLOWERS a vortex of follower avatars pours into the phone while the camera orbits through it; the odometer rolls
//             339 -> 2,400
//   POST      bullet time round the post as it is stamped "just posting"
//   GROWS     the phone falls flat and its grid shoots up as a city; the camera dives between the towers
//   FIVE      a wheel of the five moves spins in 3D and stops on the dark fifth one; the camera dives into it
//   MOVE 1    a swoop over a landscape of reels, a radar beam sweeping it; the trending ones launch up as columns
//   MOVE 2    a flight down a corridor of storyboard frames that flip to the lens; four snap into the shot list
//   MOVE 3    skimming a giant keyboard rippling with keystrokes, rising to the script as it types
//   MOVE 4    a storm of comments flying at the lens, Claude's replies shooting back
//   MOVE 5    the lights go out: the camera orbits the last reel as it is scanned, breaks apart past the lens, comes back v2
//   CTA       back out through the screen: AGENT typed into the comments, a sky full of AGENT comments, the DM
// Cue times come from the voice (window.GA_T, written by build/generate.py).
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";

const T = window.GA_T;
const L = T.l;
const W = 1080, H = 1920;
const IN_Z = -100, TUN_Z = -200;                     // the world inside the phone, and the hook's tunnel

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
const BG_OUT = new THREE.Color(0xf2e8dc), BG_IN = new THREE.Color(0xefcdb7), BG_DARK = new THREE.Color(0x0b0710), BG_TUN = new THREE.Color(0x2a1216);
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
const linear = (k) => k;
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
const tM = new THREE.Matrix4(), tP = new THREE.Vector3(), tQ = new THREE.Quaternion(), tS = new THREE.Vector3(), tE = new THREE.Euler(), tC = new THREE.Color();
const ZERO = new THREE.Matrix4().makeScale(0, 0, 0);
const FACES = [];                                    // [mesh, texture key], handed out once the fonts are in
const face = (m, k) => { FACES.push([m, k]); return m; };

// palette
const CREAM = 0xfaf4ec, TERRA = 0xd97757, CORAL_L = 0xf0a07c, PEACH = 0xf6c9a8, INK = 0x1d1418, GREEN = 0x2fbf71, GOLD = 0xffbf47,
  ROSE = 0xe9a2a0, SAND = 0xe8cfb6, LILAC = 0xb9a4f0;
const AVATAR = [0x8b6cf6, 0x3d8bff, GREEN, TERRA, GOLD, ROSE, CORAL_L, 0x5ad1c8];

// ---------------------------------------------------------------- lights
const hemi = new THREE.HemisphereLight(0xfff3e6, 0xd4b39c, 1.15); scene.add(hemi);
const key = new THREE.DirectionalLight(0xfff0e0, 2.3);
key.castShadow = true; key.shadow.mapSize.set(2048, 2048); key.shadow.radius = 5; key.shadow.bias = -.0004; key.shadow.normalBias = .02;
Object.assign(key.shadow.camera, { left: -3.5, right: 3.5, top: 3.5, bottom: -3.5, near: .5, far: 24 });
scene.add(key, key.target);
const fill = new THREE.DirectionalLight(0xffd6c2, .55); fill.position.set(4, 2, 3); scene.add(fill);
const spot = new THREE.SpotLight(0xffe7d2, 0, 14, .36, .55, 1.1);            // move five's one light
spot.castShadow = true; spot.shadow.mapSize.set(1024, 1024); spot.shadow.bias = -.0004; scene.add(spot, spot.target);
const coralLight = new THREE.PointLight(TERRA, 0, 4, 1.5); scene.add(coralLight);   // follows Claude
const portalLight = new THREE.PointLight(0xffe8d6, 0, 14, 1.3); scene.add(portalLight);
const fx = new THREE.PointLight(0xffe8d6, 0, 6, 1.4); scene.add(fx);                // flashes

// shared shapes: hearts, play buttons, pills, tiles, rings, balls
const heart = new THREE.Shape();
heart.moveTo(0, -.5); heart.bezierCurveTo(-.15, -.35, -.55, -.05, -.5, .2); heart.bezierCurveTo(-.45, .5, -.08, .52, 0, .25);
heart.bezierCurveTo(.08, .52, .45, .5, .5, .2); heart.bezierCurveTo(.55, -.05, .15, -.35, 0, -.5);
const heartGeo = new THREE.ExtrudeGeometry(heart, { depth: .18, bevelEnabled: true, bevelSize: .06, bevelThickness: .06, bevelSegments: 4, curveSegments: 18 }).center();
const play = new THREE.Shape(); play.moveTo(-.3, -.35); play.lineTo(.4, 0); play.lineTo(-.3, .35); play.closePath();
const playGeo = new THREE.ExtrudeGeometry(play, { depth: .12, bevelEnabled: true, bevelSize: .06, bevelThickness: .05, bevelSegments: 3 }).center();
const SHAPES = [heartGeo, new THREE.CapsuleGeometry(.18, .5, 6, 16).rotateZ(Math.PI / 2), playGeo, rb(.5, .5, .16, .12, 4),
  new THREE.TorusGeometry(.26, .09, 14, 32), new THREE.SphereGeometry(.24, 24, 16)];
const SHAPE_COL = [TERRA, CREAM, CORAL_L, PEACH, ROSE, 0xffffff, SAND, LILAC];
// floating UI shapes scattered round a centre, away from a clear zone; they bob and turn (parallax as the camera moves)
function decor(parent, n, place, seed = 0) {
  const out = [];
  for (let i = 0; i < n; i++) {
    const k = i + seed * 97;
    const m = mesh(SHAPES[k % SHAPES.length], phys(SHAPE_COL[(k * 3) % SHAPE_COL.length], { roughness: .45, clearcoat: .5 }), false, false);
    m.scale.setScalar(.5 + hash(k + 11) * .9);
    m.position.copy(place(i, k)); m.rotation.set(hash(k + 1) * 3, hash(k + 2) * 3, hash(k + 3) * 3);
    parent.add(m);
    out.push({ m, y: m.position.y, ph: hash(k + 13) * 6, rs: (hash(k + 21) - .5) * .8 });
  }
  return out;
}
const animDecor = (D, t) => D.forEach((d) => { d.m.position.y = d.y + Math.sin(t * .9 + d.ph) * .12; d.m.rotation.x = d.ph + t * d.rs; d.m.rotation.z = d.ph * .5 + t * d.rs * .6; });

// ---------------------------------------------------------------- the outside: a cream infinity studio, floating shapes and the phone
const outside = grp(scene);
const floorO = mesh(new THREE.PlaneGeometry(90, 90), std(0xefe2d3, { roughness: .95 }), false, true); floorO.rotation.x = -Math.PI / 2; outside.add(floorO);
const DECO_OUT = decor(outside, 44, (i, k) => {
  const a = Math.PI * .28 + hash(k + 5) * Math.PI * 1.44;                  // all round, except the camera's side
  const r = 3.6 + hash(k + 6) * 5;
  return V(Math.sin(a) * r, .4 + hash(k + 7) * 4.2, Math.cos(a) * r);
}, 1);
const PW = .78, PHH = 1.6, PD = .085, SCW = PW - .066, SCH = PHH - .066;
const phone = grp(outside, 0, 1.15, 0);
const phoneM = phys(0xd3a088, { metalness: .8, roughness: .28, clearcoat: .7, clearcoatRoughness: .2 });
phone.add(mesh(rb(PW, PHH, PD, .12, 5), phoneM));
phone.add(at(mesh(roundedPlane(PW - .024, PHH - .024, .11), std(0x0a090b, { roughness: .12 }), false, false), 0, 0, PD / 2 + .0006));
const SCR = document.createElement("canvas"); SCR.width = 720; SCR.height = 1552;
const screenTex = new THREE.CanvasTexture(SCR); screenTex.colorSpace = THREE.SRGBColorSpace; screenTex.anisotropy = 8;
const screen = new THREE.Mesh(roundedPlane(SCW, SCH, .088), new THREE.MeshBasicMaterial({ map: screenTex, toneMapped: false }));
screen.position.z = PD / 2 + .0015; phone.add(screen);
phone.add(at(mesh(rb(.2, .056, .004, .028, 2), std(0x050505, { roughness: .2 }), false, false), 0, SCH / 2 - .055, PD / 2 + .004));
for (const [x, y, h] of [[PW / 2 + .004, .32, .2], [-PW / 2 - .004, .42, .1], [-PW / 2 - .004, .24, .15]]) phone.add(at(mesh(rb(.012, h, .03, .006, 2), phoneM), x, y, 0));
const glare = new THREE.Mesh(roundedPlane(SCW, SCH, .088), new THREE.MeshBasicMaterial({ transparent: true, depthWrite: false, toneMapped: false, opacity: .5 }));
glare.position.z = PD / 2 + .0025; phone.add(glare);
const screenGlow = halo(2.6, 0xffd9c2, .0); screenGlow.position.z = -.08; phone.add(screenGlow);
const spx = (x, y) => V((x / 720 - .5) * SCW, (.5 - y / 1552) * SCH, PD / 2 + .002);    // screen px -> phone-local

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
// Claude's coral trail
const TRAIL_N = 26;
const trail = new THREE.InstancedMesh(new THREE.PlaneGeometry(.22, .22), add(CORAL_L, .7, { map: glowTex }), TRAIL_N); trail.frustumCulled = false; scene.add(trail);

// ---------------------------------------------------------------- the 3D odometer (339 -> 2,400)
// each drum is a cylinder lying on its side; its texture strip holds 0-9 and a blank (slot 10), and turning the drum is
// shifting the strip, so a number rolls the way a mechanical counter does; a mask leaves one digit per drum in view
const DRUMS = [];
function odometer(parent, n, commaAt) {
  const g = grp(parent);
  const R = .125, HD = .17, SP = .195;
  g.add(at(mesh(rb(n * SP + .16, .38, .2, .1, 4), std(INK, { roughness: .35, metalness: .2 })), 0, 0, -.07));
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
  const label = card(.62, .1, 1, null); label.position.set(0, -.29, .02); g.add(label);
  return { g, drums, n, comma, label, commaAt };
}
function setOdo(o, v) {
  v = Math.max(0, v);
  for (let i = 0; i < o.n; i++) {
    const p = o.n - 1 - i;                             // place: 0 = units
    const P = Math.pow(10, p);
    let s;
    if (p > 0 && v < P) s = 10;
    else s = Math.floor(v / P) % 10 + (p === 0 ? v % 1 : clamp((v % P) - (P - 1)));
    const tx = o.drums[i].map;
    if (tx) tx.offset.x = (s + .5) / 11;
  }
  o.comma.visible = v >= Math.pow(10, o.n - o.commaAt);
}

// ---------------------------------------------------------------- HOOK: the tunnel of content behind the screen
const tunnel = grp(scene, 0, 0, TUN_Z);
const TUN_RINGS = 24, TUN_STEP = 1.05, PORTAL_Z = -1.4 - TUN_RINGS * TUN_STEP;
const RINGS = [];
for (let r = 0; r < TUN_RINGS; r++) {
  const g = grp(tunnel, 0, 1.15, -1.2 - r * TUN_STEP);
  for (let j = 0; j < 9; j++) {
    const k = r * 9 + j, a = j / 9 * Math.PI * 2 + r * .41, rad = 1.2 + hash(k) * .7, kind = k % 7;
    let o;
    if (kind < 3) { o = card(.42, .7, 1, 0xfffaf5, .05); face(o.userData.face, "tc" + (k % 4)); }
    else if (kind === 3) { o = card(.6, .14, 1, 0xfffaf5, .06); face(o.userData.face, ["cm0", "cm1", "cm2", "pill0"][k % 4]); }
    else { o = mesh(SHAPES[[0, 2, 1, 0][kind - 3]], phys([TERRA, CORAL_L, ROSE, CREAM][k % 4], { roughness: .4, clearcoat: .6 }), false, false); o.scale.setScalar(.45 + hash(k + 3) * .3); }
    o.position.set(Math.cos(a) * rad, Math.sin(a) * rad, (hash(k + 7) - .5) * .6);
    o.rotation.set((hash(k + 8) - .5) * .5, (hash(k + 9) - .5) * .8, (hash(k + 10) - .5) * .6);
    g.add(o);
  }
  RINGS.push(g);
}
const portal = new THREE.Mesh(roundedPlane(1.5, 2.95, .2), glow(0xfff2e6, 1.8)); portal.position.set(0, 1.15, PORTAL_Z); tunnel.add(portal);
const portalHalo = halo(9, 0xffd9c2, .7); portalHalo.position.set(0, 1.15, PORTAL_Z + .05); tunnel.add(portalHalo);
const portalFrame = mesh(rb(1.66, 3.1, .08, .26, 4), phoneM); portalFrame.position.set(0, 1.15, PORTAL_Z - .05); tunnel.add(portalFrame);
const STREAK_N = 70;
const streaks = new THREE.InstancedMesh(new THREE.BoxGeometry(.01, .01, 1.4), add(0xffd9c2, .8), STREAK_N); streaks.frustumCulled = false; tunnel.add(streaks);

// ---------------------------------------------------------------- FOLLOWERS: the odometer, the vortex, the pills
const odo1 = odometer(outside, 4, 1); odo1.g.position.set(0, 2.3, .28); face(odo1.label.userData.face, "lblFollowers");
const GAL_N = 380;
const galaxy = new THREE.InstancedMesh(new THREE.SphereGeometry(.03, 12, 8), new THREE.MeshStandardMaterial({ roughness: .35, emissive: 0xffffff, emissiveIntensity: .08 }), GAL_N);
for (let i = 0; i < GAL_N; i++) galaxy.setColorAt(i, new THREE.Color(AVATAR[i % AVATAR.length]));
galaxy.instanceColor.needsUpdate = true; galaxy.frustumCulled = false; outside.add(galaxy);
const PILLS = [];
for (let i = 0; i < 14; i++) {
  const c = card(.4, .105, 1, 0xfffaf5, .05); outside.add(c); face(c.userData.face, "pill" + (i % 3)); c.visible = false;
  PILLS.push({ c, t0: L[1] + .1 + i * .24 + hash(i + 2) * .08, sx: (hash(i) - .5) * .5, sy: .55 + hash(i + 9) * 1.1, dx: (hash(i + 4) - .5) * 1.8, dy: (hash(i + 6) - .3) * .9 });
}
const CONF_N = 150;
function confetti(parent) {
  const m = new THREE.InstancedMesh(new THREE.PlaneGeometry(.035, .055), new THREE.MeshStandardMaterial({ side: THREE.DoubleSide, roughness: .5 }), CONF_N);
  const cols = [TERRA, CORAL_L, GOLD, CREAM, GREEN, PEACH, LILAC];
  for (let i = 0; i < CONF_N; i++) m.setColorAt(i, new THREE.Color(cols[i % cols.length]));
  m.instanceColor.needsUpdate = true; m.frustumCulled = false; parent.add(m);
  return m;
}
const confA = confetti(outside);
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
const shock = new THREE.Mesh(new THREE.RingGeometry(.3, .36, 64), add(CORAL_L, 1.4, { side: THREE.DoubleSide })); outside.add(shock);

// ---------------------------------------------------------------- POST and GROWS: the stamped post; the city out of the grid
const reel = card(.46, .78, 1, 0xfffaf5, .05); outside.add(reel); face(reel.userData.face, "reel");
const REEL_P = V(-.05, 1.55, 1.05);
const TILE_COL = [TERRA, PEACH, INK, CORAL_L, SAND, TERRA, ROSE, INK, CORAL_L];
const TILE_H = [.42, .62, .5, .74, .96, .8, .9, 1.18, 1.48];
const tiles = TILE_COL.map((c, i) => {
  const r = Math.floor(i / 3), k = i % 3;
  const m = mesh(rb(.218, .218, 1, .03, 3), std(c, { roughness: .45 })); m.geometry.translate(0, 0, .5);
  m.position.copy(spx(126 + k * 234, 958 + r * 234)); phone.add(m); m.visible = false;
  const win_ = mesh(new THREE.BoxGeometry(.222, .222, .012), glow(i % 3 === 1 ? GOLD : 0xfff2e6, 1.3), false, false); m.add(win_);
  return { m, r, k, win: win_ };
});
const arrowShape = new THREE.Shape();
arrowShape.moveTo(-.03, -.5); arrowShape.lineTo(.03, -.5); arrowShape.lineTo(.03, .32); arrowShape.lineTo(.1, .32); arrowShape.lineTo(0, .5);
arrowShape.lineTo(-.1, .32); arrowShape.lineTo(-.03, .32); arrowShape.closePath();
const arrow = mesh(new THREE.ExtrudeGeometry(arrowShape, { depth: .04, bevelEnabled: true, bevelSize: .012, bevelThickness: .012, bevelSegments: 2 }),
  phys(GREEN, { roughness: .3, clearcoat: 1, emissive: GREEN, emissiveIntensity: .25 }));
outside.add(arrow); arrow.visible = false;

// ---------------------------------------------------------------- FIVE: the wheel of moves
const WC = V(0, 1.78, 1.25);
const wheel = grp(outside, WC.x, WC.y, WC.z);
const wheelRing = new THREE.Mesh(new THREE.TorusGeometry(.5, .012, 10, 96), add(TERRA, 1.3)); wheel.add(wheelRing);
const ICONS = Array.from({ length: 5 }, (_, i) => {
  const g = grp(wheel);
  g.add(mesh(rb(.26, .26, .08, .07, 4), phys(i === 4 ? INK : 0xfffaf5, { roughness: .3, clearcoat: 1 })));
  const f = new THREE.Mesh(roundedPlane(.235, .235, .06), faceMat(1)); f.position.z = .0405; g.add(f); face(f, "icon" + i);
  const h = halo(.9, TERRA, 0); h.position.z = -.08; g.add(h);
  g.userData = { f, h };
  return g;
});
wheel.visible = false;

// ---------------------------------------------------------------- inside the phone: five worlds, side by side
const inside = grp(scene, 0, 0, IN_Z);
const floorI = mesh(new THREE.PlaneGeometry(400, 120), std(0xf0d6c3, { roughness: .9 }), false, true); floorI.rotation.x = -Math.PI / 2; floorI.position.x = 60; inside.add(floorI);
const M1 = V(0, 0, 0), M2 = V(30, 0, 0), M3 = V(60, 0, 0), M4 = V(90, 0, 0), LAB = V(120, 0, 0);
const wp = (o, x, y, z) => [o.x + x, o.y + y, o.z + z + IN_Z];              // a point in one of the worlds, as an array
// MOVE 1: a landscape of reels and a radar beam sweeping it
const field = grp(inside, M1.x, 0, M1.z);
const FC = 15, FR = 15, FIELD_N = FC * FR;
const fieldTiles = new THREE.InstancedMesh(rb(.3, .05, .46, .03, 2), new THREE.MeshStandardMaterial({ roughness: .4, emissive: 0xffffff, emissiveIntensity: 0 }), FIELD_N);
fieldTiles.frustumCulled = false; fieldTiles.receiveShadow = true; field.add(fieldTiles);
const FT = [];
for (let i = 0; i < FIELD_N; i++) {
  const c = i % FC, r = Math.floor(i / FC);
  const x = (c - (FC - 1) / 2) * .4, z = (r - (FR - 1) / 2) * .56 - 1.5;
  FT.push({ x, z, a: Math.atan2(x, z + 1.5), col: new THREE.Color([TERRA, PEACH, CREAM, CORAL_L, SAND, ROSE, INK][(c * 7 + r * 3) % 7]) });
}
const pylon = mesh(new THREE.CylinderGeometry(.05, .09, 1.6, 16), phys(INK, { roughness: .3 })); pylon.position.set(0, .8, -1.5); field.add(pylon);
const pylonTop = mesh(new THREE.SphereGeometry(.12, 20, 14), glow(TERRA, 2.2), false, false); pylonTop.position.set(0, 1.62, -1.5); field.add(pylonTop);
const beamG = grp(field, 0, 0, -1.5);
const beam = new THREE.Mesh(new THREE.PlaneGeometry(6, 1.5), add(TERRA, .35, { side: THREE.DoubleSide })); beam.geometry.translate(3, .75, 0); beamG.add(beam);
const HOT = [[-.4, .35], [.8, -.35], [-.05, -1.2]];
const COLS = HOT.map(([x, z], i) => {
  const m = mesh(rb(.3, 1, .46, .04, 3), phys(i === 0 ? TERRA : CORAL_L, { roughness: .35, clearcoat: 1, emissive: TERRA, emissiveIntensity: i === 0 ? .4 : .15 }));
  m.geometry.translate(0, .5, 0); m.position.set(x, .03, z); field.add(m); m.visible = false;
  const c = card(.82, .25, 1, 0xfffaf5, .05); field.add(c); face(c.userData.face, "trend" + i); c.visible = false;
  return { m, c, x, z, h: [1.15, .6, .45][i] };
});
const hotBadge = card(.52, .14, 1, null); field.add(hotBadge); face(hotBadge.userData.face, "hot");
const FLAME = Array.from({ length: 16 }, (_, i) => { const h = halo(.16 + hash(i) * .12, i % 2 ? GOLD : TERRA, .9); field.add(h); return h; });
const radarTitle = card(.9, .13, 1, null); field.add(radarTitle); face(radarTitle.userData.face, "radarTitle");
const DECO_M1 = decor(field, 16, (i, k) => V((i % 2 ? 1 : -1) * (3.5 + hash(k + 5) * 3), 1.2 + hash(k + 7) * 3, -6 + hash(k) * 9), 2);
// MOVE 2: a corridor of storyboard frames that flip to the lens, ending at the shot list
const corridor = grp(inside, M2.x, 0, M2.z);
const CORR = Array.from({ length: 24 }, (_, i) => {
  const side = i % 2 ? 1 : -1, z = .8 - Math.floor(i / 2) * .66;
  const c = card(.32, .55, 1, 0xfffaf5, .04); c.position.set(side * (.34 + hash(i) * .14), .85 + hash(i + 3) * .7, z); corridor.add(c);
  face(c.userData.face, i % 3 ? "frame" + (i % 4) : "tc" + (i % 4));
  return { c, side, z };
});
const boardG = grp(corridor, 0, 1.25, -8.6);
boardG.add(at(mesh(rb(1.08, 1.62, .06, .06, 3), phys(0xfffaf5, { roughness: .45, clearcoat: .5 })), 0, -.06, -.04));
const boardHead = card(.9, .1, 1, null); boardHead.position.set(0, .64, 0); boardG.add(boardHead); face(boardHead.userData.face, "boardHead");
const FRAMES = Array.from({ length: 4 }, (_, i) => { const c = card(.36, .62, 1, 0xfffaf5, .03); boardG.add(c); face(c.userData.face, "frame" + i); c.visible = false; return c; });
const SWATCH = [TERRA, CORAL_L, CREAM, INK, GOLD].map((col) => { const m = mesh(new THREE.SphereGeometry(.07, 24, 16), phys(col, { roughness: .3, clearcoat: 1 })); boardG.add(m); m.visible = false; return m; });
const DECO_M2 = decor(corridor, 18, (i, k) => V((i % 2 ? 1 : -1) * (2.2 + hash(k + 5) * 3), .5 + hash(k + 7) * 3.2, 2 - hash(k) * 12), 3);
// MOVE 3: a giant keyboard; the script types above it
const keys = grp(inside, M3.x, 0, M3.z);
const KC = 11, KR = 6, KEY_N = KC * KR;
const keyMesh = new THREE.InstancedMesh(rb(.5, .26, .5, .08, 3), new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: .4, clearcoat: .6 }), KEY_N);
for (let i = 0; i < KEY_N; i++) keyMesh.setColorAt(i, new THREE.Color([CREAM, PEACH, SAND, CREAM, ROSE, CORAL_L][(i * 7 + Math.floor(i / KC)) % 6]));
keyMesh.instanceColor.needsUpdate = true;
keyMesh.castShadow = true; keyMesh.receiveShadow = true; keyMesh.frustumCulled = false; keys.add(keyMesh);
const KB = mesh(rb(KC * .56 + .3, .2, KR * .56 + .3, .1, 3), phys(INK, { roughness: .4, clearcoat: .6 })); KB.position.set(0, .05, -.3); keys.add(KB);
const AG = "AGENT".split("").map((ch, i) => {
  const g = grp(keys, (i - 2) * .56, .27, -.3 + .56 * 1.5);
  g.add(mesh(rb(.5, .26, .5, .08, 3), phys(i === 0 ? TERRA : CORAL_L, { roughness: .35, clearcoat: 1 })));
  const f = new THREE.Mesh(new THREE.PlaneGeometry(.38, .38), faceMat(1)); f.rotation.x = -Math.PI / 2; f.position.y = .132; g.add(f); face(f, "key" + i);
  return g;
});
const page = card(1.0, 1.2, 1, 0xfffaf5, .04); page.position.set(0, 1.75, -1.6); page.rotation.x = -.18; keys.add(page); face(page.userData.face, "page");
const PLINES = Array.from({ length: 5 }, (_, i) => {
  const w = .84, h = .085;
  const geo = new THREE.PlaneGeometry(w, h); geo.translate(w / 2, 0, 0);
  const m = new THREE.Mesh(geo, faceMat(1)); m.position.set(-.42, .3 - i * .13, .016); page.add(m); face(m, "pl" + i);
  return m;
});
const caret = mesh(new THREE.BoxGeometry(.012, .07, .004), glow(TERRA, 1.2), false, false); page.add(caret);
const capCard = card(.82, .3, 1, 0xfffaf5, .05); capCard.position.set(.3, 1.08, -1.1); capCard.rotation.set(-.2, 0, .05); keys.add(capCard); face(capCard.userData.face, "caption"); capCard.visible = false;
const LETTERS = Array.from({ length: 12 }, (_, i) => { const c = card(.12, .12, 1, null); keys.add(c); face(c.userData.face, "key" + (i % 5)); c.visible = false; return c; });
// MOVE 4: a storm of comments at the lens, replies shooting back; three land with their replies
const storm = grp(inside, M4.x, 0, M4.z);
const STORM = Array.from({ length: 34 }, (_, i) => {
  const c = card(.7, .15, 1, 0xfffaf5, .06); storm.add(c); face(c.userData.face, ["cm0", "cm1", "cm2", "ag0", "ag1", "ag2"][i % 6]);
  const a = hash(i) * Math.PI * 2, r = .5 + hash(i + 1) * 1.3;
  return { c, x: Math.cos(a) * r, y: 1.45 + Math.sin(a) * r * .9, t0: L[7] - .3 + i * .045, sp: 7 + hash(i + 2) * 4 };
});
const REPLIES = Array.from({ length: 12 }, (_, i) => {
  const c = card(.6, .14, 1, TERRA, .06); storm.add(c); face(c.userData.face, "rp" + (i % 3));
  const a = hash(i + 40) * Math.PI * 2, r = .4 + hash(i + 41) * 1.0;
  return { c, x: Math.cos(a) * r, y: 1.45 + Math.sin(a) * r * .9, t0: T.replies - .1 + i * .07 };
});
const roomG = grp(storm, 0, 1.45, -3); roomG.scale.setScalar(.72);
const CMS = Array.from({ length: 3 }, (_, i) => {
  const c = card(.98, .2, 1, 0xfffaf5, .06); c.position.set(-.18, .52 - i * .5, 0); roomG.add(c); face(c.userData.face, "cm" + i); c.visible = false;
  const r = card(.78, .17, 1, TERRA, .06); r.position.set(.28, .3 - i * .5, .12); roomG.add(r); face(r.userData.face, "rp" + i); r.visible = false;
  return { c, r };
});
const DECO_M4 = decor(storm, 16, (i, k) => V((i % 2 ? 1 : -1) * (2.5 + hash(k + 5) * 3), .5 + hash(k + 7) * 3.2, 1 - hash(k) * 10), 4);
// MOVE 5: the lab
const lab = grp(inside, LAB.x, 0, LAB.z);
lab.add(at(mesh(new THREE.CylinderGeometry(.42, .5, .62, 48), phys(0x1b1218, { roughness: .25, clearcoat: 1 })), 0, .31, 0));
const rim = mesh(new THREE.TorusGeometry(.42, .012, 8, 64), glow(TERRA, 2.2), false, false); rim.rotation.x = -Math.PI / 2; rim.position.y = .62; lab.add(rim);
const labFloor = mesh(new THREE.CircleGeometry(3.2, 64), std(0x150d12, { roughness: .35, metalness: .3 }), false, true); labFloor.rotation.x = -Math.PI / 2; labFloor.position.y = .004; lab.add(labFloor);
for (const r of [.9, 1.5, 2.2]) { const ring = new THREE.Mesh(new THREE.RingGeometry(r, r + .012, 96), add(TERRA, .35, { side: THREE.DoubleSide })); ring.rotation.x = -Math.PI / 2; ring.position.y = .01; lab.add(ring); }
const oldReel = card(.5, .88, 1, 0x1a1220, .05); oldReel.position.set(0, 1.12, 0); lab.add(oldReel); face(oldReel.userData.face, "reelOld");
const scanRing = new THREE.Mesh(new THREE.TorusGeometry(.43, .008, 8, 80), add(0xffd9c2, 2.0)); scanRing.rotation.x = Math.PI / 2; lab.add(scanRing);
const scanDisc = new THREE.Mesh(new THREE.CircleGeometry(.43, 64), add(TERRA, .25, { side: THREE.DoubleSide })); scanDisc.rotation.x = -Math.PI / 2; lab.add(scanDisc);
const METRICS = Array.from({ length: 3 }, (_, i) => {
  const c = card(.62, .17, 1, 0x1a1220, .05); lab.add(c); face(c.userData.face, "met" + i); c.visible = false;
  const bar = mesh(new THREE.BoxGeometry(.4, .022, .01), glow([TERRA, CORAL_L, GOLD][i], 1.5), false, false); bar.geometry.translate(.2, 0, 0); bar.position.set(-.24, -.045, .02); c.add(bar);
  return { c, bar, fill: [.82, .64, .9][i] };
});
const DATA = Array.from({ length: 28 }, (_, i) => { const h = halo(.07, i % 3 ? CORAL_L : 0xffffff, 1.2); lab.add(h); h.visible = false; return h; });
const SH_C = 7, SH_R = 12, SH_N = SH_C * SH_R;
const shards = new THREE.InstancedMesh(new THREE.BoxGeometry(.066, .066, .02), new THREE.MeshStandardMaterial({ roughness: .4, emissive: 0xffffff, emissiveIntensity: .04 }), SH_N);
for (let i = 0; i < SH_N; i++) { const r = Math.floor(i / SH_C), k = i % SH_C; shards.setColorAt(i, new THREE.Color().setHSL((18 + r * 2 + k) / 360, .62, .42 + (r / SH_R) * .25)); }
shards.instanceColor.needsUpdate = true; shards.frustumCulled = false; lab.add(shards); shards.visible = false;
const newReel = card(.5, .88, .8, TERRA, .05); lab.add(newReel); face(newReel.userData.face, "reelNew"); newReel.visible = false;
const newHalo = halo(2.2, CORAL_L, 0); newHalo.position.z = -.1; newReel.add(newHalo);
const loopG = grp(lab, 0, 1.12, 0);
const loopRing = new THREE.Mesh(new THREE.TorusGeometry(.4, .01, 8, 96), add(CORAL_L, 1.6)); loopG.add(loopRing);
const LOOP = Array.from({ length: 3 }, (_, i) => { const c = card(.22, .065, 1, null); loopG.add(c); face(c.userData.face, "loop" + i); return c; });
loopG.visible = false;
const WORLDS = [field, corridor, keys, storm, lab];

// ---------------------------------------------------------------- CTA: the sky of AGENT comments and the DM
const SWARM = Array.from({ length: 38 }, (_, i) => {
  const c = card(.5, .12, 1, 0xfffaf5, .06); outside.add(c); face(c.userData.face, "ag" + (i % 6)); c.visible = false;
  const near = i % 3 === 0, side = i % 2 ? 1 : -1;
  return { c, t0: T.agentcta - .1 + i * .07, x: side * (near ? .55 + hash(i + 3) * .4 : .6 + hash(i + 3) * 1.2), z: near ? .9 + hash(i + 8) * .6 : -.4 + hash(i + 8) * 1.2, sp: .55 + hash(i + 1) * .5 };
});
const dm = card(.78, .2, 1, 0xfffaf5, .07); outside.add(dm); face(dm.userData.face, "dm"); dm.visible = false;

// drifting dust in the light, everywhere
const DUST_N = 160;
const dust = new THREE.InstancedMesh(new THREE.PlaneGeometry(.03, .03), add(0xfff0e0, .5, { map: glowTex }), DUST_N); dust.frustumCulled = false; scene.add(dust);

// ---------------------------------------------------------------- the screen (one canvas, redrawn when its state changes)
let screenKey = "";
const fmt = (n) => Math.round(n).toLocaleString("en-US");
function write(g, s, x, y, size, o = {}) {
  g.font = `${o.i ? "italic " : ""}${o.w || 700} ${size}px ${o.f || "Montserrat"}`; g.fillStyle = o.c || "#1d1418"; g.textAlign = o.a || "left"; g.textBaseline = "middle";
  g.fillText(s, x, y, o.max);
}
function tick(g, x, y, s, c = "#2fbf71", lw = 0) {
  g.strokeStyle = c; g.lineWidth = lw || s * .2; g.lineCap = "round"; g.lineJoin = "round";
  g.beginPath(); g.moveTo(x - s * .45, y); g.lineTo(x - s * .12, y + s * .32); g.lineTo(x + s * .48, y - s * .36); g.stroke();
}
function sparkGlyph(g, x, y, R, c = "#d97757") {
  g.fillStyle = c;
  for (let i = 0; i < 12; i++) {
    const a = i / 12 * Math.PI * 2 + (i % 2) * .05, l = R * (.75 + hash(i + 3) * .3);
    g.save(); g.translate(x, y); g.rotate(a); rr(g, -R * .13, R * .2, R * .26, l, R * .13); g.fill(); g.restore();
  }
  g.beginPath(); g.arc(x, y, R * .42, 0, Math.PI * 2); g.fill();
}
const TILE_GR = [["#d97757", "#f0a07c"], ["#f6c9a8", "#e8cfb6"], ["#1d1418", "#4a2c30"], ["#f0a07c", "#ffd9c2"], ["#e8cfb6", "#d9b79a"],
  ["#c4603f", "#d97757"], ["#e9a2a0", "#f6c9a8"], ["#2a1c22", "#1d1418"], ["#f0a07c", "#d97757"]];
function thumb(g, x, y, w, h, k) {
  const [a, b] = TILE_GR[k % 9], gr = g.createLinearGradient(x, y, x + w, y + h); gr.addColorStop(0, a); gr.addColorStop(1, b);
  g.fillStyle = gr; g.fillRect(x, y, w, h);
  g.fillStyle = "rgba(255,255,255,.75)"; g.beginPath(); const cx = x + w / 2, cy = y + h / 2; g.moveTo(cx - 12, cy - 16); g.lineTo(cx + 16, cy); g.lineTo(cx - 12, cy + 16); g.fill();
}
function heartGlyph(g, x, y, s, c) {
  g.fillStyle = c; g.beginPath(); g.moveTo(x, y + s * .35);
  g.bezierCurveTo(x - s * .6, y - s * .1, x - s * .35, y - s * .6, x, y - s * .25); g.bezierCurveTo(x + s * .35, y - s * .6, x + s * .6, y - s * .1, x, y + s * .35); g.fill();
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
    g.fillStyle = "#f1e7dc"; rr(g, 30, 520, 560, 96, 48); g.fill();
    g.fillStyle = "#d97757"; g.beginPath(); g.arc(90, 568, 30, 0, 7); g.fill();
    if (a) write(g, a, 140, 568, 40, { w: 800 }); else write(g, "Add a comment…", 140, 568, 34, { w: 500, c: "#a8968c" });
    g.fillStyle = a ? "#d97757" : "#e1d3c6"; g.beginPath(); g.arc(650, 568, 44, 0, 7); g.fill();
    g.strokeStyle = "#fff"; g.lineWidth = 7; g.lineCap = "round"; g.beginPath(); g.moveTo(632, 568); g.lineTo(668, 568); g.moveTo(654, 552); g.lineTo(670, 568); g.lineTo(654, 584); g.stroke();
    const rows = [["creator.sana", "AGENT"], ["tech.aman", "agent pls"], ["neha.edits", "AGENT"], ["j.reels", "AGENT!!"], ["studio.kai", "agent"], ["mira.makes", "AGENT"]];
    if (b === "sent") rows.unshift(["you", "AGENT"]);
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
  ct("lblFollowers", 512, 82, (g, w, h) => write(g, "FOLLOWERS", w / 2, h / 2, 46, { f: "JBMono", c: "#1d1418", a: "center" }));
  ["+1 follower", "+1 follower", "+2 followers"].forEach((s, i) => ct("pill" + i, 400, 105, (g, w, h) => {
    panel(g, w, h, { bg: "#2fbf71", r: 52 });
    g.fillStyle = "#fff"; g.beginPath(); g.arc(56, 42, 15, 0, 7); g.fill(); g.beginPath(); g.ellipse(56, 78, 26, 16, 0, Math.PI, 0); g.fill();
    write(g, s, 96, h / 2 + 2, 42, { w: 800, c: "#fff", max: w - 110 });
  }));
  for (let i = 0; i < 4; i++) ct("tc" + i, 420, 700, (g, w, h) => {        // the tunnel's reels: a thumbnail, a play button, a heart
    panel(g, w, h, { r: 30 }); thumb(g, 16, 16, w - 32, 560, [0, 3, 5, 8][i]);
    heartGlyph(g, 60, 632, 50, "#e5484d"); g.fillStyle = "#efe4d8"; rr(g, 104, 618, 200, 26, 13); g.fill();
    g.fillStyle = "rgba(29,20,24,.6)"; rr(g, 34, 34, 104, 44, 22); g.fill(); write(g, "Reel", 86, 57, 24, { w: 700, c: "#fff", a: "center" });
  });
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
  ct("boardHead", 900, 100, (g, w, h) => write(g, "SHOT LIST · VISUALS", w / 2, h / 2, 54, { f: "JBMono", c: "#1d1418", a: "center" }));
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
  [["HOOK:", " I turned Claude into an agent"], ["PROOF:", " 339 → 2,400 followers"], ["LIST:", " five moves, best one last"],
    ["SHOW:", " a world for every move"], ["CTA:", " comment AGENT"]].forEach(([a, b], i) => ct("pl" + i, 840, 85, (g, w, h) => {
    write(g, a, 0, h / 2, 46, { f: "JBMono", c: "#d97757" }); const aw = g.measureText(a).width;
    write(g, b, aw, h / 2, 46, { w: 700 });
  }));
  ct("caption", 820, 300, (g, w, h) => {
    panel(g, w, h, { r: 40, line: "#d97757", lw: 6 }); write(g, "CAPTION", 40, 56, 30, { f: "JBMono", c: "#d97757" });
    write(g, "Steal my Claude setup.", 40, 124, 48, { w: 800, max: w - 80 }); write(g, "Comment AGENT below", 40, 184, 44, { w: 600, max: w - 80 });
    write(g, "#reels  #ai  #instagramgrowth", 40, 250, 34, { w: 600, c: "#3d8bff", max: w - 80 });
  });
  "AGENT".split("").forEach((ch, i) => ct("key" + i, 128, 128, (g, w, h) => write(g, ch, w / 2, h / 2 + 4, 96, { w: 800, c: "#fff", a: "center" })));
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
  [["creator.sana", "AGENT"], ["tech.aman", "agent pls"], ["neha.edits", "AGENT"], ["j.reels", "AGENT!!"], ["studio.kai", "agent"], ["mira.makes", "AGENT"]].forEach(([n, s], i) =>
    ct("ag" + i, 500, 120, (g, w, h) => {
      panel(g, w, h, { r: 60 }); avatar(g, 60, h / 2, 38, ["#8b6cf6", "#3d8bff", "#2fbf71", "#d97757", "#ffbf47", "#e9a2a0"][i], n[0].toUpperCase());
      write(g, "@" + n, 116, 40, 24, { f: "JBMono", c: "#8a7a72" }); write(g, s, 116, 84, 40, { w: 800 });
    }));
  ct("dm", 780, 200, (g, w, h) => {
    panel(g, w, h, { r: 56 }); g.fillStyle = "#1d1418"; g.beginPath(); g.arc(100, h / 2, 60, 0, 7); g.fill();
    sparkGlyph(g, 100, h / 2, 34, "#d97757");
    write(g, "ai.nxtlvl · now", 190, 66, 30, { f: "JBMono", c: "#8a7a72" }); write(g, "My whole Claude setup", 190, 130, 44, { w: 800, max: w - 310 });
    g.fillStyle = "#2fbf71"; rr(g, w - 120, h / 2 - 30, 92, 60, 30); g.fill(); write(g, "sent", w - 74, h / 2 + 2, 28, { w: 800, c: "#fff", a: "center" });
  });
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
  [T.portal, V(0, 1.15, .1), .2, .001], [T.portal + .4, V(.46, 1.98, .52), .42, .4],
  [L[1] + .1, V(.72, 2.25, .45), .38, .4], [L[2] - .05, V(.55, 1.95, 1.2), .36, .35], [T.grows - .12, V(.55, 2.35, .9), .36, .3],
  [L[3] - .05, V(.62, 2.25, 1.35), .3, .35], [T.in0 - .3, V(0, 1.78, 1.45), .2, .3],
  [T.in0, wp(M1, .55, 1.25, 1.3), .4, .001], [L[5] - .14, wp(M2, .32, 1.55, -5.2), .36, .001], [L[6] - .14, wp(M3, .65, 1.15, .1), .38, .001],
  [L[7] - .14, wp(M4, .5, 1.95, -1.8), .34, .001], [T.dark0, wp(LAB, .72, 1.62, .35), .38, .001],
  [T.rewrites - .1, wp(LAB, .62, 1.8, .45), .38, .3],
  [T.out1, V(.58, 2.05, .8), .36, .001], [L[10] - .1, V(.56, 2.15, .6), .36, .35],
].map((k) => ({ t: k[0], p: Array.isArray(k[1]) ? V(...k[1]) : k[1], s: k[2], d: k[3] || .3 }));
function clAt(t) {
  if (t < T.portal) {                                 // the hook: flying ahead of the camera down the tunnel
    const cz = camera.position.z;
    return { p: V(Math.sin(t * 3.1) * .22, 1.1 + Math.cos(t * 2.3) * .14, cz - 1.5 - easeIn(win(t, T.portal - .35, T.portal)) * 1.2), s: .42 * backOut(win(t, T.claude - .15, T.claude + .15), 2) };
  }
  let i = 0; for (let j = 0; j < CLK.length; j++) if (t >= CLK[j].t) i = j;
  const a = CLK[Math.max(0, i - 1)], b = CLK[i];
  const k = i === 0 ? 1 : easeIO(clamp((t - b.t) / b.d));
  return { p: a.p.clone().lerp(b.p, k), s: lerp(a.s, b.s, k) };
}
function animClaude(t) {
  const { p, s } = clAt(t);
  const bob = Math.sin(t * 2.4) * .025;
  cl.root.position.set(p.x, p.y + bob, p.z);
  show(cl.root, s * (1 + pulse(t, T.portal + .35, .06, .3) * .25 + pulse(t, T.followers, .05, .3) * .15 + pulse(t, T.next, .05, .3) * .15));
  cl.root.lookAt(camera.position.x, camera.position.y, camera.position.z);
  cl.body.rotation.z = Math.sin(t * 1.6) * .12 + (t > L[10] ? Math.sin(t * 9) * .18 : 0) + (t < T.portal ? t * 4 : 0);
  cl.rs.forEach((r, i) => { r.piv.rotation.z = r.base + Math.sin(t * 3 + i) * .05; r.r.scale.y = 1 + Math.sin(t * 6 + i * 1.7) * .08; });
  const blink = ((t + .3) % 2.9) < .1;
  const happy = between(t, T.followers, T.followers + 1) || t > L[10];
  cl.eyes.forEach((e) => { e.open.visible = !(blink || happy); e.shut.visible = blink || happy; });
  cl.mouthO.visible = between(t, T.claude, T.claude + .8) || between(t, T.five5, T.five5 + .6) || between(t, T.next, T.next + .6);
  cl.smile.visible = !cl.mouthO.visible;
  const dark = between(t, T.dark0, T.out1), tun = t < T.portal;
  coralLight.position.copy(cl.root.position); coralLight.intensity = cl.root.visible ? (dark || tun ? 6 : 1.2) : 0;
  cl.halo.material.color.set(CORAL_L).multiplyScalar(dark || tun ? .45 : .2);
  // the trail: only while it flies fast (the tunnel, the dive, the lab)
  const fast = tun || between(t, T.in0 - .35, T.in0);
  for (let k = 0; k < TRAIL_N; k++) {
    const tt = t - (k + 2) * .02;
    if (!fast || tt < T.claude) { trail.setMatrixAt(k, ZERO); continue; }
    const q = clAt(tt).p;
    tP.set(q.x, q.y, tun ? q.z + (k + 2) * .02 * 22 : q.z);
    tS.setScalar(Math.sin((k + 1) / (TRAIL_N + 1) * Math.PI) * .9);
    trail.setMatrixAt(k, tM.compose(tP, camera.quaternion, tS));
  }
  trail.instanceMatrix.needsUpdate = true;
}

// ---------------------------------------------------------------- the hook's tunnel at work
function animTunnel(t) {
  RINGS.forEach((g, r) => { g.rotation.z = t * (r % 2 ? .5 : -.4) + r * .2; });
  const cz = camera.position.z - TUN_Z;
  for (let i = 0; i < STREAK_N; i++) {
    const a = hash(i) * Math.PI * 2, r = .55 + hash(i + 1) * .5;
    const z = cz - 1 - ((hash(i + 2) * 18 + t * 26) % 18);
    tP.set(Math.cos(a) * r, 1.15 + Math.sin(a) * r, z); tS.set(1, 1, .5 + hash(i + 3));
    streaks.setMatrixAt(i, tM.compose(tP, tQ.identity(), tS));
  }
  streaks.instanceMatrix.needsUpdate = true;
  portalLight.position.set(0, 1.15, TUN_Z + PORTAL_Z + 1.5); portalLight.intensity = 30 + 60 * win(t, T.portal - .6, T.portal);
  portal.material.color.set(0xfff2e6).multiplyScalar(1.6 + 1.5 * win(t, T.portal - .5, T.portal));
}

// ---------------------------------------------------------------- the outside at work
function animOutside(t) {
  animDecor(DECO_OUT, t);
  // the phone: still after the portal; it falls flat for the city and stands back up behind the wheel
  const flat = easeIO(win(t, T.grows - .2, T.grows + .1)) * (1 - easeIO(win(t, L[3] - .1, L[3] + .3)));
  phone.position.set(0, 1.15 - flat * .3 + Math.sin(t * 1.3) * .012, -flat * .1);
  phone.rotation.set(-flat * Math.PI / 2 + Math.sin(t * .9) * .02 * (1 - flat), Math.sin(t * .7) * .035 * (1 - flat), 0);
  const sq = pulse(t, T.portal, .02, .25); phone.scale.set(1 + sq * .03, 1 - sq * .04, 1);
  // what the screen shows
  const v1 = lerp(339, 2400, easeIO(win(t, T.twenty - .2, T.followers + .1)));
  if (t < T.in0) drawScreen(`p|${fmt(v1)}|${between(t, T.grows - .1, L[3] + .3) ? "nogrid" : ""}`);
  else if (t < L[10] - .1) drawScreen("p|2,400|");
  else {
    const typed = "AGENT".slice(0, clamp(Math.floor((t - T.agentcta + .06) / .075) + 1, 0, 5));
    drawScreen(`c|${t < T.agentcta - .06 ? "" : typed}|${t > T.agentcta + .5 ? "sent" : ""}`);
  }
  screenGlow.material.color.set(0xffd9c2).multiplyScalar(.12 + pulse(t, T.portal, .05, .6) * .7);
  // Claude's burst out of the screen: the shockwave
  const sw = win(t, T.portal, T.portal + .55);
  shock.visible = sw > 0 && sw < 1; shock.position.set(0, 1.15, .1 + sw * .3); shock.scale.setScalar(.3 + easeOut(sw) * 3.2);
  shock.material.color.set(CORAL_L).multiplyScalar(1.4 * (1 - sw));
  // the odometer and the vortex of followers pouring into the screen
  const o1 = backOut(win(t, L[1] - .15, L[1] + .2), 1.8) * (1 - easeIn(win(t, L[2] - .15, L[2] + .05)));
  show(odo1.g, o1 * (1 + pulse(t, T.followers, .05, .3) * .12));
  odo1.g.rotation.y = Math.sin(t * .8) * .1; odo1.g.position.y = 2.3 + Math.sin(t * 1.7) * .015;
  odo1.g.quaternion.setFromEuler(tE.set(0, Math.atan2(camera.position.x, camera.position.z) * .7, 0));
  setOdo(odo1, t < T.twenty - .2 ? 339 : v1);
  burst(confA, t, T.followers, V(0, 2.3, .35));
  const gv = win(t, L[1] - .3, L[1] + .3) * (1 - win(t, L[2] - .2, L[2] + .1));
  galaxy.visible = gv > 0;
  if (galaxy.visible) {
    for (let i = 0; i < GAL_N; i++) {
      const ph = ((t - L[1]) * (.5 + hash(i + 5) * .35) + hash(i)) % 1;
      const r0 = 1.0 + hash(i + 1) * 2.4, th = hash(i + 2) * Math.PI * 2 + ph * 5.5 + t * .4, y0 = .1 + hash(i + 3) * 3.0;
      const r = r0 * Math.pow(1 - ph, 1.25);
      tP.set(Math.cos(th) * r, lerp(y0, 1.15, Math.pow(ph, 1.4)), .06 + Math.sin(th) * r * .8 + (1 - ph) * .2);
      tS.setScalar(gv * (1 - Math.pow(ph, 4)) * (.6 + hash(i + 4) * .9));
      galaxy.setMatrixAt(i, tM.compose(tP, tQ.identity(), tS));
    }
    galaxy.instanceMatrix.needsUpdate = true;
  }
  PILLS.forEach((p) => {
    const dt = t - p.t0, life = 1.2;
    if (dt < 0 || dt > life || t > L[2]) { p.c.visible = false; return; }
    const k2 = dt / life;
    p.c.visible = true;
    p.c.position.set(p.sx + p.dx * k2 * 1.3, p.sy + p.dy * k2, .1 + easeIn(k2) * 1.9 + k2 * .4);
    p.c.quaternion.copy(camera.quaternion);
    p.c.scale.setScalar(Math.max(.001, backOut(win(dt, 0, .18), 2) * (.7 + k2 * .5)));
  });
  // the post: out of the screen into bullet time, stamped, flung away
  const ra = L[2] - .1, rk = backOut(win(t, ra, ra + .28), 1.6), fling = easeIn(win(t, T.post + .3, T.post + .62));
  reel.visible = t > ra && t < T.post + .65;
  if (reel.visible) {
    reel.position.set(lerp(0, REEL_P.x, rk) - fling * 1.8, lerp(1.15, REEL_P.y, rk) + fling * .5, lerp(.05, REEL_P.z, rk) - fling * .6);
    reel.rotation.set(fling * 1.2, fling * 3, fling * 2.2 + pulse(t, T.post, .03, .2) * .08);
    reel.scale.setScalar(Math.max(.001, lerp(.4, .82, rk) * (1 + pulse(t, T.post, .03, .2) * .1)));
    reel.userData.face.material.map = t < T.post ? TX.reel : TX.reelStrike;
  }
  // the city: the grid's tiles shoot up from the flat phone, windows lit
  tiles.forEach((tl, i) => {
    const a = T.grows - .02 + (tl.k + (2 - tl.r)) * .05;
    const up = easeOut(win(t, a, a + .4)) * (1 - easeIn(win(t, L[3] - .15, L[3] + .1)));
    tl.m.visible = up > .002;
    const hgt = Math.max(.001, up * TILE_H[i] * (1 + pulse(t, T.page, .05, .3) * .12));
    tl.m.scale.set(1, 1, hgt); tl.win.position.z = 1.003; tl.win.scale.set(1, 1, 1 / hgt);
  });
  const ar = easeOut(win(t, T.grows + .15, T.page + .1)) * (1 - easeIn(win(t, L[3] - .2, L[3])));
  arrow.visible = ar > .002; arrow.position.set(.23, .9 + 1.5 + ar * 1.0, .64); arrow.rotation.set(0, -.6, 0); arrow.scale.setScalar(Math.max(.001, ar * .9));
  // the wheel of five moves: spins in 3D, lands with the dark fifth at the front, which leads the dive
  wheel.visible = between(t, L[3] - .12, T.in0 + .02);
  if (wheel.visible) {
    const spin = 1 - easeOut(win(t, L[3] - .1, T.last + .05));
    const phiEnd = -Math.PI / 2 - 4 * Math.PI * 2 / 5;
    const phi = phiEnd - spin * 2.2 * Math.PI * 2;
    const focus = easeIO(win(t, T.last - .02, T.last + .35)), dive = easeIn(win(t, T.in0 - .38, T.in0));
    wheel.rotation.set(Math.sin(t * 1.3) * .12 * (1 - focus), Math.sin(t * 1.5) * .45 * (1 - focus), 0);
    wheelRing.scale.setScalar(Math.max(.001, backOut(win(t, L[3] - .1, L[3] + .2), 2) * (1 + focus * .4)));
    wheelRing.material.color.set(TERRA).multiplyScalar(1.3 * (1 - dive));
    ICONS.forEach((g, i) => {
      const a = phi + i * Math.PI * 2 / 5, pk = backOut(win(t, L[3] + i * .07, L[3] + i * .07 + .25), 2);
      const p0 = V(Math.cos(a) * .5, Math.sin(a) * .5, 0);
      if (i < 4) {
        g.position.copy(p0.multiplyScalar(1 + focus * 1.4)); g.position.z = -focus * .3;
        g.scale.setScalar(Math.max(.001, pk * (1 - focus * .4) * (1 - dive)));
        g.userData.f.material.color.setScalar(1 - focus * .45);
      } else {
        g.position.copy(p0.lerp(V(0, 0, .2), focus));
        g.scale.setScalar(Math.max(.001, pk * (1 + focus * .5 + pulse(t, T.smartest, .05, .3) * .25)));
        g.userData.h.material.color.set(TERRA).multiplyScalar(focus * (.5 + .25 * Math.sin(t * 14)));
      }
      g.rotation.set(Math.sin(t * 1.3 + i) * .1, Math.sin(t * 1.1 + i * 2) * .2, -wheel.rotation.z);
    });
  }
  // the CTA: the sky of AGENT comments, the DM
  SWARM.forEach((s, i) => {
    const dt = t - s.t0;
    if (dt < 0) { s.c.visible = false; return; }
    s.c.visible = true;
    s.c.position.set(s.x + Math.sin(dt * 2 + i) * .05, -.1 + dt * s.sp, s.z);
    s.c.quaternion.copy(camera.quaternion);
    s.c.scale.setScalar(Math.max(.001, backOut(win(dt, 0, .25), 2) * (1 - win(s.c.position.y, 1.9, 2.3)) * .85));
  });
  const dk = backOut(win(t, T.setup - .15, T.setup + .2), 1.8);
  dm.visible = dk > .002; dm.scale.setScalar(Math.max(.001, dk)); dm.position.set(0, lerp(2.1, 1.66, dk), .42); dm.quaternion.copy(camera.quaternion);
}

// ---------------------------------------------------------------- the worlds inside the phone at work
function animInside(t) {
  const W1 = t < L[5] - .14, W2 = between(t, L[5] - .14, L[6] - .14), W3 = between(t, L[6] - .14, L[7] - .14), W4 = between(t, L[7] - .14, T.dark0), W5 = t >= T.dark0;
  [W1, W2, W3, W4, W5].forEach((on, i) => { WORLDS[i].visible = on; });
  if (W1) {                                                     // MOVE 1: the beam sweeps, tiles light as it passes; the trends launch
    animDecor(DECO_M1, t);
    const ang = -t * 2.8;
    beamG.rotation.y = ang;
    for (let i = 0; i < FIELD_N; i++) {
      const f = FT[i];
      let d = ((f.a - Math.PI / 2 - ang) % (Math.PI * 2) + Math.PI * 3) % (Math.PI * 2) - Math.PI;
      const hit = Math.exp(-d * d * 30);
      tP.set(f.x, .05 + hit * .08 + Math.sin(t * 2 + i) * .01, f.z);
      tM.compose(tP, tQ.identity(), tS.setScalar(1)); fieldTiles.setMatrixAt(i, tM);
      fieldTiles.setColorAt(i, tC.copy(f.col).lerp(new THREE.Color(0xffe0cc), hit * .6));
    }
    fieldTiles.instanceMatrix.needsUpdate = true; fieldTiles.instanceColor.needsUpdate = true;
    COLS.forEach((c, i) => {
      const a = i === 0 ? T.blowing - .1 : L[4] + .15 + i * .3, up = easeOut(win(t, a, a + .4));
      c.m.visible = up > .002; c.m.scale.y = Math.max(.001, up * c.h);
      c.c.position.set(c.x, .03 + up * c.h + .22, c.z + .1); c.c.quaternion.copy(camera.quaternion);
      show(c.c, backOut(win(t, a + .05, a + .3), 2.2) * (1 + (i === 0 ? pulse(t, T.niche, .05, .3) * .12 : 0)));
    });
    const hb = easeOut(win(t, T.blowing - .1, T.blowing + .3));
    hotBadge.position.set(COLS[0].x, .03 + hb * COLS[0].h + .4, COLS[0].z + .15); hotBadge.quaternion.copy(camera.quaternion);
    show(hotBadge, backOut(win(t, T.blowing + .1, T.blowing + .35), 2.4));
    FLAME.forEach((f, i) => {
      const ph = ((t * 1.4 + hash(i)) % 1);
      f.visible = hb > .5; f.position.set(COLS[0].x + (hash(i + 3) - .5) * .22, .03 + hb * COLS[0].h + ph * .45, COLS[0].z + (hash(i + 5) - .5) * .14);
      f.scale.setScalar(1 - ph); f.quaternion.copy(camera.quaternion);
    });
    radarTitle.position.set(0, 1.95, -1.5); radarTitle.quaternion.copy(camera.quaternion); show(radarTitle, backOut(win(t, T.in0 + .1, T.in0 + .35), 2));
  }
  if (W2) {                                                     // MOVE 2: the frames flip to the lens as it passes; four snap in
    animDecor(DECO_M2, t);
    const cz = camera.position.z - IN_Z - M2.z;
    CORR.forEach((f, i) => {
      const open = easeIO(clamp(1 - (cz - f.z - .25) / 1.4));
      f.c.rotation.set(0, -f.side * (.12 + open * 1.45), f.side * .05);
      f.c.position.x = f.side * (.34 + hash(i) * .14 + open * .35);
    });
    FRAMES.forEach((c, i) => {
      const a = T.plans - .1 + i * .1, k = easeOut(win(t, a, a + .28));
      const home = V(-.21 + (i % 2) * .42, .26 - Math.floor(i / 2) * .68, .02), from = V((i % 2 ? 1 : -1) * 1.4, home.y + (i < 2 ? 1 : -1), 1.6);
      c.visible = t > a; c.position.copy(from.clone().lerp(home, k)); c.rotation.set(0, 0, (1 - k) * (i % 2 ? .9 : -.9));
      c.scale.setScalar(Math.max(.001, .6 + .4 * k + pulse(t, a + .28, .03, .15) * .06));
    });
    show(boardHead, backOut(win(t, T.plans - .25, T.plans), 2));
    SWATCH.forEach((m, i) => {
      const a = T.visuals - .05 + i * .06, k = backOut(win(t, a, a + .22), 2.6), ang = i / 5 * Math.PI * 2 + t * 2;
      show(m, k); m.position.set(Math.cos(ang) * .72, -.1 + Math.sin(ang) * .95, .25 + Math.sin(ang) * .1);
    });
  }
  if (W3) {                                                     // MOVE 3: the keyboard ripples; AGENT hammers; the page types
    const ty0 = L[6] - .05;
    for (let i = 0; i < KEY_N; i++) {
      const c = i % KC, r = Math.floor(i / KC);
      if (r === 1 && c >= 3 && c <= 7) { keyMesh.setMatrixAt(i, ZERO); continue; }
      const pr = Math.max(0, Math.sin(t * 13 - c * .8 - r * 1.3)) ** 6 * .07;
      tP.set((c - (KC - 1) / 2) * .56, .27 - pr, -.3 + (r - (KR - 1) / 2) * .56);
      keyMesh.setMatrixAt(i, tM.compose(tP, tQ.identity(), tS.setScalar(1)));
    }
    keyMesh.instanceMatrix.needsUpdate = true;
    AG.forEach((g, i) => { const pr = pulse(t, ty0 + i * .25, .04, .16); g.position.y = .27 - pr * .12; });
    LETTERS.forEach((c, i) => {
      const a = ty0 + (i % 5) * .25 + Math.floor(i / 5) * .03, ph = win(t, a, a + .7);
      c.visible = ph > 0 && ph < 1;
      c.position.set((i % 5 - 2) * .56 + (hash(i) - .5) * .3, .45 + easeOut(ph) * 1.4, -.3 + .84 - ph * 1.6);
      c.quaternion.copy(camera.quaternion); c.scale.setScalar(1.6 * (1 - ph * .5));
    });
    PLINES.forEach((m, i) => {
      const k = win(t, ty0 + i * .27, ty0 + i * .27 + .3);
      m.visible = k > 0; m.scale.x = Math.max(.001, k); if (m.material.map) m.material.map.repeat.x = Math.max(.001, k);
    });
    const cur = clamp(Math.floor((t - ty0) / .27), 0, 4), ck = win(t, ty0 + cur * .27, ty0 + cur * .27 + .3);
    caret.position.set(-.42 + .84 * ck + .01, .3 - cur * .13, .018); caret.visible = Math.floor(t * 4) % 2 === 0 || ck < 1;
    show(capCard, backOut(win(t, T.caption - .08, T.caption + .2), 2));
  }
  if (W4) {                                                     // MOVE 4: comments rush the lens; replies fire back; three land
    animDecor(DECO_M4, t);
    STORM.forEach((s, i) => {
      const dt = t - s.t0, z = -5.5 + dt * s.sp;
      s.c.visible = dt > 0 && z < 2.6;
      s.c.position.set(s.x, s.y, z); s.c.rotation.set(0, Math.sin(i) * .3, Math.sin(i * 2) * .2);
    });
    REPLIES.forEach((s, i) => {
      const dt = t - s.t0;
      s.c.visible = dt > 0 && dt < 1.2;
      s.c.position.set(s.x * (1 + dt), s.y, 1.2 - dt * 9); s.c.rotation.set(0, -Math.sin(i) * .3, 0);
    });
    CMS.forEach(({ c, r }, i) => {
      const a = T.comments - .25 + i * .1, k = backOut(win(t, a, a + .3), 1.8);
      c.visible = t > a; c.position.z = lerp(-2.2, 0, Math.min(1, k)); c.scale.setScalar(Math.max(.001, .7 + .3 * k));
      const b = a + .18, rk = backOut(win(t, b, b + .22), 2);
      r.visible = t > b; r.position.x = lerp(1.6, .3, Math.min(1, rk)); r.scale.setScalar(Math.max(.001, rk));
    });
  }
  if (W5) {                                                     // MOVE 5: the lab
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
      show(m.c, .56 * backOut(win(t, a, a + .25), 2) * (1 - easeIn(win(t, T.rewrites - .1, T.rewrites + .1))));
      m.c.position.set(-.05, 1.5 - i * .13, .34); m.c.quaternion.copy(camera.quaternion);
      m.bar.scale.x = Math.max(.001, easeOut(win(t, a + .15, a + .9)) * m.fill);
    });
    DATA.forEach((d, i) => {
      const ph = ((t - T.studies) * .9 + hash(i)) % 1;
      d.visible = between(t, T.studies + .3, T.rewrites);
      d.position.copy(V(-.1 + (hash(i + 2) - .5) * .3, .8 + hash(i + 4) * .7, .05).lerp(V(.72, 1.62, .35), easeIn(ph)));
      d.scale.setScalar(1 - ph * .6); d.quaternion.copy(camera.quaternion);
    });
    // rewrites: the old reel breaks apart, the pieces fly past the lens and come back together as v2
    const ex = easeOut(win(t, T.rewrites, T.rewrites + .32)), co = easeIO(win(t, T.rewrites + .32, T.next - .02));
    shards.visible = between(t, T.rewrites, T.next + .02);
    if (shards.visible) {
      const camL = camera.position.clone().sub(V(LAB.x, 0, LAB.z + IN_Z));
      for (let i = 0; i < SH_N; i++) {
        const r = Math.floor(i / SH_C), k = i % SH_C;
        const home = V((k - (SH_C - 1) / 2) * .068, 1.12 + ((SH_R - 1) / 2 - r) * .07, .02);
        const away = i % 3 === 0 ? camL.clone().add(V((hash(i) - .5) * 1.2, (hash(i + 1) - .5) * 1.0, -.3 - hash(i + 2) * .6))
          : home.clone().add(V((hash(i) - .5) * 2.4, (hash(i + 1) - .5) * 1.8, hash(i + 2) * 1.4));
        tP.copy(home.clone().lerp(away, ex * (1 - co)));
        tE.set((hash(i + 3) - .5) * 8 * ex * (1 - co), (hash(i + 4) - .5) * 8 * ex * (1 - co), 0); tQ.setFromEuler(tE);
        shards.setMatrixAt(i, tM.compose(tP, tQ, tS.setScalar(1)));
      }
      shards.instanceMatrix.needsUpdate = true;
    }
    const nk = backOut(win(t, T.next - .05, T.next + .2), 1.8), launch = easeIn(win(t, T.out1 - .32, T.out1));
    newReel.visible = nk > .002;
    newReel.scale.setScalar(Math.max(.001, nk * (1 + pulse(t, T.next + .15, .05, .3) * .1)));
    newReel.position.set(0, 1.12 + launch * .25, launch * 1.4); newReel.rotation.set(0, Math.sin(t * 1.1) * .08 * (1 - launch), 0);
    newHalo.material.color.set(CORAL_L).multiplyScalar(nk * .28 * (1 + .3 * Math.sin(t * 9)));
    const lk = backOut(win(t, T.next + .05, T.next + .35), 2);
    loopG.visible = lk > .002 && launch < .5; loopG.scale.setScalar(Math.max(.001, lk)); loopG.rotation.set(1.25, 0, 0);
    loopRing.rotation.z = -(t - T.next) * 1.6;
    LOOP.forEach((c, i) => { const a = i / 3 * Math.PI * 2 + (t - T.next) * 1.6 + Math.PI / 2; c.position.set(Math.cos(a) * .4, Math.sin(a) * .4, 0); c.quaternion.copy(loopG.quaternion).invert().multiply(camera.quaternion); });
  } else spot.intensity = 0;
}

// ---------------------------------------------------------------- camera: one shot list, blended where a cut isn't hard
// a shot is a move from p[0] to p[1] looking from q[0] to q[1], or an orbit {c, r, a, y} round a point
const TU = (x, y, z) => [x, y, z + TUN_Z];
const SHOTS = [
  { a: 0, b: T.portal, ease: (k) => k * .75 + k * k * .25, p: [TU(0, 1.15, 1.0), TU(0, 1.15, PORTAL_Z + .25)], q: [TU(0, 1.15, -8), TU(0, 1.15, PORTAL_Z - 6)], fov: [48, 40] },
  { a: T.portal, b: T.portal + .75, ease: easeOut, p: [[0, 1.15, .25], [.3, 1.52, 3.2]], q: [[0, 1.2, 0], [0, 1.42, 0]], fov: [32, 42] },
  { a: T.portal + .75, b: L[1], p: [[.3, 1.52, 3.2], [.42, 1.56, 3.45]], q: [[0, 1.42, 0], [0, 1.45, 0]], fov: 42 },
  { a: L[1], b: L[2] - .12, blend: .45, orbit: { c: [0, 0, 0], r: [3.1, 2.7], a: [-.85, .75], y: [1.2, 1.6] }, q: [[0, 1.85, 0], [0, 1.95, 0]], fov: 46 },
  { a: L[2] - .12, b: T.post + .3, blend: .25, orbit: { c: REEL_P.toArray(), r: [1.75, 1.6], a: [.75, -.55], y: [1.7, 1.55] }, q: [REEL_P.toArray(), REEL_P.toArray()], fov: 44 },
  { a: T.post + .3, b: T.grows - .12, p: [[.2, 2.6, 2.6], [0, 3.2, 2.4]], q: [[0, 1.0, 0], [0, .9, 0]], fov: 44 },
  { a: T.grows - .12, b: L[3] - .1, p: [[0, 3.4, 2.4], [1.35, 1.75, 2.6]], q: [[0, .9, 0], [-.1, 1.4, -.3]], fov: [44, 46] },
  { a: L[3] - .1, b: T.in0 - .4, p: [[0, 1.82, 3.7], [0, 1.8, 3.35]], q: [WC.toArray(), WC.toArray()], fov: 42 },
  { a: T.in0 - .4, b: T.in0, ease: easeIn, p: [[0, 1.8, 3.35], [0, WC.y, WC.z + .35]], q: [WC.toArray(), [0, WC.y, WC.z - 2]], fov: [42, 30] },
  { a: T.in0, b: L[5] - .14, ease: easeOut, p: [wp(M1, 0, 3.4, 5.6), wp(M1, .45, 1.45, 3.15)], q: [wp(M1, 0, .1, -1.5), wp(M1, -.2, 1.2, .1)], fov: [50, 44] },
  { a: L[5] - .14, b: L[6] - .14, ease: (k) => easeOut(k), p: [wp(M2, 0, 1.3, 2.2), wp(M2, 0, 1.25, -6.1)], q: [wp(M2, 0, 1.25, -4), wp(M2, 0, 1.2, -8.6)], fov: 46 },
  { a: L[6] - .14, b: L[7] - .14, p: [wp(M3, .25, 1.35, 3.0), wp(M3, 0, 1.6, 1.05)], q: [wp(M3, 0, .25, 0), wp(M3, 0, 1.62, -1.6)], fov: 46 },
  { a: L[7] - .14, b: T.dark0, ease: easeOut, p: [wp(M4, 0, 1.5, 3.2), wp(M4, 0, 1.45, .2)], q: [wp(M4, 0, 1.45, -3), wp(M4, 0, 1.45, -3)], fov: [50, 44] },
  { a: T.dark0, b: T.rewrites - .1, orbit: { c: wp(LAB, 0, 0, 0), r: [2.6, 2.0], a: [.7, -.35], y: [1.6, 1.42] }, q: [wp(LAB, 0, 1.18, 0), wp(LAB, 0, 1.2, 0)], fov: 40 },
  { a: T.rewrites - .1, b: T.out1, blend: .3, orbit: { c: wp(LAB, 0, 0, 0), r: [1.7, 2.2], a: [-.35, .1], y: [1.3, 1.38] }, q: [wp(LAB, 0, 1.15, 0), wp(LAB, 0, 1.25, .3)], fov: 44 },
  { a: T.out1, b: T.out1 + .7, ease: easeOut, p: [[0, 1.45, 1.1], [0, 1.6, 3.3]], q: [[0, 1.45, 0], [0, 1.55, 0]], fov: [34, 42] },
  { a: T.out1 + .7, b: T.end, orbit: { c: [0, 0, 0], r: [3.5, 3.85], a: [.05, -.3], y: [1.55, 1.5] }, q: [[0, 1.55, 0], [0, 1.52, 0]], fov: 42 },
];
function evalShot(s, t) {
  const k = (s.ease || easeIO)(win(t, s.a, s.b));
  const fov = Array.isArray(s.fov) ? lerp(s.fov[0], s.fov[1], k) : s.fov;
  let p;
  if (s.orbit) {
    const o = s.orbit, r = lerp(o.r[0], o.r[1], k), a = lerp(o.a[0], o.a[1], k);
    p = [o.c[0] + Math.sin(a) * r, lerp(o.y[0], o.y[1], k), o.c[2] + Math.cos(a) * r];
  } else p = lerpV(s.p[0], s.p[1], k);
  return [p, lerpV(s.q[0], s.q[1], k), fov];
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
let HIT_LIST = null;
function hitsAt(t) {
  HIT_LIST = HIT_LIST || [[T.claude, .5], [T.portal, 1.3], [T.followers, .6], [T.post, .7], [T.grows, .6], [T.smartest, .4], [T.in0, 1.2], [T.blowing, .5],
    [L[5] - .14, .6], [L[6] - .14, .6], [L[7] - .14, .6], [T.five5, .8], [T.rewrites, 1.0], [T.next, .5], [T.out1, 1.1], [T.agentcta, .5]];
  return HIT_LIST.reduce((a, [at_, g]) => a + pulse(t, at_, .02, .35) * g, 0);
}

// ---------------------------------------------------------------- render
function renderAt(t) {
  const tun = t < T.portal, inPhone = between(t, T.in0, T.out1), dark = between(t, T.dark0, T.out1);
  const [p, q, fov] = shot(t);
  const hits = hitsAt(t), hand = dark ? .006 : .01;
  camera.position.set(p[0] + Math.sin(t * 1.9) * hand + Math.sin(t * 91) * .02 * hits, p[1] + Math.cos(t * 1.6) * hand + Math.cos(t * 77) * .02 * hits, p[2]);
  camera.lookAt(q[0], q[1], q[2]);
  camera.rotateZ((tun ? Math.sin(t * 2.2) * .22 : Math.sin(t * .7) * .012) + Math.sin(t * 61) * .008 * hits
    + (between(t, L[5] - .14, L[6] - .14) ? Math.sin((t - L[5]) * 3) * .08 : 0) + (between(t, T.grows - .12, L[3] - .1) ? -.12 * easeIO(win(t, T.grows, L[3] - .1)) : 0));
  const snaps = [L[5] - .14, L[6] - .14, L[7] - .14, L[3] - .1, T.post + .3];
  const snap = snaps.reduce((a, c) => a + (t >= c ? (1 - easeOut(win(t, c, c + .3))) * 8 : 0), 0);
  camera.fov = fov + snap + pulse(t, T.in0, .02, .5) * 14 + pulse(t, T.out1, .02, .5) * 10 + pulse(t, T.portal, .02, .5) * 12;
  camera.updateProjectionMatrix(); camera.updateMatrixWorld();
  tunnel.visible = tun; outside.visible = !tun && !inPhone; inside.visible = inPhone;
  // light and air for each world
  const bg = tun ? BG_TUN : dark ? BG_DARK : inPhone ? BG_IN : BG_OUT;
  scene.background.copy(bg); scene.fog.color.copy(bg);
  scene.fog.near = tun ? 2 : dark ? 3 : inPhone ? 5 : 7; scene.fog.far = tun ? 15 : dark ? 11 : inPhone ? 24 : 26;
  hemi.intensity = dark ? .06 : tun ? .55 : 1.15; key.intensity = dark || tun ? 0 : 2.3; fill.intensity = dark ? 0 : tun ? .3 : .55;
  scene.environmentIntensity = dark ? .12 : tun ? .3 : .55;
  portalLight.intensity = 0;
  const focus = V(q[0], 0, q[2]);
  key.target.position.copy(focus); key.position.copy(focus).add(V(-2.2, 5, 3.6)); key.target.updateMatrixWorld();
  if (tun) animTunnel(t);
  else if (inPhone) animInside(t);
  else animOutside(t);
  if (!inPhone) spot.intensity = 0;
  animClaude(t);
  for (let i = 0; i < DUST_N; i++) {
    tP.set(p[0] + ((hash(i) * 6 + t * .05 * (hash(i + 2) - .5)) % 6) - 3, p[1] - 1.5 + ((hash(i + 1) * 4 + t * .08 + hash(i * 1.7) * 50) % 4), p[2] - .5 - hash(i + 3) * 5);
    tS.setScalar(.6 + hash(i + 4) * 1.4);
    dust.setMatrixAt(i, tM.compose(tP, camera.quaternion, tS));
  }
  dust.instanceMatrix.needsUpdate = true;
  dust.material.color.set(dark || tun ? CORAL_L : 0xfff0e0).multiplyScalar(dark || tun ? .55 : .35);
  fx.position.copy(camera.position).add(V(0, .5, -1)); fx.intensity = hits * 4 + (tun ? 3 : 0);
  // the grade: warm and clean outside and in, deep in the tunnel and the lab
  const g = grade.uniforms;
  g.uTime.value = Math.round(t * 30) / 30;
  g.uTint.value.set(dark || tun ? 1.04 : 1.0, dark || tun ? .97 : 1.0, dark ? 1.02 : .98);
  g.uGrain.value = dark || tun ? .05 : .03;
  g.uVig.value = dark ? .9 : tun ? .75 : .28;
  g.uChroma.value = hits * 1.1 + pulse(t, T.in0, .02, .4) * 2 + pulse(t, T.out1, .02, .4) * 2 + (tun ? .6 : 0);
  bloom.strength = dark ? .55 : tun ? .65 : .32; bloom.threshold = dark ? .92 : tun ? .85 : 1.05;
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
