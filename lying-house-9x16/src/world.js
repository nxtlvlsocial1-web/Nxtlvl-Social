// The Lying House sets. Hallway at the origin (runs toward -z); house exterior at EXT; dining room at DIN;
// broccoli hall at BRC. Light rig is the same fixed set as The Counter (stable shader programs).
import * as THREE from "three";
import * as T from "./textures.js";
import { box, mesh, std } from "./chars.js";
import { rng } from "./util.js";
import { mergeGeometries } from "three/addons/utils/BufferGeometryUtils.js";

export const EXT = new THREE.Vector3(300, 0, 0);
export const DIN = new THREE.Vector3(-300, 0, 0);
export const BRC = new THREE.Vector3(0, 0, -420);
export const HALL_W = 8, HALL_H = 9;
export const doorZ = (n) => 2 - n * 2.4; // door n position along the hallway
export const doorSide = (n) => (n % 2 ? -1 : 1); // odd left (-x), even right (+x)
export const END_Z = -116;

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

// one merged broccoli floret with vertex colours (stem + crown)
function broccoliGeometry() {
  const parts = [];
  const tint = (g, hex) => {
    const c = new THREE.Color(hex);
    const n = g.attributes.position.count;
    const arr = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) arr.set([c.r, c.g, c.b], i * 3);
    g.setAttribute("color", new THREE.BufferAttribute(arr, 3));
    return g;
  };
  const stem = new THREE.CylinderGeometry(0.22, 0.32, 1.2, 8);
  stem.translate(0, 0.6, 0);
  parts.push(tint(stem.toNonIndexed(), "#a6c96a"));
  const r = rng(3);
  const pts = [[0, 1.5, 0, 0.52], [0.42, 1.3, 0.1, 0.4], [-0.4, 1.32, -0.1, 0.42], [0.1, 1.32, 0.42, 0.4], [-0.08, 1.3, -0.44, 0.4], [0.3, 1.62, -0.25, 0.34], [-0.3, 1.6, 0.25, 0.34]];
  for (const [x, y, z, rad] of pts) {
    const s = new THREE.IcosahedronGeometry(rad, 1);
    s.translate(x, y, z);
    parts.push(tint(s.toNonIndexed(), ["#2f6b24", "#3a7d2b", "#336f27"][Math.floor(r() * 3)]));
  }
  for (const p of parts) {
    for (const k of Object.keys(p.attributes)) if (!["position", "normal", "color"].includes(k)) p.deleteAttribute(k);
  }
  return mergeGeometries(parts);
}

export function buildWorld(scene) {
  const W = { props: {}, sets: {} };
  const brocGeo = broccoliGeometry();
  const brocMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.75 });
  W.brocGeo = brocGeo;
  W.brocMat = brocMat;
  buildHall(scene, W);
  buildExterior(scene, W);
  buildDining(scene, W);
  buildBroccoliHall(scene, W);
  buildLights(scene, W);

  // travelling props
  const floret = mesh(brocGeo, brocMat);
  floret.scale.setScalar(0.28);
  scene.add(floret);
  W.props.floret = floret;
  // dust motes (rumble, door rising)
  const dustGeo = new THREE.BufferGeometry();
  dustGeo.setAttribute("position", new THREE.BufferAttribute(new Float32Array(1500 * 3), 3));
  const dust = new THREE.Points(dustGeo, new THREE.PointsMaterial({ map: T.softDot("235,225,205"), size: 0.22, transparent: true, opacity: 0.75, depthWrite: false }));
  dust.frustumCulled = false;
  scene.add(dust);
  W.dust = dust;
  return W;
}

// ---------------------------------------------------------------------------
function buildHall(scene, W) {
  const g = new THREE.Group();
  scene.add(g);
  W.sets.hall = g;
  const len = 8 - END_Z; // z from 8 down to END_Z
  const zc = (8 + END_Z) / 2;
  const floor = mesh(new THREE.PlaneGeometry(HALL_W, len), std(0xffffff, { map: T.woodFloor({ repeat: [1, len / 8] }), roughness: 0.5 }), { cast: false });
  floor.rotation.x = -Math.PI / 2;
  floor.position.set(0, 0, zc);
  g.add(floor);
  const runner = mesh(new THREE.PlaneGeometry(3.2, len - 2), std(0xffffff, { map: rep(T.rug({ seed: 8 }), 1, len / 12), roughness: 0.95 }), { cast: false });
  runner.rotation.x = -Math.PI / 2;
  runner.position.set(0, 0.03, zc);
  g.add(runner);
  const ceil = mesh(new THREE.PlaneGeometry(HALL_W, len), std(0xffffff, { map: T.plaster({ color: [40, 30, 86], repeat: [1, len / 6] }), roughness: 0.9 }), { cast: false });
  ceil.rotation.x = Math.PI / 2;
  ceil.position.set(0, HALL_H, zc);
  g.add(ceil);
  const wallTex = T.wallpaper({ color: [130, 22, 36], stripe: true, repeat: [1, 1], seed: 12 });
  const wainTex = T.woodFloor({ seed: 21, base: [22, 38, 26], plankW: 128, repeat: [1, 1] });
  const trim = std("#efe4cf", { roughness: 0.45 });
  const doorOpenings = new Map();
  for (let n = 1; n <= 47; n++) doorOpenings.set(n, { z: doorZ(n), side: doorSide(n), w: n === 47 ? 1.9 : 3.2, h: n === 47 ? 3.4 : 6.4 });
  // walls: one long slab per side (doors are drawn on top; lie rooms get real holes below)
  for (const side of [-1, 1]) {
    const holes = [12, 30, 47].map((n) => doorOpenings.get(n)).filter((o) => o.side === side).sort((a, b) => b.z - a.z);
    let zTop = 8;
    const segs = [];
    for (const o of holes) {
      segs.push([zTop, o.z + o.w / 2, 0, HALL_H]);
      segs.push([o.z + o.w / 2, o.z - o.w / 2, o.h, HALL_H]);
      zTop = o.z - o.w / 2;
    }
    segs.push([zTop, END_Z, 0, HALL_H]);
    for (const [z0, z1, y0, y1] of segs) {
      const L = z0 - z1, H = y1 - y0;
      const wall = box(0.5, H, L, std(0xffffff, { map: rep(wallTex, L / 4, H / 4), roughness: 0.85 }), 0.02);
      wall.position.set(side * (HALL_W / 2 + 0.25), (y0 + y1) / 2, (z0 + z1) / 2);
      g.add(wall);
      if (y0 === 0) {
        const wain = box(0.25, 3.2, L, std(0xffffff, { map: rep(wainTex, L / 6, 1), roughness: 0.6 }), 0.02);
        wain.position.set(side * (HALL_W / 2 - 0.05), 1.6, (z0 + z1) / 2);
        g.add(wain);
        const rail = box(0.35, 0.2, L, trim, 0.04);
        rail.position.set(side * (HALL_W / 2 - 0.1), 3.25, (z0 + z1) / 2);
        g.add(rail);
      }
    }
  }
  // back wall (behind camera start) and end wall
  const back = box(HALL_W + 1, HALL_H, 0.5, std(0xffffff, { map: rep(wallTex, 2, 2), roughness: 0.85 }), 0.02);
  back.position.set(0, HALL_H / 2, 8.25);
  g.add(back);
  // end wall with an opening for door 48 (plugged until the door appears)
  const endMat = std(0xffffff, { map: rep(wallTex, 1, 2), roughness: 0.85 });
  for (const [w, h, x, y] of [[2.7, HALL_H, -3.15, HALL_H / 2], [2.7, HALL_H, 3.15, HALL_H / 2], [3.6, HALL_H - 7.0, 0, 7.0 + (HALL_H - 7.0) / 2]]) {
    const p = box(w, h, 0.5, endMat, 0.02);
    p.position.set(x, y, END_Z - 0.25);
    g.add(p);
  }
  const plug = box(3.6, 7.0, 0.5, endMat, 0.02);
  plug.position.set(0, 3.5, END_Z - 0.25);
  g.add(plug);
  W.props.endPlug = plug;
  // pendant lamps
  const shadeMat = new THREE.MeshStandardMaterial({ color: "#f6e2b8", emissive: "#ffcf86", emissiveIntensity: 1.6, roughness: 0.7 });
  W.props.hallShade = shadeMat;
  for (let z = 2; z > END_Z + 2; z -= 10) {
    const cord = mesh(new THREE.CylinderGeometry(0.03, 0.03, 1.2, 6), std("#222"), { cast: false });
    cord.position.set(0, HALL_H - 0.6, z);
    g.add(cord);
    const shade = mesh(new THREE.CylinderGeometry(0.45, 0.8, 0.7, 20, 1, true), shadeMat, { cast: false });
    shade.position.set(0, HALL_H - 1.4, z);
    g.add(shade);
  }
  // doors
  const doorColors = ["#6a3f26", "#2d4f7c", "#7a2630", "#3f6a4a", "#5a4a7a"];
  W.props.doors = {};
  const doorTexCache = {};
  for (let n = 1; n <= 47; n++) {
    const o = doorOpenings.get(n);
    const col = doorColors[n % doorColors.length];
    if (!doorTexCache[col]) doorTexCache[col] = T.panelDoor({ color: col });
    const door = makeDoor(o.w, o.h, doorTexCache[col], trim, n);
    door.root.position.set(o.side * (HALL_W / 2 + 0.02), 0, o.z);
    door.root.rotation.y = o.side < 0 ? Math.PI / 2 : -Math.PI / 2;
    g.add(door.root);
    W.props.doors[n] = door;
  }
  // door 48: at the end of the hall, rises out of the floor
  const d48 = makeDoor(3.6, 7.0, T.panelDoor({ color: "#3b2a1c" }), std("#c9a24a", { metalness: 0.6, roughness: 0.35 }), 48, true);
  d48.root.position.set(0, 0, END_Z + 0.02);
  g.add(d48.root);
  W.props.doors[48] = d48;
  const glowBack = mesh(new THREE.PlaneGeometry(3.6, 7.0), basic("#d9ffb0", 1.1), { cast: false });
  glowBack.position.set(0, 3.5, END_Z - 0.9);
  g.add(glowBack);
  W.props.glow48 = glowBack;
  // door 49: pops out of the left wall near the end
  const d49 = makeDoor(3.2, 6.4, T.panelDoor({ color: "#7a2630" }), trim, 49, true);
  d49.root.position.set(HALL_W / 2 + 0.02, 0, END_Z + 2.9);
  d49.root.rotation.y = -Math.PI / 2;
  g.add(d49.root);
  W.props.doors[49] = d49;

  // lie rooms behind their doors
  W.props.rooms = {};
  // room 12: meatloaf (right side)
  {
    const o = doorOpenings.get(12);
    const room = new THREE.Group();
    room.position.set(HALL_W / 2 + 0.5, 0, o.z);
    roomShell(room, 8, 8, 8, std("#5a3a2a", { roughness: 0.9 }));
    const loafTex = T.meatloaf();
    const loafMat = std(0xffffff, { map: loafTex, roughness: 0.7 });
    const r = rng(12);
    const loaves = [];
    for (let i = 0; i < 70; i++) {
      const l = box(1.6, 0.9, 0.9, loafMat, 0.25);
      l.position.set(0.6 + r() * 7, 0.45 + Math.floor(i / 12) * 0.85 + r() * 0.2, (r() - 0.5) * 7);
      l.rotation.set((r() - 0.5) * 0.4, r() * 3, (r() - 0.5) * 0.4);
      room.add(l);
      loaves.push(l);
    }
    // a few loaves that tumble into the hallway when the door opens
    const spill = [0, 1, 2].map((i) => {
      const l = box(1.6, 0.9, 0.9, loafMat, 0.25);
      g.add(l);
      return l;
    });
    g.add(room);
    W.props.rooms[12] = { room, spill };
  }
  // room 30: homework towers
  {
    const o = doorOpenings.get(30);
    const room = new THREE.Group();
    room.position.set(HALL_W / 2 + 0.5, 0, o.z);
    roomShell(room, 8, 8, 8, std("#cfd6df", { roughness: 0.9 }));
    const pTex = T.paper();
    const pMat = std(0xffffff, { map: pTex, roughness: 0.8 });
    const r = rng(30);
    for (let i = 0; i < 42; i++) {
      const h = 1 + r() * 6.5;
      const st = box(1.1, h, 0.85, pMat, 0.03);
      st.position.set(0.8 + (i % 6) * 1.15 + (r() - 0.5) * 0.2, h / 2, -3.2 + Math.floor(i / 6) * 1.05);
      st.rotation.y = (r() - 0.5) * 0.25;
      room.add(st);
    }
    const sheets = [];
    for (let i = 0; i < 14; i++) {
      const sh = mesh(new THREE.PlaneGeometry(0.85, 1.1), new THREE.MeshStandardMaterial({ map: pTex, side: THREE.DoubleSide, roughness: 0.8 }), { cast: false });
      g.add(sh);
      sheets.push(sh);
    }
    g.add(room);
    W.props.rooms[30] = { room, sheets };
  }
  // room 47: Grandma's closet full of "39" balloons (left side)
  {
    const o = doorOpenings.get(47);
    const room = new THREE.Group();
    room.position.set(-HALL_W / 2 - 0.5, 0, o.z);
    room.rotation.y = Math.PI;
    roomShell(room, 4, 3.6, 3, std("#e8d8e8", { roughness: 0.9 }));
    g.add(room);
    const balloons = [];
    const cols = ["#ff5d8f", "#ffd23f", "#4fc3f7", "#9b5de5", "#00f5d4", "#ff8c42"];
    const r = rng(47);
    for (let i = 0; i < 26; i++) {
      const b = new THREE.Group();
      const m = mesh(new THREE.SphereGeometry(0.42, 18, 14), std(cols[i % cols.length], { roughness: 0.25 }));
      m.scale.set(1, 1.18, 1);
      b.add(m);
      const knot = mesh(new THREE.ConeGeometry(0.07, 0.12, 8), std(cols[i % cols.length]), { cast: false });
      knot.position.y = -0.52;
      b.add(knot);
      g.add(b);
      balloons.push({ obj: b, a: r(), b: r(), c: r() });
    }
    const nums = ["3", "9"].map((ch) => {
      const m = mesh(new THREE.PlaneGeometry(1.5, 1.9), new THREE.MeshStandardMaterial({ map: T.numberBalloon(ch), transparent: true, alphaTest: 0.4, side: THREE.DoubleSide, metalness: 0.4, roughness: 0.3 }), { cast: false });
      g.add(m);
      return m;
    });
    W.props.rooms[47] = { room, balloons, nums };
  }
}

function roomShell(room, w, h, d, mat) {
  // open toward the hallway (local -x side); w runs along +x (away from hall)
  for (const [sx, sy, sz, px, py, pz] of [[w, 0.3, d, w / 2, -0.15, 0], [w, 0.3, d, w / 2, h + 0.15, 0], [0.3, h, d, w + 0.15, h / 2, 0], [w, h, 0.3, w / 2, h / 2, d / 2 + 0.15], [w, h, 0.3, w / 2, h / 2, -d / 2 - 0.15]]) {
    const p = box(sx, sy, sz, mat, 0.02);
    p.position.set(px, py, pz);
    room.add(p);
  }
}

function makeDoor(w, h, tex, trimMat, n, plateBig = false) {
  const root = new THREE.Group();
  for (const [sx, sy, px, py] of [[0.35, h + 0.35, -w / 2 - 0.17, h / 2], [0.35, h + 0.35, w / 2 + 0.17, h / 2], [w + 0.7, 0.35, 0, h + 0.17]]) {
    const f = box(sx, sy, 0.3, trimMat, 0.05);
    f.position.set(px, py, 0.05);
    root.add(f);
  }
  const pivot = new THREE.Group();
  pivot.position.set(-w / 2, 0, 0.05);
  const panel = box(w, h, 0.22, std(0xffffff, { map: tex, roughness: 0.55 }), 0.04);
  panel.position.set(w / 2, h / 2, 0);
  pivot.add(panel);
  const knob = mesh(new THREE.SphereGeometry(0.16, 12, 10), std("#d4ac54", { metalness: 0.8, roughness: 0.3 }));
  knob.position.set(w - 0.35, h * 0.47, 0.2);
  pivot.add(knob);
  root.add(pivot);
  const pw = plateBig ? 1.2 : 0.9;
  const plate = mesh(new THREE.PlaneGeometry(pw, pw / 2), std(0xffffff, { map: T.numberPlate(n), metalness: 0.5, roughness: 0.35 }), { cast: false });
  plate.position.set(0, h + 0.75, 0.12);
  root.add(plate);
  return { root, pivot, plate, knob, w, h };
}

// ---------------------------------------------------------------------------
function buildExterior(scene, W) {
  const g = new THREE.Group();
  g.position.copy(EXT);
  scene.add(g);
  W.sets.ext = g;
  const lawn = mesh(new THREE.PlaneGeometry(220, 90), std(0xffffff, { map: T.grass({ repeat: [30, 12] }), roughness: 1 }), { cast: false });
  lawn.rotation.x = -Math.PI / 2;
  lawn.position.set(0, 0, 0);
  g.add(lawn);
  const walk = mesh(new THREE.BoxGeometry(4, 0.2, 22), std(0xffffff, { map: T.concrete({ repeat: [1, 5] }), roughness: 0.9 }));
  walk.position.set(0, 0.1, 18);
  walk.receiveShadow = true;
  g.add(walk);
  const road = mesh(new THREE.PlaneGeometry(220, 14), std(0xffffff, { map: T.asphalt({ repeat: [20, 2] }), roughness: 0.85 }), { cast: false });
  road.rotation.x = -Math.PI / 2;
  road.position.set(0, 0.02, 36);
  g.add(road);
  const sky = mesh(new THREE.PlaneGeometry(420, 200), new THREE.MeshBasicMaterial({ map: T.cloudsSky() }), { cast: false });
  sky.position.set(0, 60, -90);
  g.add(sky);
  // main house
  const sid = (c, seed, rx = 3, ry = 2) => std(0xffffff, { map: T.siding({ color: c, repeat: [rx, ry], seed }), roughness: 0.85 });
  const trim = std("#f3ead8", { roughness: 0.5 });
  const roofMat = std("#5a2f2a", { roughness: 0.9 });
  const main = box(16, 9, 12, sid([200, 35, 62], 1, 4, 3), 0.05);
  main.position.set(0, 4.5, 0);
  g.add(main);
  for (const side of [-1, 1]) {
    const rf = box(17.5, 0.5, 8.4, roofMat, 0.05);
    rf.position.set(0, 11.6, side * 3.1);
    rf.rotation.x = side * 0.72;
    g.add(rf);
  }
  const hdoor = box(2.6, 5, 0.3, std(0xffffff, { map: T.panelDoor({ color: "#7a2630" }), roughness: 0.5 }), 0.05);
  hdoor.position.set(0, 2.5, 6.1);
  g.add(hdoor);
  const windowMat = std("#9fd0ff", { roughness: 0.1, metalness: 0.3, emissive: "#3a5f80", emissiveIntensity: 0.25 });
  W.props.windowMat = windowMat;
  for (const x of [-5, 5]) {
    const w = mesh(new THREE.PlaneGeometry(2.6, 3), windowMat, { cast: false });
    w.position.set(x, 4.8, 6.06);
    g.add(w);
    const f = box(3.0, 3.4, 0.15, trim, 0.04);
    f.position.set(x, 4.8, 6.0);
    g.add(f);
  }
  // the bolted-on rooms (one per lie), deterministic patchwork
  const r = rng(99);
  const hues = [[10, 55, 55], [45, 70, 58], [160, 35, 48], [280, 30, 55], [200, 55, 50], [100, 35, 50], [330, 45, 62], [25, 60, 50]];
  const spots = [
    [6, 5, 6, -11, 2.5, 0], [5, 4, 5, 10.5, 2, -1], [7, 5, 6, -2.5, 15.3, 0], [4.5, 4, 4.5, 4, 14.8, 1], [5, 3.6, 4, -7.5, 11.3, 1],
    [3.5, 3.5, 3.5, 1.5, 19.6, 0.5], [6, 4, 5, 12, 8.2, 0], [4, 4, 4, -12.5, 7, 1], [3, 7, 3, 14.5, 3.5, 4], [5, 4, 5, -3.5, 19.8, -1],
    [3.5, 3, 3.5, -10.5, 14.4, 0], [4, 3.5, 4, 8.5, 12.3, -1.5], [3, 3, 3, -6.5, 21.5, 0], [4.5, 3.5, 4, 11, 15.2, 0.5],
  ];
  W.props.extRooms = [];
  spots.forEach(([w, h, d, x, y, z], i) => {
    const grp = new THREE.Group();
    grp.position.set(x, y, z);
    const body = box(w, h, d, sid(hues[i % hues.length], 20 + i, w / 4, h / 4), 0.06);
    grp.add(body);
    const cap = box(w + 0.6, 0.4, d + 0.6, roofMat, 0.06);
    cap.position.y = h / 2 + 0.2;
    grp.add(cap);
    const win = mesh(new THREE.PlaneGeometry(Math.min(1.6, w * 0.4), Math.min(1.6, h * 0.4)), windowMat, { cast: false });
    win.position.set((r() - 0.5) * w * 0.3, 0.2, d / 2 + 0.02);
    grp.add(win);
    const wf = box(Math.min(1.6, w * 0.4) + 0.3, Math.min(1.6, h * 0.4) + 0.3, 0.1, trim, 0.03);
    wf.position.copy(win.position);
    wf.position.z -= 0.04;
    grp.add(wf);
    if (y - h / 2 > 9.5 || (Math.abs(x) > 9 && y - h / 2 > 1)) {
      const stilt = box(0.35, y - h / 2, 0.35, std("#6a5a48"), 0.05);
      stilt.position.set(w / 2 - 0.4, -(y - h / 2) / 2 - h / 2, d / 2 - 0.4);
      if (Math.abs(x) > 9) grp.add(stilt);
    }
    g.add(grp);
    W.props.extRooms.push(grp);
  });
  // two rooms that pop into existence (hook, end card)
  W.props.popRooms = [[5, 4, 5, 6.5, 20.2, 0, [50, 75, 60]], [4, 3.5, 4, -1.5, 23.6, 0.5, [190, 60, 55]]].map(([w, h, d, x, y, z, hue], i) => {
    const grp = new THREE.Group();
    grp.position.set(x, y, z);
    const inner = new THREE.Group();
    inner.position.y = -h / 2;
    grp.add(inner);
    const body = box(w, h, d, sid(hue, 40 + i, w / 4, h / 4), 0.06);
    body.position.y = h / 2;
    inner.add(body);
    const cap = box(w + 0.6, 0.4, d + 0.6, roofMat, 0.06);
    cap.position.y = h + 0.2;
    inner.add(cap);
    const win = mesh(new THREE.PlaneGeometry(1.4, 1.4), windowMat, { cast: false });
    win.position.set(0, h / 2, d / 2 + 0.02);
    inner.add(win);
    g.add(grp);
    return { grp, inner, x, y, z };
  });
  // trees and a fence
  const treeMat = std("#3f7a32", { roughness: 0.9 });
  const trunkMat = std("#6a4a2a", { roughness: 0.9 });
  for (const [x, z, s] of [[-24, 4, 1.2], [22, 6, 1.0], [-30, -10, 1.5], [28, -8, 1.3], [-18, 14, 0.8]]) {
    const t = box(1, 5 * s, 1, trunkMat, 0.1);
    t.position.set(x, 2.5 * s, z);
    g.add(t);
    const c = box(5 * s, 4.5 * s, 5 * s, treeMat, 1.2 * s);
    c.position.set(x, 6.2 * s, z);
    g.add(c);
  }
  for (let x = -40; x <= 40; x += 2.2) {
    if (Math.abs(x) < 3) continue;
    const post = box(0.3, 1.8, 0.3, trim, 0.05);
    post.position.set(x, 0.9, 27);
    g.add(post);
  }
  const rail = box(80, 0.25, 0.2, trim, 0.05);
  rail.position.set(0, 1.4, 27);
  g.add(rail);
}

// ---------------------------------------------------------------------------
function buildDining(scene, W) {
  const g = new THREE.Group();
  g.position.copy(DIN);
  scene.add(g);
  W.sets.dining = g;
  const floor = mesh(new THREE.PlaneGeometry(36, 30), std(0xffffff, { map: T.woodFloor({ seed: 5, repeat: [4, 3.5] }), roughness: 0.55 }), { cast: false });
  floor.rotation.x = -Math.PI / 2;
  g.add(floor);
  const wallTex = T.wallpaper({ color: [215, 22, 38], stripe: true, repeat: [1, 1], seed: 14 });
  for (const [w, h, d, x, y, z] of [[36, 12, 0.5, 0, 6, -12], [0.5, 12, 30, -16, 6, 0], [0.5, 12, 30, 16, 6, 0], [36, 12, 0.5, 0, 6, 13]]) {
    const wall = box(w, h, d, std(0xffffff, { map: rep(wallTex, Math.max(w, d) / 4, 3), roughness: 0.85 }), 0.02);
    wall.position.set(x, y, z);
    g.add(wall);
  }
  const ceil = mesh(new THREE.PlaneGeometry(36, 30), std(0xffffff, { map: T.plaster({ repeat: [5, 4] }), roughness: 0.9 }), { cast: false });
  ceil.rotation.x = Math.PI / 2;
  ceil.position.y = 12;
  g.add(ceil);
  const win = mesh(new THREE.PlaneGeometry(6, 4.5), new THREE.MeshBasicMaterial({ map: T.skyGradient([[0, "#0b1230"], [1, "#2c3b72"]], { stars: 80 }) }), { cast: false });
  win.position.set(-3, 6.2, -11.7);
  g.add(win);
  const winDay = mesh(new THREE.PlaneGeometry(6, 4.5), new THREE.MeshBasicMaterial({ map: T.cloudsSky({ seed: 7 }), transparent: true, opacity: 0 }), { cast: false });
  winDay.position.set(-3, 6.2, -11.68);
  g.add(winDay);
  W.props.dinWinDay = winDay;
  const trim = std("#efe4cf", { roughness: 0.45 });
  const wf = box(6.6, 5.1, 0.2, trim, 0.05);
  wf.position.set(-3, 6.2, -11.8);
  g.add(wf);
  // table, cloth, chairs
  const wood = std("#6a4126", { roughness: 0.5 });
  const top = box(11, 0.35, 4.6, wood, 0.08);
  top.position.y = 3.1;
  g.add(top);
  for (const [x, z] of [[-5, -2], [5, -2], [-5, 2], [5, 2]]) {
    const l = box(0.35, 3, 0.35, wood, 0.05);
    l.position.set(x, 1.5, z);
    g.add(l);
  }
  const runner = box(9.5, 0.04, 1.4, std("#c9b28a", { roughness: 0.9 }), 0.01);
  runner.position.y = 3.3;
  g.add(runner);
  W.props.chairs = {};
  const seats = { kid: [-2.6, 3.2, Math.PI], sister: [2.6, 3.2, Math.PI], mom: [-2.6, -3.2, 0], dad: [2.6, -3.2, 0], grandma: [6.6, 0, -Math.PI / 2] };
  for (const [who, [x, z, ry]] of Object.entries(seats)) {
    const ch = new THREE.Group();
    ch.position.set(x, 0, z);
    ch.rotation.y = ry;
    const seat = box(2.4, 0.3, 2.2, wood, 0.06);
    seat.position.y = 2.05;
    ch.add(seat);
    const backrest = box(2.4, 3.2, 0.3, wood, 0.06);
    backrest.position.set(0, 3.6, -1.0);
    ch.add(backrest);
    for (const [lx, lz] of [[-1, -0.9], [1, -0.9], [-1, 0.9], [1, 0.9]]) {
      const l = box(0.22, 2, 0.22, wood, 0.04);
      l.position.set(lx, 1, lz);
      ch.add(l);
    }
    g.add(ch);
    W.props.chairs[who] = { x: DIN.x + x, z: DIN.z + z, ry };
  }
  // plates
  W.props.plates = {};
  const plateMat = std("#f4f1ea", { roughness: 0.3 });
  for (const [who, [x, z]] of Object.entries({ kid: [-2.6, 1.4], sister: [2.6, 1.4], mom: [-2.6, -1.4], dad: [2.6, -1.4], grandma: [4.6, 0] })) {
    const p = mesh(new THREE.CylinderGeometry(0.75, 0.6, 0.08, 24), plateMat);
    p.position.set(x, 3.32, z);
    g.add(p);
    W.props.plates[who] = new THREE.Vector3(DIN.x + x, 3.38, DIN.z + z);
  }
  const loaf = box(1.0, 0.45, 0.55, std(0xffffff, { map: T.meatloaf(), roughness: 0.7 }), 0.15);
  loaf.position.set(2.6, 3.6, -1.4);
  g.add(loaf);
  W.props.dadLoaf = loaf;
  // broccoli on the kid's plate (flashback)
  const plateBroc = [0, 1, 2].map((i) => {
    const b = mesh(W.brocGeo, W.brocMat);
    b.scale.setScalar(0.32);
    b.position.set(DIN.x - 2.9 + i * 0.32, 3.36, DIN.z + 1.3 + (i % 2) * 0.2);
    b.rotation.set(0, i * 1.7, 0.2);
    scene.add(b);
    return b;
  });
  W.props.plateBroc = plateBroc;
  // pendant over the table
  const lampMat = new THREE.MeshStandardMaterial({ color: "#f6e2b8", emissive: "#ffcf86", emissiveIntensity: 1.6, roughness: 0.7 });
  const shade = mesh(new THREE.CylinderGeometry(0.8, 1.6, 1.2, 24, 1, true), lampMat, { cast: false });
  shade.position.set(0, 9.3, 0);
  g.add(shade);
  const cord = mesh(new THREE.CylinderGeometry(0.04, 0.04, 2.2, 6), std("#222"), { cast: false });
  cord.position.set(0, 11, 0);
  g.add(cord);
  W.props.dinLamp = lampMat;
}

// ---------------------------------------------------------------------------
function buildBroccoliHall(scene, W) {
  const g = new THREE.Group();
  g.position.copy(BRC);
  scene.add(g);
  W.sets.broc = g;
  const floor = mesh(new THREE.PlaneGeometry(110, 120), std(0xffffff, { map: T.woodFloor({ seed: 9, repeat: [10, 11] }), roughness: 0.55 }), { cast: false });
  floor.rotation.x = -Math.PI / 2;
  g.add(floor);
  const wallTex = T.wallpaper({ color: [110, 25, 30], stripe: true, repeat: [1, 1], seed: 19 });
  for (const [w, h, d, x, y, z] of [[110, 60, 1, 0, 30, -60], [1, 60, 120, -55, 30, 0], [1, 60, 120, 55, 30, 0], [110, 60, 1, 0, 30, 60]]) {
    const wall = box(w, h, d, std(0xffffff, { map: rep(wallTex, Math.max(w, d) / 6, h / 6), roughness: 0.85 }), 0.02);
    wall.position.set(x, y, z);
    g.add(wall);
  }
  // skylight ceiling
  const ceil = mesh(new THREE.PlaneGeometry(110, 120), std("#2a3a2a", { roughness: 0.9 }), { cast: false });
  ceil.rotation.x = Math.PI / 2;
  ceil.position.y = 60;
  g.add(ceil);
  const sky = mesh(new THREE.PlaneGeometry(40, 50), basic("#f2ffe0", 1.4), { cast: false });
  sky.rotation.x = Math.PI / 2;
  sky.position.set(0, 59.5, -5);
  g.add(sky);
  // the doorway we came in through (on the +z wall), warm hallway light behind
  const trim = std("#c9a24a", { metalness: 0.6, roughness: 0.35 });
  for (const [sx, sy, px, py] of [[0.4, 7.4, -2.0, 3.7], [0.4, 7.4, 2.0, 3.7], [4.4, 0.4, 0, 7.4]]) {
    const f = box(sx, sy, 0.6, trim, 0.05);
    f.position.set(px, py, 59.4);
    g.add(f);
  }
  const hallGlow = mesh(new THREE.PlaneGeometry(3.6, 7.0), basic("#ffcf86", 0.75), { cast: false });
  hallGlow.position.set(0, 3.5, 59.6);
  hallGlow.rotation.y = Math.PI;
  g.add(hallGlow);
  // broccoli mountains: bumpy green cones dressed with florets
  const r = rng(48);
  const mounts = [[-18, -22, 22, 34], [14, -30, 26, 42], [0, -8, 16, 24], [-30, 10, 14, 20], [26, 4, 15, 22], [-8, 22, 9, 12], [12, 26, 8, 10]];
  const coneMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.85 });
  const florets = [];
  for (const [x, z, R, H] of mounts) {
    const cg = new THREE.ConeGeometry(R, H, 36, 10);
    const pos = cg.attributes.position;
    const col = new Float32Array(pos.count * 3);
    const c = new THREE.Color();
    for (let i = 0; i < pos.count; i++) {
      const y = pos.getY(i);
      if (y < H / 2 - 0.1 && y > -H / 2 + 0.1) {
        const k = 1 + (r() - 0.5) * 0.18;
        pos.setX(i, pos.getX(i) * k);
        pos.setZ(i, pos.getZ(i) * k);
      }
      c.setHSL(0.27 + r() * 0.04, 0.55, 0.22 + r() * 0.1);
      col.set([c.r, c.g, c.b], i * 3);
    }
    cg.setAttribute("color", new THREE.BufferAttribute(col, 3));
    cg.computeVertexNormals();
    const cone = mesh(cg, coneMat);
    cone.position.set(x, H / 2, z);
    g.add(cone);
    const n = Math.round(R * R * 0.55);
    for (let k = 0; k < n; k++) {
      const hy = Math.pow(r(), 0.8);
      const rad = R * (1 - hy) * 0.98;
      const a = r() * Math.PI * 2;
      florets.push([x + Math.cos(a) * rad, hy * H - 0.3, z + Math.sin(a) * rad, 1.1 + r() * 1.6, a, r()]);
    }
    florets.push([x, H - 0.8, z, 4 + r() * 1.5, r() * 6, 0.5]);
  }
  for (let k = 0; k < 140; k++) florets.push([(r() - 0.5) * 90, -0.2, (r() - 0.5) * 100, 0.8 + r() * 1.4, r() * 6, r()]);
  const inst = new THREE.InstancedMesh(W.brocGeo, W.brocMat, florets.length);
  inst.castShadow = true;
  inst.receiveShadow = true;
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler();
  florets.forEach(([x, y, z, s, a, tilt], i) => {
    e.set((tilt - 0.5) * 0.6, a, (tilt - 0.5) * 0.5);
    q.setFromEuler(e);
    m4.compose(new THREE.Vector3(x + BRC.x, y + BRC.y, z + BRC.z), q, new THREE.Vector3(s, s, s));
    inst.setMatrixAt(i, m4);
  });
  scene.add(inst);
  W.props.brocCount = florets.length;
  // a few loose florets for the avalanche
  W.props.avalanche = Array.from({ length: 24 }, () => {
    const b = mesh(W.brocGeo, W.brocMat);
    scene.add(b);
    return b;
  });
}

// ---------------------------------------------------------------------------
function buildLights(scene, W) {
  const hemi = new THREE.HemisphereLight("#8fa0d0", "#3a2418", 0.5);
  scene.add(hemi);
  const key = new THREE.DirectionalLight("#9fb4ff", 1.2);
  key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  key.shadow.bias = -0.0004;
  key.shadow.normalBias = 0.03;
  const sc = key.shadow.camera;
  sc.left = -40;
  sc.right = 40;
  sc.top = 40;
  sc.bottom = -40;
  sc.near = 1;
  sc.far = 220;
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
