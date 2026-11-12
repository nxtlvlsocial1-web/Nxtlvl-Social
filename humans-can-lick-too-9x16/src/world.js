// Humans Can Lick Too: the kid's bedroom (bed on the left, the dark gap under it) and, off to the side,
// the bathroom: dripping sink, fogged mirror, glass shower with a chair wedged against it. Fixed rig.
import * as THREE from "three";
import * as T from "./textures.js";
import { box, mesh, std } from "./chars.js";
import { rng } from "./util.js";
import { makePhone } from "./phone.js";

export const BED = { x: -6, edgeX: -2.8, top: 3.2, zHead: -9.6, zFoot: -1.6 };
export const CHAIR = new THREE.Vector3(8.2, 0, -5.4);
// closet opening in the right wall (x = 12): z 2.8..6.2, 7.2 tall; walk-in space behind it
export const CLOSET = { x: 12, z0: 2.8, z1: 6.2, zc: 4.5, h: 7.2, inX: 14.6 };
export const HX = 70; // bathroom set origin (far from the bedroom)

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
  // right wall, split around the closet opening
  wall(0.5, 11, 12.8, 12.25, 5.5, -3.6);
  wall(0.5, 11, 3.8, 12.25, 5.5, 8.1);
  wall(0.5, 3.8, 3.4, 12.25, 9.1, 4.5);
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
  const underM = basic("#020203");
  underM.side = THREE.DoubleSide;
  const under = mesh(new THREE.PlaneGeometry(7.6, 2.1), underM, { cast: false });
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
  for (const tt of ["8:47", "12:00", "12:03", "1:12", "2:47", "4:05", "7:30"]) ledTex[tt] = T.ledClock(tt);
  const face = mesh(new THREE.PlaneGeometry(1.4, 0.7), new THREE.MeshBasicMaterial({ map: ledTex["12:03"] }), { cast: false });
  face.position.set(0, 0.43, 0.36);
  clock.add(face);
  room.add(clock);
  P.clock = { group: clock, face, tex: ledTex, set: (t) => (face.material.map = ledTex[t] || ledTex["12:03"]) };
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

  // walk-in closet behind the right wall
  const cl = new THREE.Group();
  room.add(cl);
  const clWall = std(0xffffff, { map: T.plaster({ color: [225, 12, 30], repeat: [2, 2] }), roughness: 0.9 });
  const cfloor = mesh(new THREE.PlaneGeometry(4.6, 5.2), std(0xffffff, { map: T.woodFloor({ repeat: [0.5, 0.5] }), roughness: 0.6 }), { cast: false });
  cfloor.rotation.x = -Math.PI / 2;
  cfloor.position.set(14.8, 0.005, 4.5);
  cl.add(cfloor);
  for (const [w, h, d, x, y, z] of [[0.3, 11, 5.6, 17.2, 5.5, 4.5], [5.0, 11, 0.3, 14.8, 5.5, 1.75], [5.0, 11, 0.3, 14.8, 5.5, 7.25], [5.0, 0.3, 5.6, 14.8, 10.7, 4.5]]) {
    const m = box(w, h, d, clWall, 0.02);
    m.position.set(x, y, z);
    cl.add(m);
  }
  const rod = mesh(new THREE.CylinderGeometry(0.06, 0.06, 5.2, 8), std("#b9b9c0", { metalness: 0.6, roughness: 0.3 }));
  rod.rotation.x = Math.PI / 2;
  rod.position.set(16.3, 8.4, 4.5);
  cl.add(rod);
  const shirtCols = ["#3b5c8a", "#8a3b3b", "#2f9e9a", "#d9a23a", "#555a66", "#2f9e9a", "#6b4a7a"];
  for (let i = 0; i < 7; i++) {
    const sh = box(1.5, 2.4 + (i % 3) * 0.4, 0.22, std(shirtCols[i], { roughness: 0.85 }), 0.08);
    sh.position.set(16.25, 8.3 - (2.4 + (i % 3) * 0.4) / 2, 2.4 + i * 0.7);
    sh.rotation.y = Math.PI / 2 + ((i % 2) - 0.5) * 0.12;
    cl.add(sh);
  }
  const frameM = std("#e9e2d2", { roughness: 0.5 });
  for (const [w, h, d, x, y, z] of [[0.6, 7.4, 0.3, 11.95, 3.7, 2.65], [0.6, 7.4, 0.3, 11.95, 3.7, 6.35], [0.6, 0.3, 4.0, 11.95, 7.35, 4.5]]) {
    const f = box(w, h, d, frameM, 0.04);
    f.position.set(x, y, z);
    room.add(f);
  }
  // door hinged at z = 6.2; rotation -PI/2 is closed, more positive swings it into the room
  const cdoorPivot = new THREE.Group();
  cdoorPivot.position.set(11.85, 0, 6.2);
  cdoorPivot.rotation.y = -Math.PI / 2 + 0.22;
  const cdoor = box(3.4, 7.15, 0.22, std(0xffffff, { map: T.panelDoor({ color: "#e9e2d2" }), roughness: 0.55 }), 0.04);
  cdoor.position.set(-1.7, 3.58, 0);
  cdoorPivot.add(cdoor);
  const knob = mesh(new THREE.SphereGeometry(0.16, 12, 10), std("#c9a24a", { metalness: 0.7, roughness: 0.3 }));
  knob.position.set(-3.1, 3.4, 0.2);
  cdoorPivot.add(knob);
  room.add(cdoorPivot);
  P.closetDoor = cdoorPivot;
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

  // the two phones: the kid's, and Mom's lost one
  P.phone = makePhone(scene, { caseColor: "#2a3550" });
  P.momPhone = makePhone(scene, { caseColor: "#7a5a6a", gripSkin: "#d4beac", gripSleeve: "#2f9e9a", long: true });
  buildBedroomExtras(room, scene, P);
  buildBathroom(scene, P);
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

// --- bedroom extras: lamp, door with a deadbolt, the dangling arm, what's under the bed ----------
function buildBedroomExtras(room, scene, P) {
  // nightstand lamp
  const lamp = new THREE.Group();
  lamp.position.set(-0.6, 2.8, -9.05);
  room.add(lamp);
  const lb = mesh(new THREE.CylinderGeometry(0.3, 0.36, 0.2, 16), std("#c9b28a", { roughness: 0.5 }));
  lb.position.y = 0.1;
  lamp.add(lb);
  const lp = mesh(new THREE.CylinderGeometry(0.06, 0.06, 1.1, 8), std("#c9b28a", { roughness: 0.5 }));
  lp.position.y = 0.7;
  lamp.add(lp);
  const shadeM = new THREE.MeshStandardMaterial({ color: "#f3e3c3", roughness: 0.9, emissive: "#ffcf8a", emissiveIntensity: 0, side: THREE.DoubleSide });
  const shade = mesh(new THREE.CylinderGeometry(0.45, 0.7, 0.8, 20, 1, true), shadeM, { cast: false });
  shade.position.y = 1.45;
  lamp.add(shade);
  P.lamp = { group: lamp, shadeM, pos: [-0.6, 4.25, -9.05] };
  // bedroom door on the front wall, with a deadbolt
  const door = box(3.4, 7.2, 0.25, std(0xffffff, { map: T.panelDoor({ color: "#e9e2d2" }), roughness: 0.55 }), 0.04);
  door.position.set(7, 3.6, 9.9);
  room.add(door);
  const plate = mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.06, 20), std("#c9a24a", { metalness: 0.7, roughness: 0.3 }));
  plate.rotation.x = Math.PI / 2;
  plate.position.set(5.75, 4.4, 9.74);
  room.add(plate);
  const turn = box(0.1, 0.34, 0.12, std("#c9a24a", { metalness: 0.7, roughness: 0.3 }), 0.03);
  turn.position.set(5.75, 4.4, 9.68);
  room.add(turn);
  const knob = mesh(new THREE.SphereGeometry(0.18, 14, 10), std("#c9a24a", { metalness: 0.7, roughness: 0.3 }));
  knob.position.set(5.75, 3.5, 9.7);
  room.add(knob);
  P.deadbolt = turn;
  // the arm that hangs off the bed (a prop matching the kid's pajamas), pivot at the mattress edge
  const arm = new THREE.Group();
  const sleeve = box(0.9, 1.9, 0.9, std("#7fa7d9", { roughness: 0.85 }), 0.1);
  sleeve.position.y = -0.85;
  arm.add(sleeve);
  const skinM = std("#f0c39b", { roughness: 0.55 });
  const hand = box(0.86, 0.62, 0.86, skinM, 0.12);
  hand.position.y = -2.08;
  arm.add(hand);
  for (let f = 0; f < 4; f++) {
    const fg = box(0.17, 0.42, 0.2, skinM, 0.06);
    fg.position.set(-0.3 + f * 0.2, -2.55, 0.12);
    arm.add(fg);
  }
  scene.add(arm);
  P.arm = arm;
  // the tongue that licks it
  const tongueM = std("#e07a90", { roughness: 0.3, emissive: "#7a2236", emissiveIntensity: 0.55 });
  const tongue = new THREE.Group();
  const tm = box(1, 0.2, 0.5, tongueM, 0.09);
  tm.position.x = 0.5;
  tongue.add(tm);
  const tip = mesh(new THREE.SphereGeometry(0.26, 14, 10), tongueM);
  tip.scale.set(1, 0.32, 1);
  tip.position.x = 1;
  tongue.add(tip);
  scene.add(tongue);
  P.tongue = { group: tongue, body: tm, tip };
  // what's really under the bed: a face in the dark and a pale hand
  const faceM = new THREE.MeshBasicMaterial({ map: T.underFace(), transparent: true, alphaTest: 0.3 });
  faceM.color.setScalar(0.85);
  const uface = mesh(new THREE.PlaneGeometry(1.5, 1.5), faceM, { cast: false });
  uface.rotation.y = Math.PI / 2;
  scene.add(uface);
  const pale = std("#d8cfc6", { roughness: 0.55 });
  const uhand = new THREE.Group();
  const up = box(0.9, 0.28, 0.85, pale, 0.1);
  uhand.add(up);
  for (let f = 0; f < 4; f++) {
    const fg = box(0.62, 0.16, 0.16, pale, 0.05);
    fg.position.set(0.72, -0.02, -0.3 + f * 0.2);
    uhand.add(fg);
  }
  const wrist = box(1.6, 0.4, 0.7, std("#2a2a30", { roughness: 0.9 }), 0.1);
  wrist.position.x = -1.15;
  uhand.add(wrist);
  scene.add(uhand);
  P.under = { face: uface, faceM, hand: uhand };
}

// --- the bathroom ------------------------------------------------------------------
function buildBathroom(scene, P) {
  const H = new THREE.Group();
  H.position.set(HX, 0, 0);
  scene.add(H);
  const add = (m, x, y, z) => {
    m.position.set(x, y, z);
    H.add(m);
    return m;
  };
  const floor = mesh(new THREE.PlaneGeometry(22, 18), std(0xffffff, { map: T.checker({ repeat: [5, 4] }), roughness: 0.35 }), { cast: false });
  floor.rotation.x = -Math.PI / 2;
  add(floor, 0, 0, 1);
  const ceil = mesh(new THREE.PlaneGeometry(22, 18), std("#e6e8e6", { roughness: 0.9 }), { cast: false });
  ceil.rotation.x = Math.PI / 2;
  add(ceil, 0, 11, 1);
  const tileM = std(0xffffff, { map: T.tiles({ repeat: [5, 3] }), roughness: 0.3 });
  const tileS = std(0xffffff, { map: T.tiles({ repeat: [4, 3] }), roughness: 0.3 });
  add(box(22, 11, 0.5, tileM, 0.02), 0, 5.5, -6.25);
  add(box(0.5, 11, 18, tileS, 0.02), -11.25, 5.5, 1);
  add(box(0.5, 11, 18, tileS, 0.02), 11.25, 5.5, 1);
  // frosted window high on the back wall
  const winM = new THREE.MeshStandardMaterial({ color: "#000", emissive: "#cfe0ff", emissiveIntensity: 0.6 });
  P.bathWindow = add(box(3.2, 2.0, 0.1, winM, 0.03), 0.6, 8.6, -5.98);
  add(box(3.5, 0.2, 0.4, std("#f2f2f0"), 0.03), 0.6, 7.5, -5.9);
  // vanity, basin, faucet, mirror
  add(box(4.2, 2.8, 2.0, std("#5d6f7c", { roughness: 0.6 }), 0.06), -5.2, 1.4, -5.0);
  add(box(4.5, 0.3, 2.3, std("#eef0ee", { roughness: 0.25 }), 0.05), -5.2, 2.95, -5.0);
  const basin = mesh(new THREE.CylinderGeometry(1.0, 0.8, 0.3, 24), std("#ffffff", { roughness: 0.15 }));
  add(basin, -5.2, 3.05, -4.9);
  const chrome = std("#d9dde2", { metalness: 0.85, roughness: 0.18 });
  add(mesh(new THREE.CylinderGeometry(0.12, 0.14, 0.9, 12), chrome), -5.2, 3.5, -5.75);
  const spout = add(box(0.18, 0.18, 0.75, chrome, 0.06), -5.2, 3.9, -5.45);
  spout.rotation.x = 0.1;
  for (const dx of [-0.55, 0.55]) add(mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.25, 12), chrome), -5.2 + dx, 3.3, -5.7);
  P.spout = [HX - 5.2, 3.78, -5.1];
  P.basinY = 3.1;
  const frame = add(box(3.7, 4.2, 0.2, std("#c9cdd2", { metalness: 0.6, roughness: 0.3 }), 0.05), -5.2, 6.4, -6.0);
  const fogPlain = T.foggedMirror(null);
  const fogText = T.foggedMirror(["HUMANS", "CAN LICK", "TOO"]);
  const mirM = new THREE.MeshBasicMaterial({ map: fogPlain });
  mirM.color.setScalar(0.92);
  const mir = mesh(new THREE.PlaneGeometry(3.4, 3.9), mirM, { cast: false });
  add(mir, -5.2, 6.4, -5.88);
  P.mirror = { mat: mirM, plain: fogPlain, text: fogText, pos: [HX - 5.2, 6.4, -5.88] };
  // towel bar + towel
  add(box(2.4, 0.12, 0.12, chrome, 0.04), -0.8, 5.0, -5.95);
  add(box(1.8, 2.6, 0.18, std("#c9734a", { roughness: 0.95 }), 0.08), -0.8, 3.8, -5.9);
  // the shower stall (right): tiled walls, glass front, shower head
  add(box(0.3, 9.5, 4.4, tileS, 0.02), 2.6, 4.75, -4.0);
  add(box(5.5, 0.3, 4.4, std("#f4f5f4", { roughness: 0.3 }), 0.04), 5.5, 0.15, -4.0);
  add(mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.15, 18), chrome), 6.2, 8.2, -5.6).rotation.x = 1.2;
  add(box(0.12, 0.12, 0.8, chrome, 0.04), 6.2, 8.4, -5.95);
  P.showerHead = [HX + 6.2, 8.05, -5.45];
  const glassM = new THREE.MeshStandardMaterial({ color: "#cfe3ee", transparent: true, opacity: 0.16, roughness: 0.08, metalness: 0.1, depthWrite: false });
  P.glassM = glassM;
  const glass = mesh(new THREE.BoxGeometry(5.4, 8.6, 0.08), glassM, { cast: false, receive: false });
  add(glass, 5.5, 4.6, -1.8);
  add(box(5.6, 0.14, 0.16, chrome, 0.04), 5.5, 8.95, -1.8);
  add(box(0.12, 2.0, 0.22, chrome, 0.04), 3.4, 4.4, -1.62);
  // the chair jammed under the handle
  const chair = new THREE.Group();
  chair.position.set(3.4, 0, -0.2);
  chair.rotation.set(0.42, 0.25, 0);
  H.add(chair);
  const cw = std("#7a5338", { roughness: 0.6 });
  const seat = box(2.0, 0.22, 1.9, cw, 0.05);
  seat.position.y = 2.1;
  chair.add(seat);
  const back = box(2.0, 2.8, 0.22, cw, 0.05);
  back.position.set(0, 3.5, -0.85);
  chair.add(back);
  for (const [lx, lz] of [[-0.85, -0.8], [0.85, -0.8], [-0.85, 0.8], [0.85, 0.8]]) {
    const l = box(0.2, 2.1, 0.2, cw, 0.04);
    l.position.set(lx, 1.05, lz);
    chair.add(l);
  }
  // water drops (faucet + shower), placed per frame
  const dropM = new THREE.MeshStandardMaterial({ color: "#cfe8ff", roughness: 0.05, metalness: 0.1, transparent: true, opacity: 0.85, emissive: "#3a5a7a", emissiveIntensity: 0.4 });
  P.drops = [];
  for (let i = 0; i < 6; i++) {
    const d = mesh(new THREE.SphereGeometry(0.07, 10, 8), dropM, { cast: false });
    d.scale.y = 1.5;
    scene.add(d);
    P.drops.push(d);
  }
  return H;
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
