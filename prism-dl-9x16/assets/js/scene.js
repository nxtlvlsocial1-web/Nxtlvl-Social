// AI.NXTLVL "Prism: a free download manager" (9:16). The 3D stage is a pure function of time t (rendered on HyperFrames'
// hf-seek). Beats come from window.PR_T (build/generate.py, from the voice's word times). Layout grid, all centred on x:
// headline band (HTML, y 300-560 px), 3D stage centred at y ~1000 px, live caption (HTML, y ~1480 px).
//   hook   two timer rings: one connection 4:16, Prism 0:17 (Prism's own benchmark, 1 GiB, throttled server)
//   name   a glass prism: a white beam in, 32 coloured rays out
//   one    a server, one white beam, a file creeping along; a speed cap clamps the beam
//   split  the prism drops in between: the beam fans into up to 32 rays, the file fills as 32 columns at once
//   steal  8 lanes; one finishes early and takes half of the biggest part left; nothing sits idle
//   video  a video card, 1,800+ sites, 8K badge, then the MP3 waveform
//   resume a laptop: the battery dies at 63 %, the lid shuts, it opens and carries on from 63 %
//   more   a magnet (torrents) and a model card (Hugging Face)
//   catch  the rays squeeze through one pipe: your internet is the ceiling
//   end    the prism again, the share line, the comment box
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";

const W = 1080, H = 1920;
const T = window.PR_T;
const VIOLET = 0x7a2ffb, LAV = 0xb687f9;
const SPECTRUM = [0xff4d6d, 0xff8c42, 0xffd23f, 0x7ee081, 0x3ddbd9, 0x4d9bff, 0x7a5cff, 0xd35cff];
const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(34, W / H, .1, 100);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), .04).texture;
scene.environmentIntensity = .5;
const composer = new EffectComposer(renderer);
composer.setSize(W, H);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), .9, .5, .55);
composer.addPass(bloom);
composer.addPass(new OutputPass());
scene.add(new THREE.HemisphereLight(0xd8ccff, 0x0a0614, .6));
const key = new THREE.DirectionalLight(0xffffff, 1.6); key.position.set(-3, 6, 8); scene.add(key);
const rim = new THREE.PointLight(VIOLET, 40, 20); rim.position.set(3, 2, -3); scene.add(rim);

// ---------------------------------------------------------------- helpers
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const win = (t, a, b) => clamp((t - a) / (b - a));
const ease = (x) => 1 - Math.pow(1 - clamp(x), 3);
const easeIO = (x) => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const back = (x) => { x = clamp(x); const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const lerp = (a, b, x) => a + (b - a) * x;
const pulse = (t, at, w = .25) => Math.exp(-Math.pow((t - at) / w, 2));
const $ = (id) => document.getElementById(id);
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const v3 = new THREE.Vector3();
// a scene window: 0 before, rises over .45 s from a, holds, falls over .35 s before b
const life = (t, a, b) => easeIO(win(t, a - .05, a + .4)) * (1 - easeIO(win(t, b - .35, b)));
function project(obj, local, el, a = null, s = 1) {
  if (!el) return;
  v3.copy(local); if (obj) obj.localToWorld(v3); v3.project(camera);
  el.style.transform = `translate(${(v3.x * .5 + .5) * W}px, ${(-v3.y * .5 + .5) * H}px) translate(-50%, -50%) scale(${Math.max(.001, s)})`;
  if (a !== null) el.style.opacity = clamp(a);
}
function setText(id, txt) { const el = $(id); if (el && el.textContent !== txt) el.textContent = txt; }
const glow = (c, i = 1.4) => new THREE.MeshBasicMaterial({ color: new THREE.Color(c).multiplyScalar(i), transparent: true, toneMapped: false });
const glass = () => new THREE.MeshPhysicalMaterial({ color: 0xffffff, metalness: 0, roughness: .05, transmission: .9, thickness: .6, ior: 1.45,
  transparent: true, opacity: .55, clearcoat: 1, side: THREE.DoubleSide, emissive: LAV, emissiveIntensity: .06 });
const dark = new THREE.MeshPhysicalMaterial({ color: 0x15111f, metalness: .4, roughness: .35, clearcoat: .8 });

// ---------------------------------------------------------------- backdrop: a slow field of light streaks
const streaks = new THREE.Group(); scene.add(streaks);
const SN = 60;
for (let i = 0; i < SN; i++) {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(.012, .9), glow(SPECTRUM[i % 8], .7));
  m.material.opacity = .35; streaks.add(m);
}
const rnd = (i, k = 1) => { const s = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return s - Math.floor(s); };

// ---------------------------------------------------------------- the prism (glass triangle) + beam + rays
const prism = new THREE.Group(); scene.add(prism);
{
  const shape = new THREE.Shape(); const r = .95;
  for (let k = 0; k < 3; k++) { const a = Math.PI / 2 + k * 2 * Math.PI / 3; k ? shape.lineTo(Math.cos(a) * r, Math.sin(a) * r) : shape.moveTo(Math.cos(a) * r, Math.sin(a) * r); }
  shape.closePath();
  const geo = new THREE.ExtrudeGeometry(shape, { depth: .7, bevelEnabled: true, bevelSize: .05, bevelThickness: .05, bevelSegments: 3 });
  geo.center();
  prism.add(new THREE.Mesh(geo, glass()));
  const edges = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 30), new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: .8 }));
  prism.add(edges);
  const core = new THREE.Mesh(new THREE.SphereGeometry(.12, 24, 16), glow(0xffffff, 2)); prism.add(core);
}
const beam = new THREE.Mesh(new THREE.CylinderGeometry(.035, .035, 1, 12), glow(0xffffff, 2.2)); beam.rotation.z = Math.PI / 2; scene.add(beam);
const RN = 32;
const rays = [];
for (let i = 0; i < RN; i++) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(.016, .016, 1, 8), glow(SPECTRUM[i % 8], 1.15)); scene.add(m); rays.push(m);
}
function setBeam(a, b, thick, op) {                            // a white cylinder from point a to b
  const d = b.clone().sub(a), len = d.length();
  beam.visible = op > .01 && len > .01;
  beam.position.copy(a).add(b).multiplyScalar(.5);
  beam.scale.set(thick, len, thick);
  beam.quaternion.setFromUnitVectors(V(0, 1, 0), d.normalize());
  beam.material.opacity = op;
}
function setRay(i, a, b, op) {
  const m = rays[i], d = b.clone().sub(a), len = d.length();
  m.visible = op > .01 && len > .01;
  m.position.copy(a).add(b).multiplyScalar(.5); m.scale.set(1, len, 1);
  m.quaternion.setFromUnitVectors(V(0, 1, 0), d.normalize()); m.material.opacity = op;
}

// ---------------------------------------------------------------- hook: two timer rings built from 96 ticks each
function ring(color) {
  const g = new THREE.Group(); scene.add(g);
  const n = 96, ticks = [];
  for (let k = 0; k < n; k++) {
    const a = Math.PI / 2 - k / n * Math.PI * 2;
    const m = new THREE.Mesh(new THREE.BoxGeometry(.05, .2, .06), glow(color === "spectrum" ? SPECTRUM[k % 8] : color, 1.5));
    m.position.set(Math.cos(a) * 1.05, Math.sin(a) * 1.05, .17); m.rotation.z = a - Math.PI / 2; g.add(m); ticks.push(m);
  }
  const track = new THREE.Mesh(new THREE.TorusGeometry(1.05, .14, 12, 96), new THREE.MeshStandardMaterial({ color: 0x1c1630, roughness: .6, transparent: true }));
  track.position.z = -.06; g.add(track);
  return { g, ticks, track };
}
const ringA = ring(0x9b97b0), ringB = ring("spectrum");
function fillRing(R, x) { R.ticks.forEach((m, k) => { m.visible = k / R.ticks.length < x; }); }

// ---------------------------------------------------------------- server stack + file card + speed cap
const server = new THREE.Group(); scene.add(server);
for (let k = 0; k < 3; k++) {
  const slab = new THREE.Mesh(new RoundedBoxGeometry(1.7, .34, .9, 4, .06), dark); slab.position.y = k * .42; server.add(slab);
  for (let j = 0; j < 2; j++) { const led = new THREE.Mesh(new THREE.CircleGeometry(.035, 12), glow(0x7ee081, 2)); led.position.set(-.65 + j * .12, k * .42, .46); server.add(led); }
}
const file = new THREE.Group(); scene.add(file);
file.add(new THREE.Mesh(new RoundedBoxGeometry(2.6, .9, .14, 4, .06), dark));
const barTrack = new THREE.Mesh(new RoundedBoxGeometry(2.3, .12, .04, 2, .02), new THREE.MeshStandardMaterial({ color: 0x2a2440 })); barTrack.position.set(0, -.22, .09); file.add(barTrack);
const barFill = new THREE.Mesh(new THREE.BoxGeometry(1, .12, .05), glow(0xffffff, 1.4)); barFill.position.set(0, -.22, .1); file.add(barFill);
const cols = [];
for (let k = 0; k < 32; k++) {                                  // the split view: 32 columns filling at once
  const m = new THREE.Mesh(new THREE.BoxGeometry(.06, 1, .05), glow(SPECTRUM[k % 8], 1.05)); file.add(m); cols.push(m);
}
const cap = new THREE.Mesh(new THREE.TorusGeometry(.42, .05, 12, 64), glow(0xff4d6d, 1.8)); scene.add(cap);

// ---------------------------------------------------------------- work stealing: 8 lanes
const lanes = [];
const laneG = new THREE.Group(); scene.add(laneG);
for (let k = 0; k < 8; k++) {
  const y = 1.05 - k * .3;
  const tr = new THREE.Mesh(new RoundedBoxGeometry(3.2, .18, .08, 2, .04), new THREE.MeshStandardMaterial({ color: 0x221c36, roughness: .5 }));
  tr.position.set(0, y, 0); laneG.add(tr);
  const f = new THREE.Mesh(new THREE.BoxGeometry(1, .18, .1), glow(SPECTRUM[k], 1.3)); f.position.set(0, y, .02); laneG.add(f);
  const h = new THREE.Mesh(new THREE.BoxGeometry(.04, .22, .12), glow(0xffffff, 2)); h.position.set(0, y, .04); laneG.add(h);
  lanes.push({ f, h, y });
}
const stolen = new THREE.Mesh(new THREE.BoxGeometry(1, .18, .11), glow(0x7ee081, 1.6)); laneG.add(stolen);

// ---------------------------------------------------------------- video card + waveform
const video = new THREE.Group(); scene.add(video);
video.add(new THREE.Mesh(new RoundedBoxGeometry(3.0, 1.7, .12, 4, .1), dark));
{
  const scr = new THREE.Mesh(new THREE.PlaneGeometry(2.8, 1.5), new THREE.MeshBasicMaterial({ color: 0x1a1336 })); scr.position.z = .065; video.add(scr);
  const play = new THREE.Shape(); play.moveTo(-.2, -.25); play.lineTo(.3, 0); play.lineTo(-.2, .25); play.closePath();
  const pm = new THREE.Mesh(new THREE.ShapeGeometry(play), glow(0xffffff, 1.6)); pm.position.z = .08; video.add(pm);
  const pr = new THREE.Mesh(new THREE.RingGeometry(.42, .47, 64), glow(LAV, 1.6)); pr.position.z = .08; video.add(pr);
}
const wave = [];
const waveG = new THREE.Group(); scene.add(waveG);
for (let k = 0; k < 40; k++) { const m = new THREE.Mesh(new RoundedBoxGeometry(.05, 1, .05, 2, .02), glow(SPECTRUM[Math.floor(k / 5) % 8], 1.5)); m.position.x = (k - 19.5) * .085; waveG.add(m); wave.push(m); }

// ---------------------------------------------------------------- laptop (resume)
const laptop = new THREE.Group(); scene.add(laptop);
const alu = new THREE.MeshPhysicalMaterial({ color: 0x34363f, metalness: .9, roughness: .5, envMapIntensity: .4 });
{ const b = new THREE.Mesh(new RoundedBoxGeometry(2.6, .08, 1.7, 4, .04), alu); laptop.add(b);
  const kb = new THREE.Mesh(new THREE.PlaneGeometry(2.3, .8), new THREE.MeshStandardMaterial({ color: 0x0f1014, roughness: .7 })); kb.rotation.x = -Math.PI / 2; kb.position.set(0, .045, -.25); laptop.add(kb); }
const lid = new THREE.Group(); lid.position.set(0, .04, -.83); laptop.add(lid);
{ const s = new THREE.Mesh(new RoundedBoxGeometry(2.6, 1.65, .05, 4, .03), alu); s.position.y = .825; lid.add(s);
  const d = new THREE.Mesh(new THREE.PlaneGeometry(2.45, 1.5), new THREE.MeshBasicMaterial({ color: 0x120e22 })); d.position.set(0, .825, .03); lid.add(d); }
const lbarT = new THREE.Mesh(new THREE.PlaneGeometry(1.9, .1), new THREE.MeshBasicMaterial({ color: 0x2c2545 })); lbarT.position.set(0, .62, .035); lid.add(lbarT);
const lbarF = new THREE.Mesh(new THREE.PlaneGeometry(1, .1), glow(LAV, 1.4)); lbarF.position.set(0, .62, .036); lid.add(lbarF);
const lscr = new THREE.Mesh(new THREE.PlaneGeometry(2.45, 1.5), new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true })); lscr.position.set(0, .825, .037); lid.add(lscr);

// ---------------------------------------------------------------- magnet + model card
const magnet = new THREE.Group(); scene.add(magnet);
{ const u = new THREE.Mesh(new THREE.TorusGeometry(.5, .17, 16, 48, Math.PI), new THREE.MeshPhysicalMaterial({ color: 0xff4d6d, metalness: .3, roughness: .3, clearcoat: 1 }));
  u.rotation.z = Math.PI; magnet.add(u);
  for (const x of [-.5, .5]) { const tip = new THREE.Mesh(new THREE.CylinderGeometry(.17, .17, .32, 24), new THREE.MeshPhysicalMaterial({ color: 0xdde3ee, metalness: .9, roughness: .25 })); tip.position.set(x, .16, 0); magnet.add(tip); } }
const card = new THREE.Mesh(new RoundedBoxGeometry(2.4, 1.2, .1, 4, .08), dark); scene.add(card);

// ---------------------------------------------------------------- the catch: rays squeezed through one pipe
const pipe = new THREE.Mesh(new THREE.CylinderGeometry(.16, .16, 1.6, 32, 1, true), new THREE.MeshPhysicalMaterial({ color: 0xffffff, metalness: .2, roughness: .1, transparent: true, opacity: .35, side: THREE.DoubleSide, clearcoat: 1 }));
pipe.rotation.z = Math.PI / 2; scene.add(pipe);

// ---------------------------------------------------------------- per frame
function renderAt(t) {
  // camera: frontal, a slow breathing orbit; stage centre sits a touch under the frame centre
  const yaw = Math.sin(t * .35) * .06;
  camera.position.set(Math.sin(yaw) * 12, .25 + Math.sin(t * .27) * .08, Math.cos(yaw) * 12);
  camera.lookAt(0, .18, 0); camera.updateMatrixWorld(true);

  streaks.children.forEach((m, i) => {
    const u = (t * (.05 + rnd(i) * .07) + rnd(i, 2)) % 1;
    m.position.set((rnd(i, 3) - .5) * 9, (u - .5) * 16, -6 - rnd(i, 4) * 6);
    m.rotation.z = .5 + (rnd(i, 5) - .5) * .3;
  });

  // ---- hook: the two rings
  const hk = life(t, -1, T.p01 + .1);
  [ringA, ringB].forEach((R, i) => {
    R.g.visible = hk > .01;
    R.g.position.set(i ? 1.02 : -1.02, -.05, 0);
    R.g.scale.setScalar(.74 * Math.max(.001, hk));
    R.g.rotation.set(0, (i ? -.18 : .18) + Math.sin(t * .6 + i) * .05, 0);
  });
  // frame 1 shows the result; the rings re-run as the numbers are spoken
  fillRing(ringB, t < T.seventeen - .3 ? 1 : ease(win(t, T.seventeen - .3, T.seventeen + .5)));
  fillRing(ringA, t < T.four - .6 ? 1 : ease(win(t, T.four - .6, T.minutes + .4)));
  const secB = t < T.seventeen - .3 ? 17 : Math.round(17 * ease(win(t, T.seventeen - .3, T.seventeen + .5)));
  const secA = t < T.four - .6 ? 256 : Math.round(256 * ease(win(t, T.four - .6, T.minutes + .4)));
  setText("tmB", `0:${String(secB).padStart(2, "0")}`); setText("tmA", `${Math.floor(secA / 60)}:${String(secA % 60).padStart(2, "0")}`);
  project(ringA.g, V(0, 0, .2), $("tmA"), hk); project(ringB.g, V(0, 0, .2), $("tmB"), hk);
  project(ringA.g, V(0, -1.6, 0), $("lbA"), hk); project(ringB.g, V(0, -1.6, 0), $("lbB"), hk);

  // ---- the prism: name beat, split beat, end beat
  const pName = life(t, T.p01, T.p02 + .05), pSplit = life(t, T.p03 - .1, T.p04 + .05), pEnd = life(t, T.p09 - .1, 99);
  const pv = Math.max(pName, pSplit, pEnd);
  prism.visible = pv > .01;
  const pPos = pSplit > .01 ? V(0, .2, 0) : pEnd > .01 ? V(0, .45, 0) : V(0, .1, 0);
  prism.position.copy(pPos);
  prism.scale.setScalar(Math.max(.001, back(pv)) * (pSplit > .01 ? .55 : 1.15));
  prism.rotation.set(pSplit > .01 ? Math.PI / 2 : .1, Math.sin(t * .6) * .35 + (1 - pv) * 2, 0);
  rays.forEach((m) => (m.visible = false)); beam.visible = false;
  if (pName > .01 || pEnd > .01) {                              // a beam in from the left, a fan of rays out to the right
    const a = pName > .01 ? pName : pEnd;
    const L = V(-4.5, .1 + (pEnd > .01 ? .3 : 0), 0), C = prism.position.clone();
    setBeam(L, C, 1, a);
    for (let i = 0; i < RN; i++) {
      const ang = (i / (RN - 1) - .5) * .9;
      const len = 4.6 * ease(win(t, (pName > .01 ? T.p01 : T.p09) + .1 + i * .008, (pName > .01 ? T.p01 : T.p09) + .8 + i * .008));
      setRay(i, C, C.clone().add(V(Math.cos(ang) * len, Math.sin(ang) * len, 0)), a * .9);
    }
  }
  project(null, V(0, -1.4, 0), $("chips"), pName);

  // ---- one connection, then the split
  const one = life(t, T.p02, T.p04 + .05);
  server.visible = file.visible = one > .01;
  server.position.set(0, 1.05, 0); server.scale.setScalar(Math.max(.001, one) * .6);
  file.position.set(0, -1.15, 0); file.scale.setScalar(Math.max(.001, one));
  const capOn = win(t, T.cap - .1, T.cap + .3) * (1 - win(t, T.p03 - .2, T.p03 + .1));
  if (one > .01 && pSplit < .5) setBeam(V(0, .95, 0), V(0, -.72, 0), 1 - capOn * .55, one * (1 - capOn * .5));
  cap.visible = capOn > .01; cap.position.set(0, .12, .1); cap.scale.setScalar(Math.max(.001, back(capOn)));
  cap.rotation.z = t * 2;
  project(null, V(1.25, .12, .1), $("capTag"), capOn);
  const slow = win(t, T.p02, T.p03) * .12;
  barFill.visible = pSplit < .3; barFill.scale.x = Math.max(.001, 2.3 * slow); barFill.position.x = -1.15 + 1.15 * slow;
  const split = win(t, T.p03 + .3, T.once + .4);
  const nRays = Math.round(lerp(1, 32, ease(win(t, T.split, T.thirtytwo + .2))));
  cols.forEach((m, k) => {
    const on = pSplit > .3 && k < nRays;
    m.visible = on; const h = .62 * ease(win(t, T.p03 + .4 + k * .015, T.once + .9));
    m.scale.y = Math.max(.001, h); m.position.set(-1.15 + (k + .5) * (2.3 / 32), -.3 + h / 2 - .02, .1);
  });
  if (pSplit > .01) {
    setBeam(V(0, .95, 0), prism.position, 1, pSplit);
    for (let i = 0; i < nRays; i++) {
      const x = -1.15 + (i + .5) * (2.3 / 32);
      setRay(i, prism.position, V(x, -.78, 0), pSplit * .6);
    }
  }
  setText("nRays", String(nRays));
  project(null, V(1.42, .3, 0), $("nBig"), pSplit * win(t, T.split - .2, T.split + .1));
  project(file, V(0, .25, .1), $("fname"), one);

  // ---- work stealing: 8 lanes; lane 2 finishes early and takes half of the biggest part left (lane 5)
  const st = life(t, T.p04, T.p05 + .05);
  laneG.visible = st > .01; laneG.position.set(0, -.05, 0); laneG.scale.setScalar(Math.max(.001, st));
  const base = [.55, .62, .7, .5, .58, .3, .66, .48];
  const u = win(t, T.p04, T.half - .2), take = win(t, T.half - .1, T.half + .4), done = win(t, T.idle - .2, T.idle + .5);
  lanes.forEach((L, k) => {
    let p = Math.min(1, base[k] + u * (k === 2 ? .3 : .1));
    if (k === 5) p = lerp(p, p + (1 - p) * .1, take);
    p = lerp(p, 1, done);
    L.f.scale.x = Math.max(.001, 3.2 * p); L.f.position.x = -1.6 + 1.6 * p;
    L.h.position.x = -1.6 + 3.2 * p; L.h.visible = p < .999;
    L.f.material.opacity = k === 2 && u >= 1 && done < .01 ? .55 : 1;
  });
  // the stolen half: lane 5's remaining part splits; its back half lights green (lane 2's new work)
  const p5 = .4 + .1 * u, rem = 1 - p5, x0 = -1.6 + 3.2 * (p5 + rem / 2), wdt = 3.2 * rem / 2;
  stolen.visible = take > .01 && done < .99; stolen.position.set(x0 + wdt / 2, lanes[5].y, .03);
  stolen.scale.x = Math.max(.001, wdt * take * (1 - done));
  project(laneG, V(-1.25, lanes[2].y, .1), $("doneTag"), st * win(t, T.half - .6, T.half - .4) * (1 - done));
  project(laneG, V(x0 + wdt / 2, lanes[5].y + .26, .1), $("halfTag"), st * take * (1 - done));

  // ---- video card, 1,800+ sites, 8K, MP3 waveform
  const vd = life(t, T.p05, T.mp3 - .05), wv = life(t, T.mp3 - .15, T.p06 + .05);
  video.visible = vd > .01; video.position.set(0, .05, 0); video.scale.setScalar(Math.max(.001, back(vd)));
  video.rotation.set(-.08, Math.sin(t * .5) * .12, 0);
  project(video, V(1.2, .7, .2), $("k8"), vd * back(win(t, T.k8 - .1, T.k8 + .25)));
  setText("sites", Math.round(1800 * ease(win(t, T.eighteen - .3, T.eighteen + .6))).toLocaleString("en-US") + "+");
  project(null, V(0, -1.45, 0), $("sitesBox"), vd * win(t, T.eighteen - .3, T.eighteen));
  waveG.visible = wv > .01; waveG.position.set(0, .05, 0); waveG.scale.setScalar(Math.max(.001, wv));
  wave.forEach((m, k) => { const h = .15 + 1.4 * Math.abs(Math.sin(t * 6 + k * .55) * Math.sin(t * 2.3 + k * .2)) * Math.exp(-Math.pow((k - 19.5) / 14, 2)); m.scale.y = h; });

  // ---- laptop: battery dies at 63 %, lid shuts, opens, carries on from 63 %
  const lp = life(t, T.p06, T.p07 + .05);
  laptop.visible = lp > .01; laptop.position.set(0, -.75, 0); laptop.scale.setScalar(Math.max(.001, lp) * 1.05);
  laptop.rotation.set(.32, Math.sin(t * .4) * .15, 0);
  const shut = win(t, T.dies - .05, T.dies + .4) * (1 - win(t, T.picks - .2, T.picks + .3));
  lid.rotation.x = -.22 + easeIO(shut) * 1.33;
  const prog = t < T.picks ? Math.min(.63, .5 + win(t, T.p06, T.dies) * .13) : .63 + .37 * ease(win(t, T.picks + .3, T.stopped + 1.2));
  lbarF.scale.x = Math.max(.001, 1.9 * prog); lbarF.position.x = -.95 + .95 * prog;
  lscr.material.opacity = shut * .95;
  setText("pct", `${Math.round(prog * 100)}%`);
  project(lid, V(0, .95, .05), $("pct"), lp * (1 - shut));
  project(null, V(0, -1.22, 0), $("batt"), lp * win(t, T.p06 - .1, T.p06 + .2) * (1 - win(t, T.picks, T.picks + .3)));
  $("battFill") && ($("battFill").style.width = `${Math.max(4, 70 * (1 - win(t, T.p06, T.dies)))}%`);
  project(null, V(0, -1.22, 0), $("resumed"), lp * win(t, T.picks + .1, T.picks + .4));

  // ---- torrents (magnet) + Hugging Face (model card)
  const mg = life(t, T.p07, T.hugging + .05), cd = life(t, T.hugging - .15, T.p08 + .05);
  magnet.visible = mg > .01; magnet.position.set(0, .05, 0); magnet.scale.setScalar(Math.max(.001, back(mg)) * 1.2);
  magnet.rotation.set(.2, t * .9, Math.sin(t * 1.3) * .15);
  card.visible = cd > .01; card.position.set(0, .05, 0); card.scale.setScalar(Math.max(.001, back(cd)) * 1.15);
  card.rotation.set(-.05, Math.sin(t * .5) * .12, 0);
  project(card, V(0, 0, .1), $("model"), cd);

  // ---- the catch: every ray funnels through one pipe
  const ct = life(t, T.p08, T.p09 + .05);
  pipe.visible = ct > .01; pipe.position.set(1.2, .35, 0); pipe.scale.setScalar(Math.max(.001, ct));
  if (ct > .01) {
    for (let i = 0; i < RN; i++) {
      const y0 = (i / (RN - 1) - .5) * 2.6;
      setRay(i, V(-3.4, y0 * .7 + .35, 0), V(.4, .35 + y0 * .03, 0), ct * .7);
    }
    setBeam(V(.4, .35, 0), V(3.2, .35, 0), 1.6, ct);
  }
  project(null, V(1.2, .35, .3), $("pipeTag"), ct);
  project(null, V(0, -1.05, 0), $("bench"), ct * win(t, T.slow - .2, T.slow + .2));

  bloom.strength = .75 + pulse(t, T.seventeen, .3) * .3 + pulse(t, T.thirtytwo, .3) * .2;
  composer.render();
}

const ready = (async () => {
  try { await Promise.all(["800 40px Mont", "700 40px Inter"].map((f) => document.fonts.load(f))); } catch (e) { /* fallback */ }
  renderer.compile(scene, camera); renderAt(window.__hfThreeTime || 0);
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["scene"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
