// Sets, props and the light rig. Living room at the origin; street at x=+300; wedding at x=-300;
// macro insert table at z=+300.
import * as THREE from "three";
import * as T from "./textures.js";
import { box, mesh, std } from "./chars.js";
import { rng } from "./util.js";

export const EXT = new THREE.Vector3(300, 0, 0);
export const WED = new THREE.Vector3(-300, 0, 0);
export const INS = new THREE.Vector3(0, 0, 300);

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
  const W = { props: {}, sets: {} };
  const tex = {
    floor: T.woodFloor({ repeat: [1, 1] }),
    wall: T.wallpaper({ color: [292, 18, 33], repeat: [1, 1] }),
    wainscot: T.woodFloor({ seed: 21, base: [22, 38, 26], plankW: 128, repeat: [1, 1] }),
    ceiling: T.plaster({ color: [30, 14, 78], repeat: [1, 1] }),
    rug: T.rug(),
    couch: T.knit({ colors: ["#5b3f2b", "#7a5a34", "#36515a", "#8e3a2a"], band: 5, repeat: [3, 1] }),
    armchair: T.velvet({ color: [120, 22, 26], repeat: [2, 2] }),
    rice: T.rice({ repeat: [1, 1] }),
  };

  // ---------------- living room ----------------
  const room = new THREE.Group();
  room.name = "room";
  scene.add(room);
  W.sets.room = room;
  const floorMat = std(0xffffff, { map: rep(tex.floor, 4.2, 3.5), roughness: 0.55 });
  const floor = mesh(new THREE.PlaneGeometry(44, 36), floorMat, { cast: false });
  floor.rotation.x = -Math.PI / 2;
  room.add(floor);
  const ceil = mesh(new THREE.PlaneGeometry(44, 36), std(0xffffff, { map: rep(tex.ceiling, 6, 5), roughness: 0.9 }), { cast: false });
  ceil.rotation.x = Math.PI / 2;
  ceil.position.y = 14;
  room.add(ceil);

  const wallMat = (w, h) => std(0xffffff, { map: rep(tex.wall, w / 4, h / 4), roughness: 0.85 });
  // wall segment along X (facing +z if dir=1) or along Z
  function wallX(x0, x1, y0, y1, z, t = 0.6) {
    const w = x1 - x0, h = y1 - y0;
    const m = box(w, h, t, wallMat(w, h), 0.02);
    m.position.set((x0 + x1) / 2, (y0 + y1) / 2, z);
    room.add(m);
    return m;
  }
  function wallZ(z0, z1, y0, y1, x, t = 0.6) {
    const w = z1 - z0, h = y1 - y0;
    const m = box(t, h, w, wallMat(w, h), 0.02);
    m.position.set(x, (y0 + y1) / 2, (z0 + z1) / 2);
    room.add(m);
    return m;
  }
  // back wall z=-16 with window hole x 0..8, y 3.5..9.5
  wallX(-20, 0, 0, 14, -16.3);
  wallX(8, 20, 0, 14, -16.3);
  wallX(0, 8, 0, 3.5, -16.3);
  wallX(0, 8, 9.5, 14, -16.3);
  // left wall x=-20 with door hole z -8.5..-3.5, y 0..9
  wallZ(-16, -8.5, 0, 14, -20.3);
  wallZ(-3.5, 16, 0, 14, -20.3);
  wallZ(-8.5, -3.5, 9, 14, -20.3);
  // right wall, front wall (with dark kitchen arch x 6..14)
  wallZ(-16, 16, 0, 14, 20.3);
  wallX(-20, 6, 0, 14, 16.3);
  wallX(14, 20, 0, 14, 16.3);
  wallX(6, 14, 10, 14, 16.3);
  const archDark = mesh(new THREE.PlaneGeometry(8, 10), basic("#1a1410"), { cast: false });
  archDark.position.set(10, 5, 17.5);
  archDark.rotation.y = Math.PI;
  room.add(archDark);

  // wainscot panels + chair rail + baseboard
  const wainMat = (len) => std(0xffffff, { map: rep(tex.wainscot, len / 6, 1), roughness: 0.6 });
  const trimMat = std("#e8dcc6", { roughness: 0.5 });
  function wainX(x0, x1, z, s) {
    const len = x1 - x0;
    const p = box(len, 4, 0.3, wainMat(len), 0.02);
    p.position.set((x0 + x1) / 2, 2, z + s * 0.2);
    room.add(p);
    const rail = box(len, 0.25, 0.5, trimMat, 0.05);
    rail.position.set((x0 + x1) / 2, 4.1, z + s * 0.3);
    room.add(rail);
  }
  function wainZ(z0, z1, x, s) {
    const len = z1 - z0;
    const p = box(0.3, 4, len, wainMat(len), 0.02);
    p.position.set(x + s * 0.2, 2, (z0 + z1) / 2);
    room.add(p);
    const rail = box(0.5, 0.25, len, trimMat, 0.05);
    rail.position.set(x + s * 0.3, 4.1, (z0 + z1) / 2);
    room.add(rail);
  }
  wainX(-20, 0, -16, 1);
  wainX(8, 20, -16, 1);
  wainX(0, 8, -16, 1);
  wainZ(-16, -8.5, -20, 1);
  wainZ(-3.5, 16, -20, 1);
  wainZ(-16, 16, 20, -1);
  wainX(-20, 6, 16, -1);
  wainX(14, 20, 16, -1);

  // window (back wall) with frame, cross bars, sill, curtains and sky behind
  const frameMat = std("#efe6d4", { roughness: 0.45 });
  for (const [w, h, x, y] of [[8.6, 0.4, 4, 9.6], [8.6, 0.4, 4, 3.4], [0.4, 6.4, -0.1, 6.5], [0.4, 6.4, 8.1, 6.5], [0.2, 6, 4, 6.5], [8, 0.2, 4, 6.5]]) {
    const f = box(w, h, 0.5, frameMat, 0.05);
    f.position.set(x, y, -16.1);
    room.add(f);
  }
  const sill = box(9.4, 0.3, 1.2, frameMat, 0.06);
  sill.position.set(4, 3.25, -15.6);
  room.add(sill);
  const skyGeo = new THREE.PlaneGeometry(30, 22);
  const skyNight = mesh(skyGeo, new THREE.MeshBasicMaterial({ map: T.skyGradient([[0, "#0b1230"], [0.6, "#1d2a5a"], [1, "#2c3b72"]], { stars: 160, moon: [170, 150, 16] }) }), { cast: false });
  skyNight.position.set(4, 6, -24);
  room.add(skyNight);
  const skyDawn = mesh(skyGeo, new THREE.MeshBasicMaterial({ map: T.skyGradient([[0, "#3a4f8a"], [0.45, "#e98a5a"], [0.75, "#ffc27a"], [1, "#fff0c0"]]), transparent: true, opacity: 0 }), { cast: false });
  skyDawn.position.set(4, 6, -23.9);
  room.add(skyDawn);
  const skyDay = mesh(skyGeo, new THREE.MeshBasicMaterial({ map: T.skyGradient([[0, "#7fb4ef"], [1, "#d8ecff"]]), transparent: true, opacity: 0 }), { cast: false });
  skyDay.position.set(4, 6, -23.8);
  room.add(skyDay);
  // a tree silhouette outside
  const treeMat = basic("#0a0f1c");
  const trunk = mesh(new THREE.BoxGeometry(1, 10, 1), treeMat, { cast: false });
  trunk.position.set(15, 4, -22);
  room.add(trunk);
  const crown = mesh(new THREE.SphereGeometry(4.5, 12, 10), treeMat, { cast: false });
  crown.position.set(16.5, 10, -22.5);
  room.add(crown);
  W.props.sky = { night: skyNight, dawn: skyDawn, day: skyDay, tree: [trunk, crown] };
  const curtainMat = std("#7a2630", { roughness: 0.9 });
  for (const side of [-1, 1]) {
    for (let i = 0; i < 4; i++) {
      const c = box(0.7, 10, 0.5, curtainMat, 0.2);
      c.position.set(4 + side * (5.2 + i * 0.6), 6.2, -15.5 + (i % 2) * 0.25);
      room.add(c);
    }
  }
  const rod = mesh(new THREE.CylinderGeometry(0.1, 0.1, 15, 8), std("#3a2a1a", { metalness: 0.5, roughness: 0.4 }));
  rod.rotation.z = Math.PI / 2;
  rod.position.set(4, 11.3, -15.4);
  room.add(rod);

  // front door (left wall) on a hinge at z=-8.5
  const doorPivot = new THREE.Group();
  doorPivot.position.set(-20.1, 0, -8.5);
  room.add(doorPivot);
  const door = box(0.35, 9, 5, std(0xffffff, { map: T.panelDoor(), roughness: 0.55 }), 0.05);
  door.position.set(0, 4.5, 2.5);
  doorPivot.add(door);
  const knob = mesh(new THREE.SphereGeometry(0.22, 12, 10), std("#c9a24a", { metalness: 0.8, roughness: 0.3 }));
  knob.position.set(0.35, 4.4, 4.4);
  doorPivot.add(knob);
  for (const [w, h, d, y, z] of [[0.7, 0.45, 6.0, 9.2, -6], [0.7, 9, 0.45, 4.5, -8.75], [0.7, 9, 0.45, 4.5, -3.25]]) {
    const f = box(w, h, d, frameMat, 0.05);
    f.position.set(-19.9, y, z);
    room.add(f);
  }
  W.props.door = doorPivot;
  // outside the door: porch + night
  const porch = mesh(new THREE.PlaneGeometry(14, 14), std("#5d5548", { roughness: 0.9 }), { cast: false });
  porch.rotation.x = -Math.PI / 2;
  porch.position.set(-27, 0.02, -6);
  room.add(porch);
  const outside = mesh(new THREE.PlaneGeometry(30, 24), new THREE.MeshBasicMaterial({ map: T.skyGradient([[0, "#060a1a"], [0.7, "#141d40"], [1, "#25305a"]], { stars: 60 }) }), { cast: false });
  outside.position.set(-34, 8, -6);
  outside.rotation.y = Math.PI / 2;
  room.add(outside);
  for (const z of [-11, -1]) {
    const post = box(0.6, 10, 0.6, frameMat, 0.06);
    post.position.set(-25, 5, z);
    room.add(post);
  }

  // jar table by the door
  const woodDark = std("#5a3a22", { roughness: 0.55 });
  const woodMid = std("#7a5230", { roughness: 0.55 });
  const table = new THREE.Group();
  table.position.set(-18.4, 0, 0.2);
  const top = box(1.8, 0.25, 3.6, woodDark, 0.06);
  top.position.y = 3.3;
  table.add(top);
  for (const [x, z] of [[-0.7, -1.5], [0.7, -1.5], [-0.7, 1.5], [0.7, 1.5]]) {
    const l = box(0.25, 3.2, 0.25, woodDark, 0.04);
    l.position.set(x, 1.6, z);
    table.add(l);
  }
  room.add(table);
  W.props.jarTable = table;

  // grandfather clock
  const clock = new THREE.Group();
  clock.position.set(-18.6, 0, -13);
  clock.rotation.y = Math.PI / 2;
  const cbody = box(2.6, 9.5, 1.4, woodMid, 0.08);
  cbody.position.y = 4.75;
  clock.add(cbody);
  const hood = box(3.0, 1.0, 1.7, woodDark, 0.1);
  hood.position.y = 10.0;
  clock.add(hood);
  const crest = box(1.4, 0.6, 1.4, woodDark, 0.1);
  crest.position.y = 10.8;
  clock.add(crest);
  const faceDisc = mesh(new THREE.CircleGeometry(1.05, 40), std(0xffffff, { map: T.clockFace(), roughness: 0.4 }), { cast: false });
  faceDisc.position.set(0, 8.2, 0.72);
  clock.add(faceDisc);
  const handMat = std("#16110c", { roughness: 0.3, metalness: 0.4 });
  const hourHand = new THREE.Group(), minHand = new THREE.Group();
  for (const [g, len, w] of [[hourHand, 0.55, 0.09], [minHand, 0.85, 0.06]]) {
    const m = box(w, len, 0.03, handMat, 0.01);
    m.position.y = len / 2 - 0.08;
    g.add(m);
    g.position.set(0, 8.2, 0.76);
    clock.add(g);
  }
  const pend = new THREE.Group();
  pend.position.set(0, 7.0, 0.5);
  const rodP = box(0.08, 3.2, 0.05, std("#c9a24a", { metalness: 0.8, roughness: 0.3 }), 0.02);
  rodP.position.y = -1.6;
  pend.add(rodP);
  const bob = mesh(new THREE.CylinderGeometry(0.42, 0.42, 0.12, 24), std("#d8b25a", { metalness: 0.85, roughness: 0.25 }));
  bob.rotation.x = Math.PI / 2;
  bob.position.y = -3.3;
  pend.add(bob);
  clock.add(pend);
  const cglass = mesh(new THREE.PlaneGeometry(1.8, 4.2), new THREE.MeshStandardMaterial({ color: "#cfe0ea", transparent: true, opacity: 0.12, roughness: 0.05 }), { cast: false });
  cglass.position.set(0, 4.9, 0.71);
  clock.add(cglass);
  const cdark = mesh(new THREE.PlaneGeometry(1.9, 4.4), basic("#20140b"), { cast: false });
  cdark.position.set(0, 4.9, 0.45);
  clock.add(cdark);
  room.add(clock);
  W.props.clock = { root: clock, hourHand, minHand, pend };
  // hands from a clock time in hours (e.g. 11.9167 = 11:55)
  W.setClock = (hours) => {
    minHand.rotation.z = -((hours % 1) * Math.PI * 2);
    hourHand.rotation.z = -(((hours % 12) / 12) * Math.PI * 2);
  };

  // bookshelf: 300 books
  const shelf = new THREE.Group();
  shelf.position.set(-11, 0, -15.2);
  const sw = 8.4, sh = 11;
  for (const [w, h, d, x, y, z] of [[0.35, sh, 1.6, -sw / 2, sh / 2, 0], [0.35, sh, 1.6, sw / 2, sh / 2, 0], [sw, 0.35, 1.6, 0, sh, 0], [sw, sh, 0.15, 0, sh / 2, -0.75]]) {
    const p = box(w, h, d, woodDark, 0.04);
    p.position.set(x, y, z);
    shelf.add(p);
  }
  const bookGeo = new THREE.BoxGeometry(1, 1, 1);
  const books = new THREE.InstancedMesh(bookGeo, std(0xffffff, { roughness: 0.7 }), 300);
  books.castShadow = true;
  books.receiveShadow = true;
  const r = rng(77);
  const palette = ["#8c2f2b", "#2f4a6b", "#3d6b4a", "#c9a24a", "#5a3a5e", "#d8cfb7", "#a5552a", "#1f2a36", "#6e7b3a"];
  const mtx = new THREE.Matrix4(), col = new THREE.Color();
  let bi = 0;
  for (let s = 0; s < 5; s++) {
    const y0 = 0.4 + s * 2.15;
    const board = box(sw, 0.25, 1.5, woodDark, 0.04);
    board.position.set(0, y0 - 0.12, 0);
    shelf.add(board);
    let x = -sw / 2 + 0.25;
    for (let k = 0; k < 60; k++) {
      const bw = 0.11 + r() * 0.03, bh = 1.3 + r() * 0.5, bd = 1.0 + r() * 0.3;
      mtx.compose(new THREE.Vector3(x + bw / 2, y0 + bh / 2, 0.1), new THREE.Quaternion().setFromEuler(new THREE.Euler(0, 0, (r() - 0.5) * 0.05)), new THREE.Vector3(bw, bh, bd));
      books.setMatrixAt(bi, mtx);
      books.setColorAt(bi, col.set(palette[Math.floor(r() * palette.length)]).offsetHSL(0, 0, (r() - 0.5) * 0.08));
      bi++;
      x += bw + 0.005;
    }
  }
  shelf.add(books);
  room.add(shelf);
  W.props.shelf = shelf;

  // rug
  const rugM = mesh(new THREE.PlaneGeometry(14, 19), std(0xffffff, { map: tex.rug, roughness: 0.95 }), { cast: false });
  rugM.rotation.x = -Math.PI / 2;
  rugM.rotation.z = Math.PI / 2;
  rugM.position.set(1, 0.03, -3.5);
  room.add(rugM);

  // couch (faces the back wall; its back is towards +z)
  const couch = new THREE.Group();
  couch.position.set(-1, 0, 3);
  const cm = std(0xffffff, { map: tex.couch, roughness: 0.95 });
  const cm2 = std(0xffffff, { map: rep(tex.couch, 1, 1), roughness: 0.95 });
  const base = box(12, 1.7, 4.6, cm, 0.2);
  base.position.set(0, 1.25, 0);
  couch.add(base);
  const back = box(12, 2.9, 1.3, cm, 0.3);
  back.position.set(0, 2.95, 1.75);
  couch.add(back);
  for (const side of [-1, 1]) {
    const arm = box(1.3, 2.9, 4.6, cm, 0.3);
    arm.position.set(side * 6.0, 2.0, 0);
    couch.add(arm);
  }
  for (let i = -1; i <= 1; i++) {
    const cu = box(3.6, 0.8, 3.4, cm2, 0.3);
    cu.position.set(i * 3.65, 2.45, -0.3);
    couch.add(cu);
  }
  const cushions = [];
  for (const [x, c] of [[-4, "#c7843a"], [4.1, "#3f6a72"]]) {
    const p = box(2.1, 2.1, 0.7, std(c, { roughness: 0.9 }), 0.35);
    p.position.set(x, 3.4, 0.75);
    p.rotation.set(-0.25, 0, x < 0 ? 0.15 : -0.12);
    couch.add(p);
    cushions.push(p);
  }
  for (const [x, z] of [[-5.6, -2], [5.6, -2], [-5.6, 2], [5.6, 2]]) {
    const l = box(0.4, 0.45, 0.4, woodDark, 0.05);
    l.position.set(x, 0.22, z);
    couch.add(l);
  }
  room.add(couch);
  W.props.couch = couch;
  W.props.cushions = cushions;

  // Grandpa's armchair
  const chair = new THREE.Group();
  chair.position.set(11, 0, -5);
  chair.rotation.y = 2.3;
  const vm = std(0xffffff, { map: tex.armchair, roughness: 0.8 });
  const cbase = box(5, 1.8, 4.6, vm, 0.25);
  cbase.position.set(0, 1.3, 0);
  chair.add(cbase);
  const cback = box(5, 5.2, 1.2, vm, 0.35);
  cback.position.set(0, 3.9, 1.8);
  chair.add(cback);
  for (const side of [-1, 1]) {
    const a = box(1.0, 2.8, 4.6, vm, 0.35);
    a.position.set(side * 2.5, 2.2, 0);
    chair.add(a);
  }
  const seat = box(3.9, 0.7, 3.4, vm, 0.3);
  seat.position.set(0, 2.45, -0.3);
  chair.add(seat);
  room.add(chair);
  W.props.chair = chair;

  // floor lamp (the practical light)
  const lamp = new THREE.Group();
  lamp.position.set(15.5, 0, -9);
  const brass = std("#b8913f", { metalness: 0.8, roughness: 0.35 });
  const lbase = mesh(new THREE.CylinderGeometry(0.9, 1.0, 0.25, 24), brass);
  lbase.position.y = 0.12;
  lamp.add(lbase);
  const pole = mesh(new THREE.CylinderGeometry(0.09, 0.09, 6.6, 10), brass);
  pole.position.y = 3.4;
  lamp.add(pole);
  const shadeMat = new THREE.MeshStandardMaterial({ color: "#f3dfb6", emissive: "#ffb768", emissiveIntensity: 1.4, side: THREE.DoubleSide, roughness: 0.8 });
  const shade = mesh(new THREE.CylinderGeometry(0.9, 1.35, 1.5, 28, 1, true), shadeMat, { cast: false });
  shade.position.y = 7.2;
  lamp.add(shade);
  const bulb = mesh(new THREE.SphereGeometry(0.28, 12, 10), glow("#ffd9a0", 6), { cast: false });
  bulb.position.y = 6.95;
  lamp.add(bulb);
  room.add(lamp);
  W.props.lamp = { root: lamp, shadeMat, bulb, pos: new THREE.Vector3(15.5, 7.1, -9) };

  // side table + cup
  const stable = new THREE.Group();
  stable.position.set(8.2, 0, -8.6);
  const stTop = mesh(new THREE.CylinderGeometry(1.2, 1.2, 0.2, 24), woodDark);
  stTop.position.y = 2.6;
  stable.add(stTop);
  const stLeg = mesh(new THREE.CylinderGeometry(0.15, 0.25, 2.5, 10), woodDark);
  stLeg.position.y = 1.3;
  stable.add(stLeg);
  room.add(stable);
  const cup = new THREE.Group();
  const cupM = mesh(new THREE.CylinderGeometry(0.32, 0.27, 0.62, 18), std("#e9e2d2", { roughness: 0.3 }));
  cupM.position.y = 0.31;
  cup.add(cupM);
  const handle = mesh(new THREE.TorusGeometry(0.17, 0.05, 8, 14), std("#e9e2d2", { roughness: 0.3 }));
  handle.position.set(0.36, 0.33, 0);
  cup.add(handle);
  room.add(cup);
  W.props.cup = cup;
  W.props.cupHome = () => { cup.position.set(8.2, 2.7, -8.6); cup.rotation.set(0, 0.6, 0); };

  // sock basket
  const basket = new THREE.Group();
  basket.position.set(-8.6, 0, 6.2);
  const bk = mesh(new THREE.CylinderGeometry(1.25, 1.05, 1.7, 20, 1, true), std(0xffffff, { map: T.wicker(), roughness: 0.9, side: THREE.DoubleSide }));
  bk.position.y = 0.85;
  basket.add(bk);
  const sockCols = ["#d94b4b", "#3f7fd1", "#f2d04a", "#5bb36a", "#f2f2f2", "#9b59b6", "#ff8c42", "#222", "#ec6fa5"];
  const sr = rng(5);
  for (let i = 0; i < 26; i++) {
    const s = box(0.5, 0.32, 1.1, std(sockCols[i % sockCols.length], { roughness: 0.95 }), 0.14);
    const a = sr() * Math.PI * 2, d = sr() * 0.9;
    s.position.set(Math.cos(a) * d, 1.5 + sr() * 0.9 - d * 0.4, Math.sin(a) * d);
    s.rotation.set(sr() * 2, sr() * 3, sr() * 2);
    basket.add(s);
  }
  room.add(basket);
  W.props.basket = basket;

  // wall socket by the armchair (right wall)
  const socket = new THREE.Group();
  socket.position.set(-19.95, 1.4, 4.5);
  socket.rotation.y = Math.PI;
  const plate = box(0.1, 0.9, 0.6, std("#f4efe4", { roughness: 0.4 }), 0.04);
  socket.add(plate);
  for (const y of [0.18, -0.18]) {
    for (const z of [-0.08, 0.08]) {
      const slot = mesh(new THREE.BoxGeometry(0.04, 0.12, 0.04), basic("#1a1a1a"), { cast: false });
      slot.position.set(-0.06, y, z);
      socket.add(slot);
    }
  }
  room.add(socket);
  W.props.socket = socket;

  // picture frames
  for (const [x, y, z, ry, w, h, c] of [[-4.5, 8.2, -15.9, 0, 3, 2.2, "#4c6a8a"], [19.9, 7.8, 4, -Math.PI / 2, 4, 3, "#7a8a4c"], [-19.9, 7.6, 9, Math.PI / 2, 3, 3.6, "#8a5a4c"]]) {
    const fr = box(w + 0.4, h + 0.4, 0.2, woodDark, 0.04);
    fr.position.set(x, y, z);
    fr.rotation.y = ry;
    room.add(fr);
    const pic = mesh(new THREE.PlaneGeometry(w, h), std(c, { roughness: 0.6 }), { cast: false });
    pic.position.set(x, y, z);
    pic.rotation.y = ry;
    pic.translateZ(0.12);
    room.add(pic);
  }
  // ceiling light fixture (off)
  const fixture = mesh(new THREE.CylinderGeometry(1.6, 1.2, 0.8, 24), std("#e8dcc6", { roughness: 0.5 }));
  fixture.position.set(0, 13.6, -2);
  room.add(fixture);

  // ---------------- props that travel between shots ----------------
  W.props.jar = makeJar(tex.rice);
  scene.add(W.props.jar.root);
  W.props.vacuum = makeVacuum();
  scene.add(W.props.vacuum.root);
  W.props.broom = makeBroom();
  scene.add(W.props.broom);
  W.props.bag = makeRiceBag();
  scene.add(W.props.bag);
  W.props.moth = makeMoth();
  scene.add(W.props.moth.root);
  W.props.plug = makePlug();
  scene.add(W.props.plug);
  W.props.hands = [makePaleHand(), makePaleHand()];
  W.props.hands.forEach((h) => scene.add(h.root));
  const crumb = box(0.22, 0.12, 0.2, std("#8a5a2a", { roughness: 0.9 }), 0.04);
  scene.add(crumb);
  W.props.crumb = crumb;
  const stool = new THREE.Group();
  const stoolWood = std("#a8743f", { roughness: 0.6 });
  const stTop2 = box(2.4, 0.3, 2.0, stoolWood, 0.08);
  stTop2.position.y = 1.05;
  stool.add(stTop2);
  for (const [x, z] of [[-0.95, -0.75], [0.95, -0.75], [-0.95, 0.75], [0.95, 0.75]]) {
    const l = box(0.25, 1.0, 0.25, stoolWood, 0.04);
    l.position.set(x, 0.5, z);
    stool.add(l);
  }
  scene.add(stool);
  W.props.stool = stool;

  // Z letters for snoring
  const zMat = new THREE.SpriteMaterial({ map: T.zLetter(), transparent: true, depthWrite: false });
  W.props.zs = [0, 1, 2].map(() => {
    const s = new THREE.Sprite(zMat.clone());
    scene.add(s);
    return s;
  });

  // rice grains (instanced) and dust motes
  const riceGeo = new THREE.CapsuleGeometry(0.028, 0.12, 2, 6);
  const rice = new THREE.InstancedMesh(riceGeo, std("#f3eedf", { roughness: 0.45 }), 7000);
  rice.castShadow = false;
  rice.receiveShadow = true;
  rice.frustumCulled = false;
  rice.count = 0;
  scene.add(rice);
  W.rice = rice;
  const dustGeo = new THREE.BufferGeometry();
  dustGeo.setAttribute("position", new THREE.BufferAttribute(new Float32Array(3000 * 3), 3));
  const dust = new THREE.Points(dustGeo, new THREE.PointsMaterial({ map: T.softDot("235,225,205"), size: 0.18, transparent: true, opacity: 0.7, depthWrite: false, sizeAttenuation: true }));
  dust.frustumCulled = false;
  scene.add(dust);
  W.dust = dust;

  buildStreet(scene, W);
  buildWedding(scene, W);
  buildInserts(scene, W, tex);
  buildLights(scene, W);
  return W;
}

// ---------------------------------------------------------------------------
function makeJar(riceTex) {
  const root = new THREE.Group();
  const glass = mesh(new THREE.CylinderGeometry(0.75, 0.75, 1.9, 32, 1, true),
    new THREE.MeshStandardMaterial({ color: "#d9eef0", transparent: true, opacity: 0.28, roughness: 0.04, side: THREE.DoubleSide, depthWrite: false }), { cast: false });
  glass.position.y = 0.95;
  root.add(glass);
  const bottom = mesh(new THREE.CylinderGeometry(0.75, 0.75, 0.08, 32), new THREE.MeshStandardMaterial({ color: "#cfe6e8", transparent: true, opacity: 0.4, roughness: 0.05 }), { cast: false });
  bottom.position.y = 0.04;
  root.add(bottom);
  const neck = mesh(new THREE.TorusGeometry(0.66, 0.08, 10, 32), new THREE.MeshStandardMaterial({ color: "#d9eef0", transparent: true, opacity: 0.4, roughness: 0.05 }), { cast: false });
  neck.rotation.x = Math.PI / 2;
  neck.position.y = 1.9;
  root.add(neck);
  const fill = mesh(new THREE.CylinderGeometry(0.7, 0.7, 1, 32), std(0xffffff, { map: riceTex, roughness: 0.7 }), { cast: false });
  root.add(fill);
  const lid = mesh(new THREE.CylinderGeometry(0.78, 0.78, 0.3, 32), std("#8a5a30", { roughness: 0.6 }));
  lid.position.y = 2.05;
  root.add(lid);
  const label = mesh(new THREE.CylinderGeometry(0.755, 0.755, 0.6, 32, 1, true, -0.7, 1.4), std("#e9dcc0", { roughness: 0.8 }), { cast: false });
  label.position.y = 0.9;
  root.add(label);
  return {
    root, lid, fill,
    setFill(f) {
      fill.visible = f > 0.01;
      fill.scale.y = Math.max(0.01, f * 1.8);
      fill.position.y = 0.08 + (f * 1.8) / 2;
    },
  };
}

function makeVacuum() {
  const root = new THREE.Group();
  const red = std("#c0332b", { roughness: 0.35 });
  const grey = std("#3a3d44", { roughness: 0.5 });
  const fabric = std("#9aa0a6", { roughness: 0.95 });
  const base = box(2.4, 0.55, 1.8, red, 0.18);
  base.position.y = 0.42;
  root.add(base);
  for (const x of [-1.0, 1.0]) {
    const w = mesh(new THREE.CylinderGeometry(0.28, 0.28, 0.2, 16), grey);
    w.rotation.z = Math.PI / 2;
    w.position.set(x, 0.28, -0.7);
    root.add(w);
  }
  const body = box(1.5, 3.2, 0.9, red, 0.2);
  body.position.set(0, 2.2, -0.4);
  root.add(body);
  // removable parts
  const bag = box(1.15, 2.2, 0.55, fabric, 0.18);
  bag.position.set(0, 2.15, 0.15);
  root.add(bag);
  const lid = box(1.55, 0.45, 1.25, grey, 0.12);
  lid.position.set(0, 3.95, -0.2);
  root.add(lid);
  const handle = mesh(new THREE.CylinderGeometry(0.09, 0.09, 3.4, 10), grey);
  handle.position.set(0, 5.4, -0.55);
  root.add(handle);
  const grip = box(0.9, 0.3, 0.3, grey, 0.1);
  grip.position.set(0, 7.1, -0.55);
  root.add(grip);
  const light = mesh(new THREE.SphereGeometry(0.09, 10, 8), glow("#40ff70", 0.1), { cast: false });
  light.position.set(0.5, 3.5, 0.06);
  root.add(light);
  return { root, bag, lid, light, homes: { bag: bag.position.clone(), lid: lid.position.clone() } };
}

function makeBroom() {
  const g = new THREE.Group();
  const stick = mesh(new THREE.CylinderGeometry(0.08, 0.08, 6, 10), std("#b0844a", { roughness: 0.6 }));
  stick.position.y = 3.5;
  g.add(stick);
  const head = box(1.4, 1.0, 0.45, std("#d9b45a", { roughness: 0.95 }), 0.1);
  head.position.y = 0.5;
  g.add(head);
  const band = box(1.45, 0.25, 0.5, std("#c0332b"), 0.05);
  band.position.y = 1.0;
  g.add(band);
  return g;
}

function makeRiceBag() {
  const g = new THREE.Group();
  const b = box(1.3, 1.9, 0.6, std("#e9dcc0", { roughness: 0.9 }), 0.2);
  b.position.y = 0.95;
  g.add(b);
  const lbl = box(1.32, 0.6, 0.62, std("#c0332b", { roughness: 0.8 }), 0.05);
  lbl.position.y = 0.9;
  g.add(lbl);
  return g;
}

function makeMoth() {
  const root = new THREE.Group();
  const wm = new THREE.MeshStandardMaterial({ color: "#f4efe2", emissive: "#fff4dc", emissiveIntensity: 0.4, side: THREE.DoubleSide, roughness: 0.9 });
  const wings = [];
  for (const side of [-1, 1]) {
    const w = new THREE.Group();
    const m = mesh(new THREE.PlaneGeometry(0.35, 0.28), wm, { cast: false });
    m.position.x = side * 0.18;
    w.add(m);
    root.add(w);
    wings.push(w);
  }
  const body = mesh(new THREE.CapsuleGeometry(0.04, 0.14, 2, 6), std("#8a7a64"), { cast: false });
  body.rotation.z = Math.PI / 2;
  root.add(body);
  return { root, wings };
}

// a detached Counter forearm + hand for inserts. Origin at the wrist, fingers along -y.
function makePaleHand() {
  const root = new THREE.Group();
  const pale = std("#d6d3ca", { roughness: 0.55 });
  const coat = std("#26262f", { roughness: 0.8 });
  const fore = box(0.4, 2.6, 0.4, pale, 0.08);
  fore.position.y = 1.3;
  root.add(fore);
  const cuff = box(0.64, 0.5, 0.64, coat, 0.08);
  cuff.position.y = 2.7;
  root.add(cuff);
  const sleeve = box(0.6, 3, 0.6, std("#1b1b22", { roughness: 0.85 }), 0.1);
  sleeve.position.y = 4.4;
  root.add(sleeve);
  const palm = box(0.5, 0.55, 0.22, pale, 0.06);
  palm.position.y = -0.2;
  root.add(palm);
  const fingers = [];
  for (let f = 0; f < 4; f++) {
    const fg = new THREE.Group();
    fg.position.set(-0.18 + f * 0.12, -0.46, 0);
    const m = box(0.1, 1.05 - Math.abs(f - 1.5) * 0.12, 0.12, pale, 0.04);
    m.position.y = -0.48;
    fg.add(m);
    root.add(fg);
    fingers.push(fg);
  }
  const thumb = new THREE.Group();
  thumb.position.set(-0.28, -0.25, 0.05);
  const tm = box(0.1, 0.6, 0.12, pale, 0.04);
  tm.position.y = -0.28;
  thumb.add(tm);
  thumb.rotation.z = -0.6;
  root.add(thumb);
  return { root, fingers };
}

function makePlug() {
  const g = new THREE.Group();
  const head = box(0.3, 0.45, 0.32, std("#f4efe4", { roughness: 0.5 }), 0.06);
  g.add(head);
  for (const z of [-0.08, 0.08]) {
    const p = mesh(new THREE.BoxGeometry(0.22, 0.04, 0.03), std("#c9a24a", { metalness: 0.9, roughness: 0.3 }));
    p.position.set(-0.24, 0, z);
    g.add(p);
  }
  const cord = mesh(new THREE.CylinderGeometry(0.05, 0.05, 3, 8), std("#2a2a2a", { roughness: 0.6 }));
  cord.rotation.z = Math.PI / 2;
  cord.position.x = 1.6;
  g.add(cord);
  return g;
}

// ---------------------------------------------------------------------------
function buildStreet(scene, W) {
  const g = new THREE.Group();
  g.position.copy(EXT);
  scene.add(g);
  W.sets.street = g;
  const road = mesh(new THREE.PlaneGeometry(220, 22), std(0xffffff, { map: T.asphalt({ repeat: [20, 2] }), roughness: 0.85 }), { cast: false });
  road.rotation.x = -Math.PI / 2;
  road.position.set(0, 0, 14);
  g.add(road);
  for (let x = -100; x < 100; x += 8) {
    const dash = mesh(new THREE.PlaneGeometry(3.5, 0.35), basic("#bfb68a", 0.6), { cast: false });
    dash.rotation.x = -Math.PI / 2;
    dash.position.set(x, 0.02, 14);
    g.add(dash);
  }
  const walk = mesh(new THREE.BoxGeometry(220, 0.4, 5), std(0xffffff, { map: T.concrete({ repeat: [40, 1] }), roughness: 0.9 }));
  walk.position.set(0, 0.2, 0.5);
  walk.receiveShadow = true;
  g.add(walk);
  const lawn = mesh(new THREE.PlaneGeometry(220, 26), std(0xffffff, { map: T.grass({ repeat: [24, 3] }), roughness: 1 }), { cast: false });
  lawn.rotation.x = -Math.PI / 2;
  lawn.position.set(0, 0.05, -10);
  g.add(lawn);
  const sky = mesh(new THREE.PlaneGeometry(400, 160), new THREE.MeshBasicMaterial({ map: T.skyGradient([[0, "#070b20"], [0.55, "#16214a"], [0.85, "#2a356a"], [1, "#3b4478"]], { stars: 240, moon: [190, 120, 14] }) }), { cast: false });
  sky.position.set(0, 50, -90);
  g.add(sky);
  W.props.streetJars = [];
  const colors = [[214, 30, 40], [292, 20, 34], [150, 14, 36]];
  for (let i = 0; i < 3; i++) {
    const hx = (i - 1) * 26;
    const house = new THREE.Group();
    house.position.set(hx, 0, -16);
    const walls = box(20, 13, 14, std(0xffffff, { map: T.siding({ color: colors[i], repeat: [4, 3], seed: 7 + i }), roughness: 0.85 }), 0.05);
    walls.position.y = 6.5;
    house.add(walls);
    const roofMat = std("#2a2326", { roughness: 0.9 });
    for (const side of [-1, 1]) {
      const rf = box(22, 0.6, 9.8, roofMat, 0.05);
      rf.position.set(0, 16.2, side * 3.6);
      rf.rotation.x = side * 0.72;
      house.add(rf);
    }
    const gable = mesh(new THREE.CylinderGeometry(0, 9.5, 6, 3, 1), std(0xffffff, { map: T.siding({ color: colors[i], repeat: [3, 2], seed: 9 + i }), roughness: 0.85 }));
    gable.rotation.set(0, 0, 0);
    gable.scale.set(1, 1, 0.01);
    gable.position.set(0, 16, 7.05);
    house.add(gable);
    const trim = std("#ece4d4", { roughness: 0.5 });
    // porch deck, steps, posts, roof
    const deck = box(12, 1.2, 5, std("#6b5a48", { roughness: 0.8 }), 0.05);
    deck.position.set(0, 0.6, 9.4);
    house.add(deck);
    for (let s = 0; s < 2; s++) {
      const st = box(4, 0.4, 1.0, std("#7d6a55", { roughness: 0.8 }), 0.04);
      st.position.set(0, 0.2 + s * 0.4, 12.4 - s * 1.0);
      house.add(st);
    }
    for (const x of [-5.6, 5.6]) {
      const p = box(0.5, 8, 0.5, trim, 0.05);
      p.position.set(x, 5.2, 11.6);
      house.add(p);
    }
    const proof = box(13, 0.5, 5.6, roofMat, 0.05);
    proof.position.set(0, 9.4, 9.6);
    house.add(proof);
    const hdoor = box(3.6, 7, 0.3, std(0xffffff, { map: T.panelDoor({ color: ["#7a2630", "#2d4f7c", "#2f5a3a"][i] }), roughness: 0.5 }), 0.05);
    hdoor.position.set(0, 4.7, 7.1);
    house.add(hdoor);
    for (const x of [-6.5, 6.5]) {
      const win = mesh(new THREE.PlaneGeometry(3.4, 4), i === 1 && x > 0 ? glow("#ffb968", 1.6) : basic("#141a2e"), { cast: false });
      win.position.set(x, 6.5, 7.06);
      house.add(win);
      const wf = box(3.9, 4.5, 0.15, trim, 0.04);
      wf.position.set(x, 6.5, 7.0);
      house.add(wf);
    }
    const plamp = mesh(new THREE.BoxGeometry(0.5, 0.7, 0.4), glow("#ffd29a", 5), { cast: false });
    plamp.position.set(2.6, 7.2, 7.3);
    house.add(plamp);
    g.add(house);
    const jar = makeJar(T.rice());
    jar.setFill(0.92);
    jar.root.position.set(hx + 1.2, 1.2, -16 + 11.3);
    g.add(jar.root);
    W.props.streetJars.push(jar);
  }
  // street lamp
  const pole = mesh(new THREE.CylinderGeometry(0.2, 0.25, 16, 10), std("#2a2c30", { metalness: 0.4, roughness: 0.5 }));
  pole.position.set(16, 8, 3.5);
  g.add(pole);
  const lampHead = mesh(new THREE.BoxGeometry(1.4, 0.5, 2.4), glow("#ffcf8a", 4), { cast: false });
  lampHead.position.set(16, 15.8, 4.2);
  g.add(lampHead);
}

function buildWedding(scene, W) {
  const g = new THREE.Group();
  g.position.copy(WED);
  scene.add(g);
  W.sets.wedding = g;
  const fl = mesh(new THREE.PlaneGeometry(80, 60), std(0xffffff, { map: T.woodFloor({ seed: 31, base: [30, 30, 40], repeat: [7, 5] }), roughness: 0.5 }), { cast: false });
  fl.rotation.x = -Math.PI / 2;
  g.add(fl);
  const back = mesh(new THREE.PlaneGeometry(80, 30), std(0xffffff, { map: T.wallpaper({ color: [30, 25, 22], stripe: true, repeat: [16, 6], seed: 33 }), roughness: 0.9 }), { cast: false });
  back.position.set(0, 15, -20);
  g.add(back);
  // string lights: catenary arcs of glowing bulbs
  const bulbGeo = new THREE.SphereGeometry(0.18, 8, 6);
  const bulbMat = glow("#ffd59a", 7);
  for (let arc = 0; arc < 6; arc++) {
    const z = -18 + arc * 4.2, y0 = 13 - arc * 0.3;
    for (let k = 0; k <= 28; k++) {
      const x = -30 + (k / 28) * 60;
      const y = y0 - 2.4 * (1 - ((x / 30) ** 2));
      const b = mesh(bulbGeo, bulbMat, { cast: false });
      b.position.set(x, y, z);
      g.add(b);
    }
  }
  // table, cloth, cake
  const cloth = box(10, 3.2, 4.5, std("#f6f2ea", { roughness: 0.9 }), 0.15);
  cloth.position.set(6, 1.6, -4);
  g.add(cloth);
  const frost = T.cakeFrosting();
  const icing = std(0xffffff, { map: frost, roughness: 0.6 });
  [[1.6, 1.3], [1.15, 1.1], [0.75, 0.95]].reduce((y, [rad, h]) => {
    const tier = mesh(new THREE.CylinderGeometry(rad, rad, h, 32), icing);
    tier.position.set(6, y + h / 2, -4);
    g.add(tier);
    return y + h;
  }, 3.2);
  const topper = mesh(new THREE.SphereGeometry(0.3, 12, 10), std("#f2b8c6"));
  topper.position.set(6, 6.7, -4);
  g.add(topper);
  // bunting
  const flagCols = ["#f2b8c6", "#f6f2ea", "#c9e4de", "#f7d794"];
  for (let k = 0; k < 18; k++) {
    const f = mesh(new THREE.CircleGeometry(0.6, 3), basic(flagCols[k % 4], 0.8), { cast: false });
    f.position.set(-14 + k * 1.7, 10.5 - Math.sin((k / 17) * Math.PI) * 1.4, -12);
    f.rotation.z = -Math.PI / 2;
    g.add(f);
  }
}

function buildInserts(scene, W, tex) {
  const g = new THREE.Group();
  g.position.copy(INS);
  scene.add(g);
  W.sets.inserts = g;
  // a long wooden surface for macro shots
  const top = mesh(new THREE.BoxGeometry(80, 1, 20), std(0xffffff, { map: T.woodFloor({ seed: 41, base: [26, 42, 36], repeat: [6, 2] }), roughness: 0.5 }));
  top.position.set(20, -0.5, 0);
  top.receiveShadow = true;
  g.add(top);
  const backdrop = mesh(new THREE.PlaneGeometry(90, 30), std("#2b2230", { roughness: 1 }), { cast: false });
  backdrop.position.set(20, 10, -9);
  g.add(backdrop);
  // spoons in an open drawer at x=0
  const drawer = new THREE.Group();
  const wood = std("#6a4528", { roughness: 0.6 });
  for (const [w, h, d, x, y, z] of [[7, 0.2, 4, 0, 0.1, 0], [7, 1, 0.2, 0, 0.5, -2], [7, 1, 0.2, 0, 0.5, 2], [0.2, 1, 4, -3.5, 0.5, 0], [0.2, 1, 4, 3.5, 0.5, 0]]) {
    const p = box(w, h, d, wood, 0.03);
    p.position.set(x, y, z);
    drawer.add(p);
  }
  const steel = new THREE.MeshStandardMaterial({ color: "#d8dde2", metalness: 1, roughness: 0.22 });
  for (let i = 0; i < 8; i++) {
    const sp = new THREE.Group();
    const bowl = mesh(new THREE.SphereGeometry(0.32, 16, 10), steel);
    bowl.scale.set(0.75, 0.25, 1.1);
    bowl.position.z = 1.2;
    sp.add(bowl);
    const h = box(0.12, 0.05, 2.4, steel, 0.02);
    sp.add(h);
    sp.position.set(-3 + i * 0.85, 0.35, 0);
    sp.rotation.y = (i % 2 ? 1 : -1) * 0.04;
    drawer.add(sp);
  }
  g.add(drawer);
  // socks on a rug at x=20
  const rugS = mesh(new THREE.PlaneGeometry(10, 8), std(0xffffff, { map: tex.rug, roughness: 0.95 }), { cast: false });
  rugS.rotation.x = -Math.PI / 2;
  rugS.position.set(20, 0.02, 0);
  g.add(rugS);
  const sockCols = ["#d94b4b", "#3f7fd1", "#f2d04a", "#5bb36a", "#f2f2f2", "#9b59b6", "#ff8c42", "#ec6fa5"];
  const r = rng(9);
  for (let i = 0; i < 34; i++) {
    const s = new THREE.Group();
    const leg = box(0.55, 0.3, 1.5, std(sockCols[i % sockCols.length], { roughness: 0.95 }), 0.14);
    s.add(leg);
    const foot = box(0.55, 0.3, 0.8, leg.material, 0.14);
    foot.position.set(0, 0, 0.9);
    foot.rotation.y = 0.9;
    s.add(foot);
    const a = r() * Math.PI * 2, d = r() * 2.6;
    s.position.set(20 + Math.cos(a) * d, 0.2 + (2.6 - d) * 0.35 + r() * 0.2, Math.sin(a) * d);
    s.rotation.set((r() - 0.5) * 0.8, r() * 6, (r() - 0.5) * 0.8);
    g.add(s);
  }
  // rice heap at x=40 handled by the instanced rice
  W.props.insert = { drawerAt: new THREE.Vector3(0, 0, 0).add(INS), socksAt: new THREE.Vector3(20, 0, 0).add(INS), riceAt: new THREE.Vector3(40, 0, 0).add(INS) };
}

// ---------------------------------------------------------------------------
// Fixed light rig: the same lights every frame (stable shader programs); presets move and tint them.
function buildLights(scene, W) {
  const hemi = new THREE.HemisphereLight("#8fa0d0", "#3a2418", 0.5);
  scene.add(hemi);
  const key = new THREE.DirectionalLight("#9fb4ff", 1.2);
  key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  key.shadow.bias = -0.0004;
  key.shadow.normalBias = 0.03;
  const sc = key.shadow.camera;
  sc.left = -32;
  sc.right = 32;
  sc.top = 32;
  sc.bottom = -32;
  sc.near = 1;
  sc.far = 160;
  scene.add(key);
  scene.add(key.target);
  const prac = new THREE.SpotLight("#ffb46a", 120, 0, 1.25, 0.85, 2);
  prac.castShadow = true;
  prac.shadow.mapSize.set(1024, 1024);
  prac.shadow.bias = -0.0005;
  prac.shadow.normalBias = 0.04;
  prac.shadow.camera.near = 0.5;
  prac.shadow.camera.far = 80;
  scene.add(prac);
  scene.add(prac.target);
  const glows = [0, 1, 2, 3].map(() => {
    const p = new THREE.PointLight("#ffb46a", 0, 0, 2);
    scene.add(p);
    return p;
  });
  W.lights = { hemi, key, prac, glows };
}
