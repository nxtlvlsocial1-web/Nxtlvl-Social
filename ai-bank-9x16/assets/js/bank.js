// AI Bank reel: the 3D world. A cream diorama on a floating tile: a cutaway two-storey home (living room, kitchen,
// bedroom) with a vault dug out underneath, a glass money pipe up the side of the house, a money tree in the garden, the
// phone company's tower with its own AI on the balcony, and far away a night street in another country. The bank's AI
// is the coral orb with an eye. Everything is a pure function of time t (seconds), drawn on HyperFrames' hf-seek; cue
// times come from the voice (window.CT, written by build/generate.py). The month, beat by beat:
//   day 1     four forgotten subscriptions float over the coffee table; each is stamped and bursts into coins in a jar
//   day 3     the orb flies to the tower and argues with the phone company's robot; the bill shrinks 40%
//   day 9     2 AM in bed, a sneaker hologram over the phone; the card freezes over in ice
//   week 2    every sip of coffee sends coins arcing out to the money tree, which grows coin leaves
//   day 21    3 AM, another country: a hooded figure at an ATM; the card was blocked before they tried
//   day 30    the vault door swings open by itself, every gold bar rises into the pipe and vanishes through a portal
//   real      the house shrinks into a world of homes whose payments all flow through the AI; red ones are stopped
//   close     the whole diorama under the orb
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
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
const col = (h) => new THREE.Color(h);
const tmpC = new THREE.Color(), tmpC2 = new THREE.Color();
const M4 = new THREE.Matrix4(), Q = new THREE.Quaternion(), V = new THREE.Vector3(), V2 = new THREE.Vector3(), V3 = new THREE.Vector3(), S = new THREE.Vector3();
const UP = new THREE.Vector3(0, 1, 0);
const pulse = (t, a, w = .35) => Math.exp(-(((t - a) / w) ** 2));
const bump = (t, a, b, e = .35) => ss(t, a, a + e) * (1 - ss(t, b - e, b));
const v3 = (a) => new THREE.Vector3(...a);
const INK = 0x1E1B18, CORAL = 0xE8735A, NAVY = 0x34508F, CREAM = 0xFFFDF8, GOLD = 0xF2B33D, RED = 0xD9483B, BLUE = 0x3A7BD5, GREEN = 0x3FA372;
const sceneOf = (t) => { let s = 0; while (s < CU.length && t >= CU[s]) s++; return s; };

// ---------------------------------------------------------------- renderer, scene, post
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
scene.background = col(0xF1E9DC);
scene.fog = new THREE.Fog(0xF1E9DC, 60, 200);
const camera = new THREE.PerspectiveCamera(40, W / H, .03, 800);
const rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });
const composer = new EffectComposer(renderer, rt);
composer.setPixelRatio(1);
composer.setSize(W, H);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), .3, .5, .85);
composer.addPass(bloom);
composer.addPass(new OutputPass());
const grade = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uSat: { value: 1 }, uVig: { value: .28 }, uFlash: { value: 0 }, uCool: { value: 0 }, uRed: { value: 0 },
    uBlur: { value: 0 }, uCA: { value: 0 }, uBars: { value: 0 }, uScan: { value: 0 }, uCon: { value: 0 } },
  vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }",
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime, uSat, uVig, uFlash, uCool, uRed, uBlur, uCA, uBars, uScan, uCon; varying vec2 vUv;
    float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
    void main(){
      vec2 uv = vUv, d = vec2(.5, .5) - uv;
      vec3 c = vec3(0.);
      for (int i = 0; i < 8; i++) {
        vec2 o = d * uBlur * float(i) / 7.;
        c.r += texture2D(tDiffuse, uv + o + d * uCA).r;
        c.g += texture2D(tDiffuse, uv + o).g;
        c.b += texture2D(tDiffuse, uv + o - d * uCA).b;
      }
      c /= 8.;
      float g = dot(c, vec3(.299, .587, .114));
      c = mix(vec3(g), c, uSat);
      c = mix(c, c * vec3(.9, .98, 1.1), uCool);
      c = (c - .5) * (1. + uCon) + .5;
      vec2 q = vUv - .5; float r = dot(q, q);
      c *= 1. - r * uVig * 2.2;
      c = mix(c, c * vec3(1.3, .5, .45), uRed * smoothstep(.04, .3, r));
      vec2 px = vUv * vec2(1080., 1920.);
      float grid = max(step(.96, fract(px.x / 54.)), step(.96, fract(px.y / 54.)));
      float sweep = 1. - smoothstep(0., .012, abs(fract(-vUv.y - uTime * .45) - .5));
      c = mix(c, vec3(.91, .45, .35), uScan * (.22 * grid + .5 * sweep));
      c += (h(floor(px) + fract(uTime * 7.13) * 97.) - .5) * .026;
      c = mix(c, vec3(1., .99, .96), uFlash);
      float bh = uBars * 150. / 1920.;
      if (vUv.y < bh || vUv.y > 1. - bh) c = vec3(.075, .065, .06);
      gl_FragColor = vec4(c, 1.);
    }`,
});
composer.addPass(grade);

// ---------------------------------------------------------------- lights
const hemi = new THREE.HemisphereLight(0xfff6ea, 0xcdbfa8, .95);
scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff1dc, 2.0);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.bias = -.0005;
sun.shadow.normalBias = .02;
scene.add(sun, sun.target);
const plight = (c, d = 8, decay = 1.6) => { const l = new THREE.PointLight(c, 0, d, decay); scene.add(l); return l; };
const lampL = plight(0xffc98a, 7), tvL = plight(0x9fc4ff, 5), phoneL = plight(0xcfe3ff, 3.2, 1.4), bedL = plight(0xffc98a, 5);
const vaultL = plight(0xffd9a0, 9), alarmL = plight(0xff3a28, 9), neonA = plight(0xff4fa3, 9), neonB = plight(0x4fe0ff, 9), atmL = plight(0x7fffb0, 3), faceKey = plight(0xfff0e0, 5, 1.2);
const kitchenL = plight(0xffe2b8, 7);
lampL.position.set(-5.9, 2.0, -2.8); tvL.position.set(-5.8, 1.6, -1.2); bedL.position.set(-3.85, 4.4, -2.7);
vaultL.position.set(-2.5, -.7, -1.0); alarmL.position.set(.6, -.8, -3.2); kitchenL.position.set(-.4, 2.6, -1.6);
neonA.position.set(13.4, 4.6, -16.4); neonB.position.set(16.4, 4.2, -15.6); atmL.position.set(14.2, 3.6, -15.5);

// ---------------------------------------------------------------- materials, text textures
const mat = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: .85, metalness: 0, ...o });
const gloss = (c, o = {}) => new THREE.MeshPhysicalMaterial({ color: c, roughness: .35, clearcoat: .7, clearcoatRoughness: .15, envMap: ENV, envMapIntensity: .35, ...o });
const metal = (c, r = .3) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: .85, envMap: ENV, envMapIntensity: 1 });
const goldM = new THREE.MeshStandardMaterial({ color: 0xF2B33D, roughness: .25, metalness: .9, envMap: ENV, envMapIntensity: 1.3, emissive: 0x4a2a00, emissiveIntensity: .25 });
const glow = (c) => new THREE.MeshBasicMaterial({ color: c, toneMapped: false });
const ROOT3 = new THREE.Group(); scene.add(ROOT3);
const add = (m, cast = true, recv = true, parent = ROOT3) => { m.castShadow = cast; m.receiveShadow = recv; parent.add(m); return m; };
const box = (w, h, d, c, x, y, z, o = {}) => { const m = add(new THREE.Mesh(o.round ? new RoundedBoxGeometry(w, h, d, 2, Math.min(o.round, w / 2, h / 2, d / 2)) : new THREE.BoxGeometry(w, h, d), c.isMaterial ? c : mat(c)), o.cast ?? true, true, o.parent); m.position.set(x, y, z); return m; };
const cyl = (r1, r2, h, c, x, y, z, seg = 20) => { const m = add(new THREE.Mesh(new THREE.CylinderGeometry(r1, r2, h, seg), c.isMaterial ? c : mat(c))); m.position.set(x, y, z); return m; };
const sph = (r, c, x, y, z) => { const m = add(new THREE.Mesh(new THREE.SphereGeometry(r, 20, 14), c.isMaterial ? c : mat(c))); m.position.set(x, y, z); return m; };
// textures drawn on canvases once the fonts are ready (init); the meshes get them then
const TEX = {};
function canvasTex(w, h, draw) {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  const g = c.getContext("2d"); draw(g, w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
}
const rr = (g, x, y, w, h, r) => { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); };
const LATE = [];
const setMap = (m, tx) => { if (m.map !== tx) { m.map = tx || null; m.needsUpdate = true; } };                                  // [material, textureKey] assigned in init
const texMat = (key, o = {}) => { const m = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, ...o }); LATE.push([m, key]); return m; };

// ---------------------------------------------------------------- the tile, with the vault dug out under the house
const tileM = mat(0xEADFCB), wallStone = mat(0xD9CCB4), ink = mat(INK, { roughness: .6 });
box(2.5, 4, 8.2, tileM, -7.75, -2, -1.9);                  // left
box(8, 4, 2.4, wallStone, -2.5, -2, -4.8);                 // behind the vault
box(8, .6, 5.8, wallStone, -2.5, -3.7, -.7);               // vault floor slab
box(8, .3, 5.8, tileM, -2.5, -.15, -.7);                   // vault ceiling / ground floor
box(7.5, 4, 12, tileM, 5.25, -2, 0);                        // right (garden)
for (const [w, d, x, z] of [[2.5, 8.2, -7.75, -1.9], [8, .01, -2.5, 2.2], [7.5, 12, 5.25, 0]]) { const e = box(w + .3, .35, d + .3, ink, x, -4.15, z); e.castShadow = false; }
// garden lawn, path stones, hedges, bench, lamp post, mailbox
box(7.2, .06, 11.6, mat(0xB4C99B), 5.25, .03, 0, { cast: false });
for (let k = 0; k < 6; k++) cyl(.32, .32, .05, mat(0xE6DCC8), 2.4 + k * .55, .07, 2.6 + Math.sin(k) * .3, 16);
for (const [x, z, w] of [[8.5, 0, 11], [5.2, 5.6, 6.4]]) box(x > 8 ? .5 : w, .7, x > 8 ? w : .5, mat(0x7FA36B), x, .38, z, { round: .15 });
box(1.3, .08, .4, mat(0xC9A27A), 6.6, .5, 3.6); box(1.3, .4, .06, mat(0xC9A27A), 6.6, .75, 3.8);
for (const sx of [-.55, .55]) box(.06, .5, .4, ink, 6.6 + sx, .25, 3.6);
cyl(.05, .07, 2.8, ink, 7.6, 1.4, 1.2, 8); sph(.18, glow(0xFFE7B0), 7.6, 2.9, 1.2);
box(.25, .3, .4, mat(CORAL), 2.6, 1.0, 4.6, { round: .05 }); cyl(.03, .03, .85, ink, 2.6, .42, 4.6, 6);

// ---------------------------------------------------------------- the house (open at the front, z = 1.5)
const HX0 = -6.5, HX1 = 1.5, HZ0 = -3.6, HZ1 = 1.5;
const wood = (c) => canvasTex(512, 512, (g, w, h) => { g.fillStyle = c; g.fillRect(0, 0, w, h); for (let k = 0; k < 8; k++) { g.fillStyle = k % 2 ? "rgba(0,0,0,.05)" : "rgba(255,255,255,.04)"; g.fillRect(0, k * 64, w, 64); g.fillStyle = "rgba(60,40,20,.18)"; g.fillRect(0, k * 64, w, 2); } });
const floorWood = new THREE.MeshStandardMaterial({ map: wood("#C9A27A"), roughness: .7 });
box(HX1 - HX0 - .2, .02, HZ1 - HZ0 - .1, floorWood, (HX0 + HX1) / 2, .01, (HZ0 + HZ1) / 2 + .05, { cast: false });
box(HX1 - HX0, 6.2, .2, mat(0xF2E4D4), (HX0 + HX1) / 2, 3.1, HZ0 + .1);           // back wall
box(.2, 6.2, HZ1 - HZ0, mat(0xF2E4D4), HX0 - .1, 3.1, (HZ0 + HZ1) / 2);           // left wall
box(.2, 6.2, HZ1 - HZ0, mat(0xF2E4D4), HX1 + .1, 3.1, (HZ0 + HZ1) / 2);           // right wall
box(HX1 - HX0 + .4, .22, HZ1 - HZ0, mat(0xEADFCB), (HX0 + HX1) / 2, 3.11, (HZ0 + HZ1) / 2);   // first floor
box(HX1 - HX0 - .2, .02, HZ1 - HZ0 - .1, new THREE.MeshStandardMaterial({ map: wood("#D8B48C"), roughness: .7 }), (HX0 + HX1) / 2, 3.23, (HZ0 + HZ1) / 2 + .05, { cast: false });
for (const y of [0, 3.0, 6.1]) box(HX1 - HX0 + .45, .14, .14, mat(CORAL), (HX0 + HX1) / 2, y + .07, HZ1 + .02);   // coral trims on the cut edges
for (const x of [HX0 - .1, HX1 + .1]) box(.24, 6.2, .14, mat(CORAL), x, 3.1, HZ1 + .02);
// wallpaper per room
box(4.4, 2.95, .02, mat(0xF4DCCB), -4.3, 1.5, HZ0 + .21, { cast: false });         // living
box(3.4, 2.95, .02, mat(0xE9EFE2), -.25, 1.5, HZ0 + .21, { cast: false });         // kitchen
box(7.8, 2.85, .02, mat(0xDDE6EE), -2.5, 4.68, HZ0 + .21, { cast: false });        // bedroom
// roof: two slopes, a ridge and a chimney
const ROOF = mat(0xC9644E);
for (const s of [-1, 1]) { const r = box(HX1 - HX0 + .9, .22, 3.25, ROOF, (HX0 + HX1) / 2, 7.05, (HZ0 + HZ1) / 2 + s * 1.27); r.rotation.x = s * .62; }
box(HX1 - HX0 + .95, .2, .3, mat(0xA9503D), (HX0 + HX1) / 2, 7.95, (HZ0 + HZ1) / 2);
box(.6, 1.2, .6, mat(0xD9CCB4), -.6, 7.9, -2.6);
// living room: sofa, cushions, coffee table, rug, lamp, plant, TV, frames, shelf
const rugTex = canvasTex(512, 384, (g, w, h) => { g.fillStyle = "#C9785A"; g.fillRect(0, 0, w, h); g.strokeStyle = "#F2D3B8"; g.lineWidth = 14; g.strokeRect(24, 24, w - 48, h - 48); for (let k = 0; k < 6; k++) { g.fillStyle = k % 2 ? "#B0614A" : "#E39A7A"; g.fillRect(70 + k * 62, 90, 30, h - 180); } });
box(3.3, .02, 2.3, new THREE.MeshStandardMaterial({ map: rugTex, roughness: .95 }), -4.3, .025, -1.6, { cast: false });
const sofaM = gloss(NAVY, { roughness: .8, clearcoat: 0 });
box(2.5, .42, .95, sofaM, -4.3, .32, -2.85, { round: .1 }); box(2.5, .75, .28, sofaM, -4.3, .78, -3.22, { round: .1 });
for (const s of [-1, 1]) box(.28, .62, .95, sofaM, -4.3 + s * 1.25, .48, -2.85, { round: .1 });
for (const s of [-1, 1]) box(1.08, .14, .78, mat(0x4E6AA8), -4.3 + s * .55, .6, -2.8, { round: .06 });
box(.5, .45, .14, mat(GOLD), -5.25, .95, -3.0, { round: .06 }).rotation.z = .2;
box(1.5, .08, .75, mat(0xB98E62), -4.3, .44, -1.4, { round: .03 });
for (const sx of [-.65, .65]) for (const sz of [-.3, .3]) box(.06, .4, .06, ink, -4.3 + sx, .2, -1.4 + sz);
const jar = add(new THREE.Mesh(new THREE.CylinderGeometry(.16, .16, .36, 24, 1, true), new THREE.MeshPhysicalMaterial({ color: 0xE8F2F6, transparent: true, opacity: .35, roughness: .05, envMap: ENV, side: THREE.DoubleSide })), false, false);
jar.position.set(-3.75, .66, -1.35);
cyl(.165, .165, .04, mat(0xC9A27A), -3.75, .5, -1.35, 24);
const JAR = new THREE.Vector3(-3.75, .62, -1.35);
cyl(.025, .025, 1.6, ink, -6.0, .8, -3.1, 8); const shade = add(new THREE.Mesh(new THREE.ConeGeometry(.32, .36, 20, 1, true), new THREE.MeshStandardMaterial({ color: 0xFFE7C2, emissive: 0xffc98a, emissiveIntensity: .2, side: THREE.DoubleSide }))); shade.position.set(-6.0, 1.75, -3.1);
cyl(.2, .16, .32, mat(0xC9644E), -2.5, .16, -3.1, 16); for (let k = 0; k < 5; k++) { const l = sph(.22, mat(0x6E9A5C), -2.5 + Math.sin(k * 1.3) * .12, .55 + k * .14, -3.1 + Math.cos(k * 1.3) * .1); l.scale.set(.8, 1.3, .8); }
const tvScreenM = new THREE.MeshBasicMaterial({ color: 0x1b2440, toneMapped: false });
box(.08, 1.0, 1.7, ink, -6.35, 1.65, -1.25); const tvScr = box(.01, .88, 1.56, tvScreenM, -6.3, 1.65, -1.25, { cast: false });
box(.5, .5, 1.6, mat(0xB98E62), -6.15, .25, -1.25);
for (const [x, y, w, c] of [[-5.0, 2.0, .8, 0xE8735A], [-3.9, 2.15, .55, 0x3FA372], [-3.0, 1.95, .7, 0xF2B33D]]) { box(w + .08, w * .75 + .08, .04, ink, x, y, HZ0 + .24); box(w, w * .75, .03, mat(c), x, y, HZ0 + .26, { cast: false }); }
// kitchen: counter, upper cabinets, coffee machine, fridge, island, stools, window, pendant
box(3.3, .88, .65, mat(0xF7F1E6), -.25, .44, -3.1); box(3.36, .06, .7, mat(0x8C7B6B), -.25, .91, -3.1);
box(3.3, .7, .4, mat(0xF7F1E6), -.25, 2.25, -3.25);
box(.36, .46, .3, mat(INK, { roughness: .4 }), .35, 1.17, -3.1, { round: .04 }); box(.1, .06, .02, glow(0x7FE0A8), .35, 1.32, -2.94);
cyl(.06, .05, .12, mat(CREAM), .35, 1.0, -2.92, 14);
box(.85, 2.05, .72, gloss(0xDCE4E6, { metalness: .3 }), 1.0, 1.03, -3.0, { round: .05 });
box(1.9, .9, .62, mat(0xE6DCC8), -.4, .45, -1.25); box(1.98, .06, .7, mat(0x8C7B6B), -.4, .92, -1.25);
for (const sx of [-.55, .35]) { cyl(.2, .2, .06, mat(CORAL), -.4 + sx, .7, -.6, 16); cyl(.03, .03, .68, ink, -.4 + sx, .34, -.6, 6); }
const winSkyM = new THREE.MeshBasicMaterial({ color: 0xBFD9EC });
box(.02, 1.0, 1.1, winSkyM, HX1 - .02, 1.75, -1.6, { cast: false }); box(.05, 1.12, .06, mat(CREAM), HX1 - .04, 1.75, -1.6); box(.05, .06, 1.22, mat(CREAM), HX1 - .04, 1.75, -1.6);
cyl(.01, .01, .8, ink, -.4, 2.6, -1.3, 4); const pend = add(new THREE.Mesh(new THREE.SphereGeometry(.16, 16, 10, 0, Math.PI * 2, 0, Math.PI / 2), mat(CORAL, { side: THREE.DoubleSide }))); pend.position.set(-.4, 2.2, -1.3);
// bedroom: bed, pillows, blanket, nightstand, lamp, clock, window (sky changes), wardrobe, rug
box(1.8, .36, 2.4, mat(0xB98E62), -2.6, 3.41, -2.3, { round: .05 }); box(1.8, .9, .12, mat(0xB98E62), -2.6, 3.8, -3.45, { round: .04 });
box(1.68, .26, 2.28, mat(CREAM), -2.6, 3.72, -2.3, { round: .08 });
box(1.0, .18, .45, mat(0xF7F1E6), -2.6, 3.94, -3.05, { round: .08 });
const blanket = box(1.74, .16, 1.55, mat(0x3E8E8A), -2.6, 4.06, -1.62, { round: .07 });
box(.5, .55, .45, mat(0xB98E62), -3.85, 3.5, -2.95, { round: .04 }); cyl(.05, .07, .3, ink, -3.85, 3.93, -3.0, 8);
const bedShade = add(new THREE.Mesh(new THREE.ConeGeometry(.18, .22, 16, 1, true), new THREE.MeshStandardMaterial({ color: 0xFFE7C2, emissive: 0xffc98a, emissiveIntensity: .1, side: THREE.DoubleSide }))); bedShade.position.set(-3.85, 4.17, -3.0);
const clockM = texMat("clock"); const clock = box(.3, .14, .02, clockM, -3.75, 3.86, -2.78, { cast: false });
box(.32, .16, .1, ink, -3.75, 3.86, -2.84);
const nightWinM = new THREE.MeshBasicMaterial({ color: 0xBFD9EC });
box(1.5, 1.1, .02, nightWinM, -.6, 4.75, HZ0 + .23, { cast: false }); box(1.62, .06, .05, mat(CREAM), -.6, 4.75, HZ0 + .26); box(.06, 1.22, .05, mat(CREAM), -.6, 4.75, HZ0 + .26);
const moon = sph(.12, glow(0xF4F0E0), -.25, 5.05, HZ0 + .25); moon.scale.z = .2;
box(1.0, 2.3, .6, mat(0xC9A27A), .85, 4.4, -3.15, { round: .04 });
box(1.6, .02, 1.0, mat(0xC9785A), -2.6, 3.24, -.4, { cast: false });

// ---------------------------------------------------------------- the vault (y -3.4 .. -0.3)
const vtile = canvasTex(512, 512, (g, w, h) => { for (let i = 0; i < 8; i++) for (let j = 0; j < 8; j++) { g.fillStyle = (i + j) % 2 ? "#CFC2AC" : "#BFB09A"; g.fillRect(i * 64, j * 64, 64, 64); } });
vtile.wrapS = vtile.wrapT = THREE.RepeatWrapping; vtile.repeat.set(3, 2);
box(7.9, .02, 5.7, new THREE.MeshStandardMaterial({ map: vtile, roughness: .6, envMap: ENV, envMapIntensity: .3 }), -2.5, -3.39, -.7, { cast: false });
// the door: frame, disc on a hinge, locking wheel
box(3.0, 2.9, .2, mat(0xBDB2A2), -2.5, -1.85, -3.55);
const vframe = add(new THREE.Mesh(new THREE.TorusGeometry(1.08, .14, 14, 48), metal(0x8C8780))); vframe.position.set(-2.5, -1.85, -3.42);
const vdark = add(new THREE.Mesh(new THREE.CircleGeometry(1.0, 40), glow(0x14110f)), false, false); vdark.position.set(-2.5, -1.85, -3.445);
const doorPivot = new THREE.Group(); doorPivot.position.set(-3.55, -1.85, -3.35); ROOT3.add(doorPivot);
const door = add(new THREE.Mesh(new THREE.CylinderGeometry(1.0, 1.0, .3, 48).rotateX(Math.PI / 2), metal(0xA9A39A, .35)), true, true, doorPivot); door.position.set(1.05, 0, 0);
const wheel = add(new THREE.Mesh(new THREE.TorusGeometry(.38, .045, 10, 32), metal(0x5a5650, .3)), true, true, doorPivot); wheel.position.set(1.05, 0, .22);
for (let k = 0; k < 3; k++) { const sp = add(new THREE.Mesh(new THREE.BoxGeometry(.8, .05, .05), metal(0x5a5650, .3)), true, true, wheel); sp.rotation.z = k * Math.PI / 3; }
for (let k = 0; k < 8; k++) { const b = add(new THREE.Mesh(new THREE.CylinderGeometry(.06, .06, .08, 10).rotateX(Math.PI / 2), metal(0x8C8780)), true, true, doorPivot); b.position.set(1.05 + Math.cos(k * Math.PI / 4) * .82, Math.sin(k * Math.PI / 4) * .82, .17); }
// safe deposit boxes on the side walls
const depGeo = new RoundedBoxGeometry(.04, .38, .58, 1, .015);
const depM = new THREE.InstancedMesh(depGeo, metal(0xC2B49A, .4), 2 * 6 * 4); let di = 0;
for (const x of [-6.48, 1.48]) for (let i = 0; i < 6; i++) for (let j = 0; j < 4; j++) { M4.makeTranslation(x, -3.0 + j * .44 + .2, -3.1 + i * .62); depM.setMatrixAt(di++, M4); }
add(depM);
// gold bars in three stacks, coin heaps, a cage lamp, the alarm beacon, the pipe inlet
const BARS = [];
for (const [cx, cz] of [[-5.0, -2.4], [-.2, -2.4], [-2.5, .6]]) for (let l = 0; l < 4; l++) for (let i = 0; i < 4 - (l > 1 ? 1 : 0); i++) for (let j = 0; j < 3; j++) BARS.push([cx - .48 + i * .32 + (l % 2) * .08, -3.33 + l * .11, cz - .2 + j * .2]);
const barM = new THREE.InstancedMesh(new RoundedBoxGeometry(.3, .1, .16, 1, .02), goldM, BARS.length);
add(barM);
const HEAP = [];
for (const [cx, cz] of [[-4.0, -.4], [-1.0, -.6]]) for (let k = 0; k < 120; k++) { const a = hash(k + cx) * Math.PI * 2, r = Math.sqrt(hash(k * 3 + cz)) * .55, hgt = Math.max(0, .42 - r * .7); HEAP.push([cx + Math.cos(a) * r, -3.37 + hash(k * 7) * hgt, cz + Math.sin(a) * r, a]); }
const coinGeo = new THREE.CylinderGeometry(.07, .07, .016, 18);
const heapM = new THREE.InstancedMesh(coinGeo, goldM, HEAP.length);
HEAP.forEach(([x, y, z, a], i) => { M4.compose(V.set(x, y, z), Q.setFromAxisAngle(V2.set(Math.cos(a), 0, Math.sin(a)).normalize(), .3 * hash(i)), S.setScalar(1)); heapM.setMatrixAt(i, M4); });
add(heapM);
cyl(.01, .01, .3, ink, -2.5, -.45, -1.0, 4); sph(.13, glow(0xFFE7B0), -2.5, -.65, -1.0);
const beacon = add(new THREE.Mesh(new THREE.CylinderGeometry(.12, .14, .2, 16), new THREE.MeshStandardMaterial({ color: 0x5a1a14, emissive: 0xff2a18, emissiveIntensity: 0 }))); beacon.position.set(.9, -.55, -3.38);
// the glass money pipe: from the vault, out through the ground, up the house, over the roof to where the portal opens
const PIPE = new THREE.CatmullRomCurve3([[.9, -1.15, -2.9], [.95, -.5, -2.95], [1.7, -.25, -3.05], [1.95, .5, -3.0], [1.95, 6.3, -3.0], [2.25, 7.7, -2.8], [3.0, 9.1, -2.2], [3.6, 10.3, -1.6]].map(v3), false, "centripetal");
add(new THREE.Mesh(new THREE.TubeGeometry(PIPE, 160, .15, 14, false), new THREE.MeshPhysicalMaterial({ color: 0xE9F4F6, transparent: true, opacity: .28, roughness: .05, envMap: ENV, envMapIntensity: 1.2, side: THREE.DoubleSide, depthWrite: false })), false, false);
for (const u of [.12, .3, .5, .7, .86]) { const p = PIPE.getPointAt(u); const r = add(new THREE.Mesh(new THREE.TorusGeometry(.17, .03, 8, 20), metal(0xB0A898))); r.position.copy(p); r.lookAt(p.clone().add(PIPE.getTangentAt(u))); }
const funnel = add(new THREE.Mesh(new THREE.CylinderGeometry(.35, .16, .35, 20, 1, true), metal(0xB0A898))); funnel.position.set(.9, -1.32, -2.9); funnel.material.side = THREE.DoubleSide;
const PORTAL = PIPE.getPointAt(1).clone().add(V.set(.5, .9, .5));
const portalRing = add(new THREE.Mesh(new THREE.TorusGeometry(1.1, .1, 12, 64), new THREE.MeshStandardMaterial({ color: CORAL, emissive: CORAL, emissiveIntensity: 1.6 })), false, false);
portalRing.position.copy(PORTAL);
const portalDisc = add(new THREE.Mesh(new THREE.CircleGeometry(1.05, 48), texMat("swirl", { side: THREE.DoubleSide, depthWrite: false })), false, false);
portalDisc.position.copy(PORTAL);

// ---------------------------------------------------------------- the money tree (grows in week 2)
const treeG = new THREE.Group(); treeG.position.set(4.6, .05, .4); ROOT3.add(treeG);
add(new THREE.Mesh(new THREE.CylinderGeometry(.09, .16, 1.6, 10).translate(0, .8, 0), mat(0x8A6446)), true, true, treeG);
for (let k = 0; k < 4; k++) { const b = add(new THREE.Mesh(new THREE.CylinderGeometry(.04, .07, .7, 8).translate(0, .35, 0), mat(0x8A6446)), true, true, treeG); b.position.set(0, 1.2 + k * .12, 0); b.rotation.set(.7 * Math.cos(k * 1.7), k * 1.6, .7 * Math.sin(k * 1.7)); }
const CANOPY = [[0, 2.1, 0, .75], [.45, 1.8, .2, .5], [-.42, 1.85, -.1, .52], [.1, 1.75, -.45, .48]];
const canopyM = mat(0x6E9A5C);
const canopies = CANOPY.map(([x, y, z, r]) => { const m = add(new THREE.Mesh(new THREE.IcosahedronGeometry(r, 1), canopyM), true, true, treeG); m.position.set(x, y, z); return m; });
const LEAF_N = 80, LEAVES = [];
for (let k = 0; k < LEAF_N; k++) { const [cx, cy, cz, r] = CANOPY[k % 4]; const th = hash(k * 2.1) * Math.PI * 2, ph = Math.acos(2 * hash(k * 3.7) - 1); LEAVES.push([cx + Math.sin(ph) * Math.cos(th) * r * 1.02, cy + Math.cos(ph) * r * 1.02, cz + Math.sin(ph) * Math.sin(th) * r * 1.02, th, ph]); }
const leafM = new THREE.InstancedMesh(new THREE.CylinderGeometry(.075, .075, .016, 16), goldM, LEAF_N);
treeG.add(leafM);
// a planter
box(.9, .3, .9, mat(0xC9644E), 4.6, .15, .4, { round: .06 });

// ---------------------------------------------------------------- the phone company: tower, sign, balcony, its robot
const towerTex = canvasTex(256, 1024, (g, w, h) => { g.fillStyle = "#AFC3D4"; g.fillRect(0, 0, w, h); for (let i = 0; i < 4; i++) for (let j = 0; j < 18; j++) { g.fillStyle = (hash(i * 7 + j) > .6) ? "#E8EEF2" : "#8DA5BA"; g.fillRect(14 + i * 60, 14 + j * 56, 48, 42); } });
const tower = box(2.2, 9.2, 2.0, new THREE.MeshStandardMaterial({ map: towerTex, roughness: .3, metalness: .3, envMap: ENV, envMapIntensity: .6 }), 7.3, 4.6, -4.6);
box(2.4, .3, 2.2, mat(0x34508F), 7.3, 9.3, -4.6);
const signM = texMat("sign"); box(2.0, .5, .05, signM, 7.3, 8.6, -3.57, { cast: false });
box(1.4, .12, 1.1, mat(0xE6DCC8), 5.5, 5.95, -3.95); box(1.4, .5, .05, new THREE.MeshPhysicalMaterial({ color: 0xE9F4F6, transparent: true, opacity: .35, envMap: ENV }), 5.5, 6.25, -3.42, { cast: false });
const ROBOT = (() => {
  const g = new THREE.Group(); g.position.set(5.6, 6.02, -4.05); g.rotation.y = -.4; ROOT3.add(g);
  const blue = gloss(BLUE);
  add(new THREE.Mesh(new RoundedBoxGeometry(.5, .55, .34, 2, .1), blue), true, true, g).position.y = .55;
  for (const s of [-1, 1]) { const l = add(new THREE.Mesh(new THREE.CylinderGeometry(.06, .06, .3, 10), metal(0x8C8780)), true, true, g); l.position.set(s * .13, .15, 0); }
  const head = new THREE.Group(); head.position.y = 1.08; g.add(head);
  add(new THREE.Mesh(new RoundedBoxGeometry(.6, .44, .42, 3, .12), blue), true, true, head);
  const face = add(new THREE.Mesh(new THREE.PlaneGeometry(.48, .3), texMat("botA")), false, false, head); face.position.z = .215;
  const ant = add(new THREE.Mesh(new THREE.CylinderGeometry(.012, .012, .25, 6), metal(0x8C8780)), true, true, head); ant.position.y = .34;
  const bulb = add(new THREE.Mesh(new THREE.SphereGeometry(.045, 10, 8), new THREE.MeshStandardMaterial({ color: 0xff8a6a, emissive: 0xff5a3a, emissiveIntensity: 1 })), false, false, head); bulb.position.y = .48;
  const arms = [-1, 1].map((s) => { const p = new THREE.Group(); p.position.set(s * .3, .76, 0); g.add(p); const a = add(new THREE.Mesh(new THREE.CapsuleGeometry(.05, .32, 4, 8).translate(0, -.2, 0), blue), true, true, p); const hnd = add(new THREE.Mesh(new THREE.SphereGeometry(.07, 10, 8), metal(0x8C8780)), true, true, p); hnd.position.y = -.42; return p; });
  return { g, head, face, bulb, arms };
})();

// ---------------------------------------------------------------- another country: a floating street at night
const ISL = new THREE.Group(); ISL.position.set(15, 0, -17); ROOT3.add(ISL);
const ib = (w, h, d, c, x, y, z, o) => box(w, h, d, c, x, y, z, { ...o, parent: ISL });
ib(7.4, 2.4, 5.2, mat(0x6E6A72), 0, 1.2, 0, { round: .4 });
ib(7.4, .08, 1.6, mat(0x55525a), 0, 2.44, 1.3);
ib(7.4, .14, 1.4, mat(0x8a8790), 0, 2.47, -.2);
const facadeTex = canvasTex(512, 512, (g, w, h) => { g.fillStyle = "#4E4A5C"; g.fillRect(0, 0, w, h); for (let i = 0; i < 5; i++) for (let j = 0; j < 5; j++) { g.fillStyle = hash(i * 5 + j + 2) > .55 ? "#FFD98A" : "#2E2B38"; g.fillRect(24 + i * 98, 30 + j * 96, 66, 60); } });
ib(3.2, 4.6, 1.6, new THREE.MeshStandardMaterial({ map: facadeTex, roughness: .8 }), -1.9, 4.8, -1.8);
ib(2.8, 3.8, 1.6, new THREE.MeshStandardMaterial({ map: facadeTex, roughness: .8 }), 1.9, 4.4, -1.8);
const neonM = texMat("neon"); ib(1.9, .55, .05, neonM, -1.6, 4.0, -.98, { cast: false });
// the ATM: body, screen, keypad, slot
ib(.8, 1.5, .5, mat(0x3a3742, { roughness: .4 }), -.8, 3.25, -.85, { round: .05 });
const atmM = texMat("atm0"); const atmScr = ib(.5, .36, .02, atmM, -.8, 3.55, -.59, { cast: false });
ib(.36, .2, .04, mat(0x22202a), -.8, 3.12, -.57); ib(.26, .03, .04, glow(0x7fffb0), -.8, 3.28, -.57, { cast: false });
const ATM = new THREE.Vector3(14.2, 3.55, -17.58);
// street lamp, puddles, a scooter
const lp = ib(.06, 3.0, .06, ink, 2.9, 3.9, .8); ib(.4, .1, .2, glow(0xffd9a0), 2.75, 5.35, .8, { cast: false });
for (const [x, z] of [[-.2, 1.4], [1.6, 1.0]]) { const pd = ib(1.1, .01, .5, new THREE.MeshStandardMaterial({ color: 0x2c3045, roughness: .05, metalness: .5, envMap: ENV }), x, 2.49, z, { cast: false }); pd.rotation.y = x; }
// the shield and the X when the payment is stopped
const shield = add(new THREE.Mesh(new THREE.IcosahedronGeometry(.75, 1), new THREE.MeshBasicMaterial({ color: CORAL, wireframe: true, transparent: true, opacity: 0, toneMapped: false })), false, false);
shield.position.copy(ATM);
const xMark = new THREE.Group(); xMark.position.copy(ATM).add(V.set(0, .9, .3)); ROOT3.add(xMark);
for (const s of [-1, 1]) { const b = add(new THREE.Mesh(new THREE.BoxGeometry(.7, .12, .06), glow(0xff3a28)), false, false, xMark); b.rotation.z = s * .785; }

// ---------------------------------------------------------------- the bank's AI: the orb with an eye
const orb = new THREE.Group(); scene.add(orb);
const orbCoreM = new THREE.MeshStandardMaterial({ color: CORAL, emissive: CORAL, emissiveIntensity: 1.0, roughness: .35 });
orb.add(new THREE.Mesh(new THREE.SphereGeometry(.42, 40, 28), orbCoreM));
orb.add(new THREE.Mesh(new THREE.SphereGeometry(.52, 40, 28), new THREE.MeshPhysicalMaterial({ color: CREAM, transparent: true, opacity: .22, roughness: .05, envMap: ENV })));
const ring1 = new THREE.Mesh(new THREE.TorusGeometry(.72, .03, 8, 64), mat(INK, { roughness: .5 }));
const ring2 = new THREE.Mesh(new THREE.TorusGeometry(.88, .022, 8, 64), new THREE.MeshStandardMaterial({ color: CORAL, emissive: CORAL, emissiveIntensity: .6 }));
orb.add(ring1, ring2);
const eyeG = new THREE.Group(); orb.add(eyeG);
const eyeW = new THREE.Mesh(new THREE.CircleGeometry(.2, 32), glow(0xFFFDF8)); eyeW.position.z = .43; eyeG.add(eyeW);
const eyeP = new THREE.Mesh(new THREE.CircleGeometry(.09, 24), glow(0x1E1B18)); eyeP.position.z = .435; eyeG.add(eyeP);
const eyeLid = new THREE.Mesh(new THREE.CircleGeometry(.205, 32), new THREE.MeshBasicMaterial({ color: CORAL, toneMapped: false })); eyeLid.position.z = .437; eyeG.add(eyeLid);
const orbLight = new THREE.PointLight(0xff9a7a, 1.2, 4, 1.6); orb.add(orbLight);
// beam from the orb to whatever it is working on
const beamPos = new Float32Array(6);
const beamG = new THREE.BufferGeometry(); beamG.setAttribute("position", new THREE.BufferAttribute(beamPos, 3));
const beamM = new THREE.LineBasicMaterial({ color: CORAL, transparent: true, opacity: 0, toneMapped: false });
scene.add(new THREE.LineSegments(beamG, beamM));
const pulseM = new THREE.InstancedMesh(new THREE.SphereGeometry(.06, 10, 8), glow(CORAL), 10); scene.add(pulseM);

// ---------------------------------------------------------------- floating props: subscriptions, bubbles, bill, shoe, card
const SUBP = [[-5.05, 1.55, -1.55, .18], [-4.55, 1.82, -1.4, .06], [-4.05, 1.82, -1.4, -.06], [-3.55, 1.55, -1.55, -.18]];
const subCards = SUBP.map((p, k) => {
  const g = new THREE.Group(); scene.add(g);
  add(new THREE.Mesh(new RoundedBoxGeometry(.46, .3, .03, 2, .04), mat(CREAM)), true, false, g);
  const f = add(new THREE.Mesh(new THREE.PlaneGeometry(.43, .27), texMat("sub" + k)), false, false, g); f.position.z = .017;
  const st = add(new THREE.Mesh(new THREE.PlaneGeometry(.44, .14), texMat("stamp")), false, false, g); st.position.z = .02; st.rotation.z = -.25;
  return { g, st };
});
const BUB = [[4.75, 7.55, -2.1, 0], [5.75, 7.8, -3.75, 1], [4.7, 8.05, -2.15, 0], [5.7, 8.3, -3.7, 1]];
const bubbles = BUB.map(([x, y, z, side], k) => {
  const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = -.5; scene.add(g);
  add(new THREE.Mesh(new RoundedBoxGeometry(1.15, .38, .05, 2, .12), mat(side ? 0xDCE8F8 : 0xFFE3D8)), false, false, g);
  const f = add(new THREE.Mesh(new THREE.PlaneGeometry(1.08, .33), texMat("bub" + k)), false, false, g); f.position.z = .028;
  return g;
});
const billG = new THREE.Group(); billG.position.set(5.25, 6.85, -2.95); billG.rotation.y = -.45; scene.add(billG);
add(new THREE.Mesh(new THREE.BoxGeometry(.62, .86, .01), mat(CREAM)), true, false, billG);
const billA = add(new THREE.Mesh(new THREE.PlaneGeometry(.6, .84), texMat("billA")), false, false, billG); billA.position.z = .006;
const billB = add(new THREE.Mesh(new THREE.PlaneGeometry(.6, .84), texMat("billB")), false, false, billG); billB.position.z = .007;
const shoeG = new THREE.Group(); scene.add(shoeG);
const holo = new THREE.MeshStandardMaterial({ color: 0x7fe6ff, emissive: 0x4fd0ff, emissiveIntensity: .9, transparent: true, opacity: .75 });
add(new THREE.Mesh(new RoundedBoxGeometry(.5, .14, .2, 2, .05), holo), false, false, shoeG).position.set(0, .07, 0);
add(new THREE.Mesh(new RoundedBoxGeometry(.28, .18, .19, 2, .06), holo), false, false, shoeG).position.set(-.1, .2, 0);
add(new THREE.Mesh(new RoundedBoxGeometry(.52, .04, .22, 1, .02), new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xffffff, emissiveIntensity: .6, transparent: true, opacity: .8 })), false, false, shoeG);
const buyTag = add(new THREE.Mesh(new THREE.PlaneGeometry(.42, .14), texMat("buy")), false, false, shoeG); buyTag.position.set(0, .42, 0);
const cardG = new THREE.Group(); scene.add(cardG);
add(new THREE.Mesh(new RoundedBoxGeometry(.5, .32, .02, 2, .03), gloss(0x2A2623)), true, false, cardG);
const cardFace = add(new THREE.Mesh(new THREE.PlaneGeometry(.48, .3), texMat("card")), false, false, cardG); cardFace.position.z = .011;
const frost = add(new THREE.Mesh(new THREE.PlaneGeometry(.52, .34), new THREE.MeshStandardMaterial({ color: 0xE6F6FF, transparent: true, opacity: 0, roughness: .2, emissive: 0x9fd8ff, emissiveIntensity: .3 })), false, false, cardG); frost.position.z = .014;
const ICE_N = 26;
const iceM = new THREE.InstancedMesh(new THREE.ConeGeometry(.035, .16, 5), new THREE.MeshStandardMaterial({ color: 0xDDF3FF, transparent: true, opacity: .85, roughness: .05, metalness: .1, envMap: ENV, emissive: 0x6fbfff, emissiveIntensity: .25 }), ICE_N);
cardG.add(iceM);
const thiefCard = new THREE.Mesh(new RoundedBoxGeometry(.25, .16, .01, 1, .015), gloss(0x2A2623)); scene.add(thiefCard);
const phoneHolo = new THREE.Mesh(new THREE.PlaneGeometry(.5, .14), texMat("phoneTxt")); scene.add(phoneHolo);

// ---------------------------------------------------------------- coins in flight (instanced)
const FLY_N = 4 * 14 + 30 + 60;
const flyM = new THREE.InstancedMesh(coinGeo, goldM, FLY_N); scene.add(flyM);
const JAR_N = 46; const jarM = new THREE.InstancedMesh(coinGeo, goldM, JAR_N); scene.add(jarM);
const RAIN_N = 0;
// the real-world beat: a whole world of homes; every payment pulses to the AI, the bad ones are stopped
const GRID = [];
for (let i = -16; i <= 16; i++) for (let j = -16; j <= 16; j++) { if (Math.abs(i) < 3 && Math.abs(j) < 3) continue; GRID.push([i * 5 + (hash(i * 31 + j) - .5) * 1.6, j * 5 + (hash(j * 17 + i) - .5) * 1.6, hash(i * 7 + j * 13)]); }
const homeM = new THREE.InstancedMesh(new RoundedBoxGeometry(1.4, 1.1, 1.2, 1, .1).translate(0, .55, 0), mat(0xFFFDF8), GRID.length);
const roofM2 = new THREE.InstancedMesh(new THREE.ConeGeometry(1.05, .7, 4).rotateY(Math.PI / 4).translate(0, 1.45, 0), mat(0xC9644E), GRID.length);
scene.add(homeM, roofM2);
const PAY_N = 520;
const payM = new THREE.InstancedMesh(new THREE.SphereGeometry(.16, 8, 6), glow(0xffffff), PAY_N); scene.add(payM);
const worldGround = box(240, .2, 240, mat(0xE9DDC8), 0, -4.4, 0, { cast: false }); worldGround.receiveShadow = true;

// ---------------------------------------------------------------- people: one articulated figure builder
// joints in the figure's own frame (y up, facing +z, feet at y = 0); arms and legs are solved with two-bone IK from
// hand and foot targets; every limb is a capsule placed between two joints
const QA = new THREE.Quaternion(), SA = new THREE.Vector3(), VA = new THREE.Vector3(), VB = new THREE.Vector3(), VC = new THREE.Vector3();
function seg(mesh, a, b, baseLen, rx = 1, rz = 1) {
  VA.subVectors(b, a); const len = Math.max(1e-4, VA.length()); VA.divideScalar(len);
  QA.setFromUnitVectors(UP, VA);
  mesh.matrix.compose(VB.addVectors(a, b).multiplyScalar(.5), QA, SA.set(rx, len / baseLen, rz));
  mesh.matrixWorldNeedsUpdate = true;
}
function ik(s, h, l1, l2, pole, out) {
  VA.subVectors(h, s); let d = VA.length(); const dir = VA.clone().divideScalar(d || 1);
  d = Math.min(d, l1 + l2 - 1e-3);
  const a = (l1 * l1 - l2 * l2 + d * d) / (2 * d), hh = Math.sqrt(Math.max(0, l1 * l1 - a * a));
  const p = pole.clone().sub(dir.clone().multiplyScalar(pole.dot(dir))).normalize();
  return out.copy(s).addScaledVector(dir, a).addScaledVector(p, hh);
}
const skinMat = (c) => new THREE.MeshStandardMaterial({ color: c, roughness: .6 });
function makePerson({ top, pants, shoe, skin, hair, hood = false }) {
  const P = { parts: [] };
  const mk = (geo, m, cast = true) => { const x = new THREE.Mesh(geo, m); x.matrixAutoUpdate = false; x.castShadow = cast; x.receiveShadow = true; scene.add(x); P.parts.push(x); return x; };
  const cloth = (c) => new THREE.MeshStandardMaterial({ color: c, roughness: .9 });
  const sk = skinMat(skin), tp = cloth(top), pt = cloth(pants), sh = new THREE.MeshStandardMaterial({ color: shoe, roughness: .5 }), hr = new THREE.MeshStandardMaterial({ color: hair, roughness: .95 });
  P.torso = mk(new THREE.CapsuleGeometry(.17, .3, 6, 16), tp); P.torsoLen = .64;
  P.pelvis = mk(new THREE.SphereGeometry(.165, 16, 12), pt);
  P.hoodRing = mk(new THREE.TorusGeometry(.12, .055, 8, 20), tp);
  P.pocket = mk(new RoundedBoxGeometry(.24, .1, .04, 1, .02), cloth(new THREE.Color(top).multiplyScalar(.85)));
  P.thigh = [0, 1].map(() => mk(new THREE.CapsuleGeometry(.078, .36, 4, 10), pt));
  P.shin = [0, 1].map(() => mk(new THREE.CapsuleGeometry(.064, .36, 4, 10), pt));
  P.shoe = [0, 1].map(() => mk(new RoundedBoxGeometry(.13, .09, .28, 2, .04), sh));
  P.sole = [0, 1].map(() => mk(new THREE.BoxGeometry(.135, .025, .29), new THREE.MeshStandardMaterial({ color: 0xF4EFE6 })));
  P.uarm = [0, 1].map(() => mk(new THREE.CapsuleGeometry(.06, .2, 4, 10), tp));
  P.farm = [0, 1].map(() => mk(new THREE.CapsuleGeometry(.052, .18, 4, 10), tp));
  P.cuff = [0, 1].map(() => mk(new THREE.CylinderGeometry(.056, .056, .05, 12), cloth(new THREE.Color(top).multiplyScalar(.8))));
  P.hand = [0, 1].map(() => mk(new THREE.SphereGeometry(.054, 12, 10), sk));
  P.thumb = [0, 1].map(() => mk(new THREE.CapsuleGeometry(.018, .04, 3, 6), sk));
  P.neck = mk(new THREE.CylinderGeometry(.055, .062, .14, 12), sk);
  P.head = mk(new THREE.SphereGeometry(.135, 30, 24), sk);
  P.ear = [0, 1].map(() => mk(new THREE.SphereGeometry(.032, 10, 8), sk));
  // hair: a cap tilted back (forehead free), a soft fringe on top, short sides above the ears
  P.hairCap = mk(new THREE.SphereGeometry(.146, 32, 18, 0, Math.PI * 2, 0, Math.PI * .56), hr);
  P.quiff = mk(new RoundedBoxGeometry(.2, .07, .12, 2, .035), hr);
  P.side = [0, 1].map(() => mk(new RoundedBoxGeometry(.03, .09, .1, 1, .014), hr));
  if (hood) P.hood = mk(new THREE.SphereGeometry(.18, 26, 18, Math.PI / 2 + .9, Math.PI * 2 - 1.8, 0, Math.PI * .72), new THREE.MeshStandardMaterial({ color: top, roughness: .9, side: THREE.DoubleSide }));
  const basic = (c) => new THREE.MeshBasicMaterial({ color: c });
  // a clean cartoon face: glossy dark eyes with a highlight (they squint to blink), soft brows, a small nose,
  // a small mouth (arc for smile / frown / flat, a filled oval for "o"), light cheeks
  P.eye = [0, 1].map(() => mk(new THREE.SphereGeometry(.024, 18, 14), new THREE.MeshStandardMaterial({ color: 0x241a14, roughness: .15, envMap: ENV, envMapIntensity: .6 }), false));
  P.hi = [0, 1].map(() => mk(new THREE.SphereGeometry(.0065, 8, 6), basic(0xF4EFE6), false));
  P.brow = [0, 1].map(() => mk(new RoundedBoxGeometry(.05, .013, .012, 1, .006), hr, false));
  P.nose = mk(new THREE.SphereGeometry(.016, 12, 10), skinMat(new THREE.Color(skin).multiplyScalar(.93)), false);
  P.cheek = [0, 1].map(() => mk(new THREE.CircleGeometry(.022, 16), new THREE.MeshBasicMaterial({ color: 0xE88C78, transparent: true, opacity: .35 }), false));
  P.mouthArc = mk(new THREE.TorusGeometry(.024, .0065, 6, 16, Math.PI), basic(0x6a2a20), false);
  P.mouthO = mk(new THREE.CircleGeometry(.016, 20), basic(0x5a1e18), false);
  P.sweat = mk(new THREE.SphereGeometry(.011, 10, 8).scale(1, 1.4, 1), new THREE.MeshStandardMaterial({ color: 0xBFE3F2, roughness: .05, envMap: ENV }), false);
  P.zzz = null;
  return P;
}
const YOU = makePerson({ top: 0x2E6F8E, pants: 0x2A3550, shoe: 0xF4EFE6, skin: 0xE0AC84, hair: 0x3A2618 });
const THIEF = makePerson({ top: 0x2b2a33, pants: 0x1E1D24, shoe: 0x3a3742, skin: 0x8a6a58, hair: 0x1E1B18, hood: true });
THIEF.cheek.forEach((c) => { c.visible = false; });
// the phone in your hand
const phoneG = new THREE.Group(); scene.add(phoneG);
add(new THREE.Mesh(new RoundedBoxGeometry(.085, .17, .014, 2, .008), mat(0x1E1B18, { roughness: .3 })), true, false, phoneG);
const phoneScr = add(new THREE.Mesh(new THREE.PlaneGeometry(.075, .155), texMat("app0", { transparent: false, toneMapped: false })), false, false, phoneG); phoneScr.position.z = .008;
const mug = new THREE.Group(); scene.add(mug);
add(new THREE.Mesh(new THREE.CylinderGeometry(.06, .05, .13, 16), mat(CORAL)), true, false, mug);
add(new THREE.Mesh(new THREE.TorusGeometry(.035, .012, 6, 12), mat(CORAL)), true, false, mug).position.set(.065, 0, 0);
add(new THREE.Mesh(new THREE.CircleGeometry(.052, 16).rotateX(-Math.PI / 2), mat(0x4a2a18)), false, false, mug).position.y = .055;

// poses: pelvis, chest, head, hands, feet in the figure's frame (y up, +z forward)
const POSE = {
  stand: { pel: [0, .95, 0], chest: [0, 1.38, .02], head: [0, 1.7, .03], hands: [[.27, .92, .05], [-.27, .92, .05]], feet: [[.12, .05, .04], [-.12, .05, .04]] },
  sit: { pel: [0, .7, -.05], chest: [0, 1.12, -.1], head: [0, 1.44, -.06], hands: [[.18, .78, .22], [-.2, .76, .2]], feet: [[.13, .05, .52], [-.13, .05, .52]] },
};
const J = { pel: new THREE.Vector3(), chest: new THREE.Vector3(), head: new THREE.Vector3(), hands: [new THREE.Vector3(), new THREE.Vector3()], feet: [new THREE.Vector3(), new THREE.Vector3()] };
function setPose(p) { J.pel.set(...p.pel); J.chest.set(...p.chest); J.head.set(...p.head); for (let k = 0; k < 2; k++) { J.hands[k].set(...p.hands[k]); J.feet[k].set(...p.feet[k]); } }
function blendPose(a, b, u) { setPose(a); const T2 = { pel: v3(b.pel), chest: v3(b.chest), head: v3(b.head) }; J.pel.lerp(T2.pel, u); J.chest.lerp(T2.chest, u); J.head.lerp(T2.head, u); for (let k = 0; k < 2; k++) { J.hands[k].lerp(v3(b.hands[k]), u); J.feet[k].lerp(v3(b.feet[k]), u); } }
const RM = new THREE.Matrix4(), HM = new THREE.Matrix4(), TMP = new THREE.Matrix4(), EU = new THREE.Euler();
const W_ = (v) => v.clone().applyMatrix4(RM);
const HEADW = { you: new THREE.Vector3(), thief: new THREE.Vector3() }, HEADM = { you: new THREE.Matrix4(), thief: new THREE.Matrix4() };
// draw a figure: root matrix RM must be set; ex = face; hr = head rotation {pitch, yaw, roll}
function drawPerson(P, ex, hr, key) {
  const pel = W_(J.pel), chest = W_(J.chest);
  P.pelvis.matrix.compose(pel, QA.setFromRotationMatrix(TMP.extractRotation(RM)), SA.set(1.05, .85, .9));
  // shoulders and hips sit on the torso's frame
  const right = new THREE.Vector3(1, 0, 0).transformDirection(RM), fwd = new THREE.Vector3(0, 0, 1).transformDirection(RM);
  const upT = VC.subVectors(chest, pel).normalize().clone();
  // the torso runs from the hips up to the shoulder line (a little wider than deep), so the collar sits on it
  seg(P.torso, pel.clone().addScaledVector(upT, -.05), chest.clone().addScaledVector(upT, .13), P.torsoLen, 1.15, .85);
  for (let k = 0; k < 2; k++) {
    const sx = k ? -1 : 1;
    const sh = chest.clone().addScaledVector(right, .2 * sx).addScaledVector(upT, .03);
    const hip = pel.clone().addScaledVector(right, .1 * sx).addScaledVector(upT, -.02);
    const hand = W_(J.hands[k]), foot = W_(J.feet[k]);
    const elbow = ik(sh, hand, .3, .28, right.clone().multiplyScalar(sx * .5).addScaledVector(upT, -1).addScaledVector(fwd, -.3), new THREE.Vector3());
    const knee = ik(hip, foot.clone().addScaledVector(upT, .06), .44, .44, fwd.clone().addScaledVector(upT, .2), new THREE.Vector3());
    seg(P.uarm[k], sh, elbow, .32); seg(P.farm[k], elbow, hand, .284);
    seg(P.cuff[k], hand.clone().lerp(elbow, .18), hand.clone().lerp(elbow, .3), .05);
    seg(P.thigh[k], hip, knee, .516); seg(P.shin[k], knee, foot.clone().addScaledVector(upT, .06), .488);
    P.hand[k].matrix.compose(hand, QA.identity(), SA.set(1, 1, 1));
    P.thumb[k].matrix.compose(hand.clone().addScaledVector(fwd, .03).addScaledVector(right, -sx * .03).addScaledVector(upT, .02), QA.setFromUnitVectors(UP, fwd), SA.set(1, 1, 1));
    const sq = QA.setFromRotationMatrix(TMP.extractRotation(RM));
    P.shoe[k].matrix.compose(foot.clone().addScaledVector(fwd, .06), sq, SA.set(1, 1, 1));
    P.sole[k].matrix.compose(foot.clone().addScaledVector(fwd, .06).addScaledVector(upT, -.045), sq, SA.set(1, 1, 1));
  }
  P.pocket.matrix.compose(pel.clone().lerp(chest, .3).addScaledVector(fwd, .16), QA.setFromRotationMatrix(TMP.extractRotation(RM)), SA.set(1, 1, 1));
  const neckA = chest.clone().addScaledVector(upT, .06), headC = W_(J.head);
  seg(P.neck, neckA, headC.clone().addScaledVector(upT, -.06), .14, 1.05, 1.05);
  P.hoodRing.matrix.compose(chest.clone().addScaledVector(upT, .115).addScaledVector(fwd, -.02), QA.setFromUnitVectors(V.set(0, 0, 1), upT), SA.set(1.2, 1.05, 1));
  // head frame: the root's rotation, then the head's own pitch / yaw / roll
  HM.copy(RM).setPosition(0, 0, 0).premultiply(TMP.makeTranslation(headC.x, headC.y, headC.z)).multiply(TMP.makeRotationFromEuler(EU.set(hr.pitch, hr.yaw, hr.roll, "YXZ")));
  HEADW[key].copy(headC); HEADM[key].copy(HM);
  const hp = (m, x, y, z, rx = 0, ry = 0, rz = 0, sx = 1, sy = 1, sz = 1) => { m.matrix.multiplyMatrices(HM, TMP.compose(V.set(x, y, z), QA.setFromEuler(EU.set(rx, ry, rz, "YXZ")), SA.set(sx, sy, sz))); };
  hp(P.head, 0, .01, 0, 0, 0, 0, .96, 1.05, 1);
  for (let k = 0; k < 2; k++) hp(P.ear[k], (k ? -1 : 1) * .126, 0, -.01, 0, 0, 0, .5, .95, .75);
  hp(P.hairCap, 0, .03, -.018, -.78, 0, 0, 1, .92, 1);
  hp(P.quiff, 0, .138, .035, -.42);
  for (let k = 0; k < 2; k++) hp(P.side[k], (k ? -1 : 1) * .127, .045, -.02, 0, 0, 0);
  if (P.hood) hp(P.hood, 0, .02, -.02, -.2);
  // the face (features sit on the head's surface)
  const squint = clamp((ex.lid - .25) / .75);
  for (let k = 0; k < 2; k++) {
    const sx = k ? -.044 : .044, b = k ? ex.br : ex.bl;
    const ox = ex.lx * .004, oy = ex.ly * .004;
    const ey = .02 + oy, es = ex.eyes;
    hp(P.eye[k], sx + ox, ey - .006 * squint, .121, 0, 0, 0, es * (1 + .25 * squint), Math.max(.2, 1.18 * es * (1 - .82 * squint)), .45);
    hp(P.hi[k], sx + ox + .008, ey + .009, .131, 0, 0, 0, squint > .7 ? .001 : 1, squint > .7 ? .001 : 1, 1);
    hp(P.brow[k], sx, .068 + ex.lift + (k === 0 && ex.bl < -.3 ? .008 : 0), .118, 0, 0, (k ? -1 : 1) * b);
    hp(P.cheek[k], sx * 1.55, -.03, .111, 0, (k ? -1 : 1) * .5, 0, 1, .65, 1);
  }
  hp(P.nose, 0, -.012, .13, 0, 0, 0, 1, .8, .7);
  const mo = ex.mouth, o = mo === "o", arc = !o;
  hp(P.mouthArc, 0, -.056 + (mo === "smile" ? .019 : 0), .121, 0, 0, mo === "smile" ? Math.PI : 0, arc ? 1 : .001, mo === "flat" ? .2 : arc ? 1 : .001, 1);
  hp(P.mouthO, 0, -.057, .1215, 0, 0, 0, o ? 1 : .001, o ? 1.3 : .001, 1);
  hp(P.sweat, .08, .08 - (ex.sweatY || 0), .084, 0, 0, 0, ex.sweat ? 1 : .001, ex.sweat ? 1 : .001, ex.sweat ? 1 : .001);
  for (const m of P.parts) m.matrixWorldNeedsUpdate = true;
}
function hidePerson(P) { for (const m of P.parts) { m.matrix.makeScale(0, 0, 0); m.matrixWorldNeedsUpdate = true; } }
const blinkAt = (seed, t) => { const p = 2.6 + hash(seed) * 1.6, u = (t + hash(seed * 3) * 7) % p; return u < .14 ? Math.sin(Math.PI * u / .14) : 0; };
const face0 = () => ({ mouth: "smile", bl: -.05, br: -.05, lift: 0, eyes: 1, lid: .28, lx: 0, ly: 0, sweat: 0 });

// ---------------------------------------------------------------- the story: where YOU are and what you do
// returns the root matrix in RM, the pose in J, face ex, head rotation hr, and what the hands hold
const LIEQ = new THREE.Quaternion().setFromEuler(new THREE.Euler(-Math.PI / 2, 0, 0));
function youAt(t) {
  const s = sceneOf(t);
  const st = { ex: face0(), hr: { pitch: 0, yaw: 0, roll: 0 }, phone: 0, mug: 0, visible: true };
  const ex = st.ex, hr = st.hr;
  const breath = Math.sin(t * 1.7) * .006;
  if (s === 0 || s === 1) {                               // the sofa
    RM.compose(V.set(-4.3, 0, -2.72), Q.identity(), S.setScalar(1));
    setPose(POSE.sit); J.chest.y += breath; J.head.y += breath;
    st.phone = 1;
    J.hands[0].set(.08, 1.0, .3); J.hands[1].set(-.06, .92, .28);
    if (s === 0) {
      const look = ss(t, C.ai - .2, C.ai + .3);                      // looks up at the cards
      hr.pitch = lerp(.38, -.05, look); ex.ly = lerp(-.7, .4, look);
      ex.lx = Math.sin(t * 1.1) * .4 * look;
      if (t > C.forgot - .2) { ex.mouth = "o"; ex.eyes = 1.3; ex.lid = 0; ex.bl = ex.br = -.35; ex.lift = .016; ex.ly = .2; ex.lx = 0; hr.pitch = -.08; J.hands[0].y += .05; }
    } else {
      hr.yaw = -.55; hr.pitch = .05; ex.lx = -.9;                       // watching the phone company lose on the TV
      ex.mouth = "smile";
      const pump = ss(t, C.forty - .25, C.forty + .05);
      if (pump > 0) { J.hands[0].set(lerp(.08, .3, pump), lerp(1.0, 1.55, pump) + Math.abs(Math.sin((t - C.forty) * 12)) * .07 * pump, lerp(.3, .2, pump)); ex.mouth = "o"; ex.eyes = 1.2; ex.lid = .05; hr.yaw = lerp(-.55, 0, pump); ex.lx = 0; st.phone = 2; }
    }
  } else if (s === 2) {                                   // 2 AM: sitting up in bed against the headboard, phone in hand
    RM.compose(V.set(-2.6, 3.22, -2.8), Q.identity(), S.setScalar(1));
    setPose(POSE.sit); J.chest.y += breath; J.head.y += breath; J.feet[0].set(.13, .62, .9); J.feet[1].set(-.13, .62, .9);
    J.hands[0].set(.07, 1.02, .32); J.hands[1].set(-.05, .95, .3); hr.pitch = .3;
    {
      st.phone = 1; ex.lid = .5; ex.mouth = "flat"; ex.ly = -.7; ex.bl = ex.br = .1;
      if (t > C.freezes - .1) { ex.mouth = "o"; ex.lid = .02; ex.eyes = 1.2; ex.bl = ex.br = -.35; ex.lift = .014; ex.ly = .2; hr.pitch = -.05; }
      if (t > C.card + .45) { ex.mouth = "frown"; ex.eyes = 1; ex.lid = .35; ex.bl = ex.br = .45; ex.lift = 0; }
    }
  } else if (s === 4) {                                   // 3 AM: fast asleep
    RM.compose(V.set(-2.6, 3.98, -1.17), LIEQ, S.setScalar(1));
    setPose(POSE.stand);
    {
      J.hands[0].set(.24, 1.0, .12); J.hands[1].set(-.24, 1.0, .12);
      ex.lid = 1; ex.mouth = "smile"; ex.bl = ex.br = -.1; hr.roll = .25 + Math.sin(t * .8) * .03;
    }
  } else if (s === 3) {                                    // the kitchen, coffee, a dance
    RM.compose(V.set(-.4, 0, -2.0), Q.identity(), S.setScalar(1));
    setPose(POSE.stand); J.chest.y += breath;
    const sip = Math.max(0, Math.sin((t - CU[2]) * 2.2 - 1.2));
    st.mug = 1;
    J.hands[1].set(lerp(-.2, -.06, sip), lerp(1.1, 1.58, sip), lerp(.25, .2, sip));
    J.hands[0].set(.3, .96, .42);
    hr.pitch = -.06 * sip; ex.lid = .3 - .2 * sip; ex.mouth = "smile";
    const dance = ss(t, C.up - .2, C.up + .2);
    if (dance > 0) {
      const b = Math.abs(Math.sin(t * 7)) * .07 * dance;
      J.pel.y += b; J.chest.y += b; J.head.y += b;
      J.hands[0].set(lerp(.3, .32, dance), lerp(.96, 1.85 + Math.sin(t * 7) * .1, dance), lerp(.42, .1, dance));
      J.hands[1].set(lerp(-.06, -.32, dance), lerp(1.1, 1.85 - Math.sin(t * 7) * .1, dance), lerp(.2, .1, dance));
      hr.roll = Math.sin(t * 7) * .15 * dance; ex.mouth = "o"; ex.lid = .45; ex.bl = ex.br = -.3; st.mug = 0;
    }
  } else if (s === 5) {                                    // day 30, the living room, the phone, panic
    RM.compose(V.set(-3.5, 0, -1.25), Q.identity(), S.setScalar(1));
    setPose(POSE.stand); J.chest.y += breath;
    st.phone = 1; J.hands[0].set(.06, 1.24, .32); J.hands[1].set(-.08, 1.18, .3); hr.pitch = .25; ex.ly = -.7; ex.mouth = "flat";
    if (t > C.savings - .2) { ex.mouth = "o"; ex.eyes = 1.25; ex.lid = 0; ex.bl = ex.br = -.35; ex.lift = .014; hr.pitch = .1; }
    const pan = ss(t, C.wont - .5, C.wont - .1);
    if (pan > 0) {
      J.hands[0].lerp(V.set(.15, 1.72, .03), pan); J.hands[1].lerp(V.set(-.15, 1.72, .03), pan);
      hr.pitch = lerp(.1, -.1, pan); ex.ly = .1; ex.sweat = 1; st.phone = pan > .5 ? 0 : 1;
      ex.lx = Math.sin(t * 9) * .4; hr.yaw = Math.sin(t * 3) * .12;
    }
  } else {                                                // outside in the garden, looking up at the orb
    RM.compose(V.set(3.4, 0, 2.3), Q.setFromAxisAngle(UP, -.5), S.setScalar(1));
    setPose(POSE.stand); J.chest.y += breath;
    hr.pitch = -.35; ex.ly = .8; ex.mouth = "flat"; ex.bl = ex.br = -.1;
    J.hands[0].set(.24, 1.0, .15); J.hands[1].set(-.24, 1.0, .15);
  }
  ex.lid = Math.max(ex.lid, blinkAt(3, t));
  return st;
}
function thiefAt(t) {
  const ex = { mouth: "flat", bl: .4, br: .4, lift: 0, eyes: .9, lid: .35, lx: 0, ly: .1, sweat: 0 };
  const hr = { pitch: .05, yaw: 0, roll: 0 };
  RM.compose(V.set(14.2, 2.54, -16.9), Q.setFromAxisAngle(UP, Math.PI), S.setScalar(1));
  setPose(POSE.stand);
  const ins = ss(t, C.tries - .4, C.tries + .1) * (1 - ss(t, C.blocked + .4, C.blocked + .8));
  J.hands[0].set(lerp(.27, .05, ins), lerp(.92, 1.0, ins), lerp(.05, .42, ins));
  const mad = ss(t, C.blocked + .3, C.blocked + .7);
  if (mad > 0) { J.hands[0].lerp(V.set(.3, 1.7, .1), mad); J.hands[1].lerp(V.set(-.3, 1.7, .1), mad); ex.mouth = "o"; ex.eyes = 1.2; ex.bl = ex.br = -.3; hr.pitch = -.15; }
  ex.lx = Math.sin(t * 1.3) * .3;
  ex.lid = Math.max(ex.lid, blinkAt(9, t));
  return { ex, hr };
}

// ---------------------------------------------------------------- the orb's path
const ORBK = [
  [0, [-3.3, 2.3, -.8]], [CU[0] - .01, [-3.0, 2.4, -.6]],
  [CU[0], [-2.0, 2.6, .6]], [CU[0] + 1.9, [4.9, 6.85, -2.35]], [CU[1] - .01, [4.9, 6.95, -2.35]],
  [CU[1], [-3.5, 5.35, -1.7]], [CU[2] - .01, [-3.6, 5.3, -1.8]],
  [CU[2], [.6, 2.25, -1.1]], [C.coffee + .4, [1.0, 2.4, -.6]], [C.up, [3.4, 3.0, 1.3]], [CU[3] - .01, [3.5, 3.1, 1.3]],
  [CU[3], [-1.5, 5.6, 1.0]], [CU[3] + 1.2, [15.8, 6.4, -15.0]], [CU[4] - .01, [15.6, 6.5, -15.0]],
  [CU[4], [-1.6, -1.6, .6]], [C.savings, [-.4, -1.2, -.4]], [C.go + .3, [3.3, 9.9, -.7]], [CU[5] - .01, [3.0, 10.1, -.4]],
  [CU[5], [0, 13, 0]], [CU[6] - .01, [0, 13.5, 0]],
  [CU[6], [-2.4, 9.6, 1.2]], [DUR + 1, [-2.4, 9.9, 1.2]],
];
function orbAt(t, out) {
  let i = 0; while (i < ORBK.length - 2 && t > ORBK[i + 1][0]) i++;
  const [a, pa] = ORBK[i], [b, pb] = ORBK[i + 1];
  const u = b - a < .05 ? 1 : ss(t, a, b);
  out.set(lerp(pa[0], pb[0], u), lerp(pa[1], pb[1], u), lerp(pa[2], pb[2], u));
  out.y += Math.sin(t * 1.6) * .06 + Math.sin(Math.PI * u) * (b - a > 1 ? .8 : 0);
  return out;
}

// ---------------------------------------------------------------- camera shots
const SH = { p: new THREE.Vector3(), l: new THREE.Vector3(), fov: 40 };
const fixed = (p, l, fov = 40) => () => { SH.p.set(...p); SH.l.set(...l); SH.fov = fov; return SH; };
const move = (a, b, p0, p1, l0, l1, f0, f1) => (t) => { const u = ss(t, a, b); SH.p.set(lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u), lerp(p0[2], p1[2], u)); SH.l.set(lerp(l0[0], l1[0], u), lerp(l0[1], l1[1], u), lerp(l0[2], l1[2], u)); SH.fov = lerp(f0, f1, u); return SH; };
const ORBP = new THREE.Vector3();
const orbShot = (dx, dy, dz, fov = 34) => (t) => { orbAt(t, ORBP); SH.p.set(ORBP.x + dx, ORBP.y + dy, ORBP.z + dz); SH.l.copy(ORBP); SH.fov = fov; return SH; };
// on a face: d in front, h above (along the head's own axes), side to its right; look a little below the eyes
const FV = new THREE.Vector3(), UV = new THREE.Vector3(), RV = new THREE.Vector3();
const faceShot = (key, d, h, side, fov, d1 = null, f1 = null, win = null) => (t) => {
  const M = HEADM[key];
  FV.set(0, 0, 1).transformDirection(M); UV.set(0, 1, 0).transformDirection(M); RV.set(1, 0, 0).transformDirection(M);
  let dd = d, ff = fov;
  if (win) { const u = ss(t, win[0], win[1]); ff = lerp(fov, f1, u); dd = d1 != null ? lerp(d, d1, u) : d * Math.tan(fov * Math.PI / 360) / Math.tan(ff * Math.PI / 360); }
  SH.p.copy(HEADW[key]).addScaledVector(FV, dd).addScaledVector(UV, h).addScaledVector(RV, side);
  SH.l.copy(HEADW[key]).addScaledVector(UV, -.05); SH.fov = ff; return SH;
};
const F = FOC;
const SHOTS = [
  { t: 0, tr: 0, f: move(0, C.ai - .2, [-3.15, 1.95, 2.3], [-3.3, 1.85, 1.7], [-4.15, 1.25, -1.9], [-4.15, 1.4, -1.8], 46, 44) },
  { t: F[0].a, tr: .45, f: orbShot(.9, .15, 1.9, 34) },
  { t: F[0].b, tr: .45, f: move(F[0].b, C.forgot, [-3.6, 1.75, .9], [-3.9, 1.7, .6], [-4.3, 1.55, -1.6], [-4.25, 1.4, -1.8], 42, 42) },
  { t: F[1].a, tr: .35, f: faceShot("you", 1.35, .04, .24, 30) },
  { t: CU[0], tr: 0, f: move(CU[0], CU[0] + 2.1, [10.5, 6.2, 11], [9.5, 7.6, 8.5], [-1, 3.2, -1.5], [4.6, 6.4, -2.6], 42, 38) },
  { t: F[2].a, tr: .5, f: fixed([3.7, 7.45, .3], [5.3, 7.0, -3.2], 38) },
  { t: F[2].b, tr: .4, f: fixed([4.75, 7.2, -1.1], [5.25, 7.15, -2.95], 34) },
  { t: C.forty - .35, tr: .35, f: fixed([-3.5, 1.55, .95], [-4.3, 1.25, -2.55], 38) },
  { t: CU[1], tr: 0, f: move(CU[1], C.shoes - .9, [-1.2, 5.0, 2.6], [-1.6, 4.85, 1.4], [-2.6, 4.2, -2.4], [-2.6, 4.35, -2.4], 44, 40) },
  { t: F[3].a, tr: .4, f: faceShot("you", 1.3, .02, .26, 30) },
  { t: F[3].b, tr: .35, f: fixed([-2.15, 4.75, -.75], [-2.6, 4.55, -2.0], 34) },
  { t: CU[2], tr: 0, f: move(CU[2], C.coffee + .2, [.8, 1.9, 2.1], [.5, 1.8, 1.5], [-.4, 1.4, -2.0], [-.4, 1.45, -2.0], 42, 40) },
  { t: C.coffee + .25, tr: .55, f: move(C.coffee + .25, C.up - .3, [2.0, 3.4, 8.6], [4.4, 3.6, 8.2], [2.0, 1.9, -.3], [3.8, 2.0, .2], 44, 42) },
  { t: C.up - .3, tr: .45, f: fixed([.5, 1.45, 2.4], [-.4, 1.98, -2.0], 46) },
  { t: CU[3], tr: 0, f: move(CU[3], F[4].a - .1, [17.5, 6.4, 7.5], [16.4, 5.0, -6.5], [11.0, 3.6, -13.0], [14.2, 3.7, -16.6], 42, 38) },
  { t: F[4].a, tr: .4, f: fixed([13.25, 4.15, -18.0], [14.2, 4.2, -16.9], 32) },
  { t: F[4].b, tr: .35, f: fixed([14.95, 3.75, -15.6], [14.2, 3.5, -17.5], 40) },
  { t: F[5].a, tr: .35, f: fixed([-2.2, 4.72, -2.0], [-2.6, 4.05, -2.85], 32) },
  { t: CU[4], tr: 0, f: move(CU[4], C.savings, [-2.5, -1.55, 3.9], [-2.5, -1.75, 2.5], [-2.5, -1.8, -3.0], [-2.4, -1.8, -2.6], 46, 44) },
  { t: C.savings + .1, tr: .4, f: move(C.savings + .1, C.go, [4.6, .2, 4.4], [6.4, 9.0, 5.4], [1.6, -.4, -2.6], [3.5, 9.6, -1.6], 46, 44) },
  { t: F[6].a, tr: .35, f: faceShot("you", 2.2, .05, .3, 18, null, 44, [F[6].a + .15, F[6].b]) },
  { t: CU[5], tr: 0, f: move(CU[5], CU[6] - .3, [0, 18, 15], [2, 92, 52], [-1, 1.5, -1], [0, 0, -4], 42, 40) },
  { t: CU[6], tr: 1.2, f: move(CU[6], DUR, [13, 10, 19], [9, 12.5, 21], [-1.2, 2.6, -1], [-1.2, 3.0, -1], 40, 40) },
];
const ease3 = (x) => (x < .5 ? 4 * x * x * x : 1 - (-2 * x + 2) ** 3 / 2);
const CAMP = new THREE.Vector3(), CAML = new THREE.Vector3(), PREV = { p: new THREE.Vector3(), l: new THREE.Vector3(), fov: 40 };
function camAt(t) {
  let i = 0; while (i < SHOTS.length - 1 && t >= SHOTS[i + 1].t) i++;
  const cur = SHOTS[i]; const r = cur.f(t);
  CAMP.copy(r.p); CAML.copy(r.l); let fov = r.fov;
  if (cur.tr > 0 && i > 0 && t < cur.t + cur.tr) {
    const pr = SHOTS[i - 1].f(t); PREV.p.copy(pr.p); PREV.l.copy(pr.l); PREV.fov = pr.fov;
    const u = ease3(ramp(t, cur.t, cur.t + cur.tr));
    const dist = PREV.p.distanceTo(CAMP);
    CAMP.lerpVectors(PREV.p, CAMP, u); CAMP.y += Math.sin(Math.PI * u) * Math.min(dist * .12, 3);
    CAML.lerpVectors(PREV.l, CAML, u); fov = lerp(PREV.fov, fov, u);
  }
  return fov;
}

// ---------------------------------------------------------------- lighting per scene
const LOOKS = [
  { bg: 0xF0DCC8, sky: 0xFFE9D2, gr: 0xCDB8A0, hi: .8, sun: 0xFFC49A, si: 1.4, sp: [12, 10, 14], lamp: 1.4, tv: .6, win: 0xF6C9A6 },     // day 1, evening
  { bg: 0xF1E9DC, sky: 0xFFF6EA, gr: 0xCDBFA8, hi: .95, sun: 0xFFF1DC, si: 2.0, sp: [10, 22, 14], lamp: 0, tv: 1.0, win: 0xBFD9EC },     // day 3
  { bg: 0x232A4E, sky: 0x6A78B8, gr: 0x22223a, hi: .42, sun: 0xA9BCFF, si: .45, sp: [-8, 18, 10], lamp: 0, tv: 0, win: 0x2A3666 },          // 2 AM
  { bg: 0xF6ECDA, sky: 0xFFF8EC, gr: 0xD5C6AE, hi: 1.0, sun: 0xFFF0D8, si: 2.3, sp: [14, 20, 12], lamp: 0, tv: 0, win: 0xCDE6F6 },        // week 2, morning
  { bg: 0x232A4E, sky: 0x6A78B8, gr: 0x22223a, hi: .55, sun: 0xA9BCFF, si: .6, sp: [-8, 18, 10], lamp: 0, tv: 0, win: 0x2A3666 },          // 3 AM
  { bg: 0xCFCCC6, sky: 0xE4E8EE, gr: 0xA9A397, hi: .7, sun: 0xDDE6F2, si: .95, sp: [8, 16, 12], lamp: 0, tv: 0, win: 0xC9D2DA },           // day 30, grey
  { bg: 0xF1E9DC, sky: 0xFFF6EA, gr: 0xCDBFA8, hi: .95, sun: 0xFFF1DC, si: 2.1, sp: [20, 40, 24], lamp: 0, tv: 0, win: 0xBFD9EC },      // real world
  { bg: 0xF1E9DC, sky: 0xFFF6EA, gr: 0xCDBFA8, hi: .95, sun: 0xFFF1DC, si: 2.1, sp: [14, 24, 16], lamp: 0, tv: 0, win: 0xBFD9EC },      // close
];

// ---------------------------------------------------------------- render at time t
const flyPos = new THREE.Vector3(), JARP = new THREE.Vector3();
const bezier = (p0, p1, p2, u, out) => out.set((1 - u) ** 2 * p0.x + 2 * (1 - u) * u * p1.x + u * u * p2.x, (1 - u) ** 2 * p0.y + 2 * (1 - u) * u * p1.y + u * u * p2.y, (1 - u) ** 2 * p0.z + 2 * (1 - u) * u * p1.z + u * u * p2.z);
const TREE_TOP = new THREE.Vector3(4.6, 2.2, .4);
function renderAt(t) {
  const s = sceneOf(t), Lk = LOOKS[s];
  scene.background.set(Lk.bg); scene.fog.color.set(Lk.bg);
  hemi.color.set(Lk.sky); hemi.groundColor.set(Lk.gr); hemi.intensity = Lk.hi;
  sun.color.set(Lk.sun); sun.intensity = Lk.si;
  winSkyM.color.set(Lk.win); nightWinM.color.set(Lk.win); moon.visible = s === 2 || s === 4;
  lampL.intensity = Lk.lamp; shade.material.emissiveIntensity = .2 + Lk.lamp * .5;
  tvL.intensity = Lk.tv * (.8 + .2 * Math.sin(t * 13)); tvScreenM.color.set(Lk.tv > 0 ? 0x6f9fe0 : 0x1b2440);
  kitchenL.intensity = s === 3 ? .6 : 0;
  bedL.intensity = 0; bedShade.material.emissiveIntensity = .05;
  bloom.strength = s === 2 || s === 4 ? .45 : .28; bloom.threshold = s === 2 || s === 4 ? .72 : .85;
  const night = s === 2 || s === 4;
  bedL.intensity = s === 4 ? .5 : 0; kitchenL.intensity = s === 4 ? .35 : kitchenL.intensity;

  // the orb
  orbAt(t, orb.position);
  const talk = Math.max(bump(t, C.calls - .3, C.forty, .3), bump(t, C.freezes - .4, C.card + .6, .2), bump(t, C.blocked - .5, C.eleven + .6, .2), bump(t, C.moves - .3, C.go + .4, .3));
  orbCoreM.emissiveIntensity = .9 + talk * 1.2 + (night ? .6 : 0) + Math.sin(t * 20) * .15 * talk;
  orb.scale.setScalar(1 + talk * .08);
  ring1.rotation.set(Math.PI / 2 + Math.sin(t * .7) * .4, t * .9, 0);
  ring2.rotation.set(Math.PI / 2.6, -t * 1.3 * (1 + talk), t * .4);
  orbLight.intensity = 1.0 + talk * 1.5;
  // the orb's eye looks at what it is working on (or at the camera in its close-up)
  const tgt = new THREE.Vector3();
  if (s === 0) tgt.set(-4.3, 1.6, -1.5); else if (s === 1) tgt.set(5.6, 7.1, -4.05); else if (s === 2) tgt.set(-2.6, 4.6, -2.0);
  else if (s === 3) tgt.copy(TREE_TOP); else if (s === 4) tgt.copy(ATM); else if (s === 5) tgt.set(-2.5, -2.6, -2.0); else tgt.copy(camera.position);
  if (t > FOC[0].a && t < FOC[0].b) tgt.copy(camera.position);
  eyeG.lookAt(tgt); eyeG.quaternion.premultiply(Q.copy(orb.quaternion).invert());
  eyeLid.scale.setScalar(Math.max(.001, blinkAt(17, t) * 1.0));
  eyeLid.position.z = .437 + (blinkAt(17, t) > .01 ? 0 : -.01);

  // YOU
  const st = youAt(t);
  drawPerson(YOU, st.ex, st.hr, "you");
  // the phone in the right hand, screen to the face; the mug in the left
  const handR = W_(J.hands[0]), handL = W_(J.hands[1]);
  phoneG.visible = st.phone > 0;
  if (st.phone) { phoneG.position.copy(handR).add(V.set(0, .05, 0)); phoneG.lookAt(HEADW.you); if (st.phone === 2) phoneG.rotateX(-.6); }
  mug.visible = st.mug > 0; mug.position.copy(handL).add(V.set(0, .02, .04));
  phoneL.position.copy(phoneG.position).add(V.copy(HEADW.you).sub(phoneG.position).multiplyScalar(.4));
  phoneL.intensity = st.phone && (s === 2 || s === 5) ? (s === 2 ? 1.1 : .5) : st.phone ? .25 : 0;
  setMap(phoneScr.material, TEX[s === 5 ? (t > C.savings ? "app3" : "app2") : s === 2 ? (t > C.freezes ? "app1b" : "app1") : "app0"]);

  // the hooded figure in the other country
  const th = thiefAt(t);
  drawPerson(THIEF, th.ex, th.hr, "thief");
  // card from their hand into the slot, then pushed back out
  const ins = ss(t, C.tries - .4, C.tries + .1), back = ss(t, C.blocked + .2, C.blocked + .6);
  thiefCard.position.copy(W_(J.hands[0])).lerp(V.copy(ATM).add(V2.set(0, -.3, .25)), ins * (1 - back));
  thiefCard.rotation.set(0, 0, 0); thiefCard.visible = t > CU[3] - 1 && t < CU[4];
  const atmKey = t < C.tries ? "atm0" : t < C.blocked - .1 ? "atm1" : "atm2";
  setMap(atmScr.material, TEX[atmKey]);
  atmL.color.set(atmKey === "atm2" ? 0xff4a3a : 0x7fffb0); atmL.intensity = s === 4 ? 2.2 : 0;
  neonA.intensity = neonB.intensity = s === 4 ? 4 : 0;
  const blk = s === 4 ? ss(t, C.blocked - .2, C.blocked + .1) : 0;
  shield.material.opacity = blk * (.6 + .4 * Math.sin(t * 14)); shield.scale.setScalar(.6 + .5 * blk + .05 * Math.sin(t * 10)); shield.rotation.y = t * .8;
  xMark.scale.setScalar(Math.max(.001, ss(t, C.blocked, C.blocked + .2) * (s === 4 ? 1 : 0) * (1 + .15 * Math.sin(t * 16))));

  // subscriptions: pop in, get stamped, burst into coins that drop into the jar
  let fly = 0, jarCount = 0;
  subCards.forEach((c, k) => {
    const [x, y, z, ry] = SUBP[k];
    const tin = C.ai + .2 + k * .18, tc = C.cancels + k * .32, burst = tc + .3;
    const sIn = s === 0 ? ss(t, tin, tin + .25) * (1 - ss(t, burst, burst + .12)) : 0;
    c.g.position.set(x, y + Math.sin(t * 2 + k) * .03, z); c.g.rotation.set(0, ry, Math.sin(t * 1.5 + k) * .04);
    c.g.scale.setScalar(Math.max(.001, sIn * (1 + .25 * pulse(t, tc, .08))));
    c.st.scale.setScalar(Math.max(.001, ss(t, tc, tc + .1) * (1.6 - .6 * ss(t, tc, tc + .12))));
    for (let j = 0; j < 14; j++) {
      const u = ramp(t, burst + j * .02, burst + .55 + j * .02);
      let sc = .001;
      if (s === 0 && u > 0 && u < 1) {
        const a = hash(k * 31 + j) * Math.PI * 2;
        bezier(V.set(x, y, z), V2.set(x + Math.cos(a) * .5, y + .5 + hash(j) * .3, z + Math.sin(a) * .3), JAR.clone().add(V3.set(0, .25, 0)), u, flyPos);
        sc = 1;
      } else flyPos.set(0, -50, 0);
      M4.compose(flyPos, Q.setFromEuler(EU.set(t * 9 + j, j, t * 7)), S.setScalar(sc)); flyM.setMatrixAt(fly++, M4);
      if (t > burst + .55 + j * .02 && s <= 1 && j % 2 === 0) jarCount += 1;
    }
  });
  for (let k = 0; k < JAR_N; k++) {
    const on = k < jarCount + (s >= 2 ? JAR_N : 0) ? 1 : .001;
    M4.compose(V.set(JAR.x + (hash(k) - .5) * .18, JAR.y - .14 + Math.floor(k / 4) * .016, JAR.z + (hash(k * 3) - .5) * .18), Q.setFromAxisAngle(UP, k), S.setScalar(on));
    jarM.setMatrixAt(k, M4);
  }
  jarM.instanceMatrix.needsUpdate = true;

  // day 3: the argument in chat bubbles, the robot gets flustered, the bill shrinks
  bubbles.forEach((g, k) => {
    const tb = C.argues - .5 + k * .5;
    const on = s === 1 ? ss(t, tb, tb + .18) * (1 - ss(t, C.forty + .3, C.forty + .6)) : 0;
    g.scale.setScalar(Math.max(.001, on * (1 + .15 * pulse(t, tb + .1, .08))));
    g.position.y = BUB[k][1] + Math.sin(t * 2 + k) * .02 + (t - tb) * .02 * on;
  });
  setMap(ROBOT.face.material, TEX[t > C.drops ? "botC" : t > C.argues + .6 ? "botB" : "botA"]);
  ROBOT.head.rotation.set(Math.sin(t * 3) * .05, (s === 1 && t > C.drops ? -.25 : 0), t > C.drops ? -.18 : Math.sin(t * 2) * .05);
  ROBOT.arms[0].rotation.z = .3 + (s === 1 ? Math.sin(t * 7) * .4 * bump(t, C.argues - .3, C.drops, .2) : 0);
  ROBOT.arms[1].rotation.z = -.3 - (s === 1 ? Math.sin(t * 6 + 1) * .4 * bump(t, C.argues - .3, C.drops, .2) : 0) + (t > C.drops ? -.8 : 0);
  ROBOT.bulb.material.emissiveIntensity = .6 + Math.sin(t * 10) * .5;
  const billOn = s === 1 ? ss(t, C.bill - .45, C.bill - .2) : 0;
  billG.scale.setScalar(Math.max(.001, billOn * lerp(1, .78, ss(t, C.drops, C.drops + .6))));
  billG.position.y = 6.75 + .4 * billOn + Math.sin(t * 1.8) * .03;
  billB.visible = t > C.drops + .3;

  // day 9: the sneaker hologram over the phone, then the card freezing over
  const shoeOn = s === 2 ? ss(t, C.two + .2, C.two + .6) * (1 - ss(t, C.freezes - .05, C.freezes + .15)) : 0;
  shoeG.position.set(-2.6, 4.62 + Math.sin(t * 2) * .03, -1.95); shoeG.rotation.set(.2, t * 1.4, 0);
  shoeG.scale.setScalar(Math.max(.001, shoeOn * (1 + .1 * Math.sin(t * 30) * ss(t, C.freezes - .3, C.freezes))));
  const cardOn = s === 2 ? ss(t, C.freezes - .4, C.freezes - .1) : 0;
  cardG.position.set(-2.6, 4.55 + Math.sin(t * 1.6) * .02, -1.85); cardG.rotation.set(-.35, Math.sin(t) * .15, .08);
  cardG.scale.setScalar(Math.max(.001, cardOn));
  const fr = ss(t, C.freezes, C.freezes + .7);
  frost.material.opacity = fr * .78;
  for (let k = 0; k < ICE_N; k++) {
    const g = ss(t, C.freezes + k * .025, C.freezes + .25 + k * .025);
    const a = k / ICE_N * Math.PI * 2;
    const ex = Math.cos(a) * .25, ey = Math.sin(a) * .16;
    M4.compose(V.set(ex * (1 + hash(k) * .1), ey * (1 + hash(k * 3) * .1), (hash(k * 5) - .5) * .05), Q.setFromEuler(EU.set(0, 0, a - Math.PI / 2 + (hash(k) - .5))), S.setScalar(Math.max(.001, g * (.6 + hash(k * 7) * .9))));
    iceM.setMatrixAt(k, M4);
  }
  iceM.instanceMatrix.needsUpdate = true;
  phoneHolo.visible = false;

  // week 2: coins arc from the coffee mug to the money tree, which grows coin leaves
  const grow = s >= 3 ? ss(t, C.coffee - .2, C.up + .4) : 0;
  treeG.scale.setScalar(Math.max(.15, s >= 3 ? lerp(.35, 1, grow) : .35));
  canopies.forEach((c, k) => c.scale.setScalar(Math.max(.001, s >= 3 ? lerp(.3, 1, ss(t, C.coffee + k * .3, C.coffee + .8 + k * .3)) : .3)));
  const leaves = s >= 3 ? Math.floor(LEAF_N * ss(t, C.coffee + .4, C.hundred + .2)) : 0;
  for (let k = 0; k < LEAF_N; k++) {
    const [x, y, z, th, ph] = LEAVES[k];
    const on = k < leaves ? 1 : .001;
    M4.compose(V.set(x, y, z), Q.setFromEuler(EU.set(ph + Math.sin(t * 3 + k) * .1, th, 0)), S.setScalar(on * (1 + .3 * pulse(t, C.coffee + .4 + k / LEAF_N * (C.hundred - C.coffee - .2), .08))));
    leafM.setMatrixAt(k, M4);
  }
  leafM.instanceMatrix.needsUpdate = true;
  const MUGP = mug.position.clone();
  for (let j = 0; j < 30; j++) {
    const t0 = C.coffee + j * .1, u = ramp(t, t0, t0 + .9);
    let sc = .001;
    if (s === 3 && u > 0 && u < 1) { bezier(MUGP, V2.set(2.2, 3.6, 5.4), TREE_TOP, u, flyPos); sc = 1.1; } else flyPos.set(0, -50, 0);
    M4.compose(flyPos, Q.setFromEuler(EU.set(t * 8 + j, j, 0)), S.setScalar(sc)); flyM.setMatrixAt(fly++, M4);
  }

  // day 30: the vault door swings open, the bars rise into the pipe and vanish through the portal
  const open = s === 5 ? ss(t, C.moves - .2, C.moves + .9) : 0;
  doorPivot.rotation.y = -open * 1.75;
  wheel.rotation.z = s === 5 ? -ss(t, CU[4] + .3, C.moves) * Math.PI * 2 : 0;
  vaultL.intensity = s === 5 ? (1.6 + (t > C.savings ? (Math.sin(t * 31) > .4 ? -1.2 : 0) : 0)) : 0;
  const alarm = s === 5 ? ss(t, C.moves, C.moves + .3) : 0;
  alarmL.intensity = alarm * (2.5 + 2.5 * Math.sin(t * 9));
  beacon.material.emissiveIntensity = alarm * (1.5 + Math.sin(t * 9) * 1.5); beacon.rotation.y = t * 6;
  const portal = s >= 5 ? ss(t, C.moves + .3, C.savings + .2) * (s === 5 ? 1 : 0) : 0;
  portalRing.scale.setScalar(Math.max(.001, portal * (1 + .05 * Math.sin(t * 8))));
  portalDisc.scale.setScalar(Math.max(.001, portal)); portalDisc.rotation.z = -t * 2.5; portalDisc.lookAt(camera.position);
  portalRing.lookAt(camera.position);
  BARS.forEach(([x, y, z], k) => {
    const t0 = C.savings - .1 + (k / BARS.length) * (C.go - C.savings), u = ramp(t, t0, t0 + 1.25);
    if (s === 5 && u > 0) {
      if (u < .2) { const w = u / .2; flyPos.set(lerp(x, .9, w), lerp(y, -1.0, w) + Math.sin(Math.PI * w) * .5, lerp(z, -2.9, w)); }
      else if (u < .95) PIPE.getPointAt((u - .2) / .75, flyPos);
      else flyPos.copy(PORTAL);
      M4.compose(flyPos, Q.setFromEuler(EU.set(t * 5 + k, k, 0)), S.setScalar(u < .95 ? (u < .2 ? 1 : .55) : Math.max(.001, 1 - (u - .95) * 20)));
    } else if (s === 5 || s < 5) M4.compose(V.set(x, y, z), Q.identity(), S.setScalar(1));
    if (s > 5) M4.makeScale(0, 0, 0);
    barM.setMatrixAt(k, M4);
  });
  barM.instanceMatrix.needsUpdate = true;
  heapM.visible = !(s === 5 && t > C.go - .3) && s <= 5;
  for (let j = 0; j < 60; j++) {                             // the loose coins go too
    const t0 = C.every - .2 + j * .03, u = ramp(t, t0, t0 + 1.1);
    let sc = .001;
    if (s === 5 && u > 0 && u < .97) { if (u < .2) flyPos.set(lerp(-4 + (hash(j) - .5), .9, u / .2), lerp(-3.2, -1.0, u / .2), lerp(-.4, -2.9, u / .2)); else PIPE.getPointAt((u - .2) / .77, flyPos); sc = .9; } else flyPos.set(0, -50, 0);
    M4.compose(flyPos, Q.setFromEuler(EU.set(t * 9 + j, j, 0)), S.setScalar(sc)); flyM.setMatrixAt(fly++, M4);
  }
  flyM.instanceMatrix.needsUpdate = true;

  // the beam from the orb to its work
  const work = new THREE.Vector3();
  const beamOn = Math.max(bump(t, C.calls, C.argues - .4, .2) * 0, bump(t, C.freezes - .3, C.card + .3, .15), bump(t, C.blocked - .5, C.eleven + .8, .15), bump(t, C.moves - .2, C.savings + .5, .2), bump(t, C.cancels - .2, C.cancels + 1.4, .15));
  if (s === 2) work.copy(cardG.position); else if (s === 4) work.copy(ATM); else if (s === 5) work.set(-2.5, -1.85, -3.3); else work.set(-4.3, 1.7, -1.45);
  beamPos.set([orb.position.x, orb.position.y, orb.position.z, work.x, work.y, work.z]); beamG.attributes.position.needsUpdate = true;
  beamM.opacity = .85 * beamOn;
  for (let k = 0; k < 10; k++) { const u = (t * 1.8 + k / 10) % 1; M4.compose(V.lerpVectors(orb.position, work, u), Q.identity(), S.setScalar(Math.max(.001, beamOn * (s === 2 ? .35 : 1)))); pulseM.setMatrixAt(k, M4); }
  pulseM.instanceMatrix.needsUpdate = true;

  // the real world: homes appear around the diorama; payments flow to the AI, the red ones stop and flash
  const wo = s === 6 ? ss(t, CU[5] + .4, C.visa + .5) : s === 7 ? 1 - ss(t, CU[6], CU[6] + 1.2) : 0;
  GRID.forEach(([x, z, h], k) => {
    const on = wo * ss(wo, h * .6, h * .6 + .4);
    M4.compose(V.set(x, -4.3, z), Q.setFromAxisAngle(UP, h * 6), S.setScalar(Math.max(.001, on * (1.6 + h * 1.6))));
    homeM.setMatrixAt(k, M4); roofM2.setMatrixAt(k, M4);
  });
  homeM.instanceMatrix.needsUpdate = roofM2.instanceMatrix.needsUpdate = true;
  const ORBW = orb.position;
  for (let k = 0; k < PAY_N; k++) {
    const g = GRID[Math.floor(hash(k * 3.3) * GRID.length)];
    const per = 1.6 + hash(k) * 1.2, u = ((t * (1 + ss(t, C.checks, C.payment)) + hash(k * 7) * per) % per) / per;
    const bad = hash(k * 11) < .12;
    const uu = bad ? Math.min(u, .55) : u;
    V.set(lerp(g[0], ORBW.x, uu), lerp(-2.5, ORBW.y, uu) + Math.sin(Math.PI * uu) * 6, lerp(g[1], ORBW.z, uu));
    const on = wo * (s === 6 ? 1 : 0) * (bad && u > .55 ? Math.max(0, 1 - (u - .55) * 4) * 2 : 1);
    M4.compose(V, Q.identity(), S.setScalar(Math.max(.001, on * (bad ? 1.6 : 1))));
    payM.setMatrixAt(k, M4); payM.setColorAt(k, tmpC.set(bad ? 0xff3a28 : (k % 3 ? 0xF2B33D : 0x3FA372)));
  }
  payM.instanceMatrix.needsUpdate = true; if (payM.instanceColor) payM.instanceColor.needsUpdate = true;
  worldGround.visible = s >= 6;

  // clock on the nightstand
  setMap(clock.material, TEX[s === 4 ? "clock2" : "clock"]);
  clock.visible = night;

  // tension: letterbox, handheld, AI vision, blur, flashes
  const bars = Math.max(bump(t, C.someone - .5, CU[4] - .3, .4), bump(t, CU[4], CU[5] - .2, .4));
  const scan = Math.max(.8 * bump(t, C.cancels - .4, C.cancels + 1.6, .25), .7 * bump(t, C.argues - .2, C.drops + .2, .25), bump(t, C.blocked - .6, C.eleven + .9, .2));
  let fl = 0; for (const ct of CU) fl += .7 * Math.exp(-(((t - ct) / .07) ** 2)) * (t >= ct ? 1 : .2);
  fl += .4 * pulse(t, C.freezes, .08) + .35 * pulse(t, C.blocked, .08) + .25 * pulse(t, C.moves + .1, .08);
  grade.uniforms.uFlash.value = fl;
  grade.uniforms.uSat.value = 1 - scan * .3;
  grade.uniforms.uCool.value = s === 2 ? .5 * fr + .3 : s === 5 ? .35 : 0;
  grade.uniforms.uRed.value = s === 5 ? alarm * (.5 + .35 * Math.sin(t * 9)) : 0;
  grade.uniforms.uBars.value = bars;
  grade.uniforms.uScan.value = scan;
  grade.uniforms.uCon.value = .12 * bars;
  grade.uniforms.uBlur.value = .02 * pulse(t, CU[0] + .8, .5) + .025 * pulse(t, CU[3] + 1.2, .6) + .03 * pulse(t, C.savings + .9, .5) + .02 * pulse(t, CU[5] + .6, .4);
  grade.uniforms.uCA.value = .0012 + .0035 * bars + .006 * pulse(t, C.blocked, .12) + .006 * pulse(t, C.moves + .1, .15);
  grade.uniforms.uTime.value = t;

  // camera
  let fov = camAt(t);
  let fb = 0; for (const f of FOC) fb = Math.max(fb, bump(t, f.a, f.b, .3));
  camera.position.copy(CAMP);
  const hand = .03 * bars * Math.min(1, CAMP.distanceTo(CAML) / 3);
  camera.position.x += Math.sin(t * .37) * .03 + (Math.sin(t * 3.1) + Math.sin(t * 7.3 + 1) * .5) * hand;
  camera.position.y += Math.sin(t * .29 + 1) * .02 + (Math.sin(t * 2.7 + 2) + Math.sin(t * 6.1) * .5) * hand;
  camera.fov = fov;
  grade.uniforms.uVig.value = .28 + .45 * fb + (night ? .2 : 0);
  faceKey.position.copy(camera.position).add(V.set(.3, .4, 0));
  faceKey.intensity = fb * (night ? 1.6 : 1.0);
  const look = CAML.clone();
  const cv = window.BANK_COVER;
  if (cv) { camera.position.set(...cv.cam); camera.fov = cv.fov; look.set(...cv.look); for (const u of ["uBars", "uBlur", "uScan", "uFlash"]) grade.uniforms[u].value = 0; grade.uniforms.uCA.value = .001; }
  camera.updateProjectionMatrix();
  camera.lookAt(look);
  const cd = camera.position.distanceTo(look), ext = clamp(cd * .8, 6, 70);
  sun.target.position.copy(look); sun.position.copy(look).add(V.set(...Lk.sp).normalize().multiplyScalar(40));
  Object.assign(sun.shadow.camera, { left: -ext, right: ext, top: ext, bottom: -ext, near: 1, far: 120 });
  sun.shadow.camera.updateProjectionMatrix();
  scene.fog.near = cd * 2 + 30; scene.fog.far = cd * 5 + 120;
  composer.render();
}

// ---------------------------------------------------------------- textures (after fonts), then the first frame
function buildTextures() {
  const F = (w, f) => `${w} ${f}px Manrope, sans-serif`, MONO = (f) => `700 ${f}px JBMono, monospace`;
  const SUBS = [["STREAMFLIX", "$15.99/mo", "#D9483B", "▶"], ["GYMPASS", "$39.00/mo", "#3FA372", "◆"], ["TUNES+", "$10.99/mo", "#7E5BB0", "♪"], ["CLOUDBOX", "$3.98/mo", "#3A7BD5", "☁"]];
  SUBS.forEach(([n, p, c, icon], k) => { TEX["sub" + k] = canvasTex(512, 320, (g, w, h) => { g.fillStyle = "#FFFDF8"; g.fillRect(0, 0, w, h); g.fillStyle = c; rr(g, 26, 26, 110, 110, 26); g.fill(); g.fillStyle = "#fff"; g.font = F(800, 64); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(icon, 81, 84); g.textAlign = "left"; g.fillStyle = "#1E1B18"; g.font = F(800, 52); g.fillText(n, 160, 70); g.font = MONO(40); g.fillStyle = "#5b5650"; g.fillText(p, 160, 128); g.font = MONO(30); g.fillStyle = "#A8452F"; g.fillText("LAST USED: " + ["8 MONTHS", "1 YEAR", "5 MONTHS", "2 YEARS"][k] + " AGO", 30, 230); }); });
  TEX.stamp = canvasTex(512, 160, (g, w, h) => { g.strokeStyle = "#D9483B"; g.lineWidth = 14; rr(g, 10, 10, w - 20, h - 20, 22); g.stroke(); g.fillStyle = "#D9483B"; g.font = F(800, 84); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("CANCELLED", w / 2, h / 2 + 4); });
  const bub = ["Loyal customer, 6 years.", "Best I can do: $79.", "Competitor offers $49.", "...fine. $53.40."];
  bub.forEach((txt, k) => { TEX["bub" + k] = canvasTex(1024, 300, (g, w, h) => { g.fillStyle = "rgba(0,0,0,0)"; g.clearRect(0, 0, w, h); g.fillStyle = k % 2 ? "#1E3A6E" : "#7A2E1E"; g.font = F(800, 92); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(txt, w / 2, h / 2 + 4); }); });
  const bill = (amt, after) => canvasTex(600, 840, (g, w, h) => { g.fillStyle = "#FFFDF8"; g.fillRect(0, 0, w, h); g.fillStyle = "#3A7BD5"; g.fillRect(0, 0, w, 110); g.fillStyle = "#fff"; g.font = F(800, 52); g.fillText("LINKTEL", 36, 74); g.fillStyle = "#1E1B18"; g.font = MONO(34); g.fillText("MONTHLY BILL", 36, 190); for (let k = 0; k < 6; k++) { g.fillStyle = "#E4D9C7"; g.fillRect(36, 240 + k * 52, w - 72, 22); } g.font = F(800, 120); g.fillStyle = after ? "#3FA372" : "#1E1B18"; g.fillText(amt, 36, 680); if (after) { g.save(); g.translate(400, 520); g.rotate(-.3); g.strokeStyle = "#3FA372"; g.lineWidth = 12; rr(g, -150, -60, 300, 120, 18); g.stroke(); g.fillStyle = "#3FA372"; g.font = F(800, 86); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("−40%", 0, 6); g.restore(); } });
  TEX.billA = bill("$89.00", false); TEX.billB = bill("$53.40", true);
  const botFace = (mode) => canvasTex(480, 300, (g, w, h) => { g.fillStyle = "#0E1A2E"; rr(g, 0, 0, w, h, 50); g.fill(); g.strokeStyle = "#7FD8FF"; g.fillStyle = "#7FD8FF"; g.lineWidth = 22; g.lineCap = "round";
    if (mode === 0) { g.beginPath(); g.arc(150, 140, 40, 0, Math.PI * 2); g.fill(); g.beginPath(); g.arc(330, 140, 40, 0, Math.PI * 2); g.fill(); g.beginPath(); g.moveTo(190, 230); g.lineTo(290, 230); g.stroke(); }
    if (mode === 1) { g.beginPath(); g.moveTo(100, 100); g.lineTo(200, 140); g.moveTo(380, 100); g.lineTo(280, 140); g.stroke(); g.beginPath(); g.arc(150, 170, 26, 0, Math.PI * 2); g.fill(); g.beginPath(); g.arc(330, 170, 26, 0, Math.PI * 2); g.fill(); g.beginPath(); g.moveTo(180, 240); g.lineTo(300, 240); g.stroke(); }
    if (mode === 2) { g.beginPath(); g.moveTo(110, 150); g.lineTo(190, 150); g.moveTo(290, 150); g.lineTo(370, 150); g.stroke(); g.beginPath(); g.arc(240, 250, 50, Math.PI * 1.1, Math.PI * 1.9); g.stroke(); g.fillStyle = "#9fd8ff"; g.beginPath(); g.arc(395, 90, 16, 0, Math.PI * 2); g.fill(); } });
  TEX.botA = botFace(0); TEX.botB = botFace(1); TEX.botC = botFace(2);
  TEX.sign = canvasTex(800, 200, (g, w, h) => { g.fillStyle = "#1E3A6E"; rr(g, 0, 0, w, h, 30); g.fill(); g.fillStyle = "#fff"; g.font = F(800, 120); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("LINKTEL", w / 2, h / 2 + 8); });
  TEX.buy = canvasTex(512, 170, (g, w, h) => { g.fillStyle = "#1E1B18"; rr(g, 0, 0, w, h, 40); g.fill(); g.fillStyle = "#7FE6FF"; g.font = F(800, 74); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("BUY · $189", w / 2, h / 2 + 4); });
  TEX.card = canvasTex(600, 380, (g, w, h) => { const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, "#2A2623"); gr.addColorStop(1, "#4A3E36"); g.fillStyle = gr; g.fillRect(0, 0, w, h); g.fillStyle = "#F2B33D"; rr(g, 50, 120, 90, 70, 12); g.fill(); g.fillStyle = "#E8735A"; g.beginPath(); g.arc(500, 80, 34, 0, Math.PI * 2); g.fill(); g.fillStyle = "#FFFDF8"; g.font = MONO(50); g.fillText("•••• 4821", 50, 290); g.font = MONO(28); g.fillText("YOU", 50, 340); });
  TEX.clock = canvasTex(300, 140, (g, w, h) => { g.fillStyle = "#120c0a"; g.fillRect(0, 0, w, h); g.fillStyle = "#FF5A3A"; g.font = MONO(96); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("2:04", w / 2, h / 2 + 4); });
  TEX.clock2 = canvasTex(300, 140, (g, w, h) => { g.fillStyle = "#120c0a"; g.fillRect(0, 0, w, h); g.fillStyle = "#FF5A3A"; g.font = MONO(96); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("3:12", w / 2, h / 2 + 4); });
  TEX.neon = canvasTex(760, 220, (g, w, h) => { g.clearRect(0, 0, w, h); g.shadowColor = "#ff4fa3"; g.shadowBlur = 30; g.fillStyle = "#ffd0ec"; g.font = F(800, 110); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("CAMBIO 24H", w / 2, h / 2 + 6); });
  const atm = (title, sub, c) => canvasTex(500, 360, (g, w, h) => { g.fillStyle = "#0B1A14"; g.fillRect(0, 0, w, h); g.fillStyle = c; g.font = F(800, 64); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(title, w / 2, 150); g.font = MONO(30); g.fillText(sub, w / 2, 240); });
  TEX.atm0 = atm("WELCOME", "INSERT CARD", "#7FFFB0"); TEX.atm1 = atm("PROCESSING", "PLEASE WAIT ...", "#7FFFB0"); TEX.atm2 = atm("DECLINED", "CARD BLOCKED", "#FF5A4A");
  TEX.swirl = canvasTex(512, 512, (g, w, h) => { const gr = g.createRadialGradient(w / 2, h / 2, 10, w / 2, h / 2, w / 2); gr.addColorStop(0, "#FFFDF8"); gr.addColorStop(.35, "#F2B33D"); gr.addColorStop(.75, "#E8735A"); gr.addColorStop(1, "rgba(232,115,90,0)"); g.fillStyle = gr; g.fillRect(0, 0, w, h); g.strokeStyle = "rgba(255,253,248,.7)"; g.lineWidth = 10; for (let k = 0; k < 5; k++) { g.beginPath(); for (let a = 0; a < 6; a += .05) { const r = a * 36; g.lineTo(w / 2 + Math.cos(a + k * 1.25) * r, h / 2 + Math.sin(a + k * 1.25) * r); } g.stroke(); } });
  const app = (title, line, c) => canvasTex(160, 330, (g, w, h) => { g.fillStyle = "#FFFDF8"; g.fillRect(0, 0, w, h); g.fillStyle = c; g.fillRect(0, 0, w, 70); g.fillStyle = "#fff"; g.font = F(800, 22); g.fillText("YOUR BANK", 14, 44); g.fillStyle = "#1E1B18"; g.font = F(800, 26); g.fillText(title, 14, 130); g.font = F(600, 18); g.fillStyle = "#5b5650"; g.fillText(line, 14, 170); for (let k = 0; k < 4; k++) { g.fillStyle = "#E4D9C7"; g.fillRect(14, 200 + k * 28, w - 28, 14); } });
  TEX.app0 = app("$48,210", "savings", "#E8735A"); TEX.app1 = app("$189.00", "sneakers · cart", "#3A7BD5"); TEX.app1b = app("FROZEN", "card paused", "#3A7BD5");
  TEX.app2 = app("$48,210", "savings", "#E8735A"); TEX.app3 = app("$0.00", "transfer done", "#D9483B");
  TEX.phoneTxt = TEX.buy;
  for (const [m, key] of LATE) { m.map = TEX[key]; m.needsUpdate = true; }
}

const ready = (async () => {
  try { await Promise.all([document.fonts.load("800 40px Manrope"), document.fonts.load("700 30px JBMono")]); } catch (e) { /* fall back */ }
  buildTextures();
  scene.traverse((o) => { if (o.isInstancedMesh) o.frustumCulled = false; if (o.isMesh && o.matrixAutoUpdate === false) o.frustumCulled = false; });
  renderer.compile(scene, camera);
  renderAt(window.BANK_COVER ? window.BANK_COVER.t : (window.__hfThreeTime || 0));
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["bank"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(window.BANK_COVER ? window.BANK_COVER.t : e.detail.time));
window.BANK_DEBUG = { HEADW };
