// The Hallmark noir: the whole film in 3D. A private eye's office at night, rain and wind on the window, a violet
// NXTLVLSOCIAL.AI neon across the street. She walks in with a website Claude built her; he finds the evidence on it
// (made-up numbers, reviews from nobody, labels shouting in capitals), calls a specialist, Hallmark, which deals a design
// and checks it against the book. Same prompt, same Claude: the new page lights up in colour, the only colour in the
// film besides the neon. Everything is a pure function of time t, rendered on HyperFrames' hf-seek. Cue times come from
// the voiceover (window.NOIR_T, build/generate.py).
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { BokehPass } from "three/addons/postprocessing/BokehPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";
import { detective, client, reach, handQ, setHand, look, express, mat } from "./chars.js";

const T = window.NOIR_T;
const DEBUG_RAW = new URLSearchParams(location.search).has("raw");
const W = 1080, H = 1920;
const V = (x, y, z) => new THREE.Vector3(x, y, z);

// WebGL draws off-screen and each frame is copied into the page's 2D canvas (HyperFrames' software compositing can drop
// a band of an in-page WebGL canvas)
const glEl = document.getElementById("gl"); glEl.width = W; glEl.height = H;
const out2d = glEl.getContext("2d");
const canvas = document.createElement("canvas"); canvas.width = W; canvas.height = H;
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, powerPreference: "high-performance", preserveDrawingBuffer: true });
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.3;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x05060a);
scene.fog = new THREE.FogExp2(0x07080c, .05);
const camera = new THREE.PerspectiveCamera(35, W / H, .03, 80);

// ---------------------------------------------------------------- helpers
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, k) => a + (b - a) * k;
const easeIO = (k) => (k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
const easeOut = (k) => 1 - Math.pow(1 - k, 3);
const easeIn = (k) => k * k * k;
const win = (t, a, b) => clamp((t - a) / (b - a));
const between = (t, a, b) => t >= a && t < b;
const pulse = (t, at, up = .03, down = .3) => (t < at ? 0 : t < at + up ? (t - at) / up : Math.max(0, 1 - (t - at - up) / down));
const lerpV = (a, b, k) => a.map((x, i) => lerp(x, b[i], k));
function hash(i) { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); }
const rb = (w, h, d, r = .01, s = 2) => new RoundedBoxGeometry(w, h, d, s, Math.min(r, w / 2 - 1e-4, h / 2 - 1e-4, d / 2 - 1e-4));
function mesh(geo, m, x = 0, y = 0, z = 0, parent = scene) { const o = new THREE.Mesh(geo, m); o.position.set(x, y, z); o.castShadow = o.receiveShadow = true; if (parent) parent.add(o); return o; }
function grp(parent = scene, x = 0, y = 0, z = 0) { const g = new THREE.Group(); g.position.set(x, y, z); if (parent) parent.add(g); return g; }
function canvasTex(w, h, draw) {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  draw(c.getContext("2d"), w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; t.userData.canvas = c; return t;
}
const glow = (color, k = 1, o = {}) => new THREE.MeshBasicMaterial({ color: new THREE.Color(color).multiplyScalar(k), toneMapped: false, ...o });
function txt(g, s, x, y, size, o = {}) {
  g.font = `${o.i ? "italic " : ""}${o.w || 700} ${size}px ${o.f || "Montserrat"}`;
  g.fillStyle = o.c || "#111"; g.textAlign = o.a || "center"; g.textBaseline = "middle";
  if (o.ls) g.letterSpacing = o.ls + "px";
  g.fillText(s, x, y); g.letterSpacing = "0px";
}
const loadImg = (src) => new Promise((ok, no) => { const i = new Image(); i.onload = () => ok(i); i.onerror = no; i.src = src; });

// ---------------------------------------------------------------- post: depth of field, bloom, then the noir grade
const rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });
const composer = new EffectComposer(renderer, rt);
composer.setPixelRatio(1); composer.setSize(W, H);
composer.addPass(new RenderPass(scene, camera));
const bokeh = new BokehPass(scene, camera, { focus: 1.5, aperture: .004, maxblur: .008 });
composer.addPass(bokeh);
if (new URLSearchParams(location.search).has("nobokeh")) bokeh.enabled = false;
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), .5, .45, 2.4);
composer.addPass(bloom);
if (new URLSearchParams(location.search).has("nobloom")) bloom.enabled = false;
composer.addPass(new OutputPass());
// the colour mask: which pixels keep their colour (the neon always, the Hallmark page once it is revealed)
const maskRT = new THREE.WebGLRenderTarget(W / 4, H / 4, { type: THREE.UnsignedByteType });
const grade = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, tMask: { value: maskRT.texture }, uTime: { value: 0 }, uFlash: { value: 0 }, uFade: { value: 0 },
    uPx: { value: new THREE.Vector2(4 / W, 4 / H) } },
  vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }",
  fragmentShader: `uniform sampler2D tDiffuse, tMask; uniform float uTime, uFlash, uFade; uniform vec2 uPx; varying vec2 vUv;
    float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
    void main(){
      vec3 col = texture2D(tDiffuse, vUv).rgb;
      float m = 0.;
      for (int i = -2; i <= 2; i++) for (int j = -2; j <= 2; j++) m += texture2D(tMask, vUv + vec2(float(i), float(j)) * uPx).r;
      m = clamp(m / 25. * 1.25, 0., 1.);
      float l = dot(col, vec3(.3, .59, .11));
      l = smoothstep(.0, 1., pow(l, .95));                          // a silver-print contrast curve
      vec3 mono = vec3(l) * vec3(1., .99, .97);
      col = mix(mono, col, m);
      col += (h(floor(vUv * vec2(540., 960.)) + fract(uTime * 7.31) * 91.) - .5) * .075;
      vec2 c = (vUv - .5) * vec2(1., .68);
      col *= 1. - 1.0 * dot(c, c) * 1.5;
      col = mix(col, vec3(.92), uFlash * .5);
      col *= 1. - uFade;
      gl_FragColor = vec4(col, 1.);
    }`,
});
composer.addPass(grade);
grade.uniforms.tMask.value = maskRT.texture;   // ShaderPass clones its uniforms, which would cut the mask loose from its render target
const maskWhite = new THREE.MeshBasicMaterial({ color: 0xffffff }), maskBlack = new THREE.MeshBasicMaterial({ color: 0x000000 });

// ---------------------------------------------------------------- light
const hemi = new THREE.HemisphereLight(0x8a94b0, 0x14100c, .6); scene.add(hemi);
const fill = new THREE.DirectionalLight(0xc0c8dc, .45); fill.position.set(1.5, 2.2, 4); scene.add(fill);
const bounce = new THREE.PointLight(0xffd8b0, .9, 1.6, 1.5); bounce.position.set(-.1, .95, -.25); scene.add(bounce);
const ceiling = new THREE.PointLight(0xffe0c0, 2.2, 6, 1.3); ceiling.position.set(-.3, 2.7, .9); scene.add(ceiling);
// the desk lamp: a warm cone down onto the desk and his hands
const lampLight = new THREE.SpotLight(0xffd6a8, 4.5, 5, .95, .55, 1.4);
lampLight.position.set(-.66, 1.1, -.28); lampLight.target.position.set(-.1, .76, .0);
lampLight.castShadow = true; lampLight.shadow.mapSize.set(2048, 2048); lampLight.shadow.bias = -.0004; lampLight.shadow.radius = 3;
scene.add(lampLight, lampLight.target);
// the window light: a cold streetlight through the blinds, painting stripes across him and the room
const blindTex = canvasTex(512, 512, (g, w, h) => {
  g.fillStyle = "#000"; g.fillRect(0, 0, w, h);
  const r = g.createRadialGradient(w / 2, h / 2, 10, w / 2, h / 2, w / 2); r.addColorStop(0, "#fff"); r.addColorStop(1, "#000");
  for (let y = 0; y < h; y += 26) { g.fillStyle = r; g.fillRect(0, y + 9, w, 15); }
});
const winLight = new THREE.SpotLight(0xc8d4ff, 34, 14, .55, .35, 1.2);
winLight.position.set(.6, 2.3, -4.2); winLight.target.position.set(-.1, 1.0, .4);
winLight.map = blindTex; winLight.castShadow = true; winLight.shadow.mapSize.set(1024, 1024); winLight.shadow.bias = -.0005;
scene.add(winLight, winLight.target);
const flashLight = new THREE.DirectionalLight(0xdfe6ff, 0); flashLight.position.set(1, 4, -6); scene.add(flashLight);
const doorLight = new THREE.SpotLight(0xffe4c0, 0, 7, .7, .6, 1.3); doorLight.position.set(-3.6, 2.0, 1.4); doorLight.target.position.set(-.8, .6, .9);
doorLight.castShadow = true; doorLight.shadow.mapSize.set(1024, 1024); scene.add(doorLight, doorLight.target);
const screenLight = new THREE.PointLight(0xdfe8ff, 0, 1.6, 1.6); scene.add(screenLight);
const herLight = new THREE.SpotLight(0xfff0dc, 0, 6, .45, .6, 1.2); herLight.castShadow = true; herLight.shadow.mapSize.set(1024, 1024); scene.add(herLight, herLight.target);
const rimLight = new THREE.DirectionalLight(0xb8c4e0, .55); rimLight.position.set(-2.5, 2.4, -3.5); scene.add(rimLight);

// ---------------------------------------------------------------- the office
const RX = 2.6, BZ = -1.9, CH = 3.0;
const plank = canvasTex(1024, 1024, (g, w, h) => {
  for (let i = 0; i < 16; i++) { const v = 52 + hash(i) * 26; g.fillStyle = `rgb(${v},${v * .72},${v * .55})`; g.fillRect(0, i * 64, w, 64); g.fillStyle = "rgba(0,0,0,.45)"; g.fillRect(0, i * 64, w, 3);
    for (let k = 0; k < 40; k++) { g.fillStyle = `rgba(0,0,0,${.05 + hash(i * 40 + k) * .08})`; g.fillRect(hash(i * 7 + k) * w, i * 64 + hash(k) * 60, 120 + hash(k + 3) * 200, 2); }
    g.fillStyle = "rgba(0,0,0,.35)"; g.fillRect(hash(i + 50) * w, i * 64, 3, 64); }
});
plank.wrapS = plank.wrapT = THREE.RepeatWrapping; plank.repeat.set(3, 3);
mesh(new THREE.PlaneGeometry(RX * 2, 6).rotateX(-Math.PI / 2), mat(0xffffff, { map: plank, flatShading: false, roughness: .55 }), 0, 0, 1.1);
const paper = canvasTex(512, 512, (g, w, h) => {
  g.fillStyle = "#3a3630"; g.fillRect(0, 0, w, h);
  for (let x = 0; x < w; x += 64) { g.fillStyle = "rgba(255,240,210,.05)"; g.fillRect(x, 0, 26, h); g.fillStyle = "rgba(0,0,0,.08)"; g.fillRect(x + 30, 0, 4, h); }
  for (let i = 0; i < 1600; i++) { g.fillStyle = `rgba(0,0,0,${hash(i) * .06})`; g.fillRect(hash(i + 1) * w, hash(i + 2) * h, 3, 3); }
});
paper.wrapS = paper.wrapT = THREE.RepeatWrapping; paper.repeat.set(4, 2);
const wallM = mat(0xffffff, { map: paper, flatShading: false, roughness: .9 });
const trimM = mat(0x1e140e, { roughness: .5 });
// back wall with the window hole
const WX0 = -.95, WX1 = .95, WY0 = .95, WY1 = 2.35;
const backShape = new THREE.Shape(); backShape.moveTo(-RX, 0); backShape.lineTo(RX, 0); backShape.lineTo(RX, CH); backShape.lineTo(-RX, CH); backShape.closePath();
const hole = new THREE.Path(); hole.moveTo(WX0, WY0); hole.lineTo(WX1, WY0); hole.lineTo(WX1, WY1); hole.lineTo(WX0, WY1); hole.closePath(); backShape.holes.push(hole);
const backWall = mesh(new THREE.ShapeGeometry(backShape), wallM, 0, 0, BZ);
{ const uv = backWall.geometry.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) / 2.6, uv.getY(i) / 3); }
const sideM = wallM.clone();
const leftWall = mesh(new THREE.PlaneGeometry(6, CH).rotateY(Math.PI / 2), sideM, -RX, CH / 2, 1.1);
mesh(new THREE.PlaneGeometry(6, CH).rotateY(-Math.PI / 2), sideM, RX, CH / 2, 1.1);
mesh(new THREE.PlaneGeometry(RX * 2, 6).rotateX(Math.PI / 2), mat(0x16140f), 0, CH, 1.1);
for (const [x, z, ry, len] of [[0, BZ + .02, 0, RX * 2], [-RX + .02, 1.1, Math.PI / 2, 6], [RX - .02, 1.1, -Math.PI / 2, 6]]) {
  const b = mesh(new THREE.BoxGeometry(len, .14, .03), trimM, x, .07, z); b.rotation.y = ry;
  const c = mesh(new THREE.BoxGeometry(len, .08, .05), trimM, x, CH - .04, z); c.rotation.y = ry;
}
// the window: frame, mullion, glass with the rain running down it, and venetian blinds raised over the lower part
const frameM = mat(0x1a120c, { roughness: .45 });
for (const [x, y, w, h] of [[0, WY0 - .03, WX1 - WX0 + .12, .07], [0, WY1 + .03, WX1 - WX0 + .12, .07], [WX0 - .03, (WY0 + WY1) / 2, .07, WY1 - WY0 + .12], [WX1 + .03, (WY0 + WY1) / 2, .07, WY1 - WY0 + .12], [0, (WY0 + WY1) / 2, .04, WY1 - WY0]])
  mesh(new THREE.BoxGeometry(w, h, .08), frameM, x, y, BZ + .02);
mesh(new THREE.BoxGeometry(WX1 - WX0 + .3, .05, .26), frameM, 0, WY0 - .07, BZ + .1);
const glass = mesh(new THREE.PlaneGeometry(WX1 - WX0, WY1 - WY0), new THREE.MeshStandardMaterial({ color: 0x9aa8c0, roughness: .05, metalness: .2, transparent: true, opacity: .12 }), 0, (WY0 + WY1) / 2, BZ + .005);
glass.castShadow = false;
const SLATS = [], SLAT_N = 22, BLIND_TOP = WY1 - .02;
const slatM = mat(0xb8b0a0, { roughness: .6 });
for (let i = 0; i < SLAT_N; i++) {
  const y = BLIND_TOP - i * .028;
  const s = mesh(new THREE.BoxGeometry(WX1 - WX0 + .04, .004, .026), slatM, 0, y, BZ + .07);
  SLATS.push(s);
}
mesh(new THREE.BoxGeometry(WX1 - WX0 + .1, .04, .05), slatM, 0, BLIND_TOP + .03, BZ + .07);
const bottomRail = mesh(new THREE.BoxGeometry(WX1 - WX0 + .06, .016, .03), slatM, 0, BLIND_TOP - SLAT_N * .028, BZ + .07);
for (const x of [-.6, .6]) mesh(new THREE.CylinderGeometry(.002, .002, SLAT_N * .028 + .05, 4), slatM, x, BLIND_TOP - SLAT_N * .014, BZ + .085);
// drops on the glass: little streaks that run down and wander
const DROP_N = 160;
const dropM = new THREE.MeshBasicMaterial({ color: 0xcfd8ec, transparent: true, opacity: .5, depthWrite: false, toneMapped: false });
const drops = new THREE.InstancedMesh(new THREE.PlaneGeometry(.006, .03), dropM, DROP_N); drops.frustumCulled = false; scene.add(drops);
// outside: rain, the street lamp, buildings with lit windows, the violet neon
const RAIN_N = 700;
const rain = new THREE.InstancedMesh(new THREE.PlaneGeometry(.008, .4), new THREE.MeshBasicMaterial({ color: 0xc0cce6, transparent: true, opacity: .4, depthWrite: false, toneMapped: false }), RAIN_N);
rain.frustumCulled = false; scene.add(rain);
const bldM = mat(0x0b0c10, { roughness: 1 });
const litTex = canvasTex(256, 512, (g, w, h) => {
  g.fillStyle = "#07080b"; g.fillRect(0, 0, w, h);
  for (let y = 10; y < h; y += 34) for (let x = 10; x < w; x += 30) { const on = hash(x * 3 + y) > .62; g.fillStyle = on ? `rgba(255,${210 + hash(x + y) * 30},150,${.5 + hash(y + x * 7) * .5})` : "#0c0d12"; g.fillRect(x, y, 16, 22); }
});
const litM = new THREE.MeshBasicMaterial({ map: litTex, toneMapped: false, fog: false });
for (const [x, w, h, z] of [[-3.5, 3, 9, -9], [-.6, 2.4, 12, -12], [2.3, 3.2, 8, -8], [5.2, 2.8, 10, -11], [-6.4, 2.6, 7, -10]]) {
  const b = mesh(new THREE.BoxGeometry(w, h, 2), [bldM, bldM, bldM, bldM, litM, bldM], x, h / 2 - 1, z); b.castShadow = false;
}
const neon = grp(scene, .38, 2.0, -5.2);
let neonMat = null;
// the street lamp outside, a soft halo
const halo = mesh(new THREE.PlaneGeometry(1.4, 1.4), new THREE.MeshBasicMaterial({ map: canvasTex(128, 128, (g, w) => { const r = g.createRadialGradient(w / 2, w / 2, 0, w / 2, w / 2, w / 2); r.addColorStop(0, "rgba(255,240,220,.9)"); r.addColorStop(.25, "rgba(255,230,200,.25)"); r.addColorStop(1, "rgba(0,0,0,0)"); g.fillStyle = r; g.fillRect(0, 0, w, w); }), transparent: true, depthWrite: false, toneMapped: false, blending: THREE.AdditiveBlending, fog: false }), -1.4, 2.9, -6);
halo.castShadow = false;

// the door, with frosted glass lettered from the other side
const DOORZ = 1.4, DOORW = .92, DOORH = 2.12;
const doorPivot = grp(scene, -RX + .03, 0, DOORZ + DOORW / 2);
const doorTex = canvasTex(512, 640, (g, w, h) => {
  g.fillStyle = "#c8ccd2"; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 3000; i++) { g.fillStyle = `rgba(255,255,255,${hash(i) * .12})`; g.fillRect(hash(i + 1) * w, hash(i + 2) * h, 2, 2); }
  g.save(); g.translate(w, 0); g.scale(-1, 1);
  txt(g, "SAM MARLOWE", w / 2, 210, 54, { f: "Montserrat", w: 800, c: "#1b1a1c", ls: 4 });
  txt(g, "PRIVATE INVESTIGATOR", w / 2, 290, 34, { f: "Montserrat", w: 700, c: "#1b1a1c", ls: 6 });
  g.restore();
});
const doorM = mat(0x2a1b12, { roughness: .5 });
const door = grp(doorPivot, 0, 0, -DOORW / 2); door.rotation.y = Math.PI / 2;
mesh(new THREE.BoxGeometry(DOORW, .7, .05), doorM, 0, .35, 0, door);
mesh(new THREE.BoxGeometry(DOORW, .25, .05), doorM, 0, DOORH - .125, 0, door);
for (const s of [1, -1]) mesh(new THREE.BoxGeometry(.12, DOORH, .05), doorM, s * (DOORW / 2 - .06), DOORH / 2, 0, door);
const frosted = mesh(new THREE.PlaneGeometry(DOORW - .24, DOORH - .95), new THREE.MeshStandardMaterial({ map: doorTex, roughness: .3, emissive: 0xffffff, emissiveMap: doorTex, emissiveIntensity: .25, transparent: true, opacity: .95 }), 0, .7 + (DOORH - .95) / 2, 0, door);
frosted.rotation.y = 0;
mesh(new THREE.SphereGeometry(.03, 8, 6), mat(0xb89a50, { metalness: .8, roughness: .3, flatShading: false }), DOORW / 2 - .1, 1.0, .05, door);
// the hall behind the door: a bright wedge of light
const hallM = new THREE.MeshBasicMaterial({ color: new THREE.Color(0xfff0dc).multiplyScalar(1.6), toneMapped: false });
mesh(new THREE.PlaneGeometry(DOORW, DOORH).rotateY(Math.PI / 2), hallM, -RX - .4, DOORH / 2, DOORZ);
for (const [y, h] of [[DOORH + .05, .1]]) mesh(new THREE.BoxGeometry(.08, h, DOORW + .16), frameM, -RX + .02, y, DOORZ);
for (const s of [1, -1]) mesh(new THREE.BoxGeometry(.08, DOORH, .08), frameM, -RX + .02, DOORH / 2, DOORZ + s * (DOORW / 2 + .04));
// the left wall needs a hole for the door: cover it with two panels instead of the plain plane
leftWall.visible = false;
for (const [z0, z1] of [[-1.9, DOORZ - DOORW / 2], [DOORZ + DOORW / 2, 4.1]]) mesh(new THREE.PlaneGeometry(z1 - z0, CH).rotateY(Math.PI / 2), sideM, -RX, CH / 2, (z0 + z1) / 2);
mesh(new THREE.PlaneGeometry(DOORW, CH - DOORH).rotateY(Math.PI / 2), sideM, -RX, DOORH + (CH - DOORH) / 2, DOORZ);

// the corkboard on the right wall, covered in sites that all look the same
const CORK = { x: RX - .03, y: 1.55, z: .55, w: 1.9, h: 1.15 };
const corkTex = canvasTex(512, 512, (g, w, h) => { g.fillStyle = "#6a4a2e"; g.fillRect(0, 0, w, h); for (let i = 0; i < 9000; i++) { g.fillStyle = `rgba(${hash(i) > .5 ? 40 : 140},${hash(i) > .5 ? 26 : 100},${hash(i) > .5 ? 14 : 60},.35)`; g.fillRect(hash(i + 1) * w, hash(i + 2) * h, 3, 2); } });
const cork = grp(scene, CORK.x, CORK.y, CORK.z); cork.rotation.y = -Math.PI / 2;
mesh(new THREE.BoxGeometry(CORK.w, CORK.h, .03), mat(0xffffff, { map: corkTex, flatShading: false }), 0, 0, 0, cork);
for (const [x, y, w, h] of [[0, CORK.h / 2 + .02, CORK.w + .08, .04], [0, -CORK.h / 2 - .02, CORK.w + .08, .04], [-CORK.w / 2 - .02, 0, .04, CORK.h + .08], [CORK.w / 2 + .02, 0, .04, CORK.h + .08]])
  mesh(new THREE.BoxGeometry(w, h, .05), frameM, x, y, .01, cork);
const PRINTS = [];
const pinM = mat(0xa01818, { roughness: .3 });

// ---------------------------------------------------------------- the desk and what is on it
const woodTex = canvasTex(512, 256, (g, w, h) => { g.fillStyle = "#3e2618"; g.fillRect(0, 0, w, h); for (let i = 0; i < 120; i++) { g.strokeStyle = `rgba(${hash(i) > .5 ? 20 : 90},${hash(i) > .5 ? 10 : 56},${hash(i) > .5 ? 4 : 34},.35)`; g.lineWidth = 1 + hash(i + 3) * 2; g.beginPath(); const y = hash(i + 1) * h; g.moveTo(0, y); g.bezierCurveTo(w * .3, y + (hash(i + 5) - .5) * 20, w * .7, y + (hash(i + 6) - .5) * 20, w, y + (hash(i + 7) - .5) * 10); g.stroke(); } });
const woodM = mat(0xffffff, { map: woodTex, flatShading: false, roughness: .42 });
const DESK_Y = .76;
mesh(rb(1.76, .055, .94, .012, 2), woodM, 0, DESK_Y - .0275, 0);
mesh(new THREE.BoxGeometry(1.68, .64, .88), mat(0x2a1a10, { roughness: .6 }), 0, .38, -.02);
for (const s of [-1, 1]) for (let k = 0; k < 3; k++) { mesh(new THREE.BoxGeometry(.5, .17, .02), mat(0x3a2416, { roughness: .5 }), s * .52, .58 - k * .2, .43); mesh(new THREE.BoxGeometry(.1, .018, .02), mat(0xb08c48, { metalness: .8, roughness: .3, flatShading: false }), s * .52, .6 - k * .2, .445); }
mesh(new THREE.BoxGeometry(.9, .06, .015), mat(0x2a1a10), 0, .7, .447);
// blotter
mesh(new THREE.BoxGeometry(.8, .006, .5), mat(0x1d2a22, { roughness: .9 }), 0, DESK_Y + .003, -.12);
// the banker's lamp
const lamp = grp(scene, -.74, DESK_Y, -.36);
mesh(new THREE.CylinderGeometry(.08, .095, .03, 12), mat(0x9a7a3c, { metalness: .8, roughness: .3, flatShading: false }), 0, .015, 0, lamp);
mesh(new THREE.CylinderGeometry(.01, .01, .3, 8), mat(0x9a7a3c, { metalness: .8, roughness: .3 }), 0, .17, 0, lamp);
const shade = mesh(new THREE.CylinderGeometry(.07, .11, .24, 14, 1, true, 0, Math.PI).rotateZ(Math.PI / 2).rotateY(Math.PI / 2), mat(0x0e2a1a, { roughness: .2, metalness: .1, flatShading: false }), .02, .33, .02, lamp);
mesh(new THREE.CylinderGeometry(.069, .109, .238, 14, 1, true, 0, Math.PI).rotateZ(Math.PI / 2).rotateY(Math.PI / 2), mat(0x3a3428, { roughness: .9, side: THREE.BackSide }), .02, .33, .02, lamp);
const bulb = mesh(new THREE.SphereGeometry(.03, 10, 8), glow(0xfff0d0, 5), .02, .31, .02, lamp); bulb.castShadow = false;
// the rotary phone
const phone = grp(scene, .55, DESK_Y, -.24); phone.rotation.y = -.5;
const bake = mat(0x101012, { roughness: .25 });
mesh(rb(.2, .09, .22, .03, 3), bake, 0, .045, 0, phone);
mesh(new THREE.CylinderGeometry(.075, .075, .012, 20).rotateX(-.35), mat(0xd8d2c4, { roughness: .4, flatShading: false }), 0, .098, .055, phone);
const dial = grp(phone, 0, .104, .057); dial.rotation.x = -.35;
const dialTex = canvasTex(256, 256, (g, w) => { g.fillStyle = "#151517"; g.beginPath(); g.arc(w / 2, w / 2, w / 2, 0, 7); g.fill(); for (let i = 0; i < 10; i++) { const a = -Math.PI * .35 + i * .5; g.fillStyle = "#e8e2d4"; g.beginPath(); g.arc(w / 2 + Math.cos(a) * 88, w / 2 + Math.sin(a) * 88, 22, 0, 7); g.fill(); } g.fillStyle = "#e8e2d4"; g.beginPath(); g.arc(w / 2, w / 2, 40, 0, 7); g.fill(); });
mesh(new THREE.CircleGeometry(.074, 24).rotateX(-Math.PI / 2), new THREE.MeshStandardMaterial({ map: dialTex, roughness: .3 }), 0, .001, 0, dial);
const handset = grp(scene, 0, 0, 0);
mesh(rb(.22, .03, .045, .014, 2), bake, 0, 0, 0, handset);
for (const s of [-1, 1]) mesh(new THREE.CylinderGeometry(.03, .025, .045, 12), bake, s * .1, -.02, 0, handset);
const cradle = new THREE.Vector3(0, .13, -.005); // on the phone, in phone space
// the laptop: a base and a hinged lid whose screen is a live canvas
const laptop = grp(scene);
const lapM = mat(0x2c2e33, { roughness: .35, metalness: .4, flatShading: false });
mesh(rb(.34, .016, .24, .006, 2), lapM, 0, .008, 0, laptop);
const keysTex = canvasTex(512, 256, (g, w, h) => { g.fillStyle = "#1b1c20"; g.fillRect(0, 0, w, h); for (let r = 0; r < 5; r++) for (let c = 0; c < 14; c++) { g.fillStyle = "#3a3c42"; g.fillRect(14 + c * 34.5, 18 + r * 34, 29, 28); } g.fillStyle = "#3a3c42"; g.fillRect(150, 196, 200, 28); g.fillStyle = "#2a2c31"; g.fillRect(180, 232, 150, 20); });
const keys = mesh(new THREE.PlaneGeometry(.3, .15).rotateX(-Math.PI / 2), new THREE.MeshStandardMaterial({ map: keysTex, roughness: .6 }), 0, .0165, -.03, laptop);
keys.rotation.y = Math.PI;
const lid = grp(laptop, 0, .016, .115);    // the hinge, at the back edge (away from him)
mesh(rb(.34, .222, .01, .006, 2).translate(0, .111, 0), lapM, 0, 0, 0, lid);
const screenCanvas = document.createElement("canvas"); screenCanvas.width = 1280; screenCanvas.height = 800;
const sg = screenCanvas.getContext("2d");
const screenTex = new THREE.CanvasTexture(screenCanvas); screenTex.colorSpace = THREE.SRGBColorSpace; screenTex.anisotropy = 8;
const screenM = new THREE.MeshBasicMaterial({ map: screenTex, toneMapped: false, color: 0xbdbdbd });
const screen = mesh(new THREE.PlaneGeometry(.32, .2), screenM, 0, .111, -.0055, lid); screen.rotation.y = Math.PI; screen.castShadow = false;
// the magnifying glass
const loupe = grp(scene);
mesh(new THREE.TorusGeometry(.06, .007, 8, 28), mat(0x1a1a1c, { metalness: .6, roughness: .3, flatShading: false }), 0, 0, 0, loupe);
const lensCanvas = document.createElement("canvas"); lensCanvas.width = lensCanvas.height = 512;
const lensTex = new THREE.CanvasTexture(lensCanvas); lensTex.colorSpace = THREE.SRGBColorSpace;
const lens = mesh(new THREE.CircleGeometry(.059, 32), new THREE.MeshBasicMaterial({ map: lensTex, toneMapped: false }), 0, 0, .001, loupe); lens.castShadow = false;
mesh(new THREE.CylinderGeometry(.009, .011, .11, 10), mat(0x2a1a10, { roughness: .4 }), 0, -.12, 0, loupe);
mesh(new THREE.CylinderGeometry(.01, .01, .012, 10), mat(0x9a7a3c, { metalness: .8, roughness: .3 }), 0, -.066, 0, loupe);
// the evidence markers: yellow tents, 1 2 3
const MARKERS = [1, 2, 3].map((n) => {
  const tx = canvasTex(256, 256, (g, w) => { g.fillStyle = "#e8c020"; g.fillRect(0, 0, w, w); txt(g, String(n), w / 2, w / 2 + 6, 170, { w: 800, c: "#111" }); });
  const m = grp(scene);
  const face = new THREE.MeshStandardMaterial({ map: tx, roughness: .5 }), side = mat(0xe8c020, { roughness: .5 });
  for (const s of [1, -1]) { const p = mesh(new THREE.PlaneGeometry(.07, .08), face, 0, .036, s * .018, m); p.rotation.x = s * .42; p.rotation.y = s > 0 ? 0 : Math.PI; }
  m.visible = false; return m;
});
// the business card
const cardTex = canvasTex(1024, 580, (g, w, h) => {
  g.fillStyle = "#f2ede2"; g.fillRect(0, 0, w, h);
  g.strokeStyle = "#1a1a1a"; g.lineWidth = 6; g.strokeRect(34, 34, w - 68, h - 68);
  txt(g, "HALLMARK", w / 2, 210, 132, { w: 800, c: "#141414", ls: 10 });
  txt(g, "design specialist", w / 2, 320, 64, { f: "ISerif", i: true, w: 400, c: "#2a2a2a" });
  txt(g, "A free skill for Claude Code", w / 2, 404, 40, { w: 600, c: "#2a2a2a" });
  txt(g, "github.com/Nutlope/hallmark", w / 2, 476, 34, { f: "JBMono", w: 700, c: "#3a3a3a" });
});
const card = mesh(new THREE.BoxGeometry(.17, .002, .096), [mat(0xf2ede2), mat(0xf2ede2), new THREE.MeshStandardMaterial({ map: cardTex, roughness: .7 }), mat(0xf2ede2), mat(0xf2ede2), mat(0xf2ede2)]);
// the dealt designs: five of Hallmark's real themes, as cards
const THEMES = [["Hum", "card stock, torn edges", ["#efe9dc", "#f0c419", "#3b6fb6", "#e35d4f"]], ["Coral", "warm grey, one coral signal", ["#ece8e3", "#f06b4f", "#2b2b2b", "#bdb5ab"]],
  ["Ink", "civic, monochrome", ["#f4f1ea", "#111111", "#6f6f6f", "#d0ccc2"]], ["Riso", "two-colour print", ["#f3efe6", "#ff5aa5", "#2d6bff", "#1b1b1b"]], ["Cobalt", "deep blue, precise", ["#eef1f7", "#1f3fbf", "#0b1440", "#9fb3ff"]]];
const DEAL = THEMES.map(([name, sub, sw], i) => {
  const tx = canvasTex(512, 720, (g, w, h) => {
    g.fillStyle = "#f4f0e6"; g.fillRect(0, 0, w, h); g.strokeStyle = "#1a1a1a"; g.lineWidth = 5; g.strokeRect(22, 22, w - 44, h - 44);
    sw.forEach((c, k) => { g.fillStyle = c; g.fillRect(48 + k * 106, 70, 96, 300); });
    txt(g, name, w / 2, 470, 96, { w: 800, c: "#141414" }); txt(g, sub, w / 2, 560, 34, { f: "ISerif", i: true, w: 400, c: "#333" });
    txt(g, `THEME ${String(i + 1).padStart(2, "0")} / 50`, w / 2, 640, 26, { f: "JBMono", w: 700, c: "#555" });
  });
  const back = canvasTex(256, 360, (g, w, h) => { g.fillStyle = "#151515"; g.fillRect(0, 0, w, h); g.strokeStyle = "#d8d2c4"; g.lineWidth = 4; g.strokeRect(14, 14, w - 28, h - 28); txt(g, "H", w / 2, h / 2 + 4, 120, { w: 800, c: "#d8d2c4" }); });
  return mesh(new THREE.BoxGeometry(.088, .0015, .124), [mat(0xf4f0e6), mat(0xf4f0e6), new THREE.MeshStandardMaterial({ map: tx, roughness: .6 }), new THREE.MeshStandardMaterial({ map: back, roughness: .6 }), mat(0xf4f0e6), mat(0xf4f0e6)]);
});
// the book: Hallmark's Floor, the giveaways it never allows
const RULES = ["No invented metrics", "No fake testimonials", "No eyebrow labels", "No emoji as icons", "No purple-blue gradients", "No card inside a card"];
const book = grp(scene);
const coverTex = canvasTex(512, 700, (g, w, h) => { g.fillStyle = "#1c1c1e"; g.fillRect(0, 0, w, h); g.strokeStyle = "#c8c2b4"; g.lineWidth = 6; g.strokeRect(30, 30, w - 60, h - 60); txt(g, "THE", w / 2, 230, 50, { w: 700, c: "#c8c2b4", ls: 12 }); txt(g, "FLOOR", w / 2, 320, 110, { w: 800, c: "#e8e2d4", ls: 6 }); txt(g, "every giveaway, banned", w / 2, 420, 34, { f: "ISerif", i: true, w: 400, c: "#c8c2b4" }); txt(g, "HALLMARK", w / 2, 590, 34, { w: 800, c: "#c8c2b4", ls: 8 }); });
const pageCanvas = document.createElement("canvas"); pageCanvas.width = 1024; pageCanvas.height = 700;
const pageTex = new THREE.CanvasTexture(pageCanvas); pageTex.colorSpace = THREE.SRGBColorSpace;
const pagesM = mat(0xe8e2d2, { roughness: .9 });
mesh(new THREE.BoxGeometry(.34, .03, .235), pagesM, 0, .015, 0, book);
mesh(new THREE.PlaneGeometry(.33, .225).rotateX(-Math.PI / 2), new THREE.MeshStandardMaterial({ map: pageTex, roughness: .85 }), 0, .0305, 0, book);
const bookCover = grp(book, -.17, .032, 0);
mesh(new THREE.BoxGeometry(.172, .006, .24), [mat(0x1c1c1e), mat(0x1c1c1e), new THREE.MeshStandardMaterial({ map: coverTex, roughness: .7 }), mat(0x1c1c1e), mat(0x1c1c1e), mat(0x1c1c1e)], .086, 0, 0, bookCover);
const coverR = mesh(new THREE.BoxGeometry(.172, .006, .24), mat(0x1c1c1e), .086 + .17, -.032, 0, book); coverR.visible = false;
// the case file and the rubber stamp
const folderTex = canvasTex(1024, 720, (g, w, h) => { g.fillStyle = "#c9a86a"; g.fillRect(0, 0, w, h); for (let i = 0; i < 2000; i++) { g.fillStyle = `rgba(80,50,20,${hash(i) * .08})`; g.fillRect(hash(i + 1) * w, hash(i + 2) * h, 4, 2); } txt(g, "CASE FILE  No. 047", 70, 110, 52, { a: "left", w: 800, c: "#2a1e10", ls: 3 }); txt(g, "Client: Tally", 70, 190, 44, { a: "left", f: "JBMono", w: 700, c: "#3a2a16" }); txt(g, "Charge: looked like every other site", 70, 250, 36, { a: "left", f: "JBMono", w: 400, c: "#3a2a16" }); });
const stampCanvas = document.createElement("canvas"); stampCanvas.width = 1024; stampCanvas.height = 720;
const folderC = stampCanvas.getContext("2d");
const folderLive = new THREE.CanvasTexture(stampCanvas); folderLive.colorSpace = THREE.SRGBColorSpace;
const folder = grp(scene);
mesh(new THREE.BoxGeometry(.32, .008, .225), [mat(0xc9a86a), mat(0xc9a86a), new THREE.MeshStandardMaterial({ map: folderLive, roughness: .8 }), mat(0xc9a86a), mat(0xc9a86a), mat(0xc9a86a)], 0, .004, 0, folder);
const stamp = grp(scene);
mesh(new THREE.CylinderGeometry(.018, .024, .07, 10), mat(0x3a2414, { roughness: .4 }), 0, .095, 0, stamp);
mesh(new THREE.SphereGeometry(.03, 10, 8), mat(0x3a2414, { roughness: .4 }), 0, .14, 0, stamp);
mesh(rb(.085, .03, .05, .006, 2), mat(0x1a1a1a, { roughness: .6 }), 0, .045, 0, stamp);
mesh(new THREE.BoxGeometry(.08, .012, .046), mat(0x8a1414, { roughness: .8 }), 0, .022, 0, stamp);
// the coffee mug, steaming
const mug = grp(scene, -.32, DESK_Y, .08);
mesh(new THREE.CylinderGeometry(.04, .036, .095, 12), mat(0xe8e2d4, { roughness: .35, flatShading: false }), 0, .0475, 0, mug);
mesh(new THREE.TorusGeometry(.024, .007, 6, 12, Math.PI).rotateZ(-Math.PI / 2), mat(0xe8e2d4, { roughness: .35 }), .045, .05, 0, mug);
mesh(new THREE.CircleGeometry(.036, 12).rotateX(-Math.PI / 2), mat(0x1a0e08, { roughness: .1 }), 0, .085, 0, mug);
const STEAM_N = 18;
const steamTex = canvasTex(64, 64, (g, w) => { const r = g.createRadialGradient(w / 2, w / 2, 0, w / 2, w / 2, w / 2); r.addColorStop(0, "rgba(255,255,255,.5)"); r.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = r; g.fillRect(0, 0, w, w); });
const steam = new THREE.InstancedMesh(new THREE.PlaneGeometry(.05, .05), new THREE.MeshBasicMaterial({ map: steamTex, transparent: true, depthWrite: false, opacity: .35 }), STEAM_N);
steam.frustumCulled = false; scene.add(steam);
// a stack of papers that lifts in the draught, a filing cabinet, a coat rack, the chair
const PAPERS = [];
for (let i = 0; i < 4; i++) { const p = mesh(new THREE.BoxGeometry(.21, .0015, .29), mat(0xe8e2d2, { roughness: .9 }), .62 + i * .006, DESK_Y + .002 + i * .0016, .2 + i * .004); p.rotation.y = .4 + i * .08; PAPERS.push([p, p.position.clone(), p.rotation.y]); }
const cab = grp(scene, 2.05, 0, -1.55);
mesh(new THREE.BoxGeometry(.5, 1.3, .6), mat(0x3a3c3a, { roughness: .5, metalness: .3 }), 0, .65, 0, cab);
for (let k = 0; k < 4; k++) { mesh(new THREE.BoxGeometry(.46, .29, .01), mat(0x454846, { roughness: .45, metalness: .3 }), 0, .17 + k * .31, .305, cab); mesh(new THREE.BoxGeometry(.12, .02, .03), mat(0x9a9a92, { metalness: .8, roughness: .3 }), 0, .26 + k * .31, .315, cab); }
const rack = grp(scene, -2.2, 0, -1.35);
mesh(new THREE.CylinderGeometry(.02, .025, 1.8, 8), mat(0x2a1a10), 0, .9, 0, rack);
mesh(new THREE.CylinderGeometry(.2, .22, .03, 10), mat(0x2a1a10), 0, .015, 0, rack);
for (let k = 0; k < 4; k++) { const a = k * Math.PI / 2; const hk = mesh(new THREE.CylinderGeometry(.008, .008, .16, 6), mat(0x2a1a10), Math.cos(a) * .06, 1.72, Math.sin(a) * .06, rack); hk.rotation.set(Math.sin(a) * .8, 0, -Math.cos(a) * .8); }
mesh(new THREE.CylinderGeometry(.16, .22, .7, 8, 1, true), mat(0x2c2a2e, { side: THREE.DoubleSide }), .06, 1.35, 0, rack);
const chair = grp(scene, 0, 0, -.78);
mesh(rb(.5, .07, .48, .02, 2), mat(0x2a1810, { roughness: .5 }), 0, .45, 0, chair);
mesh(rb(.5, .55, .07, .03, 2), mat(0x2a1810, { roughness: .5 }), 0, .78, -.22, chair);
mesh(new THREE.CylinderGeometry(.03, .03, .42, 8), mat(0x1a1a1a, { metalness: .5 }), 0, .23, 0, chair);
mesh(new THREE.CylinderGeometry(.26, .26, .02, 5), mat(0x1a1a1a, { metalness: .5 }), 0, .03, 0, chair);
// a framed licence and a clock on the back wall
const lic = canvasTex(512, 380, (g, w, h) => { g.fillStyle = "#e6dcc4"; g.fillRect(0, 0, w, h); txt(g, "LICENSED", w / 2, 110, 54, { w: 800, c: "#2a2418", ls: 6 }); txt(g, "Private Investigator", w / 2, 190, 40, { f: "ISerif", i: true, w: 400, c: "#2a2418" }); txt(g, "No. 047 . City of Los Angeles", w / 2, 270, 26, { f: "JBMono", w: 400, c: "#3a3020" }); });
mesh(new THREE.BoxGeometry(.5, .38, .03), frameM, -1.65, 1.8, BZ + .02);
mesh(new THREE.PlaneGeometry(.44, .32), new THREE.MeshStandardMaterial({ map: lic, roughness: .8 }), -1.65, 1.8, BZ + .04);

// ---------------------------------------------------------------- the cast
const D = detective(); scene.add(D.root); D.root.position.set(0, 0, -.7);
const C = client(); scene.add(C.root);
// the beauty light: a soft key on her face, as the old films lit their leading lady
const beauty = new THREE.PointLight(0xfff0e4, .5, 1.0, 1.4); beauty.position.set(.12, .14, .5); C.head.add(beauty);

// ---------------------------------------------------------------- the screens
let IMG = {};
const SCREEN = { before: [[0, 0], [640, 0], [2690, 0], [1080, 0]], after: 0 };
const PROMPT = "/hallmark Build a landing page for Tally, an app that splits group expenses with friends.";
function drawPage(img, y, fade = 1) {
  sg.globalAlpha = 1; sg.fillStyle = "#fff"; sg.fillRect(0, 0, 1280, 800);
  const yy = clamp(y, 0, img.height - 800);
  sg.globalAlpha = fade; sg.drawImage(img, 0, yy, 1280, 800, 0, 0, 1280, 800); sg.globalAlpha = 1;
  return yy;
}
function drawTerminal(t) {
  sg.fillStyle = "#121316"; sg.fillRect(0, 0, 1280, 800);
  sg.fillStyle = "#1e2026"; sg.fillRect(0, 0, 1280, 56);
  for (let i = 0; i < 3; i++) { sg.fillStyle = ["#5a5c62", "#5a5c62", "#5a5c62"][i]; sg.beginPath(); sg.arc(34 + i * 30, 28, 9, 0, 7); sg.fill(); }
  txt(sg, "Claude Code", 640, 28, 24, { f: "JBMono", w: 700, c: "#9a9ca4" });
  const n = Math.floor(clamp(win(t, T.same - .1, T.same + 1.15)) * PROMPT.length);
  const words = PROMPT.slice(0, n);
  sg.font = "700 40px JBMono"; sg.fillStyle = "#e8e6e0"; sg.textAlign = "left"; sg.textBaseline = "top";
  const lines = []; let cur = "> ";
  for (const w of words.split(" ")) { if (sg.measureText(cur + w).width > 1140) { lines.push(cur); cur = "  "; } cur += w + " "; }
  lines.push(cur.trimEnd());
  lines.forEach((ln, i) => sg.fillText(ln, 64, 120 + i * 58));
  if (Math.floor(t * 3) % 2 === 0 || n < PROMPT.length) { const last = lines[lines.length - 1]; sg.fillRect(64 + sg.measureText(last).width + 6, 122 + (lines.length - 1) * 58, 22, 44); }
  if (t > T.same2) { txt(sg, "Hallmark  .  building", 64, 470, 34, { a: "left", f: "JBMono", w: 700, c: "#9a9ca4" }); const k = win(t, T.same2, T.no - .1); sg.fillStyle = "#2a2c32"; sg.fillRect(64, 520, 1152, 18); sg.fillStyle = "#e8e6e0"; sg.fillRect(64, 520, 1152 * easeIO(k), 18); }
}
function drawLens(cx, cy, z = 3.0) {
  const lg = lensCanvas.getContext("2d"), r = 512 / 2 / z;
  lg.fillStyle = "#fff"; lg.fillRect(0, 0, 512, 512);
  lg.drawImage(screenCanvas, cx - r, cy - r, r * 2, r * 2, 0, 0, 512, 512);
  const v = lg.createRadialGradient(256, 256, 170, 256, 256, 256); v.addColorStop(0, "rgba(0,0,0,0)"); v.addColorStop(1, "rgba(0,0,0,.45)"); lg.fillStyle = v; lg.fillRect(0, 0, 512, 512);
  const hl = lg.createLinearGradient(80, 60, 300, 260); hl.addColorStop(0, "rgba(255,255,255,.45)"); hl.addColorStop(1, "rgba(255,255,255,0)"); lg.fillStyle = hl; lg.beginPath(); lg.ellipse(190, 150, 120, 60, -.7, 0, 7); lg.fill();
  lensTex.needsUpdate = true;
}
// a point on the screen, in page pixels of the 1280x800 view, as a world position
function screenPoint(px, py, off = 0) {
  screen.updateMatrixWorld(true);
  return screen.localToWorld(V((px / 1280 - .5) * -.32 * -1, (.5 - py / 800) * .2, off));
}

// ---------------------------------------------------------------- the story
// her walk: from the door to the front of the desk
const DOOR_IN = V(-RX - .2, 0, DOORZ), STAND = V(-.42, 0, .86);
function clientPos(t) {
  const k = easeIO(win(t, T.enter, T.arrive));
  const p = DOOR_IN.clone().lerp(STAND, k);
  return { p, walking: k > 0 && k < 1, k };
}
// where the laptop is: in her arms, then set down and opened in front of him
const LAP_DESK = V(0, DESK_Y, -.16);
function laptopAt(t) {
  if (t < T.place) {
    const c = clientPos(t);
    const fwd = V(Math.sin(C.root.rotation.y), 0, Math.cos(C.root.rotation.y));
    const p = c.p.clone().add(fwd.multiplyScalar(.2)).add(V(0, 1.12, 0));
    return { p, ry: C.root.rotation.y, rx: -Math.PI / 2 + .15, open: 0 };
  }
  const k = easeIO(win(t, T.place, T.place + .7));
  const start = laptopAt(T.place - .001);
  const p = start.p.clone().lerp(LAP_DESK, k);
  p.y += Math.sin(k * Math.PI) * .05;
  let ry = start.ry; while (ry > Math.PI) ry -= Math.PI * 2;
  return { p, ry: lerp(ry, 0, k), rx: lerp(start.rx, 0, k), open: easeOut(win(t, T.place + .55, T.place + 1.2)) };
}

// shots: [start, end, cam from, cam to, look from, look to, fov, focus distance or "subject"]
let SHOTS = null;
function buildShots() {
  const S = [];
  const add = (a, b, p0, p1, q0, q1, fov, ap = .003) => S.push({ a, b, p0, p1, q0, q1, fov, ap });
  const c = T.cut;
  add(0, c[1], [.18, 1.08, 1.35], [.12, 1.12, .95], [0, 1.24, -.7], [0, 1.25, -.7], 30, .003);              // him at the desk, the rain and the neon behind
  add(c[1], c[2], [1.9, 1.55, 3.3], [1.5, 1.45, 2.9], [-1.4, 1.1, .9], [-.6, 1.05, .5], 34, .002);               // the door, she walks in
  add(c[2], c[3], [-.5, 1.45, -1.2], [-.44, 1.42, -1.1], [.02, .9, .0], [.02, .89, .0], 26, .003);           // over his shoulder: the site
  add(c[3], c[4], [-.2, 1.16, .75], [-.17, 1.17, .6], [0, 1.22, -.65], [0, 1.22, -.65], 28, .003);             // his face in the screen glow
  add(c[4], c[5], [1.05, 1.55, 1.05], [1.15, 1.55, .15], [2.55, 1.55, 1.0], [2.55, 1.55, .1], 40, .0025);     // the corkboard
  add(c[5], c[6], [-.46, 1.36, -1.02], [-.42, 1.33, -.95], [.01, .9, .0], [.01, .9, .0], 18, .003);         // the evidence, through the glass
  add(c[6], c[7], [.55, 1.25, .75], [.45, 1.22, .62], [0, 1.15, -.7], [0, 1.15, -.7], 30, .0035);             // the culprit: his face
  add(c[7], c[8], [1.05, 1.15, .45], [.95, 1.12, .35], [.3, 1.05, -.55], [.3, 1.08, -.55], 32, .003);         // the call
  add(c[8], c[9], [.3, 1.28, -.66], [.3, 1.24, -.63], [.3, DESK_Y, -.38], [.3, DESK_Y, -.38], 30, .003);     // the card
  add(c[9], c[10], [.02, 1.72, .62], [.0, 1.62, .56], [0, DESK_Y, .2], [0, DESK_Y, .16], 32, .003);           // the deal and the book
  add(c[10], c[11], [-.5, 1.42, -1.15], [-.44, 1.38, -1.05], [.02, .86, -.05], [.02, .86, -.05], 24, .003);  // same prompt: his hands on the keys
  add(c[11], c[12], [-.46, 1.38, -1.05], [-.42, 1.35, -.98], [.01, .9, .0], [.01, .9, .0], 19, .003);       // the new page
  add(c[12], c[13], [.5, 1.5, -1.4], [.44, 1.5, -1.3], [-.38, 1.45, .86], [-.38, 1.47, .86], 28, .002);       // over his shoulder, her: she smiles
  add(c[13], c[14], [.24, 1.28, .64], [.22, 1.22, .58], [.16, DESK_Y, .21], [.16, DESK_Y, .21], 36, .003);       // the stamp
  add(c[14], T.end + 1, [.2, 1.45, 2.4], [.15, 1.5, 2.85], [.15, 1.45, -1.2], [.15, 1.5, -1.2], 36, .002);   // case closed, the neon
  return S;
}
function shot(t) {
  let s = SHOTS[0]; for (const x of SHOTS) if (t >= x.a) s = x;
  const k = easeIO(win(t, s.a, s.b));
  return { p: lerpV(s.p0, s.p1, k), q: lerpV(s.q0, s.q1, k), fov: s.fov, ap: s.ap, i: SHOTS.indexOf(s) };
}
const flash = (t) => Math.max(...T.lightning.map(([at, k]) => (pulse(t, at, .02, .12) + pulse(t, at + .16, .02, .3) * .7) * k));
const gust = (t) => .5 + .5 * Math.sin(t * .7) * Math.sin(t * .23 + 1) + .4 * pulse(t, T.enter, .3, 2.2);

// ---------------------------------------------------------------- render
function renderAt(t) {
  const s = shot(t);
  const fl = flash(t), gu = gust(t);
  lamp.visible = ![2, 5, 10, 11].includes(s.i);    // a film cheat: the lamp keeps lighting, its shade leaves the over-the-shoulder frames
  const hand = .004;
  camera.position.set(s.p[0] + Math.sin(t * .9) * hand, s.p[1] + Math.cos(t * .7) * hand, s.p[2]);
  camera.lookAt(s.q[0], s.q[1], s.q[2]);
  camera.fov = s.fov; camera.updateProjectionMatrix(); camera.updateMatrixWorld();
  const focusDist = camera.position.distanceTo(V(...s.q));
  bokeh.uniforms.focus.value = focusDist; bokeh.uniforms.aperture.value = s.ap; bokeh.uniforms.maxblur.value = .009;

  // the room: lightning, the door, the draught
  flashLight.intensity = fl * 5; hemi.intensity = .6 + fl * 1.2;
  scene.background.setRGB(.02 + fl * .25, .024 + fl * .26, .04 + fl * .3);
  const dk = easeOut(win(t, T.enter - .55, T.enter + .2)) * (1 - easeIO(win(t, T.arrive + .3, T.arrive + 1.4)));
  doorPivot.rotation.y = -dk * 1.25;
  doorLight.intensity = dk * 40; hallM.color.setRGB(1, .94, .86).multiplyScalar(2.4 * Math.max(.05, dk));
  SLATS.forEach((sl, i) => { sl.rotation.x = .62 + Math.sin(t * 2.2 + i * .35) * .05 * (.4 + gu) + fl * .02; sl.position.z = BZ + .07 + Math.sin(t * 1.7 + i * .2) * .004 * gu; });
  bottomRail.position.z = BZ + .07 + Math.sin(t * 1.7) * .006 * gu;
  winLight.intensity = 30 + fl * 60;
  PAPERS.forEach(([p, base, ry], i) => {
    const lift = i === 3 ? Math.max(0, Math.sin((t - T.enter) * 7)) * .012 * pulse(t, T.enter, .2, 1.6) : 0;
    p.position.y = base.y + lift; p.rotation.z = lift * 4; p.rotation.y = ry + lift * 3;
  });
  // rain outside, slanting with the wind
  const slant = .18 + gu * .25;
  for (let i = 0; i < RAIN_N; i++) {
    const y = 6 - ((hash(i) * 7 + t * (9 + hash(i + 1) * 3)) % 7);
    const x = -5 + hash(i + 2) * 10 + (6 - y) * slant;
    tPos.set(x, y, -2.25 - hash(i + 3) * 6);
    tQ.setFromAxisAngle(Z1, -slant * .8);
    rain.setMatrixAt(i, tM.compose(tPos, tQ, tS.setScalar(.7 + hash(i + 4) * .6)));
  }
  rain.instanceMatrix.needsUpdate = true;
  for (let i = 0; i < DROP_N; i++) {
    const sp = .05 + hash(i + 5) * .35, ph = (hash(i) + t * sp) % 1;
    const y = WY1 - ph * (WY1 - WY0), x = WX0 + hash(i + 1) * (WX1 - WX0) + Math.sin(t * 2 + i) * .004 + ph * gu * .03;
    tPos.set(x, y, BZ - .006);
    dropM.opacity = .5;
    drops.setMatrixAt(i, tM.compose(tPos, tQ.identity(), tS.set(1, .6 + hash(i + 2) * 1.4 + sp * 2, 1)));
  }
  drops.instanceMatrix.needsUpdate = true;
  if (neonMat) { const fk = (hash(Math.floor(t * 12)) > .93 ? .3 : 1) * (t > T.designed ? 1.25 : 1); neonMat.color.setRGB(.78, .45, 1.0).multiplyScalar(3.4 * fk); }
  for (let i = 0; i < STEAM_N; i++) {
    const ph = (hash(i) + t * .25) % 1;
    tPos.set(-.32 + Math.sin(ph * 6 + i) * .015 + ph * gu * .03, DESK_Y + .1 + ph * .22, .08 + Math.cos(ph * 5 + i) * .01);
    steam.setMatrixAt(i, tM.compose(tPos, camera.quaternion, tS.setScalar((.4 + ph * 1.6) * (1 - ph))));
  }
  steam.instanceMatrix.needsUpdate = true;

  // ---- her
  const c = clientPos(t);
  C.root.visible = t > T.enter - .2;
  const faceDir = c.walking ? Math.atan2(STAND.x - DOOR_IN.x, STAND.z - DOOR_IN.z) : Math.PI - .45;
  C.root.rotation.y = c.k < 1 ? lerp(Math.atan2(STAND.x - DOOR_IN.x, STAND.z - DOOR_IN.z), Math.PI - .45, easeIO(win(t, T.arrive - .45, T.arrive + .1))) : faceDir;
  const ph = (t - T.enter) * 7.2;
  const wk = c.walking ? Math.min(1, Math.min(c.k, 1 - c.k) * 6) : 0;
  C.root.position.copy(c.p); C.root.position.y = Math.abs(Math.sin(ph)) * .025 * wk;
  for (const [k, sgn] of [["L", 1], ["R", -1]]) {
    C["thigh" + k].rotation.x = Math.sin(ph + (sgn > 0 ? 0 : Math.PI)) * .42 * wk;
    C["knee" + k].rotation.x = Math.max(0, Math.sin(ph + (sgn > 0 ? 0 : Math.PI) - 1.2)) * .7 * wk;
  }
  C.skirt.rotation.x = Math.sin(ph * 2) * .04 * wk + Math.sin(t * 1.3) * .015 * gu;
  C.hips.rotation.z = Math.sin(ph) * .05 * wk;
  C.spine.rotation.x = .03; C.hat.rotation.z = -.2 + Math.sin(t * 1.1) * .01;
  // a soft top light keeps her readable as she crosses the dark room
  herLight.position.copy(c.p).add(V(.6, 2.7, .9)); herLight.target.position.copy(c.p).add(V(0, 1.1, 0));
  herLight.intensity = t < T.arrive + 1.5 ? 14 : 6;
  // her hands: on the laptop while she carries it, then at her sides, then one on her hip
  const L = laptopAt(t);
  laptop.position.copy(L.p); laptop.rotation.set(0, 0, 0); laptop.rotateY(L.ry); laptop.rotateX(L.rx);
  lid.rotation.x = lerp(-1.6, .3, L.open);
  if (t < T.place + .55) {
    laptop.updateMatrixWorld(true);
    const a = laptop.localToWorld(V(.17, .01, 0)), b = laptop.localToWorld(V(-.17, .01, 0));
    const fwd = V(Math.sin(C.root.rotation.y), 0, Math.cos(C.root.rotation.y));
    reach(C, "L", a, a.clone().add(V(0, -.4, 0)).sub(fwd.clone().multiplyScalar(.2)), null);
    reach(C, "R", b, b.clone().add(V(0, -.4, 0)).sub(fwd.clone().multiplyScalar(.2)), null);
    setHand(C.handL, .55); setHand(C.handR, .55);
  } else {
    const k = easeIO(win(t, T.place + .55, T.place + 1.3));
    C.root.updateMatrixWorld(true);
    const side = (sx) => C.root.localToWorld(V(sx * .23, .82, .04));
    const hip = C.root.localToWorld(V(-.2, 1.0, .02));
    const lt = side(1), rt = side(-1).lerp(hip, easeIO(win(t, T.designed, T.designed + .6)));
    reach(C, "L", lt, C.root.localToWorld(V(.5, 1.1, -.35)), null);
    reach(C, "R", rt, C.root.localToWorld(V(-.55, 1.1, -.35)), null);
    setHand(C.handL, .42 + k * .08, { spread: .015, thumb: .45 }); setHand(C.handR, .5, { spread: .015, thumb: .5 });
  }
  look(C, t < T.arrive - .3 ? V(-.2, 1.25, -.4) : V(0, 1.2, -.7), 1);
  express(C, { blink: (t % 3.7 < .12) ? 1 : 0, smile: easeOut(win(t, T.designed, T.designed + .5)) * .8, brow: t > T.designed ? .3 : -.1 });

  // ---- him
  const breathe = Math.sin(t * 1.6) * .012;
  D.spine.rotation.x = .1 + breathe;
  const lean = easeIO(win(t, T.culprit - .9, T.culprit - .2)) * (1 - easeIO(win(t, T.called - .6, T.called)));
  D.spine.rotation.x -= lean * .22;
  D.chest.rotation.x = breathe * .5;
  const restR = V(-.24, DESK_Y + .03, -.36), restL = V(.24, DESK_Y + .03, -.36);
  const palmDown = (f) => handQ(f, V(0, -1, 0));
  let rT = restR.clone(), lT = restL.clone(), rQ = palmDown(V(.25, 0, 1)), lQ = palmDown(V(-.25, 0, 1)), rCurl = .2, lCurl = .25, rOpt = {}, lOpt = {};
  let lookAt = V(-.4, 1.25, .8);
  if (t < T.arrive) lookAt = between(t, T.enter - .4, T.arrive) ? C.head.getWorldPosition(V()) : V(0, 1.0, .5);
  else if (t < T.place + 1.2) lookAt = C.head.getWorldPosition(V());
  else lookAt = screenPoint(640, 400);
  // the screen: grey site, the evidence, the prompt, then the new page in colour
  let reveal = 0;
  if (t < T.same - .3) {
    let y = 0;
    if (t < T.two - .3) y = win(t, T.place + 1.2, T.two - .3) * 260;
    else { const k = [T.two, T.reviews, T.labels]; const Y = [640, 2690, 1080]; let i = 0; for (let j = 0; j < 3; j++) if (t > k[j] - .35) i = j; const prevY = i === 0 ? 260 : Y[i - 1]; y = lerp(prevY, Y[i], easeIO(win(t, k[i] - .35, k[i] + .15))); }
    drawPage(IMG.before, y, 1);
  } else if (t < T.no - .1) drawTerminal(t);
  else {
    reveal = easeOut(win(t, T.no - .1, T.no + .6));
    const sy = easeIO(win(t, T.no + .3, T.comment - .2)) * 2400;
    drawPage(IMG.after, sy, reveal);
  }
  screenTex.needsUpdate = true;
  // the evidence: the loupe over the three giveaways
  const ev = [T.two, T.reviews, T.labels];
  const EVPX = [[214, 330], [270, 400], [640, 82]];
  loupe.visible = between(t, T.two - .7, T.labels + 1.6);
  if (loupe.visible) {
    let i = 0; for (let k = 0; k < 3; k++) if (t > ev[k] - .25) i = k;
    const prev = EVPX[Math.max(0, i - 1)], cur = EVPX[i];
    const mk = easeIO(win(t, ev[i] - .25, ev[i] + .3));
    const px = i === 0 ? cur : lerpV(prev, cur, mk);
    const hover = .055 + Math.sin(t * 2.3) * .004;
    const lp = screenPoint(px[0], px[1], hover);
    const rise = easeOut(win(t, T.two - .7, T.two - .2));
    loupe.position.copy(lp.clone().lerp(V(-.2, DESK_Y + .02, -.04), 1 - rise));
    loupe.lookAt(camera.position);
    loupe.rotation.z += -.6;
    drawLens(px[0], px[1]);
    loupe.updateMatrixWorld(true);
    rT = loupe.localToWorld(V(0, -.14, -.01)); rQ = handQ(V(1, .3, .2), V(0, 0, 1));
    rCurl = .78; rOpt = { thumb: .9 };
  }
  // evidence markers drop onto the desk
  MARKERS.forEach((m, i) => {
    const at = ev[i] + .5, k = easeOut(win(t, at, at + .3));
    m.visible = t > at && t < T.cut[9];
    m.position.set(.27 + i * .085, DESK_Y + (1 - k) * .18, .1 - i * .02); m.rotation.y = -.3 + i * .1;
  });
  // the culprit: a finger tips the hat brim up
  const tip = pulse(t, T.culprit - .15, .35, .8);
  if (between(t, T.culprit - .6, T.defaults + .6)) {
    D.head.updateMatrixWorld(true);
    const brimFront = D.head.localToWorld(V(.02, .2, .2));
    const k = easeIO(win(t, T.culprit - .6, T.culprit - .15)) * (1 - easeIO(win(t, T.defaults, T.defaults + .6)));
    rT = restR.clone().lerp(brimFront.add(V(0, -.07, 0)), k); rQ = rQ.clone().slerp(handQ(V(-.2, 1, .2), V(-.3, 0, -1)), k); rCurl = lerp(.25, .85, k); rOpt = { point: true, thumb: .8 };
    lookAt = V(.5, 1.25, .7);
  }
  D.hat.rotation.x = .12 - tip * .22;
  // the call: left hand takes the handset to his ear, right index dials
  phone.updateMatrixWorld(true);
  const onCradle = phone.localToWorld(cradle.clone());
  const callK = easeIO(win(t, T.called - .5, T.called + .1)) * (1 - easeIO(win(t, T.cut[9] - .3, T.cut[9] + .2)));
  D.head.updateMatrixWorld(true);
  const ear = D.head.localToWorld(V(.13, .07, .02));
  handset.position.copy(onCradle.clone().lerp(ear.clone().add(V(.02, -.02, .04)), callK));
  handset.quaternion.copy(phone.quaternion).slerp(new THREE.Quaternion().setFromEuler(new THREE.Euler(.2, -1.2, 1.35)), callK);
  if (callK > 0) {
    lT = onCradle.clone().lerp(ear.clone().add(V(.05, -.07, .05)), callK); lQ = lQ.clone().slerp(handQ(V(-.2, 1, .4), V(-1, 0, .1)), callK); lCurl = lerp(.3, .8, callK); lOpt = { thumb: .9 };
    lookAt = V(.6, 1.0, .3);
  }
  const dialK = between(t, T.called + .05, T.hallmark - .1) ? 1 : 0;
  dial.rotation.y = dialK ? -Math.sin(win(t, T.called + .1, T.hallmark - .2) * Math.PI * 3) * .9 : 0;
  if (dialK) { const dp = phone.localToWorld(V(.05, .12, .07)); rT = dp.add(V(0, .025, 0)); rQ = handQ(V(0, -1, .3), V(0, 0, -1)); rCurl = .85; rOpt = { point: true, thumb: .8 }; }
  // the card slides out under the lamp
  const ck = easeOut(win(t, T.hallmark - .25, T.hallmark + .35));
  card.visible = t > T.hallmark - .3;
  card.position.set(lerp(.62, .3, ck), DESK_Y + .002, lerp(-.1, -.38, ck)); card.rotation.set(0, Math.PI + lerp(.8, .1, ck), 0);
  // the deal: five themes flicked out of a deck in a fan
  DEAL.forEach((cd, i) => {
    const at = T.deals - .1 + i * .2, k = easeOut(win(t, at, at + .35));
    cd.visible = t > at && t < T.cut[10];
    const fx = (i - 2) * .095, fz = .16 + Math.abs(i - 2) * .012;
    cd.position.set(lerp(.0, fx, k), DESK_Y + .004 + i * .0015 + Math.sin(k * Math.PI) * .05, lerp(-.02, fz, k));
    cd.rotation.set(0, (i - 2) * -.12 * k, (1 - k) * Math.PI);
  });
  // the book slams down, falls open, and the rules get ticked
  const bk = easeIn(win(t, T.checks - .35, T.checks));
  book.visible = between(t, T.checks - .35, T.cut[10]);
  book.position.set(-.02, DESK_Y + (1 - bk) * .25, -.0); book.rotation.set(0, .05, 0);
  const op = easeOut(win(t, T.checks + .05, T.checks + .45));
  bookCover.rotation.z = op * Math.PI;
  if (book.visible) drawRules(t);
  // same prompt: both hands on the keys, fingers tapping
  const typing = between(t, T.same - .25, T.no);
  if (typing) {
    laptop.updateMatrixWorld(true);
    const kl = laptop.localToWorld(V(.07, .045, -.05)), kr = laptop.localToWorld(V(-.07, .045, -.05));
    rT = kr; lT = kl;
    rQ = handQ(V(.15, -.35, 1), V(0, -1, -.3)); lQ = handQ(V(-.15, -.35, 1), V(0, -1, -.3));
    rCurl = .45; lCurl = .45; lookAt = screenPoint(640, 300);
  }
  // the stamp: lifted, then brought down hard on "closed"
  folder.position.set(.08, DESK_Y + .001, .17); folder.rotation.y = -.08;
  folder.visible = t > T.cut[13] - .2;
  const sUp = easeIO(win(t, T.comment - .2, T.comment + .5)), sDown = easeIn(win(t, T.closed - .25, T.closed));
  const sH = .22 * sUp * (1 - sDown) + easeOut(win(t, T.closed + .35, T.closed + .8)) * .2;
  const stampHome = V(-.36, DESK_Y, .02), stampHit = V(.1, DESK_Y + .008, .2);
  stamp.visible = t > T.cut[13] - .2;
  stamp.position.copy(stampHome.clone().lerp(stampHit, sUp).lerp(V(.3, DESK_Y, .02), easeIO(win(t, T.closed + .35, T.closed + .9)))); stamp.position.y += sH;
  stamp.rotation.set(0, -.1, 0);
  drawFolder(t);
  if (between(t, T.comment - .3, T.end + 1)) {
    stamp.updateMatrixWorld(true);
    rT = stamp.localToWorld(V(0, .12, -.03)); rQ = handQ(V(0, -1, .25), V(0, 0, -1)); rCurl = .9; rOpt = { thumb: .9 };
    lookAt = V(.1, DESK_Y, .2);
    if (t > T.closed + .6) { lookAt = camera.position.clone(); }
  }
  // the reveal: he sits back, nods
  if (between(t, T.designed - .2, T.comment - .3)) lookAt = C.head.getWorldPosition(V());
  const poleR = V(.75, .6, -.95), poleL = V(-.75, .6, -.95);
  reach(D, "R", rT, poleR, rQ); reach(D, "L", lT, poleL, lQ);
  setHand(D.handR, rCurl + (typing ? Math.max(0, Math.sin(t * 22)) * .2 : 0), rOpt); setHand(D.handL, lCurl + (typing ? Math.max(0, Math.sin(t * 19 + 1)) * .2 : 0), lOpt);
  look(D, lookAt, .9);
  express(D, { blink: (t % 4.3 < .12) ? 1 : 0, brow: t > T.designed ? .2 : between(t, T.two, T.cut[6]) ? -.8 : -.35, smile: easeOut(win(t, T.designed + .3, T.designed + .9)) * .45 });
  D.hat.position.y = .205 + pulse(t, T.closed + .6, .3, .8) * .03;

  screenM.color.setScalar(.55 + L.open * .2);
  screenLight.intensity = L.open * 1.2; laptop.updateMatrixWorld(true); screenLight.position.copy(screen.getWorldPosition(V())).add(V(0, .02, -.25));
  colourScreen = reveal;
  lampLight.intensity = 4.5 + (t > T.designed ? easeOut(win(t, T.designed, T.designed + .8)) * 1.5 : 0);

  // ---- render: the mask (what keeps its colour), then the frame
  grade.uniforms.uTime.value = Math.round(t * 30) / 30;
  grade.uniforms.uFlash.value = fl;
  grade.uniforms.uFade.value = 0;
  renderMask();
  if (DEBUG_RAW) renderer.render(scene, camera); else composer.render();
  out2d.drawImage(canvas, 0, 0);
}
let colourScreen = 0;
function renderMask() {
  const bg = scene.background, fog = scene.fog;
  scene.background = new THREE.Color(0); scene.fog = null; scene.overrideMaterial = maskBlack;
  renderer.setRenderTarget(maskRT); renderer.setClearColor(0x000000, 1); renderer.clear();
  const hideRain = [rain.visible, drops.visible, steam.visible, glass.visible]; rain.visible = drops.visible = steam.visible = glass.visible = false;
  renderer.render(scene, camera);
  scene.overrideMaterial = null;
  renderer.autoClear = false;
  const keep = [];
  for (const [m, k] of [[screen, () => colourScreen], ...NEON_PARTS.map((n) => [n, () => 1])]) {
    if (!m.visible) continue;
    keep.push([m, m.material]);
    const w = maskWhite.clone(); w.color.setScalar(k()); w.depthFunc = THREE.LessEqualDepth; m.material = w;
    renderer.render(m, camera);
  }
  for (const [m, mt] of keep) { m.material.dispose(); m.material = mt; }
  renderer.autoClear = true; renderer.setRenderTarget(null);
  rain.visible = hideRain[0]; drops.visible = hideRain[1]; steam.visible = hideRain[2]; glass.visible = hideRain[3];
  scene.background = bg; scene.fog = fog;
}
function drawRules(t) {
  const g = pageCanvas.getContext("2d"), w = 1024, h = 700;
  g.fillStyle = "#ebe5d6"; g.fillRect(0, 0, w, h);
  g.fillStyle = "rgba(0,0,0,.06)"; g.fillRect(w / 2 - 6, 0, 12, h);
  txt(g, "The Floor", 70, 70, 46, { a: "left", w: 800, c: "#1a1a1a" });
  RULES.forEach((r, i) => {
    const y = 160 + i * 88, at = T.every - .35 + i * .26;
    txt(g, r, 120, y, 38, { a: "left", f: "ISerif", i: true, w: 400, c: "#1e1e1e" });
    g.strokeStyle = "#999"; g.lineWidth = 3; g.strokeRect(62, y - 20, 40, 40);
    const k = clamp((t - at) / .15);
    if (k > 0) { g.strokeStyle = "#a01818"; g.lineWidth = 9; g.lineCap = "round"; g.beginPath(); g.moveTo(66, y); g.lineTo(66 + 14 * Math.min(1, k * 2), y + 14 * Math.min(1, k * 2)); if (k > .5) g.lineTo(80 + 30 * (k - .5) * 2, y + 14 - 34 * (k - .5) * 2); g.stroke(); }
  });
  pageTex.needsUpdate = true;
}
let folderBase = null;
function drawFolder(t) {
  if (!folderBase) return;
  folderC.drawImage(folderBase, 0, 0);
  const k = clamp((t - T.closed) / .05);
  if (k > 0) {
    folderC.save(); folderC.translate(560, 470); folderC.rotate(-.12); folderC.globalAlpha = .88;
    folderC.strokeStyle = "#8a1414"; folderC.lineWidth = 14; folderC.strokeRect(-330, -95, 660, 190);
    txt(folderC, "CASE CLOSED", 0, 6, 118, { w: 800, c: "#8a1414", ls: 6 }); folderC.restore();
  }
  folderLive.needsUpdate = true;
}
const tPos = new THREE.Vector3(), tQ = new THREE.Quaternion(), tS = new THREE.Vector3(), tM = new THREE.Matrix4(), Z1 = V(0, 0, 1), Y1 = V(0, 1, 0);

// ---------------------------------------------------------------- the neon and the prints, once the images load
const NEON_PARTS = [];
async function loadAll() {
  await Promise.all(["800 90px Montserrat", "700 34px JBMono", "400 34px ISerif", "italic 400 34px ISerif"].map((f) => document.fonts.load(f)));
  const [before, after, fold, mark] = await Promise.all(["assets/tex/before_page.jpg", "assets/tex/after_page.jpg", "assets/tex/before_fold.jpg", "assets/img/logo-mark.svg"].map(loadImg));
  IMG = { before, after, fold };
  // the neon: the comet-star mark and the name, in tubes
  const neonTex = canvasTex(1024, 1024, (g, w, h) => {
    g.clearRect(0, 0, w, h);
    g.filter = "blur(10px)"; g.drawImage(mark, 262, 40, 500, 500); g.filter = "none"; g.drawImage(mark, 262, 40, 500, 500);
    g.shadowColor = "#fff"; g.shadowBlur = 24;
    txt(g, "NXTLVLSOCIAL.AI", w / 2, 700, 108, { w: 800, c: "#fff", ls: 4 });
  });
  neonMat = new THREE.MeshBasicMaterial({ map: neonTex, transparent: true, depthWrite: false, toneMapped: false, fog: false, color: new THREE.Color(.78, .45, 1).multiplyScalar(2.2) });
  const np = mesh(new THREE.PlaneGeometry(1.45, 1.45), neonMat, 0, 0, 0, neon); np.castShadow = false;
  NEON_PARTS.push(np);
  const nlight = new THREE.PointLight(0xa070ff, 6, 9, 1.4); nlight.position.set(0, 0, 1.5); neon.add(nlight);
  // prints on the corkboard
  const pt = new THREE.CanvasTexture((() => { const c = document.createElement("canvas"); c.width = 640; c.height = 400; c.getContext("2d").drawImage(fold, 0, 0, 640, 400); return c; })());
  pt.colorSpace = THREE.SRGBColorSpace;
  const pm = new THREE.MeshStandardMaterial({ map: pt, roughness: .8 });
  for (let r = 0; r < 4; r++) for (let k = 0; k < 6; k++) {
    const p = mesh(new THREE.PlaneGeometry(.26, .162), pm, -CORK.w / 2 + .17 + k * .312 + (hash(r * 6 + k) - .5) * .04, CORK.h / 2 - .16 - r * .27 + (hash(r * 6 + k + 9) - .5) * .03, .02 + (r * 6 + k) * .0004, cork);
    p.rotation.z = (hash(r * 6 + k + 3) - .5) * .12; PRINTS.push(p);
    mesh(new THREE.SphereGeometry(.009, 6, 5), pinM, p.position.x, p.position.y + .07, .035, cork);
  }
  // red string between some of them
  const strM = new THREE.MeshStandardMaterial({ color: 0xa01818, roughness: .6 });
  for (let i = 0; i < 9; i++) {
    const a = PRINTS[Math.floor(hash(i + 40) * PRINTS.length)].position, b = PRINTS[Math.floor(hash(i + 70) * PRINTS.length)].position;
    const A = V(a.x, a.y + .07, .036), B = V(b.x, b.y + .07, .036), mid = A.clone().add(B).multiplyScalar(.5), len = A.distanceTo(B);
    if (len < .2) continue;
    const s = mesh(new THREE.CylinderGeometry(.0018, .0018, len, 4), strM, mid.x, mid.y, mid.z, cork);
    s.quaternion.setFromUnitVectors(V(0, 1, 0), B.clone().sub(A).normalize());
  }
  const fb = document.createElement("canvas"); fb.width = 1024; fb.height = 720; fb.getContext("2d").drawImage(folderTex.userData.canvas, 0, 0);
  folderBase = fb;
  SHOTS = buildShots();
  renderer.compile(scene, camera);
}

const ready = (async () => {
  await loadAll();
  const qt = new URLSearchParams(location.search).get("t");
  renderAt(qt !== null ? +qt : (window.__hfThreeTime || 0));
  if (qt !== null) window.__done = true;
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["noirworld"] = ready;
window.addEventListener("hf-seek", (e) => { if (SHOTS) renderAt(e.detail.time); });
