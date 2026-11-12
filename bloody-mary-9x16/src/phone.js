// A smartphone prop whose screen is a canvas redrawn from a plain state object (seek-safe:
// the same state always draws the same pixels). Screens: map, msgs, call, lock, off.
import * as THREE from "three";
import { box, std } from "./chars.js";
import { rng, clamp, lerp } from "./util.js";

export const CW = 600, CH = 1268;
const F = (w, s) => `${w} ${s}px Poppins, sans-serif`;
const TEAL = "#2f9e9a", BLUE = "#2f7cf6";

export function makePhone(scene, { caseColor = "#1d1f26", gripSkin = "#f0c39b", gripSleeve = "#7fa7d9", long = false } = {}) {
  const group = new THREE.Group();
  const body = box(0.56, 1.18, 0.07, std(caseColor, { roughness: 0.35, metalness: 0.4 }), 0.03);
  group.add(body);
  const c = document.createElement("canvas");
  c.width = CW;
  c.height = CH;
  const g = c.getContext("2d");
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 8;
  const mat = new THREE.MeshBasicMaterial({ map: tex });
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(0.5, (0.5 * CH) / CW), mat);
  screen.position.z = 0.037;
  group.add(screen);
  // a blocky hand holding the phone from behind: thumb on the left edge, fingers wrapping the right
  const grip = new THREE.Group();
  const skin = std(gripSkin, { roughness: 0.55 });
  const palm = box(0.5, 0.6, 0.2, skin, 0.08);
  palm.position.set(0.02, -0.3, -0.15);
  grip.add(palm);
  const thumb = box(0.13, long ? 0.62 : 0.34, 0.12, skin, 0.05);
  thumb.position.set(-0.31, -0.24, 0.05);
  thumb.rotation.z = -0.12;
  grip.add(thumb);
  grip.userData.thumb = thumb;
  for (let f = 0; f < 3; f++) {
    const fl = long ? 0.5 : 0.1;
    const fg = box(fl, 0.12, long ? 0.12 : 0.14, skin, 0.04);
    fg.position.set(long ? 0.28 + fl / 2 - 0.06 : 0.31, -0.12 - f * 0.17, long ? 0.0 : -0.01);
    if (long) fg.rotation.z = -0.25 - f * 0.12;
    grip.add(fg);
  }
  const sleeve = box(0.62, 0.9, 0.5, std(gripSleeve, { roughness: 0.85 }), 0.1);
  sleeve.position.set(0.1, long ? -1.15 : -1.0, long ? -0.8 : -0.55);
  sleeve.rotation.x = long ? 1.25 : 0.9;
  sleeve.visible = !long;
  grip.add(sleeve);
  grip.visible = false;
  group.add(grip);
  scene.add(group);
  let last = "";
  return {
    group,
    grip,
    screen,
    mat,
    draw(state) {
      const key = JSON.stringify(state);
      if (key === last) return;
      last = key;
      g.save();
      render(g, state);
      g.restore();
      tex.needsUpdate = true;
    },
  };
}

function render(g, s) {
  if (s.screen === "map") drawMap(g, s);
  else if (s.screen === "msgs") drawMsgs(g, s);
  else if (s.screen === "call") drawCall(g, s);
  else if (s.screen === "lock") drawLock(g, s);
  else {
    g.fillStyle = "#000";
    g.fillRect(0, 0, CW, CH);
  }
}

// ---- primitives --------------------------------------------------------------
function rr(g, x, y, w, h, r) {
  r = Math.min(r, w / 2, h / 2);
  g.beginPath();
  g.moveTo(x + r, y);
  g.arcTo(x + w, y, x + w, y + h, r);
  g.arcTo(x + w, y + h, x, y + h, r);
  g.arcTo(x, y + h, x, y, r);
  g.arcTo(x, y, x + w, y, r);
  g.closePath();
}
function circle(g, x, y, r, fill) {
  g.fillStyle = fill;
  g.beginPath();
  g.arc(x, y, r, 0, Math.PI * 2);
  g.fill();
}
function text(g, str, x, y, { font = F(700, 30), color = "#fff", align = "left", base = "middle", alpha = 1 } = {}) {
  g.globalAlpha = alpha;
  g.font = font;
  g.fillStyle = color;
  g.textAlign = align;
  g.textBaseline = base;
  g.fillText(str, x, y);
  g.globalAlpha = 1;
}
function avatar(g, x, y, r, letter, fill = TEAL) {
  circle(g, x, y, r, fill);
  text(g, letter, x, y + r * 0.06, { font: F(800, Math.round(r * 1.05)), align: "center" });
}
function statusBar(g, time = "2:14", color = "#fff") {
  text(g, time, 54, 46, { font: F(700, 30), color });
  g.fillStyle = color;
  for (let i = 0; i < 4; i++) g.fillRect(420 + i * 13, 56 - (i + 1) * 7, 9, (i + 1) * 7);
  g.strokeStyle = color;
  g.lineWidth = 3;
  rr(g, 488, 34, 54, 25, 7);
  g.stroke();
  g.fillRect(493, 39, 32, 15);
  g.fillRect(544, 41, 4, 11);
}
function wrap(g, str, maxW) {
  const words = str.split(" ");
  const lines = [];
  let cur = "";
  for (const w of words) {
    const t = cur ? cur + " " + w : w;
    if (g.measureText(t).width > maxW && cur) {
      lines.push(cur);
      cur = w;
    } else cur = t;
  }
  if (cur) lines.push(cur);
  return lines;
}

// ---- map ---------------------------------------------------------------------
// house plan in map units, house centred on (0,0), 72 x 48
const ROOMS = [
  ["KITCHEN", -36, 0, 30, 24],
  ["LIVING", -36, -24, 30, 24],
  ["BATH", 4, 8, 20, 16],
  ["BEDROOM", 4, -24, 32, 32],
  ["CLOSET", 24, 8, 12, 16],
];
export const PLAN = { closet: [30, 16], bedroom: [16, -8], home: [0, 0] };
let mapCache = null;
function mapBase() {
  if (mapCache) return mapCache;
  const r = rng(5);
  const houses = [];
  for (let gx = -6; gx <= 6; gx++)
    for (let gy = -7; gy <= 7; gy++) {
      if (gx === 0 && gy === 0) continue;
      houses.push([gx * 100 + (r() - 0.5) * 16, gy * 92 + (r() - 0.5) * 12, 44 + r() * 26, 30 + r() * 18]);
    }
  mapCache = { houses };
  return mapCache;
}
function drawMap(g, s) {
  const z = clamp(s.zoom ?? 0);
  const sc = 1.15 * Math.pow(7.2, z);
  const cx = 300, cy = 540;
  g.fillStyle = "#0c1320";
  g.fillRect(0, 0, CW, CH);
  g.save();
  g.translate(cx, cy);
  g.scale(sc, sc);
  // park + water
  g.fillStyle = "#0f2a1c";
  g.fillRect(150, -340, 210, 190);
  g.fillStyle = "#0d2238";
  g.beginPath();
  g.moveTo(-600, 300);
  g.bezierCurveTo(-300, 260, -200, 520, 200, 470);
  g.lineTo(200, 560);
  g.lineTo(-600, 560);
  g.fill();
  // houses
  g.fillStyle = "#16233a";
  for (const [x, y, w, h] of mapBase().houses) g.fillRect(x - w / 2, y - h / 2, w, h);
  // streets
  g.fillStyle = "#24344d";
  for (let k = -4; k <= 4; k++) {
    g.fillRect(-900, 60 + k * 184 - 13, 1800, 26);
    g.fillRect(-120 + k * 230 - 13, -900, 26, 1800);
  }
  g.strokeStyle = "#33496a";
  g.lineWidth = 40;
  g.beginPath();
  g.moveTo(-520, 420);
  g.bezierCurveTo(-200, 120, 160, 160, 560, -560);
  g.stroke();
  // home
  g.fillStyle = "#1d3a63";
  g.fillRect(-36, -24, 72, 48);
  g.strokeStyle = "rgba(90,162,255,0.85)";
  g.lineWidth = 2.2 / Math.sqrt(sc);
  g.strokeRect(-36, -24, 72, 48);
  g.restore();
  // floor plan fades in when zoomed
  const fp = clamp((z - 0.45) / 0.35);
  if (fp > 0) {
    g.save();
    g.globalAlpha = fp;
    g.translate(cx, cy);
    g.scale(sc, sc);
    g.strokeStyle = "rgba(220,235,255,0.9)";
    g.lineWidth = 0.55;
    for (const [, x, y, w, h] of ROOMS) g.strokeRect(x, y, w, h);
    g.fillStyle = "rgba(40,90,150,0.25)";
    g.fillRect(4, -24, 32, 32);
    g.fillStyle = "rgba(60,180,170,0.28)";
    g.fillRect(24, 8, 12, 16);
    g.restore();
    for (const [name, x, y, w, h] of ROOMS)
      text(g, name, cx + (x + w / 2) * sc, cy + (y + h / 2) * sc + (name === "CLOSET" ? -sc * 5.5 : 0), {
        font: F(800, name === "CLOSET" ? 26 : 22), color: name === "CLOSET" ? "#bff3ee" : "#9fb4d4", align: "center", alpha: fp * 0.95,
      });
  }
  // pins
  const ph = ((s.ph ?? 0) % 1 + 1) % 1;
  const me = s.me || PLAN.bedroom;
  const mx = cx + me[0] * sc * fp + (1 - fp) * -18, my = cy + me[1] * sc * fp + (1 - fp) * 6;
  if (s.showMe !== false) {
    circle(g, mx, my, 16 + ph * 34, `rgba(47,124,246,${0.45 * (1 - ph)})`);
    circle(g, mx, my, 21, "#fff");
    circle(g, mx, my, 15, BLUE);
  }
  const mom = s.mom || PLAN.home;
  const px = cx + mom[0] * sc, py = cy + mom[1] * sc;
  circle(g, px, py, 14 + ph * 44, `rgba(47,158,154,${0.55 * (1 - ph)})`);
  circle(g, px, py, 9, TEAL);
  g.fillStyle = "#fff";
  g.beginPath();
  g.moveTo(px - 16, py - 50);
  g.lineTo(px + 16, py - 50);
  g.lineTo(px, py - 14);
  g.fill();
  circle(g, px, py - 70, 40, "#fff");
  avatar(g, px, py - 70, 33, "M");
  // header
  const hg = g.createLinearGradient(0, 0, 0, 190);
  hg.addColorStop(0, "rgba(12,19,32,1)");
  hg.addColorStop(1, "rgba(12,19,32,0)");
  g.fillStyle = hg;
  g.fillRect(0, 0, CW, 190);
  statusBar(g, s.time || "2:14");
  text(g, "People", 40, 124, { font: F(800, 50) });
  // bottom sheet
  g.fillStyle = "#151b27";
  rr(g, 0, 930, CW, 420, 40);
  g.fill();
  g.fillStyle = "#3a4458";
  rr(g, 270, 950, 60, 9, 4);
  g.fill();
  avatar(g, 96, 1044, 52, "M");
  text(g, "Mom", 172, 1018, { font: F(800, 50) });
  text(g, s.where || "Home · Now", 172, 1074, { font: F(700, 31), color: "#9aa7bb" });
  text(g, s.dist || "", 560, 1020, { font: F(800, 36), color: s.distColor || "#5aa2ff", align: "right" });
  for (const [x, label] of [[40, "Contact"], [312, "Directions"]]) {
    g.fillStyle = "#222b3b";
    rr(g, x, 1128, 248, 80, 22);
    g.fill();
    text(g, label, x + 124, 1169, { font: F(700, 32), color: "#5aa2ff", align: "center" });
  }
}

// ---- messages ----------------------------------------------------------------
// items: {t:'day', text} | {t:'me'|'them', text, k} | {t:'typing', k} | {t:'note', text}
function drawMsgs(g, s) {
  g.fillStyle = "#000";
  g.fillRect(0, 0, CW, CH);
  const ph = ((s.ph ?? 0) % 1 + 1) % 1;
  // content
  g.save();
  g.beginPath();
  g.rect(0, 250, CW, 892);
  g.clip();
  let y = 1124 + (s.scroll || 0);
  g.font = F(700, 40);
  const items = s.items || [];
  for (let i = items.length - 1; i >= 0; i--) {
    const it = items[i];
    const k = it.k ?? 1;
    if (it.t === "day") {
      y -= 46;
      text(g, it.text, 300, y + 18, { font: F(700, 25), color: "#8e8e93", align: "center" });
      y -= 18;
    } else if (it.t === "note") {
      y -= 34;
      text(g, it.text, 568, y + 14, { font: F(700, 24), color: "#8e8e93", align: "right", alpha: k });
      y -= 2;
    } else if (it.t === "typing") {
      const w = 132, h = 82;
      y -= h;
      g.save();
      g.translate(30, y + h);
      g.scale(k, k);
      g.fillStyle = "#2b2b2e";
      rr(g, 0, -h, w, h, 38);
      g.fill();
      for (let d = 0; d < 3; d++) {
        const a = 0.35 + 0.65 * Math.max(0, Math.sin((ph - d * 0.18) * Math.PI * 2));
        circle(g, 34 + d * 32, -h / 2, 11, `rgba(200,200,205,${a})`);
      }
      g.restore();
      y -= 16;
    } else {
      g.font = F(700, 40);
      const lines = wrap(g, it.text, 420);
      const w = Math.max(...lines.map((l) => g.measureText(l).width)) + 54;
      const h = lines.length * 52 + 34;
      y -= h;
      const me = it.t === "me";
      const x = me ? 572 - w : 28;
      g.save();
      g.translate(me ? 572 : 28, y + h);
      g.scale(k, k);
      g.translate(-(me ? 572 : 28), -(y + h));
      g.globalAlpha = clamp(k * 1.5);
      g.fillStyle = me ? BLUE : "#2b2b2e";
      rr(g, x, y, w, h, 36);
      g.fill();
      lines.forEach((l, j) => text(g, l, x + 27, y + 17 + 26 + j * 52, { font: F(700, 40) }));
      g.restore();
      y -= 14;
    }
  }
  g.restore();
  // header over content
  g.fillStyle = "rgba(18,18,20,0.97)";
  g.fillRect(0, 0, CW, 250);
  g.fillStyle = "#26262a";
  g.fillRect(0, 249, CW, 2);
  statusBar(g, s.time || "2:14");
  g.strokeStyle = "#3b8bff";
  g.lineWidth = 7;
  g.lineCap = "round";
  g.beginPath();
  g.moveTo(52, 112);
  g.lineTo(32, 136);
  g.lineTo(52, 160);
  g.stroke();
  avatar(g, 300, 132, 50, s.initial || "M", s.avatarColor || TEAL);
  text(g, (s.name || "Mom") + "  ›", 300, 214, { font: F(700, 30), align: "center" });
  // input bar
  g.fillStyle = "#000";
  g.fillRect(0, 1142, CW, CH - 1142);
  circle(g, 52, 1200, 30, "#2c2c2e");
  text(g, "+", 52, 1202, { font: F(700, 44), color: "#b9b9bf", align: "center" });
  g.strokeStyle = "#3a3a3c";
  g.lineWidth = 3;
  rr(g, 100, 1166, 472, 68, 34);
  g.stroke();
  if (s.draft) {
    g.font = F(700, 34);
    let d = s.draft;
    while (g.measureText(d).width > 360) d = d.slice(1);
    text(g, d, 126, 1201, { font: F(700, 34) });
    if (Math.floor((s.ph ?? 0) * 2) % 2 === 0) {
      g.fillStyle = "#3b8bff";
      g.fillRect(130 + g.measureText(d).width, 1182, 4, 40);
    }
    circle(g, 535, 1200, 26, BLUE);
    g.strokeStyle = "#fff";
    g.lineWidth = 6;
    g.beginPath();
    g.moveTo(535, 1214);
    g.lineTo(535, 1186);
    g.moveTo(524, 1196);
    g.lineTo(535, 1185);
    g.lineTo(546, 1196);
    g.stroke();
  } else text(g, "Text Message", 126, 1201, { font: F(700, 32), color: "#6c6c70" });
}

// ---- incoming / active call ---------------------------------------------------
function handset(g, x, y, s, rot) {
  g.save();
  g.translate(x, y);
  g.rotate(rot);
  g.scale(s, s);
  g.fillStyle = "#fff";
  rr(g, -26, -8, 52, 16, 8);
  g.fill();
  rr(g, -30, -8, 16, 22, 6);
  g.fill();
  rr(g, 14, -8, 16, 22, 6);
  g.fill();
  g.restore();
}
function drawCall(g, s) {
  const bg = g.createLinearGradient(0, 0, 0, CH);
  bg.addColorStop(0, "#26383f");
  bg.addColorStop(1, "#090d10");
  g.fillStyle = bg;
  g.fillRect(0, 0, CW, CH);
  statusBar(g, s.time || "2:15");
  const ph = ((s.ph ?? 0) % 1 + 1) % 1;
  text(g, "County General", 300, 286, { font: F(800, 54), align: "center" });
  text(g, "Hospital", 300, 352, { font: F(800, 54), align: "center" });
  text(g, s.active ? `00:0${Math.min(9, Math.floor(s.secs || 0))}` : "incoming call…", 300, 420, { font: F(700, 32), color: "#b8c6cc", align: "center" });
  circle(g, 300, 640, 118, "#3b4d55");
  circle(g, 300, 640, 74, "#d94b4b");
  g.fillStyle = "#fff";
  g.fillRect(286, 594, 28, 92);
  g.fillRect(254, 626, 92, 28);
  if (!s.active) {
    circle(g, 150, 1060, 64, "#e5484d");
    handset(g, 150, 1060, 1.1, Math.PI * 0.75);
    circle(g, 450, 1060, 64 + ph * 30, `rgba(52,199,89,${0.5 * (1 - ph)})`);
    circle(g, 450, 1060, 64, "#34c759");
    handset(g, 450, 1056, 1.1, 0);
    text(g, "Decline", 150, 1162, { font: F(700, 30), align: "center" });
    text(g, "Accept", 450, 1162, { font: F(700, 30), align: "center" });
  } else {
    ["mute", "keypad", "speaker"].forEach((l, i) => {
      circle(g, 130 + i * 170, 860, 54, "#33424a");
      text(g, l, 130 + i * 170, 944, { font: F(700, 26), color: "#c9d3d7", align: "center" });
    });
    circle(g, 300, 1090, 64, "#e5484d");
    handset(g, 300, 1090, 1.1, Math.PI * 0.75);
  }
}

// ---- lock screen with a notification ----------------------------------------------
function drawLock(g, s) {
  const bg = g.createLinearGradient(0, 0, 0, CH);
  bg.addColorStop(0, "#1a2140");
  bg.addColorStop(0.6, "#2b1c3a");
  bg.addColorStop(1, "#0b0b12");
  g.fillStyle = bg;
  g.fillRect(0, 0, CW, CH);
  statusBar(g, "");
  text(g, "Wednesday, November 11", 300, 190, { font: F(700, 30), color: "#d9dcf0", align: "center" });
  text(g, s.time || "2:17", 300, 318, { font: F(800, 170), color: "#eef0ff", align: "center" });
  const k = clamp(s.notif ?? 0);
  if (k > 0) {
    g.save();
    g.globalAlpha = clamp(k * 1.4);
    g.translate(0, (1 - k) * 60);
    g.fillStyle = "rgba(48,48,58,0.92)";
    rr(g, 26, 470, 548, s.msg2 ? 228 : 190, 34);
    g.fill();
    g.fillStyle = s.appColor || "#34c759";
    rr(g, 52, 498, 54, 54, 14);
    g.fill();
    g.fillStyle = "#fff";
    if (s.app) text(g, s.appLetter || "N", 79, 526, { font: F(800, 34), align: "center" });
    else {
      g.beginPath();
      g.ellipse(79, 523, 17, 13, 0, 0, Math.PI * 2);
      g.fill();
    }
    text(g, s.app || "MESSAGES", 124, 526, { font: F(700, 24), color: "#c8c8d0" });
    text(g, "now", 548, 526, { font: F(700, 24), color: "#c8c8d0", align: "right" });
    text(g, s.title || "Mom", 52, 586, { font: F(800, 36) });
    text(g, s.msg || "", 52, 630, { font: F(700, 31), color: "#ececf2" });
    if (s.msg2) text(g, s.msg2, 52, 668, { font: F(700, 31), color: "#ececf2" });
    g.restore();
  }
  text(g, "swipe up to open", 300, 1210, { font: F(700, 24), color: "rgba(220,220,235,0.55)", align: "center" });
}

