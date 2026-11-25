// AI.NXTLVL "Your first 100 customers" (9:16): Sahil Lavingia's Minimalist Entrepreneur Claude skills. The 3D stage is a
// pure function of time t (rendered on HyperFrames' hf-seek). Beats come from window.FC_T (build/generate.py, from the
// voice's word times). Layout grid, all centred: headline band (HTML, y 300-560), 3D stage (~y 1000), caption (y ~1480).
// The cast: 100 little 3D customers (one instanced crowd) who change formation every beat:
//   hook    they rain in and build a giant "100"
//   stars   a glass jar fills with stars (11k)
//   find    three floating community islands; a magnifier hops between them; the crowd gathers on them
//   hand    a phone and a spreadsheet beat a code editor stuck at 0 lines
//   circles three rings: friends (10), community (30), strangers (60); envelopes fly out to the strangers
//   money   coin stacks rise: $10 a month x 200 customers
//   launch  a rocket locked on its pad; customers turn gold as they pay; at 100 it lifts off
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";

const W = 1080, H = 1920;
const T = window.FC_T;
const VIOLET = 0x7a2ffb, LAV = 0xb687f9, GOLD = 0xffc23d;
const PAL = [0xff6b6b, 0xffa94d, 0xffd43b, 0x69db7c, 0x38d9a9, 0x4dabf7, 0x748ffc, 0xda77f2, 0xf783ac];
const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H, false); renderer.setPixelRatio(1);
renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping;
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(34, W / H, .1, 100);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), .04).texture; scene.environmentIntensity = .45;
const composer = new EffectComposer(renderer);
composer.setSize(W, H); composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), .38, .45, .88); composer.addPass(bloom); composer.addPass(new OutputPass());
scene.add(new THREE.HemisphereLight(0xeee6ff, 0x1a1030, .7));
const key = new THREE.DirectionalLight(0xffffff, 1.35); key.position.set(-3, 7, 8); scene.add(key);
const rim = new THREE.PointLight(VIOLET, 50, 20); rim.position.set(3, 2, -3); scene.add(rim);

// ---------------------------------------------------------------- helpers
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const win = (t, a, b) => clamp((t - a) / (b - a));
const ease = (x) => 1 - Math.pow(1 - clamp(x), 3);
const easeIO = (x) => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const back = (x) => { x = clamp(x); const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const lerp = (a, b, x) => a + (b - a) * x;
const pulse = (t, at, w = .25) => Math.exp(-Math.pow((t - at) / w, 2));
const rnd = (i, k = 1) => { const s = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return s - Math.floor(s); };
const life = (t, a, b) => easeIO(win(t, a - .05, a + .4)) * (1 - easeIO(win(t, b - .35, b)));
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
const glow = (c, i = 1.4) => new THREE.MeshBasicMaterial({ color: new THREE.Color(c).multiplyScalar(i), transparent: true, toneMapped: false });
const plastic = (c) => new THREE.MeshPhysicalMaterial({ color: c, roughness: .35, clearcoat: .8, clearcoatRoughness: .2 });

// ---------------------------------------------------------------- the crowd: 100 little customers (instanced)
const N = 100;
const bodyGeo = new THREE.CapsuleGeometry(.075, .1, 6, 12); bodyGeo.translate(0, .125, 0);
const headGeo = new THREE.SphereGeometry(.072, 16, 12); headGeo.translate(0, .32, 0);
const bodies = new THREE.InstancedMesh(bodyGeo, new THREE.MeshPhysicalMaterial({ roughness: .35, clearcoat: .9 }), N);
const heads = new THREE.InstancedMesh(headGeo, new THREE.MeshPhysicalMaterial({ color: 0xffe2c6, roughness: .45, clearcoat: .5 }), N);
scene.add(bodies, heads);
const baseCol = [...Array(N)].map((_, i) => new THREE.Color(PAL[i % PAL.length]));
const tmpC = new THREE.Color(), m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), sc = new THREE.Vector3();
// "100" built from 100 points sampled from the glyphs
const P100 = (() => {
  const c = document.createElement("canvas"); c.width = 300; c.height = 140; const g = c.getContext("2d");
  g.fillStyle = "#000"; g.fillRect(0, 0, 300, 140); g.fillStyle = "#fff"; g.font = "900 128px Mont, Arial"; g.textAlign = "center"; g.textBaseline = "middle";
  g.fillText("100", 150, 74);
  const d = g.getImageData(0, 0, 300, 140).data, pts = [];
  for (let y = 4; y < 140; y += 7) for (let x = 4; x < 300; x += 7) if (d[(y * 300 + x) * 4] > 128) pts.push([x, y]);
  const out = [];
  for (let i = 0; i < N; i++) { const p = pts[Math.floor(i * pts.length / N)] || [150, 70]; out.push(V((p[0] - 150) / 300 * 3.9, (70 - p[1]) / 140 * 1.85, 0)); }
  return out;
})();
// formations
const ISL = [V(-1.25, .75, 0), V(1.25, .45, -.3), V(0, -.75, .3)];
const isle = (i) => { const k = i % 3, j = Math.floor(i / 3), a = j * 2.4, r = .12 + .07 * Math.sqrt(j); return ISL[k].clone().add(V(Math.cos(a) * r, .08, Math.sin(a) * r * .6)); };
const RINGS = [{ n: 10, r: .55 }, { n: 30, r: 1.15 }, { n: 60, r: 1.75 }];
const ringPos = (i) => { let k = 0, s = 0; while (i >= s + RINGS[k].n) { s += RINGS[k].n; k++; } const a = (i - s) / RINGS[k].n * Math.PI * 2 + k * .3; return V(Math.cos(a) * RINGS[k].r, -.2 + Math.sin(a) * RINGS[k].r * .42, Math.sin(a) * .2); };
const ringOf = (i) => (i < 10 ? 0 : i < 40 ? 1 : 2);
const queue = (i) => { const row = Math.floor(i / 20), col = i % 20; return V(-1.9 + col * .2, -1.25 + row * .16, -row * .12); };

// ---------------------------------------------------------------- props
const jar = new THREE.Group(); scene.add(jar);
jar.add(new THREE.Mesh(new THREE.CylinderGeometry(.85, .85, 1.9, 48, 1, true), new THREE.MeshPhysicalMaterial({ color: 0xffffff, transmission: .9, roughness: .05, thickness: .3, transparent: true, opacity: .35, side: THREE.DoubleSide, clearcoat: 1 })));
{ const lidm = new THREE.Mesh(new THREE.CylinderGeometry(.9, .9, .14, 48), plastic(0x2b2240)); lidm.position.y = 1.0; jar.add(lidm); }
const starShape = new THREE.Shape(); for (let k = 0; k < 10; k++) { const r = k % 2 ? .045 : .11, a = Math.PI / 2 + k * Math.PI / 5; k ? starShape.lineTo(Math.cos(a) * r, Math.sin(a) * r) : starShape.moveTo(Math.cos(a) * r, Math.sin(a) * r); }
const starGeo = new THREE.ExtrudeGeometry(starShape, { depth: .03, bevelEnabled: false }); starGeo.center();
const SN = 140, stars = new THREE.InstancedMesh(starGeo, new THREE.MeshPhysicalMaterial({ color: GOLD, metalness: .6, roughness: .25, emissive: 0x6b4500, emissiveIntensity: .4 }), SN); jar.add(stars);
const islands = ISL.map((p) => { const g = new THREE.Group(); g.position.copy(p); scene.add(g);
  const top = new THREE.Mesh(new THREE.CylinderGeometry(.55, .4, .16, 40), plastic(0x2e2450)); g.add(top);
  const rock = new THREE.Mesh(new THREE.DodecahedronGeometry(.42, 1), plastic(0x1d1733)); rock.scale.set(1.05, .55, .8); rock.position.y = -.22; g.add(rock);
  const rimL = new THREE.Mesh(new THREE.TorusGeometry(.55, .02, 8, 64), glow(LAV, 1.3)); rimL.rotation.x = Math.PI / 2; rimL.position.y = .08; g.add(rimL); return g; });
const mag = new THREE.Group(); scene.add(mag);
{ const ringM = new THREE.Mesh(new THREE.TorusGeometry(.28, .045, 12, 48), plastic(0xeeeeff)); mag.add(ringM);
  const lens = new THREE.Mesh(new THREE.CircleGeometry(.27, 40), new THREE.MeshPhysicalMaterial({ color: 0xbfe3ff, transmission: .9, transparent: true, opacity: .4 })); mag.add(lens);
  const hnd = new THREE.Mesh(new THREE.CylinderGeometry(.05, .05, .45, 16), plastic(VIOLET)); hnd.position.set(.3, -.3, 0); hnd.rotation.z = Math.PI / 4; mag.add(hnd); }
const phone = new THREE.Group(); scene.add(phone);
phone.add(new THREE.Mesh(new RoundedBoxGeometry(.85, 1.6, .09, 6, .12), plastic(0x15111f)));
{ const scr = new THREE.Mesh(new THREE.PlaneGeometry(.75, 1.45), new THREE.MeshBasicMaterial({ color: 0x241b44 })); scr.position.z = .05; phone.add(scr); }
const sheet = new THREE.Group(); scene.add(sheet);
sheet.add(new THREE.Mesh(new RoundedBoxGeometry(1.5, 1.1, .05, 4, .05), plastic(0xf4f1ea)));
for (let r = 0; r < 5; r++) for (let c2 = 0; c2 < 3; c2++) { const cell = new THREE.Mesh(new THREE.PlaneGeometry(.42, .15), new THREE.MeshBasicMaterial({ color: r === 0 ? 0x2f9e6b : 0xd9d4c8 })); cell.position.set(-.46 + c2 * .46, .38 - r * .2, .03); sheet.add(cell); }
const editor = new THREE.Group(); scene.add(editor);
editor.add(new THREE.Mesh(new RoundedBoxGeometry(1.6, 1.0, .05, 4, .05), plastic(0x0e0c18)));
for (let r = 0; r < 4; r++) { const ln = new THREE.Mesh(new THREE.PlaneGeometry(.3 + rnd(r) * .7, .06), new THREE.MeshBasicMaterial({ color: 0x3a3358 })); ln.position.set(-.55 + (.3 + rnd(r) * .7) / 2, .25 - r * .16, .03); editor.add(ln); }
const ringsG = new THREE.Group(); scene.add(ringsG);
const ringMeshes = RINGS.map((R, k) => { const m = new THREE.Mesh(new THREE.TorusGeometry(R.r, .015, 8, 128), glow([0xffc23d, 0xb687f9, 0x4dabf7][k], 1.3)); m.scale.set(1, .42, 1); m.rotation.x = 0; m.position.y = -.2; ringsG.add(m); return m; });
const EN = 24, envGeo = new THREE.BoxGeometry(.16, .11, .02), envs = new THREE.InstancedMesh(envGeo, new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: .4, clearcoat: .6 }), EN); scene.add(envs);
const coinGeo = new THREE.CylinderGeometry(.16, .16, .05, 32), CN = 60, coins = new THREE.InstancedMesh(coinGeo, new THREE.MeshPhysicalMaterial({ color: GOLD, metalness: .9, roughness: .25 }), CN); scene.add(coins);
const rocket = new THREE.Group(); scene.add(rocket);
{ const prof = []; for (let i = 0; i <= 20; i++) { const u = i / 20; prof.push(new THREE.Vector2(Math.max(.001, .32 * Math.sin(Math.min(1, u * 1.15) * Math.PI) ** .6 * (u < .75 ? 1 : (1 - u) * 4)), u * 1.6)); }
  const body = new THREE.Mesh(new THREE.LatheGeometry(prof, 32), plastic(0xf4f1ea)); rocket.add(body);
  const win1 = new THREE.Mesh(new THREE.CircleGeometry(.09, 24), glow(0x4dabf7, 1.2)); win1.position.set(0, 1.0, .3); rocket.add(win1);
  for (let k = 0; k < 3; k++) { const fin = new THREE.Mesh(new THREE.BoxGeometry(.04, .35, .28), plastic(VIOLET)); const a = k * 2 * Math.PI / 3; fin.position.set(Math.sin(a) * .27, .15, Math.cos(a) * .27); fin.rotation.y = a; rocket.add(fin); } }
const flame = new THREE.Mesh(new THREE.ConeGeometry(.2, .7, 24), glow(0xffa94d, 2)); flame.rotation.x = Math.PI; rocket.add(flame); flame.position.y = -.3;
const pad = new THREE.Mesh(new THREE.CylinderGeometry(.75, .85, .12, 40), plastic(0x2e2450)); scene.add(pad);

// ---------------------------------------------------------------- per frame
function crowd(t) {
  const kHook = life(t, -1, T.stars0 + .05), kFind = life(t, T.find, T.hand + .05), kCirc = life(t, T.friends, T.ten + .05), kLaunch = life(t, T.launch - .1, T.send + .2), kEnd = life(t, T.send, 99);
  const fall = (i) => ease(win(t, -.15 + rnd(i) * .5, .3 + rnd(i) * .5));
  const paidN = Math.round(100 * ease(win(t, T.launch + .2, T.paid + .3)));
  for (let i = 0; i < N; i++) {
    let p = null, s = 0, gold = 0, lit = 1;
    if (kHook > .01) {                                            // rain in, land into the "100"
      const f = fall(i), tgt = P100[i];
      p = V(tgt.x + (1 - f) * (rnd(i, 3) - .5) * 1.3, tgt.y + .05 + (1 - f) * (.35 + rnd(i, 4) * .45) + Math.abs(Math.sin((t - .6 - rnd(i) * .55) * 9)) * .12 * Math.exp(-Math.max(0, t - 1.0 - rnd(i) * .55) * 4) * (f >= 1 ? 1 : 0), 0);
      p.y += Math.sin(t * 3 + i) * .015; s = kHook;
    } else if (kFind > .01) {
      const g = ease(win(t, T.places - .2 + (i % 3) * .15, T.places + .6 + (i % 3) * .15));
      const from = V((rnd(i, 5) - .5) * 4, -2.2, 0); p = from.lerp(isle(i), g); s = kFind * g;
    } else if (kCirc > .01) {
      p = ringPos(i); const k = ringOf(i), tk = [T.friends, T.community, T.strangers][k];
      lit = .25 + .75 * win(t, tk - .1, tk + .3); s = kCirc * back(win(t, T.friends - .2 + k * .1, T.friends + .3 + k * .1));
    } else if (kLaunch > .01) {
      p = queue(i); s = kLaunch; gold = i < paidN ? 1 : 0;
    } else if (kEnd > .01) {
      p = P100[i].clone().multiplyScalar(.8).add(V(0, .9, 0)); s = kEnd * .8;
      p.y += Math.abs(Math.sin(t * 5 + i * .3)) * .06;
    }
    if (!p || s < .01) { m4.makeScale(0, 0, 0); bodies.setMatrixAt(i, m4); heads.setMatrixAt(i, m4); continue; }
    q.setFromAxisAngle(V(0, 1, 0), Math.sin(t * 2 + i) * .3); sc.setScalar(s * (kLaunch > .01 ? .8 : 1));
    m4.compose(p, q, sc); bodies.setMatrixAt(i, m4); heads.setMatrixAt(i, m4);
    tmpC.copy(baseCol[i]).lerp(new THREE.Color(GOLD), gold).multiplyScalar(lit); bodies.setColorAt(i, tmpC);
  }
  bodies.instanceMatrix.needsUpdate = heads.instanceMatrix.needsUpdate = true; if (bodies.instanceColor) bodies.instanceColor.needsUpdate = true;
  setText("paidN", String(paidN));
}

function renderAt(t) {
  const yaw = Math.sin(t * .35) * .07;
  camera.position.set(Math.sin(yaw) * 11.5, .6 + Math.sin(t * .27) * .08, Math.cos(yaw) * 11.5); camera.lookAt(0, .2, 0); camera.updateMatrixWorld(true);
  crowd(t);

  // stars jar (11k)
  const sj = life(t, T.stars0, T.find + .05);
  jar.visible = sj > .01; jar.position.set(0, .05, 0); jar.scale.setScalar(Math.max(.001, back(sj)) * .95); jar.rotation.y = t * .3;
  const fill = ease(win(t, T.eleven - .4, T.starred + .6));
  for (let i = 0; i < SN; i++) {
    const land = clamp(fill * 1.15 - i / SN * .9);
    const a = rnd(i) * Math.PI * 2, r = rnd(i, 2) * .65, yb = -.85 + (i / SN) * 1.4;
    m4.compose(V(Math.cos(a) * r, lerp(2.6, yb, ease(land)), Math.sin(a) * r), q.setFromEuler(new THREE.Euler(rnd(i, 3) * 6, t + i, 0)), sc.setScalar(land > 0 ? 1 : 0));
    stars.setMatrixAt(i, m4);
  }
  stars.instanceMatrix.needsUpdate = true;
  setText("starN", (Math.round(11000 * fill / 100) * 100).toLocaleString("en-US"));
  project(null, V(0, -1.45, 0), $("starBox"), sj);
  project(null, V(0, 1.55, 0), $("repo"), sj);

  // islands + magnifier (find)
  const fd = life(t, T.find, T.hand + .05);
  islands.forEach((g, k) => { g.visible = fd > .01; g.position.copy(ISL[k]).add(V(0, Math.sin(t * 1.2 + k) * .05, 0)); g.scale.setScalar(Math.max(.001, back(win(t, T.find + k * .12, T.find + .5 + k * .12)) * (1 - win(t, T.hand - .35, T.hand)))); });
  ["isl0", "isl1", "isl2"].forEach((id, k) => project(islands[k], V(0, -.62, 0), $(id), fd));
  const hop = (t - T.maps) / .8, hk = Math.floor(clamp(hop, 0, 2.99)), hu = hop - hk;
  mag.visible = fd > .01 && t > T.maps - .2;
  const mp = ISL[Math.min(2, hk)].clone().lerp(ISL[Math.min(2, hk + 1)], easeIO(clamp(hu * 1.6 - .6))).add(V(.15, .6, .5));
  mag.position.copy(mp); mag.scale.setScalar(Math.max(.001, fd * win(t, T.maps - .2, T.maps + .2)));
  mag.rotation.z = Math.sin(t * 2) * .2;

  // phone + sheet beat the code editor (hand)
  const hd = life(t, T.hand, T.friends + .05);
  phone.visible = sheet.visible = editor.visible = hd > .01;
  phone.position.set(-1.05, .35, 0); phone.rotation.set(0, .35 + Math.sin(t) * .05, -.05); phone.scale.setScalar(Math.max(.001, back(hd)) * .9);
  sheet.position.set(.75, .6, -.2); sheet.rotation.set(0, -.3, .04); sheet.scale.setScalar(Math.max(.001, back(win(t, T.hand + .1, T.hand + .5))) * hd);
  editor.position.set(.45, -.85, .3); editor.rotation.set(-.1, -.2, 0);
  editor.scale.setScalar(Math.max(.001, back(win(t, T.code - .4, T.code)) * hd * .85));
  project(editor, V(0, 0, .06), $("zero"), hd * win(t, T.code - .4, T.code));
  project(phone, V(0, .1, .06), $("dm"), hd * win(t, T.hand + .2, T.hand + .5));

  // circles + envelopes
  const cc = life(t, T.friends, T.ten + .05);
  ringsG.visible = cc > .01;
  ringMeshes.forEach((m, k) => { const tk = [T.friends, T.community, T.strangers][k]; m.scale.set(Math.max(.001, back(win(t, tk - .2, tk + .3))), .42 * Math.max(.001, back(win(t, tk - .2, tk + .3))), 1); m.material.opacity = cc; });
  ["rg0", "rg1", "rg2"].forEach((id, k) => { const R = RINGS[k].r; project(null, V(0, -.2 - R * .42 - .16, .3), $(id), cc * win(t, [T.friends, T.community, T.strangers][k] - .1, [T.friends, T.community, T.strangers][k] + .2)); });
  for (let i = 0; i < EN; i++) {
    const t0 = T.email - .6 + i * .07, u = win(t, t0, t0 + .9), a = i / EN * Math.PI * 2;
    const p = V(0, -.2, 0).lerp(V(Math.cos(a) * 1.75, -.2 + Math.sin(a) * 1.75 * .42, .2), ease(u)); p.y += Math.sin(u * Math.PI) * .5;
    m4.compose(p, q.setFromEuler(new THREE.Euler(0, 0, a)), sc.setScalar(cc * (u > 0 && u < 1 ? 1 : 0))); envs.setMatrixAt(i, m4);
  }
  envs.instanceMatrix.needsUpdate = true;
  project(null, V(0, 1.55, 0), $("gumroadTag"), cc * win(t, T.grew - .5, T.grew - .2));

  // money: coin stacks ($10 x 200)
  const mn = life(t, T.ten, T.launch - .05);
  for (let i = 0; i < CN; i++) {
    const stack = Math.floor(i / 12), lvl = i % 12, tt = T.ten + .1 + stack * .25 + lvl * .03, u = win(t, tt, tt + .25);
    m4.compose(V(-1.4 + stack * .7, -1.05 + lvl * .06 + (1 - ease(u)) * 1.5, 0), q.identity(), sc.setScalar(mn * (u > 0 ? 1 : 0))); coins.setMatrixAt(i, m4);
  }
  coins.instanceMatrix.needsUpdate = true;
  setText("mrr", "$" + (Math.round(2000 * ease(win(t, T.twothousand - .6, T.twothousand + .4)) / 10) * 10).toLocaleString("en-US"));
  project(null, V(0, .55, 0), $("math"), mn);

  // launch: locked until 100 paid, then lift-off
  const ln = life(t, T.launch - .1, T.send + .1), lift = ease(win(t, T.paid + .5, T.paid + 2.2));
  rocket.visible = pad.visible = ln > .01;
  pad.position.set(0, -.15, 0); pad.scale.setScalar(Math.max(.001, ln));
  rocket.position.set(0, -.1 + lift * 4 + Math.sin(t * 40) * .01 * win(t, T.paid + .2, T.paid + .5), 0); rocket.scale.setScalar(Math.max(.001, back(ln)) * .9); rocket.rotation.y = t * .6;
  flame.visible = t > T.paid + .3; flame.scale.set(1, .8 + Math.sin(t * 50) * .2, 1);
  project(null, V(0, -.62, 0), $("lock"), ln * (1 - win(t, T.paid + .2, T.paid + .5)));
  project(null, V(0, -.62, 0), $("go"), ln * win(t, T.paid + .3, T.paid + .6));
  project(null, V(1.55, .5, 0), $("paidBox"), ln);

  bloom.strength = .38 + pulse(t, T.paid + .4, .3) * .3;
  composer.render();
}

const ready = (async () => {
  try { await Promise.all(["900 40px Mont", "800 40px Mont", "700 40px Inter"].map((f) => document.fonts.load(f))); } catch (e) { /* fallback */ }
  renderer.compile(scene, camera); renderAt(window.__hfThreeTime || 0);
})();
window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["scene"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
