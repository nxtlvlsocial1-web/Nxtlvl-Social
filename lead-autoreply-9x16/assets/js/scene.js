// samarpit.ai "Wed · System Build: lead auto-reply" (9:16). The whole 3D scene is a pure function of time t, rendered on
// HyperFrames' hf-seek, so every frame is exact. Beats come from window.LR_T (written by build/generate.py from the
// voice's word timings). HTML labels that sit on 3D objects are projected from 3D each frame.
//   hook:  a phone at night (11:02 PM enquiry), the clock time-lapses to 10:04 AM, the late reply, "already booked"
//   l01:   the clock rewinds to 11:02 PM and an instant reply lands in the same minute
//   l02:   four glass boxes drop into a column joined by glass tubes
//   steps: the camera rides the lead (an amber orb) down box by box: form card in, sheet row, reply parts, phone buzz
//   live:  pull back, the orb races through all four, the phone flies in with the reply already there
//   end:   the column keeps running under a moving moon; the CTA
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";

const W = 1080, H = 1920;
const T = window.LR_T;
const STEEL = 0x5b8cff, AMBER = 0xffb020, CORAL = 0xff5a36;
const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(34, W / H, .1, 120);
scene.add(camera);                                                   // the phone and clock ride the camera
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), .04).texture;
scene.environmentIntensity = .35;
scene.fog = new THREE.Fog(0x060810, 16, 40);

// night sky: a vertical gradient behind everything
{
  const c = document.createElement("canvas"); c.width = 4; c.height = 512;
  const g = c.getContext("2d"), gr = g.createLinearGradient(0, 0, 0, 512);
  gr.addColorStop(0, "#03050a"); gr.addColorStop(.55, "#081022"); gr.addColorStop(1, "#05070d");
  g.fillStyle = gr; g.fillRect(0, 0, 4, 512);
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; scene.background = tx;
}

const composer = new EffectComposer(renderer);
composer.setSize(W, H);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), .75, .5, .58);
composer.addPass(bloom);
composer.addPass(new OutputPass());

scene.add(new THREE.HemisphereLight(0xb8c8ff, 0x080a12, .55));
const key = new THREE.DirectionalLight(0xffffff, 1.6); key.position.set(4, 6, 7); scene.add(key);
const rimS = new THREE.PointLight(STEEL, 26, 16); rimS.position.set(-4, 2, 3); scene.add(rimS);
const rimA = new THREE.PointLight(AMBER, 0, 16); scene.add(rimA);

// ---------------------------------------------------------------- helpers
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const win = (t, a, b) => clamp((t - a) / (b - a));
const ease = (x) => 1 - Math.pow(1 - clamp(x), 3);
const easeIO = (x) => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const back = (x) => { x = clamp(x); const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const lerp = (a, b, x) => a + (b - a) * x;
const pulse = (t, at, w = .25) => Math.exp(-Math.pow((t - at) / w, 2));
const rnd = (i, k = 1) => { const s = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return s - Math.floor(s); };
const v3 = new THREE.Vector3();
const $ = (id) => document.getElementById(id);
function project(obj, local, el, dx = 0, dy = 0, a = null) {         // glue an HTML label to a point on a 3D object
  if (!el) return;
  v3.copy(local); obj.localToWorld(v3); v3.project(camera);
  el.style.transform = `translate(${(v3.x * .5 + .5) * W + dx}px, ${(-v3.y * .5 + .5) * H + dy}px) translate(-50%, -50%)`;
  if (a !== null) el.style.opacity = a;
}
function rr(g, x, y, w, h, r) { g.beginPath(); g.roundRect(x, y, w, h, r); }
function canvasTex(w, h) {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 4;
  return { c, g: c.getContext("2d"), tx };
}
function wrap(g, text, maxW) {
  const out = []; let line = "";
  for (const w of text.split(" ")) { const tst = line ? line + " " + w : w; if (g.measureText(tst).width > maxW && line) { out.push(line); line = w; } else line = tst; }
  if (line) out.push(line); return out;
}
const fmt = (m) => { m = ((Math.round(m) % 1440) + 1440) % 1440; const h = Math.floor(m / 60), mi = m % 60; return `${(h % 12) || 12}:${String(mi).padStart(2, "0")} ${h < 12 ? "AM" : "PM"}`; };

// ---------------------------------------------------------------- the story clock (minutes since midnight of day 1)
const NIGHT = 23 * 60 + 2, MORNING = 34 * 60 + 4, LATE = 34 * 60 + 9;
function clockMin(t) {
  if (t < T.l01 - .1) {
    let m = lerp(NIGHT, MORNING, easeIO(win(t, T.ten - .85, T.ten + .35)));
    return lerp(m, LATE, easeIO(win(t, T.booked - .5, T.booked + .1)));
  }
  return lerp(LATE, NIGHT + 1440, easeIO(win(t, T.l01 - .1, T.l01 + .55))) - 1440 * (t > T.l01 + .55 ? 1 : 0);
}

// ---------------------------------------------------------------- stars + moon
const SN = 700, sp = new Float32Array(SN * 3);
for (let i = 0; i < SN; i++) {
  const th = rnd(i) * Math.PI * 2, ph = Math.acos(rnd(i, 2) * 1.6 - .6), r = 34 + rnd(i, 3) * 8;
  sp[i * 3] = Math.sin(ph) * Math.cos(th) * r; sp[i * 3 + 1] = Math.cos(ph) * r - 4; sp[i * 3 + 2] = Math.sin(ph) * Math.sin(th) * r;
}
const starGeo = new THREE.BufferGeometry(); starGeo.setAttribute("position", new THREE.BufferAttribute(sp, 3));
const stars = new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xc9d6ff, size: .09, transparent: true, opacity: .8, fog: false, sizeAttenuation: true }));
scene.add(stars);
const moon = new THREE.Mesh(new THREE.SphereGeometry(1, 48, 32), new THREE.MeshBasicMaterial({ color: 0xe9eeff, transparent: true, opacity: 0, fog: false }));
camera.add(moon);
const moonHalo = new THREE.Mesh(new THREE.RingGeometry(1.05, 2.4, 64), new THREE.MeshBasicMaterial({ color: 0x7f9cff, transparent: true, opacity: 0, fog: false, side: THREE.DoubleSide }));
moon.add(moonHalo);

// ---------------------------------------------------------------- the phone (camera-space)
const darkMetal = new THREE.MeshPhysicalMaterial({ color: 0x12161f, metalness: .85, roughness: .22, clearcoat: 1, clearcoatRoughness: .15 });
function makePhone(w, h, cw, ch) {
  const g = new THREE.Group();
  g.add(new THREE.Mesh(new RoundedBoxGeometry(w, h, .16, 6, Math.min(w, h) * .14), darkMetal));
  const scr = canvasTex(cw, ch);
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(w * .9, h * .95), new THREE.MeshBasicMaterial({ map: scr.tx, toneMapped: false, color: 0xd8d8d8 }));
  screen.position.z = .082; g.add(screen);
  const bezel = new THREE.Mesh(new RoundedBoxGeometry(w * .2, .055, .01, 2, .025), new THREE.MeshBasicMaterial({ color: 0x000000 }));
  bezel.position.set(0, h * .44, .09); g.add(bezel);
  for (const [y, l] of [[.22, .28], [-.05, .16]]) {
    const b = new THREE.Mesh(new THREE.BoxGeometry(.03, l * h / 2.9, .06), darkMetal); b.position.set(w / 2 + .01, y * h / 2.9 * 2, 0); g.add(b);
  }
  return { g, scr };
}
const P = makePhone(1.42, 2.88, 560, 1080);
camera.add(P.g);
const phoneGlow = new THREE.PointLight(STEEL, 0, 6); P.g.add(phoneGlow); phoneGlow.position.set(0, 0, 1.2);

// chat bubbles: drawn on the phone's canvas every frame
const BUB = {
  ask: { side: "in", text: "Hi! Are you free this week? How much for a session?" },
  late: { side: "out", text: "Hi! So sorry, just saw this. Yes, we are free!" },
  gone: { side: "in", text: "Thanks, I already booked someone else.", cold: true },
  auto: { side: "auto", text: "Hi Priya! Thanks for reaching out. Here's our price list and a link to book a slot." },
};
function drawChat(sc, items, timeStr, lost, autoTag) {
  const { c, g } = sc, w = c.width, h = c.height;
  g.fillStyle = "#0b0f17"; g.fillRect(0, 0, w, h);
  g.fillStyle = "#e8ecf5"; g.font = "700 30px Mont"; g.textBaseline = "middle";
  g.fillText(timeStr, 34, 42);
  g.fillStyle = "rgba(232,236,245,.75)"; g.fillRect(w - 90, 33, 46, 20); g.fillRect(w - 42, 38, 4, 10);
  // header
  g.fillStyle = "#121826"; g.fillRect(0, 78, w, 124);
  g.fillStyle = "#2b3550"; g.beginPath(); g.arc(74, 140, 38, 0, 7); g.fill();
  g.fillStyle = "#c9d6ff"; g.font = "800 34px Mont"; g.textAlign = "center"; g.fillText("P", 74, 141); g.textAlign = "left";
  g.fillStyle = "#f4f1ea"; g.font = "800 38px Mont"; g.fillText("Priya", 130, 122);
  g.fillStyle = "#8a93a6"; g.font = "700 25px Mont"; g.fillText("Website enquiry", 130, 162);
  let y = 232;
  for (const it of items) {
    if (it.a <= .001) continue;
    const b = BUB[it.k], out = b.side !== "in", auto = b.side === "auto";
    g.font = "700 37px Mont";
    const lines = wrap(g, b.text, w * .74);
    const bw = Math.max(...lines.map((l) => g.measureText(l).width)) + 48;
    let bh = lines.length * 46 + 34 + 30;
    if (auto) bh += 150;
    const x = out ? w - 20 - bw : 20;
    const s = .6 + .4 * back(it.a);
    g.save(); g.globalAlpha = clamp(it.a * 1.6);
    g.translate(out ? x + bw : x, y); g.scale(s, s); g.translate(out ? -(x + bw) : -x, -y);
    g.fillStyle = auto ? "#ffb020" : out ? "#2b6bff" : (b.cold && lost ? "#3a1c18" : "#1d2433");
    rr(g, x, y, bw, bh, 26); g.fill();
    if (b.cold && lost) { g.strokeStyle = "#ff5a36"; g.lineWidth = 3; rr(g, x, y, bw, bh, 26); g.stroke(); }
    g.fillStyle = auto ? "#1a1206" : "#f4f1ea";
    lines.forEach((l, k) => g.fillText(l, x + 24, y + 40 + k * 46));
    let yy = y + 40 + lines.length * 46;
    if (auto) {
      g.fillStyle = "rgba(26,18,6,.14)"; rr(g, x + 18, yy - 4, bw - 36, 62, 14); g.fill();
      g.fillStyle = "#1a1206"; g.font = "800 30px Mont"; g.fillText("Price list.pdf", x + 40, yy + 28);
      g.fillStyle = "#1a1206"; rr(g, x + 18, yy + 72, bw - 36, 62, 31); g.fill();
      g.fillStyle = "#ffb020"; g.textAlign = "center"; g.fillText("Book a slot", x + bw / 2, yy + 104); g.textAlign = "left";
      yy += 150;
    }
    g.fillStyle = auto ? "rgba(26,18,6,.6)" : "rgba(244,241,234,.55)"; g.font = "700 23px Mont";
    const ts = it.time + (auto && autoTag ? "  ·  auto" : "");
    g.fillText(ts, x + bw - 22 - g.measureText(ts).width, yy + 8);
    g.restore();
    y += (bh + 24) * clamp(it.a * 1.4);
  }
  if (lost > .01) {                                                   // the lost lead: a cold red wash
    g.fillStyle = `rgba(255,90,54,${.12 * lost})`; g.fillRect(0, 0, w, h);
  }
  sc.tx.needsUpdate = true;
}

// ---------------------------------------------------------------- the clock (camera-space)
const clock = new THREE.Group(); camera.add(clock);
const clockRimMat = new THREE.MeshStandardMaterial({ color: 0x1b2230, metalness: .8, roughness: .25, emissive: STEEL, emissiveIntensity: .8 });
clock.add(new THREE.Mesh(new THREE.TorusGeometry(.62, .055, 16, 96), clockRimMat));
const face = new THREE.Mesh(new THREE.CircleGeometry(.6, 64), new THREE.MeshStandardMaterial({ color: 0x0c1019, metalness: .3, roughness: .6 }));
face.position.z = -.02; clock.add(face);
for (let k = 0; k < 12; k++) {
  const tk = new THREE.Mesh(new THREE.BoxGeometry(k % 3 ? .02 : .04, k % 3 ? .07 : .12, .02), new THREE.MeshBasicMaterial({ color: 0xa9b6d6 }));
  const a = k / 12 * Math.PI * 2; tk.position.set(Math.sin(a) * .5, Math.cos(a) * .5, .01); tk.rotation.z = -a; clock.add(tk);
}
const handMat = new THREE.MeshStandardMaterial({ color: 0xf4f1ea, emissive: 0xffffff, emissiveIntensity: .3 });
const hourHand = new THREE.Group(), minHand = new THREE.Group();
{ const m = new THREE.Mesh(new THREE.BoxGeometry(.05, .3, .02), handMat); m.position.y = .13; hourHand.add(m); }
{ const m = new THREE.Mesh(new THREE.BoxGeometry(.03, .45, .02), handMat); m.position.y = .2; minHand.add(m); }
hourHand.position.z = .03; minHand.position.z = .045; clock.add(hourHand, minHand);
clock.add(new THREE.Mesh(new THREE.CircleGeometry(.04, 24), handMat)).position.z = .06;

// ---------------------------------------------------------------- the flow: four glass boxes in a zig-zag column
const flow = new THREE.Group(); scene.add(flow);
const GAPY = 1.75, ZIG = [-.55, .55, -.55, .55];
const BOXP = [0, 1, 2, 3].map((k) => new THREE.Vector3(ZIG[k], -k * GAPY, 0));
function iconTex(kind) {
  const { c, g, tx } = canvasTex(256, 256);
  g.clearRect(0, 0, 256, 256); g.strokeStyle = "#f4f1ea"; g.fillStyle = "#f4f1ea"; g.lineWidth = 12; g.lineCap = "round"; g.lineJoin = "round";
  if (kind === 0) {                       // form
    rr(g, 58, 36, 140, 184, 16); g.stroke();
    for (const y of [82, 118, 154]) { g.beginPath(); g.moveTo(86, y); g.lineTo(170, y); g.stroke(); }
    rr(g, 86, 178, 84, 26, 13); g.fill();
  } else if (kind === 1) {                // sheet
    rr(g, 40, 56, 176, 144, 14); g.stroke();
    for (const y of [104, 152]) { g.beginPath(); g.moveTo(40, y); g.lineTo(216, y); g.stroke(); }
    for (const x of [98, 156]) { g.beginPath(); g.moveTo(x, 56); g.lineTo(x, 200); g.stroke(); }
  } else if (kind === 2) {                // reply bubble
    rr(g, 36, 50, 184, 124, 34); g.stroke();
    g.beginPath(); g.moveTo(80, 172); g.lineTo(70, 214); g.lineTo(118, 174); g.stroke();
    for (const x of [92, 128, 164]) { g.beginPath(); g.arc(x, 112, 9, 0, 7); g.fill(); }
  } else {                                // phone alert
    rr(g, 76, 30, 104, 196, 20); g.stroke();
    g.beginPath(); g.moveTo(112, 50); g.lineTo(144, 50); g.stroke();
    g.beginPath(); g.arc(128, 134, 26, Math.PI, 0); g.lineTo(158, 152); g.lineTo(98, 152); g.closePath(); g.fill();
    g.beginPath(); g.arc(128, 162, 8, 0, 7); g.fill();
    g.lineWidth = 8; for (const s of [-1, 1]) { g.beginPath(); g.arc(128, 134, 62, s > 0 ? -.5 : Math.PI - .4, s > 0 ? .4 : Math.PI + .5); g.stroke(); }
  }
  tx.needsUpdate = true; return tx;
}
const boxes = BOXP.map((p, k) => {
  const g = new THREE.Group(); g.position.copy(p); flow.add(g);
  const mat = new THREE.MeshPhysicalMaterial({ color: 0x161c28, metalness: .35, roughness: .18, clearcoat: 1, clearcoatRoughness: .1, emissive: AMBER, emissiveIntensity: 0 });
  const body = new THREE.Mesh(new RoundedBoxGeometry(1.1, 1.1, 1.1, 6, .16), mat); g.add(body);
  const edges = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(1.06, 1.06, 1.06)), new THREE.LineBasicMaterial({ color: STEEL, transparent: true, opacity: .5 }));
  g.add(edges);
  const icon = new THREE.Mesh(new THREE.PlaneGeometry(.66, .66), new THREE.MeshBasicMaterial({ map: iconTex(k), transparent: true, toneMapped: false, color: 0x9fb0d0 }));
  icon.position.z = .56; g.add(icon);
  return { g, mat, edges, icon };
});
// glass tubes between the boxes (the orb rides the same curves)
const CURVES = [0, 1, 2].map((k) => new THREE.CubicBezierCurve3(BOXP[k].clone(), BOXP[k].clone().add(new THREE.Vector3(0, -1.0, 0)),
  BOXP[k + 1].clone().add(new THREE.Vector3(0, 1.0, 0)), BOXP[k + 1].clone()));
const tubeMat = new THREE.MeshPhysicalMaterial({ color: 0x8fb0ff, transparent: true, opacity: .2, roughness: .05, metalness: 0, clearcoat: 1, emissive: STEEL, emissiveIntensity: .25 });
const tubeCore = new THREE.MeshBasicMaterial({ color: AMBER, transparent: true, opacity: 0 });
const tubes = CURVES.map((cv) => {
  const a = new THREE.Mesh(new THREE.TubeGeometry(cv, 48, .075, 16), tubeMat); flow.add(a);
  const b = new THREE.Mesh(new THREE.TubeGeometry(cv, 48, .022, 8), tubeCore.clone()); flow.add(b);
  return b;
});
const pathPos = (u, out) => { const k = Math.min(2, Math.max(0, Math.floor(u))); return CURVES[k].getPoint(clamp(u - k), out); };

// step props
const formTex = canvasTex(400, 500);
{
  const { g } = formTex; g.fillStyle = "#f4f1ea"; rr(g, 0, 0, 400, 500, 30); g.fill();
  g.fillStyle = "#07090d"; g.font = "800 36px Mont"; g.fillText("New enquiry", 34, 64);
  const f = [["Name", "Priya"], ["Phone", "98xxx xxx21"], ["Message", "Free this week?"]];
  f.forEach(([l, v], k) => {
    g.fillStyle = "#8a93a6"; g.font = "700 20px Mont"; g.fillText(l, 34, 118 + k * 96);
    g.fillStyle = "#e6e1d6"; rr(g, 30, 130 + k * 96, 340, 50, 12); g.fill();
    g.fillStyle = "#07090d"; g.font = "700 24px Mont"; g.fillText(v, 46, 163 + k * 96);
  });
  g.fillStyle = "#ffb020"; rr(g, 30, 418, 340, 56, 28); g.fill();
  g.fillStyle = "#1a1206"; g.font = "800 26px Mont"; g.textAlign = "center"; g.fillText("Submit", 200, 455); g.textAlign = "left";
  formTex.tx.needsUpdate = true;
}
const formCard = new THREE.Mesh(new THREE.PlaneGeometry(.92, 1.15), new THREE.MeshBasicMaterial({ map: formTex.tx, transparent: true, toneMapped: false, side: THREE.DoubleSide, color: 0xd0d0d0 }));
flow.add(formCard);
const sheetTex = canvasTex(620, 420);
function drawSheet(rowA) {
  const { g } = sheetTex;
  g.clearRect(0, 0, 620, 420); g.fillStyle = "#f4f1ea"; rr(g, 0, 0, 620, 420, 26); g.fill();
  g.fillStyle = "#0f8f5c"; rr(g, 0, 0, 620, 70, [26, 26, 0, 0]); g.fill();
  g.fillStyle = "#fff"; g.font = "800 28px Mont"; g.fillText("Leads", 28, 46);
  const cols = [28, 210, 420], heads = ["Name", "Phone", "Time"];
  g.fillStyle = "#8a93a6"; g.font = "700 22px Mont"; heads.forEach((h, k) => g.fillText(h, cols[k], 112));
  const rows = [["Rahul", "99xxx", "6:40 PM"], ["Meera", "97xxx", "8:15 PM"]];
  g.font = "700 25px Mont";
  rows.forEach((r, i) => { g.fillStyle = "#cfc9bc"; g.fillRect(20, 134 + i * 70, 580, 2); g.fillStyle = "#2a2f3a"; r.forEach((v, k) => g.fillText(v, cols[k], 176 + i * 70)); });
  if (rowA > .001) {
    const y = 134 + 2 * 70, s = 1 - back(rowA);
    g.save(); g.globalAlpha = clamp(rowA * 1.5); g.translate(s * 60, 0);
    g.fillStyle = "#ffe2a6"; rr(g, 14, y + 6, 592, 62, 12); g.fill();
    g.fillStyle = "#1a1206"; g.font = "800 25px Mont"; ["Priya", "98xxx", "11:02 PM"].forEach((v, k) => g.fillText(v, cols[k], y + 46));
    g.restore();
  }
  sheetTex.tx.needsUpdate = true;
}
const sheet = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 1.02), new THREE.MeshBasicMaterial({ map: sheetTex.tx, transparent: true, toneMapped: false, side: THREE.DoubleSide, color: 0xcfcfcf }));
flow.add(sheet);
const MP = makePhone(.62, 1.26, 300, 600);
flow.add(MP.g);
function drawAlert(a) {
  const { c, g } = MP.scr, w = c.width, h = c.height;
  g.fillStyle = "#070a12"; g.fillRect(0, 0, w, h);
  g.fillStyle = "#e8ecf5"; g.font = "800 64px Mont"; g.textAlign = "center"; g.fillText("11:02", w / 2, 120); g.textAlign = "left";
  if (a > .001) {
    const s = .7 + .3 * back(a);
    g.save(); g.globalAlpha = clamp(a * 1.5); g.translate(w / 2, 230); g.scale(s, s); g.translate(-w / 2, -230);
    g.fillStyle = "rgba(255,176,32,.95)"; rr(g, 16, 170, w - 32, 130, 22); g.fill();
    g.fillStyle = "#1a1206"; g.font = "800 26px Mont"; g.fillText("New lead", 34, 214);
    g.font = "700 22px Mont"; g.fillText("Priya · 98xxx", 34, 250); g.fillText("Free this week?", 34, 280);
    g.restore();
  }
  MP.scr.tx.needsUpdate = true;
}

// orbs: the lead (pool reused by every beat), each with a short trail
const ON = 8, TR = 5;
const orbGeo = new THREE.SphereGeometry(.1, 24, 16);
const orbs = [];
for (let i = 0; i < ON * TR; i++) {
  const m = new THREE.Mesh(orbGeo, new THREE.MeshBasicMaterial({ color: 0xffe0a0, transparent: true }));
  m.visible = false; flow.add(m); orbs.push(m);
}
function orbAt(i, u, du, a = 1) {                                  // orb i at path position u, trail spaced by du
  for (let j = 0; j < TR; j++) {
    const m = orbs[i * TR + j], uu = u - j * du;
    if (uu < 0 || uu > 3 || a <= .01) { m.visible = false; continue; }
    pathPos(uu, m.position); m.visible = true;
    m.scale.setScalar(1 - j * .17); m.material.opacity = a * (1 - j * .2);
    m.material.color.setHex(j ? AMBER : 0xffe9bf);
  }
}

// ---------------------------------------------------------------- camera poses
const POSE = {
  O: { x: 0, y: -1.9, z: 0, R: 23, a: .16, h: 1.2 },
  S: (k) => ({ x: ZIG[k] * .45, y: -k * GAPY + .36, z: 0, R: 7.4, a: ZIG[k] > 0 ? -.26 : .26, h: .7 }),
};
function poseAt(t) {
  const K = [[-1, 0, POSE.O], [T.s1 - .45, T.s1 + .3, POSE.S(0)], [T.s2 - .6, T.s2 + .2, POSE.S(1)], [T.s3 - .6, T.s3 + .2, POSE.S(2)],
    [T.s4 - .6, T.s4 + .2, POSE.S(3)], [T.live - .4, T.live + .45, { ...POSE.O, a: -.1 }], [T.l08, T.l08 + 1.2, { ...POSE.O, a: .12, R: 22 }],
    [T.cta - .2, T.cta + .6, { ...POSE.O, y: .4, R: 26, a: .05 }]];
  let p = K[0][2];
  for (let i = 1; i < K.length; i++) {
    const [a, b, q] = K[i]; if (t <= a) break;
    const x = easeIO(win(t, a, b)); p = Object.fromEntries(Object.keys(q).map((k) => [k, lerp(p[k], q[k], x)]));
  }
  return p;
}

// ---------------------------------------------------------------- per frame
function renderAt(t) {
  const p = poseAt(t);
  const ang = p.a + Math.sin(t * .35) * .035;
  camera.position.set(p.x + Math.sin(ang) * p.R, p.y + p.h, p.z + Math.cos(ang) * p.R);
  camera.lookAt(p.x, p.y, p.z);
  camera.updateMatrixWorld(true);
  stars.rotation.y = t * .012 + win(t, T.l08, T.cta) * .25;
  stars.material.opacity = .75 - win(t, T.ten - .6, T.ten) * .55 + win(t, T.l01 - .2, T.l01 + .4) * .55;

  // ---- phone + clock: hook and l01 on the left, flown out at l02, back for the live test
  const out1 = easeIO(win(t, T.l02 - .25, T.l02 + .35));
  const liveIn = back(win(t, T.already - .35, T.already + .2)), liveOut = easeIO(win(t, T.l08 + .05, T.l08 + .55));
  const hookVis = out1 < 1, liveVis = liveIn > .001 && liveOut < 1;
  P.g.visible = hookVis || liveVis;
  const buzzHook = pulse(t, T.eleven, .18) + pulse(t, T.seconds + .1, .18);
  if (hookVis) {
    P.g.position.set(lerp(-.42, -1.2, out1), lerp(-.5, -4.6, out1) + Math.sin(t * 1.1) * .03, -10.5);
    P.g.rotation.set(.06 + Math.sin(t * .7) * .02, -.3 + Math.sin(t * .5) * .05 + Math.sin(t * 60) * .03 * buzzHook, Math.sin(t * 55) * .02 * buzzHook + out1 * .6);
    P.g.scale.setScalar(1);
  } else if (liveVis) {
    P.g.position.set(0, lerp(-5.5, -.62, liveIn) - liveOut * 5.5, -9.6);
    P.g.rotation.set(.04, lerp(.6, -.12, liveIn) + Math.sin(t * .6) * .04, liveOut * -.5);
    P.g.scale.setScalar(.96);
  }
  const lost = win(t, T.booked, T.booked + .35) * (1 - win(t, T.l01 - .1, T.l01 + .2));
  const tm = fmt(clockMin(t));
  if (t < T.l01 - .1) {
    drawChat(P.scr, [{ k: "ask", a: 1, time: "11:02 PM" }, { k: "late", a: win(t, T.ten + .35, T.ten + .75), time: "10:04 AM" },
      { k: "gone", a: win(t, T.booked - .1, T.booked + .3), time: "10:09 AM" }], tm, lost, false);
  } else if (t < T.l02 + .4) {
    drawChat(P.scr, [{ k: "ask", a: 1, time: "11:02 PM" }, { k: "auto", a: win(t, T.seconds - .15, T.seconds + .3), time: "11:02 PM" }], tm, 0, true);
  } else {
    drawChat(P.scr, [{ k: "ask", a: 1, time: "11:02 PM" }, { k: "auto", a: win(t, T.already - .1, T.already + .3), time: "11:02 PM" }], "11:02 PM", 0, true);
  }
  phoneGlow.color.setHex(lost > .5 ? CORAL : t > T.seconds ? AMBER : STEEL);
  phoneGlow.intensity = 4 + buzzHook * 10 + pulse(t, T.already, .3) * 10;

  clock.visible = hookVis;
  clock.position.set(lerp(1.22, 2.6, out1), lerp(.6, 2.4, out1), -11.4);
  clock.rotation.set(.1, -.35 + Math.sin(t * .4) * .06, out1 * -1);
  clock.scale.setScalar(1 + pulse(t, T.ten, .35) * .12 + pulse(t, T.l01 + .2, .3) * .1);
  const cm = clockMin(t);
  minHand.rotation.z = -(cm % 60) / 60 * Math.PI * 2;
  hourHand.rotation.z = -((cm / 60) % 12) / 12 * Math.PI * 2;
  clockRimMat.emissive.setHex(lost > .5 ? CORAL : t > T.l01 ? AMBER : STEEL);
  clockRimMat.emissiveIntensity = .7 + pulse(t, T.ten, .4) * 1.5 + pulse(t, T.l01 + .25, .3) * 1.5;
  const dawn = win(t, T.ten - .7, T.ten + .1) * (1 - win(t, T.l01 - .15, T.l01 + .3));
  const de = $("dawn"); if (de) de.style.opacity = dawn * .85;
  const ld = $("lost"); if (ld) ld.style.opacity = lost * .5 * (1 - win(t, T.booked + .2, T.booked + 1.2) * .5);

  // ---- the flow column
  const dropK = (k) => back(win(t, T.boxes - .55 + k * .13, T.boxes - .05 + k * .13));
  flow.visible = t > T.l02 - .7;
  flow.rotation.y = Math.sin(t * .3) * .05 + win(t, T.l08, T.cta + 2) * .5;
  const stepT = [T.s1, T.s2, T.s3, T.s4], litT = [T.form, T.sheet, T.instant, T.buzz];
  const liveHit = (k) => T.formIn + .1 + k * ((T.already - .25 - T.formIn - .1) / 3);
  boxes.forEach((b, k) => {
    const d = dropK(k);
    b.g.position.set(BOXP[k].x, BOXP[k].y + (1 - d) * 6, 0);
    b.g.scale.setScalar(Math.max(.001, d) * (1 + pulse(t, litT[k] + .05, .16) * .12 + pulse(t, liveHit(k), .1) * .14));
    b.g.rotation.y = (1 - d) * 1.5 + Math.sin(t * .8 + k) * .06;
    const lit = t > litT[k] ? 1 : 0;
    const pz = pulse(t, litT[k] + .05, .3) + pulse(t, liveHit(k), .15) + (t > T.l08 ? .35 + .35 * Math.sin(t * 4 - k * 1.2) : 0);
    b.mat.emissiveIntensity = lit * .22 + pz * .8;
    b.edges.material.color.setHex(lit ? AMBER : STEEL);
    b.edges.material.opacity = .45 + lit * .3 + pz * .3;
    b.icon.material.color.setHex(lit ? 0xffd27a : 0x9fb0d0);
    // focus: the box being talked about is bright, the others sit back
    const focus = t > stepT[k] - .3 && t < (k < 3 ? stepT[k + 1] - .3 : T.live - .2);
    b.icon.material.opacity = (t > T.s1 - .3 && t < T.live - .2 && !focus) ? .45 : 1;
  });
  tubes.forEach((tb, k) => {
    const on = t > (k < 3 ? stepT[k + 1] - .1 : 1e9) ? 1 : 0;
    tb.material.opacity = on * .55 + (t > T.l08 ? .25 : 0);
  });
  rimA.position.copy(camera.position).add(new THREE.Vector3(3, -2, -2));
  rimA.intensity = flow.visible ? 18 : 0;
  // orbs: the lead rides down segment by segment between the steps; the live test runs all four in one go; at night a stream
  orbs.forEach((o) => (o.visible = false));
  for (let k = 0; k < 3; k++) {
    const a0 = stepT[k + 1] - .72, a1 = stepT[k + 1] - .06;
    if (t > a0 && t < a1 + .1) orbAt(k, k + easeIO(win(t, a0, a1)), .05, 1 - win(t, a1, a1 + .1));
  }
  if (t > T.formIn - .05 && t < T.already) orbAt(3, lerp(-.05, 3, win(t, T.formIn, T.already - .2)), .09, 1 - win(t, T.already - .2, T.already));
  if (t > T.l08) for (let i = 0; i < 4; i++) { const u = ((t - T.l08) * 1.1 + i * .75) % 3; orbAt(4 + i, u, .06, win(t, T.l08, T.l08 + .4) * (1 - win(t, T.end - .6, T.end))); }

  // step 1: the form card flies in and drops into box 1
  const fc = win(t, T.form - .55, T.form + .1);
  formCard.visible = fc > 0 && fc < 1;
  formCard.position.set(lerp(1.7, BOXP[0].x, easeIO(fc)), lerp(.9, BOXP[0].y + .1, easeIO(fc)) + Math.sin(fc * Math.PI) * .5, lerp(.6, 0, fc));
  formCard.rotation.set(lerp(-.3, 0, fc), lerp(-.7, 0, fc), lerp(.25, 0, fc));
  formCard.scale.setScalar(lerp(1, .25, Math.pow(fc, 3)));
  formCard.material.opacity = 1 - win(t, T.form, T.form + .1);
  // step 2: the sheet beside box 2, the new row slides in
  const shIn = back(win(t, T.s2 + .05, T.s2 + .5)), shOut = win(t, T.s3 - .1, T.s3 + .25);
  sheet.visible = shIn > .001 && shOut < 1;
  sheet.position.set(BOXP[1].x - .98, BOXP[1].y + .16, .8);
  sheet.rotation.set(0, .34, 0);
  sheet.scale.setScalar(Math.max(.001, .84 * shIn * (1 - shOut)));
  if (sheet.visible) drawSheet(win(t, T.sheet - .05, T.sheet + .35));
  // step 4: the small phone pops out of box 4 and buzzes
  const mpIn = back(win(t, T.s4 + .15, T.s4 + .6)), mpOut = win(t, T.live - .45, T.live - .1);
  MP.g.visible = mpIn > .001 && mpOut < 1;
  const bz = Math.max(pulse(t, T.buzz + .1, .3), 0);
  MP.g.position.set(BOXP[3].x - 1.12, BOXP[3].y + .1, .45);
  MP.g.rotation.set(0, .42 + Math.sin(t * 70) * .07 * bz, Math.sin(t * 64) * .06 * bz);
  MP.g.scale.setScalar(Math.max(.001, mpIn * (1 - mpOut)));
  if (MP.g.visible) drawAlert(win(t, T.buzz - .05, T.buzz + .3));
  flow.updateMatrixWorld(true);

  // HTML labels glued to the boxes and step props
  const labA = (k) => clamp(dropK(k) * 2 - 1) * (1 - win(t, T.cta - .2, T.cta + .2)) * (1 - clamp(liveIn) * (1 - liveOut));
  for (let k = 0; k < 4; k++) project(boxes[k].g, new THREE.Vector3(0, .78, 0), $("lab" + k), 0, 0, labA(k));
  const rcT = [T.name, T.thank, T.price, T.booking];
  for (let k = 0; k < 4; k++) {
    const el = $("rc" + k); if (!el) continue;
    const a = back(win(t, rcT[k] - .08, rcT[k] + .22)) * (1 - win(t, T.s4 - .55, T.s4 - .2));
    project(flow, new THREE.Vector3(BOXP[2].x + 1.12, BOXP[2].y + .66 - k * .42, .7), el, 0, 0, clamp(a));
    el.style.transform += ` scale(${Math.max(.001, .5 + .5 * a)})`;
  }

  // ---- the moon rises over "it runs all night"
  const mn = win(t, T.l08 - .3, T.l08 + 1.2);
  moon.material.opacity = mn; moonHalo.material.opacity = mn * .12;
  moon.position.set(lerp(4.5, 3.4, ease(win(t, T.l08, T.end))), lerp(-.6, .5, ease(win(t, T.l08, T.cta))) - ease(win(t, T.cta, T.end)) * 1.2, -30);
  moon.scale.setScalar(.55);

  bloom.strength = .7 + pulse(t, T.already, .3) * .5 + pulse(t, T.flow, .3) * .4;
  composer.render();
}

const ready = (async () => {
  try { await Promise.all(["800 40px Mont", "700 40px Mont"].map((f) => document.fonts.load(f))); } catch (e) { /* fall back to the system font */ }
  renderer.compile(scene, camera); renderAt(window.__hfThreeTime || 0);
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["scene"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
