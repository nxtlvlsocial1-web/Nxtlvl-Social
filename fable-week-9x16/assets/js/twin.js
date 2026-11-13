// Fable week reel (AI.NXTLVL): the "3D twin" example, an original low-poly owl in the page's violets. It is a pure
// function of time t, rendered on HyperFrames' hf-seek: a glowing wireframe draws itself in, the faceted solid fades up
// through it, then it idles (slow turn, bob, blink) on a hologram ring while sparks drift up. Times come from
// window.FB_T.twin = [appear, build start, build end, leave] (written by build/generate.py from the voice timings).
import * as THREE from "three";

const W = 1080, H = 1080;
const T = window.FB_T.twin;
const canvas = document.getElementById("twin");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.setClearColor(0x000000, 0);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(30, W / H, .1, 50);
camera.position.set(0, 1.25, 7.2);
camera.lookAt(0, .95, 0);

scene.add(new THREE.HemisphereLight(0xd9c4ff, 0x1a0538, 1.3));
const key = new THREE.DirectionalLight(0xffffff, 2.4); key.position.set(3, 5, 4); scene.add(key);
const rim = new THREE.DirectionalLight(0x8a3bff, 3.2); rim.position.set(-4, 2, -3); scene.add(rim);

// ---------------------------------------------------------------- the owl, built from low-poly pieces
const owl = new THREE.Group();
scene.add(owl);
const solids = [], wires = [];
function part(geo, color, pos, scale = [1, 1, 1], rot = [0, 0, 0], emissive = 0x000000, ei = 0) {
  const mat = new THREE.MeshStandardMaterial({ color, flatShading: true, roughness: .55, metalness: .1, transparent: true, opacity: 0,
    emissive, emissiveIntensity: ei });
  const m = new THREE.Mesh(geo, mat);
  m.position.set(...pos); m.scale.set(...scale); m.rotation.set(...rot);
  owl.add(m); solids.push(m);
  const w = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 1), new THREE.LineBasicMaterial({ color: 0xcfb3ff, transparent: true, opacity: 0 }));
  w.position.copy(m.position); w.scale.copy(m.scale); w.rotation.copy(m.rotation);
  owl.add(w); wires.push(w);
  return m;
}
const VIOLET = 0x7a2ffb, LAV = 0xb687f9, DEEP = 0x4b14b8, GOLD = 0xffb547, WHITE = 0xf6f0ff;
part(new THREE.IcosahedronGeometry(1, 1), VIOLET, [0, .95, 0], [.86, 1.02, .78]);                         // body
part(new THREE.IcosahedronGeometry(.62, 1), LAV, [0, .82, .42], [.95, 1.05, .55]);                         // belly
part(new THREE.IcosahedronGeometry(.74, 1), VIOLET, [0, 2.02, .05], [1.08, .92, .92]);                     // head
part(new THREE.IcosahedronGeometry(.5, 1), LAV, [0, 1.98, .44], [1.25, .9, .45]);                          // face disc
part(new THREE.ConeGeometry(.17, .5, 4), DEEP, [-.5, 2.62, -.02], [1, 1, 1], [0, 0, .32]);                 // ear tufts
part(new THREE.ConeGeometry(.17, .5, 4), DEEP, [.5, 2.62, -.02], [1, 1, 1], [0, 0, -.32]);
part(new THREE.IcosahedronGeometry(.55, 0), DEEP, [-.82, .98, -.05], [.45, 1.15, .8], [0, 0, .18]);       // wings
part(new THREE.IcosahedronGeometry(.55, 0), DEEP, [.82, .98, -.05], [.45, 1.15, .8], [0, 0, -.18]);
part(new THREE.ConeGeometry(.11, .28, 4), GOLD, [0, 1.86, .86], [1, 1, 1], [Math.PI / 2 + .25, 0, 0], GOLD, .4);   // beak
part(new THREE.ConeGeometry(.1, .26, 4), GOLD, [-.28, .02, .3], [1, 1, 1], [Math.PI / 2, 0, 0], GOLD, .2);          // feet
part(new THREE.ConeGeometry(.1, .26, 4), GOLD, [.28, .02, .3], [1, 1, 1], [Math.PI / 2, 0, 0], GOLD, .2);
// eyes: white disc, dark pupil, a glow ring; lids are scaled discs for the blink
const eyes = [];
for (const s of [-1, 1]) {
  const e = new THREE.Group(); e.position.set(.27 * s, 2.06, .78); owl.add(e);
  const white = new THREE.Mesh(new THREE.CircleGeometry(.2, 16), new THREE.MeshBasicMaterial({ color: WHITE, transparent: true, opacity: 0 }));
  const ring = new THREE.Mesh(new THREE.RingGeometry(.2, .245, 24), new THREE.MeshBasicMaterial({ color: GOLD, transparent: true, opacity: 0 }));
  const pupil = new THREE.Mesh(new THREE.CircleGeometry(.105, 16), new THREE.MeshBasicMaterial({ color: 0x14062e, transparent: true, opacity: 0 }));
  pupil.position.z = .01;
  const glint = new THREE.Mesh(new THREE.CircleGeometry(.035, 10), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0 }));
  glint.position.set(.045, .045, .02);
  const lid = new THREE.Mesh(new THREE.CircleGeometry(.215, 16), new THREE.MeshBasicMaterial({ color: VIOLET, transparent: true, opacity: 0 }));
  lid.position.z = .03; lid.scale.y = 0;
  e.add(white, ring, pupil, glint, lid);
  eyes.push({ white, ring, pupil, glint, lid });
}
// hologram base and drifting sparks
const base = new THREE.Mesh(new THREE.RingGeometry(1.05, 1.18, 64), new THREE.MeshBasicMaterial({ color: LAV, transparent: true, opacity: 0, side: THREE.DoubleSide }));
base.rotation.x = -Math.PI / 2; scene.add(base);
const base2 = new THREE.Mesh(new THREE.CircleGeometry(1.05, 64), new THREE.MeshBasicMaterial({ color: VIOLET, transparent: true, opacity: 0 }));
base2.rotation.x = -Math.PI / 2; base2.position.y = -.005; scene.add(base2);
const N = 70, sp = new Float32Array(N * 3), seeds = [];
for (let i = 0; i < N; i++) { seeds.push([Math.sin(i * 12.9) * .5 + .5, Math.sin(i * 78.2) * .5 + .5, Math.sin(i * 37.7) * .5 + .5]); }
const spGeo = new THREE.BufferGeometry(); spGeo.setAttribute("position", new THREE.BufferAttribute(sp, 3));
const sparks = new THREE.Points(spGeo, new THREE.PointsMaterial({ color: 0xd8c2ff, size: .05, transparent: true, opacity: 0 }));
scene.add(sparks);

// ---------------------------------------------------------------- time
const clamp = (x) => Math.min(1, Math.max(0, x));
const win = (t, a, b) => clamp((t - a) / (b - a));
const ease = (x) => 1 - Math.pow(1 - x, 3);

function renderAt(t) {
  const [a, b0, b1, z] = T;
  const show = t >= a - .05 && t <= z + .05;
  canvas.style.visibility = show ? "visible" : "hidden";
  if (!show) return;
  const wire = ease(win(t, b0, b0 + .7)) * (1 - win(t, b1 - .2, b1 + .5) * .85);
  const solid = ease(win(t, b0 + .55, b1));
  const glowPulse = Math.exp(-Math.pow((t - b1) / .25, 2));
  solids.forEach((m, i) => {
    const k = clamp(solid * 1.25 - i * .02);
    m.material.opacity = k;
    m.material.emissive.setHex(i >= 8 ? 0xffb547 : 0x7a2ffb);
    m.material.emissiveIntensity = (i >= 8 ? .4 : .15) + glowPulse * .9;
  });
  wires.forEach((w, i) => { w.material.opacity = clamp(wire * 1.2 - i * .03) * .95; });
  // the whole owl rises a little as it builds, then idles: slow turn, bob
  const idle = Math.max(0, t - b0);
  owl.rotation.y = -.7 + idle * .55 + Math.sin(idle * 1.3) * .08;
  owl.position.y = (1 - ease(win(t, a, b0 + .6))) * -.4 + Math.sin(idle * 2.2) * .05;
  owl.scale.setScalar(.92 + ease(win(t, a, b1)) * .08);
  // eyes open with the solid, blink twice
  const blink = Math.max(Math.exp(-Math.pow((t - (b1 + 1.0)) / .07, 2)), Math.exp(-Math.pow((t - (b1 + 2.6)) / .07, 2)));
  eyes.forEach((e) => {
    e.white.material.opacity = solid; e.ring.material.opacity = solid * .9; e.pupil.material.opacity = solid; e.glint.material.opacity = solid;
    e.lid.material.opacity = solid; e.lid.scale.y = blink;
    e.pupil.position.x = Math.sin(idle * .9) * .03;
  });
  base.material.opacity = ease(win(t, a, a + .5)) * (.55 + Math.sin(t * 6) * .1);
  base2.material.opacity = ease(win(t, a, a + .5)) * .18;
  base.scale.setScalar(1 + Math.sin(t * 2.4) * .03);
  for (let i = 0; i < N; i++) {
    const [r1, r2, r3] = seeds[i];
    const life = ((t * (.25 + r3 * .35) + r1) % 1);
    const ang = r2 * Math.PI * 2 + t * .3;
    sp[i * 3] = Math.cos(ang) * (1.1 + r1 * .6);
    sp[i * 3 + 1] = life * 3.2;
    sp[i * 3 + 2] = Math.sin(ang) * (1.1 + r1 * .6);
  }
  spGeo.attributes.position.needsUpdate = true;
  sparks.material.opacity = solid * .8;
  renderer.render(scene, camera);
}

const ready = (async () => { renderer.compile(scene, camera); renderAt(window.__hfThreeTime || 0); })();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["twin"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
