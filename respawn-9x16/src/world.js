// Respawn: three sets, each its own group (shots switch them on).
//  city : a sunset beach boulevard. Hospital at the north end (big steps, glowing doors), pastel art-deco blocks,
//         palms, a beach and the sea at the east end with the sun on the horizon. Traffic, a getaway car, a cruiser.
//  icu  : the real hospital room, far away at z = 900: bed, heart monitor, chair, window, Lily's drawing.
//  rain : the real street on the day of the crash, at z = -900: grey, wet, a school sign, an oncoming truck.
import * as THREE from "three";
import * as T from "./textures.js";
import * as K from "./tex-city.js";
import { box, mesh, std } from "./chars.js";
import { rng } from "./util.js";

export const STEPS = { x0: -12, x1: 12, z0: -22, n: 8, rise: 0.5, run: 1.0 }; // step i top: y=(i+1)*0.5, z -22-i .. -23-i
export const LAND = { y: 4, z: -32 }; // landing at the top of the steps
export const DOORS = { z: -35.9, x: 0, y: 4, w: 10, h: 8 };
export const ICU = [0, 0, 900];
export const RAIN = [0, 0, -900];
export const PHOTO = [0, 0, 1400];
export const SUN = [390, 22, 0];

const glowM = (color, k = 2) => new THREE.MeshStandardMaterial({ color: "#000", emissive: color, emissiveIntensity: k });
const basic = (color, k = 1, o = {}) => {
  const m = new THREE.MeshBasicMaterial({ color, ...o });
  m.color.multiplyScalar(k);
  return m;
};
const add = (parent, m, x = 0, y = 0, z = 0) => {
  m.position.set(x, y, z);
  parent.add(m);
  return m;
};
const plane = (w, h, mat, o = {}) => mesh(new THREE.PlaneGeometry(w, h), mat, { cast: false, ...o });

export function buildWorld(scene) {
  const W = { props: {}, sets: {} };
  const P = W.props;
  for (const [name, pos] of [["city", [0, 0, 0]], ["icu", ICU], ["rain", RAIN], ["photo", PHOTO]]) {
    const g = new THREE.Group();
    g.position.set(...pos);
    g.visible = false;
    scene.add(g);
    W.sets[name] = g;
  }
  buildCity(W.sets.city, P);
  buildICU(W.sets.icu, P);
  buildRain(W.sets.rain, P);
  buildPhoto(W.sets.photo, P);
  P.car = makeCar({ color: "#8c1424", interior: true });
  P.cop = makeCar({ color: "#f2f2f0", police: true });
  P.famCar = makeCar({ color: "#9aa3ab", interior: true, wipers: true });
  for (const c of [P.car, P.cop, P.famCar]) scene.add(c.group);
  buildLights(scene, W);
  scene.fog = new THREE.FogExp2("#f29a7a", 0.0);
  return W;
}

// ---------------------------------------------------------------------------------------------
function palm(parent, x, z, { h = 15, lean = 0.12, dir = 0, seed = 1, cast = true } = {}) {
  const r = rng(seed);
  const g = new THREE.Group();
  g.position.set(x, 0, z);
  g.rotation.y = dir;
  parent.add(g);
  const barkM = std(0xffffff, { map: K.bark(), roughness: 0.9 });
  const segs = 7;
  let px = 0, py = 0;
  for (let i = 0; i < segs; i++) {
    const k = i / segs, len = h / segs;
    const ang = lean * (0.4 + k * 1.2);
    const s = mesh(new THREE.CylinderGeometry(0.42 - k * 0.12, 0.5 - k * 0.12, len + 0.1, 7), barkM, { cast });
    s.position.set(px + Math.sin(ang) * len / 2, py + Math.cos(ang) * len / 2, 0);
    s.rotation.z = -ang;
    g.add(s);
    px += Math.sin(ang) * len;
    py += Math.cos(ang) * len;
  }
  const crown = new THREE.Group();
  crown.position.set(px, py, 0);
  g.add(crown);
  const leafM = std("#2f8a4a", { roughness: 0.7 });
  const leafM2 = std("#3fa35a", { roughness: 0.7 });
  for (let i = 0; i < 9; i++) {
    const a = (i / 9) * Math.PI * 2 + r() * 0.3;
    const leaf = new THREE.Group();
    leaf.rotation.y = a;
    crown.add(leaf);
    const l1 = box(0.9, 0.16, 3.4, i % 2 ? leafM : leafM2, 0.06);
    l1.position.set(0, 0.5, 1.6);
    l1.rotation.x = -0.25;
    leaf.add(l1);
    const l2 = box(0.75, 0.14, 3.0, i % 2 ? leafM : leafM2, 0.06);
    l2.position.set(0, -0.35, 4.3);
    l2.rotation.x = 0.55 + r() * 0.2;
    leaf.add(l2);
  }
  const nut = box(1.1, 0.9, 1.1, std("#6b4a2a"), 0.3);
  nut.position.set(0, -0.3, 0);
  crown.add(nut);
  return g;
}

function streetLamp(parent, x, z, face = 1) {
  const g = new THREE.Group();
  g.position.set(x, 0, z);
  parent.add(g);
  const m = std("#2a2d33", { roughness: 0.5, metalness: 0.4 });
  add(g, mesh(new THREE.CylinderGeometry(0.18, 0.24, 13, 8), m), 0, 6.5, 0);
  add(g, box(0.25, 0.25, 3, m, 0.05), 0, 13, face * 1.4);
  const head = add(g, box(0.9, 0.35, 1.4, std("#2a2d33"), 0.1), 0, 12.8, face * 2.8);
  const bulb = add(g, plane(0.7, 1.1, glowM("#ffd7a0", 0)), 0, 12.6, face * 2.8);
  bulb.rotation.x = Math.PI / 2;
  return { g, bulb: bulb.material, head };
}

function buildCity(G, P) {
  // ground, road, sidewalks, plaza
  add(G, plane(900, 900, std("#cdb497", { roughness: 0.95 }), { receive: true }), 0, -0.02, 0).rotation.x = -Math.PI / 2;
  const roadHold = add(G, new THREE.Group(), -20, 0.01, 0);
  roadHold.rotation.y = Math.PI / 2;
  const rt = K.road();
  rt.repeat.set(1, 15);
  const roadM = std(0xffffff, { map: rt, roughness: 0.82 });
  const rd = add(roadHold, plane(12, 260, roadM, { receive: true }), 0, 0, 0);
  rd.rotation.x = -Math.PI / 2;
  const walkT = T.concrete({ repeat: [60, 1] });
  const walkM = std(0xe8dfd2, { map: walkT, roughness: 0.9 });
  for (const z of [-8.2, 8.2]) add(G, box(260, 0.32, 4.4, walkM, 0.02), -20, 0.16, z);
  const plazaM = std(0xf0e8dc, { map: T.concrete({ repeat: [10, 3] }), roughness: 0.85 });
  add(G, box(52, 0.3, 11.6, plazaM, 0.02), 0, 0.15, -16.2);
  // crosswalk at the plaza
  const stripeM = std("#efece6", { roughness: 0.7 });
  for (let i = 0; i < 8; i++) add(G, box(1.2, 0.04, 11, stripeM, 0.01), -8.4 + i * 2.4, 0.03, 0);

  // the steps, the landing, the hospital
  const stepM = std(0xf4efe6, { map: T.concrete({ repeat: [6, 1] }), roughness: 0.8 });
  for (let i = 0; i < STEPS.n; i++) {
    const hgt = (i + 1) * STEPS.rise, depth = STEPS.n - i + 2;
    add(G, box(26, hgt, depth, stepM, 0.02), 0, hgt / 2, STEPS.z0 - i - depth / 2);
  }
  add(G, box(40, LAND.y, 8, stepM, 0.02), 0, LAND.y / 2, -33);
  // handrails
  const railM = std("#b9bcc2", { roughness: 0.55, metalness: 0.25 });
  for (const x of [-6.5, 6.5]) {
    const rail = add(G, box(0.22, 0.22, 11.4, railM, 0.05), x, 3.9, -26.4);
    rail.rotation.x = Math.atan2(4, 8);
    for (const k of [0, 0.5, 1]) add(G, box(0.18, 2.6, 0.18, railM, 0.04), x, 0.5 + k * 3.6 + 1.0, -22 - k * 8.6);
  }
  const hosp = new THREE.Group();
  G.add(hosp);
  const facT = K.hospitalFacade();
  facT.repeat.set(2.5, 1.6);
  const wallM = std("#ece6db", { roughness: 0.85 });
  const facM = std(0xffffff, { map: facT, roughness: 0.6 });
  add(hosp, box(72, 46, 22, [wallM, wallM, wallM, wallM, facM, wallM], 0.05), 0, 23, -47);
  // wings stepping back
  add(hosp, box(26, 28, 18, [wallM, wallM, wallM, wallM, facM, wallM], 0.05), -48, 14, -50);
  add(hosp, box(26, 28, 18, [wallM, wallM, wallM, wallM, facM, wallM], 0.05), 48, 14, -50);
  // entrance: recess, glass doors (slide apart), white light inside
  add(hosp, box(14, 10, 0.6, std("#2a3138", { roughness: 0.4 }), 0.02), 0, 9, -35.9);
  const inside = add(hosp, plane(DOORS.w, DOORS.h, basic("#eaf6ff", 0.9)), 0, DOORS.y + DOORS.h / 2, -35.55);
  P.inside = inside.material;
  const glassM = new THREE.MeshStandardMaterial({ color: "#9fd0e8", transparent: true, opacity: 0.55, roughness: 0.05, metalness: 0.6, emissive: "#bfe6ff", emissiveIntensity: 0.6 });
  P.doorL = add(hosp, box(DOORS.w / 2, DOORS.h, 0.18, glassM, 0.02), -DOORS.w / 4, DOORS.y + DOORS.h / 2, -35.3);
  P.doorR = add(hosp, box(DOORS.w / 2, DOORS.h, 0.18, glassM, 0.02), DOORS.w / 4, DOORS.y + DOORS.h / 2, -35.3);
  P.doorGlass = glassM;
  // canopy with the sign, two pillars
  add(hosp, box(20, 0.8, 7, std("#f7f4ee", { roughness: 0.6 }), 0.1), 0, 13.4, -32.6);
  const sign = add(hosp, plane(16, 3.12, new THREE.MeshStandardMaterial({ map: K.hospitalSign(), emissive: "#ffffff", emissiveMap: K.hospitalSign(), emissiveIntensity: 0.55, roughness: 0.4 })), 0, 15.4, -32.0);
  P.sign = sign.material;
  add(hosp, box(16.4, 3.5, 0.4, std("#1b3f6e"), 0.05), 0, 15.4, -32.25);
  for (const x of [-9, 9]) add(hosp, mesh(new THREE.CylinderGeometry(0.45, 0.45, 9.2, 12), std("#f7f4ee", { roughness: 0.5 })), x, 8.8, -29.8);
  const roof = add(hosp, plane(9, 9, new THREE.MeshStandardMaterial({ map: K.roofH(), emissive: "#ffffff", emissiveMap: K.roofH(), emissiveIntensity: 0.8 })), 0, 41, -35.9);
  P.roofH = roof.material;

  // pastel art-deco blocks along the boulevard (south side faces -z, north side faces +z)
  const r = rng(5);
  const pastels = [["#f2a7b8", "#ffffff"], ["#9fe0d2", "#ffffff"], ["#ffd4a3", "#f7f0e4"], ["#c8b6f0", "#ffffff"], ["#a8d8f0", "#ffffff"], ["#f6e7a6", "#ffffff"], ["#f7b59e", "#fff4ea"]];
  const neons = [["MOTEL", "#ff4fa3"], ["DINER", "#4fe3ff"], ["OPEN", "#ff4f4f"], ["SURF", "#ffd84f"], ["PALMS", "#7dff8a"], ["ICE CREAM", "#ff8ad8"], ["LIQUOR", "#4fa3ff"], ["HOTEL", "#ff9a4f"]];
  P.windowsLit = [];
  const row = (zFront, faceSign, x0, x1, skip) => {
    let x = x0, i = 0;
    while (x < x1) {
      const w = 16 + r() * 10, h = 14 + r() * 22, d = 14 + r() * 6;
      const cx = x + w / 2;
      x += w + 1.5;
      if (skip && cx > skip[0] && cx < skip[1]) continue;
      const [base, trim] = pastels[Math.floor(r() * pastels.length)];
      const floors = Math.max(3, Math.round(h / 6));
      const fT = K.facade({ base, trim, floors, cols: Math.max(3, Math.round(w / 5)), seed: 100 + i, lit: 0.18 });
      const fM = std(0xffffff, { map: fT, roughness: 0.75, emissive: "#ffffff", emissiveMap: fT, emissiveIntensity: 0.0 });
      P.windowsLit.push(fM);
      const sideM = std(base, { roughness: 0.85 });
      const mats = [sideM, sideM, sideM, sideM, faceSign > 0 ? fM : sideM, faceSign < 0 ? fM : sideM];
      add(G, box(w, h, d, mats, 0.05), cx, h / 2, zFront - faceSign * d / 2);
      // deco crown
      add(G, box(w * 0.4, 2.2, d * 0.5, std(trim, { roughness: 0.6 }), 0.2), cx, h + 1.1, zFront - faceSign * d / 2);
      if (i % 2 === 0) {
        const [txt, col] = neons[(i / 2) % neons.length];
        const nt = K.neon(txt, col);
        const ns = add(G, plane(Math.min(w * 0.7, 10), 3.1, new THREE.MeshStandardMaterial({ map: nt, emissive: "#ffffff", emissiveMap: nt, emissiveIntensity: 1.6, transparent: false })), cx, Math.min(h - 3, 11), zFront + faceSign * 0.12);
        ns.rotation.y = faceSign > 0 ? 0 : Math.PI;
        P.neons = P.neons || [];
        P.neons.push(ns.material);
      }
      i++;
    }
  };
  row(12.5, -1, -150, 92);
  row(-12.5, 1, -150, 92, [-62, 62]);

  // palms and lamps along both sidewalks, palms around the plaza
  P.palms = [];
  let s = 0;
  for (let x = -146; x < 92; x += 15) {
    for (const z of [-8.8, 8.8]) {
      if (z < 0 && x > -30 && x < 30) continue;
      P.palms.push(palm(G, x + (z > 0 ? 7 : 0), z, { h: 14 + rng(s)() * 4, lean: 0.1 + rng(s + 7)() * 0.12, dir: z > 0 ? Math.PI : 0, seed: s, cast: Math.abs(x) < 70 }));
      s++;
    }
  }
  for (const [x, z, h] of [[-22, -12.5, 17], [22, -12.5, 17], [-16, -21, 19], [16, -21, 19], [-27, -20, 15], [27, -20, 15]]) P.palms.push(palm(G, x, z, { h, lean: 0.08, dir: x < 0 ? 0.6 : 2.5, seed: s++ }));
  P.lamps = [];
  for (let x = -138; x < 92; x += 30) for (const z of [-7.2, 7.2]) P.lamps.push(streetLamp(G, x, z, z < 0 ? 1 : -1));

  // traffic light at the side street (blinks yellow when the city is empty)
  const tl = new THREE.Group();
  tl.position.set(-38, 0, 7.4);
  G.add(tl);
  const poleM = std("#2a2d33", { roughness: 0.5, metalness: 0.4 });
  add(tl, mesh(new THREE.CylinderGeometry(0.2, 0.25, 11, 8), poleM), 0, 5.5, 0);
  add(tl, box(0.3, 0.3, 7, poleM, 0.05), 0, 10.6, -3.4);
  const head = add(tl, box(1.1, 3.2, 1.0, std("#1f2226"), 0.1), 0, 9.4, -6.2);
  P.tlLamps = ["#ff3b2f", "#ffc21a", "#3bff7a"].map((c, i) => {
    const m = glowM(c, 0);
    const l = add(tl, mesh(new THREE.CircleGeometry(0.36, 16), m, { cast: false }), 0.56, 10.4 - i * 1.0, -6.2);
    l.rotation.y = Math.PI / 2;
    const l2 = add(tl, mesh(new THREE.CircleGeometry(0.36, 16), m, { cast: false }), 0, 10.4 - i * 1.0, -5.68);
    return m;
  });

  // traffic: simple cars in both lanes
  const tColors = ["#5fb3e8", "#f2e0b0", "#e86a6a", "#ffffff", "#7a8ad8", "#f2b84b", "#3a3d44", "#9fe0d2", "#d88ac8"];
  P.traffic = tColors.map((c, i) => {
    const car = makeCar({ color: c, lights: false });
    car.group.scale.setScalar(0.92);
    G.add(car.group);
    const lane = i % 2 ? -3 : 3;
    car.group.position.set(-120 + i * 24 + (i % 3) * 5, 0, lane);
    car.group.rotation.y = lane > 0 ? -Math.PI / 2 : Math.PI / 2;
    car.home = car.group.position.clone();
    return car;
  });

  // the beach at the east end: sand, a lifeguard tower, umbrellas, a low sea wall, the sea
  add(G, box(3, 1.2, 60, std("#f2ece0", { roughness: 0.8 }), 0.1), 95, 0.6, 0);
  const sandM = std(0xffffff, { map: K.sand({ repeat: [6, 30] }), roughness: 0.95 });
  add(G, plane(50, 400, sandM, { receive: true }), 120, 0.02, 0).rotation.x = -Math.PI / 2;
  const seaT = K.sea({ repeat: [30, 40] });
  const seaM = new THREE.MeshStandardMaterial({ map: seaT, roughness: 0.18, metalness: 0.35, color: "#ffffff", emissive: "#3a5f7a", emissiveIntensity: 0.25 });
  const sea = add(G, plane(600, 900, seaM, { receive: false }), 430, -0.3, 0);
  sea.rotation.x = -Math.PI / 2;
  P.sea = seaT;
  // foam line
  add(G, plane(2.4, 400, basic("#fff4e8", 1.0, { transparent: true, opacity: 0.55 })), 131, -0.15, 0).rotation.x = -Math.PI / 2;
  const tower = new THREE.Group();
  tower.position.set(115, 0, -26);
  tower.rotation.y = -Math.PI / 2;
  G.add(tower);
  const wood = std("#f2efe6", { roughness: 0.8 });
  for (const [x, z] of [[-2.2, -2], [2.2, -2], [-2.2, 2], [2.2, 2]]) add(tower, box(0.4, 6, 0.4, wood, 0.05), x, 3, z);
  add(tower, box(5.6, 0.4, 5.6, wood, 0.05), 0, 6.1, 0);
  add(tower, box(5, 3.6, 4.6, std("#ff8fa8", { roughness: 0.7 }), 0.1), 0, 8.1, 0);
  add(tower, box(6.2, 0.4, 6.2, std("#4fc3d9", { roughness: 0.6 }), 0.1), 0, 10.2, 0);
  add(tower, box(2.2, 1.6, 0.1, std("#2a4a5a", { roughness: 0.2 }), 0.02), 0, 8.4, 2.32);
  const ramp = add(tower, box(1.6, 0.25, 8, wood, 0.05), 0, 3, 6.5);
  ramp.rotation.x = 0.75;
  const umbC = [["#ff5f6d", "#ffffff"], ["#4fc3d9", "#ffffff"], ["#ffd84f", "#ff8f3a"], ["#8fe0b4", "#ffffff"], ["#c8a6ff", "#ffffff"]];
  for (let i = 0; i < 7; i++) {
    const ug = new THREE.Group();
    ug.position.set(104 + (i % 3) * 7, 0, -60 + i * 17 + (i % 2) * 4);
    G.add(ug);
    add(ug, mesh(new THREE.CylinderGeometry(0.1, 0.1, 6, 6), std("#efe9de")), 0, 3, 0);
    const [a, b] = umbC[i % umbC.length];
    for (let k = 0; k < 8; k++) {
      const seg = mesh(new THREE.ConeGeometry(3.6, 1.4, 8, 1, true, (k / 8) * Math.PI * 2, Math.PI / 4), std(k % 2 ? a : b, { roughness: 0.7, side: THREE.DoubleSide }));
      seg.position.y = 6.4;
      ug.add(seg);
    }
    const towel = add(G, box(2.4, 0.06, 4.6, std(i % 2 ? "#ff8a5c" : "#5cc8ff", { roughness: 0.9 }), 0.02), ug.position.x + 3, 0.05, ug.position.z + 1);
    towel.rotation.y = 0.2 * (i % 3);
  }

  // sky, the sun, the hospital-ceiling sky that flickers through, the heartbeat line across the sky
  const skyM = new THREE.MeshBasicMaterial({ map: K.sunsetSky(), side: THREE.BackSide, fog: false, depthWrite: false });
  const sky = add(G, new THREE.Mesh(new THREE.SphereGeometry(470, 48, 32), skyM), 0, 0, 0);
  sky.renderOrder = -2;
  P.skyM = skyM;
  const ceilM = new THREE.MeshBasicMaterial({ map: K.ceilingSky(), side: THREE.BackSide, fog: false, transparent: true, opacity: 0, depthWrite: false });
  const ceil = add(G, new THREE.Mesh(new THREE.SphereGeometry(465, 48, 32), ceilM), 0, 0, 0);
  ceil.renderOrder = -1;
  P.ceilM = ceilM;
  const sunM = basic("#ffe2b0", 2.4, { fog: false });
  const sun = add(G, new THREE.Mesh(new THREE.CircleGeometry(24, 48), sunM), ...SUN);
  sun.rotation.y = -Math.PI / 2;
  const halo = add(G, new THREE.Mesh(new THREE.PlaneGeometry(190, 190), new THREE.MeshBasicMaterial({ map: T.softDot("255,170,110"), transparent: true, opacity: 0.85, depthWrite: false, fog: false, blending: THREE.AdditiveBlending })), SUN[0] - 5, SUN[1], SUN[2]);
  halo.rotation.y = -Math.PI / 2;
  P.sun = { disc: sun, sunM, halo };
  P.ecgSky = ecgRibbon(G);
}

// the heartbeat line drawn across the sky: a glowing ribbon (XY plane) that turns to face the camera,
// revealed left to right as the beeps land
function ecgRibbon(G) {
  const N = 360;
  const beat = (x) => {
    const rr = Math.exp(-(((x - 0.28) / 0.02) ** 2)), s = -0.32 * Math.exp(-(((x - 0.315) / 0.018) ** 2));
    const p = 0.12 * Math.exp(-(((x - 0.12) / 0.04) ** 2)), t = 0.22 * Math.exp(-(((x - 0.55) / 0.06) ** 2));
    return p + rr + s + t;
  };
  const pos = [], idx = [];
  const Wd = 150, Hh = 34, th = 0.75;
  for (let i = 0; i <= N; i++) {
    const k = i / N, v = beat((k * 3) % 1);
    const x = -Wd / 2 + k * Wd, y = v * Hh;
    pos.push(x, y + th, 0, x, y - th, 0);
    if (i) {
      const a = (i - 1) * 2;
      idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2);
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  geo.setIndex(idx);
  const m = new THREE.MeshBasicMaterial({ color: "#5dff9a", side: THREE.DoubleSide, fog: false, depthWrite: false });
  m.color.multiplyScalar(2.4);
  const ribbon = new THREE.Mesh(geo, m);
  ribbon.renderOrder = 1;
  ribbon.visible = false;
  G.add(ribbon);
  const total = idx.length;
  return {
    mesh: ribbon,
    mat: m,
    set(k, at = null, look = null) {
      ribbon.visible = k > 0;
      geo.setDrawRange(0, Math.floor((total * Math.min(1, k)) / 6) * 6);
      if (at) ribbon.position.set(at[0], at[1], at[2]);
      if (look) ribbon.lookAt(look[0], look[1], look[2]);
    },
  };
}

// ---------------------------------------------------------------------------------------------
// a blocky car facing +z. interior: seats, dash, wheel, radio, a sun visor that flips down to a photo
export function makeCar({ color = "#8c1424", interior = false, police = false, lights = true, wipers = false } = {}) {
  const group = new THREE.Group();
  const body = new THREE.Group(); // tilts and rolls in the crash
  group.add(body);
  const paint = std(color, { roughness: 0.28, metalness: 0.45 });
  const dark = std("#1a1c20", { roughness: 0.5 });
  const trim = std("#c9ccd2", { roughness: 0.25, metalness: 0.8 });
  add(body, box(9.6, 2.8, 18, paint, 0.5), 0, 2.3, 0);
  add(body, box(9.8, 0.7, 18.4, dark, 0.2), 0, 1.0, 0);
  add(body, box(9.0, 0.5, 1.0, trim, 0.15), 0, 1.9, 9.05);
  add(body, box(9.0, 0.5, 1.0, trim, 0.15), 0, 1.9, -9.05);
  // cabin: roof on six pillars, open side windows, a faint windshield
  const roofM = police ? std("#f2f2f0", { roughness: 0.3, metalness: 0.4 }) : paint;
  add(body, box(8.8, 0.45, 8.8, roofM, 0.15), 0, 7.55, -2.0);
  for (const x of [-4.25, 4.25]) {
    const a = add(body, box(0.42, 4.1, 0.42, roofM, 0.1), x, 5.6, 3.15);
    a.rotation.x = -0.42;
    add(body, box(0.42, 3.9, 0.42, roofM, 0.1), x, 5.6, -5.0);
    const c = add(body, box(0.42, 4.1, 0.42, roofM, 0.1), x, 5.6, -7.0);
    c.rotation.x = 0.42;
  }
  const glass = new THREE.MeshStandardMaterial({ color: "#bcd8e6", transparent: true, opacity: 0.1, roughness: 0.05, metalness: 0.9, depthWrite: false });
  const ws = add(body, plane(8.2, 4.1, glass), 0, 5.65, 3.15);
  ws.rotation.x = -0.42;
  const rw = add(body, plane(8.2, 4.1, glass), 0, 5.65, -7.0);
  rw.rotation.x = 0.42;
  // wheels
  const wheels = [];
  const tireM = std("#141416", { roughness: 0.8 }), hubM = std("#cfd2d8", { roughness: 0.3, metalness: 0.8 });
  for (const [x, z] of [[-4.55, 5.9], [4.55, 5.9], [-4.55, -5.9], [4.55, -5.9]]) {
    const w = new THREE.Group();
    w.position.set(x, 1.35, z);
    body.add(w);
    const t = mesh(new THREE.CylinderGeometry(1.35, 1.35, 1.0, 18), tireM);
    t.rotation.z = Math.PI / 2;
    w.add(t);
    const hb = mesh(new THREE.CylinderGeometry(0.75, 0.75, 1.04, 6), hubM);
    hb.rotation.z = Math.PI / 2;
    w.add(hb);
    wheels.push(w);
  }
  // lamps
  const headM = glowM("#fff4dc", lights ? 2.2 : 0.4), tailM = glowM("#ff2a2a", lights ? 1.6 : 0.4);
  for (const x of [-3.3, 3.3]) {
    add(body, box(2.0, 0.8, 0.2, headM, 0.1), x, 2.85, 9.0);
    add(body, box(1.8, 0.6, 0.2, tailM, 0.1), x, 2.85, -9.0);
  }
  const car = { group, body, wheels, headM, tailM, paint };
  if (police) {
    add(body, box(9.62, 1.4, 7.5, dark, 0.2), 0, 2.4, -0.5); // dark doors
    const red = glowM("#ff2020", 0), blue = glowM("#2a5cff", 0);
    add(body, box(2.8, 0.55, 1.1, red, 0.1), -1.5, 8.05, -1.2);
    add(body, box(2.8, 0.55, 1.1, blue, 0.1), 1.5, 8.05, -1.2);
    car.red = red;
    car.blue = blue;
    car.flash = (t, on = 1) => {
      const ph = (t * 3.2) % 1;
      red.emissiveIntensity = on * (ph < 0.5 ? 5 : 0.2);
      blue.emissiveIntensity = on * (ph >= 0.5 ? 5 : 0.2);
    };
  }
  if (interior) {
    const seatM = std("#2a2420", { roughness: 0.75 });
    for (const x of [-2.3, 2.3]) {
      add(body, box(3.6, 0.8, 3.4, seatM, 0.25), x, 2.6, -2.4);
      const back = add(body, box(3.6, 3.8, 0.7, seatM, 0.25), x, 4.6, -4.1);
      back.rotation.x = 0.16;
      add(body, box(2.0, 1.0, 0.6, seatM, 0.2), x, 6.7, -4.45);
    }
    add(body, box(9.0, 1.5, 2.4, std("#24262b", { roughness: 0.6 }), 0.3), 0, 4.3, 2.75);
    add(body, box(9.0, 0.3, 1.6, std("#1b1c20", { roughness: 0.4 }), 0.1), 0, 5.1, 3.2);
    // steering wheel
    const wheel = new THREE.Group();
    wheel.position.set(2.3, 5.15, -0.15);
    wheel.rotation.x = -0.55;
    body.add(wheel);
    wheel.add(mesh(new THREE.TorusGeometry(1.0, 0.13, 8, 28), std("#141416", { roughness: 0.5 })));
    const spoke = box(1.9, 0.18, 0.12, std("#202226"), 0.05);
    wheel.add(spoke);
    add(body, mesh(new THREE.CylinderGeometry(0.16, 0.2, 2.2, 8), std("#202226")), 2.3, 4.75, 0.75).rotation.x = 1.0;
    car.wheel = wheel;
    // radio in the centre console, screen faces the cabin (-z)
    add(body, box(2.6, 1.3, 0.35, std("#111214", { roughness: 0.4 }), 0.08), 0, 4.55, 1.45);
    const rs = K.makeRadioScreen();
    const screenM = new THREE.MeshStandardMaterial({ map: rs.texture, emissive: "#ffffff", emissiveMap: rs.texture, emissiveIntensity: 1.1, roughness: 0.3 });
    const screen = add(body, plane(2.1, 0.79, screenM), 0, 4.6, 1.26);
    screen.rotation.y = Math.PI;
    for (const x of [-1.05, 1.05]) add(body, mesh(new THREE.CylinderGeometry(0.17, 0.17, 0.22, 14), trim), x, 4.05, 1.22).rotation.x = Math.PI / 2;
    car.radio = { ...rs, screen, screenM };
    // sun visor over the driver: hinge at the windshield top, flips down to show a photo
    const visor = new THREE.Group();
    visor.position.set(2.3, 7.2, 2.2);
    body.add(visor);
    add(visor, box(3.2, 0.14, 1.5, std("#3a3530", { roughness: 0.9 }), 0.05), 0, 0, -0.75);
    const photoM = new THREE.MeshStandardMaterial({ color: "#ffffff", roughness: 0.6 });
    // the photo sits on the side against the roof, so it faces the driver once the visor is down
    const photo = add(visor, plane(1.3, 1.0, photoM), 0.35, 0.085, -0.75);
    photo.rotation.set(-Math.PI / 2, 0, Math.PI);
    const border = add(visor, plane(1.45, 1.15, std("#f4f2ec", { roughness: 0.8 })), 0.35, 0.08, -0.75);
    border.rotation.set(-Math.PI / 2, 0, Math.PI);
    car.visor = visor;
    car.photoM = photoM;
    // rear-view mirror
    add(body, box(1.6, 0.5, 0.2, std("#202226"), 0.08), 0, 6.9, 1.6);
    car.seatDriver = [2.3, 3.5, -2.2];
  }
  if (wipers) {
    car.wipers = [-2.0, 2.4].map((x) => {
      const piv = new THREE.Group();
      piv.position.set(x, 3.9, 3.95);
      piv.rotation.x = -0.42;
      body.add(piv);
      const arm = box(0.12, 3.6, 0.1, std("#141416"), 0.03);
      arm.position.y = 1.8;
      piv.add(arm);
      return piv;
    });
  }
  return car;
}

// ---------------------------------------------------------------------------------------------
function buildICU(G, P) {
  const floorM = std(0xffffff, { map: T.tiles({ color: "#dfe6e4", grout: "#b6c1c0", w: 32, h: 32, repeat: [8, 8] }), roughness: 0.4 });
  add(G, plane(26, 22, floorM, { receive: true }), 0, 0, 0).rotation.x = -Math.PI / 2;
  const ceilT = K.ceilingSky();
  ceilT.repeat.set(4, 3.5);
  add(G, plane(26, 22, std(0xffffff, { map: ceilT, roughness: 0.9 }), { cast: true }), 0, 11, 0).rotation.x = Math.PI / 2;
  const wallM = std("#cfe0d8", { roughness: 0.9 });
  const lowM = std("#a9c7bb", { roughness: 0.8 });
  // back wall (behind the bed), right wall, front wall; left wall has the window
  add(G, box(26, 11, 0.5, wallM, 0.02), 0, 5.5, -10.25);
  add(G, box(0.5, 11, 22, wallM, 0.02), 12.25, 5.5, 0);
  add(G, box(26, 11, 0.5, wallM, 0.02), 0, 5.5, 10.25);
  add(G, box(0.5, 3, 22, wallM, 0.02), -12.25, 1.5, 0);
  add(G, box(0.5, 2, 22, wallM, 0.02), -12.25, 10, 0);
  add(G, box(0.5, 6, 6, wallM, 0.02), -12.25, 6, -8);
  add(G, box(0.5, 6, 6, wallM, 0.02), -12.25, 6, 8);
  add(G, box(0.6, 1.0, 21.6, lowM, 0.02), 11.9, 3.2, 0); // rail band
  // window (x = -12.25, z -5..5, y 3..9): sky outside, blinds
  const outM = basic("#9fc4e8", 1.0);
  const out = add(G, plane(12, 8, outM), -13.5, 6, 0);
  out.rotation.y = Math.PI / 2;
  P.icuOut = outM;
  const blindM = std("#e9ece6", { roughness: 0.7 });
  P.blinds = [];
  for (let i = 0; i < 11; i++) {
    const b = add(G, box(0.12, 0.05, 10, blindM, 0.01), -11.95, 8.7 - i * 0.55, 0);
    b.rotation.z = 0.6;
    P.blinds.push(b);
  }
  // the bed: frame, mattress, raised head, pillow, blanket, rails
  const bed = new THREE.Group();
  bed.position.set(0, 0, -2);
  G.add(bed);
  const frameM = std("#d9dde0", { roughness: 0.35, metalness: 0.5 });
  add(bed, box(7.2, 0.5, 14, frameM, 0.08), 0, 2.3, 0);
  for (const [x, z] of [[-3.3, -6.6], [3.3, -6.6], [-3.3, 6.6], [3.3, 6.6]]) add(bed, box(0.3, 2.2, 0.3, frameM, 0.05), x, 1.1, z);
  add(bed, box(6.8, 0.9, 13.6, std("#f6f7f8", { roughness: 0.9 }), 0.25), 0, 3.0, 0);
  const head = add(bed, box(7.2, 4.4, 0.4, frameM, 0.1), 0, 4.2, -7.0);
  add(bed, box(7.2, 2.4, 0.4, frameM, 0.1), 0, 3.2, 7.0);
  P.pillow = add(bed, box(4.4, 1.0, 2.4, std("#ffffff", { roughness: 0.95 }), 0.4), 0, 3.9, -5.4);
  P.pillow.rotation.x = 0.35;
  P.icuBlanket = add(bed, box(7.0, 0.7, 8.4, std("#8fb4d8", { roughness: 0.95 }), 0.3), 0, 3.95, 2.6);
  for (const x of [-3.7, 3.7]) add(bed, box(0.2, 1.2, 6, frameM, 0.05), x, 4.0, 1.0);
  P.bed = bed;
  // heart monitor on an arm at the head of the bed (right side), screen faces the room
  const mon = new THREE.Group();
  mon.position.set(6.2, 8.2, -8.4);
  mon.rotation.y = -0.45;
  G.add(mon);
  add(mon, box(4.6, 3.2, 0.6, std("#e6e8ea", { roughness: 0.4 }), 0.15), 0, 0, 0);
  const monT = K.makeMonitor();
  const monM = new THREE.MeshStandardMaterial({ map: monT.texture, emissive: "#ffffff", emissiveMap: monT.texture, emissiveIntensity: 1.25 });
  add(mon, plane(4.0, 2.5, monM), 0, 0.05, 0.31);
  add(G, box(0.3, 0.3, 2.2, frameM, 0.05), 6.6, 8.2, -9.5);
  P.monitor = { group: mon, set: monT.set, mat: monM };
  // IV stand
  const iv = new THREE.Group();
  iv.position.set(-5.4, 0, -5.5);
  G.add(iv);
  add(iv, mesh(new THREE.CylinderGeometry(0.08, 0.08, 9, 8), frameM), 0, 4.5, 0);
  add(iv, box(1.6, 0.1, 0.1, frameM, 0.02), 0, 9, 0);
  add(iv, box(0.9, 1.3, 0.35, new THREE.MeshStandardMaterial({ color: "#e8f4ff", transparent: true, opacity: 0.7, roughness: 0.1 }), 0.15), 0.5, 8.1, 0);
  // Lily's chair beside the bed (right side)
  const chair = new THREE.Group();
  chair.position.set(-6.4, 0, 1.0);
  chair.rotation.y = Math.PI / 2;
  G.add(chair);
  const vinyl = std("#3f8f8a", { roughness: 0.45 });
  add(chair, box(4.2, 1.0, 3.6, vinyl, 0.3), 0, 2.2, 0);
  add(chair, box(4.2, 3.8, 0.8, vinyl, 0.3), 0, 3.9, -1.6);
  for (const x of [-2.2, 2.2]) add(chair, box(0.6, 1.4, 3.6, vinyl, 0.25), x, 3.0, 0);
  for (const [x, z] of [[-1.8, -1.4], [1.8, -1.4], [-1.8, 1.4], [1.8, 1.4]]) add(chair, box(0.2, 1.7, 0.2, frameM, 0.04), x, 0.85, z);
  P.chair = chair;
  // the drawing taped above the bed, a small table with a cup and flowers
  const dr = add(G, plane(4.4, 3.3, std(0xffffff, { map: K.crayonDrawing(), roughness: 0.9 })), -0.4, 8.6, -9.98);
  P.drawing = dr;
  for (const [x, y] of [[-2.4, 10.1], [1.6, 10.1]]) add(G, plane(0.7, 0.3, std("#f2e6a8", { roughness: 0.9 })), x, y, -9.97).rotation.z = 0.3;
  const table = add(G, box(2.6, 0.3, 2.2, std("#d9dde0", { roughness: 0.4 }), 0.05), 6.0, 4.0, 4.2);
  add(G, box(0.2, 4.0, 0.2, frameM, 0.04), 6.0, 2.0, 4.2);
  add(G, mesh(new THREE.CylinderGeometry(0.35, 0.3, 0.9, 12), std("#7fb2e0", { roughness: 0.2 })), 5.7, 4.6, 4.0);
  for (let i = 0; i < 5; i++) add(G, mesh(new THREE.SphereGeometry(0.28, 8, 6), std(["#ff7a9a", "#ffd84f", "#ff9a4f", "#ffffff", "#c8a6ff"][i])), 5.7 + Math.cos(i * 1.3) * 0.35, 5.35 + (i % 2) * 0.2, 4.0 + Math.sin(i * 1.3) * 0.35);
  // ceiling light panel
  const lp = add(G, plane(4, 2, basic("#f4fbff", 1.3)), 0, 10.98, 2);
  lp.rotation.x = Math.PI / 2;
  P.icuPanel = lp.material;
}

// ---------------------------------------------------------------------------------------------
function buildRain(G, P) {
  add(G, plane(400, 400, std("#3a3d42", { roughness: 0.95 })), 0, -0.02, 0).rotation.x = -Math.PI / 2;
  const rt = K.road({ seed: 12 });
  rt.repeat.set(1, 18);
  const wet = std(0xffffff, { map: rt, roughness: 0.22, metalness: 0.35, color: "#8a8f99" });
  add(G, plane(12, 320, wet, { receive: true }), 0, 0.01, 0).rotation.x = -Math.PI / 2;
  const walkM = std("#6d7076", { map: T.concrete({ repeat: [1, 60] }), roughness: 0.6 });
  for (const x of [-8.2, 8.2]) add(G, box(4.4, 0.32, 320, walkM, 0.02), x, 0.16, 0);
  const r = rng(41);
  for (const side of [-1, 1]) {
    let z = -150;
    while (z < 150) {
      const w = 14 + r() * 10, h = 12 + r() * 20, d = 14;
      const g = 0.32 + r() * 0.12;
      const c = new THREE.Color(g, g * 1.02, g * 1.06);
      add(G, box(d, h, w, std(c, { roughness: 0.9 }), 0.05), side * (12 + d / 2), h / 2, z + w / 2);
      for (let f = 0; f < h / 5 - 1; f++) for (let k = 0; k < w / 5; k++) if (r() < 0.35) add(G, plane(1.8, 2.0, basic(r() < 0.5 ? "#ffd9a0" : "#9fb8d0", 0.7)), side * 11.98, 4 + f * 5, z + 2.5 + k * 5).rotation.y = side > 0 ? -Math.PI / 2 : Math.PI / 2;
      z += w + 1;
    }
  }
  // school zone sign on the right of the lane, a second further on
  for (const z of [30, 90]) {
    const pole = add(G, mesh(new THREE.CylinderGeometry(0.12, 0.12, 7, 8), std("#8a8d92", { metalness: 0.5, roughness: 0.4 })), -7.2, 3.5, z);
    const sg = add(G, plane(3.2, 3.2, std(0xffffff, { map: K.schoolSign(), transparent: true, alphaTest: 0.3, roughness: 0.5, emissive: "#c8e02a", emissiveIntensity: 0.15 })), -7.2, 7.4, z - 0.15);
    sg.rotation.y = Math.PI;
  }
  // SCHOOL painted on the road
  const st = document.createElement("canvas");
  st.width = 512;
  st.height = 128;
  const sg2 = st.getContext("2d");
  sg2.fillStyle = "rgba(0,0,0,0)";
  sg2.fillRect(0, 0, 512, 128);
  sg2.fillStyle = "#e8e6df";
  sg2.font = "800 104px Poppins, sans-serif";
  sg2.textAlign = "center";
  sg2.textBaseline = "middle";
  sg2.fillText("SCHOOL", 256, 70);
  const stT = new THREE.CanvasTexture(st);
  stT.colorSpace = THREE.SRGBColorSpace;
  const word = add(G, plane(5.0, 1.25, new THREE.MeshStandardMaterial({ map: stT, transparent: true, roughness: 0.4 })), -2.9, 0.03, 60);
  word.rotation.set(-Math.PI / 2, 0, Math.PI);
  // street lamps, on in the gloom
  for (let z = -140; z < 150; z += 28) {
    const l = streetLamp(G, 7.4, z, -1);
    l.bulb.emissiveIntensity = 2.5;
  }
  // overcast sky
  const skyT = T.skyGradient([[0, "#4a5260"], [0.45, "#7a828e"], [0.52, "#8a909a"], [1, "#3a3d44"]]);
  const sky = add(G, new THREE.Mesh(new THREE.SphereGeometry(330, 32, 20), new THREE.MeshBasicMaterial({ map: skyT, side: THREE.BackSide, fog: false })), 0, 0, 0);
  sky.renderOrder = -2;
  // rain: instanced streaks; shots move them by time (seek-safe)
  const N = 900;
  const rm = new THREE.MeshBasicMaterial({ map: K.streak(), transparent: true, opacity: 0.55, depthWrite: false, fog: false });
  const rain = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.06, 1.6), rm, N);
  rain.frustumCulled = false;
  const seeds = [];
  for (let i = 0; i < N; i++) seeds.push([r() * 40 - 20, r() * 26, r() * 60 - 10, r()]);
  G.add(rain);
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), sc = new THREE.Vector3(1, 1, 1), v = new THREE.Vector3();
  P.rain = {
    mesh: rain,
    // centre the rain box on a point (set-local) and advance by time
    at(cx, cz, t, yaw = 0) {
      q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), yaw);
      seeds.forEach(([x, y, z, k], i) => {
        const yy = ((y - t * (38 + k * 10)) % 26 + 26) % 26;
        v.set(cx + x, yy, cz + z);
        m4.compose(v, q, sc);
        rain.setMatrixAt(i, m4);
      });
      rain.instanceMatrix.needsUpdate = true;
    },
  };
  // the box truck that crosses into the lane
  const truck = new THREE.Group();
  G.add(truck);
  add(truck, box(10, 11, 22, std("#d8d8d2", { roughness: 0.7 }), 0.2), 0, 7, -3);
  add(truck, box(9.6, 7, 7, std("#3d5f8a", { roughness: 0.4, metalness: 0.3 }), 0.4), 0, 4.6, 11.5);
  add(truck, box(8.6, 3, 0.2, std("#1a2430", { roughness: 0.1, metalness: 0.6 }), 0.05), 0, 6.4, 15.05);
  const hl = glowM("#fffaf0", 6);
  for (const x of [-3.4, 3.4]) add(truck, box(1.8, 1.0, 0.2, hl, 0.1), x, 2.6, 15.1);
  for (const [x, z] of [[-4.6, 11], [4.6, 11], [-4.6, -8], [4.6, -8], [-4.6, -2], [4.6, -2]]) add(truck, mesh(new THREE.CylinderGeometry(1.5, 1.5, 1.0, 16), std("#141416")), x, 1.5, z).rotation.z = Math.PI / 2;
  const flare = add(truck, new THREE.Mesh(new THREE.PlaneGeometry(14, 7), new THREE.MeshBasicMaterial({ map: T.softDot("255,250,235"), transparent: true, opacity: 0.9, depthWrite: false, fog: false, blending: THREE.AdditiveBlending })), 0, 2.8, 15.6);
  P.truck = { group: truck, hl, flare };
}

// a sunny little backyard for the photo on the sun visor (rendered once at boot)
function buildPhoto(G, P) {
  add(G, plane(60, 40, std("#5fae5a", { map: T.grass({ repeat: [8, 8] }), roughness: 0.95 })), 0, 0, 0).rotation.x = -Math.PI / 2;
  const bg = add(G, plane(60, 30, basic("#9fd4f2", 1)), 0, 15, -8);
  add(G, box(30, 3, 0.6, std("#f2efe6", { roughness: 0.8 }), 0.05), 0, 1.5, -6);
  for (let i = -6; i <= 6; i++) add(G, box(0.5, 4, 0.5, std("#f2efe6"), 0.05), i * 2.2, 2, -5.8);
  P.photoBg = bg;
}

function buildLights(scene, W) {
  const hemi = new THREE.HemisphereLight("#ffb48a", "#5a3a5a", 1.5);
  scene.add(hemi);
  const key = new THREE.DirectionalLight("#ffb070", 4);
  key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  key.shadow.bias = -0.0004;
  key.shadow.normalBias = 0.04;
  const sc = key.shadow.camera;
  sc.left = -40;
  sc.right = 40;
  sc.top = 40;
  sc.bottom = -40;
  sc.near = 1;
  sc.far = 400;
  scene.add(key);
  scene.add(key.target);
  const prac = new THREE.SpotLight("#ffb46a", 0, 0, 1.0, 0.8, 2);
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
