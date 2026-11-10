// The Blanket Rule: one bedroom at night. Bed on the left (head against the back wall), the clothes
// chair in the right corner, window on the back wall. Fixed light rig as in the other films.
import * as THREE from "three";
import * as T from "./textures.js";
import { box, mesh, std } from "./chars.js";
import { rng } from "./util.js";

export const BED = { x: -6, edgeX: -2.8, top: 3.2, zHead: -9.6, zFoot: -1.6 };
export const CHAIR = new THREE.Vector3(8.2, 0, -5.4);

const rep = (t, x, y) => {
  const c = t.clone();
  c.repeat.set(x, y);
  c.needsUpdate = true;
  return c;
};
const glow = (color, k = 2) => new THREE.MeshStandardMaterial({ color: "#000", emissive: color, emissiveIntensity: k });
const basic = (color, k = 1) => {
  const m = new THREE.MeshBasicMaterial({ color });
  m.color.multiplyScalar(k);
  return m;
};

export function buildWorld(scene) {
  const W = { props: {} };
  const P = W.props;
  const room = new THREE.Group();
  scene.add(room);

  // floor, ceiling, walls
  const floor = mesh(new THREE.PlaneGeometry(24, 20), std(0xffffff, { map: T.woodFloor({ repeat: [2.4, 2] }), roughness: 0.55 }), { cast: false });
  floor.rotation.x = -Math.PI / 2;
  room.add(floor);
  const ceil = mesh(new THREE.PlaneGeometry(24, 20), std(0xffffff, { map: T.plaster({ color: [220, 15, 70], repeat: [4, 3] }), roughness: 0.9 }), { cast: false });
  ceil.rotation.x = Math.PI / 2;
  ceil.position.y = 11;
  room.add(ceil);
  const wallTex = T.starWallpaper();
  const wm = (w, h) => std(0xffffff, { map: rep(wallTex, w / 5, h / 5), roughness: 0.85 });
  const wall = (w, h, d, x, y, z) => {
    const m = box(w, h, d, wm(Math.max(w, d), h), 0.02);
    m.position.set(x, y, z);
    room.add(m);
  };
  // back wall with window hole x 3..9, y 4..9
  wall(15, 11, 0.5, -4.5, 5.5, -10.25);
  wall(3, 11, 0.5, 10.5, 5.5, -10.25);
  wall(6, 4, 0.5, 6, 2, -10.25);
  wall(6, 2, 0.5, 6, 10, -10.25);
  wall(0.5, 11, 20, -12.25, 5.5, 0);
  wall(0.5, 11, 20, 12.25, 5.5, 0);
  wall(24, 11, 0.5, 0, 5.5, 10.25);
  const trim = std("#e9e2d2", { roughness: 0.5 });
  for (const [w, h, x, y] of [[6.6, 0.35, 6, 9.15], [6.6, 0.35, 6, 3.85], [0.35, 5.6, 2.85, 6.5], [0.35, 5.6, 9.15, 6.5], [0.15, 5, 6, 6.5], [6, 0.15, 6, 6.5]]) {
    const f = box(w, h, 0.4, trim, 0.04);
    f.position.set(x, y, -10.0);
    room.add(f);
  }
  const sill = box(7.2, 0.3, 1.0, trim, 0.05);
  sill.position.set(6, 3.7, -9.6);
  room.add(sill);
  const skyGeo = new THREE.PlaneGeometry(26, 18);
  const skyNight = mesh(skyGeo, new THREE.MeshBasicMaterial({ map: T.skyGradient([[0, "#070c22"], [0.6, "#16224a"], [1, "#24336a"]], { stars: 140, moon: [80, 170, 18] }) }), { cast: false });
  skyNight.position.set(6, 6, -18);
  room.add(skyNight);
  const skyDawn = mesh(skyGeo, new THREE.MeshBasicMaterial({ map: T.skyGradient([[0, "#4a63a8"], [0.45, "#f19a6a"], [0.8, "#ffd08a"], [1, "#fff2cc"]]), transparent: true, opacity: 0 }), { cast: false });
  skyDawn.position.set(6, 6, -17.9);
  room.add(skyDawn);
  P.sky = { night: skyNight, dawn: skyDawn };
  const curtain = std("#2b3566", { roughness: 0.95 });
  for (const side of [-1, 1]) {
    for (let i = 0; i < 3; i++) {
      const c = box(0.7, 7.6, 0.4, curtain, 0.2);
      c.position.set(6 + side * (3.9 + i * 0.55), 6.6, -9.5 + (i % 2) * 0.2);
      room.add(c);
    }
  }
  // glow-in-the-dark stars on the ceiling
  const starMat = glow("#c8ffb8", 1.6);
  P.starMat = starMat;
  const r = rng(13);
  for (let i = 0; i < 34; i++) {
    const s = mesh(new THREE.CircleGeometry(0.12 + r() * 0.1, 5), starMat, { cast: false });
    s.rotation.x = Math.PI / 2;
    s.position.set(-10 + r() * 20, 10.97, -9 + r() * 17);
    room.add(s);
  }
  // rug
  const rugM = mesh(new THREE.PlaneGeometry(9, 6.5), std(0xffffff, { map: T.rug({ seed: 4 }), roughness: 0.95, color: "#9fb6ff" }), { cast: false });
  rugM.rotation.x = -Math.PI / 2;
  rugM.position.set(2.5, 0.02, 0.5);
  room.add(rugM);

  // bed
  const wood = std("#6a4a32", { roughness: 0.55 });
  const bed = new THREE.Group();
  room.add(bed);
  const bx = BED.x, zc = (BED.zHead + BED.zFoot) / 2, len = BED.zFoot - BED.zHead;
  for (const [x, z] of [[-3.0, BED.zHead + 0.3], [3.0, BED.zHead + 0.3], [-3.0, BED.zFoot - 0.3], [3.0, BED.zFoot - 0.3]]) {
    const l = box(0.45, 2.0, 0.45, wood, 0.06);
    l.position.set(bx + x, 1.0, z);
    bed.add(l);
  }
  for (const side of [-1, 1]) {
    const rail = box(0.35, 0.45, len, wood, 0.05);
    rail.position.set(bx + side * 3.05, 1.8, zc);
    bed.add(rail);
  }
  const head = box(6.6, 6.2, 0.4, wood, 0.12);
  head.position.set(bx, 3.1, BED.zHead - 0.15);
  bed.add(head);
  const foot = box(6.6, 3.4, 0.35, wood, 0.12);
  foot.position.set(bx, 1.7, BED.zFoot + 0.1);
  bed.add(foot);
  const mattress = box(6.2, 1.2, len - 0.3, std("#e9eef6", { roughness: 0.9 }), 0.3);
  mattress.position.set(bx, 2.6, zc);
  bed.add(mattress);
  const sheet = box(6.3, 0.12, len - 0.2, std("#c7d6f0", { roughness: 0.9 }), 0.04);
  sheet.position.set(bx, 3.2, zc);
  bed.add(sheet);
  const pillow = box(4.2, 0.8, 1.8, std("#f4f1ea", { roughness: 0.9 }), 0.35);
  pillow.position.set(bx, 3.6, BED.zHead + 1.2);
  bed.add(pillow);
  // dark void under the bed
  const under = mesh(new THREE.PlaneGeometry(6, 1.6), basic("#020203"), { cast: false });
  under.rotation.y = -Math.PI / 2;
  under.position.set(bx - 2.9, 0.85, zc);
  room.add(under);
  // blanket (states set per shot)
  const blanketMat = std(0xffffff, { map: T.knit({ colors: ["#3f5fa8", "#355296", "#d9a23a", "#355296"], band: 4, repeat: [3, 3] }), roughness: 0.95 });
  P.blanket = box(6.5, 0.5, 6.4, blanketMat, 0.22);
  scene.add(P.blanket);

  // nightstand + LED clock + glass
  const ns = box(2.2, 2.8, 2.0, wood, 0.08);
  ns.position.set(-1.4, 1.4, -8.6);
  room.add(ns);
  const clock = new THREE.Group();
  clock.position.set(-1.3, 2.8, -8.4);
  clock.rotation.y = -0.6;
  const cb = box(1.6, 0.85, 0.7, std("#1b1b1f", { roughness: 0.4 }), 0.12);
  cb.position.y = 0.42;
  clock.add(cb);
  const ledTex = {};
  for (const tt of ["11:48", "3:06", "3:07", "3:12", "3:48", "4:31", "5:14", "5:58", "6:12", "7:30"]) ledTex[tt] = T.ledClock(tt);
  const face = mesh(new THREE.PlaneGeometry(1.4, 0.7), new THREE.MeshBasicMaterial({ map: ledTex["3:07"] }), { cast: false });
  face.position.set(0, 0.43, 0.36);
  clock.add(face);
  room.add(clock);
  P.clock = { group: clock, face, tex: ledTex, set: (t) => (face.material.map = ledTex[t] || ledTex["3:07"]) };
  const glass = mesh(new THREE.CylinderGeometry(0.22, 0.2, 0.55, 16), new THREE.MeshStandardMaterial({ color: "#d9eef0", transparent: true, opacity: 0.35, roughness: 0.05 }), { cast: false });
  glass.position.set(-2.0, 3.08, -9.0);
  room.add(glass);

  // desk fan on the floor (summer)
  const fan = new THREE.Group();
  fan.position.set(1.2, 0, -6.8);
  fan.rotation.y = -1.0;
  const fbase = mesh(new THREE.CylinderGeometry(0.7, 0.8, 0.25, 20), std("#e8e8ec", { roughness: 0.4 }));
  fbase.position.y = 0.12;
  fan.add(fbase);
  const fpole = mesh(new THREE.CylinderGeometry(0.08, 0.08, 1.8, 8), std("#e8e8ec", { roughness: 0.4 }));
  fpole.position.y = 1.1;
  fan.add(fpole);
  const cage = mesh(new THREE.TorusGeometry(0.85, 0.05, 6, 28), std("#cfd2d8", { metalness: 0.5, roughness: 0.3 }));
  cage.position.y = 2.1;
  fan.add(cage);
  const blades = new THREE.Group();
  blades.position.set(0, 2.1, 0.02);
  for (let i = 0; i < 3; i++) {
    const b = box(0.32, 0.75, 0.04, std("#9fc3e6", { roughness: 0.4 }), 0.1);
    b.position.y = 0.38;
    const holder = new THREE.Group();
    holder.rotation.z = (i / 3) * Math.PI * 2;
    holder.add(b);
    blades.add(holder);
  }
  fan.add(blades);
  room.add(fan);
  P.fanBlades = blades;

  // closet door ajar (right wall)
  const closetGap = mesh(new THREE.PlaneGeometry(3.4, 7.2), basic("#020203"), { cast: false });
  closetGap.rotation.y = -Math.PI / 2;
  closetGap.position.set(11.98, 3.6, 4.5);
  room.add(closetGap);
  const cdoorPivot = new THREE.Group();
  cdoorPivot.position.set(11.95, 0, 6.2);
  cdoorPivot.rotation.y = -Math.PI / 2 - 0.35;
  const cdoor = box(3.4, 7.2, 0.25, std(0xffffff, { map: T.panelDoor({ color: "#e9e2d2" }), roughness: 0.55 }), 0.04);
  cdoor.position.set(-1.7, 3.6, 0);
  cdoorPivot.add(cdoor);
  room.add(cdoorPivot);
  // nightlight
  const nl = mesh(new THREE.BoxGeometry(0.15, 0.5, 0.4), glow("#ffb45a", 3), { cast: false });
  nl.position.set(11.9, 1.2, -1.5);
  room.add(nl);
  // posters + shelf of toys
  for (const [k, x, y, z, ry] of [[0, -0.2, 7.0, -9.98, 0], [1, 11.98, 6.6, -6.5, -Math.PI / 2]]) {
    const p = mesh(new THREE.PlaneGeometry(2.4, 3.4), std(0xffffff, { map: T.poster(k), roughness: 0.7 }), { cast: false });
    p.position.set(x, y, z);
    p.rotation.y = ry;
    room.add(p);
  }
  const shelf = box(0.6, 0.2, 4, wood, 0.03);
  shelf.position.set(11.7, 5.0, -2.0);
  room.add(shelf);
  const toyCols = ["#e8732a", "#3f7fd1", "#f2d04a", "#5bb36a", "#d94b4b"];
  for (let i = 0; i < 6; i++) {
    const t = box(0.55, 0.55 + (i % 3) * 0.3, 0.55, std(toyCols[i % 5], { roughness: 0.5 }), 0.1);
    t.position.set(11.6, 5.1 + (0.55 + (i % 3) * 0.3) / 2, -3.6 + i * 0.62);
    room.add(t);
  }

  // the clothes chair
  const chair = new THREE.Group();
  chair.position.copy(CHAIR);
  chair.rotation.y = -Math.PI / 2;
  const cw = std("#5a3f2c", { roughness: 0.55 });
  const seat = box(2.6, 0.3, 2.4, cw, 0.06);
  seat.position.y = 2.2;
  chair.add(seat);
  const cback = box(2.6, 3.6, 0.3, cw, 0.06);
  cback.position.set(0, 4.0, -1.1);
  chair.add(cback);
  for (const [lx, lz] of [[-1.1, -1.0], [1.1, -1.0], [-1.1, 1.0], [1.1, 1.0]]) {
    const l = box(0.25, 2.1, 0.25, cw, 0.04);
    l.position.set(lx, 1.05, lz);
    chair.add(l);
  }
  room.add(chair);

  P.heap = makeHeap(scene);
  P.lint = makeLint(scene);
  // the note
  P.note = mesh(new THREE.PlaneGeometry(1.4, 1.05), std(0xffffff, { map: T.noteTexture(["You're welcome.", "Now keep your", "feet in. Some of us", "are trying to sleep."]), roughness: 0.8 }), { cast: false });
  P.note.rotation.x = -Math.PI / 2;
  scene.add(P.note);
  // dust motes in the moonbeam
  const dustGeo = new THREE.BufferGeometry();
  dustGeo.setAttribute("position", new THREE.BufferAttribute(new Float32Array(600 * 3), 3));
  W.dust = new THREE.Points(dustGeo, new THREE.PointsMaterial({ map: T.softDot("220,230,255"), size: 0.12, transparent: true, opacity: 0.6, depthWrite: false }));
  W.dust.frustumCulled = false;
  scene.add(W.dust);
  const dr = rng(3);
  const pa = dustGeo.attributes.position;
  for (let i = 0; i < 600; i++) pa.setXYZ(i, 1 + dr() * 9, 0.5 + dr() * 8, -9 + dr() * 10);

  buildLights(scene, W);
  return W;
}

// --- the clothes creature: a slumped "person" on the chair that can stand up -------
function makeHeap(scene) {
  const root = new THREE.Group();
  scene.add(root);
  const denim = std(0xffffff, { map: T.denim({ color: "#3a4f7a" }), roughness: 0.85 });
  const hood = std("#56604f", { roughness: 0.9 });
  const voidM = basic("#030304");
  const pelvis = new THREE.Group();
  root.add(pelvis);
  const legs = [-1, 1].map((side) => {
    const leg = new THREE.Group();
    leg.position.set(side * 0.55, 0, 0);
    const m = box(1.0, 3.5, 1.0, denim, 0.12);
    m.position.y = -1.75;
    leg.add(m);
    const cuff = mesh(new THREE.PlaneGeometry(0.8, 0.8), voidM, { cast: false });
    cuff.rotation.x = Math.PI / 2;
    cuff.position.y = -3.51;
    leg.add(cuff);
    pelvis.add(leg);
    return leg;
  });
  const torso = new THREE.Group();
  pelvis.add(torso);
  const body = box(2.5, 3.0, 1.4, hood, 0.22);
  body.position.y = 1.5;
  torso.add(body);
  const pocket = box(1.6, 0.8, 0.1, std("#4a5444", { roughness: 0.9 }), 0.05);
  pocket.position.set(0, 0.8, 0.72);
  torso.add(pocket);
  const arms = [-1, 1].map((side) => {
    const arm = new THREE.Group();
    arm.position.set(side * 1.55, 2.7, 0);
    const m = box(0.8, 3.6, 0.8, hood, 0.15);
    m.position.y = -1.8;
    arm.add(m);
    const cuff = mesh(new THREE.PlaneGeometry(0.62, 0.62), voidM, { cast: false });
    cuff.rotation.x = Math.PI / 2;
    cuff.position.y = -3.61;
    arm.add(cuff);
    torso.add(arm);
    return arm;
  });
  const head = new THREE.Group();
  head.position.y = 3.0;
  torso.add(head);
  const hoodM = box(1.9, 2.0, 1.8, hood, 0.55);
  hoodM.position.set(0, 1.0, -0.1);
  head.add(hoodM);
  const faceVoid = box(1.35, 1.4, 0.2, voidM, 0.3);
  faceVoid.position.set(0, 0.95, 0.75);
  head.add(faceVoid);
  const cap = box(1.95, 0.5, 1.9, std("#b3302b", { roughness: 0.7 }), 0.2);
  cap.position.set(0, 2.05, -0.05);
  head.add(cap);
  const brim = box(1.6, 0.12, 1.0, std("#9a2824", { roughness: 0.7 }), 0.05);
  brim.position.set(0, 1.85, 0.95);
  head.add(brim);
  const eyeMat = new THREE.MeshStandardMaterial({ color: "#000", emissive: "#ff5a4a", emissiveIntensity: 0 });
  for (const x of [-0.3, 0.3]) {
    const e = mesh(new THREE.SphereGeometry(0.09, 10, 8), eyeMat, { cast: false });
    e.position.set(x, 1.05, 0.88);
    head.add(e);
  }
  return {
    root, j: { pelvis, legs, torso, arms, head }, eyeMat,
    // s: 0 = slumped on the chair, 1 = standing
    pose(s) {
      const L = (a, b) => a + (b - a) * s;
      pelvis.position.y = L(2.75, 3.55);
      pelvis.position.z = L(-0.35, 0);
      legs.forEach((l, i) => l.rotation.set(L(-1.35, 0), 0, L(i ? -0.08 : 0.08, 0)));
      torso.rotation.set(L(-0.5, 0.1), 0, L(0.12, 0));
      arms.forEach((a, i) => a.rotation.set(L(-0.15, 0.05), 0, L(i ? 0.45 : -0.45, i ? 0.06 : -0.06)));
      head.rotation.set(L(0.55, 0.12), 0, L(0.35, 0));
    },
  };
}

// --- the little helper under the bed ------------------------------------------------
function makeLint(scene) {
  const root = new THREE.Group();
  scene.add(root);
  const fur = std(0xffffff, { map: T.velvet({ color: [220, 18, 22], repeat: [2, 2] }), roughness: 1 });
  const body = box(1.5, 1.25, 1.4, fur, 0.5);
  body.position.y = 0.65;
  root.add(body);
  const faceAwake = T.lintFace();
  const faceSleep = T.lintFace({ sleeping: true });
  const faceMat = new THREE.MeshStandardMaterial({ map: faceAwake, transparent: true, alphaTest: 0.3, emissive: "#ffffff", emissiveMap: faceAwake, emissiveIntensity: 0.7 });
  const face = mesh(new THREE.PlaneGeometry(1.25, 1.25), faceMat, { cast: false });
  face.position.set(0, 0.7, 0.71);
  root.add(face);
  for (const side of [-1, 1]) {
    const horn = mesh(new THREE.ConeGeometry(0.12, 0.35, 8), std("#c9d6e8", { roughness: 0.6 }), { cast: false });
    horn.position.set(side * 0.45, 1.4, 0);
    horn.rotation.z = -side * 0.4;
    root.add(horn);
  }
  const mask = box(1.3, 0.3, 0.12, std("#c45a8a", { roughness: 0.8 }), 0.06);
  mask.position.set(0, 0.85, 0.74);
  root.add(mask);
  // the long cold arm (shoulder at the body's right side), aimed at a target each frame
  const shoulder = new THREE.Group();
  shoulder.position.set(0.55, 0.6, 0.55);
  root.add(shoulder);
  const skin = std("#b9d2e8", { roughness: 0.45, emissive: "#203048", emissiveIntensity: 0.25 });
  const arm = box(0.26, 1, 0.26, skin, 0.08);
  shoulder.add(arm);
  const hand = new THREE.Group();
  shoulder.add(hand);
  const palm = box(0.42, 0.5, 0.2, skin, 0.06);
  palm.position.y = -0.2;
  hand.add(palm);
  const fingers = [];
  for (let f = 0; f < 4; f++) {
    const fg = new THREE.Group();
    fg.position.set(-0.15 + f * 0.1, -0.42, 0);
    const m = box(0.08, 0.7, 0.1, skin, 0.03);
    m.position.y = -0.33;
    fg.add(m);
    hand.add(fg);
    fingers.push(fg);
  }
  return { root, faceMat, faceAwake, faceSleep, mask, shoulder, arm, hand, fingers };
}

function buildLights(scene, W) {
  const hemi = new THREE.HemisphereLight("#8fa0d0", "#3a2418", 0.5);
  scene.add(hemi);
  const key = new THREE.DirectionalLight("#9fb4ff", 1.2);
  key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  key.shadow.bias = -0.0004;
  key.shadow.normalBias = 0.03;
  const sc = key.shadow.camera;
  sc.left = -18;
  sc.right = 18;
  sc.top = 18;
  sc.bottom = -18;
  sc.near = 1;
  sc.far = 90;
  scene.add(key);
  scene.add(key.target);
  const prac = new THREE.SpotLight("#ffb46a", 120, 0, 1.25, 0.85, 2);
  prac.castShadow = true;
  prac.shadow.mapSize.set(1024, 1024);
  prac.shadow.bias = -0.0005;
  prac.shadow.normalBias = 0.04;
  prac.shadow.camera.near = 0.5;
  prac.shadow.camera.far = 60;
  scene.add(prac);
  scene.add(prac.target);
  const glows = [0, 1, 2, 3].map(() => {
    const p = new THREE.PointLight("#ffb46a", 0, 0, 2);
    scene.add(p);
    return p;
  });
  W.lights = { hemi, key, prac, glows };
}
