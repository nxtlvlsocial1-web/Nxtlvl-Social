// AI Closer reel: the 3D world, in the voxel style of the owner's reference (the same creator street as the AI clone
// reel). THE CLOSER is a small floating voxel robot with a pixel screen face that sells in your DMs while you sleep.
// Characters are blocky figures with pixel-art faces drawn on canvas (NearestFilter) and real joints; the student in the
// AI's story is a small cyan hologram. Everything is a pure function of time t (seconds), drawn on HyperFrames' hf-seek;
// cue times come from the voice (window.CT, written by build/generate.py). Post: depth of field from the depth buffer,
// bloom, then the house grade (letterbox, AI scan grid, flashes). The month:
//   3 AM      night; you asleep in the studio; the phone on the desk buzzes, seven sales float up, orders pour in
//   day 1     the fan comments PRICE on her bench; the robot flies over from the studio and DMs her the link
//   day 4     a buyer at the cafe says it's too expensive; the robot projects a student's story on the table; paid
//   day 10    the crowd that clicked and didn't buy; a day passes; follow-ups fly; half come back
//   day 18    midnight on the bench; a stranger is ready to pay $497; the robot gently says no
//   day 30    golden hour; the billboard reads 212; she walks back up the plaza with four friends
//   real      the street rises into a whole city of DMs
//   close     you and the robot wave in front of the studio
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
const hemi = new THREE.HemisphereLight(0xEAF4FF, 0xD6C9B0, 1.0);
scene.add(hemi);
const sun = new THREE.DirectionalLight(0xFFF2DC, 2.2);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.bias = -.0004;
sun.shadow.normalBias = .03;
scene.add(sun, sun.target);
const plight = (c, d = 8, decay = 1.5) => { const l = new THREE.PointLight(c, 0, d, decay); scene.add(l); return l; };
const ceilL = plight(0xFFD9B0, 9), deskL = plight(0xFFC98A, 5), wallL = plight(0xBFEFFF, 6), cloneL = plight(0x6FE0FF, 5);
const pendL = plight(0xFFD29A, 7), lapL = plight(0xCFE3FF, 2.4), streetA = plight(0xFFD9A0, 12), streetB = plight(0xFFD9A0, 12), faceKey = plight(0xFFF0E0, 5, 1.2);
const phoneL = plight(0xBFE6FF, 1.6, 1.4);
ceilL.position.set(.5, 3.0, -2.4); deskL.position.set(1.0, 1.25, -2.6); wallL.position.set(.3, 2.0, -3.6);
pendL.position.set(-12, 2.35, -2.8); streetA.position.set(.5, 4.2, 3.5); streetB.position.set(-12, 4.2, 3.5);

// ---------------------------------------------------------------- materials, textures
const mat = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: .85, metalness: 0, ...o });
const gloss = (c, o = {}) => new THREE.MeshPhysicalMaterial({ color: c, roughness: .35, clearcoat: .6, clearcoatRoughness: .2, envMap: ENV, envMapIntensity: .35, ...o });
const metal = (c, r = .3) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: .85, envMap: ENV, envMapIntensity: 1 });
const glow = (c) => new THREE.MeshBasicMaterial({ color: c, toneMapped: false });
const goldM = new THREE.MeshStandardMaterial({ color: GOLD, roughness: .25, metalness: .9, envMap: ENV, envMapIntensity: 1.3, emissive: 0x4a2a00, emissiveIntensity: .3 });
const ROOT3 = new THREE.Group(); scene.add(ROOT3);
const add = (m, cast = true, recv = true, parent = ROOT3) => { m.castShadow = cast; m.receiveShadow = recv; parent.add(m); return m; };
const box = (w, h, d, c, x, y, z, o = {}) => { const m = add(new THREE.Mesh(o.round ? new RoundedBoxGeometry(w, h, d, 2, Math.min(o.round, w / 2, h / 2, d / 2)) : new THREE.BoxGeometry(w, h, d), Array.isArray(c) || c.isMaterial ? c : mat(c)), o.cast ?? true, true, o.parent); m.position.set(x, y, z); return m; };
const cyl = (r1, r2, h, c, x, y, z, seg = 20, parent) => { const m = add(new THREE.Mesh(new THREE.CylinderGeometry(r1, r2, h, seg), c.isMaterial ? c : mat(c)), true, true, parent); m.position.set(x, y, z); return m; };
const plane = (w, h, m, x, y, z, ry = 0, parent) => { const p = add(new THREE.Mesh(new THREE.PlaneGeometry(w, h), m), false, false, parent); p.position.set(x, y, z); p.rotation.y = ry; return p; };
function pix(w, h, draw, nearest = true) {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  const g = c.getContext("2d"); g.imageSmoothingEnabled = false; draw(g, w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
  if (nearest) t.magFilter = THREE.NearestFilter;
  return t;
}
const px = (g, c, x, y, w = 1, h = 1) => { g.fillStyle = c; g.fillRect(x, y, w, h); };
const rr = (g, x, y, w, h, r) => { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); };
const TEX = {};
const LATE = [];
const texMat = (key, o = {}) => { const m = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, toneMapped: false, ...o }); LATE.push([m, key]); return m; };
const setMap = (m, tx) => { if (m.map !== tx) { m.map = tx || null; m.needsUpdate = true; } };
const NIGHTM = [];   // facade materials whose window mask glows at night
const LAMPM = glow(0xFFE7B0);

// ---------------------------------------------------------------- ground: checker plaza, road, sidewalk
const checker = pix(64, 64, (g) => { for (let i = 0; i < 8; i++) for (let j = 0; j < 8; j++) px(g, (i + j) % 2 ? "#EFE5D3" : "#E3D6C0", i * 8, j * 8, 8, 8); });
checker.wrapS = checker.wrapT = THREE.RepeatWrapping; checker.repeat.set(600 / 12, 600 / 12);
const ground = add(new THREE.Mesh(new THREE.PlaneGeometry(600, 600), new THREE.MeshStandardMaterial({ map: checker, roughness: .9 })), false, true);
ground.rotation.x = -Math.PI / 2; ground.position.set(0, 0, 0);
const swTex = pix(64, 32, (g) => { px(g, "#D8D3CB", 0, 0, 64, 32); for (let i = 0; i < 4; i++) px(g, "#C9C3B9", i * 16, 0, 1, 32); px(g, "#C9C3B9", 0, 16, 64, 1); });
swTex.wrapS = swTex.wrapT = THREE.RepeatWrapping; swTex.repeat.set(140 / 4, 1);
box(140, .12, 2, new THREE.MeshStandardMaterial({ map: swTex, roughness: .9 }), 0, .06, 1, { cast: false });
box(140, .16, .16, mat(0xBDB6AA), 0, .08, 2.0, { cast: false });
box(140, .02, 4.5, mat(0x98A2B3, { roughness: .95 }), 0, .01, 4.25, { cast: false });
box(140, .16, .16, mat(0xBDB6AA), 0, .08, 6.5, { cast: false });
const dashM = new THREE.InstancedMesh(new THREE.BoxGeometry(1.0, .02, .14), mat(0xF4F1EA), 70);
for (let k = 0; k < 70; k++) { M4.makeTranslation(-70 + k * 2 + .5, .025, 4.25); dashM.setMatrixAt(k, M4); }
add(dashM, false, true);

// ---------------------------------------------------------------- shop facades
const S48 = 48;
function facadeTex(o) {
  const cw = Math.round(o.w * S48), ch = Math.round(o.h * S48), Y = (u) => ch - u * S48;
  const draw = (g, lit) => {
    if (!lit) {
      px(g, o.wall, 0, 0, cw, ch);
      for (let y = 0; y < ch; y += 12) for (let x = ((y / 12) % 2) * 12 - 12; x < cw; x += 24) { g.fillStyle = hash(x * .13 + y * .71) > .5 ? "rgba(255,255,255,.07)" : "rgba(0,0,0,.035)"; g.fillRect(x, y, 24, 12); }
      px(g, shc(o.wall, -.2), 0, Y(.35), cw, .35 * S48);
      px(g, shc(o.wall, .35), 0, 0, cw, 8);
    } else px(g, "#000", 0, 0, cw, ch);
    for (const wx of o.win || []) {
      const x = wx * S48, y = Y(2.3), w = 1.9 * S48, h = 1.5 * S48;
      if (lit) { px(g, "#FFD9A0", x + 6, y + 6, w - 12, h - 12); continue; }
      px(g, "#FFFDF8", x, y, w, h); px(g, "#A9CBE6", x + 6, y + 6, w - 12, h - 12); px(g, "#C9E0F2", x + 6, y + 6, w - 12, 14);
      const k = o.kind;
      for (let i = 0; i < 4; i++) {
        const cx = x + 14 + i * ((w - 28) / 4), by = y + h - 10;
        if (k === "cakes") { px(g, "#FFFDF8", cx, by - 14, 16, 14); px(g, ["#F29BB8", "#C98A5A", "#F7E3A6", "#E8735A"][i], cx, by - 20, 16, 7); px(g, "#D9483B", cx + 6, by - 24, 4, 4); }
        if (k === "cafe") { px(g, "#FFFDF8", cx, by - 12, 12, 12); px(g, "#6B4A32", cx + 2, by - 10, 8, 3); px(g, "#FFFDF8", cx + 12, by - 9, 3, 5); }
        if (k === "books") for (let b = 0; b < 4; b++) px(g, ["#D9483B", "#3A6FC4", "#3FA372", "#F2B33D"][(b + i) % 4], cx + b * 4, by - 18 - (b % 2) * 3, 4, 18 + (b % 2) * 3);
        if (k === "gym") { px(g, "#1E1B18", cx, by - 12, 4, 12); px(g, "#1E1B18", cx + 12, by - 12, 4, 12); px(g, "#5B5650", cx + 4, by - 7, 8, 3); }
        if (k === "flowers") { px(g, "#C9644E", cx + 2, by - 8, 10, 8); px(g, ["#D9483B", "#F2B33D", "#E36FA6", "#7E5BB0"][i], cx, by - 18, 14, 10); px(g, "#6E9A5C", cx + 5, by - 10, 4, 4); }
        if (k === "arcade") { px(g, "#1E1B18", cx, by - 26, 16, 26); px(g, ["#7FE6FF", "#E36FA6", "#F2B33D", "#3FA372"][i], cx + 3, by - 22, 10, 8); }
        if (k === "home") { if (i === 1) { px(g, "#F7E3A6", cx, by - 24, 30, 24); px(g, "#E8735A", cx + 4, by - 18, 8, 8); } }
      }
      px(g, "#FFFDF8", x + w / 2 - 3, y, 6, h);
    }
    if (o.door != null) {
      const x = o.door * S48, y = Y(2.2), w = 1.0 * S48, h = 2.2 * S48;
      if (lit) px(g, "#FFD9A0", x + 12, y + 10, w - 24, 30);
      else { px(g, shc(o.wall, .4), x - 5, y - 5, w + 10, h + 5); px(g, o.doorC || "#2E3A66", x, y, w, h); px(g, "#A9CBE6", x + 12, y + 10, w - 24, 30); px(g, "#F2B33D", x + w - 12, y + h / 2, 5, 5); }
    }
    for (let f = 0; f < (o.floors || 0); f++) {
      const y0 = Y(o.base + 1.6 + f * 1.9);
      for (let x0 = .5; x0 + .9 < o.w; x0 += 1.5) {
        const x = x0 * S48, w = .9 * S48, h = 1.1 * S48;
        if (lit) { if (hash(x0 * 3.1 + f * 7.7 + o.w) > .35) px(g, hash(x0 + f) > .5 ? "#FFD9A0" : "#FFE8C4", x + 4, y0 + 4, w - 8, h - 8); continue; }
        px(g, "#FFFDF8", x, y0, w, h); px(g, "#9FC2E0", x + 4, y0 + 4, w - 8, h - 8); px(g, "#C3DAEE", x + 4, y0 + 4, w - 8, 8);
      }
    }
  };
  return [pix(cw, ch, (g) => draw(g, false), false), pix(cw, ch, (g) => draw(g, true), false)];
}
function facadeMat(o) {
  const [t, e] = facadeTex(o);
  const m = new THREE.MeshStandardMaterial({ map: t, emissiveMap: e, emissive: 0xFFD9A0, emissiveIntensity: 0, roughness: .85 });
  NIGHTM.push(m); return m;
}
const signs = [];
function sign(text, bg, x, y, z, w) {
  const m = texMat("sign:" + text + ":" + bg, { transparent: false });
  const s = box(w, .62, .12, [mat(bg), mat(bg), mat(bg), mat(bg), m, mat(bg)], x, y, z);
  signs.push([text, bg]); return s;
}
function awning(x, w, c1, c2, y = 2.5) {
  const tx = pix(16, 4, (g) => { for (let i = 0; i < 8; i++) px(g, i % 2 ? c1 : c2, i * 2, 0, 2, 4); });
  tx.wrapS = THREE.RepeatWrapping; tx.repeat.set(w / 1.6, 1);
  const a = box(w, .08, 1.0, new THREE.MeshStandardMaterial({ map: tx, roughness: .9 }), x, y, .5); a.rotation.x = .38;
  for (let k = 0; k < Math.round(w / .5); k++) box(.25, .12, .04, k % 2 ? c1 : c2, x - w / 2 + .25 + k * .5, y - .22, 1.0, { cast: false });
}
function shop(x0, x1, h, wall, o = {}) {
  const w = x1 - x0, cx = (x0 + x1) / 2, d = o.d ?? 6;
  const wm = mat(wall), fm = facadeMat({ w, h, wall, ...o });
  box(w, h, d, [wm, wm, mat(shc(wall, .3)), wm, fm, wm], cx, h / 2, -d / 2);
  box(w + .14, .26, .34, mat(shc(wall, .45)), cx, h + .13, -.12);
  box(.7, .45, .7, mat(0xC9C3B9), cx + w * .25, h + .22, -d * .6);
  if (o.sign) sign(o.sign, o.signBg, cx, 2.75, .07, Math.min(w * .55, 3.2));
  if (o.awn) awning(o.win ? x0 + o.win[0] + .95 : cx, 2.3, o.awn[0], o.awn[1]);
}
shop(-30, -22, 5.0, "#F4C9C9", { sign: "FLORIST", signBg: "#D9607A", kind: "flowers", door: 1.2, win: [3.0, 5.5], floors: 1, base: 2.4 });
shop(-22, -16, 4.4, "#F6E3A6", { sign: "BOOKS", signBg: "#C9932E", kind: "books", door: .8, win: [2.8] });
shop(-8, -3, 4.2, "#BFE3D3", { sign: "CAFE", signBg: "#2F8F7A", kind: "cafe", door: .6, win: [2.4], awn: ["#2F8F7A", "#FFFDF8"] });
shop(4, 9, 4.6, "#D9CCF0", { kind: "home", door: 1.0, win: [2.6], doorC: "#E8735A" });
shop(9, 14, 4.2, "#F7CFDD", { sign: "BAKERY", signBg: "#D9607A", kind: "cakes", door: .5, win: [2.2], awn: ["#D9607A", "#FFFDF8"] });
shop(14, 20, 4.8, "#BFD3EE", { sign: "GYM", signBg: "#3A6FC4", kind: "gym", door: .6, win: [2.6] });
shop(20, 28, 5.2, "#F4D9BF", { sign: "ARCADE", signBg: "#7E5BB0", kind: "arcade", door: 1.0, win: [3.0, 5.5], floors: 1, base: 2.4 });
shop(-40, -30, 6.0, "#CFE0EE", { door: 1.0, win: [3.2, 6.0], floors: 1, base: 2.5 });
shop(28, 38, 6.2, "#E6E0F2", { door: 1.0, win: [3.2, 6.0], floors: 1, base: 2.5 });
// flower box under the fan's window
box(2.0, .3, .3, mat(0xC9644E), 4 + 2.6 + .95, .75, .15);
for (let k = 0; k < 6; k++) box(.24, .22, .22, mat([0xD9483B, 0xF2B33D, 0xE36FA6][k % 3]), 4 + 2.6 + .1 + k * .34, 1.0, .15, { cast: false });
// the back row, taller, behind the shops
for (let k = 0; k < 9; k++) {
  const x0 = -42 + k * 9.6, w = 8.6, h = 9 + hash(k * 3.3) * 6, wall = ["#DCE7F2", "#F2ECE2", "#E2EEE6", "#EFE2EA"][k % 4];
  const fm = facadeMat({ w, h, wall, floors: Math.floor((h - 1.4) / 1.9), base: -.2 });
  box(w, h, 6, [mat(wall), mat(wall), mat(shc(wall, .3)), mat(wall), fm, mat(wall)], x0 + w / 2, h / 2, -14);
}

// ---------------------------------------------------------------- your studio (x -3..4, open front, z -4.8..0)
const SX0 = -3, SX1 = 4, SZ0 = -4.8, SIH = 3.4;
const stWall = mat(0xF6E4D6), trimM = mat(CORAL);
box(.25, 4.6, 4.8, stWall, SX0 + .125, 2.3, -2.4);
box(.25, 4.6, 4.8, stWall, SX1 - .125, 2.3, -2.4);
box(7, 4.6, .25, mat(0xF1DCCB), .5, 2.3, SZ0 + .125);
box(7, .25, 4.8, mat(0xEADCCB), .5, SIH + .125, -2.4, { cast: false });
box(7, .1, 4.8, mat(0xE2D3C2), .5, 4.65, -2.4);
const headerM = facadeMat({ w: 7, h: 1.2, wall: "#F7D9C4" });
box(7, 1.2, .3, [stWall, stWall, stWall, stWall, headerM, stWall], .5, 4.0, -.15);
box(7.2, .26, .4, mat(0xFBE9DB), .5, 4.73, -.2);
for (const x of [SX0 + .15, SX1 - .15]) box(.3, 3.4, .32, trimM, x, 1.7, -.15);
box(7, .14, .32, trimM, .5, 3.35, -.15);
sign("STUDIO", "#E8735A", .5, 4.0, .07, 3.0);
const plankTex = pix(64, 64, (g) => { for (let k = 0; k < 8; k++) { px(g, k % 2 ? "#C9A27A" : "#C29A72", 0, k * 8, 64, 8); px(g, "#A9825C", (k * 23) % 64, k * 8, 1, 8); px(g, "#B08A64", 0, k * 8 + 7, 64, 1); } });
plankTex.wrapS = plankTex.wrapT = THREE.RepeatWrapping; plankTex.repeat.set(3.4, 2.4);
box(6.5, .04, 4.55, new THREE.MeshStandardMaterial({ map: plankTex, roughness: .7 }), .5, .02, -2.4, { cast: false });
box(6.5, 1.0, .03, mat(0xE9B9A2), .5, .5, SZ0 + .26, { cast: false });
box(6.4, .05, .05, glow(0xFF9A7A), .5, 3.22, SZ0 + .3, { cast: false });
const rugTex = pix(32, 24, (g) => { px(g, "#E8735A", 0, 0, 32, 24); px(g, "#F7D9C4", 2, 2, 28, 20); px(g, "#E8735A", 4, 4, 24, 16); for (let k = 0; k < 6; k++) px(g, "#F2B33D", 6 + k * 4, 8, 2, 8); });
box(2.8, .015, 1.9, new THREE.MeshStandardMaterial({ map: rugTex, roughness: .95 }), .3, .045, -2.9, { cast: false });
// the DM wall: a big screen of inbox rows that scrolls
box(3.45, 1.85, .08, mat(INK, { roughness: .4 }), .3, 2.2, SZ0 + .3);
const inboxM = texMat("inbox", { transparent: false });
const inboxScr = plane(3.3, 1.7, inboxM, .3, 2.2, SZ0 + .345);
// desk, laptop, monitor, lamp, mug, plant
const woodM = mat(0xB98E62);
box(1.9, .07, .75, woodM, .3, .735, -2.62);
for (const sx of [-.9, .9]) box(.06, .7, .7, mat(INK), .3 + sx, .35, -2.62);
box(1.8, .42, .03, mat(0xA67C55), .3, .45, -2.27);
box(.44, .025, .3, metal(0xB9BCC2, .4), .3, .785, -2.72);
const lapG = new THREE.Group(); lapG.position.set(.3, .797, -2.58); lapG.rotation.x = -.18; ROOT3.add(lapG);
box(.44, .3, .02, mat(0x8E929A, { roughness: .55 }), 0, .15, 0, { parent: lapG });
const lapScrM = texMat("lapStudio", { transparent: false });
plane(.4, .26, lapScrM, 0, .15, -.012, Math.PI, lapG);
box(.06, .06, .01, glow(0xFFFDF8), 0, .15, .012, { parent: lapG, cast: false });
box(.62, .38, .04, mat(INK, { roughness: .4 }), -.55, 1.12, -2.78);
plane(.58, .34, texMat("monitor", { transparent: false }), -.55, 1.12, -2.80, Math.PI);
box(.06, .3, .06, mat(INK), -.55, .87, -2.74); box(.24, .02, .18, mat(INK), -.55, .78, -2.74);
cyl(.07, .09, .03, mat(INK), 1.05, .785, -2.85, 14); box(.03, .4, .03, mat(INK), 1.05, .98, -2.85).rotation.z = .3;
const dlamp = add(new THREE.Mesh(new THREE.ConeGeometry(.1, .14, 14, 1, true), new THREE.MeshStandardMaterial({ color: CORAL, emissive: 0xFFB070, emissiveIntensity: 0, side: THREE.DoubleSide })));
dlamp.position.set(.97, 1.18, -2.78); dlamp.rotation.z = -.6;
cyl(.05, .045, .1, mat(CREAM), -.05, .82, -2.45, 12);
box(.16, .14, .16, mat(0xC9644E), 1.0, .84, -2.4); for (let k = 0; k < 4; k++) box(.1, .12, .1, mat(0x6E9A5C), .95 + (k % 2) * .1, .96 + k * .05, -2.42 + (k > 1 ? .06 : -.04), { cast: false });
// the chair
box(.56, .09, .56, mat(INK, { roughness: .5 }), .3, .395, -3.32);
const chairBack = box(.56, .95, .09, gloss(CORAL, { roughness: .6 }), .3, .98, -3.68, { round: .03 });
chairBack.rotation.x = -.12;
box(.4, .22, .1, gloss(CORAL, { roughness: .6 }), .3, 1.58, -3.75, { round: .03 });
cyl(.04, .04, .32, mat(INK), .3, .2, -3.32, 8);
for (let k = 0; k < 5; k++) { const a = k * Math.PI * 2 / 5; const l = box(.32, .04, .05, mat(INK), .3 + Math.cos(a) * .16, .04, -3.32 + Math.sin(a) * .16); l.rotation.y = -a; }
for (const sx of [-.3, .3]) box(.06, .05, .4, mat(INK), .3 + sx, .64, -3.3);
// ring light, camera on a tripod, beanbag, shelves, neon, plant, posters, window
cyl(.02, .02, 1.7, mat(INK), -2.0, .85, -2.3, 8);
const ring = add(new THREE.Mesh(new THREE.TorusGeometry(.3, .035, 10, 40), new THREE.MeshStandardMaterial({ color: 0xFFFDF8, emissive: 0xFFF4E6, emissiveIntensity: .6 })));
ring.position.set(-2.0, 1.75, -2.3); ring.rotation.y = .9;
const tri = new THREE.Group(); tri.position.set(-1.6, 0, -1.0); tri.rotation.y = 2.4; ROOT3.add(tri);
for (let k = 0; k < 3; k++) { const l = box(.03, 1.2, .03, mat(INK), Math.cos(k * 2.1) * .18, .58, Math.sin(k * 2.1) * .18, { parent: tri }); l.rotation.set(Math.sin(k * 2.1) * .3, 0, -Math.cos(k * 2.1) * .3); }
box(.28, .2, .16, mat(INK, { roughness: .4 }), 0, 1.25, 0, { parent: tri });
const lens = cyl(.07, .07, .14, mat(0x3A3A40), 0, 1.25, .14, 16, tri); lens.rotation.x = Math.PI / 2;
const bean = add(new THREE.Mesh(new THREE.SphereGeometry(.55, 20, 14), mat(0x3A6FC4, { roughness: .9 }))); bean.scale.set(1, .62, 1); bean.position.set(3.0, .32, -1.4);
for (const y of [1.55, 2.15]) box(.3, .04, 1.5, woodM, 3.6, y, -2.1);
for (let k = 0; k < 5; k++) box(.18, .26 + (k % 2) * .06, .12, mat([0xD9483B, 0x3A6FC4, 0x3FA372, 0xF2B33D, 0x7E5BB0][k]), 3.62, 1.7 + (k % 2) * .03, -2.65 + k * .14);
box(.05, .36, .3, goldM, 3.6, 2.35, -2.3); box(.05, .36, .3, metal(0xD8DCE2, .25), 3.6, 2.35, -1.7);
const neonM = texMat("neon"); plane(1.4, .5, neonM, SX0 + .27, 2.45, -2.6, Math.PI / 2);
for (const [x, c] of [[-1.95, 0xF2B33D], [2.6, 0x3FA372]]) { box(.8, 1.0, .04, mat(INK), x, 2.2, SZ0 + .27); box(.7, .9, .03, mat(c), x, 2.2, SZ0 + .3, { cast: false }); }
box(.4, .45, .4, mat(0xC9644E), 3.35, .23, -4.2);
for (let k = 0; k < 7; k++) box(.18, .5, .06, mat(0x6E9A5C), 3.35 + Math.cos(k) * .12, .7 + k * .1, -4.2 + Math.sin(k) * .12, { cast: false }).rotation.set(Math.cos(k * 1.7) * .6, k, Math.sin(k * 1.3) * .6);
const winSkyM = new THREE.MeshBasicMaterial({ color: 0xBFD9EC });
plane(1.3, 1.1, winSkyM, SX1 - .26, 2.0, -3.6, -Math.PI / 2);
box(.06, 1.22, .08, mat(CREAM), SX1 - .28, 2.0, -3.6); box(.06, .08, 1.42, mat(CREAM), SX1 - .28, 2.0, -3.6); box(.06, .08, 1.42, mat(CREAM), SX1 - .28, 2.57, -3.6); box(.06, .08, 1.42, mat(CREAM), SX1 - .28, 1.43, -3.6);
box(2.2, .04, .5, glow(0xFFF4E6), .5, 3.26, -2.4, { cast: false });
// the billboard on the studio roof
const billG = new THREE.Group(); ROOT3.add(billG);
for (const sx of [-1.6, 1.6]) box(.14, 1.6, .14, mat(INK), .5 + sx, 5.4, -2.0, { parent: billG });
box(4.5, 2.3, .22, mat(INK, { roughness: .4 }), .5, 6.9, -2.0, { parent: billG });
const billM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
plane(4.3, 2.1, billM, .5, 6.9, -1.885, 0, billG);
for (let k = 0; k < 6; k++) box(.1, .1, .1, LAMPM, -1.4 + k * .76, 8.1, -1.95, { cast: false, parent: billG });

// ---------------------------------------------------------------- the brand's office tower (x -16..-8)
const OX0 = -16, OX1 = -8, OZ0 = -5.6;
const offWall = mat(0xE9EEF4);
box(.25, 3.4, 5.6, offWall, OX0 + .125, 1.7, -2.8);
box(.25, 3.4, 5.6, offWall, OX1 - .125, 1.7, -2.8);
box(8, 3.4, .25, mat(0xDDE4EC), -12, 1.7, OZ0 + .125);
box(8, .25, 5.6, mat(0xD9E0E8), -12, 3.4 - .125, -2.8, { cast: false });
const towerM = facadeMat({ w: 8, h: 7.6, wall: "#AFC6DE", floors: 4, base: -1.0 });
box(8, 7.6, 6, [mat(0xAFC6DE), mat(0xAFC6DE), mat(0x9FB6CE), mat(0xAFC6DE), towerM, mat(0xAFC6DE)], -12, 3.4 + 3.8, -3);
box(8.2, .3, .4, mat(0xDDE8F2), -12, 11.15, -.2);
for (const x of [OX0 + .15, OX1 - .15]) box(.28, 3.4, .3, mat(0x23345E), x, 1.7, -.15);
box(8, .3, .32, mat(0x23345E), -12, 3.35, -.15);
sign("BRAND CO.", "#23345E", -12, 4.05, .07, 3.4);
const tileTex = pix(32, 32, (g) => { for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) px(g, (i + j) % 2 ? "#E9EBEE" : "#DDE1E6", i * 8, j * 8, 8, 8); });
tileTex.wrapS = tileTex.wrapT = THREE.RepeatWrapping; tileTex.repeat.set(4, 3);
box(7.5, .04, 5.3, new THREE.MeshStandardMaterial({ map: tileTex, roughness: .5, envMap: ENV, envMapIntensity: .25 }), -12, .02, -2.8, { cast: false });
const skyNightM = texMat("skyline", { transparent: false });
plane(4.2, 2.0, skyNightM, -13.2, 1.85, OZ0 + .27);
for (const x of [-15.3, -13.2, -11.1]) box(.08, 2.1, .08, mat(0x23345E), x, 1.85, OZ0 + .3);
box(4.3, .08, .08, mat(0x23345E), -13.2, 2.86, OZ0 + .3); box(4.3, .08, .08, mat(0x23345E), -13.2, .84, OZ0 + .3);
plane(1.6, .5, texMat("logo"), -9.5, 2.2, OZ0 + .27);
// the round table, the boss's chair, laptop, contract, pendant, projector pad
cyl(.5, .5, .05, gloss(0xF7F4EE), -12, .74, -2.8, 32); cyl(.05, .05, .7, mat(INK), -12, .37, -2.8, 10); cyl(.28, .3, .03, mat(INK), -12, .015, -2.8, 24);
box(.55, .09, .55, mat(INK, { roughness: .5 }), -12.85, .395, -2.8);
box(.09, .95, .55, gloss(0x23345E, { roughness: .6 }), -13.2, .98, -2.8, { round: .03 });
cyl(.04, .04, .32, mat(INK), -12.85, .2, -2.8, 8);
box(.3, .025, .42, metal(0x9CA0A8, .4), -12.27, .78, -2.8);
const lap2 = new THREE.Group(); lap2.position.set(-12.12, .792, -2.8); lap2.rotation.z = -.18; ROOT3.add(lap2);
box(.02, .3, .42, metal(0x9CA0A8, .4), 0, .15, 0, { parent: lap2 });
plane(.26, .4, texMat("lapOffice", { transparent: false }), -.012, .15, 0, -Math.PI / 2, lap2).rotation.set(0, -Math.PI / 2, Math.PI / 2);
const conM = texMat("con0", { transparent: false });
const contract = add(new THREE.Mesh(new THREE.PlaneGeometry(.26, .34), conM), false, true);
contract.rotation.set(-Math.PI / 2, 0, .25); contract.position.set(-11.88, .768, -2.62);
cyl(.006, .006, .9, mat(INK), -12, 2.95, -2.8, 4);
const pshade = add(new THREE.Mesh(new THREE.CylinderGeometry(.12, .3, .26, 20, 1, true), new THREE.MeshStandardMaterial({ color: 0x23345E, side: THREE.DoubleSide, emissive: 0xFFD29A, emissiveIntensity: 0 })));
pshade.position.set(-12, 2.45, -2.8);
const padM = new THREE.MeshBasicMaterial({ color: CYAN, transparent: true, opacity: 0, toneMapped: false, depthWrite: false });
const pad = add(new THREE.Mesh(new THREE.CircleGeometry(.45, 32), padM), false, false); pad.rotation.x = -Math.PI / 2; pad.position.set(-11.15, .03, -2.8);
box(.4, .45, .4, mat(0xF2F2F2), -15.4, .23, -1.0); for (let k = 0; k < 6; k++) box(.16, .5, .06, mat(0x5E8E58), -15.4 + Math.cos(k) * .1, .7 + k * .09, -1.0 + Math.sin(k) * .1, { cast: false }).rotation.set(Math.cos(k * 1.7) * .6, k, Math.sin(k * 1.3) * .6);
box(1.6, .5, .6, gloss(0xC9D3DE, { roughness: .8, clearcoat: 0 }), -9.3, .25, -4.7, { round: .08 }); box(1.6, .55, .18, gloss(0xC9D3DE, { roughness: .8, clearcoat: 0 }), -9.3, .6, -5.0, { round: .08 });

// ---------------------------------------------------------------- street furniture: bench, lamps, palms, planters, clouds
box(1.6, .08, .45, woodM, 6.5, .42, 1.3); for (const y of [.62, .8]) box(1.6, .12, .04, woodM, 6.5, y, 1.06);
for (const sx of [-.7, .7]) { box(.06, .4, .4, mat(INK), 6.5 + sx, .2, 1.3); box(.06, .45, .06, mat(INK), 6.5 + sx, .65, 1.06); }
function lamp(x, z) { box(.12, 3.6, .12, mat(0x2E3A55), x, 1.8, z); box(.6, .08, .1, mat(0x2E3A55), x + .25, 3.55, z); box(.28, .2, .28, LAMPM, x + .5, 3.42, z, { cast: false }); }
for (const x of [-25, -10.5, 4.3, 16.8, 30]) lamp(x, 1.7);
function palm(x, z, s = 1, lean = .12) {
  const g = new THREE.Group(); g.position.set(x, 0, z); g.scale.setScalar(s); ROOT3.add(g);
  for (let k = 0; k < 9; k++) box(.32, .42, .32, mat(k % 2 ? 0xA9825C : 0x94704C), Math.sin(k * .3) * lean * k * .6, .21 + k * .42, 0, { parent: g });
  const top = new THREE.Vector3(Math.sin(2.7) * lean * 5.4, 3.9, 0);
  for (let k = 0; k < 7; k++) {
    const a = k * Math.PI * 2 / 7, f = new THREE.Group(); f.position.copy(top); f.rotation.y = a; g.add(f);
    for (let j = 0; j < 4; j++) box(.42, .1, .3, mat(j % 2 ? 0x5E9A4C : 0x6FAE58), 0, -j * j * .05, .3 + j * .38, { parent: f });
  }
  box(.36, .3, .36, mat(0x6FAE58), top.x, top.y + .1, 0, { parent: g });
}
palm(-16.4, 1.3, 1, .1); palm(-3.4, 1.4, .95, -.08); palm(9.2, 1.4, 1.05, .12); palm(28.3, 1.3, 1, -.1); palm(-8.6, 9.5, 1.15, .1); palm(9.5, 10.5, 1.1, -.12);
function planter(x, z) { box(1.4, .5, 1.4, mat(0xE6DCC8), x, .25, z); for (let k = 0; k < 5; k++) box(.4, .4, .4, mat(k % 2 ? 0x6E9A5C : 0x7FAE68), x - .35 + (k % 3) * .35, .65 + (k > 2 ? .25 : 0), z - .2 + (k % 2) * .4); }
planter(-6.2, 9.0); planter(6.6, 8.6); planter(-14, 10.5); planter(15, 11);
box(.5, .8, .5, mat(0x3FA372), -2.6, .4, 2.3 - .9);   // a green bin on the sidewalk, like the reference
const clouds = [];
for (let k = 0; k < 14; k++) {
  const g = new THREE.Group(); g.position.set(-90 + k * 14 + hash(k) * 8, 22 + hash(k * 3) * 14, -70 - hash(k * 5) * 40); scene.add(g); clouds.push(g);
  for (let j = 0; j < 6; j++) { const m = new THREE.Mesh(new THREE.BoxGeometry(3 + hash(k + j) * 3, 1.6 + hash(j * 7 + k) * 1.4, 2.5), mat(0xFFFFFF, { emissive: 0xFFFFFF, emissiveIntensity: .25 })); m.position.set((j - 2.5) * 2.2, (j % 3 === 1 ? 1.2 : 0), hash(j + k) * 1.5); g.add(m); }
}

// ---------------------------------------------------------------- the city (the real-world beat), instanced and grown in
const GRID = [];
for (let gx = -9; gx <= 9; gx++) for (let gz = -10; gz <= 6; gz++) {
  const x = gx * 12 + (hash(gx * 31 + gz) - .5) * 2, z = gz * 12 - 8;
  if (Math.abs(x) < 46 && z > -24 && z < 30) continue;
  GRID.push({ x, z, w: 5 + hash(gx * 7 + gz * 3) * 3, d: 5 + hash(gx + gz * 11) * 3, h: 3 + hash(gx * 13 + gz * 17) * 8, c: ["#F4C9C9", "#F6E3A6", "#BFE3D3", "#D9CCF0", "#F7CFDD", "#BFD3EE", "#F4D9BF", "#DCE7F2"][(gx * 3 + gz * 5 + 99) % 8], r: Math.hypot(x, z) });
}
const blockTex = pix(32, 32, (g) => { px(g, "#FFFFFF", 0, 0, 32, 32); for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) px(g, "#B9D3EA", 3 + i * 10, 3 + j * 10, 6, 6); });
const cityM = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1).translate(0, .5, 0), new THREE.MeshStandardMaterial({ map: blockTex, roughness: .85 }), GRID.length);
const cityRoof = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1).translate(0, .5, 0), mat(0xFFFDF8), GRID.length);
GRID.forEach((b, i) => { cityM.setColorAt(i, tmpC.set(b.c)); });
scene.add(cityM, cityRoof);

// ---------------------------------------------------------------- characters: blocky figures with pixel faces
const HIP = .82;
const sitY = (seat) => seat + .125 - HIP;
const HOLO = { t: { value: 0 }, o: { value: 1 } };
const clipPlane = new THREE.Plane(new THREE.Vector3(0, -1, 0), 99);
function holoMat(c, map = null) {
  const base = new THREE.Color(c).lerp(new THREE.Color(CYAN), .72);
  const m = new THREE.MeshStandardMaterial({ color: map ? 0xA8F2FF : base, map, emissive: map ? 0x2FB8D8 : base.clone().multiplyScalar(.5), emissiveMap: map, emissiveIntensity: map ? .85 : 1,
    roughness: .35, transparent: true, opacity: .9, clippingPlanes: [clipPlane] });
  m.onBeforeCompile = (sh) => {
    sh.uniforms.uHT = HOLO.t; sh.uniforms.uHO = HOLO.o;
    sh.fragmentShader = "uniform float uHT, uHO;\n" + sh.fragmentShader.replace("#include <dithering_fragment>", `#include <dithering_fragment>
      float sl = step(.5, fract(gl_FragCoord.y / 6. + uHT * 2.));
      gl_FragColor.rgb = gl_FragColor.rgb * (.84 + .16 * sl) + vec3(.02, .1, .14) * sl;
      gl_FragColor.a *= uHO;`);
  };
  return m;
}
// pixel art, 24 x 24: fringe rows 0-4, brows row 8, eyes rows 10-12 at x 6 and 16, nose 13-14, mouth 16-18
function drawFace(g, sp, eyes, mouth, brows) {
  const S = sp.skin, Hc = sp.hair, D = "#1E1B18", Mo = "#5A2A22", Rd = "#C8483A", Wt = "#FFFDF8";
  px(g, S, 0, 0, 24, 24);
  if (sp.style === "cap") { px(g, sp.cap, 0, 0, 24, 5); px(g, shc(sp.cap, -.3), 0, 4, 24, 1); px(g, Hc, 0, 5, 2, 4); px(g, Hc, 22, 5, 2, 4); }
  else {
    px(g, Hc, 0, 0, 24, 4);
    if (sp.style === "short") { px(g, Hc, 0, 4, 3, 3); px(g, Hc, 21, 4, 3, 3); px(g, Hc, 4, 4, 7, 1); px(g, Hc, 14, 4, 4, 1); }
    if (sp.style === "long" || sp.style === "bun") { px(g, Hc, 0, 4, 24, 1); px(g, Hc, 0, 5, 9, 1); px(g, Hc, 15, 5, 9, 1); px(g, Hc, 0, 6, 3, 10); px(g, Hc, 21, 6, 3, 10); }
    if (sp.style === "bob") { px(g, Hc, 0, 4, 24, 2); px(g, Hc, 0, 6, 3, 11); px(g, Hc, 21, 6, 3, 11); px(g, Hc, 10, 6, 4, 0); }
    if (sp.style === "puff") { px(g, Hc, 0, 4, 2, 5); px(g, Hc, 22, 4, 2, 5); px(g, Hc, 5, 4, 14, 1); }
  }
  px(g, shc(S, -.1), 11, 13, 2, 2);
  if (!sp.beard) { px(g, "#EC9A86", 4, 15, 2, 1); px(g, "#EC9A86", 18, 15, 2, 1); }
  if (sp.beard) { const B = sp.beard; px(g, B, 3, 17, 18, 7); px(g, B, 2, 12, 2, 9); px(g, B, 20, 12, 2, 9); px(g, B, 7, 15, 10, 1); px(g, S, 9, 16, 6, 2); }
  if (sp.stache) px(g, sp.stache, 8, 15, 8, 1);
  const eye = (ex, kind) => {
    if (kind === "open") { px(g, D, ex, 10, 2, 3); px(g, Wt, ex, 10, 1, 1); }
    else if (kind === "closed") px(g, D, ex - 1, 11, 4, 1);
    else if (kind === "happy") { px(g, D, ex - 1, 11, 1, 1); px(g, D, ex, 10, 2, 1); px(g, D, ex + 2, 11, 1, 1); }
    else if (kind === "wide") { px(g, Wt, ex - 1, 10, 4, 3); px(g, D, ex, 10, 2, 2); px(g, Wt, ex, 10, 1, 1); }
    else if (kind === "half") { px(g, shc(S, -.18), ex - 1, 10, 4, 1); px(g, D, ex, 11, 2, 2); }
    else if (kind === "side") { px(g, D, ex + 1, 10, 2, 3); px(g, Wt, ex + 1, 10, 1, 1); }
    if (sp.lash && kind !== "closed" && kind !== "happy") px(g, D, ex + (ex < 12 ? -1 : 2), 9, 1, 1);
  };
  eye(6, eyes === "wink" ? "open" : eyes); eye(16, eyes === "wink" ? "happy" : eyes);
  const Bc = sp.brow || Hc;
  if (brows === "flat") { px(g, Bc, 5, 8, 4, 1); px(g, Bc, 15, 8, 4, 1); }
  if (brows === "up") { px(g, Bc, 5, 7, 4, 1); px(g, Bc, 15, 7, 4, 1); }
  if (brows === "worry") { px(g, Bc, 5, 8, 2, 1); px(g, Bc, 7, 7, 2, 1); px(g, Bc, 15, 7, 2, 1); px(g, Bc, 17, 8, 2, 1); }
  if (brows === "angry") { px(g, Bc, 5, 7, 2, 1); px(g, Bc, 7, 8, 2, 1); px(g, Bc, 15, 8, 2, 1); px(g, Bc, 17, 7, 2, 1); }
  if (brows === "raise1") { px(g, Bc, 5, 6, 4, 1); px(g, Bc, 15, 8, 4, 1); }
  if (mouth === "smile") { px(g, Mo, 10, 17, 4, 1); px(g, Mo, 9, 16, 1, 1); px(g, Mo, 14, 16, 1, 1); }
  if (mouth === "grin") { px(g, Mo, 9, 16, 6, 2); px(g, Wt, 10, 16, 4, 1); px(g, Mo, 8, 15, 1, 1); px(g, Mo, 15, 15, 1, 1); }
  if (mouth === "talk") { px(g, Mo, 10, 16, 4, 2); px(g, Rd, 11, 17, 2, 1); }
  if (mouth === "o") { px(g, Mo, 11, 16, 2, 1); px(g, Mo, 10, 17, 1, 1); px(g, Mo, 13, 17, 1, 1); px(g, Mo, 11, 18, 2, 1); px(g, Rd, 11, 17, 2, 1); }
  if (mouth === "flat") px(g, Mo, 10, 17, 4, 1);
  if (mouth === "wavy") { px(g, Mo, 9, 17, 1, 1); px(g, Mo, 10, 16, 2, 1); px(g, Mo, 12, 17, 1, 1); px(g, Mo, 13, 16, 2, 1); }
  if (mouth === "sad") { px(g, Mo, 10, 16, 4, 1); px(g, Mo, 9, 17, 1, 1); px(g, Mo, 14, 17, 1, 1); }
  if (mouth === "smirk") { px(g, Mo, 10, 17, 3, 1); px(g, Mo, 13, 16, 2, 1); }
  if (mouth === "laugh") { px(g, Mo, 9, 16, 6, 3); px(g, Wt, 10, 16, 4, 1); px(g, Rd, 10, 17, 4, 2); }
  if (sp.glasses) {
    const G = sp.glasses;
    for (const x0 of [4, 14]) { px(g, G, x0, 9, 6, 1); px(g, G, x0, 13, 6, 1); px(g, G, x0, 9, 1, 5); px(g, G, x0 + 5, 9, 1, 5); }
    px(g, G, 10, 10, 4, 1); px(g, G, 0, 10, 4, 1); px(g, G, 20, 10, 4, 1);
  }
}
const FACES = new Map();
function faceTex(sp, eyes, mouth, brows) {
  const k = sp.id + "|" + eyes + "|" + mouth + "|" + brows;
  let t = FACES.get(k);
  if (!t) { t = pix(24, 24, (g) => drawFace(g, sp, eyes, mouth, brows)); t.generateMipmaps = false; t.minFilter = THREE.LinearFilter; FACES.set(k, t); }
  return t;
}
const headSide = (sp) => pix(24, 24, (g) => {
  px(g, sp.skin, 0, 0, 24, 24);
  const long = sp.style === "long" || sp.style === "bun" || sp.style === "bob";
  if (sp.style === "cap") { px(g, sp.cap, 0, 0, 24, 5); px(g, sp.hair, 0, 5, 24, 4); }
  else px(g, sp.hair, 0, 0, 24, long ? 16 : 7);
  px(g, shc(sp.skin, -.12), 10, 10, 3, 4);
  if (sp.beard) px(g, sp.beard, 0, 14, 24, 10);
  if (sp.glasses) px(g, sp.glasses, 0, 10, 24, 1);
  if (sp.earring) px(g, "#F2B33D", 10, 15, 3, 3);
});
const headBack = (sp) => pix(24, 24, (g) => { px(g, sp.skin, 0, 0, 24, 24); px(g, sp.style === "cap" ? sp.cap : sp.hair, 0, 0, 24, sp.style === "short" || sp.style === "puff" ? 18 : 24); if (sp.style === "cap") px(g, sp.hair, 0, 8, 24, 10); });
const solidTex = (c) => pix(4, 4, (g) => px(g, c, 0, 0, 4, 4));
function torsoTex(sp, back) {
  return pix(16, 20, (g) => {
    const T = sp.top, Dk = shc(T, -.22), Lt = shc(T, .25);
    px(g, T, 0, 0, 16, 20);
    if (sp.topStyle === "hoodie") { px(g, Dk, 0, 0, 16, 2); px(g, Dk, 0, 18, 16, 2); if (back) px(g, Dk, 3, 1, 10, 5); else { px(g, "#FFFDF8", 6, 2, 1, 6); px(g, "#FFFDF8", 9, 2, 1, 6); px(g, Dk, 3, 12, 10, 5); px(g, T, 4, 13, 8, 3); } }
    if (sp.topStyle === "blazer" && !back) { px(g, "#FFFDF8", 6, 0, 4, 12); px(g, "#FFFDF8", 7, 12, 2, 2); px(g, Dk, 5, 0, 1, 12); px(g, Dk, 10, 0, 1, 12); px(g, "#F2B33D", 7, 14, 2, 1); px(g, "#F2B33D", 7, 17, 2, 1); px(g, "#E8735A", 12, 5, 2, 1); }
    if (sp.topStyle === "tee") { if (!back) { px(g, Dk, 5, 0, 6, 1); px(g, Dk, 6, 1, 4, 1); px(g, Lt, 9, 5, 3, 3); } px(g, Dk, 0, 19, 16, 1); }
    if (sp.topStyle === "cardigan" && !back) { px(g, Dk, 7, 0, 2, 20); for (let k = 0; k < 4; k++) px(g, "#FFFDF8", 7, 4 + k * 4, 1, 1); px(g, "#FFFDF8", 6, 0, 4, 2); }
  });
}
function makeChar(sp, holo = false) {
  const M = (c, map = null) => holo ? holoMat(c, map) : new THREE.MeshStandardMaterial({ color: map ? 0xffffff : c, map, roughness: .85 });
  const root = new THREE.Group(); scene.add(root);
  const hips = new THREE.Group(); hips.position.y = HIP; root.add(hips);
  const parts = [];
  const mk = (geo, m, parent, x, y, z) => { const o = new THREE.Mesh(geo, m); o.position.set(x, y, z); o.castShadow = !holo; o.receiveShadow = !holo; parent.add(o); parts.push(o); return o; };
  const Bx = (w, h, d) => new THREE.BoxGeometry(w, h, d);
  const topM = M(sp.top), pantsM = M(sp.pants), skinM = M(sp.skin), shoeM = M(sp.shoe), hairM = M(sp.hair);
  const torso = new THREE.Group(); hips.add(torso);
  mk(Bx(.56, .62, .3), [topM, topM, topM, topM, M(0xffffff, torsoTex(sp, false)), M(0xffffff, torsoTex(sp, true))], torso, 0, .31, 0);
  mk(Bx(.55, .14, .29), pantsM, hips, 0, -.04, 0);
  if (sp.topStyle === "hoodie") mk(Bx(.42, .14, .12), M(shc(sp.top, -.15)), torso, 0, .58, -.18);
  mk(Bx(.22, .08, .2), skinM, torso, 0, .64, 0);
  const neck = new THREE.Group(); neck.position.y = .66; torso.add(neck);
  const head = new THREE.Group(); head.rotation.order = "YXZ"; neck.add(head);
  const faceM = M(0xffffff, faceTex(sp, "open", "smile", "flat"));
  const sideM = M(0xffffff, headSide(sp));
  const capC = sp.style === "cap" ? sp.cap : sp.hair;
  mk(Bx(.52, .52, .52), [sideM, sideM, M(capC), skinM, faceM, M(0xffffff, headBack(sp))], head, 0, .26, 0);
  const hm = M(capC);
  if (sp.style === "cap") { mk(Bx(.56, .17, .56), hm, head, 0, .5, 0); mk(Bx(.5, .04, .24), M(shc(sp.cap, -.15)), head, 0, .425, .36); }
  else {
    mk(Bx(.56, .13, .56), hairM, head, 0, .475, 0);
    if (sp.style === "short") mk(Bx(.22, .07, .2), hairM, head, .07, .57, .06);
    if (sp.style === "long" || sp.style === "bun") { mk(Bx(.58, .7, .08), hairM, head, 0, .18, -.3); for (const s of [-1, 1]) mk(Bx(.06, .5, .24), hairM, head, s * .29, .22, -.12); }
    if (sp.style === "bun") mk(Bx(.22, .2, .22), hairM, head, 0, .63, -.1);
    if (sp.style === "bob") { for (const s of [-1, 1]) mk(Bx(.06, .36, .44), hairM, head, s * .29, .3, -.03); mk(Bx(.58, .4, .08), hairM, head, 0, .3, -.3); }
    if (sp.style === "puff") mk(Bx(.44, .3, .4), hairM, head, 0, .66, -.04);
  }
  if (sp.earring) for (const s of [-1, 1]) mk(Bx(.04, .06, .04), holo ? M(GOLD) : goldM, head, s * .275, .12, .04);
  const sh = [], el = [], hand = [], hip = [], knee = [];
  for (let k = 0; k < 2; k++) {
    const s = k ? 1 : -1;
    const a = new THREE.Group(); a.position.set(s * .37, .56, 0); torso.add(a); sh.push(a);
    mk(Bx(.17, .32, .18), topM, a, 0, -.13, 0);
    const e = new THREE.Group(); e.position.y = -.29; a.add(e); el.push(e);
    mk(Bx(.16, .27, .17), sp.topStyle === "tee" ? skinM : topM, e, 0, -.13, 0);
    hand.push(mk(Bx(.15, .13, .16), skinM, e, 0, -.32, 0));
    const h = new THREE.Group(); h.position.set(s * .135, 0, 0); hips.add(h); hip.push(h);
    mk(Bx(.23, .42, .25), pantsM, h, 0, -.19, 0);
    const kn = new THREE.Group(); kn.position.y = -.4; h.add(kn); knee.push(kn);
    mk(Bx(.22, .34, .24), pantsM, kn, 0, -.17, 0);
    mk(Bx(.24, .09, .32), shoeM, kn, 0, -.37, .04);
  }
  return { sp, holo, root, hips, torso, head, sh, el, hand, hip, knee, faceM, parts, seed: hash(sp.id.length * 7.3 + sp.skin.charCodeAt(2)) * 10 };
}
const pose = (o = {}) => ({ x: 0, y: 0, z: 0, ry: 0, lean: 0, tw: 0, hy: 0, hp: 0, hr: 0, a: [[.05, .1, .12], [.05, .1, .12]], l: [[0, 0], [0, 0]], ...o });
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
const blinkAt = (seed, t) => { const p = 2.8 + hash(seed) * 1.7, u = (t + hash(seed * 3) * 7) % p; return u < .13; };
let NOW = 0;
function setFace(P, f) {
  let eyes = f.eyes || "open";
  if ((eyes === "open" || eyes === "side") && blinkAt(P.seed, NOW)) eyes = "closed";
  let mouth = f.mouth || "smile";
  if (f.talk) mouth = Math.floor(NOW * 8.5 + P.seed) % 3 === 0 ? (f.mouth || "smile") : (Math.floor(NOW * 8.5 + P.seed) % 3 === 1 ? "talk" : "o");
  const tx = faceTex(P.sp, eyes, mouth, f.brows || "flat");
  if (P.faceM.map !== tx) { P.faceM.map = tx; if (P.holo) P.faceM.emissiveMap = tx; P.faceM.needsUpdate = true; }
}
const SP = {
  you: { id: "you", skin: "#E2AE86", hair: "#3B2A1E", style: "short", beard: "#3B2A1E", glasses: "#1E1B18", top: "#E8735A", topStyle: "hoodie", pants: "#2E3A55", shoe: "#F4EFE6" },
  fan: { id: "fan", skin: "#F3CBA5", hair: "#8A4A2A", style: "bun", top: "#F29BB8", topStyle: "hoodie", pants: "#8FB6E0", shoe: "#FFFDF8", lash: true },
  boss: { id: "boss", skin: "#8E5E40", hair: "#1E1B18", style: "bob", top: "#23345E", topStyle: "blazer", pants: "#23345E", shoe: "#1E1B18", earring: true, lash: true },
  maya: { id: "maya", skin: "#B57D58", hair: "#2A1A12", style: "puff", top: "#F2B33D", topStyle: "tee", pants: "#3A5A8C", shoe: "#E8735A", lash: true },
  jordan: { id: "jordan", skin: "#F0C49C", hair: "#B88A4A", style: "cap", cap: "#3FA372", top: "#5B7FC4", topStyle: "tee", pants: "#3A3A3A", shoe: "#FFFDF8" },
  priya: { id: "priya", skin: "#A8714C", hair: "#1E1B18", style: "long", top: "#7E5BB0", topStyle: "cardigan", pants: "#EFE6D6", shoe: "#7E5BB0", lash: true },
  ex1: { id: "ex1", skin: "#E8B894", hair: "#D8D4CC", style: "short", stache: "#D8D4CC", top: "#6E9A5C", topStyle: "cardigan", pants: "#5B5650", shoe: "#3A2618", brow: "#B8B4AC" },
  ex2: { id: "ex2", skin: "#6E4A34", hair: "#1E1B18", style: "short", top: "#D9483B", topStyle: "hoodie", pants: "#2A2E3A", shoe: "#FFFDF8" },
};

const YOU = makeChar(SP.you), FAN = makeChar(SP.fan), MAYA = makeChar(SP.maya), JORDAN = makeChar(SP.jordan), PRIYA = makeChar(SP.priya), EX1 = makeChar(SP.ex1), EX2 = makeChar(SP.ex2);
const MINI = makeChar({ ...SP.jordan, id: "jordan" }, true);   // the student in the AI's story, as a small hologram on the cafe table
MINI.root.scale.setScalar(.32);

// ---------------------------------------------------------------- THE CLOSER: a small floating voxel robot with a pixel screen face
function drawBot(g, eyes, mouth) {
  const M = "#7FFFD4", BG = "#101425";
  px(g, BG, 0, 0, 32, 20);
  for (let y = 1; y < 20; y += 2) px(g, "rgba(127,255,212,.05)", 0, y, 32, 1);
  const eye = (cx, kind) => {
    if (kind === "open") { px(g, M, cx - 1, 6, 3, 4); px(g, "#E6FFF6", cx - 1, 6, 1, 1); }
    else if (kind === "closed") px(g, M, cx - 2, 8, 5, 1);
    else if (kind === "happy") { px(g, M, cx - 2, 8, 1, 1); px(g, M, cx - 1, 7, 3, 1); px(g, M, cx + 2, 8, 1, 1); }
    else if (kind === "wide") { px(g, M, cx - 2, 5, 5, 5); px(g, BG, cx - 1, 6, 3, 3); px(g, M, cx, 7, 1, 1); }
    else if (kind === "focus") px(g, M, cx - 2, 7, 5, 2);
    else if (kind === "gentle") { px(g, M, cx - 2, 7, 1, 1); px(g, M, cx - 1, 8, 3, 1); px(g, M, cx + 2, 7, 1, 1); }
    else if (kind === "dollar") { px(g, M, cx, 4, 1, 1); px(g, M, cx - 1, 5, 3, 1); px(g, M, cx - 1, 6, 1, 1); px(g, M, cx - 1, 7, 3, 1); px(g, M, cx + 1, 8, 1, 1); px(g, M, cx - 1, 9, 3, 1); px(g, M, cx, 10, 1, 1); }
  };
  eye(10, eyes === "wink" ? "open" : eyes); eye(22, eyes === "wink" ? "happy" : eyes);
  if (mouth === "smile") { px(g, M, 13, 14, 1, 1); px(g, M, 14, 15, 4, 1); px(g, M, 18, 14, 1, 1); }
  if (mouth === "grin") { px(g, M, 12, 13, 8, 1); px(g, M, 13, 14, 6, 1); px(g, M, 14, 15, 4, 1); }
  if (mouth === "flat") px(g, M, 14, 15, 4, 1);
  if (mouth === "o") { px(g, M, 15, 13, 2, 1); px(g, M, 14, 14, 1, 2); px(g, M, 17, 14, 1, 2); px(g, M, 15, 16, 2, 1); }
  if (mouth === "soft") { px(g, M, 14, 15, 4, 1); px(g, M, 13, 16, 1, 1); px(g, M, 18, 16, 1, 1); }
  if (mouth === "talk") { px(g, M, 14, 14, 4, 2); px(g, BG, 15, 14, 2, 1); }
  px(g, "rgba(232,115,90,.55)", 6, 11, 2, 1); px(g, "rgba(232,115,90,.55)", 24, 11, 2, 1);
}
const BOTF = new Map();
const botTex = (eyes, mouth) => { const k = eyes + "|" + mouth; let t = BOTF.get(k); if (!t) { t = pix(32, 20, (g) => drawBot(g, eyes, mouth)); t.generateMipmaps = false; t.minFilter = THREE.LinearFilter; BOTF.set(k, t); } return t; };
function makeRobot() {
  const root = new THREE.Group(); scene.add(root);
  const hover = new THREE.Group(); root.add(hover);
  const parts = [];
  const mk = (geo, m, parent, x, y, z, cast = true) => { const o = new THREE.Mesh(geo, m); o.position.set(x, y, z); o.castShadow = cast; o.receiveShadow = true; parent.add(o); parts.push(o); return o; };
  const RB = (w, h, d, r = .06) => new RoundedBoxGeometry(w, h, d, 2, r);
  const coralM = gloss(CORAL, { roughness: .5 }), creamM = gloss(0xF4EFE6, { roughness: .45 }), inkM = mat(INK, { roughness: .4 });
  mk(new THREE.CylinderGeometry(.16, .22, .16, 20), inkM, hover, 0, .02, 0);
  mk(new THREE.TorusGeometry(.19, .025, 8, 28).rotateX(Math.PI / 2), glow(0x7FFFD4), hover, 0, -.06, 0, false);
  const jetM = new THREE.MeshBasicMaterial({ color: 0x9FFFE0, transparent: true, opacity: .55, toneMapped: false, depthWrite: false });
  const jet = mk(new THREE.CylinderGeometry(.13, .02, .32, 16, 1, true), jetM, hover, 0, -.24, 0, false);
  const body = new THREE.Group(); body.position.y = .1; hover.add(body);
  mk(RB(.64, .5, .44, .1), coralM, body, 0, .25, 0);
  mk(RB(.67, .08, .47, .03), creamM, body, 0, .04, 0);
  const chestM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }); LATE.push([chestM, "botChest"]);
  mk(new THREE.PlaneGeometry(.24, .17), chestM, body, 0, .28, .222, false);
  mk(new THREE.CylinderGeometry(.08, .1, .1, 12), inkM, body, 0, .54, 0);
  const head = new THREE.Group(); head.rotation.order = "YXZ"; head.position.y = .58; body.add(head);
  mk(RB(.8, .58, .52, .12), creamM, head, 0, .29, 0);
  mk(RB(.68, .44, .04, .05), inkM, head, 0, .29, .255);
  const faceM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false, map: botTex("open", "smile") });
  mk(new THREE.PlaneGeometry(.6, .37), faceM, head, 0, .29, .279, false);
  for (const s of [-1, 1]) mk(new THREE.CylinderGeometry(.08, .08, .08, 16).rotateZ(Math.PI / 2), coralM, head, s * .43, .29, 0);
  mk(new THREE.CylinderGeometry(.015, .015, .2, 8), inkM, head, 0, .67, 0);
  const tip = mk(new THREE.SphereGeometry(.06, 16, 12), glow(0xFF8A6A), head, 0, .8, 0, false);
  const sh = [], el = [], hand = [];
  for (let k = 0; k < 2; k++) {
    const s = k ? 1 : -1;
    const a = new THREE.Group(); a.position.set(s * .39, .4, 0); body.add(a); sh.push(a);
    mk(RB(.13, .24, .13, .04), coralM, a, 0, -.1, 0);
    const e = new THREE.Group(); e.position.y = -.22; a.add(e); el.push(e);
    mk(RB(.12, .2, .12, .04), creamM, e, 0, -.09, 0);
    hand.push(mk(RB(.16, .13, .16, .05), creamM, e, 0, -.24, 0));
  }
  return { root, hover, body, head, sh, el, hand, faceM, parts, jet, tip, robot: true };
}
const BOT = makeRobot();
const CAST = { you: YOU, fan: FAN, maya: MAYA, jordan: JORDAN, priya: PRIYA, ex1: EX1, ex2: EX2, mini: MINI, robot: BOT };
const rpose = (o = {}) => ({ x: 0, z: 0, y: .5, ry: 0, lean: 0, hy: 0, hp: 0, hr: 0, a: [[.15, .25, .3], [.15, .25, .3]], ...o });
function applyRobot(R, p) {
  R.root.position.set(p.x, 0, p.z); R.root.rotation.y = p.ry;
  R.hover.position.y = p.y;
  R.body.rotation.set(p.lean, 0, 0);
  R.head.rotation.set(p.hp, p.hy, p.hr);
  for (let k = 0; k < 2; k++) { R.sh[k].rotation.set(-p.a[k][0], 0, (k ? 1 : -1) * p.a[k][1]); R.el[k].rotation.x = -p.a[k][2]; }
}
function setBot(f) {
  let eyes = f.eyes || "open";
  if (eyes === "open" && blinkAt(3.3, NOW)) eyes = "closed";
  let mouth = f.mouth || "smile";
  if (f.talk) mouth = Math.floor(NOW * 8) % 2 ? "talk" : (f.mouth || "smile");
  const tx = botTex(eyes, mouth);
  if (BOT.faceM.map !== tx) { BOT.faceM.map = tx; BOT.faceM.needsUpdate = true; }
}

// ---------------------------------------------------------------- the cafe table on the sidewalk (day 4)
cyl(.34, .34, .04, mat(CREAM), -5.4, .74, 1.62, 24); cyl(.035, .035, .72, mat(INK), -5.4, .36, 1.62, 8); cyl(.2, .22, .03, mat(INK), -5.4, .015, 1.62, 16);
cyl(.2, .2, .06, mat(0x2F8F7A), -5.4, .41, .95, 16); cyl(.03, .03, .4, mat(INK), -5.4, .2, .95, 8);
cyl(.045, .04, .1, mat(CREAM), -5.18, .81, 1.52, 12);
const beamM = new THREE.MeshBasicMaterial({ color: 0x7FFFD4, transparent: true, opacity: 0, toneMapped: false, depthWrite: false, side: THREE.DoubleSide });
const beam = add(new THREE.Mesh(new THREE.ConeGeometry(.3, 1, 24, 1, true), beamM), false, false);

// ---------------------------------------------------------------- props held or floating
function makePhone() {
  const g = new THREE.Group(); scene.add(g);
  g.add(new THREE.Mesh(new RoundedBoxGeometry(.09, .17, .014, 1, .012), mat(INK, { roughness: .35 })));
  const m = texMat("phOff", { transparent: false }); const s = new THREE.Mesh(new THREE.PlaneGeometry(.078, .155), m); s.position.z = .0075; g.add(s);
  g.userData.m = m; g.visible = false; return g;
}
const PH = {};
for (const k of ["you", "fan", "maya", "priya", "jordan", "ex1", "ex2"]) PH[k] = makePhone();
const deskPhone = makePhone();
const keyM = texMat("holoKeys", { opacity: .85, depthWrite: false, side: THREE.DoubleSide });
const holoKeys = new THREE.Mesh(new THREE.PlaneGeometry(.62, .24), keyM); scene.add(holoKeys);
const holoScr = [0, 1, 2].map((k) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(.55, .38), texMat("holoChat" + k, { opacity: .8, depthWrite: false, side: THREE.DoubleSide })); scene.add(m); return m; });
const sprite = (key, w, h) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), texMat(key, { depthWrite: false })); m.visible = false; scene.add(m); return m; };
const saleS = Array.from({ length: 7 }, () => sprite("sale", .34, .136));
const linkS = Array.from({ length: 4 }, () => sprite("link", .34, .34));
const checkS = Array.from({ length: 4 }, () => sprite("paid", .62, .24));
const zz = [0, 1, 2].map(() => sprite("z", .2, .2));
const heroQ = new THREE.Group(), heroR = new THREE.Group(); scene.add(heroQ, heroR);
add(new THREE.Mesh(new RoundedBoxGeometry(.9, .42, .12, 2, .08), mat(CORAL, { emissive: CORAL, emissiveIntensity: .2 })), true, false, heroQ);
add(new THREE.Mesh(new RoundedBoxGeometry(.9, .42, .12, 2, .08), mat(CREAM, { emissive: 0xffffff, emissiveIntensity: .15 })), true, false, heroR);
plane(.82, .36, texMat("bq"), 0, 0, .065, 0, heroQ); plane(.82, .36, texMat("br"), 0, 0, .065, 0, heroR);

// instanced pools: chat bubbles, hearts, coins, confetti, city streams
const BUB_N = 120;
const bubM = new THREE.InstancedMesh(new RoundedBoxGeometry(.4, .28, .09, 1, .05), new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0x777777, emissiveIntensity: .5, roughness: .5 }), BUB_N);
for (let k = 0; k < BUB_N; k++) bubM.setColorAt(k, tmpC.set(k % 3 === 0 ? 0xE8735A : k % 3 === 1 ? 0xFFFDF8 : 0x9FFFE0));
scene.add(bubM);
const HEART_N = 30;
const heartM = new THREE.InstancedMesh(new THREE.PlaneGeometry(.3, .3), texMat("heart", { depthWrite: false, alphaTest: .4 }), HEART_N); scene.add(heartM);
const COIN_N = 60;
const coinM = new THREE.InstancedMesh(new THREE.BoxGeometry(.13, .13, .03), goldM, COIN_N); scene.add(coinM);
const CONF_N = 120;
const confM = new THREE.InstancedMesh(new THREE.BoxGeometry(.09, .13, .02), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .6, emissive: 0x333333 }), CONF_N);
for (let k = 0; k < CONF_N; k++) confM.setColorAt(k, tmpC.set([0xE8735A, 0xF2B33D, 0x7FE6FF, 0x3FA372, 0xE36FA6, 0xFFFDF8][k % 6]));
scene.add(confM);
const STR_N = 360;
const strM = new THREE.InstancedMesh(new RoundedBoxGeometry(1.1, .8, .26, 1, .12), new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0x888888, emissiveIntensity: .6, roughness: .5 }), STR_N);
for (let k = 0; k < STR_N; k++) strM.setColorAt(k, tmpC.set(k % 3 === 0 ? 0x3FA372 : k % 3 === 1 ? 0xE8735A : 0xFFFDF8));
scene.add(strM);
const ZERO = new THREE.Matrix4().makeScale(0, 0, 0);
const hideAll = (m, n) => { for (let k = 0; k < n; k++) m.setMatrixAt(k, ZERO); };
const bez = (p0, p1, p2, u, out) => out.set((1 - u) ** 2 * p0.x + 2 * (1 - u) * u * p1.x + u * u * p2.x, (1 - u) ** 2 * p0.y + 2 * (1 - u) * u * p1.y + u * u * p2.y, (1 - u) ** 2 * p0.z + 2 * (1 - u) * u * p1.z + u * u * p2.z);

// ---------------------------------------------------------------- poses
const SIT = (x, z, ry, seat = .44) => pose({ x, y: sitY(seat), z, ry, l: [[1.57, 1.57], [1.57, 1.57]], a: [[.5, .08, .95], [.5, .08, .95]] });
const withArms = (p, a, o = {}) => ({ ...p, a, ...o });
const PHONE2 = [[.4, -.18, 1.7], [.42, -.15, 1.65]];
const PHONE_UP = [[1.2, -.15, 1.2], [.42, -.15, 1.65]];
const WAVE_R = (t) => [[.25, 2.55 + .28 * Math.sin(t * 9), .45], [.05, .1, .12]];
const WAVE_L = (t) => [[.05, .1, .12], [.25, 2.55 + .28 * Math.sin(t * 9 + 1), .45]];
const CHEER = (t) => [[.3, 2.75 + .1 * Math.sin(t * 10), .2], [.3, 2.75 + .1 * Math.sin(t * 10 + 1.5), .2]];
const THUMBS = [[.9, .25, 1.55], [.9, .25, 1.55]];
function walk(p, ph, amp = 1) {
  const s = Math.sin(ph), c = Math.cos(ph);
  return { ...p, y: p.y + .035 * Math.abs(c) * amp, l: [[.42 * s * amp, (.35 + .3 * Math.max(0, -c)) * amp * (s < 0 ? 1 : .3)], [-.42 * s * amp, (.35 + .3 * Math.max(0, c)) * amp * (s > 0 ? 1 : .3)]],
    a: [[-.38 * s * amp, .1, .25], [.38 * s * amp, .1, .25]] };
}
const idle = (p, t, seed) => ({ ...p, lean: p.lean + .015 * Math.sin(t * 1.3 + seed), hr: p.hr + .03 * Math.sin(t * .9 + seed * 2), hy: p.hy + .05 * Math.sin(t * .6 + seed) });
const bob = (t) => .52 + .05 * Math.sin(t * 2.6);
const F = FOC;

// ---------------------------------------------------------------- per character, per scene: pose, face, visibility (and the phone in hand)
const BENCH = [6.5, 1.2], BOTB = { x: 7.6, z: 1.9, ry: -1.1 };
const GROUP = { priya: [1.35, 9.85, -.95], maya: [2.35, 10.55, -1.2], jordan: [2.55, 9.05, -1.3], ex1: [3.35, 10.0, -1.3], ex2: [3.2, 11.0, -1.4] };
const CROWD = { fan: [-1.0, 10.9, .3], jordan: [1.0, 11.1, -.3], ex1: [-1.75, 9.4, .45], ex2: [1.75, 9.5, -.45] };
const COMEBACK = { fan: true, ex2: true };
function youAt(t, s) {
  if (s === 0) {
    const br = Math.sin(t * 1.7);
    return { vis: true, p: pose({ ...SIT(.3, -3.32, 0), lean: -.3 + .015 * br, hy: .25, hp: -.12 + .03 * br, hr: .32, a: [[.45, .15, .9], [.45, .15, .9]] }), f: { eyes: "closed", mouth: br > .3 ? "o" : "smile", brows: "flat" } };
  }
  if (s === 5) {
    const X = -.35, Z = 9.3;
    let p = idle(withArms(pose({ x: X, z: Z, ry: .1 }), PHONE2, { hp: .35 }), t, 1);
    const cheer = { ...pose({ x: X, z: Z, ry: .1, y: .06 * Math.abs(Math.sin(t * 7)) }), a: CHEER(t), hp: -.15, lean: -.05 };
    p = mixP(p, cheer, bump(t, C.two - .1, C.calls + .4, .3));
    const look = { ...idle(pose({ x: X, z: Z, ry: .7 }), t, 1), hp: 0 };
    p = mixP(p, look, ss(t, C.woman - .2, C.woman + .3));
    if (t > C.she) p = mixP(p, withArms(look, WAVE_L(t)), ss(t, C.she, C.she + .3));
    let f = { eyes: "open", mouth: "smile", brows: "flat" };
    if (t > C.two - .1) f = { eyes: "happy", mouth: "laugh", brows: "up" };
    if (t > C.calls + .4) f = { eyes: "open", mouth: "grin", brows: "up" };
    if (t > C.woman) f = { eyes: "wide", mouth: "o", brows: "up" };
    if (t > C.she) f = { eyes: "happy", mouth: "grin", brows: "up" };
    return { vis: true, p, f, phone: t < C.two - .1 ? "phSales" : null };
  }
  if (s === 7) {
    let p = idle(pose({ x: -.1, z: 1.3, ry: .18 }), t, 3);
    p = mixP(p, withArms(p, WAVE_R(t)), bump(t, C.setup - .4, C.commentk - .3, .35));
    p = mixP(p, withArms(p, [[2.6, .25, .05], [.05, .1, .12]], { hp: -.15 }), bump(t, C.commentk - .3, C.template - .3, .3));
    p = mixP(p, withArms(p, THUMBS), ss(t, C.template - .3, C.template + .1));
    return { vis: true, p, f: { eyes: t > C.template ? "happy" : "open", mouth: t > C.commentk - .3 ? "grin" : "smile", brows: "up" } };
  }
  return { vis: false };
}
function fanAt(t, s) {
  if (s === 1) {
    let p = withArms(SIT(BENCH[0], BENCH[1], 0), PHONE2, { hp: .38 });
    const typing = { ...p, a: [[.4, -.18, 1.7 + .06 * Math.sin(t * 16)], [.42, -.15, 1.65 + .06 * Math.sin(t * 16 + 2)]] };
    p = mixP(p, typing, bump(t, C.comments - .4, C.price + .4, .2));
    const look = { ...p, hp: .05, hy: .45 };
    p = mixP(p, look, bump(t, C.scroll + .2, C.already - .2, .3));
    p = mixP(p, { ...p, hp: .3, hy: .1 }, ss(t, C.dms - .5, C.dms));
    let f = { eyes: "open", mouth: "smile", brows: "flat" };
    if (t > C.comments - .3) f = { eyes: "open", mouth: "flat", brows: "up" };
    if (t > C.scroll + .2) f = { eyes: "wide", mouth: "o", brows: "up" };
    if (t > C.already) f = { eyes: "happy", mouth: "grin", brows: "up" };
    return { vis: true, p, f, phone: t > C.already ? "phReply" : "phPrice" };
  }
  return crowdAt("fan", FAN, t, s);
}
function crowdAt(key, P, t, s) {
  if (s === 3 && CROWD[key]) {
    const [x, z, ry] = CROWD[key];
    let p = idle(withArms(pose({ x, z, ry }), PHONE2, { hp: .35 }), t, P.seed);
    const back = COMEBACK[key];
    if (back && t > C.half - .1) p = withArms({ ...p, hp: -.1, y: .05 * Math.abs(Math.sin(t * 7 + P.seed)) }, CHEER(t + P.seed));
    let f = { eyes: "open", mouth: "flat", brows: "flat" };
    if (t > C.follows + .3) f = { eyes: "open", mouth: "smile", brows: "up" };
    if (back && t > C.half - .1) f = { eyes: "happy", mouth: "grin", brows: "up" };
    return { vis: true, p, f, phone: back && t > C.half - .1 ? null : (t > C.follows + .3 ? "phFollow" : "phLink") };
  }
  if (s === 5 && GROUP[key]) {
    const [x1, z1, ry1] = GROUP[key];
    const k = Object.keys(GROUP).indexOf(key);
    const a = C.woman - .55 + k * .12, b = C.she - .15 + k * .1, x0 = x1 + 6.5;
    const u = ss(t, a, b), x = lerp(x0, x1, u);
    let p = pose({ x, z: z1, ry: u < .98 ? -Math.PI / 2 : ry1 });
    if (u > 0 && u < .98) p = walk(p, (x0 - x) / .9 * Math.PI);
    else p = idle(pose({ x, z: z1, ry: ry1 }), t, P.seed);
    if (u >= .98) p = mixP(p, withArms(p, key === "priya" ? WAVE_R(t) : CHEER(t + k)), ss(t, b, b + .3));
    const f = u >= .98 ? { eyes: "happy", mouth: key === "priya" ? "grin" : "laugh", brows: "up" } : { eyes: "open", mouth: "smile", brows: "up" };
    return { vis: t > a - .05, p, f };
  }
  if (s === 1 && (key === "ex1" || key === "ex2")) {
    const sd = key === "ex1" ? 1 : -1, z = key === "ex1" ? 8.0 : 9.6, x = sd * (-6 + (t - CU[0]) * 1.0);
    return { vis: true, p: walk(pose({ x, z, ry: sd * Math.PI / 2 }), (t - CU[0]) * 1.0 / .9 * Math.PI), f: { eyes: "open", mouth: "smile", brows: "flat" } };
  }
  return { vis: false };
}
function mayaAt(t, s) {
  if (s === 2) {
    let p = withArms(SIT(-5.4, .95, 0), PHONE2, { hp: .36 });
    const think = { ...p, hp: .1, hy: .35, a: [[.4, -.18, 1.7], [.9, -.3, 2.2]] };
    p = mixP(p, think, bump(t, C.expensive - .4, C.argue + .2, .3));
    const watch = { ...p, hp: .25, hy: .25, a: PHONE2 };
    p = mixP(p, watch, bump(t, C.story - .2, C.buys - .2, .3));
    const pay = { ...p, hp: -.05, hy: 0, a: PHONE_UP, lean: -.05 };
    p = mixP(p, pay, ss(t, C.buys - .25, C.buys + .15));
    let f = { eyes: "open", mouth: "smile", brows: "flat" };
    if (t > C.expensive - .5) f = { eyes: "half", mouth: "flat", brows: "worry" };
    if (t > C.story) f = { eyes: "open", mouth: "smile", brows: "up" };
    if (t > C.buys - .25) f = { eyes: "happy", mouth: "laugh", brows: "up" };
    return { vis: true, p, f, phone: t > C.buys - .2 ? "phPaid" : (t > C.story ? "phStory" : "phObj") };
  }
  return crowdAt("maya", MAYA, t, s);
}
function priyaAt(t, s) {
  if (s === 4) {
    let p = withArms(SIT(BENCH[0], BENCH[1], .3), PHONE2, { hp: .32 });
    const up = { ...p, hp: -.02, hy: .55, a: PHONE2 };
    p = mixP(p, up, ss(t, C.says - .4, C.says + .2));
    p = mixP(p, { ...up, hy: -.5, hp: .2, hr: -.05 }, ss(t, F[4].a - .1, F[4].a + .35));
    let f = { eyes: "open", mouth: "smile", brows: "flat" };
    if (t > C.stranger) f = { eyes: "happy", mouth: "grin", brows: "up" };
    if (t > C.says) f = { eyes: "open", mouth: "smile", brows: "up" };
    if (t > C.no - .05) f = { eyes: "wide", mouth: "o", brows: "up" };
    if (t > F[4].a) f = { eyes: "open", mouth: "flat", brows: "worry" };
    if (t > C.fit + .2) f = { eyes: "open", mouth: "smile", brows: "up" };
    return { vis: true, p, f, phone: t > C.no + .5 ? "phNo" : "phPay" };
  }
  return crowdAt("priya", PRIYA, t, s);
}
function jordanAt(t, s) { return crowdAt("jordan", JORDAN, t, s); }
function robotAt(t, s) {
  const y = bob(t);
  if (s === 0) {
    let p = rpose({ x: 1.55, z: -2.85, ry: -.28, y, hp: .25, a: [[.5, .05, 1.1 + .1 * Math.sin(t * 22)], [.5, .05, 1.1 + .1 * Math.sin(t * 22 + 1.7)]] });
    const look = { ...p, hp: -.05, hy: .1, a: [[.5, .05, 1.1], [.5, .05, 1.1]] };
    p = mixP(p, look, bump(t, C.seven - .25, C.seven + 1.3, .25));
    let f = { eyes: "focus", mouth: "flat" };
    if (t > C.seven - .2 && t < C.seven + 1.3) f = { eyes: "dollar", mouth: "grin" };
    return { vis: true, p, f };
  }
  if (s === 1) {
    const A = v3([.6, 0, .4]), B = v3([BOTB.x, 0, BOTB.z]);
    const u = ss(t, C.scroll - .7, C.scroll + .55);
    const x = lerp(A.x, B.x, u), z = lerp(A.z, B.z, u), yy = y + Math.sin(Math.PI * u) * 1.2;
    let p = rpose({ x, z, y: yy, ry: u > 0 && u < 1 ? Math.PI / 2 - .2 : (u >= 1 ? BOTB.ry : .2), lean: .35 * Math.sin(Math.PI * u), a: [[-.3 * Math.sin(Math.PI * u), .4, .2], [-.3 * Math.sin(Math.PI * u), .4, .2]] });
    if (u >= 1) p = mixP(p, { ...p, a: [[1.2, .1, .35], [.15, .25, .3]] }, bump(t, C.already - .3, C.dms + .4, .3));
    let f = { eyes: "open", mouth: "smile" };
    if (u > 0 && u < 1) f = { eyes: "focus", mouth: "grin" };
    if (t > C.closer - .2) f = { eyes: "happy", mouth: "grin", talk: t > C.already - .2 && t < C.dms + .2 };
    if (t > C.dms + .2) f = { eyes: "wink", mouth: "grin" };
    return { vis: true, p, f };
  }
  if (s === 2) {
    let p = rpose({ x: -4.25, z: 1.75, ry: -.75, y });
    const proj = { ...p, a: [[1.05, -.1, .25], [.15, .25, .3]], lean: .1 };
    p = mixP(p, proj, bump(t, C.story - .3, C.buys - .1, .3));
    const spin = ss(t, C.buys + .1, C.buys + .8) * Math.PI * 2;
    p = { ...p, ry: p.ry + spin };
    if (t > C.buys) p = { ...p, a: [[.3, 2.6, .2], [.3, 2.6, .2]] };
    let f = { eyes: "open", mouth: "smile" };
    if (t > C.expensive - .3) f = { eyes: "gentle", mouth: "smile" };
    if (t > C.story - .3) f = { eyes: "happy", mouth: "smile", talk: t < C.student + .6 };
    if (t > C.buys - .1) f = { eyes: "dollar", mouth: "grin" };
    return { vis: true, p, f };
  }
  if (s === 3) {
    let p = rpose({ x: 0, z: 8.2, ry: 0, y: y + .15, hy: .55 * Math.sin((t - C.clicked) * 2.2) * bump(t, C.clicked - .2, C.follows - .2, .3) });
    p = mixP(p, { ...p, a: [[1.1, .5, .2], [1.1, .5, .2]] }, bump(t, C.follows - .2, C.half - .2, .25));
    if (t > C.half - .1) p = { ...p, a: [[.3, 2.6, .2], [.3, 2.6, .2]] };
    let f = { eyes: "focus", mouth: "flat" };
    if (t > C.follows - .2) f = { eyes: "open", mouth: "smile", talk: t < C.half - .2 };
    if (t > C.half - .1) f = { eyes: "happy", mouth: "grin" };
    return { vis: true, p, f };
  }
  if (s === 4) {
    let p = rpose({ ...BOTB, y });
    const shake = .3 * Math.sin((t - C.no) * 11) * bump(t, C.no - .1, C.no + .9, .15);
    p = { ...p, hy: shake, hp: .05 };
    let f = { eyes: "open", mouth: "smile" };
    if (t > C.pay - .2) f = { eyes: "focus", mouth: "flat" };
    if (t > C.no - .2) f = { eyes: "gentle", mouth: "soft" };
    if (t > C.fit - .4) f = { eyes: "gentle", mouth: "smile", talk: t < C.fit + .5 };
    return { vis: true, p, f };
  }
  if (s === 5) {
    let p = rpose({ x: -1.75, z: 8.9, ry: .35, y: y + .1 });
    p = mixP(p, { ...p, a: [[.3, 2.6, .2], [.3, 2.6, .2]] }, bump(t, C.two - .1, C.calls + .4, .3));
    if (t > C.she) p = { ...p, a: [[.05, .25, .3], [.3, 2.5 + .3 * Math.sin(t * 9), .4]], ry: .7 };
    const f = t > C.two - .1 && t < C.calls + .4 ? { eyes: "dollar", mouth: "grin" } : (t > C.she ? { eyes: "happy", mouth: "grin" } : { eyes: "open", mouth: "smile" });
    return { vis: true, p, f };
  }
  if (s === 7) {
    let p = rpose({ x: 1.25, z: 1.3, ry: -.15, y });
    p = mixP(p, { ...p, a: [[.05, .25, .3], [.3, 2.5 + .3 * Math.sin(t * 9 + 1), .4]] }, bump(t, C.setup - .3, C.follow + 1.3, .35));
    p = mixP(p, { ...p, a: [[.05, .25, .3], [2.6, .25, .05]], hp: -.15 }, bump(t, C.commentk - .2, C.template - .3, .3));
    p = mixP(p, { ...p, a: [[.9, .25, 1.5], [.9, .25, 1.5]] }, ss(t, C.template - .25, C.template + .15));
    return { vis: true, p, f: { eyes: t > C.closek && t < C.template ? "wink" : "happy", mouth: "grin" } };
  }
  return { vis: false };
}
function miniAt(t, s) {
  if (s !== 2 || t < C.story - .25 || t > F[2].a - .05) return { vis: false };
  let p = idle(pose({ x: -5.08, z: 1.85, ry: -2.6 }), t, 2);
  p.y = .76;
  p = mixP(p, withArms(p, THUMBS), ss(t, C.student, C.student + .3));
  return { vis: true, p, f: { eyes: "happy", mouth: "grin", brows: "up" }, cut: lerp(.76, 1.5, ss(t, C.story - .25, C.story + .35)) };
}

// ---------------------------------------------------------------- camera shots
const SH = { p: new THREE.Vector3(), l: new THREE.Vector3(), fov: 40, ap: null };
const fixed = (p, l, fov = 40, ap = null) => () => { SH.p.set(...p); SH.l.set(...l); SH.fov = fov; SH.ap = ap; return SH; };
const move = (a, b, p0, p1, l0, l1, f0, f1, ap = null) => (t) => { const u = ss(t, a, b); SH.p.set(lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u), lerp(p0[2], p1[2], u)); SH.l.set(lerp(l0[0], l1[0], u), lerp(l0[1], l1[1], u), lerp(l0[2], l1[2], u)); SH.fov = lerp(f0, f1, u); SH.ap = ap; return SH; };
const HEADW = {}, HEADM = {};
const FV = new THREE.Vector3(), UV = new THREE.Vector3(), RV = new THREE.Vector3();
const faceShot = (key, d, h, side, fov, f1 = null, win = null, lift = .17) => (t) => {
  const M = HEADM[key];
  FV.set(0, 0, 1).transformDirection(M); UV.set(0, 1, 0).transformDirection(M); RV.set(1, 0, 0).transformDirection(M);
  FV.y *= .5; FV.normalize();
  let dd = d, ff = fov;
  if (win) { const u = ss(t, win[0], win[1]); ff = lerp(fov, f1, u); dd = d * Math.tan(fov * Math.PI / 360) / Math.tan(ff * Math.PI / 360); }
  SH.p.copy(HEADW[key]).addScaledVector(FV, dd).addScaledVector(UV, h).addScaledVector(RV, side);
  SH.l.copy(HEADW[key]).addScaledVector(UV, -lift); SH.fov = ff; SH.ap = null; return SH;
};
const SHOTS = [
  // 3 AM
  { t: 0, tr: 0, f: move(0, C.phone - .3, [.5, 7.5, 17], [.5, 2.3, 5.0], [.5, 3.0, -2], [.4, 1.5, -2.9], 40, 38) },
  { t: C.phone - .25, tr: .5, f: move(C.phone - .25, C.seven + .7, [1.95, 1.55, .7], [1.85, 1.5, .3], [1.25, 1.3, -2.8], [1.25, 1.32, -2.8], 34, 33) },
  { t: C.seven + .7, tr: .5, f: move(C.seven + .7, F[0].a, [-1.0, 2.7, 4.4], [-.8, 2.5, 3.5], [.9, 1.6, -3.0], [.9, 1.6, -3.0], 44, 42) },
  { t: F[0].a, tr: .4, f: faceShot("you", 5.6, .3, .7, 30, 26, [F[0].a, F[0].b]) },
  // day 1
  { t: CU[0], tr: 0, f: move(CU[0], C.comments + .2, [3.5, 10, 16], [7.4, 1.9, 6.6], [3, 2.5, -2], [6.7, 1.2, 1.3], 40, 36) },
  { t: C.price + .3, tr: .5, f: move(C.price + .3, F[1].a, [3.4, 2.5, 14.0], [3.8, 2.4, 13.4], [4.2, 2.3, .8], [4.4, 2.2, .9], 50, 48) },
  { t: F[1].a, tr: .4, f: faceShot("robot", 6.0, .15, -.5, 30) },
  // day 4
  { t: CU[1], tr: 0, f: move(CU[1], C.expensive, [-2.6, 2.5, 8.0], [-4.1, 2.0, 6.6], [-5.0, 1.6, 1.4], [-5.0, 1.65, 1.5], 40, 36) },
  { t: C.argue - .3, tr: .45, f: move(C.argue - .3, F[2].a, [-6.7, 2.0, 5.9], [-6.6, 1.95, 5.4], [-5.2, 1.6, 1.4], [-5.2, 1.6, 1.4], 34, 34) },
  { t: F[2].a, tr: .35, f: faceShot("maya", 5.6, .12, -.8, 30) },
  // day 10
  { t: CU[2], tr: 0, f: move(CU[2], C.follows - .3, [-3.6, 3.0, 20.0], [.6, 2.4, 19.0], [0, 2.4, 9.8], [0, 2.3, 9.8], 38, 38) },
  { t: C.follows - .3, tr: .5, f: move(C.follows - .3, CU[3], [2.2, 2.3, 17.5], [0, 6.0, 21.5], [.3, 2.2, 9.8], [0, 2.4, 9.6], 38, 40) },
  // day 18, midnight
  { t: CU[3], tr: 0, f: move(CU[3], F[3].a, [6.6, 2.2, 13], [6.2, 1.75, 7.6], [6.9, 1.6, 1.3], [7.0, 1.45, 1.4], 40, 36) },
  { t: F[3].a, tr: .35, f: faceShot("robot", 6.0, .12, -.4, 30) },
  { t: F[4].a, tr: .35, f: fixed([4.6, 1.75, 6.4], [6.45, 1.36, 1.3], 28) },
  // day 30
  { t: CU[4], tr: 0, f: move(CU[4], C.woman - .25, [-.4, .8, 17.5], [-.35, .95, 15.6], [-.2, 4.4, 0], [-.2, 3.9, 0], 40, 40) },
  { t: C.woman - .25, tr: .45, f: move(C.woman - .25, F[5].a, [-3.6, 2.2, 17.5], [-3.2, 2.1, 16.6], [1.6, 1.6, 9.8], [1.4, 1.55, 9.8], 40, 38) },
  { t: F[5].a, tr: .35, f: faceShot("priya", 6.6, .12, .4, 30, null, null, -.1) },
  // real world
  { t: CU[5], tr: 0, f: move(CU[5], C.billion, [.5, 3, 16], [.5, 24, 36], [.5, 2.2, 3], [.5, 0, 2], 40, 40, .2) },
  { t: C.billion, tr: .9, f: move(C.billion, C.week + .6, [.5, 24, 36], [16, 78, 92], [.5, 0, 2], [0, 0, -8], 40, 40, .5) },
  // close
  { t: CU[6], tr: 0, f: move(CU[6], DUR, [.55, 1.0, 12.6], [.55, 1.05, 11.6], [.55, 3.0, 1.3], [.55, 3.0, 1.3], 40, 40) },
];
const ease3 = (x) => (x < .5 ? 4 * x * x * x : 1 - (-2 * x + 2) ** 3 / 2);
const CAMP = new THREE.Vector3(), CAML = new THREE.Vector3(), PREV = { p: new THREE.Vector3(), l: new THREE.Vector3(), fov: 40 };
let CAMAP = null;
function camAt(t) {
  let i = 0; while (i < SHOTS.length - 1 && t >= SHOTS[i + 1].t) i++;
  const cur = SHOTS[i]; const r = cur.f(t);
  CAMP.copy(r.p); CAML.copy(r.l); let fov = r.fov; CAMAP = r.ap;
  if (cur.tr > 0 && i > 0 && t < cur.t + cur.tr) {
    const pr = SHOTS[i - 1].f(t); PREV.p.copy(pr.p); PREV.l.copy(pr.l); PREV.fov = pr.fov;
    const u = ease3(ramp(t, cur.t, cur.t + cur.tr));
    const dist = PREV.p.distanceTo(CAMP);
    CAMP.lerpVectors(PREV.p, CAMP, u); CAMP.y += Math.sin(Math.PI * u) * Math.min(dist * .1, 2);
    CAML.lerpVectors(PREV.l, CAML, u); fov = lerp(PREV.fov, fov, u);
  }
  return fov;
}

// ---------------------------------------------------------------- looks per scene
const SKY = {};
const DAY = { sky: "day", fog: 0xD6E9F6, hs: 0xEAF4FF, hg: 0xD6C9B0, hi: 1.0, sun: 0xFFF2DC, si: 2.3, sp: [8, 16, 12], night: 0 };
const NIGHT = { sky: "night", fog: 0x1E2850, hs: 0x6A78B8, hg: 0x22223A, hi: .7, sun: 0xA9BCFF, si: .5, sp: [-6, 14, 10], night: 1 };
const LOOKS = [
  NIGHT,
  DAY,
  { sky: "aft", fog: 0xF3E3C8, hs: 0xFFF0DC, hg: 0xD9C7A8, hi: .95, sun: 0xFFD9A8, si: 2.4, sp: [-6, 9, 12], night: 0 },
  { ...DAY, sp: [-6, 16, 12] },
  { ...NIGHT, hi: .62, sp: [6, 14, 10] },
  { sky: "gold", fog: 0xF7C493, hs: 0xFFE2C4, hg: 0xC9A88A, hi: .85, sun: 0xFFB070, si: 2.6, sp: [-12, 6, 14], night: 0 },
  { ...DAY, sp: [10, 22, 14] },
  { ...DAY, sp: [-6, 16, 14] },
];
const SALES = [[C.seven - .1, 0, 7, .5], [C.buys, 7, 31, .8], [C.half, 31, 96, 1.2], [C.two, 96, 212, 1.2]];
function salesAt(t) { let n = 0; for (const [a, v0, v1, d] of SALES) if (t >= a) n = Math.round(lerp(v0, v1, ss(t, a, a + d))); return n; }

// ---------------------------------------------------------------- render at time t
const PP = new THREE.Vector3(), A0 = new THREE.Vector3(), A1 = new THREE.Vector3(), A2 = new THREE.Vector3();
let billN = -1;
function drawBill(n) {
  if (!TEX.billC || n === billN) return; billN = n;
  const g = TEX.billG, w = 860, h = 420;
  g.fillStyle = "#FFFDF8"; g.fillRect(0, 0, w, h);
  g.fillStyle = "#3FA372"; g.fillRect(0, 0, w, 90);
  g.fillStyle = "#fff"; g.font = "700 46px JBMono, monospace"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("SALES", w / 2, 48);
  g.fillStyle = n >= 212 ? "#3FA372" : "#1E1B18"; g.font = "800 220px Manrope, sans-serif"; g.fillText(String(n), w / 2, 262);
  TEX.billT.needsUpdate = true;
}
function placeChar(P, st) {
  P.root.visible = !!st.vis;
  if (!st.vis) return;
  applyPose(P, st.p);
  setFace(P, st.f);
}
const STATE = {};
function phoneIn(key, P, tex) {
  const ph = PH[key];
  ph.visible = !!tex && P.root.visible; if (!ph.visible) return;
  P.hand[0].getWorldPosition(PP); const HP = HEADW[key];
  ph.position.copy(PP).addScaledVector(V.subVectors(HP, PP).normalize(), .07); ph.position.y += .03;
  ph.lookAt(HP); ph.rotateZ(Math.PI);
  if (TEX[tex]) setMap(ph.userData.m, TEX[tex]);
}
const billboard = (m) => m.quaternion.copy(camera.quaternion);
function renderAt(t) {
  NOW = t;
  const s = sceneOf(t), Lk = LOOKS[s];
  scene.background = SKY[Lk.sky] || null;
  scene.fog.color.set(Lk.fog);
  hemi.color.set(Lk.hs); hemi.groundColor.set(Lk.hg); hemi.intensity = Lk.hi;
  sun.color.set(Lk.sun); sun.intensity = Lk.si;
  const night = Lk.night;
  for (const m of NIGHTM) m.emissiveIntensity = night * .9;
  LAMPM.color.set(night ? 0xFFE7B0 : 0xF2EEE6);
  winSkyM.color.set(night ? 0x2A3666 : s === 2 ? 0xFFE2B8 : 0xBFD9EC);
  for (const [k, g] of clouds.entries()) { g.position.x = -90 + k * 14 + hash(k) * 8 + t * .25; g.visible = !night; }
  ceilL.intensity = s === 0 ? .9 : 0;
  deskL.intensity = s === 0 ? 1.2 : 0;
  dlamp.material.emissiveIntensity = s === 0 ? 1.2 : 0;
  wallL.intensity = s === 0 ? 2.0 : 0;
  pendL.intensity = 0; pshade.material.emissiveIntensity = 0; lapL.intensity = 0; padM.opacity = 0;
  streetA.intensity = s === 0 ? 1.4 : 0;
  streetB.intensity = s === 4 ? 2.2 : 0; streetB.position.set(4.9, 3.2, 2.4);
  inboxM.color.setScalar(s === 0 ? 1.15 : .8);
  if (TEX.inbox) TEX.inbox.offset.y = -(s === 0 ? Math.max(0, t - C.buzzing) * .45 : t * .03);

  // characters
  placeChar(YOU, STATE.you = youAt(t, s));
  placeChar(FAN, STATE.fan = fanAt(t, s));
  placeChar(MAYA, STATE.maya = mayaAt(t, s));
  placeChar(PRIYA, STATE.priya = priyaAt(t, s));
  placeChar(JORDAN, STATE.jordan = jordanAt(t, s));
  placeChar(EX1, STATE.ex1 = crowdAt("ex1", EX1, t, s));
  placeChar(EX2, STATE.ex2 = crowdAt("ex2", EX2, t, s));
  const ms = miniAt(t, s); placeChar(MINI, ms);
  clipPlane.constant = ms.vis ? ms.cut : 99;
  HOLO.t.value = t; HOLO.o.value = .92 + .08 * Math.sin(t * 23) * Math.sin(t * 7.1);
  const rs = robotAt(t, s); BOT.root.visible = rs.vis;
  if (rs.vis) { applyRobot(BOT, rs.p); setBot(rs.f); BOT.jet.scale.y = 1 + .25 * Math.sin(t * 31); BOT.tip.scale.setScalar(1 + .25 * Math.sin(t * 5)); }
  scene.updateMatrixWorld(true);
  for (const k in CAST) {
    const P = CAST[k]; if (!P.root.visible) continue;
    HEADM[k] = P.head.matrixWorld;
    HEADW[k] = (HEADW[k] || new THREE.Vector3()).set(0, P.robot ? .29 : .26, 0).applyMatrix4(P.head.matrixWorld);
  }
  cloneL.intensity = 0;
  if (rs.vis) { BOT.root.getWorldPosition(V); cloneL.position.set(V.x, 1.9, V.z).add(V2.set(0, 0, .9).applyAxisAngle(THREE.Object3D.DEFAULT_UP, BOT.root.rotation.y)); cloneL.intensity = night ? 1.1 : 0; }
  // phones in hand
  for (const k of ["you", "fan", "maya", "priya", "jordan", "ex1", "ex2"]) phoneIn(k, CAST[k], STATE[k].vis && STATE[k].phone);
  phoneL.intensity = 0;
  if (s === 4) { PH.priya.getWorldPosition(phoneL.position); phoneL.position.z += .15; phoneL.intensity = 1.0; }
  // the phone on the desk at 3 AM: buzzing, lit
  deskPhone.visible = s === 0;
  if (s === 0) {
    const buzz = t > C.buzzing - .3 ? .006 * Math.sin(t * 70) : 0;
    deskPhone.position.set(.62 + buzz, .757, -2.5); deskPhone.rotation.set(-Math.PI / 2, 0, .4 + buzz * 6);
    if (TEX.phSales) setMap(deskPhone.userData.m, t > C.buzzing - .3 ? TEX.phSales : TEX.phOff);
    if (t > C.buzzing - .3) { phoneL.position.set(.62, .95, -2.5); phoneL.intensity = 1.2; }
  }

  // the camera
  let fov = camAt(t);
  const bars = Math.max(1 - ss(t, C.seven - .4, C.seven), bump(t, C.midnight - .4, CU[4] - .2, .4));
  let fb = 0; for (const f of FOC) fb = Math.max(fb, bump(t, f.a, f.b, .3));
  camera.position.copy(CAMP);
  const hand = .025 * Math.max(bars, s === 0 ? .4 : 0) * Math.min(1, CAMP.distanceTo(CAML) / 2.5);
  camera.position.x += Math.sin(t * .37) * .02 + (Math.sin(t * 3.1) + Math.sin(t * 7.3 + 1) * .5) * hand;
  camera.position.y += Math.sin(t * .29 + 1) * .015 + (Math.sin(t * 2.7 + 2) + Math.sin(t * 6.1) * .5) * hand;
  camera.fov = fov;
  const look = CAML.clone();
  const cv = window.CLOSER_COVER;
  if (cv) { camera.position.set(...cv.cam); camera.fov = cv.fov; look.set(...cv.look); }
  camera.updateProjectionMatrix();
  camera.lookAt(look);
  camera.updateMatrixWorld();

  // floating things
  holoKeys.visible = s === 0; for (const m of holoScr) m.visible = s === 0;
  if (s === 0) {
    holoKeys.position.set(0, .92, .5).applyMatrix4(BOT.root.matrixWorld); holoKeys.rotation.set(-1.1, BOT.root.rotation.y, 0, "YXZ");
    holoScr.forEach((m, k) => { m.position.set(2.2 + k * .12, 1.6 + k * .5, -3.05 - k * .2); m.rotation.set(0, -.55 - k * .1, 0); m.position.y += .03 * Math.sin(t * 1.5 + k); });
  }
  zz.forEach((m, k) => {
    m.visible = s === 0 && t < F[0].b; if (!m.visible) return;
    const u = ((t * .45 + k / 3) % 1);
    m.position.copy(HEADW.you).add(V.set(.25 + u * .3, .3 + u * .55, .05)); m.scale.setScalar(.6 + u * .8); billboard(m); m.material.opacity = Math.sin(Math.PI * u);
  });
  saleS.forEach((m, k) => {
    const a = C.buzzing - .2 + k * .27, u = ramp(t, a, a + 2.2);
    m.visible = s === 0 && u > 0 && u < 1 && t < C.seven + .7; if (!m.visible) return;
    m.position.set(.5 + hash(k) * .35, .9 + u * 1.3, -2.3 + (hash(k * 3) - .5) * .2); billboard(m);
    m.scale.setScalar(ss(u, 0, .12) * (1 - ss(u, .8, 1)) + .001); m.material.opacity = (1 - ss(u, .7, 1)) * (1 - ss(t, C.seven + .35, C.seven + .7));
  });
  // day 10: links over the crowd, then the ones who came back
  const crowdKeys = ["fan", "jordan", "ex1", "ex2"];
  linkS.forEach((m, k) => {
    const key = crowdKeys[k], back = COMEBACK[key];
    m.visible = s === 3 && t > C.clicked - .2 && !(back && t > C.half - .1); if (!m.visible) return;
    m.position.copy(HEADW[key]).add(V.set(0, .58, 0)); billboard(m);
    m.scale.setScalar(ss(t, C.clicked - .2 + k * .1, C.clicked + .1 + k * .1) * (back ? 1 : 1 - .6 * ss(t, C.half, C.half + .4)) + .001);
  });
  checkS.forEach((m, k) => {
    const key = crowdKeys[k];
    m.visible = s === 3 && COMEBACK[key] && t > C.half - .1; if (!m.visible) return;
    m.position.copy(HEADW[key]).add(V.set(0, .62, 0)); billboard(m); m.scale.setScalar(ss(t, C.half - .1, C.half + .2) + .001);
  });
  // the story hologram's beam (day 4)
  beamM.opacity = s === 2 ? .22 * bump(t, C.story - .3, C.buys - .1, .25) : 0;
  if (beamM.opacity > 0) { BOT.hand[0].getWorldPosition(A0); A1.set(-5.08, .78, 1.85); const L_ = A0.distanceTo(A1); beam.position.lerpVectors(A0, A1, .5); beam.scale.set(1, L_, 1); beam.quaternion.setFromUnitVectors(V.set(0, -1, 0), V2.subVectors(A1, A0).normalize()); }
  beam.visible = beamM.opacity > 0;
  // hero bubbles: the PRICE comment and the instant DM (day 1)
  heroQ.visible = s === 1 && t > C.price - .1 && t < C.scroll + .4; heroR.visible = s === 1 && t > C.already - .3 && t < C.dms + .5;
  if (heroQ.visible) { const u = ss(t, C.price - .1, C.scroll + .3); PH.fan.getWorldPosition(A0); heroQ.position.copy(A0).add(V.set(0, .35 + u * 1.2, .1)); billboard(heroQ); heroQ.scale.setScalar(ss(t, C.price - .1, C.price + .2) * .9 + .001); }
  if (heroR.visible) { const u = ss(t, C.already - .3, C.already + .5); BOT.hand[0].getWorldPosition(A0); PH.fan.getWorldPosition(A2); A2.y += .35; A1.lerpVectors(A0, A2, .5).add(V.set(0, .5, 0)); bez(A0, A1, A2, u, heroR.position); billboard(heroR); heroR.scale.setScalar(.4 + .5 * u + .001); }

  // pools
  hideAll(bubM, BUB_N); hideAll(heartM, HEART_N); hideAll(coinM, COIN_N); hideAll(confM, CONF_N); hideAll(strM, STR_N);
  let bi = 0;
  const putB = (p, sc) => { if (bi < BUB_N) { M4.compose(p, camera.quaternion, S.setScalar(sc)); bubM.setMatrixAt(bi++, M4); } };
  if (s === 0 && t > C.seven - .6) {   // orders stream in through the night window onto the DM wall
    const n = Math.floor(lerp(8, 50, ss(t, C.seven - .5, E[0])));
    for (let k = 0; k < n; k++) {
      const per = 1.8 + hash(k) * .8, u = ((t * (1 + hash(k * 9) * .3) + hash(k * 3) * per) % per) / per;
      A0.set(-6 + hash(k * 11) * 13, 8 + hash(k * 13) * 5, 9 + hash(k * 17) * 6); A1.set((hash(k) - .5) * 3, 3.4, -.6); A2.set(-1.0 + hash(k * 5) * 2.6, 1.5 + hash(k * 7) * 1.3, -4.3);
      bez(A0, A1, A2, u, PP); putB(PP, .5 + Math.sin(Math.PI * u) * .6);
    }
  }
  if (s === 3) {   // the follow-ups fly from the robot to each person
    BOT.head.getWorldPosition(A0);
    crowdKeys.forEach((key, k) => { for (let j = 0; j < 2; j++) { const a = C.follows - .1 + k * .12 + j * .5, u = ramp(t, a, a + .6); if (u <= 0 || u >= 1) continue; A2.copy(HEADW[key]).add(V.set(0, .3, 0)); A1.lerpVectors(A0, A2, .5).add(V.set(0, 1.0, 0)); bez(A0, A1, A2, u, PP); putB(PP, .7); } });
  }
  if (s === 6 || (s === 5 && t > CU[5] - .3)) {
    for (let k = 0; k < 24; k++) { const u = ((t * .7 + hash(k * 3)) % 1); A0.set(.3, 4.2, -.5); A1.set(.3 + (hash(k) - .5) * 10, 12, 4); A2.set((hash(k * 7) - .5) * 60, 2, (hash(k * 5) - .5) * 60); bez(A0, A1, A2, u, PP); putB(PP, 1.6); }
  }
  let hi = 0;
  const putH = (p, sc) => { if (hi < HEART_N) { M4.compose(p, camera.quaternion, S.setScalar(sc)); heartM.setMatrixAt(hi++, M4); } };
  if (s === 1 && t > C.dms - .2) for (let k = 0; k < 5; k++) { const u = ramp(t, C.dms - .2 + k * .12, C.dms + 1.0 + k * .12); if (u <= 0) continue; PH.fan.getWorldPosition(PP); PP.add(V.set((hash(k) - .5) * .5, .2 + u * 1.1, .1)); putH(PP, .5 * Math.sin(Math.PI * Math.min(u, .999))); }
  if (s === 5 && t > C.she - .2) for (let k = 0; k < 14; k++) { const key = ["priya", "maya", "jordan", "ex1", "ex2"][k % 5]; if (!CAST[key].root.visible) continue; const per = 1.6, u = ((t - C.she + .2 + hash(k) * per) % per) / per; PP.copy(HEADW[key]).add(V.set((hash(k * 3) - .5) * .6, .4 + u * 1.5, (hash(k * 5) - .5) * .4)); putH(PP, .5 * Math.sin(Math.PI * u)); }
  if (s === 7 && t > C.template - .2) for (let k = 0; k < 10; k++) { const u = ((t - C.template + hash(k) * 1.5) % 1.5) / 1.5; PP.set(.55 + (hash(k * 3) - .5) * 2.6, 2.1 + u * 1.6, 1.4); putH(PP, .5 * Math.sin(Math.PI * u)); }
  let ci = 0;
  const burst = (t0, o, n, spread = 1.2, up = 3.0) => { for (let k = 0; k < n && ci < COIN_N; k++) { const u = ramp(t, t0, t0 + 1.3); if (u <= 0 || u >= 1) { ci++; continue; } const a = hash(k + t0) * Math.PI * 2, sp = spread * (.6 + hash(k * 3 + t0)); PP.set(o.x + Math.cos(a) * sp * u, o.y + (up + hash(k * 7)) * u - 4.5 * u * u, o.z + Math.sin(a) * sp * u); Q.setFromAxisAngle(V.set(0, 1, 0), t * 8 + k); M4.compose(PP, Q, S.setScalar(1)); coinM.setMatrixAt(ci++, M4); } };
  if (s === 0 && t > C.seven - .1) burst(C.seven - .1, A0.set(.62, .85, -2.5), 18, .9, 2.6);
  if (s === 2 && t > C.buys - .1) burst(C.buys - .1, PH.maya.getWorldPosition(A1), 20, 1.0, 2.8);
  if (s === 3 && t > C.half - .1) { burst(C.half - .1, A1.copy(HEADW.fan), 10, .8, 2.2); burst(C.half - .05, A2.copy(HEADW.ex2), 10, .8, 2.2); }
  if (s === 5 && t > C.two - .1) for (let k = 0; k < CONF_N; k++) { const u = ramp(t, C.two - .1 + hash(k * 9) * .3, C.two + 3.2); if (u <= 0 || u >= 1) continue; const a = hash(k) * Math.PI * 2; PP.set(.5 + (hash(k * 3) - .5) * 4.2 + Math.cos(a) * u * 3, 7.6 + 2.5 * u - 9 * u * u + Math.sin(t * 3 + k) * .1, -1.6 + Math.sin(a) * u * 4 + u * 6); Q.setFromEuler(new THREE.Euler(t * 5 + k, t * 3 + k * 2, 0)); M4.compose(PP, Q, S.setScalar(1.3)); confM.setMatrixAt(k, M4); }
  const grow = s === 6 ? 1 : 0;
  GRID.forEach((b, i) => {
    const g = grow * ss(t, C.billion - .5 + b.r * .006, C.billion + .3 + b.r * .006);
    M4.compose(V.set(b.x, 0, b.z), Q.identity(), S.set(b.w, Math.max(.001, b.h * g), b.d)); cityM.setMatrixAt(i, g > 0 ? M4 : ZERO);
    M4.compose(V.set(b.x, b.h * g, b.z), Q.identity(), S.set(b.w + .3, .3 * g, b.d + .3)); cityRoof.setMatrixAt(i, g > 0 ? M4 : ZERO);
  });
  if (s === 6) {
    const n = Math.floor(lerp(20, STR_N, ss(t, C.business - .3, C.every + .5)));
    for (let k = 0; k < n; k++) {
      const a = GRID[(k * 7) % GRID.length], b = GRID[(k * 13 + 5) % GRID.length]; if (!a || !b) continue;
      const ga = ss(t, C.billion + .2 + a.r * .006, C.billion + .8 + a.r * .006); if (ga < 1) continue;
      const per = 2.4 + hash(k) * 1.4, u = ((t * (1 + hash(k * 3) * .4) + hash(k * 5) * per) % per) / per;
      A0.set(a.x, a.h + .5, a.z); A2.set(b.x, b.h + .5, b.z); A1.lerpVectors(A0, A2, .5); A1.y += 10 + hash(k * 7) * 12;
      bez(A0, A1, A2, u, PP); M4.compose(PP, camera.quaternion, S.setScalar(2.6 * Math.sin(Math.PI * u) + .4)); strM.setMatrixAt(k, M4);
    }
  }
  for (const m of [bubM, heartM, coinM, confM, strM, cityM, cityRoof]) m.instanceMatrix.needsUpdate = true;
  drawBill(salesAt(t));
  billG.visible = s !== 7;

  // grade: letterbox, AI scan, flashes, warmth
  const scan = Math.max(.5 * bump(t, C.seven + .6, E[0] - .2, .3), .5 * bump(t, C.scroll - .5, C.scroll + .7, .2), .45 * bump(t, C.clicked - .2, C.half - .2, .3), .35 * bump(t, C.business - .3, C.week + .5, .4));
  let fl = 0; for (const ct of CU) fl += .65 * Math.exp(-(((t - ct) / .07) ** 2)) * (t >= ct ? 1 : .2);
  fl += .45 * pulse(t, C.seven - .05, .07) + .3 * pulse(t, C.buys, .08) + .25 * pulse(t, C.half, .08) + .35 * pulse(t, C.no, .08) + .3 * pulse(t, C.two, .08) + .25 * pulse(t, C.she, .08);
  grade.uniforms.uFlash.value = fl;
  grade.uniforms.uSat.value = 1 - scan * .2;
  grade.uniforms.uCool.value = s === 4 ? .38 : night ? .25 : 0;
  grade.uniforms.uWarm.value = s === 2 ? .25 : s === 5 ? .45 : 0;
  grade.uniforms.uBars.value = bars;
  grade.uniforms.uScan.value = scan;
  grade.uniforms.uCon.value = .1 * bars;
  grade.uniforms.uCA.value = .001 + .003 * bars + .005 * pulse(t, C.no, .15) + .004 * pulse(t, C.seven, .15);
  grade.uniforms.uTime.value = t;
  grade.uniforms.uVig.value = .24 + .4 * fb + (night ? .18 : 0);
  faceKey.position.copy(camera.position).add(V.set(.3, .4, 0));
  faceKey.intensity = fb * (night ? 1.6 : .9) + (s === 4 ? .8 : 0);
  const fd = camera.position.distanceTo(look);
  cocPass.uniforms.uF.value = fd;
  cocPass.uniforms.uAp.value = CAMAP ?? clamp(1.25 / fd, .08, .95);
  dofPass.uniforms.uMaxR.value = 16;
  if (cv) { for (const u of ["uBars", "uScan", "uFlash"]) grade.uniforms[u].value = 0; grade.uniforms.uCA.value = .001; cocPass.uniforms.uAp.value = cv.ap ?? .15; cocPass.uniforms.uF.value = cv.focus ?? fd; }
  const ext = clamp(fd * .9, 7, 60);
  const sp = V2.set(...Lk.sp);
  if (s === 3) sp.applyAxisAngle(THREE.Object3D.DEFAULT_UP, Math.PI * 2 * ss(t, C.later - .4, C.follows));   // a day passes
  sun.target.position.copy(look); sun.position.copy(look).add(sp.normalize().multiplyScalar(50));
  Object.assign(sun.shadow.camera, { left: -ext, right: ext, top: ext, bottom: -ext, near: 1, far: 140 });
  sun.shadow.camera.updateProjectionMatrix();
  scene.fog.near = fd * 2 + 40; scene.fog.far = fd * 5 + 200;
  renderer.setRenderTarget(sceneRT);
  renderer.render(scene, camera);
  renderer.setRenderTarget(null);
  composer.render();
}

// ---------------------------------------------------------------- textures that need the fonts, then the first frame
function buildTextures() {
  const FT = (w, f) => `${w} ${f}px Manrope, sans-serif`, MONO = (f) => `700 ${f}px JBMono, monospace`;
  const text = (w, h, draw) => pix(w, h, draw, false);
  for (const [txt, bg] of signs) TEX["sign:" + txt + ":" + bg] = text(640, 124, (g, w, h) => { g.fillStyle = bg; g.fillRect(0, 0, w, h); g.strokeStyle = "rgba(255,255,255,.85)"; g.lineWidth = 8; g.strokeRect(10, 10, w - 20, h - 20); g.fillStyle = "#fff"; g.font = FT(800, 70); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(txt, w / 2, h / 2 + 4); });
  const grad = (stops, stars = false) => text(16, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); stops.forEach(([o, c]) => gr.addColorStop(o, c)); g.fillStyle = gr; g.fillRect(0, 0, w, h); if (stars) for (let k = 0; k < 18; k++) px(g, "rgba(255,255,255,.8)", Math.floor(hash(k) * 16), Math.floor(hash(k * 3) * 230), 1, 1); });
  SKY.day = grad([[0, "#6FAEE6"], [.55, "#A9D2F2"], [1, "#DCEBF6"]]);
  SKY.night = grad([[0, "#0B1130"], [.6, "#1E2850"], [1, "#34407A"]], true);
  SKY.aft = grad([[0, "#8EC0EA"], [.6, "#CFE0EE"], [1, "#F5E4C8"]]);
  SKY.gold = grad([[0, "#7F95CF"], [.5, "#E9B48C"], [1, "#F9CB92"]]);
  const names = ["maya_makes", "jordan.edits", "priya.codes", "sam_lifts", "lena.draws", "kai.travels", "noor.cooks", "alex.films", "zoe.sings", "omar.builds"];
  TEX.inbox = text(512, 1024, (g, w, h) => {
    g.fillStyle = "#14182A"; g.fillRect(0, 0, w, h);
    for (let k = 0; k < 10; k++) {
      const y = k * 102 + 8;
      g.fillStyle = "#1F2540"; rr(g, 12, y, w - 24, 88, 18); g.fill();
      g.fillStyle = ["#E8735A", "#F2B33D", "#3FA372", "#7E5BB0", "#3A7BD5"][k % 5]; g.beginPath(); g.arc(56, y + 44, 28, 0, Math.PI * 2); g.fill();
      g.fillStyle = "#FFFDF8"; g.font = FT(800, 28); g.textAlign = "left"; g.fillText("@" + names[k], 100, y + 38);
      g.fillStyle = "#9AA3C0"; g.font = FT(600, 22); g.fillText(["just bought the course!", "PRICE", "is it worth it?", "how do I pay?", "sending to my friend"][k % 5], 100, y + 70);
      g.fillStyle = "#7FFFB0"; g.font = MONO(20); g.textAlign = "right"; g.fillText("PAID $97 ✓", w - 30, y + 54);
    }
  });
  TEX.inbox.wrapS = TEX.inbox.wrapT = THREE.RepeatWrapping; TEX.inbox.repeat.set(1, .5);
  TEX.lapStudio = text(256, 168, (g, w, h) => { g.fillStyle = "#14182A"; g.fillRect(0, 0, w, h); for (let k = 0; k < 5; k++) { g.fillStyle = k % 2 ? "#E8735A" : "#2C3456"; g.fillRect(16, 16 + k * 30, 120 + (k * 37) % 100, 20); } });
  TEX.monitor = text(256, 150, (g, w, h) => { g.fillStyle = "#1A1F33"; g.fillRect(0, 0, w, h); g.fillStyle = "#E8735A"; g.fillRect(14, 100, 228, 10); for (let k = 0; k < 6; k++) { g.fillStyle = ["#3A7BD5", "#3FA372", "#F2B33D"][k % 3]; g.fillRect(14 + k * 38, 120, 34, 16); } g.fillStyle = "#2C3456"; g.fillRect(14, 14, 228, 76); });
  TEX.lapOffice = text(200, 300, (g, w, h) => { g.fillStyle = "#F7F4EE"; g.fillRect(0, 0, w, h); g.fillStyle = "#23345E"; g.fillRect(0, 0, w, 40); g.fillStyle = "#3A7BD5"; rr(g, 16, 80, 160, 60, 14); g.fill(); g.fillStyle = "#fff"; g.font = FT(800, 22); g.fillText("Collab?", 30, 110); g.fillText("$1,500", 30, 132); });
  TEX.con0 = text(260, 340, (g, w, h) => { g.fillStyle = "#FFFDF8"; g.fillRect(0, 0, w, h); g.fillStyle = "#23345E"; g.font = FT(800, 30); g.fillText("CONTRACT", 22, 50); for (let k = 0; k < 6; k++) { g.fillStyle = "#E4D9C7"; g.fillRect(22, 80 + k * 26, w - 44, 12); } g.fillStyle = "#1E1B18"; g.font = FT(800, 54); g.fillText("$1,500", 22, 300); });
  TEX.con1 = text(260, 340, (g, w, h) => { g.fillStyle = "#FFFDF8"; g.fillRect(0, 0, w, h); g.fillStyle = "#23345E"; g.font = FT(800, 30); g.fillText("CONTRACT", 22, 50); for (let k = 0; k < 6; k++) { g.fillStyle = "#E4D9C7"; g.fillRect(22, 80 + k * 26, w - 44, 12); } g.fillStyle = "#3FA372"; g.font = FT(800, 54); g.fillText("$3,000", 22, 300); g.save(); g.translate(170, 200); g.rotate(-.35); g.strokeStyle = "#3FA372"; g.lineWidth = 7; rr(g, -70, -30, 140, 60, 10); g.stroke(); g.font = FT(800, 34); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("SIGNED", 0, 2); g.restore(); });
  TEX.skyline = text(512, 256, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#0B1130"); gr.addColorStop(1, "#2A3566"); g.fillStyle = gr; g.fillRect(0, 0, w, h); for (let k = 0; k < 14; k++) { const x = k * 38, bh = 60 + hash(k) * 140; g.fillStyle = "#1A2146"; g.fillRect(x, h - bh, 34, bh); for (let i = 0; i < 3; i++) for (let j = 0; j < Math.floor(bh / 18); j++) if (hash(k * 9 + i * 3 + j) > .55) { g.fillStyle = "#FFD98A"; g.fillRect(x + 5 + i * 10, h - bh + 8 + j * 18, 5, 7); } } g.fillStyle = "#F4F0E0"; g.beginPath(); g.arc(420, 50, 22, 0, Math.PI * 2); g.fill(); });
  TEX.logo = text(512, 160, (g, w, h) => { g.clearRect(0, 0, w, h); g.shadowColor = "#7FB8FF"; g.shadowBlur = 24; g.fillStyle = "#DCEBFF"; g.font = FT(800, 84); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("BRAND CO.", w / 2, h / 2 + 4); });
  TEX.neon = text(560, 200, (g, w, h) => { g.clearRect(0, 0, w, h); g.shadowColor = "#FF6F9F"; g.shadowBlur = 26; g.fillStyle = "#FFD0E4"; g.font = FT(800, 100); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("DM ME", w / 2, h / 2 + 6); });
  const phone = (draw) => text(156, 310, (g, w, h) => { g.fillStyle = "#FFFDF8"; g.fillRect(0, 0, w, h); g.fillStyle = "#1E1B18"; g.fillRect(0, 0, w, 34); g.fillStyle = "#fff"; g.font = MONO(14); g.fillText("@you", 10, 22); draw(g, w, h); });
  const bubble = (g, x, y, w, txt, c, tc = "#fff") => { g.fillStyle = c; rr(g, x, y, w, 46, 14); g.fill(); g.fillStyle = tc; g.font = FT(800, 17); g.fillText(txt, x + 10, y + 29); };
  TEX.phOff = phone((g, w, h) => { g.fillStyle = "#1E1B18"; g.fillRect(0, 0, w, h); });
  TEX.phSales = phone((g, w) => { for (let k = 0; k < 4; k++) { g.fillStyle = "#EAF6EE"; rr(g, 8, 46 + k * 62, w - 16, 54, 12); g.fill(); g.fillStyle = "#3FA372"; g.font = FT(800, 17); g.fillText("New order", 18, 70 + k * 62); g.fillStyle = "#1E1B18"; g.font = MONO(15); g.fillText("+$97.00", 18, 90 + k * 62); } });
  TEX.phPrice = phone((g, w) => { g.fillStyle = "#EFE6D6"; g.fillRect(0, 34, w, 170); g.fillStyle = "#E8735A"; g.beginPath(); g.arc(60, 120, 30, 0, Math.PI * 2); g.fill(); g.fillStyle = "#1E1B18"; g.font = MONO(13); g.fillText("@maya.makes", 10, 236); g.fillStyle = "#D45C40"; g.font = FT(800, 26); g.fillText("PRICE", 10, 270); });
  TEX.phReply = phone((g, w) => { bubble(g, 52, 50, 96, "PRICE", "#EFE6D6", "#1E1B18"); bubble(g, 8, 110, 140, "It's $97, link ->", "#E8735A"); g.fillStyle = "#3FA372"; g.font = MONO(12); g.fillText("replied in 2 sec", 10, 180); });
  TEX.phObj = phone((g, w) => { bubble(g, 8, 60, 140, "too expensive...", "#EFE6D6", "#1E1B18"); });
  TEX.phStory = phone((g, w) => { bubble(g, 8, 50, 140, "too expensive...", "#EFE6D6", "#1E1B18"); g.fillStyle = "#E8735A"; rr(g, 8, 110, 140, 120, 14); g.fill(); g.fillStyle = "#fff"; g.font = FT(800, 16); g.fillText("Jordan's story", 18, 136); g.font = FT(700, 14); g.fillText("0 -> 1,000", 18, 160); g.fillText("followers", 18, 178); });
  TEX.phPaid = phone((g, w) => { g.fillStyle = "#3FA372"; rr(g, 12, 80, w - 24, 130, 18); g.fill(); g.fillStyle = "#fff"; g.font = FT(800, 30); g.fillText("PAID", 30, 140); g.font = MONO(18); g.fillText("$97.00", 30, 180); });
  TEX.phLink = phone((g, w) => { g.fillStyle = "#1E1B18"; g.font = FT(800, 18); g.fillText("The Course", 12, 80); g.fillStyle = "#E4D9C7"; for (let k = 0; k < 4; k++) g.fillRect(12, 100 + k * 22, w - 24, 10); g.fillStyle = "#E8735A"; rr(g, 12, 210, w - 24, 44, 22); g.fill(); g.fillStyle = "#fff"; g.font = FT(800, 16); g.fillText("Buy $97", 46, 238); });
  TEX.phFollow = phone((g, w) => { bubble(g, 8, 60, 140, "still thinking?", "#E8735A"); bubble(g, 8, 116, 140, "here's 1 tip ->", "#E8735A"); });
  TEX.phPay = phone((g, w) => { g.fillStyle = "#1E1B18"; g.font = FT(800, 18); g.fillText("Coaching", 12, 80); g.font = FT(800, 30); g.fillText("$497", 12, 120); g.fillStyle = "#3A7BD5"; rr(g, 12, 210, w - 24, 44, 22); g.fill(); g.fillStyle = "#fff"; g.font = FT(800, 16); g.fillText("Pay now", 44, 238); });
  TEX.phNo = phone((g, w) => { bubble(g, 8, 60, 140, "not the right fit", "#EFE6D6", "#1E1B18"); bubble(g, 8, 116, 140, "for you, yet :)", "#EFE6D6", "#1E1B18"); });
  TEX.holoKeys = text(256, 100, (g, w, h) => { g.clearRect(0, 0, w, h); g.strokeStyle = "#9FF0FF"; g.lineWidth = 3; rr(g, 4, 4, w - 8, h - 8, 10); g.stroke(); for (let i = 0; i < 10; i++) for (let j = 0; j < 3; j++) { g.fillStyle = "rgba(159,240,255,.55)"; g.fillRect(14 + i * 23, 14 + j * 26, 18, 20); } });
  for (let k = 0; k < 3; k++) TEX["holoChat" + k] = text(256, 180, (g, w, h) => { g.clearRect(0, 0, w, h); g.fillStyle = "rgba(60,180,220,.25)"; rr(g, 2, 2, w - 4, h - 4, 14); g.fill(); g.strokeStyle = "#9FF0FF"; g.lineWidth = 3; g.stroke(); for (let j = 0; j < 3; j++) { g.fillStyle = j % 2 ? "rgba(255,253,248,.85)" : "rgba(232,115,90,.9)"; rr(g, j % 2 ? 80 : 14, 18 + j * 52, 160, 38, 12); g.fill(); } g.fillStyle = "#9FF0FF"; g.font = MONO(18); g.fillText("SENT ✓", 150, 172); });
  TEX.bq = text(400, 176, (g, w, h) => { g.clearRect(0, 0, w, h); g.fillStyle = "#fff"; g.font = FT(800, 110); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("PRICE", w / 2, h / 2 + 6); });
  TEX.br = text(400, 176, (g, w, h) => { g.clearRect(0, 0, w, h); g.fillStyle = "#E8735A"; g.font = FT(800, 84); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("$97 \u2192", w / 2, h / 2 + 4); });
  TEX.sale = text(300, 120, (g, w, h) => { g.clearRect(0, 0, w, h); g.fillStyle = "#3FA372"; rr(g, 4, 4, w - 8, h - 8, 56); g.fill(); g.fillStyle = "#fff"; g.font = FT(800, 66); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("+$97", w / 2, h / 2 + 4); });
  TEX.paid = text(320, 124, (g, w, h) => { g.clearRect(0, 0, w, h); g.fillStyle = "#3FA372"; rr(g, 4, 4, w - 8, h - 8, 58); g.fill(); g.fillStyle = "#fff"; g.font = FT(800, 58); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("PAID \u2713", w / 2, h / 2 + 4); });
  TEX.link = pix(12, 12, (g) => { px(g, "#E8735A", 1, 1, 10, 10); px(g, "#FFFDF8", 2, 5, 3, 2); px(g, "#FFFDF8", 7, 5, 3, 2); px(g, "#FFFDF8", 4, 3, 1, 1); px(g, "#FFFDF8", 7, 8, 1, 1); px(g, "#FFFDF8", 5, 5, 2, 1); });
  TEX.botChest = pix(12, 9, (g) => { px(g, "#101425", 0, 0, 12, 9); const M = "#7FFFD4"; px(g, M, 6, 1, 1, 1); px(g, M, 5, 2, 3, 1); px(g, M, 5, 3, 1, 1); px(g, M, 5, 4, 3, 1); px(g, M, 7, 5, 1, 1); px(g, M, 5, 6, 3, 1); px(g, M, 6, 7, 1, 1); });
  TEX.heart = pix(9, 8, (g) => { const R = "#E8735A"; [[1, 0, 2], [5, 0, 2], [0, 1, 4], [4, 1, 5], [0, 2, 9], [0, 3, 9], [1, 4, 7], [2, 5, 5], [3, 6, 3], [4, 7, 1]].forEach(([x, y, w]) => px(g, R, x, y, w, 1)); px(g, "#FFD0C4", 1, 1, 1, 1); px(g, "#FFD0C4", 2, 2, 1, 1); });
  TEX.z = pix(7, 7, (g) => { px(g, "#FFFDF8", 0, 0, 7, 2); px(g, "#FFFDF8", 4, 2, 2, 1); px(g, "#FFFDF8", 3, 3, 2, 1); px(g, "#FFFDF8", 2, 4, 2, 1); px(g, "#FFFDF8", 0, 5, 7, 2); });
  const bc = document.createElement("canvas"); bc.width = 860; bc.height = 420; TEX.billC = bc; TEX.billG = bc.getContext("2d");
  TEX.billT = new THREE.CanvasTexture(bc); TEX.billT.colorSpace = THREE.SRGBColorSpace; billM.map = TEX.billT; billM.needsUpdate = true;
  for (const [m, key] of LATE) { if (TEX[key]) { m.map = TEX[key]; m.needsUpdate = true; } }
  drawBill(0);
}

const ready = (async () => {
  try { await Promise.all([document.fonts.load("800 40px Manrope"), document.fonts.load("700 30px JBMono")]); } catch (e) { /* fall back */ }
  buildTextures();
  scene.traverse((o) => { if (o.isInstancedMesh) o.frustumCulled = false; });
  for (const k in CAST) for (const m of CAST[k].parts) m.frustumCulled = false;
  renderer.compile(scene, camera);
  renderAt(window.CLOSER_COVER ? window.CLOSER_COVER.t : (window.__hfThreeTime || 0));
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["closer"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(window.CLOSER_COVER ? window.CLOSER_COVER.t : e.detail.time));
window.CLOSER_DEBUG = { HEADW, CAST, renderAt };
