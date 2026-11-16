// Sets for the long-form film: 657 Boulevard and its street (Westfield, NJ), a letter desk,
// 284 Green Street (Enfield, 1977: outside, the girls' bedroom, the living room), a globe, and
// side-by-side models of both houses for the outro. Each set is one group, shown only when used.
import * as THREE from "three";
import * as T from "./textures.js";
import { box, mesh, std } from "./chars.js";
import { rng } from "./util.js";

export const WX = -260; // Westfield street origin: 657's front facade at local z = 0
export const DESK = [-150, 0, -140]; // letter desk origin
export const EX = -460; // Enfield exterior origin: facade at local z = 0
export const EB = [EX - 70, 0, 0]; // Enfield bedroom origin (room centre on the floor)
export const EL = [EX - 110, 0, 0]; // Enfield living room origin
export const GLOBE = [0, 320, 0]; // globe centre
export const DIO = [0, -300, 0]; // diorama table origin

const glowM = (color, k = 1) => {
  const m = new THREE.MeshBasicMaterial({ color });
  m.color.multiplyScalar(k);
  return m;
};
function cnv(w, h) {
  const c = document.createElement("canvas");
  c.width = w;
  c.height = h;
  return [c, c.getContext("2d")];
}
function ctex(c) {
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
}
const add = (parent, m, x, y, z) => {
  m.position.set(x, y, z);
  parent.add(m);
  return m;
};
function sky(parent, stops, o = {}) {
  const m = new THREE.MeshBasicMaterial({ map: T.skyGradient(stops, o), side: THREE.BackSide, depthWrite: false, fog: false });
  const s = new THREE.Mesh(new THREE.SphereGeometry(190, 32, 16), m);
  parent.add(s);
  return s;
}
// a window: glass plane (lit or dark), white trim, optional shutters; returns the glass material
function windowAt(parent, x, y, z, w, h, { shutters = true, trim = "#f2efe8", ry = 0, glass = null } = {}) {
  const g = new THREE.Group();
  g.position.set(x, y, z);
  g.rotation.y = ry;
  parent.add(g);
  const gm = glass || new THREE.MeshStandardMaterial({ color: "#0d1118", roughness: 0.15, metalness: 0.2, emissive: "#ffcf8a", emissiveIntensity: 0 });
  add(g, mesh(new THREE.PlaneGeometry(w, h), gm, { cast: false }), 0, 0, 0.02);
  const tm = std(trim, { roughness: 0.5 });
  for (const [bw, bh, bx, by] of [[w + 0.5, 0.3, 0, h / 2 + 0.1], [w + 0.7, 0.35, 0, -h / 2 - 0.12], [0.28, h, -w / 2 - 0.1, 0], [0.28, h, w / 2 + 0.1, 0], [0.12, h, 0, 0], [w, 0.12, 0, 0]]) add(g, box(bw, bh, 0.3, tm, 0.03), bx, by, 0.1);
  if (shutters) {
    const sm = std("#1f2a2a", { roughness: 0.7 });
    for (const s of [-1, 1]) add(g, box(w * 0.42, h + 0.2, 0.15, sm, 0.03), s * (w / 2 + w * 0.26), 0, 0.05);
  }
  return gm;
}
function tree(parent, x, z, s = 1, seed = 1) {
  const r = rng(seed);
  const t = new THREE.Group();
  t.position.set(x, 0, z);
  parent.add(t);
  add(t, box(1.4 * s, 9 * s, 1.4 * s, std("#4a3626", { roughness: 0.9 }), 0.2), 0, 4.5 * s, 0);
  const leaf = std("#35562f", { roughness: 0.95 });
  for (let i = 0; i < 6; i++) add(t, mesh(new THREE.SphereGeometry((3.2 + r() * 1.6) * s, 10, 8), leaf), (r() - 0.5) * 5 * s, (10 + r() * 4) * s, (r() - 0.5) * 5 * s);
  return t;
}
function signTex(lines, { bg = "#c8241f", fg = "#ffffff", w = 512, h = 320, font = 84 } = {}) {
  const [c, g] = cnv(w, h);
  g.fillStyle = bg;
  g.fillRect(0, 0, w, h);
  g.strokeStyle = fg;
  g.lineWidth = 10;
  g.strokeRect(14, 14, w - 28, h - 28);
  g.fillStyle = fg;
  g.textAlign = "center";
  g.textBaseline = "middle";
  lines.forEach((l, i) => {
    g.font = `800 ${i ? font * 0.5 : font}px Poppins, sans-serif`;
    g.fillText(l, w / 2, h / 2 + (i - (lines.length - 1) / 2) * font * 0.95);
  });
  return ctex(c);
}

// ======================================================================================
export function buildSets(scene, P) {
  P.sets = P.sets || {};
  P.sets.watcher = buildWatcher(scene, P);
  P.sets.desk = buildDesk(scene, P);
  P.sets.enfOut = buildEnfieldOutside(scene, P);
  P.sets.enfBed = buildEnfieldBedroom(scene, P);
  P.sets.enfLive = buildEnfieldLiving(scene, P);
  P.sets.globe = buildGlobe(scene, P);
  P.sets.dio = buildDiorama(scene, P);
  if (P.sets.house) buildReno(P.sets.house, P);
  buildProps(scene, P);
}

// ---- 657 Boulevard -------------------------------------------------------------------
function buildWatcher(scene, P) {
  const G = new THREE.Group();
  G.position.set(WX, 0, 0);
  scene.add(G);
  const W = (P.wb = { win: [], far: [] });
  W.skyDay = sky(G, [[0, "#5d8fd6"], [0.55, "#9cc3ee"], [1, "#e8f1fb"]]);
  W.skyDusk = sky(G, [[0, "#1c2550"], [0.5, "#6b4f8a"], [0.8, "#e0866a"], [1, "#f6c58a"]]);
  W.skyNight = sky(G, [[0, "#04060f"], [0.6, "#0d1530"], [1, "#1b2650"]], { stars: 160, moon: [190, 120, 10] });
  const lawn = mesh(new THREE.PlaneGeometry(200, 140), std(0xffffff, { map: T.grass({ repeat: [16, 12] }), roughness: 1, color: "#5d7a4f" }), { cast: false });
  lawn.rotation.x = -Math.PI / 2;
  add(G, lawn, 0, 0, 20);
  const asph = mesh(new THREE.PlaneGeometry(200, 13), std(0xffffff, { map: T.asphalt({ repeat: [20, 2] }), roughness: 0.9 }), { cast: false });
  asph.rotation.x = -Math.PI / 2;
  add(G, asph, 0, 0.02, 36.5);
  const conc = std(0xffffff, { map: T.concrete({ repeat: [24, 1] }), roughness: 0.85 });
  for (const z of [27.5, 45.5]) {
    const sw = mesh(new THREE.PlaneGeometry(200, 3), conc, { cast: false });
    sw.rotation.x = -Math.PI / 2;
    add(G, sw, 0, 0.03, z);
    add(G, box(200, 0.35, 0.4, std("#b9b4aa"), 0.02), 0, 0.17, z + (z < 36 ? 1.7 : -1.7));
  }
  const path = mesh(new THREE.PlaneGeometry(3.4, 26), conc, { cast: false });
  path.rotation.x = -Math.PI / 2;
  add(G, path, 0, 0.03, 13);
  const drive = mesh(new THREE.PlaneGeometry(8, 30), std(0xffffff, { map: T.asphalt({ repeat: [1, 4] }), roughness: 0.9, color: "#9a9a9a" }), { cast: false });
  drive.rotation.x = -Math.PI / 2;
  add(G, drive, 21, 0.025, 11);

  // the house: two full storeys of white siding, a steep roof with three dormers, black shutters
  const H = new THREE.Group();
  G.add(H);
  W.house = H;
  const sideM = std(0xffffff, { map: T.siding({ color: [40, 10, 86], repeat: [5, 3] }), roughness: 0.8 });
  add(H, box(28, 18, 16, sideM, 0.05), 0, 9, -8);
  add(H, box(28.6, 0.5, 16.6, std("#e9e4da"), 0.05), 0, 9, -8); // floor band
  add(H, box(28.8, 0.8, 16.8, std("#e9e4da"), 0.05), 0, 18.2, -8);
  const roofM = std("#2c2f36", { roughness: 0.75 });
  for (const s of [-1, 1]) {
    const r = add(H, box(30, 0.7, 11.2, roofM, 0.05), 0, 22.2, -8 + s * 4.1);
    r.rotation.x = s * 0.82;
  }
  for (const s of [-1, 1]) add(H, box(0.6, 8.2, 16, sideM, 0.02), s * 14, 21.8, -8);
  for (const x of [-8, 0, 8]) {
    add(H, box(3.6, 4.0, 3.6, sideM, 0.05), x, 21.6, -1.4);
    const dr = add(H, box(4.2, 0.4, 4.4, roofM, 0.05), x, 23.8, -1.3);
    dr.rotation.x = 0.25;
    W.win.push(windowAt(H, x, 21.4, 0.45, 1.7, 2.4, { shutters: false }));
  }
  for (const x of [-10, -5.2, 5.2, 10]) W.win.push(windowAt(H, x, 4.6, 0.02, 2.5, 4.0));
  for (const x of [-10, -5, 0, 5, 10]) W.win.push(windowAt(H, x, 13.4, 0.02, 2.5, 3.8));
  // front door, porch roof on columns, steps, lanterns
  const doorM = std(0xffffff, { map: T.panelDoor({ color: "#1f3a33" }), roughness: 0.55 });
  add(H, box(3.2, 7.2, 0.3, doorM, 0.04), 0, 3.6, 0.1);
  add(H, box(4.2, 0.5, 0.5, std("#f2efe8"), 0.04), 0, 7.6, 0.2);
  const col = std("#f2efe8", { roughness: 0.5 });
  for (const x of [-3.8, 3.8]) add(H, mesh(new THREE.CylinderGeometry(0.35, 0.4, 8.2, 14), col), x, 4.1, 4.4);
  add(H, box(9.2, 0.6, 5.4, col, 0.05), 0, 8.4, 2.4);
  add(H, box(9.6, 0.25, 5.8, roofM, 0.04), 0, 8.85, 2.4);
  for (let i = 0; i < 3; i++) add(H, box(7 - i * 0.6, 0.4, 1.4, std("#c9c2b6"), 0.02), 0, 0.2 + i * 0.4, 6.6 - i * 1.3 - 0.4);
  add(H, box(8, 0.5, 5, std("#c9c2b6"), 0.02), 0, 1.2, 2.5);
  const lantM = new THREE.MeshStandardMaterial({ color: "#111", emissive: "#ffcf8a", emissiveIntensity: 0 });
  for (const x of [-2.2, 2.2]) add(H, box(0.45, 0.7, 0.35, lantM, 0.06), x, 5.2, 0.4);
  W.lantern = lantM;
  W.number = add(H, mesh(new THREE.PlaneGeometry(1.6, 0.6), new THREE.MeshStandardMaterial({ map: signTex(["657"], { bg: "#1b1b1b", fg: "#e9d9a8", w: 256, h: 96, font: 70 }), roughness: 0.5 }), { cast: false }), 0, 7.95, 0.47);
  for (const x of [-11, -6.5, 6.5, 11]) add(H, box(3.4, 1.6, 2, std("#2c4a2a", { roughness: 0.95 }), 0.5), x, 0.8, 1.4);
  // the mailbox at the curb: post, box, a door that opens toward the house, red flag
  const mb = new THREE.Group();
  mb.position.set(5.5, 0, 25.6);
  G.add(mb);
  add(mb, box(0.35, 3.6, 0.35, std("#3a2a1e"), 0.04), 0, 1.8, 0);
  const mbM = std("#16181c", { roughness: 0.4, metalness: 0.4 });
  add(mb, box(1.2, 1.1, 2.0, mbM, 0.3), 0, 4.0, 0);
  const mdoor = new THREE.Group();
  mdoor.position.set(0, 3.45, -1.0);
  mb.add(mdoor);
  add(mdoor, box(1.2, 1.1, 0.08, mbM, 0.1), 0, 0.55, 0);
  const flag = new THREE.Group();
  flag.position.set(0.66, 4.0, 0.3);
  mb.add(flag);
  add(flag, box(0.06, 0.9, 0.25, std("#c8241f"), 0.02), 0, 0.45, 0);
  W.mailbox = { group: mb, door: mdoor, flag, pos: [WX + 5.5, 4.0, 25.6] };
  W.mailEnv = add(mb, box(0.9, 0.05, 1.5, std("#efe6d2", { roughness: 0.8 }), 0.01), 0, 3.6, -0.2);
  // a car in the driveway
  const car = new THREE.Group();
  car.position.set(21, 0, 9);
  G.add(car);
  const cm = std("#3b4a5e", { roughness: 0.35, metalness: 0.4 });
  add(car, box(5.6, 2.4, 11, cm, 0.5), 0, 2.0, 0);
  add(car, box(5.2, 2.0, 6.5, std("#141820", { roughness: 0.2, metalness: 0.5 }), 0.4), 0, 4.1, -0.8);
  for (const [x, z] of [[-2.6, 3.6], [2.6, 3.6], [-2.6, -3.6], [2.6, -3.6]]) {
    const wh = add(car, mesh(new THREE.CylinderGeometry(1.0, 1.0, 0.8, 16), std("#111")), x, 1.0, z);
    wh.rotation.z = Math.PI / 2;
  }
  // trees, a streetlight pair
  [[-22, 8, 1.2], [21, -6, 1.1], [-30, 28.5, 1.0], [30, 28.5, 1.0], [-62, 44, 1.1], [58, 46, 1.0]].forEach(([x, z, s], i) => tree(G, x, z, s, i + 3));
  W.lamps = [];
  for (const x of [-18, 34]) {
    add(G, box(0.35, 13, 0.35, std("#2a2c30"), 0.05), x, 6.5, 29.6);
    add(G, box(0.3, 0.3, 2.4, std("#2a2c30"), 0.05), x, 13, 30.6);
    const lm = glowM("#ffd9a0", 0.2);
    add(G, box(1.0, 0.4, 0.8, lm, 0.1), x, 12.7, 31.6);
    W.lamps.push({ m: lm, pos: [WX + x, 12.4, 31.6] });
  }
  // for-sale sign on the lawn
  const sale = new THREE.Group();
  sale.position.set(-9, 0, 20);
  G.add(sale);
  add(sale, box(0.25, 5.5, 0.25, std("#f2efe8"), 0.03), -1.6, 2.75, 0);
  add(sale, box(3.8, 0.22, 0.22, std("#f2efe8"), 0.03), 0, 5.4, 0);
  W.saleTex = { sale: signTex(["FOR SALE"]), sold: signTex(["SOLD"], { bg: "#1f5fa8" }) };
  W.saleM = new THREE.MeshStandardMaterial({ map: W.saleTex.sale, roughness: 0.6 });
  add(sale, mesh(new THREE.PlaneGeometry(3.2, 2.0), W.saleM, { cast: true }), 0, 4.1, 0.05);
  W.sale = sale;
  // houses across the street (facing the house) and next door: rows of windows
  const farSide = [[-46, 64, [12, 30, 75]], [0, 66, [0, 0, 72]], [46, 64, [210, 18, 70]], [-62, 2, [25, 25, 78]], [62, 0, [200, 12, 76]]];
  farSide.forEach(([x, z, colr], i) => {
    const across = z > 30;
    const hg = new THREE.Group();
    hg.position.set(x, 0, z);
    hg.rotation.y = across ? Math.PI : 0;
    G.add(hg);
    const hm = std(0xffffff, { map: T.siding({ color: colr, repeat: [4, 3], seed: 20 + i }), roughness: 0.8 });
    add(hg, box(24, 16, 14, hm, 0.05), 0, 8, -7);
    for (const s of [-1, 1]) {
      const r = add(hg, box(26, 0.6, 9.6, roofM, 0.05), 0, 19, -7 + s * 3.5);
      r.rotation.x = s * 0.75;
    }
    for (const s of [-1, 1]) add(hg, box(0.5, 6.5, 14, hm, 0.02), s * 12, 18.4, -7);
    for (const wx of [-8, -3, 3, 8]) for (const wy of [4.2, 12]) {
      const gm = windowAt(hg, wx, wy, 0.02, 2.2, 3.4, { shutters: false });
      W.far.push(gm);
    }
    add(hg, box(3, 6.6, 0.3, std(0xffffff, { map: T.panelDoor({ color: ["#7a2a2a", "#2b3f5c", "#3a5a3a"][i % 3] }) }), 0.04), 0, 3.3, 0.1);
  });
  // the one window that is watching back (only lit in the shot that wants it)
  const silM = new THREE.MeshBasicMaterial({ color: "#000", transparent: true, opacity: 0 });
  const [sc, sg] = cnv(128, 192);
  sg.fillStyle = "#000";
  sg.beginPath();
  sg.ellipse(64, 70, 28, 34, 0, 0, Math.PI * 2);
  sg.fill();
  sg.beginPath();
  sg.moveTo(8, 192);
  sg.quadraticCurveTo(10, 116, 64, 112);
  sg.quadraticCurveTo(118, 116, 120, 192);
  sg.fill();
  silM.map = ctex(sc);
  silM.alphaTest = 0.4;
  const sil = mesh(new THREE.PlaneGeometry(1.7, 2.6), silM, { cast: false });
  sil.rotation.y = Math.PI;
  add(G, sil, 46 - 3, 11.8, 63.86);
  W.sil = sil;
  W.silWin = W.far[2 * 8 + 5]; // house 2 (x 46), window at local (3, 12) -> world x 43
  return G;
}

// ---- the letter desk ---------------------------------------------------------------
function buildDesk(scene, P) {
  const G = new THREE.Group();
  G.position.set(...DESK);
  scene.add(G);
  const wood = std(0xffffff, { map: T.woodFloor({ repeat: [1.4, 0.8], base: [24, 40, 28] }), roughness: 0.55 });
  add(G, box(14, 0.5, 8, wood, 0.05), 0, 3.0, 0);
  add(G, box(30, 14, 0.4, std(0xffffff, { map: T.wallpaper({ color: [32, 18, 22], repeat: [3, 2] }), roughness: 0.9 }), 0.02), 0, 7, -6);
  const fl = mesh(new THREE.PlaneGeometry(40, 30), std("#2a1f18", { roughness: 0.9 }), { cast: false });
  fl.rotation.x = -Math.PI / 2;
  G.add(fl);
  // the letter: typed text drawn progressively (n characters) on aged paper
  const [c, g] = cnv(768, 1024);
  const lt = ctex(c);
  const letterM = new THREE.MeshStandardMaterial({ map: lt, roughness: 0.85 });
  const letter = add(G, mesh(new THREE.PlaneGeometry(3.0, 4.0), letterM, { cast: false }), 0.4, 3.27, 0.2);
  letter.rotation.x = -Math.PI / 2;
  letter.rotation.z = 0.06;
  let lastKey = "";
  const drawLetter = (lines, n = 9999, { sign = false } = {}) => {
    const key = lines.join("|") + n + sign;
    if (key === lastKey) return;
    lastKey = key;
    g.fillStyle = "#efe6d2";
    g.fillRect(0, 0, 768, 1024);
    const gr = g.createRadialGradient(384, 512, 200, 384, 512, 700);
    gr.addColorStop(0, "rgba(0,0,0,0)");
    gr.addColorStop(1, "rgba(90,60,20,0.22)");
    g.fillStyle = gr;
    g.fillRect(0, 0, 768, 1024);
    g.strokeStyle = "rgba(120,90,50,0.25)";
    g.lineWidth = 2;
    g.beginPath();
    g.moveTo(0, 340);
    g.lineTo(768, 346);
    g.moveTo(0, 690);
    g.lineTo(768, 684);
    g.stroke();
    g.fillStyle = "#1c1a18";
    g.font = "700 40px 'Liberation Mono', 'DejaVu Sans Mono', monospace";
    g.textBaseline = "top";
    let left = n, y = 90;
    for (const line of lines) {
      if (left <= 0) break;
      const words = line.split(" ");
      let cur = "";
      const rows = [];
      for (const w of words) {
        const t = cur ? cur + " " + w : w;
        if (g.measureText(t).width > 640 && cur) {
          rows.push(cur);
          cur = w;
        } else cur = t;
      }
      rows.push(cur);
      for (const row of rows) {
        if (left <= 0) break;
        g.fillText(row.slice(0, left), 64, y);
        left -= row.length + 1;
        y += 54;
      }
      y += 34;
    }
    if (sign) {
      g.font = "700 46px 'Liberation Mono', 'DejaVu Sans Mono', monospace";
      g.fillText("- The Watcher", 330, 880);
    }
    lt.needsUpdate = true;
  };
  drawLetter([""], 0);
  // the envelope, addressed by hand
  const [ec, eg] = cnv(768, 448);
  eg.fillStyle = "#f3ecdc";
  eg.fillRect(0, 0, 768, 448);
  eg.fillStyle = "#cfc4ad";
  eg.fillRect(600, 30, 130, 150);
  eg.fillStyle = "#23201c";
  eg.font = "italic 700 64px 'DejaVu Serif', serif";
  eg.textAlign = "center";
  eg.fillText("The New Owner", 384, 250);
  eg.font = "italic 400 40px 'DejaVu Serif', serif";
  eg.fillText("657 Boulevard", 384, 320);
  const env = add(G, mesh(new THREE.PlaneGeometry(3.4, 2.0), new THREE.MeshStandardMaterial({ map: ctex(ec), roughness: 0.85 }), { cast: false }), -3.2, 3.28, 1.2);
  env.rotation.x = -Math.PI / 2;
  env.rotation.z = -0.18;
  // a desk lamp
  const lamp = new THREE.Group();
  lamp.position.set(5.2, 3.25, -2.6);
  G.add(lamp);
  add(lamp, mesh(new THREE.CylinderGeometry(0.6, 0.7, 0.2, 18), std("#222"), { cast: false }), 0, 0.1, 0);
  const arm = add(lamp, mesh(new THREE.BoxGeometry(0.15, 3, 0.15), std("#222"), { cast: false }), 0, 1.5, 0);
  arm.rotation.z = 0.2;
  const shade = add(lamp, mesh(new THREE.ConeGeometry(0.9, 1.0, 18, 1, true), new THREE.MeshStandardMaterial({ color: "#2a4a3a", side: THREE.DoubleSide, emissive: "#ffcf8a", emissiveIntensity: 0.5 }), { cast: false }), -0.4, 3.0, 0.3);
  shade.rotation.z = 0.6;
  P.desk = { letter, drawLetter, env, lampPos: [DESK[0] + 4.6, DESK[1] + 6.2, DESK[2] - 2.0], top: [DESK[0], DESK[1] + 3.25, DESK[2]] };
  return G;
}

// ---- 284 Green Street, outside ---------------------------------------------------------
function buildEnfieldOutside(scene, P) {
  const G = new THREE.Group();
  G.position.set(EX, 0, 0);
  scene.add(G);
  const E = (P.eo = {});
  E.skyDay = sky(G, [[0, "#8a9099"], [0.6, "#b4b8be"], [1, "#d6d7d8"]]);
  E.skyNight = sky(G, [[0, "#06070b"], [0.6, "#121522"], [1, "#2a2230"]], { stars: 40 });
  const ground = mesh(new THREE.PlaneGeometry(200, 140), std(0xffffff, { map: T.grass({ repeat: [14, 10] }), roughness: 1, color: "#56664a" }), { cast: false });
  ground.rotation.x = -Math.PI / 2;
  add(G, ground, 0, 0, 20);
  const road = mesh(new THREE.PlaneGeometry(200, 11), std(0xffffff, { map: T.asphalt({ repeat: [20, 2] }), roughness: 0.9, color: "#8e8e90" }), { cast: false });
  road.rotation.x = -Math.PI / 2;
  add(G, road, 0, 0.02, 20);
  const pave = mesh(new THREE.PlaneGeometry(200, 4.5), std(0xffffff, { map: T.concrete({ repeat: [40, 1] }), roughness: 0.85, color: "#bdb9b2" }), { cast: false });
  pave.rotation.x = -Math.PI / 2;
  add(G, pave, 0, 0.03, 12.2);
  for (const x of [-60, -40, -20, 0, 20, 40, 60]) for (const s of [-1, 1]) add(G, box(1.6, 0.03, 0.18, glowM("#e8d24a", 0.9), 0.01), x + s * 0.9, 0.04, 15.0); // double yellow lines
  // the semi-detached pair: ours on the left (x < 0), the neighbours on the right
  const brickM = std(0xffffff, { map: T.brick({ repeat: [6, 4] }), roughness: 0.9 });
  add(G, box(28, 16, 14, brickM, 0.05), 0, 8, -7);
  const roofM = std("#3a3a40", { roughness: 0.8 });
  for (const s of [-1, 1]) {
    const r = add(G, box(30, 0.7, 9.8, roofM, 0.05), 0, 19, -7 + s * 3.6);
    r.rotation.x = s * 0.8;
  }
  for (const s of [-1, 1]) add(G, box(0.5, 6.4, 14, brickM, 0.02), s * 14, 18.6, -7);
  add(G, box(1.4, 4, 1.4, brickM, 0.05), 0, 23, -7); // chimney
  E.win = [];
  for (const [x, y, w, h] of [[-9.5, 4.4, 5.2, 3.6], [-9.5, 12, 3.6, 3.2], [-3.8, 12, 2.6, 3.2], [9.5, 4.4, 5.2, 3.6], [9.5, 12, 3.6, 3.2], [3.8, 12, 2.6, 3.2]]) E.win.push(windowAt(G, x, y, 0.02, w, h, { shutters: false, trim: "#f4f2ec" }));
  add(G, box(3.0, 6.8, 0.3, std(0xffffff, { map: T.panelDoor({ color: "#2f6e7a" }) }), 0.04), -3.6, 3.4, 0.12);
  add(G, box(3.0, 6.8, 0.3, std(0xffffff, { map: T.panelDoor({ color: "#7a3a2a" }) }), 0.04), 3.6, 3.4, 0.12);
  add(G, mesh(new THREE.PlaneGeometry(1.1, 0.45), new THREE.MeshStandardMaterial({ map: signTex(["284"], { bg: "#f4f2ec", fg: "#1b1b1b", w: 256, h: 104, font: 72 }) }), { cast: false }), -3.6, 7.3, 0.2);
  for (const x of [-3.6, 3.6]) add(G, box(3.8, 0.3, 1.5, std("#5a5a5e"), 0.03), x, 7.9, 0.8); // door canopies
  // front walls, gates, path, a lamp post, a parked 70s car, houses opposite
  const lowWall = std(0xffffff, { map: T.brick({ repeat: [4, 0.6] }), roughness: 0.9 });
  for (const [x0, x1] of [[-14, -5], [-2.2, 2.2], [5, 14]]) add(G, box(x1 - x0, 1.6, 0.6, lowWall, 0.03), (x0 + x1) / 2, 0.8, 9.6);
  for (const x of [-3.6, 3.6]) {
    const p = mesh(new THREE.PlaneGeometry(2.4, 9.4), std(0xffffff, { map: T.concrete({ repeat: [1, 3] }), color: "#a9a59e" }), { cast: false });
    p.rotation.x = -Math.PI / 2;
    add(G, p, x, 0.03, 4.8);
  }
  add(G, box(0.4, 12, 0.4, std("#3a3d42"), 0.05), -16, 6, 11);
  add(G, box(0.3, 0.3, 2.6, std("#3a3d42"), 0.05), -16, 12, 12.2);
  const sod = glowM("#ffa040", 0.25);
  add(G, box(1.2, 0.5, 0.9, sod, 0.1), -16, 11.7, 13.4);
  E.lamp = { m: sod, pos: [EX - 16, 11.3, 13.4] };
  const car = new THREE.Group();
  car.position.set(8, 0, 18.2);
  car.rotation.y = Math.PI / 2;
  G.add(car);
  const cm = std("#c2793a", { roughness: 0.4, metalness: 0.3 });
  add(car, box(4.4, 1.8, 10, cm, 0.4), 0, 1.5, 0);
  add(car, box(4.0, 1.6, 5.0, std("#1a1e24", { roughness: 0.2, metalness: 0.4 }), 0.35), 0, 3.1, -0.4);
  for (const [x, z] of [[-2.1, 3.2], [2.1, 3.2], [-2.1, -3.2], [2.1, -3.2]]) {
    const wh = add(car, mesh(new THREE.CylinderGeometry(0.85, 0.85, 0.7, 14), std("#111")), x, 0.85, z);
    wh.rotation.z = Math.PI / 2;
  }
  for (const [x, ry] of [[-30, 0], [30, 0]]) {
    const hg = new THREE.Group();
    hg.position.set(x, 0, 0);
    hg.rotation.y = ry;
    G.add(hg);
    add(hg, box(28, 16, 14, brickM, 0.05), 0, 8, -7);
    for (const s of [-1, 1]) {
      const r = add(hg, box(30, 0.7, 9.8, roofM, 0.05), 0, 19, -7 + s * 3.6);
      r.rotation.x = s * 0.8;
    }
    for (const [wx, wy] of [[-9.5, 4.4], [9.5, 4.4], [-9.5, 12], [9.5, 12]]) windowAt(hg, wx, wy, 0.02, 4, 3.2, { shutters: false });
  }
  for (const x of [-34, 0, 34]) {
    const hg = new THREE.Group();
    hg.position.set(x, 0, 44);
    hg.rotation.y = Math.PI;
    G.add(hg);
    add(hg, box(30, 15, 12, brickM, 0.05), 0, 7.5, -6);
    for (const [wx, wy] of [[-9, 4], [9, 4], [-9, 11.5], [9, 11.5], [0, 11.5]]) windowAt(hg, wx, wy, 0.02, 4, 3, { shutters: false });
  }
  return G;
}

// ---- the girls' bedroom: two beds, the chest of drawers, 70s wallpaper ---------------------
function buildEnfieldBedroom(scene, P) {
  const G = new THREE.Group();
  G.position.set(...EB);
  scene.add(G);
  const wp = std(0xffffff, { map: T.wallpaper({ color: [28, 45, 38], repeat: [4, 2], seed: 31 }), roughness: 0.9 });
  const fl = mesh(new THREE.PlaneGeometry(18, 16), std(0xffffff, { map: T.rug({ seed: 12 }), roughness: 1, color: "#9a6a4a" }), { cast: false });
  fl.rotation.x = -Math.PI / 2;
  G.add(fl);
  const ce = mesh(new THREE.PlaneGeometry(18, 16), std("#e8e0cc"), { cast: false });
  ce.rotation.x = Math.PI / 2;
  add(G, ce, 0, 9.5, 0);
  add(G, box(18, 9.5, 0.4, wp, 0.02), 0, 4.75, -8);
  add(G, box(0.4, 9.5, 16, wp, 0.02), -9, 4.75, 0);
  add(G, box(0.4, 9.5, 16, wp, 0.02), 9, 4.75, 0);
  add(G, box(18, 9.5, 0.4, wp, 0.02), 0, 4.75, 8);
  // window on the back wall, orange curtains
  const nightM = new THREE.MeshBasicMaterial({ map: T.nightWindow() });
  add(G, mesh(new THREE.PlaneGeometry(3.6, 3.2), nightM, { cast: false }), 0, 5.8, -7.78);
  for (const s of [-1, 1]) add(G, box(1.4, 4.6, 0.3, std("#c46a2a", { roughness: 0.95 }), 0.15), s * 2.4, 5.6, -7.5);
  // two single beds
  const bedM = std("#6a4a32", { roughness: 0.6 });
  P.enfBeds = [];
  for (const [x, cover] of [[-5.6, "#7a8fbf"], [5.6, "#b0607a"]]) {
    const b = new THREE.Group();
    b.position.set(x, 0, -2.6);
    G.add(b);
    add(b, box(3.6, 1.6, 8.6, bedM, 0.08), 0, 0.8, 0);
    add(b, box(3.6, 3.6, 0.3, bedM, 0.08), 0, 1.8, -4.3);
    add(b, box(3.3, 0.7, 8.0, std("#eee8dc"), 0.2), 0, 1.95, 0.1);
    add(b, box(3.4, 0.4, 5.6, std(cover, { roughness: 0.95 }), 0.15), 0, 2.45, 1.2);
    add(b, box(2.4, 0.5, 1.3, std("#f4f0e6"), 0.2), 0, 2.55, -3.3);
    P.enfBeds.push(b);
  }
  // the chest of drawers (slides; local origin at its base centre)
  const chest = new THREE.Group();
  G.add(chest);
  const cw = std("#7a5636", { roughness: 0.55 });
  add(chest, box(3.6, 4.2, 1.8, cw, 0.06), 0, 2.1, 0);
  for (let i = 0; i < 3; i++) {
    add(chest, box(3.2, 1.05, 0.12, std("#8a6442", { roughness: 0.5 }), 0.03), 0, 0.9 + i * 1.25, 0.92);
    add(chest, box(0.6, 0.14, 0.14, std("#c9a24a", { metalness: 0.6, roughness: 0.3 }), 0.02), 0, 0.9 + i * 1.25, 1.02);
  }
  add(chest, box(1.0, 0.8, 0.6, std("#d9c38a"), 0.1), -0.8, 4.6, 0);
  P.chest = chest;
  P.chestHome = [0, 0, -6.6]; // local to the bedroom group
  // pictures on the wall that shake with the knocks
  P.frames = [];
  for (const [x, z, ry] of [[-8.75, -1.0, Math.PI / 2], [8.75, -3.6, -Math.PI / 2], [-8.75, 3.0, Math.PI / 2]]) {
    const f = new THREE.Group();
    f.position.set(x, 5.6, z);
    f.rotation.y = ry;
    G.add(f);
    add(f, box(1.6, 2.0, 0.12, std("#3a2a1e"), 0.03), 0, 0, 0);
    add(f, mesh(new THREE.PlaneGeometry(1.2, 1.6), std(0xffffff, { map: T.poster(P.frames.length % 2) }), { cast: false }), 0, 0, 0.07);
    P.frames.push(f);
  }
  // door (right wall, near the front), pendant lamp
  add(G, box(0.3, 7.0, 3.2, std(0xffffff, { map: T.panelDoor({ color: "#e9e2d2" }) }), 0.04), 8.8, 3.5, 5.6);
  add(G, mesh(new THREE.CylinderGeometry(0.06, 0.06, 1.2, 6), std("#222")), 0, 8.9, 1);
  P.enfBulbM = new THREE.MeshStandardMaterial({ color: "#f3e0b0", emissive: "#ffcf8a", emissiveIntensity: 0, side: THREE.DoubleSide });
  add(G, mesh(new THREE.CylinderGeometry(0.6, 1.0, 0.8, 16, 1, true), P.enfBulbM, { cast: false }), 0, 8.0, 1);
  // a spoon (for the hidden-camera shot) and toy blocks
  P.spoon = new THREE.Group();
  add(P.spoon, box(0.08, 0.9, 0.05, std("#d8dadf", { metalness: 0.8, roughness: 0.2 }), 0.02), 0, 0.45, 0);
  add(P.spoon, mesh(new THREE.SphereGeometry(0.16, 10, 8), std("#d8dadf", { metalness: 0.8, roughness: 0.2 })), 0, 0.98, 0);
  scene.add(P.spoon);
  return G;
}

// ---- the living room: Bill's armchair in the corner, the chair that slid, the tape recorder ---
function buildEnfieldLiving(scene, P) {
  const G = new THREE.Group();
  G.position.set(...EL);
  scene.add(G);
  const wp = std(0xffffff, { map: T.wallpaper({ color: [40, 30, 34], repeat: [5, 2], seed: 33 }), roughness: 0.9 });
  const fl = mesh(new THREE.PlaneGeometry(22, 18), std(0xffffff, { map: T.rug({ seed: 15 }), roughness: 1, color: "#8a5a3a" }), { cast: false });
  fl.rotation.x = -Math.PI / 2;
  G.add(fl);
  const ce = mesh(new THREE.PlaneGeometry(22, 18), std("#e8e0cc"), { cast: false });
  ce.rotation.x = Math.PI / 2;
  add(G, ce, 0, 9.5, 0);
  add(G, box(22, 9.5, 0.4, wp, 0.02), 0, 4.75, -9);
  add(G, box(0.4, 9.5, 18, wp, 0.02), -11, 4.75, 0);
  add(G, box(0.4, 9.5, 18, wp, 0.02), 11, 4.75, 0);
  add(G, box(22, 9.5, 0.4, wp, 0.02), 0, 4.75, 9);
  add(G, mesh(new THREE.PlaneGeometry(5, 3.4), new THREE.MeshBasicMaterial({ map: T.nightWindow({ seed: 97 }) }), { cast: false }), 4, 5.4, -8.78);
  add(G, mesh(new THREE.PlaneGeometry(5.2, 3.6), new THREE.MeshStandardMaterial({ color: "#f4f0e4", transparent: true, opacity: 0.45, roughness: 1 }), { cast: false }), 4, 5.4, -8.7);
  // Bill's armchair, back-left corner, turned into the room
  const arm = new THREE.Group();
  arm.position.set(-8.2, 0, -6.2);
  arm.rotation.y = Math.PI / 4;
  G.add(arm);
  const fab = std("#6b4a3a", { roughness: 0.95 });
  add(arm, box(3.4, 1.8, 3.2, fab, 0.4), 0, 1.4, 0.2);
  add(arm, box(3.4, 3.6, 0.9, fab, 0.4), 0, 2.6, -1.2);
  for (const s of [-1, 1]) add(arm, box(0.8, 2.6, 3.2, fab, 0.35), s * 1.5, 1.8, 0.2);
  add(arm, box(2.4, 0.5, 2.2, std("#7a5646", { roughness: 0.95 }), 0.25), 0, 2.45, 0.4);
  P.billChair = arm;
  // the dining chair that "wobbled and slid", by a small table
  const dc = new THREE.Group();
  G.add(dc);
  const dw = std("#5a3f2c", { roughness: 0.55 });
  add(dc, box(2.0, 0.25, 2.0, dw, 0.05), 0, 2.0, 0);
  add(dc, box(2.0, 2.8, 0.25, dw, 0.05), 0, 3.4, -0.9);
  for (const [lx, lz] of [[-0.85, -0.85], [0.85, -0.85], [-0.85, 0.85], [0.85, 0.85]]) add(dc, box(0.22, 2.0, 0.22, dw, 0.03), lx, 1.0, lz);
  P.diningChair = dc;
  P.diningHome = [3.5, 0, 1.0]; // local to the living-room group
  add(G, box(4.4, 0.3, 3.0, dw, 0.05), 6.6, 2.9, 1.0);
  for (const [lx, lz] of [[-1.9, -1.2], [1.9, -1.2], [-1.9, 1.2], [1.9, 1.2]]) add(G, box(0.25, 2.9, 0.25, dw, 0.03), 6.6 + lx, 1.45, 1.0 + lz);
  // the reel-to-reel tape recorder on the table, reels that spin
  const tape = new THREE.Group();
  tape.position.set(6.4, 3.05, 1.0);
  G.add(tape);
  add(tape, box(2.4, 0.5, 1.6, std("#2a2a2e", { roughness: 0.4 }), 0.08), 0, 0.25, 0);
  P.reels = [];
  for (const x of [-0.6, 0.6]) {
    const r = add(tape, mesh(new THREE.CylinderGeometry(0.5, 0.5, 0.08, 20), std("#9aa0a8", { metalness: 0.6, roughness: 0.3 })), x, 0.56, -0.1);
    for (let i = 0; i < 3; i++) {
      const sp = box(0.12, 0.1, 0.9, std("#33363c"), 0.02);
      sp.rotation.y = (i / 3) * Math.PI;
      r.add(sp);
    }
    P.reels.push(r);
  }
  // sofa, 70s TV, standard lamp, rotary phone on a side table, radio, toy blocks
  const sofa = std("#4a6a4a", { roughness: 0.95 });
  add(G, box(8, 1.8, 3.2, sofa, 0.4), 1.0, 1.2, 6.8);
  add(G, box(8, 3.0, 0.9, sofa, 0.4), 1.0, 2.6, 8.0);
  add(G, box(3.4, 2.8, 2.4, std("#4a3020", { roughness: 0.6 }), 0.1), 9.0, 1.4, -4.0);
  add(G, box(3.0, 2.4, 2.0, std("#5a3a26"), 0.15), 9.0, 4.0, -4.0);
  const tvM = new THREE.MeshBasicMaterial({ color: "#1a2420" });
  const tv = add(G, mesh(new THREE.PlaneGeometry(2.2, 1.7), tvM, { cast: false }), 7.98, 4.0, -4.0);
  tv.rotation.y = -Math.PI / 2;
  P.tv70 = tvM;
  add(G, mesh(new THREE.CylinderGeometry(0.08, 0.08, 6, 8), std("#c9a24a", { metalness: 0.5 })), -9.5, 3, 6.5);
  P.enfLampM = new THREE.MeshStandardMaterial({ color: "#f3e3c3", emissive: "#ffcf8a", emissiveIntensity: 0.8, side: THREE.DoubleSide });
  add(G, mesh(new THREE.CylinderGeometry(0.7, 1.1, 1.2, 16, 1, true), P.enfLampM, { cast: false }), -9.5, 6.4, 6.5);
  P.enfLampPos = [EL[0] - 9.5, 6.2, EL[2] + 6.5];
  add(G, box(2, 2.6, 2, dw, 0.05), -9.0, 1.3, 2.6);
  const phone = new THREE.Group();
  phone.position.set(-9.0, 2.6, 2.6);
  G.add(phone);
  add(phone, box(1.0, 0.5, 1.1, std("#e9e4d6", { roughness: 0.4 }), 0.15), 0, 0.25, 0);
  P.handset70 = add(phone, box(1.2, 0.3, 0.35, std("#e9e4d6", { roughness: 0.4 }), 0.12), 0, 0.66, 0);
  P.radio70 = add(G, box(1.8, 1.0, 0.8, std("#7a5636", { roughness: 0.5 }), 0.15), 7.8, 3.55, 2.1);
  const toyC = ["#d94b4b", "#3f7fd1", "#f2d04a", "#5bb36a", "#e8732a", "#9a5ad9"];
  P.toys = toyC.map((c, i) => {
    const t = box(0.95, 0.75, 0.95, std(c, { roughness: 0.5 }), 0.12);
    t.position.set(-2 + (i % 3) * 0.9, 0.23, 3.5 + Math.floor(i / 3) * 0.8);
    G.add(t);
    t.userData.home = t.position.clone();
    return t;
  });
  return G;
}

// ---- the globe: New Jersey to London ---------------------------------------------------
const LAND = [
  [[-168, 65], [-140, 70], [-95, 72], [-80, 63], [-60, 55], [-55, 48], [-66, 44], [-75, 36], [-81, 25], [-97, 26], [-105, 20], [-117, 32], [-124, 40], [-125, 48], [-135, 58], [-150, 60]],
  [[-50, 60], [-42, 60], [-20, 70], [-22, 80], [-45, 83], [-60, 78], [-55, 68]],
  [[-10, 36], [-9, 43], [-2, 44], [-5, 48], [2, 51], [8, 54], [10, 57], [5, 62], [15, 69], [28, 71], [40, 67], [60, 70], [60, 45], [40, 45], [30, 45], [26, 40], [20, 40], [14, 41], [16, 38], [12, 44], [8, 44], [3, 43], [-1, 37]],
  [[-5.7, 50], [1.7, 51.3], [1.7, 52.8], [0, 53.5], [-1.6, 55.6], [-3, 58.6], [-5, 58.6], [-6.2, 56.5], [-5, 54.8], [-3.2, 54], [-4.6, 53.3], [-4.5, 51.7]],
  [[-10, 51.6], [-6, 52], [-6, 54.8], [-8, 55.2], [-10, 54]],
  [[-17, 21], [-6, 36], [10, 37], [32, 31], [35, 28], [43, 12], [51, 12], [40, -5], [30, -30], [20, -35], [12, -17], [9, 4], [-8, 4], [-17, 14]],
  [[-80, 10], [-60, 12], [-50, 0], [-35, -7], [-40, -22], [-58, -38], [-68, -55], [-75, -45], [-72, -20], [-81, -5]],
];
export const NJ = [-74.35, 40.65], LDN = [-0.05, 51.65];
export function lonLat(lon, lat, r) {
  const phi = (lat * Math.PI) / 180, th = (lon * Math.PI) / 180;
  return new THREE.Vector3(r * Math.cos(phi) * Math.sin(th), r * Math.sin(phi), r * Math.cos(phi) * Math.cos(th));
}
function buildGlobe(scene, P) {
  const G = new THREE.Group();
  G.position.set(...GLOBE);
  scene.add(G);
  const [c, g] = cnv(2048, 1024);
  g.fillStyle = "#0b1c33";
  g.fillRect(0, 0, 2048, 1024);
  g.strokeStyle = "rgba(120,170,230,0.18)";
  g.lineWidth = 2;
  for (let lon = -180; lon <= 180; lon += 15) {
    g.beginPath();
    g.moveTo(((lon + 180) / 360) * 2048, 0);
    g.lineTo(((lon + 180) / 360) * 2048, 1024);
    g.stroke();
  }
  for (let lat = -75; lat <= 75; lat += 15) {
    g.beginPath();
    g.moveTo(0, ((90 - lat) / 180) * 1024);
    g.lineTo(2048, ((90 - lat) / 180) * 1024);
    g.stroke();
  }
  g.fillStyle = "#2c5a4a";
  g.strokeStyle = "#7fd0b0";
  g.lineWidth = 3;
  for (const poly of LAND) {
    g.beginPath();
    poly.forEach(([lon, lat], i) => {
      const x = ((lon + 180) / 360) * 2048, y = ((90 - lat) / 180) * 1024;
      i ? g.lineTo(x, y) : g.moveTo(x, y);
    });
    g.closePath();
    g.fill();
    g.stroke();
  }
  const t = ctex(c);
  const globe = new THREE.Mesh(new THREE.SphereGeometry(10, 64, 32), new THREE.MeshStandardMaterial({ map: t, roughness: 0.7, emissive: "#0a1830", emissiveIntensity: 0.6 }));
  globe.rotation.y = -Math.PI / 2; // texture u=0.5 (lon 0) faces +z after this offset
  G.add(globe);
  const atm = new THREE.Mesh(new THREE.SphereGeometry(10.5, 48, 24), new THREE.MeshBasicMaterial({ color: "#4a8ad8", transparent: true, opacity: 0.12, side: THREE.BackSide }));
  G.add(atm);
  // pins + arc (positions in globe-group space; the sphere's lon offset is folded in)
  const pin = (ll, color) => {
    const p = new THREE.Group();
    const v = lonLat(ll[0], ll[1], 10.05);
    p.position.copy(v);
    p.lookAt(v.clone().multiplyScalar(2));
    add(p, mesh(new THREE.CylinderGeometry(0.06, 0.06, 1.2, 8), glowM(color, 1.4), { cast: false }), 0, 0, 0.6).rotation.x = Math.PI / 2;
    add(p, mesh(new THREE.SphereGeometry(0.28, 12, 10), glowM(color, 1.8), { cast: false }), 0, 0, 1.25);
    G.add(p);
    return p;
  };
  P.pinNJ = pin(NJ, "#ff5a4a");
  P.pinUK = pin(LDN, "#ffd04a");
  const pts = [];
  for (let i = 0; i <= 80; i++) {
    const k = i / 80;
    const a = lonLat(NJ[0], NJ[1], 1), b = lonLat(LDN[0], LDN[1], 1);
    const v = a.clone().lerp(b, k).normalize().multiplyScalar(10.1 + Math.sin(k * Math.PI) * 2.2);
    pts.push(v);
  }
  const arcGeo = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 160, 0.07, 8, false);
  P.arc = add(G, mesh(arcGeo, glowM("#ffffff", 1.6), { cast: false }), 0, 0, 0);
  P.arcCount = arcGeo.index.count;
  P.globe = globe;
  // stars around it
  const sg = new THREE.BufferGeometry();
  const r = rng(77);
  const arr = new Float32Array(900 * 3);
  for (let i = 0; i < 900; i++) {
    const v = new THREE.Vector3(r() - 0.5, r() - 0.5, r() - 0.5).normalize().multiplyScalar(90 + r() * 40);
    arr.set([v.x, v.y, v.z], i * 3);
  }
  sg.setAttribute("position", new THREE.BufferAttribute(arr, 3));
  G.add(new THREE.Points(sg, new THREE.PointsMaterial({ color: "#ffffff", size: 0.5, sizeAttenuation: true })));
  return G;
}

// ---- the outro diorama: both houses as small models on a dark table ---------------------------
function buildDiorama(scene, P) {
  const G = new THREE.Group();
  G.position.set(...DIO);
  scene.add(G);
  const tableM = std("#1a1412", { roughness: 0.4, metalness: 0.1 });
  add(G, box(60, 1, 30, tableM, 0.2), 0, -0.5, 0);
  for (const x of [-12, 12]) add(G, mesh(new THREE.CylinderGeometry(9, 9.4, 1.2, 40), std("#2a2420", { roughness: 0.6 })), x, 0.6, 0);
  P.dioSlots = [[DIO[0] - 12, DIO[1] + 1.2, DIO[2]], [DIO[0] + 12, DIO[1] + 1.2, DIO[2]]];
  P.dioLabels = [];
  for (const [x, label] of [[-12, "657 BOULEVARD · NEW JERSEY · 2014"], [12, "284 GREEN STREET · LONDON · 1977"]]) {
    const [c, g] = cnv(1024, 128);
    g.fillStyle = "#c9a24a";
    g.fillRect(0, 0, 1024, 128);
    g.fillStyle = "#1a1412";
    g.font = "800 54px Poppins, sans-serif";
    g.textAlign = "center";
    g.textBaseline = "middle";
    g.fillText(label, 512, 66);
    const pl = add(G, mesh(new THREE.PlaneGeometry(8, 1), new THREE.MeshStandardMaterial({ map: ctex(c), roughness: 0.4, metalness: 0.4 }), { cast: false }), x, 0.65, 9.5);
    pl.rotation.x = -0.6;
    P.dioLabels.push(pl);
  }
  return G;
}

// models placed on the diorama: clones of the real sets, scaled down (shared geometry and materials)
export function placeDioramaModels(P) {
  const mk = (src, s, at, ry) => {
    const m = new THREE.Group();
    for (const ch of src.children) {
      if (ch.geometry && ch.geometry.type === "SphereGeometry" && ch.geometry.parameters.radius > 100) continue; // skip skies
      if (ch.geometry && ch.geometry.type === "PlaneGeometry" && ch.geometry.parameters.width >= 200) continue; // skip ground
      const p = ch.position;
      if (Math.abs(p.x) > 16 || p.z < -18 || p.z > 10) continue; // just the house itself
      m.add(ch.clone(true));
    }
    const lawn = mesh(new THREE.CircleGeometry(30, 40), std("#4a6040", { roughness: 1 }), { cast: false });
    lawn.rotation.x = -Math.PI / 2;
    lawn.position.y = 0.05;
    m.add(lawn);
    m.scale.setScalar(s);
    m.position.set(...at);
    m.rotation.y = ry;
    P.sets.dio.parent.add(m);
    return m;
  };
  P.dioWatcher = mk(P.sets.watcher, 0.28, P.dioSlots[0], 0.35);
  P.dioEnfield = mk(P.sets.enfOut, 0.28, P.dioSlots[1], -0.35);
}

// renovation props inside the HX house (657's interior while Derek fixes it up)
export function buildReno(H, P) {
  const R = new THREE.Group();
  H.add(R);
  const lad = std("#c9c2b6", { roughness: 0.5, metalness: 0.3 });
  const ladder = new THREE.Group();
  ladder.position.set(9.4, 0, -7.8);
  ladder.rotation.y = -0.5;
  R.add(ladder);
  for (const s of [-1, 1]) {
    const rail = add(ladder, box(0.25, 9, 0.25, lad, 0.03), s * 0.9, 4.4, 0);
    rail.rotation.x = 0.12;
  }
  for (let i = 0; i < 6; i++) add(ladder, box(1.8, 0.18, 0.3, lad, 0.02), 0, 1 + i * 1.4, -0.12 - i * 0.17);
  const sheet = mesh(new THREE.PlaneGeometry(10, 7), std("#e8e4da", { roughness: 1 }), { cast: false });
  sheet.rotation.x = -Math.PI / 2;
  add(R, sheet, 7, 0.04, -5.5);
  for (const [x, z, c] of [[5.0, -7.6, "#d9d4c8"], [6.0, -8.0, "#8aa8c8"], [3.8, -7.0, "#d9d4c8"]]) {
    add(R, mesh(new THREE.CylinderGeometry(0.55, 0.55, 1.1, 16), std("#b9bcc2", { metalness: 0.6, roughness: 0.3 })), x, 0.55, z);
    add(R, mesh(new THREE.CylinderGeometry(0.5, 0.5, 0.06, 16), std(c)), x, 1.12, z);
  }
  // a half-painted wall patch and a work light
  add(R, mesh(new THREE.PlaneGeometry(7, 6), std("#cfd8de", { roughness: 0.9 }), { cast: false }), 6.0, 4.0, -9.97);
  P.roller = new THREE.Group();
  add(P.roller, box(0.1, 2.2, 0.1, std("#3a3a3a"), 0.02), 0, -1.1, 0);
  add(P.roller, mesh(new THREE.CylinderGeometry(0.28, 0.28, 1.2, 12), std("#cfd8de", { roughness: 1 })), 0, 0.1, 0).rotation.z = Math.PI / 2;
  H.parent.add(P.roller);
  P.reno = R;
  return R;
}

// small props that travel between sets (all hidden until a shot places them)
export function buildProps(scene, P) {
  const pr = (P.props2 = {});
  // a police cruiser with a light bar (Westfield)
  const car = new THREE.Group();
  const white = std("#e9ecef", { roughness: 0.35, metalness: 0.3 });
  const black = std("#15171b", { roughness: 0.35, metalness: 0.3 });
  add(car, box(5.2, 1.9, 11.5, white, 0.4), 0, 1.7, 0);
  add(car, box(5.25, 1.0, 4.0, black, 0.3), 0, 1.9, 0);
  add(car, box(4.8, 1.7, 5.6, std("#10141a", { roughness: 0.15, metalness: 0.5 }), 0.35), 0, 3.4, -0.6);
  const red = glowM("#ff2a2a", 0.3), blue = glowM("#2a6aff", 0.3);
  add(car, box(1.8, 0.4, 0.7, red, 0.08), -1.0, 4.45, -0.6);
  add(car, box(1.8, 0.4, 0.7, blue, 0.08), 1.0, 4.45, -0.6);
  for (const [x, z] of [[-2.4, 3.8], [2.4, 3.8], [-2.4, -3.8], [2.4, -3.8]]) {
    const wh = add(car, mesh(new THREE.CylinderGeometry(0.9, 0.9, 0.7, 14), std("#111")), x, 0.9, z);
    wh.rotation.z = Math.PI / 2;
  }
  scene.add(car);
  pr.cruiser = { group: car, red, blue };
  // an envelope and a sheet of paper to hold
  const envT = P.desk.env.material.map;
  pr.env = mesh(new THREE.PlaneGeometry(2.0, 1.2), new THREE.MeshStandardMaterial({ map: envT, roughness: 0.85, side: THREE.DoubleSide }), { cast: false });
  scene.add(pr.env);
  pr.handset = box(1.2, 0.3, 0.35, std("#e9e4d6", { roughness: 0.4 }), 0.12);
  scene.add(pr.handset);
  pr.paper = mesh(new THREE.PlaneGeometry(1.3, 1.7), new THREE.MeshStandardMaterial({ color: "#efe6d2", roughness: 0.85, side: THREE.DoubleSide }), { cast: false });
  scene.add(pr.paper);
  // a press camera with a flash, a notebook, a microphone on a lead
  const cam = new THREE.Group();
  add(cam, box(1.0, 0.7, 0.6, std("#1b1b1f", { roughness: 0.4 }), 0.08), 0, 0, 0);
  add(cam, mesh(new THREE.CylinderGeometry(0.25, 0.28, 0.5, 14), std("#2a2a2e")), 0, 0, 0.5).rotation.x = Math.PI / 2;
  pr.flashM = glowM("#ffffff", 0.2);
  add(cam, box(0.5, 0.35, 0.3, pr.flashM, 0.05), 0.2, 0.6, 0.1);
  scene.add(cam);
  pr.camera = cam;
  pr.notebook = box(0.6, 0.8, 0.08, std("#e8e2d0"), 0.02);
  scene.add(pr.notebook);
  const mic = new THREE.Group();
  add(mic, mesh(new THREE.CylinderGeometry(0.07, 0.07, 0.9, 10), std("#1b1b1f")), 0, 0.45, 0);
  add(mic, mesh(new THREE.SphereGeometry(0.18, 12, 10), std("#3a3a3e", { roughness: 0.6 })), 0, 0.95, 0);
  scene.add(mic);
  pr.mic = mic;
  for (const k of Object.keys(pr)) if (pr[k] && pr[k].isObject3D) pr[k].visible = false;
  car.visible = false;
}
