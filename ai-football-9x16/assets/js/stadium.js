// AI Football Club reel: the 3D stadium. A cream low-poly stadium on a floating tile, managed by one AI (the coral orb
// above it) for a season. Everything is a pure function of time t (seconds), drawn on HyperFrames' hf-seek. Cue times
// come from the voice (window.CT, written by build/generate.py). Story, peak by peak:
//   hook      the star sits on the bench, the crowd boos (grey, swaying)
//   4-0       a fast-forwarded match: four goals; then tracking rings under every player
//   week 3    a 17-year-old walks out of the tunnel and scores on debut
//   half-time 0-2 down, the formation rewires (graph lines, heart-rate pulses), three goals
//   Christmas snow, top of the league, the crowd chants in a coral wave
//   January   the captain walks off, sold; the cup final at night: he scores the winner, in the other kit, slow motion
//   real      a corner-kick tactic drawn on the pitch (TacticAI), from above
//   close     the whole stadium, small, under the orb
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";

const C = window.CT;
const L = C.l, E = C.e, DUR = C.end;
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
const M4 = new THREE.Matrix4(), Q = new THREE.Quaternion(), V = new THREE.Vector3(), V2 = new THREE.Vector3(), S = new THREE.Vector3();
const UP = new THREE.Vector3(0, 1, 0);
const pulse = (t, a, w = .35) => Math.exp(-(((t - a) / w) ** 2));
const INK = 0x1E1B18, CORAL = 0xE8735A, NAVY = 0x34508F, CREAM = 0xFFFDF8, GOLD = 0xF2B33D;

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
scene.background = col(0xF1E9DC);
scene.fog = new THREE.Fog(0xF1E9DC, 60, 130);
const camera = new THREE.PerspectiveCamera(40, W / H, .1, 300);

const rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });
const composer = new EffectComposer(renderer, rt);
composer.setPixelRatio(1);
composer.setSize(W, H);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), .25, .5, .9);
composer.addPass(bloom);
composer.addPass(new OutputPass());
const grade = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uSat: { value: 1 }, uVig: { value: .28 }, uFlash: { value: 0 }, uWarm: { value: 0 } },
  vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }",
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime, uSat, uVig, uFlash, uWarm; varying vec2 vUv;
    float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
    void main(){
      vec3 c = texture2D(tDiffuse, vUv).rgb;
      float g = dot(c, vec3(.299, .587, .114));
      c = mix(vec3(g), c, uSat);
      c = mix(c, c * vec3(1.08, 1.0, .9), uWarm);
      vec2 q = vUv - .5; c *= 1. - dot(q, q) * uVig * 2.2;
      c += (h(floor(vUv * vec2(1080., 1920.)) + fract(uTime * 7.13) * 97.) - .5) * .026;
      c = mix(c, vec3(1., .99, .96), uFlash);
      gl_FragColor = vec4(c, 1.);
    }`,
});
composer.addPass(grade);

// ---------------------------------------------------------------- lights
const hemi = new THREE.HemisphereLight(0xfff6ea, 0xcdbfa8, .95);
scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff1dc, 2.1);
sun.position.set(14, 26, 12);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, { left: -22, right: 22, top: 22, bottom: -22, near: 1, far: 80 });
sun.shadow.bias = -.0006;
sun.shadow.normalBias = .03;
scene.add(sun, sun.target);

const mat = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: .88, metalness: 0, ...o });
const add = (m, cast = true, recv = true) => { m.castShadow = cast; m.receiveShadow = recv; scene.add(m); return m; };

// ---------------------------------------------------------------- the ground: tile, pitch, lines, goals
const PX = 6.5, PZ = 10;            // pitch half sizes
add(new THREE.Mesh(new RoundedBoxGeometry(30, 1.4, 36, 4, .6), mat(0xEADFCB)), false, true).position.set(0, -.7, 0);
const edge = new THREE.Mesh(new RoundedBoxGeometry(30.3, .5, 36.3, 4, .25), mat(INK, { roughness: .6 }));
edge.position.set(0, -1.3, 0);
scene.add(edge);
// grass in mown stripes
for (let k = 0; k < 10; k++) {
  const s = add(new THREE.Mesh(new THREE.BoxGeometry(2 * PX + 1.4, .05, (2 * PZ + 1.6) / 10), mat(k % 2 ? 0x9CC18F : 0xA9CC9B)), false, true);
  s.position.set(0, .025, -PZ - .8 + (k + .5) * (2 * PZ + 1.6) / 10);
}
const lineM = new THREE.MeshBasicMaterial({ color: CREAM });
const lineBox = (w, d, x, z) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, .02, d), lineM); m.position.set(x, .062, z); scene.add(m); };
lineBox(2 * PX, .1, 0, -PZ); lineBox(2 * PX, .1, 0, PZ); lineBox(.1, 2 * PZ, -PX, 0); lineBox(.1, 2 * PZ, PX, 0); lineBox(2 * PX, .1, 0, 0);
for (const sz of [-1, 1]) {
  lineBox(6.4, .1, 0, sz * (PZ - 3)); lineBox(.1, 3, -3.2, sz * (PZ - 1.5)); lineBox(.1, 3, 3.2, sz * (PZ - 1.5));
  lineBox(3, .1, 0, sz * (PZ - 1.1)); lineBox(.1, 1.1, -1.5, sz * (PZ - .55)); lineBox(.1, 1.1, 1.5, sz * (PZ - .55));
}
const circle = new THREE.Mesh(new THREE.RingGeometry(1.75, 1.85, 64), lineM);
circle.rotation.x = -Math.PI / 2; circle.position.y = .063; scene.add(circle);
// goals: frame + soft net
const goalM = mat(CREAM, { roughness: .4 });
const netM = new THREE.MeshStandardMaterial({ color: 0xffffff, transparent: true, opacity: .35, side: THREE.DoubleSide, roughness: .9 });
for (const sz of [-1, 1]) {
  const g = new THREE.Group(); g.position.set(0, 0, sz * PZ); scene.add(g);
  for (const sx of [-1.1, 1.1]) { const p = add(new THREE.Mesh(new THREE.CylinderGeometry(.06, .06, .9, 8).translate(0, .45, 0), goalM)); p.position.x = sx; g.add(p); }
  const bar = add(new THREE.Mesh(new THREE.CylinderGeometry(.06, .06, 2.32, 8), goalM)); bar.rotation.z = Math.PI / 2; bar.position.y = .9; g.add(bar);
  const back = new THREE.Mesh(new THREE.PlaneGeometry(2.2, .9), netM); back.position.set(0, .45, sz * .7); g.add(back);
  const top = new THREE.Mesh(new THREE.PlaneGeometry(2.2, .7), netM); top.rotation.x = Math.PI / 2; top.position.set(0, .9, sz * .35); g.add(top);
}
// corner flags
for (const sx of [-1, 1]) for (const sz of [-1, 1]) {
  const f = add(new THREE.Mesh(new THREE.CylinderGeometry(.025, .025, .6).translate(0, .3, 0), mat(CREAM))); f.position.set(sx * PX, 0, sz * PZ);
  const fl = new THREE.Mesh(new THREE.BoxGeometry(.02, .16, .22), mat(CORAL)); fl.position.set(sx * PX, .52, sz * PZ + .11); scene.add(fl);
}

// ---------------------------------------------------------------- stands, crowd, floodlights
const IX = 8.4, IZ = 12.2, STEP = .75, NSTEP = 4;
const standM = mat(0xF2DCC0);
const FANS = [];
for (let s = 0; s < NSTEP; s++) {
  const x = IX + .2 + s * STEP, z = IZ + .2 + s * STEP, y = .35 + s * .55;
  const sides = [[0, z, 2 * x + STEP, 'n'], [0, -z, 2 * x + STEP, 's'], [x, 0, 2 * z - STEP, 'e'], [-x, 0, 2 * z - STEP, 'w']];
  for (const [cx, cz, len, side] of sides) {
    const along = side === 'n' || side === 's';
    const b = add(new THREE.Mesh(new THREE.BoxGeometry(along ? len : STEP, y * 2, along ? STEP : len), s % 2 ? standM : mat(0xE9D3B3)));
    b.position.set(cx, 0, cz);
    for (let u = -len / 2 + .3; u < len / 2 - .2; u += .34) {
      const fx = along ? u : cx, fz = along ? cz : u;
      if (side === 'e' && Math.abs(fz) < 2.4 && s === 0) continue;       // the dugout gap
      FANS.push({ x: fx, z: fz, y: y * 2 + .14, side, i: FANS.length });
    }
  }
}
const fanM = new THREE.InstancedMesh(new THREE.SphereGeometry(.13, 14, 10), mat(0xffffff, { roughness: .7 }), FANS.length);
fanM.castShadow = false;
scene.add(fanM);
const fanBase = FANS.map((f, i) => (f.side === 's' ? (hash(i) < .75 ? NAVY : (hash(i * 3) < .5 ? CREAM : 0x8fa3c8)) : (hash(i) < .6 ? CORAL : hash(i * 3) < .55 ? CREAM : INK)));
const towers = [];
for (const sx of [-1, 1]) for (const sz of [-1, 1]) {
  const g = new THREE.Group(); g.position.set(sx * 12.6, 0, sz * 16.2); scene.add(g);
  g.add(add(new THREE.Mesh(new THREE.CylinderGeometry(.12, .18, 9, 8).translate(0, 4.5, 0), mat(0xd9cbb2))));
  const lampM = new THREE.MeshStandardMaterial({ color: 0xfff6dc, emissive: 0xfff2c8, emissiveIntensity: .2 });
  const lamp = new THREE.Mesh(new THREE.BoxGeometry(1.6, .9, .25), lampM); lamp.position.set(0, 9.2, 0); lamp.lookAt(0, 0, 0);
  g.add(lamp); towers.push(lampM);
}
// dugout and bench on the east side
// an open dugout: back wall and two side walls; the bench sits in front of the wall
const dugWall = add(new THREE.Mesh(new THREE.BoxGeometry(.2, 1.4, 4.2).translate(0, .7, 0), mat(CREAM)));
dugWall.position.set(8.55, 0, 0);
for (const sz of [-2.05, 2.05]) { const w = add(new THREE.Mesh(new THREE.BoxGeometry(1.1, 1.4, .1).translate(0, .7, 0), mat(CREAM))); w.position.set(8.05, 0, sz); }
const benchSeat = add(new THREE.Mesh(new THREE.BoxGeometry(.45, .3, 3.8).translate(0, .15, 0), mat(CORAL)));
benchSeat.position.set(8.15, 0, 0);
// tunnel (west): a cream frame round a dark opening
const tun = add(new THREE.Mesh(new THREE.BoxGeometry(.3, 1.4, 2.0).translate(0, .7, 0), mat(CREAM)));
tun.position.set(-8.75, 0, 0);
const tunHole = new THREE.Mesh(new THREE.PlaneGeometry(1.3, 1.0), new THREE.MeshBasicMaterial({ color: INK }));
tunHole.rotation.y = Math.PI / 2; tunHole.position.set(-8.58, .5, 0); scene.add(tunHole);

// ---------------------------------------------------------------- the AI: orb and rings above the pitch
const ORB = new THREE.Vector3(0, 11, -1);
const orb = new THREE.Group(); orb.position.copy(ORB); scene.add(orb);
const orbCoreM = new THREE.MeshStandardMaterial({ color: CORAL, emissive: CORAL, emissiveIntensity: 1.1, roughness: .35 });
orb.add(new THREE.Mesh(new THREE.SphereGeometry(.85, 40, 28), orbCoreM));
orb.add(new THREE.Mesh(new THREE.SphereGeometry(1.05, 40, 28), new THREE.MeshStandardMaterial({ color: CREAM, transparent: true, opacity: .25, roughness: .2 })));
const ring1 = new THREE.Mesh(new THREE.TorusGeometry(1.55, .06, 8, 64), mat(INK, { roughness: .5 }));
const ring2 = new THREE.Mesh(new THREE.TorusGeometry(1.95, .045, 8, 64), mat(CORAL, { emissive: CORAL, emissiveIntensity: .5 }));
orb.add(ring1, ring2);

// ---------------------------------------------------------------- players
// home attacks towards z = -10, away towards z = +10. Formations are in home coordinates (own goal at +z).
const F442 = [[0, 9.1], [-4.5, 6], [-1.5, 6.6], [1.5, 6.6], [4.5, 6], [-4.5, 2], [-1.5, 2.6], [1.5, 2.6], [4.5, 2], [-1.6, -2], [1.6, -2]];
const F343 = [[0, 9.1], [-3, 6.4], [0, 6.9], [3, 6.4], [5, 1.4], [-5, 1.4], [-1.8, 2.4], [1.8, 2.4], [3.6, -2.8], [-3.6, -2.8], [0, -3.4]];
const N_HOME = 11, N_AWAY = 11, ID17 = 22, IDCAP = 23, IDSTAR = 24, IDSUB = [25, 26];
const NP = 27;
// every player is built from parts (torso, shorts, two legs, two arms, head, hair) plus a face (eyes, brows, a mouth),
// one instanced mesh per part; legs and arms swing from hip and shoulder pivots as they run
const IM = (geo, m, n = NP, cast = true) => { const x = new THREE.InstancedMesh(geo, m, n); x.castShadow = cast; scene.add(x); return x; };
const basic = (c) => new THREE.MeshBasicMaterial({ color: c });
const torsoM = IM(new THREE.CapsuleGeometry(.19, .26, 6, 16), mat(0xffffff, { roughness: .6 }));
const shortsM = IM(new RoundedBoxGeometry(.37, .17, .25, 2, .05), mat(0xffffff, { roughness: .7 }));
const legM = IM(new THREE.CapsuleGeometry(.068, .24, 4, 10), mat(0xffffff, { roughness: .7 }), NP * 2);
const bootM = IM(new RoundedBoxGeometry(.13, .07, .21, 2, .03), mat(0xffffff, { roughness: .5 }), NP * 2);
const armM = IM(new THREE.CapsuleGeometry(.054, .2, 4, 10), mat(0xffffff, { roughness: .7 }), NP * 2);
const headM = IM(new THREE.SphereGeometry(.17, 28, 20), mat(0xffffff, { roughness: .65 }));
const hairCapM = IM(new THREE.SphereGeometry(.182, 28, 12, 0, Math.PI * 2, 0, Math.PI * .44), mat(0xffffff, { roughness: .95 }));
const hairAfroM = IM(new THREE.SphereGeometry(.205, 24, 16), mat(0xffffff, { roughness: .97 }));
const hairMohM = IM(new RoundedBoxGeometry(.07, .1, .3, 2, .03), mat(0xffffff, { roughness: .95 }));
const eyeM = IM(new THREE.SphereGeometry(.026, 12, 10), basic(INK), NP * 2, false);
const eyeHiM = IM(new THREE.SphereGeometry(.009, 8, 6), basic(0xffffff), NP * 2, false);
const browM = IM(new THREE.BoxGeometry(.075, .017, .02), basic(INK), NP * 2, false);
const mouthArcM = IM(new THREE.TorusGeometry(.046, .012, 6, 16, Math.PI), basic(0x6a2a20), NP, false);
const mouthOM = IM(new THREE.TorusGeometry(.03, .013, 8, 16), basic(0x6a2a20), NP, false);
const armband = new THREE.Mesh(new THREE.TorusGeometry(.07, .022, 6, 18), mat(GOLD, { emissive: GOLD, emissiveIntensity: .3 }));
scene.add(armband);
// what makes each player look like himself: skin, hair style and colour, height, boots
const SKIN = [0xF1C9A5, 0xE3B28E, 0xC68863, 0xA06D4B, 0x7A4E34, 0xF6D7BF];
const HAIRC = [0x1E1B18, 0x4A3222, 0x7A5230, 0xD9B26A, 0xB8572E, 0x8a8580];
const LOOK = Array.from({ length: NP }, (_, i) => ({ skin: SKIN[Math.floor(hash(i * 7 + 1) * 6)], hair: HAIRC[Math.floor(hash(i * 11 + 3) * 6)],
  style: Math.floor(hash(i * 13 + 5) * 4), h: .93 + hash(i * 17) * .14, boot: [INK, CREAM, GOLD, 0x3FA372][Math.floor(hash(i * 19) * 4)] }));
Object.assign(LOOK[IDSTAR], { style: 2, hair: 0xD9B26A, skin: 0xE3B28E, h: 1.06 });     // the star: blonde mohawk
Object.assign(LOOK[IDCAP], { style: 0, hair: 0x1E1B18, skin: 0xC68863, h: 1.08 });      // the captain
Object.assign(LOOK[ID17], { style: 1, hair: 0x1E1B18, skin: 0x7A4E34, h: .95 });       // the 17-year-old
const ringM = new THREE.InstancedMesh(new THREE.RingGeometry(.42, .55, 32).rotateX(-Math.PI / 2), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .9, toneMapped: false, depthWrite: false }), NP);
scene.add(ringM);
const ball = add(new THREE.Mesh(new THREE.SphereGeometry(.14, 18, 12), mat(CREAM, { roughness: .4 })));
const trailM = new THREE.InstancedMesh(new THREE.SphereGeometry(.1, 8, 6), new THREE.MeshBasicMaterial({ color: CREAM, transparent: true, opacity: .5, toneMapped: false }), 8);
scene.add(trailM);
// formation graph lines (home)
const EDGES = [[0, 2], [0, 3], [1, 2], [2, 3], [3, 4], [1, 5], [2, 6], [3, 7], [4, 8], [5, 6], [6, 7], [7, 8], [6, 9], [7, 10], [5, 9], [8, 10], [9, 10]];
const graphPos = new Float32Array(EDGES.length * 6);
const graphG = new THREE.BufferGeometry(); graphG.setAttribute("position", new THREE.BufferAttribute(graphPos, 3));
const graphM = new THREE.LineBasicMaterial({ color: CORAL, transparent: true, opacity: 0, toneMapped: false });
scene.add(new THREE.LineSegments(graphG, graphM));
const beamPos = new Float32Array(N_HOME * 6);
const beamG = new THREE.BufferGeometry(); beamG.setAttribute("position", new THREE.BufferAttribute(beamPos, 3));
const beamM = new THREE.LineBasicMaterial({ color: CORAL, transparent: true, opacity: 0, toneMapped: false });
scene.add(new THREE.LineSegments(beamG, beamM));
// corner-kick tactic (TacticAI beat): curves from the corner into the box, and runs
const CORNER = new THREE.Vector3(PX - .2, .15, -PZ + .2);
const tactic = [[-1.4, -8.6], [.2, -7.2], [1.8, -8.4]].map(([x, z], k) => new THREE.QuadraticBezierCurve3(CORNER.clone(), new THREE.Vector3(lerp(CORNER.x, x, .5), 3 + k * .6, lerp(CORNER.z, z, .5) + 1.2), new THREE.Vector3(x, .3, z)));
const tacticMats = tactic.map((cv, k) => { const m = new THREE.MeshBasicMaterial({ color: k === 1 ? CORAL : GOLD, transparent: true, opacity: 0, toneMapped: false }); scene.add(new THREE.Mesh(new THREE.TubeGeometry(cv, 40, .06, 6), m)); return m; });
const RUNS = [[[-3, -4.5], [-1.4, -8.4]], [[0, -4], [.2, -7.2]], [[2.6, -5], [1.8, -8.2]], [[-1, -6], [-2.6, -7.6]]];
const runM = new THREE.InstancedMesh(new THREE.ConeGeometry(.16, .4, 3).rotateX(Math.PI / 2), new THREE.MeshBasicMaterial({ color: CORAL, toneMapped: false }), 40);
scene.add(runM);
// snow
const SNOW_N = 520;
const snowM = new THREE.InstancedMesh(new THREE.SphereGeometry(.035, 10, 8), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }), SNOW_N);
scene.add(snowM);
// goal bursts (confetti cones at the scoring end)
const CONF_N = 90;
const confM = new THREE.InstancedMesh(new THREE.BoxGeometry(.12, .02, .2), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false, side: THREE.DoubleSide }), CONF_N);
scene.add(confM);

// ---------------------------------------------------------------- the match script
// goals: shot time, scoring team, shooter id, shot origin, duration of the flight
const GOALS = [];
const goal = (t, team, who, from, dur = .45) => GOALS.push({ t, team, who, from, dur });
[7.32, 7.74, 8.16, 8.6].forEach((t, k) => goal(t, "home", [9, 10, 6, 9][k], [[-1, -6.5], [1.5, -6], [-2.2, -5.2], [.8, -6.8]][k], .3));
goal(C.scores + .05, "home", ID17, [1.2, -6.2], .6);
goal(C.twonil - .7, "away", 20, [.5, 6.2], .3);
goal(C.twonil - .25, "away", 21, [-1, 6.6], .3);
[C.three, C.goals + .3, C.twenty + .3].forEach((t, k) => goal(t, "home", [ID17, 9, 8][k], [[0, -6.4], [-1.8, -6], [2, -6.5]][k], .38));
goal(C.winner - .35, "away", IDCAP, [1.4, 6.4], 1.1);
const SLOWMO = [C.winner - .9, C.winner + 1.0];
// the score at time t (home, away) follows the match: one count per match
function lastGoalBefore(t) { let g = null; for (const x of GOALS) if (x.t + x.dur <= t) g = x; return g; }
window.FOOTBALL_GOALS = GOALS;

// match time runs faster in the montage, slower in the slow motion
const FR = 60, NS = Math.ceil((DUR + 1) * FR);
const PROG = new Float32Array(NS + 1);
const speedAt = (t) => (t > 7.1 && t < 9.0 ? 3.2 : t > SLOWMO[0] && t < SLOWMO[1] ? .3 : 1);
for (let i = 1; i <= NS; i++) PROG[i] = PROG[i - 1] + speedAt((i - .5) / FR) / FR;
const prog = (t) => { const f = clamp(t, 0, DUR) * FR, i = Math.floor(f); return lerp(PROG[i], PROG[Math.min(NS, i + 1)], f - i); };

function ballAt(t, out) {
  const m = prog(t);
  // the idle ball: wandering around midfield
  out.set(Math.sin(m * .61) * 3.6 + Math.sin(m * 1.37) * 1.3, .14 + Math.abs(Math.sin(m * 3.1)) * .25, Math.sin(m * .43 + 1) * 4.5 + Math.sin(m * 1.1) * 1.2);
  for (const g of GOALS) {
    const dir = g.team === "home" ? -1 : 1;
    const a = g.t - .35, b = g.t, c = g.t + g.dur;
    if (t < a - .6 || t > c + 1.4) continue;
    const from = V2.set(g.from[0], .14, g.from[1]);
    if (t < b) { out.lerp(from, ss(t, a - .6, b)); continue; }
    const net = new THREE.Vector3((hash(g.t) - .5) * 1.4, .45, dir * (PZ + .45));
    if (t < c) { const u = ramp(t, b, c); out.lerpVectors(from, net, u); out.y = .14 + Math.sin(Math.PI * u) * (g.dur > .8 ? 1.2 : .6) + u * .25; continue; }
    out.copy(net); out.y = .2;
    if (t > c + .7) out.lerp(V2.set(0, .14, 0), ss(t, c + .7, c + 1.4));
  }
  return out;
}

// who is on the pitch, in which kit, at time t
const sold = () => C.sells + .3;
const finalOn = () => C.cup - .4;
function playerAt(id, t, ballP, out) {
  // returns {x, z, vis, kit, sit}
  const m = prog(t);
  let base, team = "home", vis = 1, sit = 0;
  const rewire = ss(t, C.rewires, C.rewires + 1.6);
  if (id < N_HOME) {
    const a = F442[id], b = F343[id];
    base = [lerp(a[0], b[0], rewire), lerp(a[1], b[1], rewire)];
    if (id === 10) vis = t < C.signs + 1.6 ? 1 : 0;                 // the forward the 17-year-old replaces
    if (id === 6) vis = t < sold() + 1.2 ? 0 : 1;                    // the captain's slot after he is sold
  } else if (id < N_HOME + N_AWAY) {
    const a = F442[id - N_HOME];
    base = [-a[0], -a[1]]; team = "away";
    if (id === 20 && t > finalOn()) vis = 0;                         // the captain takes this place in the final
  } else if (id === ID17) {
    const b = F343[10], a = F442[10];
    const slot = [lerp(a[0], b[0], rewire), lerp(a[1], b[1], rewire)];
    const walk = ss(t, C.signs - .2, C.signs + 1.8);
    base = [lerp(-8.3, slot[0], walk), lerp(0, slot[1], walk)];
    vis = t > C.signs - .3 ? 1 : 0;
  } else if (id === IDCAP) {
    if (t < finalOn()) {
      const a = F442[6], b = F343[6];
      const off = ss(t, sold(), sold() + 1.8);
      base = [lerp(lerp(a[0], b[0], rewire), 7.3, off), lerp(lerp(a[1], b[1], rewire), 1.6, off)];
      vis = t < sold() + 1.9 ? 1 : 0;
    } else {
      const a = F442[9]; base = [-a[0], -a[1]]; team = "away";
    }
  } else if (id === IDSTAR) { base = [8.1, -.9]; sit = 1; }
  else { base = [8.1, id === IDSUB[0] ? .3 : 1.2]; sit = 1; }
  let x = base[0], z = base[1];
  if (!sit) {
    const k = team === "home" ? .22 : .2;
    x += (ballP.x - x) * k + Math.sin(m * 1.3 + id * 1.7) * .35;
    z += (ballP.z - z) * k * .6 + Math.cos(m * 1.1 + id * 2.3) * .35;
    for (const g of GOALS) {                                         // the shooter meets the ball
      if (g.who !== id || t < g.t - 1.2 || t > g.t + .5) continue;
      const u = ss(t, g.t - 1.2, g.t - .05) * (1 - ss(t, g.t + .1, g.t + .5));
      x = lerp(x, g.from[0] + .25, u); z = lerp(z, g.from[1] + (team === "home" ? .35 : -.35), u);
    }
  }
  out.x = x; out.z = z; out.vis = vis; out.team = team; out.sit = sit;
  return out;
}

// ---------------------------------------------------------------- camera keyframes
const K = [];
const key = (t, p, l, fov = 40) => K.push({ t, p: new THREE.Vector3(...p), l: new THREE.Vector3(...l), fov });
key(0, [4.6, 2.0, -2.8], [8.1, .8, -.6], 42);
key(2.6, [4.6, 2.3, -3.4], [8.0, .8, -.3], 42);
key(4.6, [15, 13, 19], [0, 1.2, 0], 40);
key(7.0, [0, 30, 16], [0, 0, -1], 40);
key(9.6, [-2, 31, 17], [0, 0, -1], 40);
key(C.tracking - .2, [-8, 12, 15], [0, 0, 1], 40);
key(E[1], [-9, 12, 13], [0, 0, 0], 40);
key(L[2] + .2, [-3.2, 4.4, 4.6], [-7.6, .6, -.2], 42);
key(C.signs + 1.6, [-1.6, 5.2, 3.4], [-3.6, .6, -1.6], 42);
key(C.scores - .9, [-2.5, 7.5, -15.5], [0, .5, -7], 42);
key(E[2] + .1, [-1.5, 7.8, -16], [0, .5, -7.5], 42);
key(L[3] + .4, [10, 21, 20], [0, 0, 0], 40);
key(C.rewires - .1, [0, 31, 7], [0, 0, 0], 40);
key(C.heart + .3, [1, 31, 7.5], [0, 0, 0], 40);
key(C.three - .4, [2.5, 7.5, -15.5], [0, .5, -7], 42);
key(E[3] + .1, [1.5, 7.8, -16], [0, .5, -7.5], 42);
key(L[4] + .3, [14, 8, 17], [5, 2.4, 3], 40);
key(C.chanting - .3, [-6, 11, 22], [-2, 2.4, 4], 40);
key(E[4] + .1, [-4, 11.5, 21], [0, 2.4, 3], 40);
key(L[5] + .3, [3.8, 3.2, 5.5], [8, .8, 1.2], 42);
key(C.cup - .5, [4.2, 3.4, 6], [8, .8, 1.2], 42);
key(C.cup + .2, [-2.5, 7.8, 16.5], [0, .6, 7], 42);
key(C.winner + .9, [-1.4, 6.6, 15], [0, .6, 8.8], 42);
key(E[5] + .1, [-1.2, 6.8, 15.2], [0, .6, 8.8], 42);
key(L[6] + .5, [9, 17, 1], [3, 0, -7], 40);
key(C.designs, [4.5, 19, -1.5], [2.5, 0, -7.4], 40);
key(E[6], [4, 20, -1], [2.5, 0, -7.6], 40);
key(L[7] + .3, [0, 36, 30], [0, 0, 0], 38);
key(DUR, [0, 40, 33], [0, 0, 0], 38);
const ease3 = (x) => (x < .5 ? 4 * x * x * x : 1 - (-2 * x + 2) ** 3 / 2);
function camAt(t) {
  let i = 0;
  while (i < K.length - 2 && t > K[i + 1].t) i++;
  const a = K[i], b = K[i + 1];
  const u = ease3(ramp(t, a.t, b.t));
  camera.position.lerpVectors(a.p, b.p, u);
  camera.position.y += Math.sin(Math.PI * u) * a.p.distanceTo(b.p) * .22;
  const look = V2.lerpVectors(a.l, b.l, u);
  camera.fov = lerp(a.fov, b.fov, u);
  let sh = 0;
  for (const g of GOALS) sh += .3 * pulse(t, g.t + g.dur, .18);
  sh += .3 * pulse(t, C.booing, .4);
  camera.position.x += Math.sin(t * .37) * .12 + Math.sin(t * 31) * sh * .3;
  camera.position.y += Math.sin(t * .29 + 1) * .08 + Math.sin(t * 27 + 2) * sh * .2;
  camera.updateProjectionMatrix();
  camera.lookAt(look);
}

// ---------------------------------------------------------------- render at time t
const PS = { x: 0, z: 0, vis: 1, team: "home", sit: 0 }, PS0 = { x: 0, z: 0, vis: 1, team: "home", sit: 0 };
const BP0 = new THREE.Vector3();
const PARTS = [torsoM, shortsM, legM, bootM, armM, headM, hairCapM, hairAfroM, hairMohM, eyeM, eyeHiM, browM, mouthArcM, mouthOM];
const MB = new THREE.Matrix4(), MP = new THREE.Matrix4(), MR = new THREE.Matrix4(), MOUT = new THREE.Matrix4(), EU = new THREE.Euler();
// one part of the current player: the player's base matrix MB, then the part's local position, rotation (about its
// pivot, dropping by `drop` below it) and scale
function part(mesh, idx, x, y, z, rx, ry, rz, drop = 0, s = 1, sy = 1) {
  MP.makeTranslation(x, y, z);
  MP.multiply(MR.makeRotationFromEuler(EU.set(rx, ry, rz)));
  if (drop) MP.multiply(MR.makeTranslation(0, -drop, 0));
  if (s !== 1 || sy !== 1) MP.multiply(MR.makeScale(s, s * sy, s));
  MOUT.multiplyMatrices(MB, MP);
  if (mesh) mesh.setMatrixAt(idx, MOUT);
}
// the face for player id at time t: mouth (smile / frown / o / flat), brow tilt (+ angry, - worried), brow lift, eye size
function expression(id, t, team) {
  let mouth = "flat", brow = 0, lift = 0, eyes = 1;
  if (id === IDSTAR && t < 9) { mouth = "frown"; brow = .4; }
  if (IDSUB.includes(id)) mouth = "smile";
  if (t > 9.4 && t < E[1]) mouth = team === "home" ? "smile" : "frown";
  if (t > C.rewires - .2 && t < C.three) { mouth = "flat"; brow = team === "home" ? .3 : 0; }
  if (t > L[4] - .2 && t < E[4] + .3) { mouth = team === "home" ? "smile" : "frown"; brow = team === "home" ? -.15 : .25; }
  for (const g of GOALS) {
    if (t < g.t + g.dur - .05 || t > g.t + g.dur + 2.6) continue;
    const happy = g.team === team;
    mouth = happy ? (id === g.who ? "o" : "smile") : "frown"; brow = happy ? -.2 : -.35; lift = happy ? .015 : 0; eyes = happy ? 1.1 : 1;
  }
  if (id === IDCAP && t > C.sells - .2 && t < C.sells + 2.4) { mouth = "o"; lift = .025; eyes = 1.3; brow = -.3; }
  if (IDSUB.includes(id) && t > C.sells - .2 && t < C.sells + 2.4) { mouth = "o"; lift = .02; eyes = 1.25; }
  if (t > C.winner + .3 && t < E[5] + .4) {
    if (id === IDCAP) { mouth = "smile"; brow = -.2; }
    else if (team === "home") { mouth = "o"; eyes = 1.3; lift = .02; brow = -.3; }
  }
  return { mouth, brow, lift, eyes };
}
const BP = new THREE.Vector3();
const KIT = { home: col(CORAL), away: col(NAVY) };
function renderAt(t) {
  const m = prog(t);
  // sky: day, warm late-afternoon for Christmas, night for the cup final
  const night = ss(t, C.cup - .5, C.cup + .1) * (1 - ss(t, E[5] + .1, L[6] + .3));
  tmpC.set(0xF1E9DC).lerp(tmpC2.set(0xF2E2D2), ss(t, L[4], L[4] + .5) * (1 - ss(t, E[4], E[4] + .5))).lerp(tmpC2.set(0x2F3554), night);
  scene.background.copy(tmpC); scene.fog.color.copy(tmpC);
  sun.intensity = lerp(2.1, .35, night);
  hemi.intensity = lerp(.95, .55, night);
  hemi.color.set(0xFFF6EA).lerp(tmpC2.set(0x9DA6D8), night);
  hemi.groundColor.set(0xCDBFA8).lerp(tmpC2.set(0x3A3F5E), night);
  towers.forEach((tm) => { tm.emissiveIntensity = .2 + night * 2.4; });
  bloom.strength = lerp(.22, .55, night);
  bloom.threshold = lerp(.92, .7, night);

  // the orb
  const cmd = pulse(t, C.benched, .35) + pulse(t, C.rewires, .4) + pulse(t, C.sells, .35) + pulse(t, C.signs, .35);
  orbCoreM.emissiveIntensity = .9 + cmd * 1.6 + night * .6;
  orb.scale.setScalar(1 + cmd * .12);
  orb.position.set(ORB.x, ORB.y + Math.sin(t * 1.3) * .18, ORB.z);
  ring1.rotation.set(Math.PI / 2 + Math.sin(t * .7) * .4, t * .9, 0);
  ring2.rotation.set(Math.PI / 2.6, -t * 1.3, t * .4);

  // ball and trail
  ballAt(t, BP);
  ball.position.copy(BP);
  const shot = GOALS.some((g) => t > g.t && t < g.t + g.dur);
  for (let k = 0; k < 8; k++) {
    ballAt(t - (k + 1) * .035, V);
    M4.compose(V, Q.identity(), S.setScalar(shot ? (1 - k / 8) * 1.1 : .001));
    trailM.setMatrixAt(k, M4);
  }
  trailM.instanceMatrix.needsUpdate = true;

  // players
  const trackOn = ss(t, C.tracking - .2, C.tracking + .3) * (1 - ss(t, E[1], E[1] + .4));
  const heartOn = ss(t, C.rewires - .2, C.rewires + .3) * (1 - ss(t, C.three, C.three + .4));
  const boo = 1 - ss(t, 7.0, 7.6);
  ballAt(t - .06, BP0);
  for (let id = 0; id < NP; id++) {
    playerAt(id, t - .06, BP0, PS0);
    playerAt(id, t, BP, PS);
    let vis = PS.vis;
    if (id === IDSTAR || IDSUB.includes(id)) vis = 1;
    const sc = Math.max(.001, vis);
    const lk = LOOK[id];
    // heading: along the run when moving, else towards the ball; benched players face the pitch
    const vx = (PS.x - PS0.x) / .06, vz = (PS.z - PS0.z) / .06, sp = Math.hypot(vx, vz);
    let yaw = sp > .6 ? Math.atan2(vx, vz) : Math.atan2(BP.x - PS.x, BP.z - PS.z);
    if (PS.sit) yaw = -Math.PI / 2;
    const run = PS.sit ? 0 : clamp(sp / 3, .15, 1);
    const ph = m * 9 + id * 1.3;
    let jump = 0, cheer = 0;
    for (const g of GOALS) if (g.who === id) { const u = ramp(t, g.t + g.dur, g.t + g.dur + .9); jump += Math.max(0, Math.sin(Math.PI * u)) * .6; cheer = Math.max(cheer, u > 0 && u < 1 ? 1 : 0); }
    const bob = PS.sit ? 0 : Math.abs(Math.sin(ph)) * .05 * run;
    MB.compose(V.set(PS.x, bob + jump - (PS.sit ? .2 : 0), PS.z), Q.setFromAxisAngle(UP, yaw), S.set(sc * lk.h, sc * lk.h, sc * lk.h));
    const kit = PS.team === "home" ? KIT.home : KIT.away;
    tmpC.copy(kit);
    if (id === IDSTAR) tmpC.lerp(tmpC2.set(0x9a8f86), .2);
    if (id === 0) tmpC.set(GOLD);                       // goalkeepers in their own kits
    if (id === N_HOME) tmpC.set(0x3FA372);
    if (IDSUB.includes(id)) tmpC.set(0xF4C9B4);
    // body
    part(torsoM, id, 0, .82, 0, 0, 0, 0); torsoM.setColorAt(id, tmpC);
    part(shortsM, id, 0, .52, 0, 0, 0, 0); shortsM.setColorAt(id, tmpC2.set(PS.team === "home" ? CREAM : 0x22335c));
    for (let side = 0; side < 2; side++) {
      const sx = side ? .095 : -.095;
      const swing = PS.sit ? -1.45 : Math.sin(ph + side * Math.PI) * .75 * run;
      part(legM, id * 2 + side, sx, .45, 0, swing, 0, 0, .2);
      legM.setColorAt(id * 2 + side, tmpC2.copy(tmpC).multiplyScalar(.82));
      // boots follow the foot at the end of the leg
      const fy = .45 - Math.cos(swing) * .4, fz = -Math.sin(swing) * .4;
      part(bootM, id * 2 + side, sx, Math.max(.035, fy), fz + .04, 0, 0, 0);
      bootM.setColorAt(id * 2 + side, tmpC2.set(lk.boot));
      const armSwing = cheer ? -2.8 : PS.sit ? -.5 : -Math.sin(ph + side * Math.PI) * .7 * run;
      part(armM, id * 2 + side, side ? .232 : -.232, 1.0, 0, armSwing, 0, side ? -.12 : .12, .17);
      armM.setColorAt(id * 2 + side, tmpC2.set(lk.skin));
    }
    // head, hair
    part(headM, id, 0, 1.27, 0, 0, 0, 0); headM.setColorAt(id, tmpC2.set(lk.skin));
    part(hairCapM, id, 0, 1.285, -.01, 0, 0, 0, 0, lk.style === 0 || lk.style === 3 ? 1 : .001, lk.style === 3 ? .45 : 1);
    part(hairAfroM, id, 0, 1.33, -.03, 0, 0, 0, 0, lk.style === 1 ? 1 : .001);
    part(hairMohM, id, 0, 1.43, -.02, 0, 0, 0, 0, lk.style === 2 ? 1 : .001);
    for (const hm of [hairCapM, hairAfroM, hairMohM]) hm.setColorAt(id, tmpC2.set(lk.hair));
    // the face: expression from the story
    const ex = expression(id, t, PS.team);
    for (let side = 0; side < 2; side++) {
      const sx = side ? .062 : -.062;
      part(eyeM, id * 2 + side, sx, 1.295, .148, 0, 0, 0, 0, 1, ex.eyes);
      part(eyeHiM, id * 2 + side, sx + .009, 1.304, .171, 0, 0, 0);
      part(browM, id * 2 + side, sx, 1.35 + ex.lift, .158, 0, 0, (side ? -1 : 1) * ex.brow);
    }
    const o = ex.mouth === "o";
    part(mouthArcM, id, 0, 1.2 + (ex.mouth === "smile" ? .025 : 0), .158, 0, 0, ex.mouth === "smile" ? Math.PI : 0, 0, o ? .001 : 1, ex.mouth === "flat" ? .18 : 1);
    part(mouthOM, id, 0, 1.205, .158, 0, 0, 0, 0, o ? 1 : .001);
    if (id === IDCAP) { part(null, 0, -.232, .93, 0, Math.PI / 2, 0, 0); armband.matrix.copy(MOUT); armband.matrixAutoUpdate = false; }
    // rings: tracking (green / red for the star), heart-rate pulses (red), NEW (17), captain gold
    let r = 0; tmpC.set(0x3FA372);
    if (trackOn > 0 && vis > 0) { r = trackOn; }
    if (id === IDSTAR) { r = Math.max(r, (1 - ss(t, 6.8, 7.2)) * ss(t, C.benched - .2, C.benched + .1), trackOn); tmpC.set(0xD9483B); }
    if (heartOn > 0 && PS.team === "home" && vis > 0 && id < 24) { r = heartOn * (.6 + .4 * Math.max(0, Math.sin(t * 8 + id))); tmpC.set(0xD9483B); }
    if (id === ID17 && t > C.signs - .3 && t < E[2] + .2) { r = 1; tmpC.set(GOLD); }
    if (id === IDCAP && t > sold() - .2 && t < sold() + 1.9) { r = 1; tmpC.set(GOLD); }
    if (id === IDCAP && t > C.winner - .5 && t < E[5]) { r = 1; tmpC.set(GOLD); }
    M4.compose(V.set(PS.x, .08, PS.z), Q.identity(), S.setScalar(Math.max(.001, r * sc * (1 + .15 * Math.sin(t * 6 + id)))));
    ringM.setMatrixAt(id, M4);
    ringM.setColorAt(id, tmpC);
    if (id < N_HOME && id !== 0) {
      beamPos.set([ORB.x, ORB.y - .9, ORB.z, PS.x, 1.1, PS.z], id * 6);
    }
  }
  for (const m_ of PARTS) { m_.instanceMatrix.needsUpdate = true; if (m_.instanceColor) m_.instanceColor.needsUpdate = true; }
  ringM.instanceMatrix.needsUpdate = true; ringM.instanceColor.needsUpdate = true;
  armband.visible = t < sold() + 1.9 || t > finalOn();
  armband.matrixWorldNeedsUpdate = true;
  // formation graph and the orb's beams at the rewire
  EDGES.forEach(([a, b], k) => {
    playerAt(a === 10 ? ID17 : a === 6 ? (t < sold() ? IDCAP : 6) : a, t, BP, PS); const ax = PS.x, az = PS.z;
    playerAt(b === 10 ? ID17 : b === 6 ? (t < sold() ? IDCAP : 6) : b, t, BP, PS);
    graphPos.set([ax, .12, az, PS.x, .12, PS.z], k * 6);
  });
  graphG.attributes.position.needsUpdate = true;
  graphM.opacity = .95 * ss(t, C.rewires - .1, C.rewires + .3) * (1 - ss(t, C.three - .2, C.three + .2));
  beamG.attributes.position.needsUpdate = true;
  beamM.opacity = .8 * ss(t, C.rewires - .2, C.rewires) * (1 - ss(t, C.rewires + .8, C.rewires + 1.4));

  // crowd: boo (grey, slow sway), cheer on every goal, chant in a coral wave, silence in the final
  let cheerHome = 0, cheerAway = 0;
  for (const g of GOALS) { const c = Math.max(0, Math.sin(Math.PI * ramp(t, g.t + g.dur - .05, g.t + g.dur + 1.2))); if (g.team === "home") cheerHome += c; else cheerAway += c; }
  const chant = ss(t, C.chanting - .4, C.chanting) * (1 - ss(t, E[4] + .2, E[4] + .6));
  const silence = ss(t, C.winner + .2, C.winner + .6) * (1 - ss(t, E[5], E[5] + .4));
  FANS.forEach((f, i) => {
    const away = f.side === "s";
    let y = f.y, c = fanBase[i];
    tmpC.set(c);
    if (!away) {
      y += boo * Math.sin(t * 2 + i * .3) * .03;
      tmpC.lerp(tmpC2.set(0x9a9aa8), boo * .55);
      y += cheerHome * Math.abs(Math.sin(t * 9 + i)) * .28;
      const ang = Math.atan2(f.z, f.x);
      const wave = Math.max(0, Math.sin(ang * 2 - t * 5));
      y += chant * (Math.abs(Math.sin(t * 6.2)) * .12 + wave * .3);
      tmpC.lerp(tmpC2.set(CORAL), chant * wave * .8);
      tmpC.lerp(tmpC2.set(0x6a6470), silence * .6);
    } else {
      y += cheerAway * Math.abs(Math.sin(t * 9 + i)) * .3;
    }
    M4.compose(V.set(f.x, y, f.z), Q.identity(), S.setScalar(1));
    fanM.setMatrixAt(i, M4);
    fanM.setColorAt(i, tmpC);
  });
  fanM.instanceMatrix.needsUpdate = true;
  fanM.instanceColor.needsUpdate = true;

  // confetti at the scoring end after each home goal (gold) and the final winner (navy)
  const lg = lastGoalBefore(t);
  const age = lg ? t - (lg.t + lg.dur) : 9;
  for (let k = 0; k < CONF_N; k++) {
    let s = .001;
    if (lg && age < 1.6 && lg.dur < 1) {
      const dir = lg.team === "home" ? -1 : 1;
      const a = hash(k) * Math.PI * 2, sp = 2 + hash(k * 3) * 3;
      V.set(Math.cos(a) * sp * age * .8, 1.5 + age * (3 - age * 2.2) + hash(k * 7), dir * (PZ + 1.2) + Math.sin(a) * sp * age * .5);
      s = 1 - age / 1.6;
      confM.setColorAt(k, tmpC.set([GOLD, CORAL, CREAM][k % 3]));
    }
    M4.compose(V, Q.setFromAxisAngle(UP, k + t * 3), S.setScalar(Math.max(.001, s)));
    confM.setMatrixAt(k, M4);
  }
  confM.instanceMatrix.needsUpdate = true;
  if (confM.instanceColor) confM.instanceColor.needsUpdate = true;

  // snow at Christmas
  const snow = ss(t, L[4] - .2, L[4] + .4) * (1 - ss(t, E[4] + .2, E[4] + .8));
  for (let k = 0; k < SNOW_N; k++) {
    const fall = (hash(k * 5) * 14 - t * (1.2 + hash(k) * .8)) % 14;
    V.set((hash(k) - .5) * 30 + Math.sin(t + k) * .3, (fall + 14) % 14, (hash(k * 3) - .5) * 34);
    M4.compose(V, Q.identity(), S.setScalar(Math.max(.001, snow)));
    snowM.setMatrixAt(k, M4);
  }
  snowM.instanceMatrix.needsUpdate = true;

  // corner tactic
  const tac = ss(t, C.designs - .3, C.designs + .3) * (1 - ss(t, E[6] + .2, E[6] + .6));
  tacticMats.forEach((mm, k) => { mm.opacity = tac * ss(t, C.designs + k * .25, C.designs + .3 + k * .25); });
  for (let i = 0; i < 40; i++) {
    const [a, b] = RUNS[i % RUNS.length];
    const u = ((t * .6 + hash(i) * 2) % 1);
    M4.compose(V.set(lerp(a[0], b[0], u), .3, lerp(a[1], b[1], u)), Q.setFromAxisAngle(UP, Math.atan2(b[0] - a[0], b[1] - a[1])), S.setScalar(Math.max(.001, tac * ss(t, C.designs + .6, C.designs + 1))));
    runM.setMatrixAt(i, M4);
  }
  runM.instanceMatrix.needsUpdate = true;
  if (tac > .01 && t > C.tactics) { const u = ramp(t, C.tactics, C.tactics + 1.1); tactic[1].getPointAt(Math.min(1, u), V); ball.position.copy(V); }

  // grade
  grade.uniforms.uSat.value = 1 - silence * .5 - boo * .25;
  grade.uniforms.uWarm.value = ss(t, L[4], L[4] + .5) * (1 - ss(t, E[4], E[4] + .5)) * .6;
  let fl = 0;
  for (const g of GOALS) fl += .28 * pulse(t, g.t + g.dur, .1);
  grade.uniforms.uFlash.value = fl + .3 * pulse(t, C.sells, .1);
  grade.uniforms.uTime.value = t;

  camAt(t);
  const cv = window.FOOTBALL_COVER;
  if (cv) { camera.position.set(...cv.cam); camera.fov = cv.fov; camera.updateProjectionMatrix(); camera.lookAt(...cv.look); }
  composer.render();
}

const ready = (async () => {
  renderer.compile(scene, camera);
  renderAt(window.FOOTBALL_COVER ? window.FOOTBALL_COVER.t : (window.__hfThreeTime || 0));
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["stadium"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(window.FOOTBALL_COVER ? window.FOOTBALL_COVER.t : e.detail.time));
