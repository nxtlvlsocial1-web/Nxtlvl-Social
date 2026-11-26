// AI.NXTLVL "The advisor strategy" (9:16). The 3D stage is a pure function of time t (rendered on HyperFrames' hf-seek).
// Beats come from window.AD_T (build/generate.py, from the voice's word times). Layout grid, all centred: headline band
// (HTML, y 300-560), 3D stage (~y 650-1350), live caption (y ~1450).
// The cast (both original AI.NXTLVL characters):
//   Nyx      a small robot with the page's violet star on its antenna: the small, fast model that does the work
//   Advisor  a big glass four-point star with eyes: Opus, which never types and only beams down at the hard parts
// Scenes: hook (two score bars, 19.7% -> 41.2%), same (Nyx asks for help), work (code / terminal / files panels),
// gates (keyboard, then three checkpoints the Advisor lights), command (/advisor opus terminal), tests (score and cost),
// share (a paper plane), cta.
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";

const W = 1080, H = 1920;
const T = window.AD_T;
const VIOLET = 0x7a2ffb, LAV = 0xb687f9, GREEN = 0x3ddc84, GOLD = 0xffc23d;
const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H, false); renderer.setPixelRatio(1);
renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping;
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(32, W / H, .1, 100);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), .04).texture; scene.environmentIntensity = .55;
const composer = new EffectComposer(renderer);
composer.setSize(W, H); composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), .22, .4, .92); composer.addPass(bloom); composer.addPass(new OutputPass());
scene.add(new THREE.HemisphereLight(0xf1eaff, 0x1a1030, .8));
const key = new THREE.DirectionalLight(0xffffff, 1.5); key.position.set(-3, 7, 8); scene.add(key);
const rim = new THREE.PointLight(VIOLET, 60, 22); rim.position.set(3, 3, -3); scene.add(rim);

// ---------------------------------------------------------------- helpers
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const win = (t, a, b) => clamp((t - a) / (b - a));
const ease = (x) => 1 - Math.pow(1 - clamp(x), 3);
const easeIO = (x) => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const back = (x) => { x = clamp(x); const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const lerp = (a, b, x) => a + (b - a) * x;
const pulse = (t, at, w = .25) => Math.exp(-Math.pow((t - at) / w, 2));
const rnd = (i, k = 1) => { const s = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return s - Math.floor(s); };
const life = (t, a, b) => easeIO(win(t, a - .05, a + .4)) * (1 - easeIO(win(t, b - .3, b)));
const $ = (id) => document.getElementById(id);
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const v3 = new THREE.Vector3();
function project(obj, local, el, a = null, s = 1) {
  if (!el) return;
  v3.copy(local); if (obj) obj.localToWorld(v3); v3.project(camera);
  el.style.transform = `translate(${(v3.x * .5 + .5) * W}px, ${(-v3.y * .5 + .5) * H}px) translate(-50%, -50%) scale(${Math.max(.001, s)})`;
  if (a !== null) el.style.opacity = clamp(a);
}
function setText(id, s) { const el = $(id); if (el && el.textContent !== s) el.textContent = s; }
// a vector that moves between keyed spots: keys = [[t, Vector3], ...], each move takes `d` s with ease in-out
function keyed(t, keys, d = .6) {
  let p = keys[0][1].clone();
  for (let k = 1; k < keys.length; k++) { const u = easeIO(win(t, keys[k][0], keys[k][0] + d)); if (u <= 0) break; p.lerp(keys[k][1], u); }
  return p;
}
const lit = (c, i = 1.2) => new THREE.MeshBasicMaterial({ color: new THREE.Color(c).multiplyScalar(i), transparent: true, toneMapped: false });
const plastic = (c, r = .32) => new THREE.MeshPhysicalMaterial({ color: c, roughness: r, clearcoat: .9, clearcoatRoughness: .15 });
const S = (g, s) => g.scale.setScalar(Math.max(.001, s));
function star4(r1, r2) {               // the brand's four-point star
  const sh = new THREE.Shape();
  for (let k = 0; k < 8; k++) { const r = k % 2 ? r2 : r1, a = Math.PI / 2 + k * Math.PI / 4; k ? sh.lineTo(Math.cos(a) * r, Math.sin(a) * r) : sh.moveTo(Math.cos(a) * r, Math.sin(a) * r); }
  return sh;
}

// ---------------------------------------------------------------- floor: a soft violet disc with a grid ring
const floor = new THREE.Mesh(new THREE.CircleGeometry(3.4, 64), new THREE.MeshPhysicalMaterial({ color: 0x150a2e, roughness: .6, metalness: .1, transparent: true, opacity: .9 }));
floor.rotation.x = -Math.PI / 2; floor.position.y = -1.3; scene.add(floor);
const ring = new THREE.Mesh(new THREE.RingGeometry(3.25, 3.3, 96), lit(LAV, .8)); ring.rotation.x = -Math.PI / 2; ring.position.y = -1.29; scene.add(ring);

// ---------------------------------------------------------------- Nyx
const nyx = new THREE.Group(); scene.add(nyx);
const nyxIn = new THREE.Group(); nyx.add(nyxIn);                 // bounce / lean
const bodyM = plastic(VIOLET, .28);
{ const b = new THREE.Mesh(new THREE.CapsuleGeometry(.34, .32, 8, 24), bodyM); b.position.y = .62; nyxIn.add(b);
  const belly = new THREE.Mesh(new THREE.CircleGeometry(.12, 32), lit(LAV, 1.1)); belly.position.set(0, .64, .345); nyxIn.add(belly);
  for (const x of [-.15, .15]) { const l = new THREE.Mesh(new THREE.CapsuleGeometry(.085, .12, 6, 12), plastic(0x2a1a55)); l.position.set(x, .14, 0); nyxIn.add(l); } }
const head = new THREE.Group(); head.position.y = 1.32; nyxIn.add(head);
head.add(new THREE.Mesh(new RoundedBoxGeometry(.92, .74, .72, 6, .26), plastic(0xf1ecff, .25)));
{ const visor = new THREE.Mesh(new RoundedBoxGeometry(.76, .48, .1, 5, .16), new THREE.MeshPhysicalMaterial({ color: 0x0d0720, roughness: .15, clearcoat: 1 })); visor.position.z = .33; head.add(visor);
  const ant = new THREE.Mesh(new THREE.CylinderGeometry(.018, .018, .3, 8), plastic(0xd9d0f5)); ant.position.y = .5; head.add(ant); }
const eyeGeo = new THREE.CapsuleGeometry(.055, .1, 6, 12), eyeM = lit(0xe9ddff, 1.25);
const eyes = [-.16, .16].map((x) => { const e = new THREE.Mesh(eyeGeo, eyeM); e.position.set(x, .01, .39); head.add(e); return e; });
const antStar = new THREE.Mesh(new THREE.ExtrudeGeometry(star4(.14, .045), { depth: .04, bevelEnabled: true, bevelThickness: .015, bevelSize: .012, bevelSegments: 2 }), new THREE.MeshPhysicalMaterial({ color: VIOLET, emissive: VIOLET, emissiveIntensity: .7, roughness: .2, clearcoat: 1 }));
antStar.geometry.center(); antStar.position.y = .72; head.add(antStar);
const arms = [-1, 1].map((sd) => { const g = new THREE.Group(); g.position.set(sd * .4, .86, 0); nyxIn.add(g);
  const a = new THREE.Mesh(new THREE.CapsuleGeometry(.07, .26, 6, 12), bodyM); a.position.y = -.2; g.add(a);
  const hnd = new THREE.Mesh(new THREE.SphereGeometry(.085, 16, 12), plastic(0xf1ecff)); hnd.position.y = -.4; g.add(hnd); return g; });
// pose: lift 0..1 per arm (0 = down, 1 = straight up), mood: eyes (1 open, .25 squint/happy), lean
function pose(t, o) {
  arms[0].rotation.z = -(.12 + o.l * 2.9); arms[1].rotation.z = .12 + o.r * 2.9;
  arms[0].rotation.x = o.fx || 0; arms[1].rotation.x = o.fx || 0;
  const blink = 1 - .9 * Math.max(pulse(t, Math.floor(t / 2.7) * 2.7 + 1.9, .05), 0);
  eyes.forEach((e) => { e.scale.set(1, Math.max(.12, o.eye * blink), 1); e.position.y = .01 + (o.eyeY || 0); });
  head.rotation.set(o.nod || 0, o.turn || 0, o.tilt || 0);
  nyxIn.position.y = o.hop || 0; nyxIn.rotation.z = o.lean || 0;
}

// ---------------------------------------------------------------- the Advisor (Opus)
const adv = new THREE.Group(); scene.add(adv);
const advStar = new THREE.Mesh(new THREE.ExtrudeGeometry(star4(.9, .3), { depth: .32, bevelEnabled: true, bevelThickness: .12, bevelSize: .09, bevelSegments: 4 }),
  new THREE.MeshPhysicalMaterial({ color: 0xc9a8ff, metalness: .1, roughness: .08, transmission: .55, thickness: .8, iridescence: .6, clearcoat: 1, emissive: 0x5a1fd0, emissiveIntensity: .35 }));
advStar.geometry.center(); adv.add(advStar);
const core = new THREE.Mesh(new THREE.SphereGeometry(.22, 24, 16), lit(0xd8c2ff, 1.3)); adv.add(core);
const aEyes = [-.17, .17].map((x) => { const e = new THREE.Mesh(new THREE.CapsuleGeometry(.05, .08, 6, 12), lit(0xffffff, 1.2)); e.position.set(x, .06, .3); adv.add(e); return e; });
const halo = new THREE.Mesh(new THREE.TorusGeometry(1.15, .025, 8, 96), lit(LAV, 1.0)); halo.rotation.x = Math.PI / 2.3; adv.add(halo);
const beam = new THREE.Mesh(new THREE.CylinderGeometry(.08, .32, 1, 40, 1, true), new THREE.MeshBasicMaterial({ color: 0xa77bff, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false }));
scene.add(beam);
const orb = new THREE.Mesh(new THREE.SphereGeometry(.09, 16, 12), lit(0xffffff, 1.4)); scene.add(orb);
function beamTo(from, to, a, t, tStart) {
  const len = from.distanceTo(to); beam.visible = a > .01;
  beam.position.copy(from).lerp(to, .5); beam.scale.set(1, len, 1); beam.lookAt(to); beam.rotateX(Math.PI / 2);
  beam.material.opacity = a * (.22 + .06 * Math.sin(t * 18));
  const u = win(t, tStart, tStart + .45); orb.visible = a > .01 && u > 0 && u < 1; orb.position.copy(from).lerp(to, ease(u));
}

// ---------------------------------------------------------------- hook: two score bars
const bars = new THREE.Group(); scene.add(bars);
const barA = new THREE.Mesh(new RoundedBoxGeometry(.7, 1, .7, 4, .08), plastic(0x5b5378)); barA.geometry.translate(0, .5, 0); barA.position.set(-1.15, -1.3, 0); bars.add(barA);
const barB = new THREE.Mesh(new RoundedBoxGeometry(.7, 1, .7, 4, .08), plastic(VIOLET, .22)); barB.geometry.translate(0, .5, 0); barB.position.set(-.3, -1.3, 0); bars.add(barB);
const BAR_H = 2.45;  // height of 41.2 %

// ---------------------------------------------------------------- work: three floating panels
function panel(w, h, c = 0x0f0a1f) { const g = new THREE.Group(); g.add(new THREE.Mesh(new RoundedBoxGeometry(w, h, .06, 4, .06), plastic(c, .3)));
  const bar = new THREE.Mesh(new THREE.PlaneGeometry(w - .06, .09), new THREE.MeshBasicMaterial({ color: 0x241a42 })); bar.position.set(0, h / 2 - .08, .035); g.add(bar);
  [0xff5f57, 0xfebc2e, 0x28c840].forEach((cc, k) => { const d = new THREE.Mesh(new THREE.CircleGeometry(.022, 16), new THREE.MeshBasicMaterial({ color: cc })); d.position.set(-w / 2 + .08 + k * .07, h / 2 - .08, .04); g.add(d); });
  scene.add(g); return g; }
const pCode = panel(1.25, .85), pTerm = panel(1.25, .75), pFiles = new THREE.Group(); scene.add(pFiles);
const codeLines = [...Array(6)].map((_, r) => { const w = .3 + rnd(r, 9) * .7, m = new THREE.Mesh(new THREE.PlaneGeometry(1, .055), new THREE.MeshBasicMaterial({ color: [0xb687f9, 0x7dd3fc, 0xf9a8d4, 0xe2e8f0][r % 4] }));
  m.geometry.translate(.5, 0, 0); m.position.set(-.5 + (r % 3 ? .08 : 0), .24 - r * .1, .035); m.userData.w = w; pCode.add(m); return m; });
const termLines = [...Array(4)].map((_, r) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(1, .05), new THREE.MeshBasicMaterial({ color: r === 3 ? GREEN : 0x8b84a8 }));
  m.geometry.translate(.5, 0, 0); m.position.set(-.52, .2 - r * .12, .035); m.userData.w = r === 3 ? .55 : .5 + rnd(r, 4) * .4; pTerm.add(m); return m; });
const files = [...Array(4)].map((_, k) => { const f = new THREE.Mesh(new RoundedBoxGeometry(.62, .8, .025, 3, .03), plastic(0xf4f1ff, .4)); pFiles.add(f);
  for (let r = 0; r < 4; r++) { const ln = new THREE.Mesh(new THREE.PlaneGeometry(.38 - (r % 2) * .1, .035), new THREE.MeshBasicMaterial({ color: 0xbfb6dc })); ln.position.set(-.05, .22 - r * .1, .015); f.add(ln); }
  return f; });

// ---------------------------------------------------------------- gates: a keyboard, then three checkpoints
const kb = new THREE.Group(); scene.add(kb);
kb.add(new THREE.Mesh(new RoundedBoxGeometry(1.7, .1, .62, 3, .04), plastic(0x231642)));
const KN = 36, keys = new THREE.InstancedMesh(new RoundedBoxGeometry(.15, .07, .15, 2, .025), plastic(0xe9e3ff, .4), KN); kb.add(keys);
const gates = [-1.4, 0, 1.4].map((x) => { const g = new THREE.Group(); g.position.set(x, -1.3, 0); scene.add(g);
  const arch = new THREE.Mesh(new THREE.TorusGeometry(.55, .07, 12, 48, Math.PI), plastic(0x3a2a66)); g.add(arch);
  const glowA = new THREE.Mesh(new THREE.TorusGeometry(.55, .085, 12, 48, Math.PI), lit(LAV, 1.3)); glowA.material.opacity = 0; g.add(glowA); g.userData.glow = glowA; return g; });

// ---------------------------------------------------------------- command: the terminal slab
const term = new THREE.Group(); scene.add(term);
term.add(new THREE.Mesh(new RoundedBoxGeometry(2.7, 1.45, .14, 5, .1), plastic(0x0d0820, .25)));
{ const tb = new THREE.Mesh(new THREE.PlaneGeometry(2.6, .16), new THREE.MeshBasicMaterial({ color: 0x1f1638 })); tb.position.set(0, .62, .075); term.add(tb);
  [0xff5f57, 0xfebc2e, 0x28c840].forEach((cc, k) => { const d = new THREE.Mesh(new THREE.CircleGeometry(.035, 16), new THREE.MeshBasicMaterial({ color: cc })); d.position.set(-1.2 + k * .1, .62, .08); term.add(d); }); }

// ---------------------------------------------------------------- tests: score bars + coin stacks
const tests = new THREE.Group(); scene.add(tests);
const sBarA = new THREE.Mesh(new RoundedBoxGeometry(.5, 1, .5, 4, .06), plastic(0x5b5378)); sBarA.geometry.translate(0, .5, 0); sBarA.position.set(-1.45, -1.3, 0); tests.add(sBarA);
const sBarB = new THREE.Mesh(new RoundedBoxGeometry(.5, 1, .5, 4, .06), plastic(VIOLET, .22)); sBarB.geometry.translate(0, .5, 0); sBarB.position.set(.05, -1.3, 0); tests.add(sBarB);
const coinGeo = new THREE.CylinderGeometry(.2, .2, .06, 32), CN = 19, coins = new THREE.InstancedMesh(coinGeo, new THREE.MeshPhysicalMaterial({ color: GOLD, metalness: .9, roughness: .25 }), CN); tests.add(coins);

// ---------------------------------------------------------------- share: a paper plane
const plane = new THREE.Group(); scene.add(plane);
{ const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute([0, 0, .5, -.32, 0, -.3, 0, -.05, -.2, 0, 0, .5, 0, -.05, -.2, .32, 0, -.3], 3)); g.computeVertexNormals();
  plane.add(new THREE.Mesh(g, new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: .5, side: THREE.DoubleSide }))); }
const TRN = 14, trail = new THREE.InstancedMesh(new THREE.SphereGeometry(.035, 8, 6), lit(LAV, 1.1), TRN); scene.add(trail);
const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), sc = new THREE.Vector3();

// ---------------------------------------------------------------- per frame
function renderAt(t) {
  const sHook = life(t, -1, T.same), sSame = life(t, T.same, T.trick), sWork = life(t, T.trick, T.big), sGate = life(t, T.big, T.strategy),
    sCmd = life(t, T.strategy, T.tests), sTest = life(t, T.tests, T.send), sShare = life(t, T.send, T.cta), sCta = life(t, T.cta, 999);

  // camera: a slow orbit, re-framed per scene
  // [time, distance, x]; the look height puts the floor at 1340 px for that distance (px per unit k = 960 / (D tan 16deg))
  const camK = [[-1, V(14, 0, 0)], [T.same, V(9.5, 0, 0)], [T.trick, V(12, 0, 0)], [T.big, V(10, 0, 0)], [T.plan - .5, V(14, 0, 0)],
    [T.strategy, V(11.5, 0, 0)], [T.tests, V(14, 0, 0)], [T.send, V(9.5, 0, 0)], [T.cta, V(12, 0, 0)]];
  const ck = keyed(t, camK, .7), D = ck.x, kpx = 960 / (D * .2867), ly = -1.3 + 380 / kpx, yaw = Math.sin(t * .33) * .06;
  camera.position.set(Math.sin(yaw) * D, ly + .45 + Math.sin(t * .27) * .04, Math.cos(yaw) * D);
  camera.lookAt(0, ly, 0); camera.updateMatrixWorld(true);

  // ------------------------------------------------ Nyx: where it stands and how it feels
  const walk = win(t, T.plan - .6, T.done + .7);
  const nyxK = [[-1, V(.95, -1.3, .4)], [T.same, V(-.2, -1.3, .4)], [T.trick, V(0, -1.3, 0)], [T.big, V(0, -1.3, .9)],
    [T.plan - .6, V(-2.0, -1.3, .5)], [T.strategy, V(1.2, -1.3, 1.4)], [T.tests, V(1.65, -1.3, .4)], [T.send, V(0, -1.3, .3)], [T.cta, V(-1.0, -1.3, .3)]];
  let np = keyed(t, nyxK, .6);
  if (t >= T.plan - .6 && t < T.strategy) {                       // walking through the three gates
    const xs = [-2.0, -1.4, 0, 1.4, 1.9], ts = [T.plan - .6, T.plan, T.error, T.done, T.done + .8];
    let x = xs[0]; for (let k = 1; k < xs.length; k++) x = lerp(x, xs[k], easeIO(win(t, ts[k] - .55, ts[k])));
    np = V(x, -1.3, .5);
  }
  nyx.position.copy(np); S(nyx, Math.max(sHook, sSame, sWork, sGate, sCmd * .8, sTest * .75, sShare, sCta) * (.95));
  nyx.rotation.y = Math.sin(t * .8) * .12 + (sCmd > .5 ? -.5 : 0) + (sTest > .5 ? -.35 : 0);
  const sad = sHook * (1 - win(t, T.jumps - .2, T.jumps + .1)), cheer = pulse(t, T.jumps + .35, .45) + pulse(t, T.higher + .2, .35) + pulse(t, T.kw + .2, .4);
  const ask = win(t, T.ask - .5, T.ask) * (1 - win(t, T.trick - .4, T.trick));
  const typing = Math.max(sWork, win(t, T.big - .1, T.big + .2) * (1 - win(t, T.plan - .9, T.plan - .5)));
  const throwA = win(t, T.send - .1, T.send + .25) * (1 - win(t, T.send + .7, T.send + 1.1));
  const wave = sCta * (.5 + .5 * Math.sin(t * 9));
  pose(t, {
    l: clamp(cheer * .9 + typing * (.32 + .1 * Math.sin(t * 26)) + sCta * .1),
    r: clamp(cheer * .9 + ask * .95 + typing * (.32 + .1 * Math.sin(t * 26 + 2)) + throwA * 1.0 + wave * .85),
    fx: -typing * .9,
    eye: lerp(1, .55, sad) * (cheer > .4 ? .35 : 1),
    eyeY: -.04 * sad, nod: .18 * sad + .22 * typing, tilt: .18 * ask - .1 * sad, turn: ask * .25,
    hop: Math.abs(Math.sin(t * 9)) * .18 * clamp(cheer) + (walk > 0 && walk < 1 ? Math.abs(Math.sin(t * 12)) * .05 : 0),
    lean: Math.sin(t * 2) * .03,
  });
  project(nyx, V(0, -.22, 0), $("nyxTag"), Math.max(sHook, sTest));
  setText("nyxTag", sTest > .5 ? "SONNET" : "HAIKU");
  project(nyx, V(.6, 1.95, 0), $("qmark"), ask, back(win(t, T.ask - .5, T.ask)));

  // ------------------------------------------------ the Advisor
  const advIn = Math.max(win(t, T.give - .25, T.give + .35) * sHook, sSame, sGate, win(t, T.slash + .6, T.slash + 1) * sCmd, sTest, sCta);
  const advK = [[-1, V(1.3, 1.2, -.2)], [T.same, V(1.0, .7, -.3)], [T.trick, V(2.6, 3.0, -1)], [T.big, V(0, .85, -.3)], [T.plan - .5, V(0, 1.15, -.4)],
    [T.strategy, V(-1.15, 1.35, -.3)], [T.tests, V(1.65, 1.05, -.3)], [T.send, V(2.6, 3.0, -1)], [T.cta, V(1.1, .2, -.2)]];
  const ap = keyed(t, advK, .6);
  if (t >= T.plan - .5 && t < T.strategy) ap.x = lerp(ap.x, nyx.position.x, .7);
  ap.y += Math.sin(t * 1.6) * .08 + (1 - ease(win(t, T.give - .25, T.give + .35))) * 3 * (t < T.same ? 1 : 0);
  adv.position.copy(ap); adv.visible = advIn > .01; S(adv, back(advIn) * (sCta > .5 ? .7 : .48));
  advStar.rotation.y = Math.sin(t * .9) * .35; halo.rotation.z = t * .8; core.scale.setScalar(1 + .15 * Math.sin(t * 4));
  const advBlink = 1 - .9 * pulse(t, Math.floor(t / 3.1) * 3.1 + 1.2, .05);
  aEyes.forEach((e) => e.scale.set(1, Math.max(.12, advBlink), 1));
  project(adv, V(0, -1.3, 0), $("advTag"), advIn * (sCmd > .5 || sShare > .5 || sTest > .5 ? 0 : 1));
  // consults: beam from the Advisor down to Nyx
  const consults = [T.give + .2, T.ask + .1, T.plan, T.error, T.done, T.higher - .4];
  let ba = 0, bs = 0; for (const c of consults) { const k = pulse(t, c + .35, .45); if (k > ba) { ba = k; bs = c; } }
  ba *= advIn;
  beamTo(adv.position.clone().add(V(0, -.35, 0)), nyx.position.clone().add(V(0, 1.95 * nyx.scale.x, 0)), ba, t, bs);

  // ------------------------------------------------ hook: bars
  bars.visible = sHook > .01; S(bars, sHook);
  const gA0 = .4 + .6 * ease(win(t, 0, T.scored + .6)), hA = BAR_H * 19.7 / 41.2 * gA0, hB = BAR_H * ease(win(t, T.jumps - .3, T.jumps + .5));
  barA.scale.y = Math.max(.001, hA); barB.scale.y = Math.max(.001, hB); barB.visible = hB > .01;
  setText("pA", (19.7 * gA0).toFixed(1) + "%");
  setText("pB", (41.2 * ease(win(t, T.jumps - .3, T.jumps + .5))).toFixed(1) + "%");
  project(null, V(-1.15, -1.3 + hA + .38, 0), $("lblA"), sHook);
  project(null, V(-.3, -1.3 + hB + .38, 0), $("lblB"), sHook * win(t, T.jumps - .3, T.jumps));
  const srcA = sHook, srcB = sTest; $("srcA").style.opacity = srcA; $("srcB").style.opacity = srcB; $("barTag").style.opacity = 1 - Math.max(srcA, srcB);
  bars.position.x = 0;

  // ------------------------------------------------ work: panels orbit Nyx
  const pw = [[pCode, T.writes, V(-1.15, .75, -.3), .35], [pTerm, T.runs, V(1.15, .3, -.2), -.35], [pFiles, T.reads, V(0, 1.15, -.8), 0]];
  pw.forEach(([g, at, p, ry], k) => { const a = sWork * back(win(t, at - .35, at + .1)); g.visible = a > .01; S(g, a * .78);
    g.position.copy(p).add(V(0, Math.sin(t * 1.5 + k) * .06, 0)); g.rotation.set(0, ry + Math.sin(t * .7 + k) * .06, 0); });
  codeLines.forEach((m, r) => { m.scale.x = Math.max(.001, m.userData.w * ease(win(t, T.writes - .1 + r * .12, T.writes + .15 + r * .12))); });
  termLines.forEach((m, r) => { m.scale.x = Math.max(.001, m.userData.w * ease(win(t, T.runs + r * .14, T.runs + .2 + r * .14))); });
  files.forEach((f, k) => { const u = ease(win(t, T.reads + k * .1, T.reads + .4 + k * .1)); f.position.set((k - 1.5) * .3 * u, 0, -k * .02); f.rotation.set(0, 0, (k - 1.5) * .18 * u); });
  [["p0", pCode, V(0, -.58, 0), T.writes], ["p1", pTerm, V(0, -.52, 0), T.runs], ["p2", pFiles, V(0, .58, 0), T.reads]]
    .forEach(([id, g, l, at]) => project(g, l, $(id), sWork * win(t, at - .2, at + .1)));

  // ------------------------------------------------ gates: keyboard (Nyx types, the Advisor never does), then checkpoints
  const kbA = sGate * (1 - win(t, T.plan - .9, T.plan - .5)) * win(t, T.big - .3, T.big + .1);
  kb.visible = kbA > .01; S(kb, kbA); kb.position.set(0, -.62, 1.45); kb.rotation.x = .35;
  for (let i = 0; i < KN; i++) { const r = Math.floor(i / 12), c = i % 12, dn = Math.max(0, Math.sin(t * 22 + rnd(i) * 9)) > .85 ? -.035 : 0;
    m4.compose(V(-.72 + c * .131, .07 + dn, -.18 + r * .18), q.identity(), sc.setScalar(1)); keys.setMatrixAt(i, m4); }
  keys.instanceMatrix.needsUpdate = true;
  const gA = sGate * win(t, T.plan - .9, T.plan - .4);
  [T.plan, T.error, T.done].forEach((at, k) => { const g = gates[k]; g.visible = gA > .01; S(g, back(win(t, T.plan - .9 + k * .1, T.plan - .4 + k * .1)) * sGate);
    g.userData.glow.material.opacity = win(t, at, at + .25);
    project(g, V(0, 0, .75), $("g" + k), gA * (.35 + .65 * win(t, at - .1, at + .2))); });

  // ------------------------------------------------ command: the terminal
  term.visible = sCmd > .01; S(term, back(sCmd)); term.position.set(0, .35, 0); term.rotation.set(-.04, Math.sin(t * .6) * .04, 0);
  project(term, V(0, .02, .08), $("termTx"), sCmd * win(t, T.strategy - .1, T.strategy + .3));

  // ------------------------------------------------ tests: score + cost
  tests.visible = sTest > .01; S(tests, sTest); tests.position.x = 0;
  const g1 = ease(win(t, T.tests - .1, T.tests + .7)), g2 = ease(win(t, T.higher - .4, T.higher + .3));
  sBarA.scale.y = Math.max(.001, 1.7 * g1); sBarB.scale.y = Math.max(.001, 1.7 * g1 + .4 * g2);
  const cu = ease(win(t, T.cost - .2, T.less + .3));
  for (let i = 0; i < CN; i++) { const right = i >= 10, lvl = right ? i - 10 : i, n = right ? Math.round(10 - 1.19 * cu) : 10;
    const show = lvl < n && g1 > 0;
    m4.compose(V(right ? .65 : -.85, -1.27 + lvl * .07 + (1 - g1) * 1.2, .1), q.identity(), sc.setScalar(show ? 1 : 0)); coins.setMatrixAt(i, m4); }
  coins.instanceMatrix.needsUpdate = true;
  setText("costB", "-" + (11.9 * cu).toFixed(1) + "%");
  project(null, V(-1.15, -1.3 + 1.7 * g1 + .5, 0), $("tA"), sTest * g1);
  project(null, V(.35, -1.3 + 1.7 * g1 + .4 * g2 + .62, 0), $("tB"), sTest * g1);

  // ------------------------------------------------ share: the paper plane
  const fl = win(t, T.send + .2, T.everything + .6);
  plane.visible = sShare > .01 && fl > 0 && fl < 1;
  const pp = (u) => V(lerp(.45, 3.2, u), lerp(-.1, 2.6, u) + Math.sin(u * Math.PI) * .9, lerp(.3, -1.0, u));
  plane.position.copy(pp(ease(fl))); plane.lookAt(pp(clamp(ease(fl) + .02))); S(plane, 1.1);
  for (let i = 0; i < TRN; i++) { const u = clamp(ease(fl) - i * .025); m4.compose(pp(u), q.identity(), sc.setScalar(plane.visible ? (1 - i / TRN) : 0)); trail.setMatrixAt(i, m4); }
  trail.instanceMatrix.needsUpdate = true;

  floor.material.opacity = .9 * Math.max(1 - sCmd, .0); ring.material.opacity = .8 * (1 - sCmd);
  bloom.strength = .22 + ba * .12;
  composer.render();
}

const ready = (async () => {
  try { await Promise.all(["900 40px Mont", "800 40px Mont", "700 40px Inter", "700 40px Mono"].map((f) => document.fonts.load(f))); } catch (e) { /* fallback */ }
  renderer.compile(scene, camera); renderAt(window.__hfThreeTime || 0);
})();
window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["scene"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
