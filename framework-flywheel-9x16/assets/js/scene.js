// samarpit.ai "Framework in 30: Funnel vs flywheel" (9:16). The whole 3D scene is a pure function of time t, rendered on
// HyperFrames' hf-seek, so every frame is exact. Beats come from window.FF_T (written by build/generate.py from the
// voice's word timings). Labels that sit on 3D objects are projected from 3D each frame so they stay glued on.
//   hook:   customer orbs drop onto a glowing BUY pad, then vanish
//   funnel: a glass funnel; orbs spiral past ADS / VISIT / BUY, then fall out of the spout into the dark ("then nothing")
//   wheel:  the funnel collapses, a flywheel spins up; ATTRACT / SELL / DELIGHT / REFER light in turn, orbs loop round
//   tips:   the wheel drops lower and speeds up per tip; on "bring a friend" one orb splits into two
//   cta:    a small grey funnel is tossed away; on "spin" the wheel whips round with a light burst
import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";

const W = 1080, H = 1920;
const T = window.FF_T;
const STEEL = 0x5b8cff, AMBER = 0xffb020, CORAL = 0xff5a36, MUTE = 0x3a4252;
const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.setClearColor(0x07090d, 1);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;

const scene = new THREE.Scene();
scene.fog = new THREE.Fog(0x07090d, 12, 22);
const camera = new THREE.PerspectiveCamera(34, W / H, .1, 60);
const composer = new EffectComposer(renderer);
composer.setSize(W, H);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), .62, .5, .38);
composer.addPass(bloom);
composer.addPass(new OutputPass());

scene.add(new THREE.HemisphereLight(0xcfd8ff, 0x0b0d14, .9));
const key = new THREE.DirectionalLight(0xffffff, 2.2); key.position.set(3, 6, 6); scene.add(key);
const rimL = new THREE.PointLight(STEEL, 30, 14); rimL.position.set(-3.5, 1, 2); scene.add(rimL);
const rimR = new THREE.PointLight(AMBER, 0, 14); rimR.position.set(3.5, -1, 2); scene.add(rimR);

// ---------------------------------------------------------------- helpers
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const win = (t, a, b) => clamp((t - a) / (b - a));
const ease = (x) => 1 - Math.pow(1 - clamp(x), 3);
const easeIO = (x) => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const back = (x) => { x = clamp(x); const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const lerp = (a, b, x) => a + (b - a) * x;
const rnd = (i, k = 1) => { const s = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return s - Math.floor(s); };
const v3 = new THREE.Vector3();
function project(obj, local, el, dx = 0, dy = 0) {           // glue an HTML label to a point on a 3D object
  if (!el) return;
  v3.copy(local); obj.localToWorld(v3); v3.project(camera);
  el.style.transform = `translate(${(v3.x * .5 + .5) * W + dx}px, ${(-v3.y * .5 + .5) * H + dy}px) translate(-50%, -50%)`;
}
const $ = (id) => document.getElementById(id);

// ---------------------------------------------------------------- floor, dust
const floor = new THREE.Mesh(new THREE.CircleGeometry(9, 64), new THREE.MeshStandardMaterial({ color: 0x0c1018, roughness: .35, metalness: .6 }));
floor.rotation.x = -Math.PI / 2; floor.position.y = -3.6; scene.add(floor);
const grid = new THREE.GridHelper(18, 36, 0x1d2433, 0x131a26); grid.position.y = -3.59; grid.material.transparent = true; grid.material.opacity = .5; scene.add(grid);
const DN = 160, dust = new Float32Array(DN * 3);
const dustGeo = new THREE.BufferGeometry(); dustGeo.setAttribute("position", new THREE.BufferAttribute(dust, 3));
const dustPts = new THREE.Points(dustGeo, new THREE.PointsMaterial({ color: 0x9fb3ff, size: .035, transparent: true, opacity: .55 }));
scene.add(dustPts);

// ---------------------------------------------------------------- orbs (customers): one pool reused by every beat
const ON = 24;
const orbGeo = new THREE.SphereGeometry(.13, 24, 16);
const orbs = [];
for (let i = 0; i < ON; i++) {
  const m = new THREE.Mesh(orbGeo, new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: STEEL, emissiveIntensity: 1.6, roughness: .3, transparent: true }));
  m.visible = false; scene.add(m); orbs.push(m);
}
function orb(i, x, y, z, color, a = 1, s = 1, glow = 1.6) {
  const m = orbs[i]; m.visible = a > .01; m.position.set(x, y, z); m.scale.setScalar(Math.max(.001, s));
  m.material.opacity = a; m.material.emissive.setHex(color); m.material.emissiveIntensity = glow;
}

// ---------------------------------------------------------------- the BUY pad (hook)
const pad = new THREE.Group(); scene.add(pad);
const padTop = new THREE.Mesh(new THREE.CylinderGeometry(1.15, 1.25, .22, 64), new THREE.MeshStandardMaterial({ color: 0x141922, metalness: .7, roughness: .3, emissive: STEEL, emissiveIntensity: .25 }));
pad.add(padTop);
const padRing = new THREE.Mesh(new THREE.TorusGeometry(1.2, .035, 12, 96), new THREE.MeshBasicMaterial({ color: STEEL, transparent: true }));
padRing.rotation.x = Math.PI / 2; padRing.position.y = .12; pad.add(padRing);

// ---------------------------------------------------------------- the funnel (glass lathe)
const prof = [];
for (let i = 0; i <= 40; i++) {
  const u = i / 40, y = 2.1 - u * 4.2;
  const r = u < .72 ? lerp(1.75, .32, Math.pow(u / .72, .85)) : .32 - (u - .72) * .12;
  prof.push(new THREE.Vector2(r, y));
}
const funnelR = (y) => { const u = (2.1 - y) / 4.2; return u < .72 ? lerp(1.75, .32, Math.pow(clamp(u) / .72, .85)) : .32 - (u - .72) * .12; };
const funnel = new THREE.Group(); scene.add(funnel);
const fspin = new THREE.Group(); funnel.add(fspin);                   // the glass turns; the labels stay on the front
const glassMat = new THREE.MeshPhysicalMaterial({ color: 0x8fb0ff, metalness: 0, roughness: .08, transmission: 0, transparent: true, opacity: .22,
  side: THREE.DoubleSide, emissive: STEEL, emissiveIntensity: .12, clearcoat: 1 });
fspin.add(new THREE.Mesh(new THREE.LatheGeometry(prof, 96), glassMat));
const funnelWire = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.LatheGeometry(prof.filter((_, i) => i % 4 === 0), 24), 1),
  new THREE.LineBasicMaterial({ color: STEEL, transparent: true, opacity: .55 }));
fspin.add(funnelWire);
const levelRings = [1.25, -.15, -1.3].map((y) => {
  const r = new THREE.Mesh(new THREE.TorusGeometry(funnelR(y) + .02, .03, 10, 96), new THREE.MeshBasicMaterial({ color: STEEL, transparent: true, opacity: .4 }));
  r.rotation.x = Math.PI / 2; r.position.y = y; funnel.add(r); return r;
});
const lipRing = new THREE.Mesh(new THREE.TorusGeometry(1.76, .05, 12, 128), new THREE.MeshBasicMaterial({ color: STEEL, transparent: true }));
lipRing.rotation.x = Math.PI / 2; lipRing.position.y = 2.1; funnel.add(lipRing);

// small grey funnel tossed away in the CTA
const mini = new THREE.Group(); scene.add(mini);
mini.add(new THREE.Mesh(new THREE.LatheGeometry(prof, 48), new THREE.MeshStandardMaterial({ color: 0x9aa3b5, roughness: .45, metalness: .3, emissive: 0x5b8cff, emissiveIntensity: .12, side: THREE.DoubleSide, transparent: true })));
mini.scale.setScalar(.35);

// ---------------------------------------------------------------- the flywheel: 4 arc segments, hub, spokes, inner dashes
const wheel = new THREE.Group(); scene.add(wheel);
const WR = 1.3;
const segs = [];
// segment k is centred on a diagonal: 0 ATTRACT (top right), 1 SELL (bottom right), 2 DELIGHT (bottom left), 3 REFER (top left)
const segAng = [Math.PI / 4, -Math.PI / 4, -3 * Math.PI / 4, 3 * Math.PI / 4];
for (let k = 0; k < 4; k++) {
  const arc = Math.PI / 2 - .16;
  const g = new THREE.TorusGeometry(WR, .17, 20, 64, arc);
  const m = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: 0x232a37, metalness: .55, roughness: .3, emissive: AMBER, emissiveIntensity: 0 }));
  m.rotation.z = segAng[k] - arc / 2; wheel.add(m); segs.push(m);
  // arrow head at the clockwise end of each segment
  const head = new THREE.Mesh(new THREE.ConeGeometry(.2, .34, 20), m.material);
  const a1 = segAng[k] - arc / 2 - .02;
  head.position.set(Math.cos(a1) * WR, Math.sin(a1) * WR, 0); head.rotation.z = a1 + Math.PI; wheel.add(head);
}
const spin = new THREE.Group(); wheel.add(spin);                       // the part that turns
const hub = new THREE.Mesh(new THREE.CylinderGeometry(.34, .34, .26, 48), new THREE.MeshStandardMaterial({ color: 0x1b2230, metalness: .8, roughness: .25, emissive: AMBER, emissiveIntensity: .2 }));
hub.rotation.x = Math.PI / 2; spin.add(hub);
for (let k = 0; k < 6; k++) {
  const sp = new THREE.Mesh(new THREE.BoxGeometry(.06, WR - .55, .06), new THREE.MeshStandardMaterial({ color: 0x3a4456, metalness: .6, roughness: .3, emissive: AMBER, emissiveIntensity: .15 }));
  const a = k / 6 * Math.PI * 2; sp.position.set(Math.cos(a) * (WR / 2 + .1), Math.sin(a) * (WR / 2 + .1), 0); sp.rotation.z = a - Math.PI / 2; spin.add(sp);
}
const dashes = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.TorusGeometry(WR - .42, .001, 2, 36)), new THREE.LineBasicMaterial({ color: AMBER, transparent: true, opacity: .5 }));
spin.add(dashes);
const burst = new THREE.Mesh(new THREE.RingGeometry(1, 1.06, 96), new THREE.MeshBasicMaterial({ color: AMBER, transparent: true, opacity: 0, side: THREE.DoubleSide }));
wheel.add(burst);

// ---------------------------------------------------------------- per frame
const segLit = [0, 0, 0, 0];
function renderAt(t) {
  // camera: slow drift, a swing between funnel and wheel
  const sw = easeIO(win(t, T.wheel - .25, T.wheel + .9));
  const camA = lerp(.18, -.12, sw) + Math.sin(t * .35) * .04;
  const camR = 12.2 - easeIO(win(t, 0, 3)) * .5 + sw * .4;
  camera.position.set(Math.sin(camA) * camR, lerp(1.6, .9, sw), Math.cos(camA) * camR);
  camera.lookAt(0, lerp(-.35, -.45, sw), 0);
  camera.updateMatrixWorld();

  // dust drifts up forever
  for (let i = 0; i < DN; i++) {
    dust[i * 3] = (rnd(i) - .5) * 9; dust[i * 3 + 2] = (rnd(i, 2) - .5) * 6 - 1;
    dust[i * 3 + 1] = ((rnd(i, 3) * 8 + t * (.12 + rnd(i, 4) * .2)) % 8) - 4;
  }
  dustGeo.attributes.position.needsUpdate = true;
  orbs.forEach((o) => (o.visible = false));

  // ---- hook: orbs drop onto the BUY pad, then vanish
  const padIn = ease(win(t, 0, .35)), padOut = win(t, T.funnel - .3, T.funnel + .1);
  pad.visible = padOut < 1;
  pad.position.set(0, -1.2, 0); pad.scale.setScalar(Math.max(.001, padIn * (1 - padOut)));
  const vanish = T.vanish;
  const padGlow = .25 + .6 * Math.exp(-Math.pow((t - .6) / .25, 2));
  padTop.material.emissiveIntensity = padGlow * (1 - win(t, vanish, vanish + .4) * .7);
  padRing.material.opacity = .9 - win(t, vanish, vanish + .5) * .6;
  for (let i = 0; i < 5 && t < T.funnel; i++) {
    const t0 = .05 + i * .1, land = t0 + .45;
    const ang = (i / 5) * Math.PI * 2 + .3, rr = .55 + (i % 2) * .25;
    let y;
    if (t < land) y = lerp(5, -1.0, Math.pow(win(t, t0, land), 2));
    else { const b = t - land; y = -1.0 + Math.abs(Math.sin(b * 9)) * .5 * Math.exp(-b * 6); }
    const v = win(t, vanish + i * .06, vanish + i * .06 + .35);
    orb(i, Math.cos(ang) * rr, y, Math.sin(ang) * rr, STEEL, (t > t0 ? 1 : 0) * (1 - v), (1 + v * .8) * (1 - v * .9));
  }

  // ---- funnel
  const fIn = back(win(t, T.funnel - .1, T.funnel + .5));
  const fOut = easeIO(win(t, T.wheel - .2, T.wheel + .45));
  funnel.visible = fIn > .001 && fOut < .999;
  const FS = .86;
  funnel.scale.set(FS * fIn * (1 - fOut * .6), FS * fIn * (1 - fOut), FS * fIn * (1 - fOut * .6));
  funnel.position.y = -1.1 - fOut * 1.2;
  funnel.rotation.set(lerp(.5, .12, ease(win(t, T.funnel - .1, T.funnel + .7))), 0, fOut * 1.2);
  fspin.rotation.y = t * .35;
  funnel.updateMatrixWorld(true);                                     // fresh matrices: labels and orbs read them this frame
  const dead = win(t, T.nothing, T.nothing + .6);                     // "then nothing": it goes cold and grey
  const funCol = new THREE.Color(STEEL).lerp(new THREE.Color(MUTE), dead);
  glassMat.emissive.copy(funCol); funnelWire.material.color.copy(funCol); lipRing.material.color.copy(funCol);
  rimL.intensity = 30 * (1 - dead * .7);
  const lv = [T.ads, T.visit, T.buy];
  levelRings.forEach((r, k) => {
    const hit = Math.exp(-Math.pow((t - lv[k] - .1) / .3, 2));
    r.material.opacity = (t > lv[k] ? .55 : .2) + hit * .45 - dead * .3;
    r.material.color.copy(funCol).lerp(new THREE.Color(0xffffff), hit * .6);
  });
  ["lab-ads", "lab-visit", "lab-buy"].forEach((id, k) => project(funnel, new THREE.Vector3(0, [1.25, -.15, -1.3][k], funnelR([1.25, -.15, -1.3][k]) + .08), $(id), 0, 0));
  // orbs pour in at the lip and spiral down; after "nothing" they drop out of the spout into the dark
  if (fIn > .01 && fOut < .9) {
    for (let i = 0; i < 12; i++) {
      const start = T.funnel + .15 + i * .23, life = 1.7;
      const u = (t - start) / life;
      if (u < 0) continue;
      const ph = rnd(i, 7) * 6.28;
      let x, y, z, a = 1;
      if (u <= 1) {
        y = 2.0 - u * 3.9; const r = funnelR(y) * .78, ang = ph + u * 9;
        x = Math.cos(ang) * r; z = Math.sin(ang) * r;
      } else {
        const f = (u - 1) * life; y = -1.9 - f * 1.2 - 4.9 * f * f; x = Math.sin(ph) * f * .3; z = Math.cos(ph) * f * .3;
        a = Math.max(0, 1 - f * 1.4);
      }
      v3.set(x, y, z); funnel.localToWorld(v3);
      const col = t > T.nothing && u > 1 ? CORAL : STEEL;
      orb(5 + i, v3.x, v3.y, v3.z, col, a * (1 - fOut), 1);
    }
  }

  // ---- flywheel
  const wIn = back(win(t, T.wheel, T.wheel + .7));
  wheel.visible = wIn > .001;
  const tipY = easeIO(win(t, T.tip1 - .35, T.tip1 + .35));
  const ctaUp = easeIO(win(t, T.cta - .1, T.cta + .5));
  wheel.position.set(0, lerp(-.35, -1.25, tipY) + ctaUp * .45, 0);
  wheel.scale.setScalar(wIn * lerp(.86, .8, tipY) * (1 + ctaUp * .1));
  wheel.rotation.set(-.22 + Math.sin(t * .6) * .04, Math.sin(t * .4) * .045, (1 - wIn) * -1.6);
  // spin speed: idles, steps up on every tip, whips round on "spin"
  const sp = 1.2 + win(t, T.tip1, T.tip1 + .5) * .7 + win(t, T.tip2, T.tip2 + .5) * .7 + win(t, T.tip3, T.tip3 + .5) * .9;
  const whip = easeIO(win(t, T.spin, T.spin + 1.2));
  const ang = -((t - T.wheel) * sp + whip * 9);                         // clockwise
  spin.rotation.z = ang;
  const wordT = [T.attract, T.sell, T.delight, T.refer];
  const tipSeg = [[T.tip1, 2], [T.tip2, 2], [T.tip3, 3]];
  for (let k = 0; k < 4; k++) {
    let lit = t > wordT[k] ? 1 : 0;
    let pulse = Math.exp(-Math.pow((t - wordT[k] - .12) / .25, 2));
    tipSeg.forEach(([tt, s]) => { if (s === k) pulse = Math.max(pulse, Math.exp(-Math.pow((t - tt - .3) / .35, 2))); });
    pulse = Math.max(pulse, whip > 0 && whip < 1 ? .6 : 0);
    segs[k].material.color.setHex(lit ? 0x3a2a10 : 0x232a37);
    segs[k].material.emissiveIntensity = lit * .4 + pulse * 1.2;
    segLit[k] = lit;
  }
  wheel.updateMatrixWorld(true);
  rimR.intensity = wIn * 22;
  burst.material.opacity = Math.max(0, 1 - win(t, T.spin, T.spin + .9)) * (t > T.spin ? .9 : 0);
  burst.scale.setScalar(1.2 + win(t, T.spin, T.spin + .9) * 1.6);
  ["lab-attract", "lab-sell", "lab-delight", "lab-refer"].forEach((id, k) => {
    const a = segAng[k], r = WR + .5;
    project(wheel, new THREE.Vector3(Math.cos(a) * r, Math.sin(a) * r, 0), $(id));
  });
  // orbs ride the rim clockwise; each lap they pass ATTRACT again ("puts them back in"); "bring a friend" adds one
  if (wIn > .01) {
    const n = t > T.friend ? 7 : 6;
    for (let i = 0; i < n; i++) {
      let a = (i / 6) * Math.PI * 2 + ang * .9;
      let s = 1, al = 1;
      if (i === 6) {                                                 // the friend: splits off orb 0, then joins the ride
        const f = ease(win(t, T.friend, T.friend + .6));
        a = (0 / 6) * Math.PI * 2 + ang * .9 - f * (Math.PI / 6);
        s = .4 + f * .6;
      }
      const r = WR, x = Math.cos(a) * r, y = Math.sin(a) * r;
      v3.set(x, y, .26); wheel.localToWorld(v3);
      orb(17 + i, v3.x, v3.y, v3.z, AMBER, al * wIn, s * 1.0, 1.3);
    }
  }

  // ---- CTA: the small grey funnel is tossed away
  const mIn = ease(win(t, T.cta, T.cta + .35)), mOut = win(t, T.funnelWord + .25, T.funnelWord + .9);
  mini.visible = mIn > .01 && mOut < 1;
  mini.position.set(lerp(-1.3, -4.5, mOut * mOut), lerp(1.0, 2.8, mOut), .5);
  mini.rotation.set(.3, t, lerp(.2, 3.5, mOut));
  mini.children[0].material.opacity = 1 - mOut;
  mini.scale.setScalar(.27 * mIn);

  composer.render();
}

const ready = (async () => { renderer.compile(scene, camera); renderAt(window.__hfThreeTime || 0); })();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["scene"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
