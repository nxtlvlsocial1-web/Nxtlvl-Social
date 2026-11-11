// Blocky avatar cast. Units are studs; an avatar stands 5.25 studs tall.
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import * as T from "./textures.js";

const geoCache = new Map();
function rbox(w, h, d, r = 0.07) {
  const k = [w, h, d, r].join(",");
  if (!geoCache.has(k)) geoCache.set(k, new RoundedBoxGeometry(w, h, d, 2, Math.min(r, w / 2.1, h / 2.1, d / 2.1)));
  return geoCache.get(k);
}
export const std = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.62, metalness: 0, ...o });

export function mesh(geo, material, { cast = true, receive = true } = {}) {
  const m = new THREE.Mesh(geo, material);
  m.castShadow = cast;
  m.receiveShadow = receive;
  return m;
}
export const box = (w, h, d, material, r) => mesh(rbox(w, h, d, r), material);

function bandTex(top, bottom, frac) {
  const c = document.createElement("canvas");
  c.width = 32;
  c.height = 128;
  const g = c.getContext("2d");
  g.fillStyle = top;
  g.fillRect(0, 0, 32, 128);
  g.fillStyle = bottom;
  g.fillRect(0, 128 * (1 - frac), 32, 128 * frac);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}
// a limb whose lower `frac` is another colour (hands on sleeves, shoes on trousers)
function limbMats(top, bottom, frac, extra = {}) {
  const side = std(0xffffff, { map: bandTex(top, bottom, frac), ...extra });
  return [side, side, std(top, extra), std(bottom, extra), side, side];
}

// classic rounded-cylinder head
const HEAD_R = 0.62, HEAD_H = 1.25;
let headGeo = null;
function headGeometry() {
  if (headGeo) return headGeo;
  const rr = 0.24, pts = [];
  pts.push(new THREE.Vector2(0, -HEAD_H / 2));
  for (let i = 0; i <= 6; i++) {
    const a = -Math.PI / 2 + (i / 6) * (Math.PI / 2);
    pts.push(new THREE.Vector2(HEAD_R - rr + Math.cos(a) * rr, -HEAD_H / 2 + rr + Math.sin(a) * rr));
  }
  for (let i = 0; i <= 6; i++) {
    const a = (i / 6) * (Math.PI / 2);
    pts.push(new THREE.Vector2(HEAD_R - rr + Math.cos(a) * rr, HEAD_H / 2 - rr + Math.sin(a) * rr));
  }
  pts.push(new THREE.Vector2(0, HEAD_H / 2));
  headGeo = new THREE.LatheGeometry(pts, 40);
  return headGeo;
}
const faceGeo = new THREE.CylinderGeometry(HEAD_R + 0.006, HEAD_R + 0.006, 0.82, 28, 1, true, -0.95, 1.9);

const faceTexCache = new Map();
export function face(name, opts = {}) {
  const k = name + JSON.stringify(opts);
  if (!faceTexCache.has(k)) faceTexCache.set(k, name === "mimic" ? T.mimicFace(opts) : T.faceTexture(name, opts));
  return faceTexCache.get(k);
}

// ---------------------------------------------------------------------------
export function makeAvatar(spec) {
  const root = new THREE.Group();
  root.name = spec.name;
  const skin = spec.skin || "#f2c9a0";
  const pelvis = new THREE.Group();
  pelvis.position.y = 2;
  root.add(pelvis);

  const outfits = {};
  const parts = {};
  const addOutfit = (name, o) => {
    outfits[name] = {
      torso: o.torso,
      arm: limbMats(o.sleeve, skin, o.sleeveFrac ?? 0.22),
      leg: limbMats(o.pants, o.shoes || "#2a2420", o.shoeFrac ?? 0.16),
    };
  };
  for (const [n, o] of Object.entries(spec.outfits)) addOutfit(n, o);
  const first = Object.values(outfits)[0];

  for (const side of [-1, 1]) {
    const leg = new THREE.Group();
    leg.position.set(side * 0.5, 0, 0);
    const m = box(0.98, 2, 1, first.leg);
    m.position.y = -1;
    leg.add(m);
    pelvis.add(leg);
    parts[side < 0 ? "legL" : "legR"] = leg;
    parts[side < 0 ? "legLm" : "legRm"] = m;
  }
  const torso = new THREE.Group();
  pelvis.add(torso);
  const torsoM = box(2, 2, 1, first.torso);
  torsoM.position.y = 1;
  torso.add(torsoM);
  for (const side of [-1, 1]) {
    const arm = new THREE.Group();
    arm.position.set(side * 1.5, 1.5, 0);
    const m = box(0.98, 2, 1, first.arm);
    m.position.y = -0.5;
    arm.add(m);
    torso.add(arm);
    parts[side < 0 ? "armL" : "armR"] = arm;
    parts[side < 0 ? "armLm" : "armRm"] = m;
    // hand anchor at the bottom of the arm, for holding props
    const hand = new THREE.Group();
    hand.position.y = -1.45;
    arm.add(hand);
    parts[side < 0 ? "handL" : "handR"] = hand;
  }
  const head = new THREE.Group();
  head.position.y = 2;
  torso.add(head);
  const headM = mesh(headGeometry(), std(skin, { roughness: 0.5 }));
  headM.position.y = HEAD_H / 2;
  head.add(headM);
  const faceMat = new THREE.MeshStandardMaterial({ map: face(spec.face || "smile"), transparent: true, alphaTest: 0.35,
    roughness: 0.55, polygonOffset: true, polygonOffsetFactor: -2 });
  const faceM = mesh(faceGeo, faceMat, { cast: false });
  faceM.position.y = HEAD_H / 2 + 0.02;
  head.add(faceM);
  const headTop = new THREE.Group(); // accessories origin = head centre
  headTop.position.y = HEAD_H / 2;
  head.add(headTop);
  if (spec.hair) spec.hair(headTop);

  Object.assign(parts, { root, pelvis, torso, torsoM, head, headTop });
  const av = {
    name: spec.name,
    root,
    j: parts,
    outfit: Object.keys(outfits)[0],
    faceName: spec.face || "smile",
    defaultFace: spec.face || "smile",
    setFace(name, opts) {
      this.faceName = name;
      faceMat.map = face(name, opts);
    },
    setOutfit(name) {
      const o = outfits[name];
      this.outfit = name;
      parts.torsoM.material = o.torso;
      parts.armLm.material = parts.armRm.material = o.arm;
      parts.legLm.material = parts.legRm.material = o.leg;
      if (spec.onOutfit) spec.onOutfit(name, parts);
    },
    reset() {
      root.visible = false;
      root.position.set(0, 0, 0);
      root.rotation.set(0, 0, 0);
      root.scale.setScalar(1);
      pelvis.position.set(0, 2, 0);
      pelvis.rotation.set(0, 0, 0);
      for (const k of ["torso", "head", "armL", "armR", "legL", "legR"]) parts[k].rotation.set(0, 0, 0);
      this.setFace(this.defaultFace);
      const firstName = Object.keys(outfits)[0];
      if (this.outfit !== firstName) this.setOutfit(firstName);
    },
  };
  return av;
}

// --- hair & accessories ----------------------------------------------------
const kidHair = (top) => {
  const m = std("#4a2f1c", { roughness: 0.8 });
  const cap = box(1.36, 0.46, 1.36, m, 0.14);
  cap.position.set(0, 0.5, -0.04);
  top.add(cap);
  const fringe = box(1.25, 0.3, 0.42, m, 0.1);
  fringe.position.set(0.05, 0.36, 0.5);
  fringe.rotation.set(0.35, 0, -0.08);
  top.add(fringe);
  const back = box(1.3, 0.8, 0.4, m, 0.12);
  back.position.set(0, 0.15, -0.5);
  top.add(back);
  for (const [x, z, r] of [[-0.35, 0.1, 0.4], [0.1, 0.25, -0.2], [0.4, -0.15, 0.3]]) {
    const s = box(0.38, 0.32, 0.38, m, 0.08);
    s.position.set(x, 0.78, z);
    s.rotation.set(r, r * 0.6, r * 0.8);
    top.add(s);
  }
  for (const side of [-1, 1]) {
    const sb = box(0.22, 0.5, 0.5, m, 0.08);
    sb.position.set(side * 0.62, 0.15, 0.05);
    top.add(sb);
  }
};

const grandpaHair = (top) => {
  const white = std("#ece9e2", { roughness: 0.9 });
  for (const side of [-1, 1]) {
    const tuft = box(0.3, 0.46, 0.7, white, 0.12);
    tuft.position.set(side * 0.64, 0.08, -0.08);
    tuft.rotation.z = side * -0.15;
    top.add(tuft);
    const tuft2 = box(0.22, 0.3, 0.3, white, 0.08);
    tuft2.position.set(side * 0.72, 0.32, 0.05);
    tuft2.rotation.z = side * -0.5;
    top.add(tuft2);
    // bushy brows
    const brow = box(0.3, 0.08, 0.1, white, 0.03);
    brow.position.set(side * 0.18, 0.24, 0.61);
    brow.rotation.z = side * 0.12;
    top.add(brow);
  }
  const backTuft = box(1.0, 0.4, 0.3, white, 0.12);
  backTuft.position.set(0, 0.0, -0.58);
  top.add(backTuft);
  const stache = box(0.52, 0.15, 0.14, white, 0.06);
  stache.position.set(0, -0.06, 0.64);
  stache.name = "stache";
  top.add(stache);
  // glasses
  const frame = std("#1d1a18", { roughness: 0.35, metalness: 0.3 });
  const rimGeo = new THREE.TorusGeometry(0.14, 0.02, 8, 24);
  for (const side of [-1, 1]) {
    const rim = mesh(rimGeo, frame, { cast: false });
    rim.position.set(side * 0.17, 0.06, 0.66);
    rim.scale.set(1.1, 0.85, 1);
    top.add(rim);
    const lens = mesh(new THREE.CircleGeometry(0.135, 20),
      new THREE.MeshStandardMaterial({ color: "#cfe6ff", transparent: true, opacity: 0.18, roughness: 0.05 }), { cast: false });
    lens.position.copy(rim.position);
    lens.scale.copy(rim.scale);
    top.add(lens);
    const arm = box(0.03, 0.03, 0.6, frame, 0.01);
    arm.position.set(side * 0.62, 0.08, 0.36);
    top.add(arm);
  }
  const bridge = box(0.08, 0.025, 0.025, frame, 0.01);
  bridge.position.set(0, 0.08, 0.67);
  top.add(bridge);
};

const momHair = (top) => {
  const m = std("#2b1a12", { roughness: 0.75 });
  const cap = box(1.36, 0.5, 1.36, m, 0.18);
  cap.position.set(0, 0.48, -0.02);
  top.add(cap);
  const side = box(1.4, 0.9, 0.9, m, 0.2);
  side.position.set(0, 0.1, -0.3);
  top.add(side);
  const bun = box(0.5, 0.5, 0.5, m, 0.2);
  bun.position.set(0, 0.55, -0.72);
  top.add(bun);
  const tail = box(0.34, 0.9, 0.34, m, 0.14);
  tail.position.set(0, 0.05, -0.92);
  tail.rotation.x = 0.35;
  top.add(tail);
  const fringe = box(1.2, 0.22, 0.3, m, 0.08);
  fringe.position.set(-0.12, 0.42, 0.54);
  fringe.rotation.set(0.3, 0, 0.18);
  top.add(fringe);
};

function glasses(top, frameColor = "#1d1a18", round = true) {
  const frame = std(frameColor, { roughness: 0.35, metalness: 0.3 });
  const rimGeo = new THREE.TorusGeometry(0.14, 0.02, 8, 24);
  for (const side of [-1, 1]) {
    const rim = mesh(rimGeo, frame, { cast: false });
    rim.position.set(side * 0.17, 0.06, 0.66);
    rim.scale.set(1.1, round ? 0.9 : 0.7, 1);
    top.add(rim);
    const arm = box(0.03, 0.03, 0.6, frame, 0.01);
    arm.position.set(side * 0.62, 0.08, 0.36);
    top.add(arm);
  }
  const bridge = box(0.08, 0.025, 0.025, frame, 0.01);
  bridge.position.set(0, 0.08, 0.67);
  top.add(bridge);
}

const dadHair = (top) => {
  const m = std("#2a1d14", { roughness: 0.8 });
  const cap = box(1.34, 0.36, 1.34, m, 0.12);
  cap.position.set(0, 0.52, -0.02);
  top.add(cap);
  const part = box(0.9, 0.22, 0.42, m, 0.08);
  part.position.set(0.18, 0.5, 0.5);
  part.rotation.z = -0.12;
  top.add(part);
  const back = box(1.3, 0.6, 0.3, m, 0.1);
  back.position.set(0, 0.25, -0.55);
  top.add(back);
  for (const side of [-1, 1]) {
    const sb = box(0.16, 0.45, 0.5, m, 0.06);
    sb.position.set(side * 0.62, 0.22, 0.02);
    top.add(sb);
  }
  const beard = box(1.08, 0.42, 0.3, m, 0.14);
  beard.position.set(0, -0.48, 0.5);
  top.add(beard);
  const stache = box(0.5, 0.11, 0.12, m, 0.05);
  stache.position.set(0, -0.12, 0.64);
  top.add(stache);
};

const sisterHair = (top) => {
  const m = std("#5a3420", { roughness: 0.75 });
  const cap = box(1.38, 0.46, 1.38, m, 0.18);
  cap.position.set(0, 0.5, -0.02);
  top.add(cap);
  const back = box(1.42, 2.2, 0.36, m, 0.15);
  back.position.set(0, -0.3, -0.62);
  top.add(back);
  for (const side of [-1, 1]) {
    const strand = box(0.24, 1.7, 0.46, m, 0.1);
    strand.position.set(side * 0.66, -0.15, 0.12);
    top.add(strand);
  }
  const fringe = box(1.25, 0.24, 0.3, m, 0.08);
  fringe.position.set(0.1, 0.42, 0.55);
  fringe.rotation.set(0.25, 0, -0.15);
  top.add(fringe);
};

const grandmaHair = (top) => {
  const m = std("#d9d6d0", { roughness: 0.85 });
  const cap = box(1.38, 0.5, 1.38, m, 0.2);
  cap.position.set(0, 0.48, -0.04);
  top.add(cap);
  const bun = box(0.62, 0.55, 0.62, m, 0.26);
  bun.position.set(0, 0.85, -0.35);
  top.add(bun);
  for (const side of [-1, 1]) {
    const sb = box(0.22, 0.6, 0.7, m, 0.1);
    sb.position.set(side * 0.64, 0.12, -0.05);
    top.add(sb);
  }
  glasses(top, "#7a3b5a", true);
};

const guestHair = (color) => (top) => {
  const m = std(color, { roughness: 0.8 });
  const cap = box(1.34, 0.42, 1.34, m, 0.14);
  cap.position.set(0, 0.5, -0.04);
  top.add(cap);
};

// ---------------------------------------------------------------------------
export function makeCast() {
  const sideMat = (c) => std(c, { roughness: 0.75 });
  const hoodie = T.hoodieFront();
  const kid = makeAvatar({
    name: "kid",
    skin: "#f0c39b",
    face: "smile",
    hair: kidHair,
    outfits: {
      pjs: {
        torso: Array.from({ length: 6 }, () => std(0xffffff, { map: T.pajamas(), roughness: 0.85 })),
        sleeve: "#7fa7d9", sleeveFrac: 0.16,
        pants: "#7fa7d9", shoes: "#f0c39b", shoeFrac: 0.14,
      },
      hoodie: {
        torso: [sideMat("#e8732a"), sideMat("#e8732a"), sideMat("#e8732a"), sideMat("#e8732a"), std(0xffffff, { map: hoodie, roughness: 0.75 }), sideMat("#d9661f")],
        sleeve: "#e8732a", sleeveFrac: 0.18,
        pants: "#2c3f63", shoes: "#f2f2f2", shoeFrac: 0.14,
      },
    },
  });

  const cardigan = T.cardiganFront();
  const knitSide = T.knit({ colors: ["#55704f", "#4a6345", "#6b4a2e", "#4a6345"], band: 4, repeat: [1, 1] });
  const suit = T.suitFront();
  const grandpa = makeAvatar({
    name: "grandpa",
    skin: "#f1c7a3",
    face: "sleep",
    hair: grandpaHair,
    outfits: {
      cardigan: {
        torso: [std(0xffffff, { map: knitSide, roughness: 0.9 }), std(0xffffff, { map: knitSide, roughness: 0.9 }), std("#4a6345"), std("#4a6345"),
          std(0xffffff, { map: cardigan, roughness: 0.85 }), std(0xffffff, { map: knitSide, roughness: 0.9 })],
        sleeve: "#4f6849", sleeveFrac: 0.2,
        pants: "#6a5340", shoes: "#8a6a4a", shoeFrac: 0.15,
      },
      suit: {
        torso: [sideMat("#2b2f3a"), sideMat("#2b2f3a"), sideMat("#2b2f3a"), sideMat("#2b2f3a"), std(0xffffff, { map: suit, roughness: 0.6 }), sideMat("#2b2f3a")],
        sleeve: "#2b2f3a", sleeveFrac: 0.2,
        pants: "#2b2f3a", shoes: "#111111", shoeFrac: 0.15,
      },
    },
  });

  const scrubs = T.scrubsFront();
  const mom = makeAvatar({
    name: "mom",
    skin: "#e6b48c",
    face: "momSmile",
    hair: momHair,
    outfits: {
      home: {
        torso: [sideMat("#d9a23a"), sideMat("#d9a23a"), sideMat("#d9a23a"), sideMat("#d9a23a"), std(0xffffff, { map: T.knit({ colors: ["#d9a23a", "#cf9530", "#e2ae48", "#cf9530"], band: 3, repeat: [1, 1] }), roughness: 0.85 }), sideMat("#d9a23a")],
        sleeve: "#d9a23a", sleeveFrac: 0.18,
        pants: "#3a4f78", shoes: "#f4f4f4",
      },
      scrubs: {
        torso: [sideMat("#2f9e9a"), sideMat("#2f9e9a"), sideMat("#2f9e9a"), sideMat("#2f9e9a"), std(0xffffff, { map: scrubs, roughness: 0.7 }), sideMat("#2f9e9a")],
        sleeve: "#2f9e9a", sleeveFrac: 0.45,
        pants: "#2f9e9a", shoes: "#f4f4f4",
      },
    },
  });

  const guests = [
    ["#8a2b4a", "#2b2f3a", "#3a2416", "#e8b998"],
    ["#2b4a8a", "#2b2f3a", "#d9b25a", "#c98f62"],
    ["#e9e4dc", "#e9e4dc", "#5a3a22", "#f2c9a0"],
    ["#3d6b4a", "#2b2f3a", "#1b1b1b", "#8d5a3b"],
  ].map(([shirt, pants, hair, skinC], i) =>
    makeAvatar({
      name: "guest" + i,
      skin: skinC,
      face: i % 2 ? "grin" : "smile",
      hair: guestHair(hair),
      outfits: { party: { torso: sideMat(shirt), sleeve: shirt, pants, shoes: "#151515" } },
    }),
  );

  const polo = (() => {
    const c = document.createElement("canvas");
    c.width = c.height = 256;
    const g = c.getContext("2d");
    g.fillStyle = "#3f6fb5";
    g.fillRect(0, 0, 256, 256);
    g.fillStyle = "#f2f2f2";
    g.beginPath();
    g.moveTo(80, 0); g.lineTo(128, 50); g.lineTo(176, 0); g.closePath(); g.fill();
    g.fillStyle = "#2f5a99";
    g.fillRect(118, 40, 20, 70);
    g.fillStyle = "#f2f2f2";
    for (const y of [60, 90]) { g.beginPath(); g.arc(128, y, 6, 0, Math.PI * 2); g.fill(); }
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    return t;
  })();
  const dad = makeAvatar({
    name: "dad",
    skin: "#e9b98f",
    face: "smile",
    hair: dadHair,
    outfits: {
      polo: {
        torso: [sideMat("#3f6fb5"), sideMat("#3f6fb5"), sideMat("#3f6fb5"), sideMat("#3f6fb5"), std(0xffffff, { map: polo, roughness: 0.7 }), sideMat("#3f6fb5")],
        sleeve: "#3f6fb5", sleeveFrac: 0.5,
        pants: "#b8a27a", shoes: "#4a3426",
      },
    },
  });
  const hoodieP = T.hoodieFront({ color: "#7b4fc0", dark: "#5c3699" });
  const sister = makeAvatar({
    name: "sister",
    skin: "#f0c39b",
    face: "flat",
    hair: sisterHair,
    outfits: {
      hoodie: {
        torso: [sideMat("#7b4fc0"), sideMat("#7b4fc0"), sideMat("#7b4fc0"), sideMat("#7b4fc0"), std(0xffffff, { map: hoodieP, roughness: 0.75 }), sideMat("#6a40ab")],
        sleeve: "#7b4fc0", sleeveFrac: 0.16,
        pants: "#1f1f26", shoes: "#f2f2f2",
      },
    },
  });
  const phone = new THREE.Group();
  const ph = box(0.42, 0.75, 0.08, std("#15151a", { roughness: 0.3 }), 0.04);
  phone.add(ph);
  const scr = mesh(new THREE.PlaneGeometry(0.36, 0.66), new THREE.MeshStandardMaterial({ map: T.phoneScreen(), emissive: "#ffffff", emissiveMap: T.phoneScreen(), emissiveIntensity: 1.2 }), { cast: false });
  scr.position.z = 0.045;
  phone.add(scr);
  sister.phone = phone;
  const cardiganG = T.knit({ colors: ["#e58fb0", "#d97ea0", "#efa2c0", "#d97ea0"], band: 3, repeat: [1, 1] });
  const grandma = makeAvatar({
    name: "grandma",
    skin: "#f1c9a8",
    face: "momSmile",
    hair: grandmaHair,
    outfits: {
      cardigan: {
        torso: [std(0xffffff, { map: cardiganG, roughness: 0.9 }), std(0xffffff, { map: cardiganG, roughness: 0.9 }), std("#e58fb0"), std("#e58fb0"), std(0xffffff, { map: cardiganG, roughness: 0.9 }), std(0xffffff, { map: cardiganG, roughness: 0.9 })],
        sleeve: "#e58fb0", sleeveFrac: 0.18,
        pants: "#8a7ab0", shoes: "#5a4a6a",
      },
    },
  });
  // the thing in the closet: Mom's hair, Mom's scrubs, Mom's smile, all stretched wrong
  const pale = "#d4beac";
  const mimic = makeAvatar({
    name: "mimic",
    skin: pale,
    face: "mimic",
    hair: momHair,
    outfits: {
      scrubs: {
        torso: [sideMat("#2f9e9a"), sideMat("#2f9e9a"), sideMat("#2f9e9a"), sideMat("#2f9e9a"), std(0xffffff, { map: scrubs, roughness: 0.7 }), sideMat("#2f9e9a")],
        sleeve: "#2f9e9a", sleeveFrac: 0.52,
        pants: "#2f9e9a", shoes: pale, shoeFrac: 0.3,
      },
    },
  });
  {
    const J = mimic.j;
    J.legL.scale.y = J.legR.scale.y = 1.85;
    J.torsoM.scale.y = 1.4;
    J.torsoM.position.y = 1.4;
    for (const a of [J.armL, J.armR]) {
      a.scale.y = 1.95;
      a.position.y = 2.8 - 0.5 * 1.95;
    }
    const neck = box(0.5, 0.9, 0.5, std(pale, { roughness: 0.5 }), 0.1);
    neck.position.y = 3.05;
    J.torso.add(neck);
    J.head.position.y = 3.3;
    J.head.scale.set(1, 1.1, 1);
    mimic.hipY = 2 * 1.85;
    // long pale fingers (inside the stretched arm, so they come out long too)
    mimic.fingers = { L: [], R: [] };
    const fm = std(pale, { roughness: 0.5 });
    for (const side of ["L", "R"]) {
      for (let f = 0; f < 4; f++) {
        const fg = new THREE.Group();
        fg.position.set(-0.33 + f * 0.22, -0.02, 0.12);
        const m = box(0.13, 0.5, 0.15, fm, 0.05);
        m.position.y = -0.25;
        fg.add(m);
        J["hand" + side].add(fg);
        mimic.fingers[side].push(fg);
      }
    }
  }
  return { kid, mom, dad, sister, grandma, mimic, dog: makeDog() };
}

// ---------------------------------------------------------------------------
function makeDog() {
  const root = new THREE.Group();
  const gold = std("#d39a3e", { roughness: 0.8 });
  const light = std("#ecc890", { roughness: 0.8 });
  const brown = std("#9a6428", { roughness: 0.8 });
  const body = new THREE.Group();
  body.position.y = 1.35;
  root.add(body);
  const torso = box(1.3, 1.1, 2.3, gold, 0.18);
  body.add(torso);
  const belly = box(1.0, 0.3, 1.8, light, 0.12);
  belly.position.set(0, -0.45, 0);
  body.add(belly);
  const collar = box(1.0, 0.25, 0.3, std("#c0302b"), 0.06);
  collar.position.set(0, 0.35, 1.05);
  body.add(collar);
  const head = new THREE.Group();
  head.position.set(0, 0.75, 1.15);
  body.add(head);
  const headM = box(1.15, 1.05, 1.0, gold, 0.18);
  headM.position.set(0, 0.25, 0.2);
  head.add(headM);
  const snout = box(0.66, 0.46, 0.55, light, 0.12);
  snout.position.set(0, 0.02, 0.85);
  head.add(snout);
  const nose = box(0.28, 0.2, 0.14, std("#1b1410", { roughness: 0.3 }), 0.06);
  nose.position.set(0, 0.15, 1.13);
  head.add(nose);
  const faceP = mesh(new THREE.PlaneGeometry(1.0, 0.9),
    new THREE.MeshStandardMaterial({ map: T.dogFace(), transparent: true, alphaTest: 0.3, roughness: 0.5 }), { cast: false });
  faceP.position.set(0, 0.3, 0.705);
  head.add(faceP);
  const ears = [];
  for (const side of [-1, 1]) {
    const ear = new THREE.Group();
    ear.position.set(side * 0.58, 0.68, 0.2);
    const m = box(0.18, 0.7, 0.5, brown, 0.08);
    m.position.y = -0.3;
    ear.add(m);
    ear.rotation.z = side * 0.25;
    head.add(ear);
    ears.push(ear);
  }
  const legs = [];
  for (const [x, z] of [[-0.42, 0.75], [0.42, 0.75], [-0.42, -0.75], [0.42, -0.75]]) {
    const leg = new THREE.Group();
    leg.position.set(x, -0.35, z);
    const m = box(0.36, 1.0, 0.36, gold, 0.08);
    m.position.y = -0.5;
    leg.add(m);
    const paw = box(0.4, 0.18, 0.46, light, 0.06);
    paw.position.set(0, -0.95, 0.04);
    leg.add(paw);
    body.add(leg);
    legs.push(leg);
  }
  const tail = new THREE.Group();
  tail.position.set(0, 0.35, -1.12);
  const tm = box(0.22, 0.22, 0.9, gold, 0.08);
  tm.position.z = -0.4;
  tail.add(tm);
  tail.rotation.x = 0.7;
  body.add(tail);
  return {
    name: "dog",
    root,
    j: { body, head, ears, legs, tail },
    reset() {
      root.visible = false;
      root.position.set(0, 0, 0);
      root.rotation.set(0, 0, 0);
      body.position.set(0, 1.35, 0);
      body.rotation.set(0, 0, 0);
      head.rotation.set(0, 0, 0);
      tail.rotation.set(0.7, 0, 0);
      legs.forEach((l) => l.rotation.set(0, 0, 0));
      ears.forEach((e, i) => e.rotation.set(0, 0, (i ? 1 : -1) * 0.25));
    },
  };
}

// ---------------------------------------------------------------------------
function makeCounter() {
  const root = new THREE.Group();
  const coat = std("#1b1b22", { roughness: 0.85 });
  const coatEdge = std("#26262f", { roughness: 0.8 });
  const paleSkin = std("#d6d3ca", { roughness: 0.55 });
  const bone = std("#efebe0", { roughness: 0.38 });
  const ink = std("#0d0b0a", { roughness: 0.25 });

  const pelvis = new THREE.Group();
  pelvis.position.y = 6.2;
  root.add(pelvis);
  const j = { pelvis, fingers: { L: [], R: [] } };

  const skirt = box(2.5, 3.4, 1.35, coat, 0.12);
  skirt.position.y = -1.3;
  pelvis.add(skirt);
  for (const side of [-1, 1]) {
    const k = side < 0 ? "L" : "R";
    const thigh = new THREE.Group();
    thigh.position.set(side * 0.55, 0, 0);
    const tm = box(0.62, 3.1, 0.62, coat, 0.1);
    tm.position.y = -1.5;
    thigh.add(tm);
    pelvis.add(thigh);
    const shin = new THREE.Group();
    shin.position.y = -3.0;
    const sm = box(0.52, 3.0, 0.52, coatEdge, 0.1);
    sm.position.y = -1.5;
    shin.add(sm);
    const shoe = box(0.62, 0.3, 1.1, ink, 0.1);
    shoe.position.set(0, -3.05, 0.22);
    shin.add(shoe);
    thigh.add(shin);
    j["thigh" + k] = thigh;
    j["shin" + k] = shin;
  }
  const torso = new THREE.Group();
  pelvis.add(torso);
  const chest = box(2.4, 4.5, 1.3, coat, 0.14);
  chest.position.y = 2.2;
  torso.add(chest);
  const lapel = box(0.5, 2.6, 0.08, coatEdge, 0.03);
  lapel.position.set(0, 3.1, 0.66);
  torso.add(lapel);
  j.torso = torso;

  const neck = new THREE.Group();
  neck.position.y = 4.4;
  torso.add(neck);
  const nm = box(0.42, 1.1, 0.42, paleSkin, 0.08);
  nm.position.y = 0.5;
  neck.add(nm);
  j.neck = neck;
  const head = new THREE.Group();
  head.position.y = 1.0;
  neck.add(head);
  const headM = box(1.95, 1.95, 1.95, bone, 0.28);
  headM.position.y = 0.95;
  head.add(headM);
  j.head = head;
  // six eyes, like the six face of a die
  const eyeGeo = new THREE.CylinderGeometry(0.19, 0.19, 0.06, 24);
  const glintMat = new THREE.MeshStandardMaterial({ color: "#ffffff", emissive: "#ffffff", emissiveIntensity: 1.6 });
  const glintGeo = new THREE.SphereGeometry(0.045, 10, 8);
  const eyes = [];
  for (const x of [-0.45, 0.45]) {
    for (const y of [1.55, 0.95, 0.35]) {
      const e = new THREE.Group();
      e.position.set(x, y, 0.985);
      const disc = mesh(eyeGeo, ink, { cast: false });
      disc.rotation.x = Math.PI / 2;
      e.add(disc);
      const gl = mesh(glintGeo, glintMat, { cast: false });
      gl.position.set(0.07, 0.07, 0.04);
      e.add(gl);
      head.add(e);
      eyes.push(e);
    }
  }
  j.eyes = eyes;

  for (const side of [-1, 1]) {
    const k = side < 0 ? "L" : "R";
    const upper = new THREE.Group();
    upper.position.set(side * 1.45, 4.1, 0);
    const um = box(0.6, 2.9, 0.6, coat, 0.1);
    um.position.y = -1.35;
    upper.add(um);
    torso.add(upper);
    const fore = new THREE.Group();
    fore.position.y = -2.75;
    const cuff = box(0.64, 0.4, 0.64, coatEdge, 0.08);
    cuff.position.y = -0.1;
    fore.add(cuff);
    const fm = box(0.4, 2.6, 0.4, paleSkin, 0.08);
    fm.position.y = -1.4;
    fore.add(fm);
    upper.add(fore);
    const hand = new THREE.Group();
    hand.position.y = -2.7;
    const hm = box(0.5, 0.55, 0.22, paleSkin, 0.06);
    hm.position.y = -0.2;
    hand.add(hm);
    for (let f = 0; f < 4; f++) {
      const fg = new THREE.Group();
      fg.position.set(-0.18 + f * 0.12, -0.46, 0);
      const fmm = box(0.1, 1.05 - Math.abs(f - 1.5) * 0.12, 0.12, paleSkin, 0.04);
      fmm.position.y = -0.48;
      fg.add(fmm);
      hand.add(fg);
      j.fingers[k].push(fg);
    }
    const thumb = new THREE.Group();
    thumb.position.set(-side * 0.28, -0.25, 0.05);
    const tmm = box(0.1, 0.6, 0.12, paleSkin, 0.04);
    tmm.position.y = -0.28;
    thumb.add(tmm);
    thumb.rotation.z = side * 0.6;
    hand.add(thumb);
    fore.add(hand);
    j["upper" + k] = upper;
    j["fore" + k] = fore;
    j["hand" + k] = hand;
  }

  const c = {
    name: "counter",
    root,
    j,
    // wide: 1 normal, >1 eyes widen; blink: 0 open, 1 shut
    setEyes(wide = 1, blink = 0, jitter = 0) {
      eyes.forEach((e, i) => {
        const s = wide * (1 + jitter * Math.sin(i * 2.1));
        e.scale.set(s, s * Math.max(0.06, 1 - blink), s);
      });
    },
    reset() {
      root.visible = false;
      root.position.set(0, 0, 0);
      root.rotation.set(0, 0, 0);
      pelvis.position.set(0, 6.2, 0);
      pelvis.rotation.set(0, 0, 0);
      for (const k of ["torso", "neck", "head", "thighL", "thighR", "shinL", "shinR", "upperL", "upperR", "foreL", "foreR", "handL", "handR"])
        j[k].rotation.set(0, 0, 0);
      j.upperL.rotation.z = -0.06;
      j.upperR.rotation.z = 0.06;
      for (const k of ["L", "R"]) j.fingers[k].forEach((f) => f.rotation.set(0, 0, 0));
      this.setEyes(1, 0);
    },
  };
  return c;
}
