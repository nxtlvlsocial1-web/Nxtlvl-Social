// Fight Night: the 3D world. Everything is a pure function of time t (seconds), rendered on HyperFrames' hf-seek.
// Sets: the arena (ring, ropes, posts, spotlights, big screen, crowd, judges' table), the "yes-man" room for the
// problem line, and the championship-belt podium for the CTA. Characters are the orange pixel mascot rebuilt from
// rounded boxes: two fighters (red / blue gloves), a striped referee, twelve judges with persona props and flip cards.
import * as THREE from "three";
import { RoundedBoxGeometry } from "./../vendor/three/addons/geometries/RoundedBoxGeometry.js";

const W = 1080, H = 1920;
const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.NeutralToneMapping;
renderer.toneMappingExposure = 1.0;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(38, W / H, 0.1, 200);

// ---------------------------------------------------------------- helpers
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, k) => a + (b - a) * k;
const easeIO = (k) => (k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
const easeOut = (k) => 1 - Math.pow(1 - k, 3);
const easeIn = (k) => k * k * k;
const backOut = (k) => { const c = 1.7; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); };
const win = (t, a, b) => clamp((t - a) / (b - a));
const pulse = (t, at, up = .08, down = .35) => (t < at ? 0 : t < at + up ? (t - at) / up : Math.max(0, 1 - (t - at - up) / down));
const rb = (w, h, d, r = .08, seg = 3) => new RoundedBoxGeometry(w, h, d, seg, Math.min(r, w / 2, h / 2, d / 2));
const mat = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: .55, metalness: 0, ...o });
function mesh(geo, m, shadow = true) { const x = new THREE.Mesh(geo, m); x.castShadow = shadow; x.receiveShadow = true; return x; }
function hash(i) { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); }

const ORANGE = 0xFF7436, INK = 0x111111;

// ---------------------------------------------------------------- the mascot
function mascot({ glove = null, shorts = null, scale = 1, stripes = false } = {}) {
  const root = new THREE.Group();          // world placement
  const hop = new THREE.Group();           // bounce / jumps / falls
  const body = new THREE.Group();          // squash + lean
  root.add(hop); hop.add(body);
  const bodyMat = mat(ORANGE, { roughness: .5 });
  const torso = mesh(rb(1.5, 1.08, 1.08, .2, 4), bodyMat);
  torso.position.y = .32 + .54;
  body.add(torso);
  if (stripes) {
    for (let i = 0; i < 5; i++) {
      const s = mesh(rb(1.53, .1, 1.11, .03, 2), mat(i % 2 ? 0xffffff : INK));
      s.position.y = .42 + i * .13; body.add(s);
    }
    const bow = mesh(rb(.3, .12, .08, .04, 2), mat(INK)); bow.position.set(0, 1.08, .56); body.add(bow);
  }
  if (shorts) {
    const s = mesh(rb(1.54, .34, 1.12, .12, 3), mat(shorts, { roughness: .4 }));
    s.position.y = .5; body.add(s);
    const belt = mesh(rb(1.56, .08, 1.14, .03, 2), mat(0xffffff)); belt.position.y = .68; body.add(belt);
  }
  const eyes = [];
  for (const x of [-.32, .32]) {
    const e = mesh(rb(.14, .36, .08, .05, 2), mat(INK, { roughness: .2 }), false);
    e.position.set(x, .98, .55); body.add(e); eyes.push(e);
  }
  const arms = [];
  for (const side of [-1, 1]) {
    const arm = new THREE.Group();
    arm.position.set(side * .82, .86, 0);
    if (glove) {
      const g = mesh(rb(.44, .42, .48, .16, 3), mat(glove, { roughness: .32, metalness: .05 }));
      g.position.set(side * .06, .02, .3); arm.add(g);
      const cuff = mesh(rb(.38, .38, .12, .04, 2), mat(0xffffff)); cuff.position.set(side * .06, .02, .02); arm.add(cuff);
    } else {
      const n = mesh(rb(.26, .26, .3, .07, 2), bodyMat); arm.add(n);
    }
    body.add(arm); arms.push(arm);
  }
  const legs = [];
  for (const [x, z] of [[-.5, .3], [-.18, .3], [.18, .3], [.5, .3]]) {
    const l = mesh(rb(.2, .34, .22, .05, 2), bodyMat); l.position.set(x, .17, z - .15); body.add(l); legs.push(l);
  }
  root.scale.setScalar(scale);
  return { root, hop, body, eyes, arms, legs, torso };
}

function blink(m, t, phase = 0) {
  const k = (t + phase) % 3.1;
  const s = k < .12 ? 1 - Math.sin(k / .12 * Math.PI) * .9 : 1;
  m.eyes.forEach((e) => (e.scale.y = s));
}

// ---------------------------------------------------------------- arena
const arena = new THREE.Group(); scene.add(arena);
const floor = mesh(new THREE.CircleGeometry(40, 48), mat(0x14101f, { roughness: .9 })); floor.rotation.x = -Math.PI / 2; arena.add(floor);
const RING_H = .6, RS = 7.2;
const apron = mesh(rb(RS + .4, RING_H, RS + .4, .06, 2), mat(0x1d1d2b)); apron.position.y = RING_H / 2; arena.add(apron);
const canvasTop = mesh(new THREE.BoxGeometry(RS, .04, RS), mat(0xe9e6f0, { roughness: .8 })); canvasTop.position.y = RING_H + .02; arena.add(canvasTop);
// ring logo ring
const logo = mesh(new THREE.RingGeometry(1.2, 1.45, 48), mat(0xE8794A, { roughness: .6 }), false); logo.rotation.x = -Math.PI / 2; logo.position.y = RING_H + .045; arena.add(logo);
const posts = [[-1, -1, 0xd8343f], [1, 1, 0x2f6bff], [1, -1, 0xeeeeee], [-1, 1, 0xeeeeee]];
for (const [sx, sz, c] of posts) {
  const p = mesh(rb(.24, 1.9, .24, .06, 2), mat(c, { roughness: .35 }));
  p.position.set(sx * RS / 2, RING_H + .95, sz * RS / 2); arena.add(p);
  const pad = mesh(rb(.34, 1.0, .34, .1, 2), mat(c, { roughness: .4 })); pad.position.set(sx * RS / 2, RING_H + 1.15, sz * RS / 2); arena.add(pad);
}
const ropeCols = [0xd8343f, 0xffffff, 0x2f6bff];
const frontRopes = [];
for (let i = 0; i < 3; i++) {
  const y = RING_H + .55 + i * .45;
  for (const [x, z, rot] of [[0, -RS / 2, 0], [0, RS / 2, 0], [-RS / 2, 0, Math.PI / 2], [RS / 2, 0, Math.PI / 2]]) {
    const r = mesh(new THREE.CylinderGeometry(.045, .045, RS, 10), mat(ropeCols[i], { roughness: .3 }), false);
    r.rotation.z = Math.PI / 2; r.rotation.y = rot; r.position.set(x, y, z); arena.add(r);
    if (z > 0) frontRopes.push(r);
  }
}
// crowd: instanced mascots in tiers behind the ring
const crowdGeo = rb(.9, .7, .7, .14, 2);
const crowdMat = mat(0xffffff, { roughness: .7 });
const CROWD = 260;
const crowd = new THREE.InstancedMesh(crowdGeo, crowdMat, CROWD);
const crowdBase = [];
const tmpM = new THREE.Matrix4(), tmpQ = new THREE.Quaternion(), tmpS = new THREE.Vector3(), tmpP = new THREE.Vector3();
for (let i = 0; i < CROWD; i++) {
  const tier = i % 5, k = Math.floor(i / 5);
  const ang = -1.25 + (k / (CROWD / 5)) * 2.5 + (tier % 2) * .02;
  const r = 13 + tier * 1.5;
  const x = Math.sin(ang) * r, z = -Math.cos(ang) * r + 2;
  const y = .4 + tier * 1.0;
  crowdBase.push([x, y, z, hash(i) * 6.28, -ang]);
  const hue = hash(i + 7);
  crowd.setColorAt(i, new THREE.Color().setHSL(hue < .7 ? .05 + hue * .05 : .75 + hue * .1, .55, .32 + hash(i + 3) * .18));
}
crowd.instanceColor.needsUpdate = true;
arena.add(crowd);
// stands behind the crowd
for (let tier = 0; tier < 5; tier++) {
  const st = mesh(new THREE.CylinderGeometry(13.5 + tier * 1.5, 13.5 + tier * 1.5, .5, 64, 1, true, -1.35, 2.7), mat(0x221a33, { side: THREE.DoubleSide }), false);
  st.position.set(0, tier * 1.0, 2); st.rotation.y = Math.PI; arena.add(st);
}

// big screen above the ring
function screenTexture(draw) {
  const c = document.createElement("canvas"); c.width = 1024; c.height = 600;
  const g = c.getContext("2d"); draw(g, c.width, c.height);
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; return tx;
}
const screenGroup = new THREE.Group(); screenGroup.position.set(0, 7.3, -5.5); arena.add(screenGroup);
const screenFrame = mesh(rb(6.6, 3.9, .3, .1, 2), mat(0x0c0c12, { metalness: .4, roughness: .4 })); screenGroup.add(screenFrame);
const screenMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
const screenPlane = new THREE.Mesh(new THREE.PlaneGeometry(6.2, 3.62), screenMat); screenPlane.position.z = .16; screenGroup.add(screenPlane);
const screenTex = {};

// judges' table on a riser behind the ring
const judgesGroup = new THREE.Group(); judgesGroup.position.set(0, 0, -9.2); arena.add(judgesGroup);
const riser = mesh(rb(16, 1.2, 2.4, .06, 2), mat(0x2a2140)); riser.position.y = .6; judgesGroup.add(riser);
const table = mesh(rb(15.6, .14, 1.0, .05, 2), mat(0xf2ede4, { roughness: .6 })); table.position.set(0, 1.5, .75); judgesGroup.add(table);
const tableFront = mesh(rb(15.6, .5, .08, .03, 2), mat(0xd8343f, { roughness: .5 })); tableFront.position.set(0, 1.2, 1.24); judgesGroup.add(tableFront);
const judges = [];
const PROPS = ["calculator", "bag", "trophy", "wig", "cap", "hardhat", "apron", "chart", "baby", "briefcase", "beret", "tophat"];
for (let i = 0; i < 12; i++) {
  const m = mascot({ scale: .62 });
  const x = -6.6 + i * 1.2;
  m.root.position.set(x, 1.25, 0);
  judgesGroup.add(m.root);
  // divider between judges so nobody sees the next card
  if (i < 11) {
    const dv = mesh(new THREE.BoxGeometry(.05, .9, 1.0), new THREE.MeshStandardMaterial({ color: 0xbfd8ff, transparent: true, opacity: .35, roughness: .1 }), false);
    dv.position.set(x + .6, 2.0, .6); judgesGroup.add(dv);
  }
  // persona prop
  const p = new THREE.Group(); m.body.add(p);
  const kind = PROPS[i];
  if (kind === "calculator") { const c = mesh(rb(.5, .62, .12, .04), mat(0x8a8f99)); c.position.set(.55, .9, .7); p.add(c); const s = mesh(new THREE.BoxGeometry(.38, .14, .02), mat(0x9fd68a)); s.position.set(.55, 1.1, .77); p.add(s); }
  if (kind === "bag") { const c = mesh(rb(.5, .55, .3, .05), mat(0xff5fa2)); c.position.set(.62, .7, .55); p.add(c); const h = mesh(new THREE.TorusGeometry(.14, .03, 8, 16, Math.PI), mat(0xff5fa2)); h.position.set(.62, .98, .55); p.add(h); }
  if (kind === "trophy") { const c = mesh(new THREE.CylinderGeometry(.2, .1, .35, 16), mat(0xf4c542, { metalness: .6, roughness: .3 })); c.position.set(.6, 1.0, .55); p.add(c); const b = mesh(rb(.3, .12, .3, .03), mat(0xf4c542, { metalness: .6, roughness: .3 })); b.position.set(.6, .76, .55); p.add(b); }
  if (kind === "wig") { for (let k = 0; k < 7; k++) { const s = mesh(new THREE.SphereGeometry(.22, 14, 10), mat(0xf5f5f0)); s.position.set(-.6 + k * .2, 1.42 + (k % 2) * .05, -.05); p.add(s); } }
  if (kind === "cap") { const c = mesh(new THREE.SphereGeometry(.5, 20, 12, 0, Math.PI * 2, 0, Math.PI / 2), mat(0x2f6bff)); c.position.set(0, 1.4, 0); c.scale.set(1.2, .55, 1); p.add(c); const v = mesh(rb(.6, .05, .5, .02), mat(0x2f6bff)); v.position.set(0, 1.42, -.6); p.add(v); }
  if (kind === "hardhat") { const c = mesh(new THREE.SphereGeometry(.55, 20, 12, 0, Math.PI * 2, 0, Math.PI / 2), mat(0xffcc1a, { roughness: .35 })); c.position.set(0, 1.4, 0); c.scale.set(1.25, .6, 1.05); p.add(c); }
  if (kind === "apron") { const c = mesh(rb(1.0, .6, .05, .03), mat(0x3e8e62)); c.position.set(0, .66, .56); p.add(c); }
  if (kind === "chart") { [.25, .45, .65].forEach((h, k) => { const b = mesh(rb(.13, h, .1, .02), mat([0x2f6bff, 0xf4c542, 0xd8343f][k])); b.position.set(.42 + k * .17, .5 + h / 2 + .2, .6); p.add(b); }); }
  if (kind === "baby") { const c = mascot({ scale: .32 }); c.root.position.set(.9, .3, .3); p.add(c.root); }
  if (kind === "tophat") { const c = mesh(new THREE.CylinderGeometry(.34, .34, .55, 20), mat(INK, { roughness: .3 })); c.position.set(0, 1.68, 0); p.add(c); const r = mesh(new THREE.CylinderGeometry(.55, .55, .05, 20), mat(INK)); r.position.set(0, 1.42, 0); p.add(r); }
  if (kind === "beret") { const c = mesh(new THREE.SphereGeometry(.5, 20, 12), mat(0xd8343f)); c.scale.set(1.05, .28, .9); c.position.set(.1, 1.45, 0); p.add(c); }
  if (kind === "briefcase") { const c = mesh(rb(.6, .45, .2, .05), mat(0x7a4a2a)); c.position.set(.6, .7, .55); p.add(c); }
  // scorecard: white side faces the camera, red "GUILTY" on the back, flipped when the vote is read
  const card = new THREE.Group(); card.position.set(-.15, 1.75, 1.0); m.body.add(card);
  const cardMesh = new THREE.Mesh(new THREE.BoxGeometry(.7, .5, .03), [mat(0xffffff), mat(0xffffff), mat(0xffffff), mat(0xffffff), mat(0xffffff), mat(0xd8343f)]);
  cardMesh.castShadow = true; card.add(cardMesh);
  card.visible = false;
  judges.push({ m, card, i });
}
const judgeFill = new THREE.SpotLight(0xfff0dd, 0, 30, .7, .6, 1); judgeFill.position.set(0, 9, -4); judgeFill.target.position.set(0, 1.5, -9.2);
arena.add(judgeFill); arena.add(judgeFill.target);
const judgeLights = [];
for (let i = 0; i < 12; i++) {
  const l = new THREE.SpotLight(0xffe6c7, 0, 9, .32, .6, 1.2); l.position.set(-6.6 + i * 1.2, 7, -7.4);
  l.target.position.set(-6.6 + i * 1.2, 1.6, -9.2); arena.add(l); arena.add(l.target); judgeLights.push(l);
}

// fighters and referee
const red = mascot({ glove: 0xe03140, shorts: 0xb5222e });
const blue = mascot({ glove: 0x2f6bff, shorts: 0x1f4fd1 });
const ref = mascot({ stripes: true, scale: .92 });
[red, blue, ref].forEach((m) => arena.add(m.root));
red.root.position.set(-1.45, RING_H + .02, .2); red.root.rotation.y = .95;
blue.root.position.set(1.45, RING_H + .02, .2); blue.root.rotation.y = -.95;
ref.root.position.set(0, RING_H + .02, -1.6);
// knockout stars
const stars = new THREE.Group(); blue.body.add(stars); stars.position.set(0, 1.75, 0);
for (let i = 0; i < 4; i++) { const s = mesh(new THREE.OctahedronGeometry(.13), mat(0xffd84a, { emissive: 0x806000 }), false); s.position.set(Math.cos(i * 1.57) * .55, 0, Math.sin(i * 1.57) * .55); stars.add(s); }

// lights
const hemi = new THREE.HemisphereLight(0x8b7bd6, 0x1a1028, .55); scene.add(hemi);
const key = new THREE.SpotLight(0xffffff, 0, 30, .55, .5, 1.1); key.position.set(0, 13, 3); key.target.position.set(0, RING_H, 0);
key.castShadow = true; key.shadow.mapSize.set(1024, 1024); key.shadow.bias = -.0005; scene.add(key); scene.add(key.target);
const redSpot = new THREE.SpotLight(0xff3344, 0, 22, .32, .5, 1.1); redSpot.position.set(-4, 10, 4); redSpot.target = red.root; scene.add(redSpot);
const blueSpot = new THREE.SpotLight(0x3a6dff, 0, 22, .32, .5, 1.1); blueSpot.position.set(4, 10, 4); blueSpot.target = blue.root; scene.add(blueSpot);
// visible light cones
function cone(color) {
  const g = new THREE.ConeGeometry(2.2, 11, 32, 1, true); g.translate(0, -5.5, 0);
  const c = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }));
  scene.add(c); return c;
}
const keyCone = cone(0xfff1d6); keyCone.position.set(0, 12, 1);
const redCone = cone(0xff3344); redCone.position.set(-2.6, 11, 1.4); redCone.scale.set(.6, 1, .6);
const blueCone = cone(0x3a6dff); blueCone.position.set(2.6, 11, 1.4); blueCone.scale.set(.6, 1, .6);

// ---------------------------------------------------------------- the yes-man room (problem line)
const yesRoom = new THREE.Group(); yesRoom.position.set(60, 0, 0); scene.add(yesRoom);
const yesFloor = mesh(new THREE.PlaneGeometry(40, 40), mat(0x2bc4b6, { roughness: .8 })); yesFloor.rotation.x = -Math.PI / 2; yesRoom.add(yesFloor);
const yesWall = mesh(new THREE.PlaneGeometry(40, 20), mat(0x36d2c3, { roughness: .9 })); yesWall.position.set(0, 10, -6); yesRoom.add(yesWall);
const yesMan = mascot(); yesRoom.add(yesMan.root);
const yesLight = new THREE.DirectionalLight(0xffffff, 0); yesLight.position.set(63, 9, 7); yesLight.target.position.set(60, 0, 0);
yesLight.castShadow = true; yesLight.shadow.mapSize.set(1024, 1024); yesLight.shadow.camera.left = -6; yesLight.shadow.camera.right = 6; yesLight.shadow.camera.top = 6; yesLight.shadow.camera.bottom = -6;
scene.add(yesLight); scene.add(yesLight.target);

// ---------------------------------------------------------------- the championship belt (CTA)
const beltSet = new THREE.Group(); beltSet.position.set(-60, 0, 0); scene.add(beltSet);
const beltFloor = mesh(new THREE.PlaneGeometry(40, 40), mat(0x5b2bd6, { roughness: .8 })); beltFloor.rotation.x = -Math.PI / 2; beltSet.add(beltFloor);
const beltWall = mesh(new THREE.PlaneGeometry(40, 20), mat(0x6a3ae6, { roughness: .9 })); beltWall.position.set(0, 10, -6); beltSet.add(beltWall);
const pedestal = mesh(new THREE.CylinderGeometry(1.6, 1.8, 1.1, 40), mat(0xf2ede4)); pedestal.position.y = .55; beltSet.add(pedestal);
const belt = new THREE.Group(); belt.position.set(0, 2.5, 0); beltSet.add(belt);
const strap = mesh(new THREE.TorusGeometry(1.25, .22, 12, 60), mat(0x111111, { roughness: .4 })); strap.scale.set(1, .55, 1); strap.rotation.x = Math.PI / 2; belt.add(strap);
const gold = mat(0xf4c542, { metalness: .85, roughness: .25 });
const plate = mesh(rb(1.6, 1.15, .22, .12, 3), gold); plate.position.set(0, 0, 1.28); belt.add(plate);
for (const sx of [-1, 1]) { const sp = mesh(rb(.6, .7, .16, .08, 2), gold); sp.position.set(sx * 1.05, 0, 1.0); sp.rotation.y = sx * .5; belt.add(sp); }
const gem = mesh(new THREE.OctahedronGeometry(.13), mat(0xe03140, { metalness: .3, roughness: .1, emissive: 0x400000 })); gem.position.set(0, .4, 1.42); belt.add(gem);
const plateText = new THREE.Mesh(new THREE.PlaneGeometry(1.3, .5), new THREE.MeshBasicMaterial({ transparent: true })); plateText.position.set(0, -.08, 1.395); belt.add(plateText);
const beltKey = new THREE.SpotLight(0xffffff, 0, 25, .5, .4, 1); beltKey.position.set(-58, 9, 6); beltKey.target = pedestal; beltKey.castShadow = true; scene.add(beltKey);
const beltRim = new THREE.PointLight(0xff8a5c, 0, 12); beltRim.position.set(-62.5, 4, -2); scene.add(beltRim);
const confetti = new THREE.InstancedMesh(new THREE.PlaneGeometry(.12, .2), new THREE.MeshStandardMaterial({ side: THREE.DoubleSide, roughness: .5 }), 160);
for (let i = 0; i < 160; i++) confetti.setColorAt(i, new THREE.Color([0xf4c542, 0xe03140, 0x2f6bff, 0xffffff, 0xff5fa2][i % 5]));
confetti.instanceColor.needsUpdate = true; beltSet.add(confetti);

// ---------------------------------------------------------------- timeline (cuts follow the voiceover)
const T = window.FIGHT_T;   // cut times from build/timing.py
function shot(t) {
  // returns [position, target] and the active "set"
  if (t < T.ring) {                       // arena wide: descend toward the ring as the lights come on
    const k = easeIO(win(t, 0, T.ring));
    return [[lerp(-2, 0, k), lerp(11, 6.0, k), lerp(20, 14.5, k)], [0, lerp(4.2, 3.7, k), -2]];
  }
  if (t < T.yes) {                        // two-shot, gloves touch, slow orbit
    const k = win(t, T.ring, T.yes);
    const a = lerp(-.3, .25, k);
    return [[Math.sin(a) * 7.4, 2.5, Math.cos(a) * 7.4], [0, 1.45, 0]];
  }
  if (t < T.red) {                        // the yes-man room
    const k = easeOut(win(t, T.yes, T.red));
    return [[60 + lerp(.6, 0, k), lerp(2.1, 1.7, k), lerp(6.6, 5.2, k)], [60, 1.15, 0]];
  }
  if (t < T.blue) {                       // red corner close-up
    const k = easeOut(win(t, T.red, T.blue));
    return [[lerp(1.6, 1.2, k), lerp(2.2, 1.95, k), lerp(6.6, 5.9, k)], [-1.45, 1.25, .2]];
  }
  if (t < T.fight) {                      // blue corner close-up
    const k = easeOut(win(t, T.blue, T.fight));
    return [[lerp(-1.6, -1.2, k), lerp(2.2, 1.95, k), lerp(6.6, 5.9, k)], [1.45, 1.25, .2]];
  }
  if (t < T.judges) {                     // the fight: low side angle, drifting
    const k = win(t, T.fight, T.judges);
    return [[lerp(-.6, .6, k), 2.2, lerp(8.6, 7.8, k)], [0, 1.35, 0]];
  }
  if (t < T.screen) {                     // crane over the ring to the judges' table, tracking along the row
    const k = easeIO(win(t, T.judges, T.judges + 1.4));
    const k2 = easeIO(win(t, T.judges + 1.2, T.screen));
    const x = lerp(-4.6, -3.2, k2);
    return [[lerp(0, x, k), lerp(3.2, 2.7, k), lerp(4, -2.6, k)], [lerp(0, x, k), lerp(1.5, 1.95, k), lerp(0, -9.2, k)]];
  }
  if (t < T.verdict) {                    // up to the big screen
    const k = easeOut(win(t, T.screen, T.screen + .8));
    return [[0, lerp(6.0, 7.1, k), lerp(5, 4.0, k)], [0, lerp(6.6, 7.2, k), -5.5]];
  }
  if (t < T.ko) {                         // the three judges of the test run flip their cards
    const k = win(t, T.verdict, T.ko);
    return [[lerp(2.7, 3.2, k), 2.6, lerp(-2.4, -3.0, k)], [3.0, 1.95, -9.2]];
  }
  if (t < T.ref) {                        // knockout: low dramatic angle, slow push
    const k = win(t, T.ko, T.ref);
    return [[lerp(-1.8, -.8, k), lerp(1.5, 1.7, k), lerp(9.6, 8.8, k)], [.5, 1.3, 0]];
  }
  if (t < T.belt) {                       // referee raises the red glove
    const k = easeOut(win(t, T.ref, T.belt));
    return [[lerp(-.6, -.2, k), lerp(2.6, 2.8, k), lerp(13.0, 12.0, k)], [0, 2.3, 0]];
  }
  const k = easeOut(win(t, T.belt, T.end));     // the belt
  return [[-60 + Math.sin(k * .6) * 1.2, lerp(3.4, 3.1, k), lerp(10.5, 9.2, k)], [-60, 1.7, 0]];
}

const HITS = window.FIGHT_HITS;   // [[time, who, power]]
function shake(t) {
  let s = 0;
  for (const [ht, , p] of HITS) s += pulse(t, ht, .03, .28) * p;
  s += pulse(t, T.knock, .03, .6) * 2.2;
  return s;
}

function animFighters(t) {
  // boxing bounce for both, out of phase
  for (const [m, ph] of [[red, 0], [blue, .9]]) {
    m.hop.position.y = Math.abs(Math.sin(t * 5.2 + ph)) * .09;
    m.body.rotation.z = Math.sin(t * 2.6 + ph) * .04;
    m.arms.forEach((a, i) => { a.position.z = Math.sin(t * 5.2 + ph + i) * .06; a.position.y = .86 + .12; a.rotation.x = 0; });
    blink(m, t, ph * 2);
  }
  // gloves touch on "only one leaves the ring"
  const touch = pulse(t, T.touch, .25, .5);
  red.arms[1].position.z += touch * .9; blue.arms[0].position.z += touch * .9;
  // punches during the exchange
  for (const [ht, who, p] of HITS) {
    const att = who === "r" ? red : blue, def = who === "r" ? blue : red;
    const wind = pulse(t, ht - .12, .12, .22);
    const arm = att.arms[(Math.floor(ht * 10) % 2)];
    arm.position.z += wind * 1.05; arm.position.y += wind * .1;
    const rec = pulse(t, ht, .05, .35) * p;
    def.body.rotation.x = (def.body.rotation.x || 0) - rec * .25;
    def.hop.position.x = (who === "r" ? 1 : -1) * rec * .18;
  }
  // knockout: wind-up, uppercut, blue flies back and lands
  const wind = win(t, T.knock - .55, T.knock);
  red.body.rotation.x = -easeIn(wind) * .2 + pulse(t, T.knock, .05, .5) * .35;
  red.arms[1].position.y += easeIn(wind) * -.3 + pulse(t, T.knock, .05, .5) * 1.0;
  red.arms[1].position.z += pulse(t, T.knock, .05, .5) * .8;
  const fly = win(t, T.knock, T.knock + .65);
  if (t >= T.knock) {
    blue.hop.position.y = Math.sin(fly * Math.PI) * 1.1;
    blue.hop.position.x = easeOut(fly) * 1.2;
    blue.body.rotation.x = -easeOut(fly) * 1.45;
    blue.body.rotation.z = -easeOut(fly) * .3;
    blue.eyes.forEach((e) => (e.scale.y = .25));
  }
  stars.visible = t > T.knock + .55 && t < T.belt;
  stars.rotation.y = t * 4;
  // referee raises the red glove; blue stays down
  const raise = easeOut(win(t, T.raise, T.raise + .35));
  if (t >= T.ref) {
    blue.hop.position.set(1.2, 0, 0); blue.body.rotation.set(-1.45, 0, -.3);
    red.hop.position.y = Math.abs(Math.sin(t * 7)) * .06;
    red.arms[0].position.y = .98 + raise * 1.0; red.arms[0].position.z = .1;
    red.root.position.x = lerp(-1.45, -.7, easeOut(win(t, T.ref, T.ref + .4))); red.root.rotation.y = lerp(.95, .35, easeOut(win(t, T.ref, T.ref + .4)));
  }
  ref.root.visible = t >= T.ref - .01 && t < T.belt;
  ref.root.position.set(lerp(1.2, .75, easeOut(win(t, T.ref, T.ref + .4))), RING_H + .02, .6);
  ref.root.rotation.y = -.35;
  ref.arms[0].position.y = .86 + raise * .8;
  ref.arms[0].position.x = -.82 - raise * .1;
  ref.hop.position.y = Math.abs(Math.sin(t * 4)) * .03;
  blink(ref, t, .4);
}

function animJudges(t) {
  judges.forEach(({ m, card, i }) => {
    m.hop.position.y = Math.abs(Math.sin(t * 2.2 + i)) * .05;
    m.body.rotation.z = Math.sin(t * 1.6 + i * .7) * .05;
    blink(m, t, i * .37);
    const show = t > T.judges + .9 + i * .06;
    card.visible = show;
    if (show) card.rotation.x = -.15 + Math.sin(t * 1.4 + i) * .04;
    card.rotation.y = 0;
  });
  // the test run used three jurors: the statistician, the parent and the lawyer; their cards flip to red
  const test = [7, 8, 9];
  test.forEach((ji, n) => {
    const at = T.verdict + .15 + n * .25;
    judges[ji].card.rotation.y = easeOut(win(t, at, at + .3)) * Math.PI;
  });
  // spotlights: everyone while the jury is introduced, then only the three
  judgeLights.forEach((l, i) => {
    const intro = win(t, T.judges + .6, T.judges + 1.2) * (t < T.screen ? 1 : 0);
    const named = (i <= 2 && t > T.named[i] && t < T.screen) ? 1 : 0;
    const verdict = (t >= T.verdict && t < T.ko && test.includes(i)) ? 1 : 0;
    l.intensity = 25 * Math.max(intro * .6, named, verdict);
  });
  judgeFill.intensity = t >= T.judges && t < T.ko ? (t >= T.verdict ? 25 : 70) : 0;
}

function animScreen(t) {
  let state = "dark";
  if (t > T.idea) state = "idea";
  if (t > T.screen) state = "challenger";
  if (t > T.knock + .15) state = "ko";
  screenMat.map = screenTex[state]; screenMat.needsUpdate = true;
  const flicker = t > T.idea && t < T.idea + .25 ? (Math.floor(t * 40) % 2) : 1;
  screenMat.color.setScalar(state === "dark" ? .15 : flicker ? 1 : .3);
}

function animLights(t) {
  const on = win(t, .12, .3);
  key.intensity = 150 * on * (t >= T.yes && t < T.red ? 0 : 1);
  keyCone.material.opacity = .07 * on;
  const rOn = Math.max(win(t, T.redOn, T.redOn + .15), t >= T.red && t < T.blue ? 1 : 0);
  const bOn = Math.max(win(t, T.blueOn, T.blueOn + .15), t >= T.blue && t < T.fight ? 1 : 0);
  redSpot.intensity = 110 * rOn * (t >= T.blue && t < T.fight ? .25 : 1);
  blueSpot.intensity = 110 * bOn * (t >= T.red && t < T.blue ? .25 : 1);
  redCone.material.opacity = .06 * rOn; blueCone.material.opacity = .06 * bOn;
  hemi.intensity = .35 + .35 * on;
  // the arena dims for the jury close-ups and the screen, flares on the knockout
  const ko = pulse(t, T.knock, .03, .5);
  key.color.setRGB(1, 1 - ko * .2, 1 - ko * .3);
  yesLight.intensity = t >= T.yes && t < T.red ? 2.4 : 0;
  beltKey.intensity = t >= T.belt ? 260 : 0; beltRim.intensity = t >= T.belt ? 40 : 0;
}

function animCrowd(t) {
  const hype = .4 + pulse(t, T.knock, .1, 1.6) * 1.6 + pulse(t, HITS[0][0], .1, 2.5) * .5 + win(t, .2, 1) * .3;
  for (let i = 0; i < CROWD; i++) {
    const [x, y, z, ph, ry] = crowdBase[i];
    const jump = Math.max(0, Math.sin(t * 7 + ph)) * .25 * hype;
    tmpP.set(x, y + .35 + jump, z); tmpQ.setFromEuler(new THREE.Euler(0, ry, Math.sin(t * 3 + ph) * .08)); tmpS.set(1, 1, 1);
    tmpM.compose(tmpP, tmpQ, tmpS); crowd.setMatrixAt(i, tmpM);
  }
  crowd.instanceMatrix.needsUpdate = true;
}

function animYes(t) {
  const k = t - T.yes;
  yesMan.root.position.set(0, 0, 0);
  // nods yes on every beat, little hops of approval
  yesMan.body.rotation.x = Math.max(0, Math.sin(k * 9)) * .22;
  yesMan.hop.position.y = Math.abs(Math.sin(k * 4.5)) * .08;
  yesMan.arms.forEach((a, i) => (a.position.y = .86 + Math.max(0, Math.sin(k * 4.5 + i * Math.PI)) * .35));
  blink(yesMan, t, .2);
}

function animBelt(t) {
  const k = t - T.belt;
  belt.rotation.y = Math.sin(k * 1.2) * .35 + easeOut(win(t, T.belt, T.belt + .8)) * Math.PI * 2;
  belt.position.y = 2.5 + Math.sin(k * 2) * .08 + (1 - easeOut(win(t, T.belt, T.belt + .6))) * 3;
  for (let i = 0; i < 160; i++) {
    const ph = hash(i) * 10, sp = .8 + hash(i + 9) * 1.2;
    const fall = (k * sp + ph) % 8;
    tmpP.set((hash(i + 2) - .5) * 9, 8 - fall, (hash(i + 5) - .5) * 5);
    tmpQ.setFromEuler(new THREE.Euler(k * 3 + ph, k * 2 + ph, 0)); tmpS.set(1, 1, 1);
    tmpM.compose(tmpP, tmpQ, tmpS); confetti.setMatrixAt(i, tmpM);
  }
  confetti.instanceMatrix.needsUpdate = true;
  confetti.visible = t > T.belt + .4;
}

function renderAt(t) {
  animLights(t); animCrowd(t); animFighters(t); animJudges(t); animScreen(t); animYes(t); animBelt(t);
  red.root.visible = blue.root.visible = t < T.yes || (t >= T.red && t < T.belt);
  red.root.visible = red.root.visible && !(t >= T.judges && t < T.ko);
  blue.root.visible = red.root.visible;
  frontRopes.forEach((r) => (r.visible = t < T.ring));
  screenGroup.visible = !(t >= T.ref && t < T.belt);
  const [p, q] = shot(t);
  const s = shake(t);
  camera.position.set(p[0] + Math.sin(t * 91) * .05 * s, p[1] + Math.cos(t * 77) * .05 * s, p[2]);
  camera.lookAt(q[0], q[1], q[2]);
  camera.fov = 38 - pulse(t, T.knock, .05, .7) * 6;
  camera.updateProjectionMatrix();
  renderer.render(scene, camera);
}

// ---------------------------------------------------------------- textures need the fonts first
function drawScreens() {
  const bg = (g, w, h, c1, c2) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, c1); gr.addColorStop(1, c2); g.fillStyle = gr; g.fillRect(0, 0, w, h); };
  const scan = (g, w, h) => { g.fillStyle = "rgba(0,0,0,.18)"; for (let y = 0; y < h; y += 6) g.fillRect(0, y, w, 2); };
  screenTex.dark = screenTexture((g, w, h) => { bg(g, w, h, "#0b0b18", "#05050a"); g.fillStyle = "#e03140"; g.font = "800 64px Manrope"; g.textAlign = "center"; g.fillText("● LIVE", w / 2, h / 2 + 22); scan(g, w, h); });
  const idea = (g, w, h, top) => {
    bg(g, w, h, "#1b1340", "#0b0920");
    g.textAlign = "center";
    if (top) { g.fillStyle = "#f4c542"; g.font = "800 30px JBMono"; g.fillText(top, w / 2, 70); }
    g.fillStyle = "#ffffff"; g.font = "900 92px Manrope";
    ["QUIT", "NURSING", "TO SELL", "CANDLES?"].forEach((l, i) => g.fillText(l, w / 2, 170 + i * 100));
    g.font = "64px sans-serif"; g.fillText("🕯️", w / 2 + 230, 560); scan(g, w, h);
  };
  screenTex.idea = screenTexture((g, w, h) => idea(g, w, h, "TONIGHT'S MAIN EVENT"));
  screenTex.challenger = screenTexture((g, w, h) => idea(g, w, h, ""));
  screenTex.ko = screenTexture((g, w, h) => {
    bg(g, w, h, "#3a0710", "#120206"); g.textAlign = "center"; g.fillStyle = "#ffd84a"; g.font = "900 260px Manrope"; g.fillText("K.O.", w / 2, 380);
    g.fillStyle = "#ffffff"; g.font = "800 48px JBMono"; g.fillText("GUILTY · 3–0", w / 2, 500); scan(g, w, h);
  });
  const c = document.createElement("canvas"); c.width = 520; c.height = 200; const g = c.getContext("2d");
  g.fillStyle = "#3a2600"; g.font = "900 150px Manrope"; g.textAlign = "center"; g.fillText("FIGHT", 260, 160);
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; plateText.material.map = tx; plateText.material.needsUpdate = true;
}

const ready = (async () => {
  await Promise.all(["800 96px Manrope", "900 260px Manrope", "800 46px JBMono"].map((f) => document.fonts.load(f)));
  drawScreens();
  renderer.compile(scene, camera);
  renderAt(window.__hfThreeTime || 0);
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["fight-night"] = ready;
window.addEventListener("hf-seek", (e) => { if (screenTex.idea) renderAt(e.detail.time); });
