// AI.NXTLVL "Cicada: a live interpreter for any call" (9:16). The 3D scene is a pure function of time t, rendered on
// HyperFrames' hf-seek, so every frame is exact. Beats come from window.CI_T (build/generate.py, from the voice's word
// times). HTML labels that sit on 3D objects are projected from 3D each frame (positions only; the type is HTML).
//   hook   laptop on a call: your English line goes out in Japanese (frame 1 already shows it)
//   l01-03 any call (app chips orbit), no bot joins (participants: 2), the name
//   l04-05 globe: you -> Tokyo; the client asks in Japanese, English subtitles land live
//   l06-07 the right Option key is held, you answer in English; let go, the Japanese goes into the call
//   l08-10 the notes window: summary, to-do; click it and the transcript jumps to the exact line
//   l11-13 hero + GitHub card; the globe with arcs to clients abroad; the CTA
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { LAND } from "./land_dots.js";

const W = 1080, H = 1920;
const T = window.CI_T;
const VIOLET = 0x7a2ffb, LAV = 0xb687f9, CYAN = 0x6fe3ff;
const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(38, W / H, .05, 200);
scene.add(camera);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), .03).texture;
scene.environmentIntensity = .42;
scene.fog = new THREE.Fog(0x07050f, 22, 60);
{
  const c = document.createElement("canvas"); c.width = 256; c.height = 512;
  const g = c.getContext("2d");
  g.fillStyle = "#07050f"; g.fillRect(0, 0, 256, 512);
  const a = g.createRadialGradient(20, 40, 0, 20, 40, 300); a.addColorStop(0, "rgba(127,27,248,.38)"); a.addColorStop(1, "rgba(127,27,248,0)");
  g.fillStyle = a; g.fillRect(0, 0, 256, 512);
  const b = g.createRadialGradient(240, 480, 0, 240, 480, 320); b.addColorStop(0, "rgba(96,8,242,.34)"); b.addColorStop(1, "rgba(96,8,242,0)");
  g.fillStyle = b; g.fillRect(0, 0, 256, 512);
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; scene.background = tx;
}
const composer = new EffectComposer(renderer);
composer.setSize(W, H);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), .5, .5, .9);
composer.addPass(bloom);
composer.addPass(new OutputPass());

scene.add(new THREE.HemisphereLight(0xcfc6ff, 0x0a0614, .5));
const key = new THREE.DirectionalLight(0xfff4ea, 1.6); key.position.set(-4, 7, 6); scene.add(key);
const rimV = new THREE.PointLight(VIOLET, 60, 20); rimV.position.set(4, 3.5, -4); scene.add(rimV);
const rimL = new THREE.PointLight(LAV, 18, 14); rimL.position.set(-5, 2, -2); scene.add(rimL);


// ---------------------------------------------------------------- helpers
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const win = (t, a, b) => clamp((t - a) / (b - a));
const ease = (x) => 1 - Math.pow(1 - clamp(x), 3);
const easeIO = (x) => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const back = (x) => { x = clamp(x); const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const lerp = (a, b, x) => a + (b - a) * x;
const pulse = (t, at, w = .25) => Math.exp(-Math.pow((t - at) / w, 2));
const rnd = (i, k = 1) => { const s = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return s - Math.floor(s); };
const $ = (id) => document.getElementById(id);
const v3 = new THREE.Vector3();
function project(obj, local, el, a = null, dx = 0, dy = 0, s = 1) {
  if (!el) return;
  v3.copy(local); if (obj) obj.localToWorld(v3); v3.project(camera);
  const behind = v3.z > 1;
  el.style.transform = `translate(${(v3.x * .5 + .5) * W + dx}px, ${(-v3.y * .5 + .5) * H + dy}px) translate(-50%, -50%) scale(${Math.max(.001, s)})`;
  if (a !== null) el.style.opacity = behind ? 0 : clamp(a);
}
function rr(g, x, y, w, h, r) { g.beginPath(); g.roundRect(x, y, w, h, r); }
function canvasTex(w, h) {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8;
  return { c, g: c.getContext("2d"), tx };
}
// speech envelope: a lively 0..1 level while someone talks
const level = (t, seed) => .35 + .65 * Math.abs(Math.sin(t * 13.1 + seed) * Math.sin(t * 7.3 + seed * 2.1));

// ---------------------------------------------------------------- the laptop
const alu = new THREE.MeshPhysicalMaterial({ color: 0x34363f, metalness: .9, roughness: .58, envMapIntensity: .32 });
const keyMat = new THREE.MeshStandardMaterial({ color: 0x0b0c10, roughness: .6, metalness: .1 });
const laptop = new THREE.Group(); scene.add(laptop);
const BW = 3.3, BD = 2.3, BH = .1;
{ const m = new THREE.Mesh(new RoundedBoxGeometry(BW, BH, BD, 6, .05), alu); m.position.y = BH / 2; laptop.add(m); }
const well = new THREE.Mesh(new THREE.PlaneGeometry(3.04, 1.18), new THREE.MeshStandardMaterial({ color: 0x15161b, roughness: .7, metalness: .4 }));
well.rotation.x = -Math.PI / 2; well.position.set(0, BH + .001, -.4); laptop.add(well);
// keys: 5 rows of 13 + a bottom row with the space bar; the right Option key is its own mesh (it glows and presses)
const KP = .226, KS = .19;
const keyGeo = new RoundedBoxGeometry(1, 1, 1, 2, .12);
const keySpecs = [];
for (let r = 0; r < 5; r++) for (let c = 0; c < 13; c++) keySpecs.push([-1.356 + c * KP, -.88 + r * KP, 1]);
const bottom = [1, 1, 1, 1.3, 4.9, 1.3, 1, 1, 1];                    // fn ctrl opt cmd SPACE cmd OPT left/right
let bx = -1.356 - KP / 2, optR = null;
bottom.forEach((wu, i) => { const w = wu * KP; const cx = bx + w / 2; bx += w; if (i === 6) optR = cx; else keySpecs.push([cx, -.88 + 5 * KP, wu]); });
const keys = new THREE.InstancedMesh(keyGeo, keyMat, keySpecs.length);
const m4 = new THREE.Matrix4();
keySpecs.forEach(([x, z, wu], i) => { m4.compose(new THREE.Vector3(x, BH + .02, z), new THREE.Quaternion(), new THREE.Vector3(wu * KP - (KP - KS), .035, KS)); keys.setMatrixAt(i, m4); });
laptop.add(keys);
const optTex = canvasTex(128, 128);
{ const g = optTex.g; g.fillStyle = "#0b0c10"; g.fillRect(0, 0, 128, 128); g.fillStyle = "#d9d2ff"; g.font = "700 44px Mont"; g.textAlign = "center"; g.fillText("⌥", 64, 62); g.font = "700 20px Mont"; g.fillText("option", 64, 104); optTex.tx.needsUpdate = true; }
const optMat = new THREE.MeshStandardMaterial({ color: 0x14121c, roughness: .5, emissive: VIOLET, emissiveIntensity: 0 });
const optKey = new THREE.Mesh(keyGeo, optMat); optKey.scale.set(KS, .035, KS); optKey.position.set(optR, BH + .02, -.88 + 5 * KP); laptop.add(optKey);
const optCap = new THREE.Mesh(new THREE.PlaneGeometry(.92, .92), new THREE.MeshBasicMaterial({ map: optTex.tx, transparent: true, toneMapped: false }));
optCap.rotation.x = -Math.PI / 2; optCap.position.set(0, .51, 0); optKey.add(optCap);      // in the key's unit space
const optRing = new THREE.Mesh(new THREE.RingGeometry(.14, .16, 48), new THREE.MeshBasicMaterial({ color: LAV, transparent: true, opacity: 0, side: THREE.DoubleSide }));
optRing.rotation.x = -Math.PI / 2; optRing.position.set(optR, BH + .045, -.88 + 5 * KP); laptop.add(optRing);
const pad = new THREE.Mesh(new RoundedBoxGeometry(1.32, .004, .78, 2, .002), new THREE.MeshPhysicalMaterial({ color: 0x24262d, metalness: .9, roughness: .45 }));
pad.position.set(0, BH + .002, .62); laptop.add(pad);
// the lid (hinged at the back edge) with the bezel and the display
const lid = new THREE.Group(); lid.position.set(0, BH, -BD / 2 + .03); laptop.add(lid);
const LH = 2.15;
{ const m = new THREE.Mesh(new RoundedBoxGeometry(BW, LH, .06, 6, .03), alu); m.position.set(0, LH / 2, 0); lid.add(m); }
const bezel = new THREE.Mesh(new THREE.PlaneGeometry(BW - .1, LH - .1), new THREE.MeshPhysicalMaterial({ color: 0x030304, roughness: .22, clearcoat: .4, envMapIntensity: .25 }));
bezel.position.set(0, LH / 2, .031); lid.add(bezel);
const SCR = canvasTex(1600, 1000);
const display = new THREE.Mesh(new THREE.PlaneGeometry(3.02, 1.8875), new THREE.MeshBasicMaterial({ map: SCR.tx, toneMapped: false, color: 0xe2e2e2 }));
display.position.set(0, LH / 2 + .02, .0325); lid.add(display);
lid.rotation.x = -.27;
const toScreen = (u, v) => new THREE.Vector3((u - .5) * 3.02, (.5 - v) * 1.8875, .04);   // canvas uv -> display local
// floor + contact shadow
const floor = new THREE.Mesh(new THREE.CircleGeometry(30, 64), new THREE.MeshStandardMaterial({ color: 0x0a0713, roughness: .7, metalness: .15 }));
floor.rotation.x = -Math.PI / 2; scene.add(floor);
{
  const c = canvasTex(256, 256), g = c.g, gr = g.createRadialGradient(128, 128, 10, 128, 128, 128);
  gr.addColorStop(0, "rgba(0,0,0,.85)"); gr.addColorStop(.6, "rgba(0,0,0,.35)"); gr.addColorStop(1, "rgba(0,0,0,0)");
  g.fillStyle = gr; g.fillRect(0, 0, 256, 256); c.tx.needsUpdate = true;
  const sh = new THREE.Mesh(new THREE.PlaneGeometry(5.2, 3.8), new THREE.MeshBasicMaterial({ map: c.tx, transparent: true, depthWrite: false }));
  sh.rotation.x = -Math.PI / 2; sh.position.y = .002; scene.add(sh);
}
// voice particles: from the keyboard up into the call (your voice going out) or from the screen out (the client)
const PN = 70;
const partGeo = new THREE.SphereGeometry(.014, 10, 8);
const parts = [];
for (let i = 0; i < PN; i++) { const m = new THREE.Mesh(partGeo, new THREE.MeshBasicMaterial({ color: LAV, transparent: true })); m.visible = false; scene.add(m); parts.push(m); }
const voiceCurve = new THREE.CatmullRomCurve3([new THREE.Vector3(.62, .16, .38), new THREE.Vector3(1.55, .9, .7), new THREE.Vector3(1.35, 1.7, .1), new THREE.Vector3(.55, 1.45, -.75)]);

// ---------------------------------------------------------------- the screen UI (drawn every frame)
const JP = "NotoJP", MO = "Mont";
const ASK_JA = "金曜日までに価格表を送っていただけますか？";
const REPLY_JA = "はい、木曜日に送ります。";
const ASK_EN = ["Can", "you", "send", "the", "price", "list", "by", "Friday?"];
const REPLY_EN = ["Yes,", "I'll", "send", "it", "Thursday."];
function person(g, cx, cy, s, skin, shirt) {                          // a simple head-and-shoulders silhouette
  g.fillStyle = shirt; g.beginPath(); g.ellipse(cx, cy + s * 1.15, s * 1.25, s * .8, 0, Math.PI, 0); g.fill();
  g.fillStyle = skin; g.beginPath(); g.arc(cx, cy, s * .55, 0, 7); g.fill();
  g.fillStyle = "rgba(20,14,30,.85)"; g.beginPath(); g.arc(cx, cy - s * .18, s * .57, Math.PI * 1.05, Math.PI * 1.95); g.fill();
}
function bars(g, x, y, w, h, n, lv, col) {
  for (let i = 0; i < n; i++) {
    const a = lv * (.35 + .65 * Math.abs(Math.sin(i * 1.7 + lv * 9)));
    const bh = Math.max(6, h * a); g.fillStyle = col; rr(g, x + i * (w / n), y + (h - bh) / 2, w / n * .55, bh, 4); g.fill();
  }
}
function drawCall(t, st) {
  const g = SCR.g, w = 1600, h = 1000;
  g.fillStyle = "#0d0b14"; g.fillRect(0, 0, w, h);
  // title bar
  g.fillStyle = "#16131f"; g.fillRect(0, 0, w, 64);
  ["#ff5f57", "#febc2e", "#28c840"].forEach((c, i) => { g.fillStyle = c; g.beginPath(); g.arc(34 + i * 30, 32, 9, 0, 7); g.fill(); });
  g.fillStyle = "#cfc8e6"; g.font = `700 26px ${MO}`; g.textAlign = "center"; g.fillText("Client call", w / 2, 41); g.textAlign = "left";
  g.fillStyle = "#ff4d6d"; g.beginPath(); g.arc(w - 150, 32, 8, 0, 7); g.fill(); g.fillStyle = "#cfc8e6"; g.font = `700 22px ${MO}`; g.fillText("REC 12:47", w - 132, 40);
  // the client's tile
  const panel = st.panel, tw = panel > 0 ? lerp(w - 48, w - 48 - 420, panel) : w - 48;
  const tx = 24, ty = 84, th = 700;
  const grd = g.createLinearGradient(tx, ty, tx + tw, ty + th); grd.addColorStop(0, "#2a1c3f"); grd.addColorStop(1, "#140f22");
  g.fillStyle = grd; rr(g, tx, ty, tw, th, 22); g.fill();
  person(g, tx + tw / 2, ty + 300, 150, "#e7b98f", "#3b3150");
  if (st.client > .01) { g.strokeStyle = `rgba(111,227,255,${.5 + .5 * st.client})`; g.lineWidth = 8; rr(g, tx + 4, ty + 4, tw - 8, th - 8, 20); g.stroke(); }
  g.fillStyle = "rgba(10,8,16,.72)"; rr(g, tx + 20, ty + th - 70, 360, 50, 14); g.fill();
  g.fillStyle = "#f2efff"; g.font = `700 26px ${MO}`; g.fillText("Haruka Mori · Tokyo", tx + 40, ty + th - 37);
  if (st.client > .01) bars(g, tx + tw - 130, ty + th - 66, 100, 40, 6, st.client, "#6fe3ff");
  if (st.hear > .01) {                                              // the client hears your Japanese
    g.fillStyle = `rgba(122,47,251,${.85 * st.hear})`; rr(g, tx + tw - 380, ty + 22, 356, 56, 28); g.fill();
    g.fillStyle = `rgba(255,255,255,${st.hear})`; g.font = `700 25px ${MO}`; g.fillText("Hearing you in Japanese", tx + tw - 356, ty + 59);
  }
  // your tile
  const yx = tx + tw - 300, yy = ty + th - 230;
  g.fillStyle = "#211a33"; rr(g, yx, yy, 270, 200, 18); g.fill();
  person(g, yx + 135, yy + 82, 58, "#c58b62", "#5b3fa0");
  if (st.you > .01) { g.strokeStyle = `rgba(182,135,249,${.5 + .5 * st.you})`; g.lineWidth = 6; rr(g, yx + 3, yy + 3, 264, 194, 16); g.stroke(); }
  g.fillStyle = "#f2efff"; g.font = `700 22px ${MO}`; g.fillText("You", yx + 16, yy + 186);
  // participants panel (no bot)
  if (panel > .01) {
    const px = w - 24 - 400 * panel, pw = 400;
    g.save(); g.globalAlpha = panel;
    g.fillStyle = "#16131f"; rr(g, px, ty, pw, th, 22); g.fill();
    g.fillStyle = "#cfc8e6"; g.font = `800 40px ${MO}`; g.fillText("Participants (2)", px + 30, ty + 80);
    [["Haruka Mori", "#e7b98f"], ["You", "#c58b62"]].forEach(([n, c], i) => {
      g.fillStyle = c; g.beginPath(); g.arc(px + 66, ty + 180 + i * 120, 38, 0, 7); g.fill();
      g.fillStyle = "#f2efff"; g.font = `700 38px ${MO}`; g.fillText(n, px + 124, ty + 194 + i * 120);
    });
    g.strokeStyle = "rgba(255,255,255,.1)"; g.lineWidth = 3; g.beginPath(); g.moveTo(px + 24, ty + 420); g.lineTo(px + pw - 24, ty + 420); g.stroke();
    g.fillStyle = "#7ee2a8"; g.font = `800 38px ${MO}`; g.fillText("✓ No bots", px + 30, ty + 500);
    g.fillStyle = "#9b93b8"; g.font = `700 30px ${MO}`; g.fillText("in this call", px + 30, ty + 546);
    g.restore();
  }
  // control bar
  g.fillStyle = "#16131f"; g.fillRect(0, h - 150, w, 150);
  for (let i = 0; i < 5; i++) { g.fillStyle = i === 4 ? "#e5484d" : "#2a2538"; g.beginPath(); g.arc(w / 2 - 240 + i * 120, h - 75, 34, 0, 7); g.fill(); }
  // the Cicada subtitle bar
  if (st.sub > .01) {
    const sw = 1300, sx = (w - sw) / 2, sy = 560, sh = 330;
    g.save(); g.globalAlpha = st.sub;
    g.fillStyle = "rgba(14,10,24,.92)"; rr(g, sx, sy, sw, sh, 26); g.fill();
    g.strokeStyle = "rgba(182,135,249,.55)"; g.lineWidth = 3; rr(g, sx, sy, sw, sh, 26); g.stroke();
    g.font = `800 30px ${MO}`; const tw2 = g.measureText(st.tag).width + 56;
    g.fillStyle = "#7a2ffb"; rr(g, sx + 30, sy - 28, tw2, 56, 28); g.fill();
    g.fillStyle = "#fff"; g.fillText(st.tag, sx + 58, sy + 10);
    const fit = (txt, full, fam, wt, size) => { const n = full.length ? full : txt; g.font = `${wt} ${size}px ${fam}`; const m = g.measureText(n).width; return Math.min(size, Math.floor(size * (sw - 96) / Math.max(1, m))); };
    const s1 = fit(st.l1, st.l1full || "", st.l1ja ? JP : MO, st.l1ja ? 700 : 800, st.l1ja ? 84 : 78);
    g.fillStyle = "#ffffff"; g.font = st.l1ja ? `700 ${s1}px ${JP}` : `800 ${s1}px ${MO}`; g.fillText(st.l1, sx + 48, sy + 150);
    const s2 = fit(st.l2, st.l2full || "", st.l2ja ? JP : MO, 700, st.l2ja ? 62 : 58);
    g.fillStyle = "#c4bbe6"; g.font = st.l2ja ? `700 ${s2}px ${JP}` : `700 ${s2}px ${MO}`; g.fillText(st.l2, sx + 48, sy + 262);
    g.restore();
  }
}
function drawNotes(t, st) {
  const g = SCR.g, w = 1600, h = 1000;
  g.fillStyle = "#100c1c"; g.fillRect(0, 0, w, h);
  g.fillStyle = "#18132a"; g.fillRect(0, 0, w, 64);
  ["#ff5f57", "#febc2e", "#28c840"].forEach((c, i) => { g.fillStyle = c; g.beginPath(); g.arc(34 + i * 30, 32, 9, 0, 7); g.fill(); });
  g.fillStyle = "#cfc8e6"; g.font = `800 26px ${MO}`; g.textAlign = "center"; g.fillText("Cicada · Notes", w / 2, 41); g.textAlign = "left";
  const sc = st.jump;                                                 // 0 = notes, 1 = slid over to the transcript line
  g.save(); g.translate(-sc * 820, 0);
  g.fillStyle = "#ffffff"; g.font = `800 64px ${MO}`; g.fillText("Call with Haruka Mori", 80, 170);
  g.fillStyle = "#b687f9"; g.font = `800 28px ${MO}`; g.fillText("SUMMARY", 80, 262);
  g.save(); g.globalAlpha = st.sum;
  g.fillStyle = "#e9e4ff"; g.font = `700 46px ${MO}`;
  g.fillText("Haruka asked for the price list", 80, 330); g.fillText("by Friday. You'll send it Thursday.", 80, 392);
  g.restore();
  g.fillStyle = "#b687f9"; g.font = `800 28px ${MO}`; g.fillText("TO-DO", 80, 506);
  if (st.todo > .01) {
    g.save(); g.globalAlpha = clamp(st.todo * 1.5);
    const y = 534, hi = st.hover;
    g.fillStyle = `rgba(122,47,251,${.22 + .2 * hi})`; rr(g, 60, y, 900, 124, 22); g.fill();
    g.strokeStyle = `rgba(182,135,249,${.5 + .5 * hi})`; g.lineWidth = 3; rr(g, 60, y, 900, 124, 22); g.stroke();
    g.strokeStyle = "#b687f9"; g.lineWidth = 5; rr(g, 92, y + 38, 48, 48, 10); g.stroke();
    g.fillStyle = "#ffffff"; g.font = `800 46px ${MO}`; g.fillText("Send the price list by Thursday", 166, y + 78);
    g.restore();
  }
  // transcript (to the right; the window slides over to it)
  const X = 1000;
  g.fillStyle = "#b687f9"; g.font = `800 28px ${MO}`; g.fillText("TRANSCRIPT", X, 262);
  const lines = [["12:46", "Haruka", "お疲れさまです。", "Hi, thanks for joining."], ["12:47", "Haruka", ASK_JA, "Can you send the price list by Friday?"],
    ["12:47", "You", REPLY_JA, "Yes, I'll send it Thursday."]];
  lines.forEach(([ts, who, ja, en], i) => {
    const y = 300 + i * 210;
    if (i === 1 && st.flash > .01) { g.fillStyle = `rgba(122,47,251,${.25 + .3 * st.flash})`; rr(g, X - 24, y - 4, 1400, 196, 20); g.fill(); g.fillStyle = "#b687f9"; g.fillRect(X - 24, y - 4, 10, 196); }
    g.fillStyle = "#b687f9"; g.font = `800 32px ${MO}`; g.fillText(ts, X, y + 48);
    g.fillStyle = "#ffffff"; g.font = `800 34px ${MO}`; g.fillText(who, X + 118, y + 48);
    g.fillStyle = "#ffffff"; g.font = `700 48px ${JP}`; g.fillText(ja, X + 118, y + 112);
    g.fillStyle = "#a59cc6"; g.font = `700 38px ${MO}`; g.fillText(en, X + 118, y + 166);
  });
  g.restore();
  if (st.jump > .5) {                                                 // the playhead after the jump
    g.save(); g.globalAlpha = win(st.jump, .5, 1);
    g.fillStyle = "#7a2ffb"; rr(g, w - 420, h - 120, 360, 72, 36); g.fill();
    g.fillStyle = "#fff"; g.font = `800 32px ${MO}`; g.fillText("▶  Playing 12:47", w - 384, h - 72);
    g.restore();
  }
  if (st.cur > .01) {                                                 // the cursor
    const cx = lerp(1350, 620, st.curP), cy = lerp(940, 600, st.curP), s = 1 - .15 * st.press;
    g.save(); g.globalAlpha = st.cur * (1 - win(st.jump, 0, .4)); g.translate(cx, cy); g.scale(s * 1.9, s * 1.9);
    g.fillStyle = "#ffffff"; g.strokeStyle = "#14101f"; g.lineWidth = 2.5;
    g.beginPath(); g.moveTo(0, 0); g.lineTo(0, 30); g.lineTo(8, 23); g.lineTo(14, 36); g.lineTo(19, 34); g.lineTo(13, 21); g.lineTo(23, 21); g.closePath(); g.fill(); g.stroke();
    g.restore();
    if (st.ripple > .01 && st.ripple < 1) { g.strokeStyle = `rgba(182,135,249,${1 - st.ripple})`; g.lineWidth = 6; g.beginPath(); g.arc(cx, cy, 24 + st.ripple * 90, 0, 7); g.stroke(); }
  }
}
function typed(words, t, t0, t1) { const n = Math.floor(clamp((t - t0) / Math.max(.01, t1 - t0)) * words.length + .0001); return words.slice(0, n).join(" "); }
function drawScreen(t) {
  if (t < T.l08 - .15) {
    const st = { panel: easeIO(win(t, T.bot - .35, T.bot + .1)) * (1 - easeIO(win(t, T.l03 - .2, T.l03 + .2))), client: 0, you: 0, hear: 0, sub: 0, tag: "", l1: "", l2: "", l1ja: false, l2ja: false };
    if (t < T.l01) {                                                   // hook: you spoke English, the client hears Japanese
      st.sub = 1; st.tag = "INTERPRETING  EN → JA"; st.l1 = REPLY_JA; st.l1ja = true; st.l2 = REPLY_EN.join(" ");
      st.hear = 1; st.client = 0; st.you = .3 + .7 * level(t, 1) * (1 - win(t, T.l00 + 1.2, T.l00 + 1.6));
    } else if (t >= T.asks - .1 && t < T.l06 - .1) {                  // the client asks, the subtitles land live
      st.sub = win(t, T.asks - .1, T.asks + .15); st.tag = "LIVE SUBTITLES  JA → EN";
      const n = Math.round(clamp((t - T.asks) / Math.max(.3, T.friday + .3 - T.asks)) * ASK_JA.length);
      st.l1 = ASK_JA.slice(0, n); st.l1full = ASK_JA; st.l1ja = true; st.l2 = typed(ASK_EN, t, T.can, T.friday + .25); st.l2full = ASK_EN.join(" ");
      st.client = t < T.l05 + .4 ? level(t, 3) : 0;
    } else if (t >= T.l06 - .1) {                                      // you hold the key and answer; let go: Japanese out
      st.sub = 1; st.tag = t < T.let ? "HOLD ⌥ TO TALK  EN → JA" : "INTERPRETING  EN → JA";
      st.l1 = typed(REPLY_EN, t, T.yes, T.thursday + .3); st.l1full = REPLY_EN.join(" "); st.l2 = t > T.let + .15 ? REPLY_JA : (t > T.thursday + .3 && t < T.let ? "translating…" : "");
      st.l2ja = t > T.let + .15;
      st.you = t > T.yes - .1 && t < T.thursday + .5 ? level(t, 2) : 0;
      st.hear = win(t, T.let + .1, T.let + .4); st.client = 0;
    }
    drawCall(t, st);
  } else {
    drawNotes(t, {
      sum: win(t, T.summary - .1, T.summary + .3), todo: back(win(t, T.todo - .1, T.todo + .35)),
      cur: win(t, T.l10 - .5, T.l10 - .2), curP: easeIO(win(t, T.l10 - .45, T.click - .05)), press: pulse(t, T.click, .08),
      ripple: win(t, T.click, T.click + .5) * (t > T.click ? 1 : 0), hover: win(t, T.click - .3, T.click),
      jump: easeIO(win(t, T.jumps - .05, T.jumps + .45)), flash: t > T.jumps + .3 ? .5 + .5 * pulse(t, T.exact + .1, .35) : 0,
    });
  }
  SCR.tx.needsUpdate = true;
}

// ---------------------------------------------------------------- the globe (real land outlines: Natural Earth)
const globe = new THREE.Group(); scene.add(globe);
const GR = 2;
globe.add(new THREE.Mesh(new THREE.SphereGeometry(GR, 64, 48), new THREE.MeshStandardMaterial({ color: 0x0d0a1c, roughness: .6, metalness: .2 })));
const atmoTex = canvasTex(512, 512);
{ const g = atmoTex.g, gr = g.createRadialGradient(256, 256, 150, 256, 256, 256); gr.addColorStop(0, "rgba(122,47,251,0)"); gr.addColorStop(.62, "rgba(122,47,251,.55)"); gr.addColorStop(.72, "rgba(150,110,255,.25)"); gr.addColorStop(1, "rgba(122,47,251,0)"); g.fillStyle = gr; g.fillRect(0, 0, 512, 512); atmoTex.tx.needsUpdate = true; }
const atmo = new THREE.Sprite(new THREE.SpriteMaterial({ map: atmoTex.tx, transparent: true, depthWrite: false, fog: false, opacity: .8 }));
atmo.scale.set(GR * 3.3, GR * 3.3, 1); scene.add(atmo);
const ll = (lat, lon, r = GR) => { const p = lat * Math.PI / 180, l = lon * Math.PI / 180; return new THREE.Vector3(r * Math.cos(p) * Math.sin(l), r * Math.sin(p), r * Math.cos(p) * Math.cos(l)); };
{
  const dot = new THREE.CircleGeometry(.018, 8);
  const dots = new THREE.InstancedMesh(dot, new THREE.MeshBasicMaterial({ color: 0xb9a3ff, side: THREE.DoubleSide, fog: false }), LAND.length);
  const q = new THREE.Quaternion(), z = new THREE.Vector3(0, 0, 1);
  LAND.forEach(([la, lo], i) => { const p = ll(la, lo, GR * 1.002); q.setFromUnitVectors(z, p.clone().normalize()); m4.compose(p, q, new THREE.Vector3(1, 1, 1)); dots.setMatrixAt(i, m4); });
  globe.add(dots);
}
const CITY = { you: [28.6, 77.2], tokyo: [35.7, 139.7], berlin: [52.5, 13.4], ny: [40.7, -74.0], dubai: [25.2, 55.3], sydney: [-33.9, 151.2], sp: [-23.5, -46.6] };
function arc(a, b, lift = .55) {
  const p0 = ll(...a), p1 = ll(...b), mid = p0.clone().add(p1).multiplyScalar(.5);
  mid.normalize().multiplyScalar(GR * (1 + lift * p0.distanceTo(p1) / (2 * GR) + .1));
  const cv = new THREE.QuadraticBezierCurve3(p0, mid, p1);
  const geo = new THREE.TubeGeometry(cv, 80, .014, 8);
  const mesh = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: CYAN, transparent: true, fog: false }));
  globe.add(mesh); return { mesh, cv, n: geo.index.count };
}
const arcs = { tokyo: arc(CITY.you, CITY.tokyo), berlin: arc(CITY.you, CITY.berlin), ny: arc(CITY.you, CITY.ny, .4), dubai: arc(CITY.you, CITY.dubai), sydney: arc(CITY.you, CITY.sydney), sp: arc(CITY.you, CITY.sp, .35) };
const pins = {};
for (const k of Object.keys(CITY)) {
  const p = new THREE.Mesh(new THREE.SphereGeometry(.05, 16, 12), new THREE.MeshBasicMaterial({ color: k === "you" ? LAV : CYAN, fog: false }));
  p.position.copy(ll(...CITY[k], GR * 1.01)); globe.add(p); pins[k] = p;
}
const arcHead = new THREE.Mesh(new THREE.SphereGeometry(.06, 16, 12), new THREE.MeshBasicMaterial({ color: 0xffffff, fog: false }));
globe.add(arcHead);
const G1 = new THREE.Vector3(10, 3.0, -3);

// ---------------------------------------------------------------- camera shots
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const S = {
  hook: { p: V(2.6, 2.7, 9.4), t: V(.2, 1.2, -.6) },
  b: { p: V(-4.6, 3.2, 11.0), t: V(0, 1.25, -.3) },
  bot: { p: V(2.3, 1.6, 3.6), t: V(1.2, 1.45, -.95) },
  name: { p: V(0, 3.6, 11.5), t: V(0, 2.2, -.3) },
  globe: { p: G1.clone().add(V(0, .7, 8.6)), t: G1.clone().add(V(0, 1.0, 0)) },
  ask: { p: V(0, 1.15, 5.2), t: V(0, 1.02, -1.0) },
  live: { p: V(.45, 1.0, 4.8), t: V(.05, .97, -1.05) },
  key: { p: V(2.1, 1.7, 1.9), t: V(.85, .2, -.1) },
  out: { p: V(-3.0, 2.7, 10.4), t: V(0, 1.45, -.4) },
  notes: { p: V(0, 1.2, 6.5), t: V(0, 1.3, -.85) },
  click: { p: V(-.2, 1.05, 3.6), t: V(-.45, 1.05, -.9) },
  hero: { p: V(0, 3.4, 12.5), t: V(0, 2.4, -.4) },
  world: { p: G1.clone().add(V(0, .8, 15.5)), t: G1.clone().add(V(0, 2.3, 0)) },
};
function shotAt(t) {
  const K = [[-1, 0, S.hook], [T.l01 - .25, T.l01 + .45, S.b], [T.bot - .45, T.bot + .1, S.bot], [T.l03 - .3, T.l03 + .3, S.name],
    [T.l04 - .2, T.l04 + .35, S.globe], [T.can - .35, T.can + .1, S.ask], [T.l05 - .2, T.l05 + .4, S.live], [T.l06 - .3, T.l06 + .15, S.key],
    [T.let - .1, T.let + .45, S.out], [T.l08 - .3, T.l08 + .3, S.notes], [T.l10 - .3, T.l10 + .3, S.click], [T.l11 - .3, T.l11 + .45, S.hero],
    [T.l12 - .3, T.l12 + .35, S.world]];
  let p = K[0][2].p.clone(), q = K[0][2].t.clone();
  for (let i = 1; i < K.length; i++) {
    const [a, b, s] = K[i]; if (t <= a) break;
    const x = easeIO(win(t, a, b)); p.lerp(s.p, x); q.lerp(s.t, x);
  }
  return { p, q };
}

// ---------------------------------------------------------------- per frame
function renderAt(t) {
  const { p, q } = shotAt(t);
  // a slow orbit drift around the target keeps every shot alive
  const d = p.clone().sub(q), a = Math.sin(t * .4) * .045;
  d.applyAxisAngle(V(0, 1, 0), a);
  camera.position.copy(q).add(d); camera.lookAt(q);
  camera.updateMatrixWorld(true);

  // laptop + screen
  drawScreen(t);
  // the right Option key: held from "hold" to "let go"
  const held = win(t, T.hold - .05, T.hold + .08) * (1 - win(t, T.let - .02, T.let + .1));
  optKey.position.y = BH + .02 - held * .018;
  optMat.emissiveIntensity = held * 2.2 + pulse(t, T.hold, .2) * 2;
  optRing.material.opacity = held * (.6 + .4 * Math.sin(t * 10));
  optRing.scale.setScalar(1 + ((t * 1.6) % 1) * .45 * held);
  // voice particles: your voice goes up into the call (hook, while you talk, after you let go)
  const flowOn = Math.max(t < T.l01 - .2 ? 1 : 0, win(t, T.let - .05, T.let + .3) * (1 - win(t, T.l08 - .6, T.l08 - .2)));
  parts.forEach((m, i) => {
    const u = ((t * .55 + rnd(i)) % 1);
    if (flowOn < .01) { m.visible = false; return; }
    voiceCurve.getPoint(u, m.position); m.position.x += (rnd(i, 2) - .5) * .12; m.position.y += (rnd(i, 3) - .5) * .12;
    m.visible = true; m.material.opacity = flowOn * Math.sin(u * Math.PI) * .9;
    m.material.color.setHex(t > T.let ? CYAN : LAV);
    m.scale.setScalar(.6 + rnd(i, 4) * .9);
  });

  // globe: the Tokyo arc on "Tokyo", all arcs on the share line
  const gOn = (t > T.l04 - .6 && t < T.can + .2) || t > T.l12 - .6;
  globe.visible = gOn;
  globe.position.copy(G1);
  const lonC = t > T.l12 - .6 ? lerp(105, 60, ease(win(t, T.l12 - .3, T.end))) : lerp(95, 112, win(t, T.l04 - .6, T.can + .2));
  globe.rotation.set(.42, -lonC * Math.PI / 180, 0);
  const tok = easeIO(win(t, T.tokyo - .5, T.tokyo + .25));
  const showArc = (A, x) => { A.mesh.geometry.setDrawRange(0, Math.floor(A.n * clamp(x) / 3) * 3); A.mesh.visible = x > .01; };
  showArc(arcs.tokyo, t > T.l12 - .6 ? 1 : tok);
  arcHead.visible = tok > .01 && tok < 1 && t < T.l12;
  if (arcHead.visible) arcs.tokyo.cv.getPoint(tok, arcHead.position);
  ["berlin", "ny", "dubai", "sydney", "sp"].forEach((k, i) => showArc(arcs[k], easeIO(win(t, T.l12 + i * .16, T.l12 + .55 + i * .16))));
  for (const k of Object.keys(pins)) pins[k].scale.setScalar(k === "you" || k === "tokyo" ? 1 + pulse(t, T.tokyo + .25, .2) * .8 : (t > T.l12 ? 1 : 0.001));
  atmo.visible = gOn; atmo.position.copy(G1); atmo.material.opacity = .75 + pulse(t, T.tokyo + .25, .3) * .25;
  globe.updateMatrixWorld(true);

  // HTML labels glued to 3D
  const apps = ["Zoom", "Teams", "Google Meet", "Discord", "Telegram"];
  apps.forEach((_, i) => {
    const el = $("app" + i), aa = back(win(t, T.call - .25 + i * .07, T.call + .15 + i * .07)) * (1 - win(t, T.bot - .5, T.bot - .25));
    const ang = t * .5 + i / apps.length * Math.PI * 2;
    project(null, V(Math.cos(ang) * 2.5, 1.3 + Math.sin(ang * 2) * .35 + (i % 2) * .5, Math.sin(ang) * 1.6 - .2), el, aa, 0, 0, .6 + .4 * clamp(aa));
  });
  project(globe, ll(...CITY.you, GR * 1.04), $("pinYou"), win(t, T.l04 - .1, T.l04 + .2) * (1 - win(t, T.can - .3, T.can - .05)), 0, -46);
  project(globe, ll(...CITY.tokyo, GR * 1.04), $("pinTokyo"), back(win(t, T.tokyo + .1, T.tokyo + .4)) * (1 - win(t, T.can - .3, T.can - .05)), 0, -46);
  project(laptop, V(optR, .3, -.88 + 5 * KP), $("keyTip"), back(win(t, T.hold - .05, T.hold + .3)) * (1 - win(t, T.let, T.let + .3)), -10, -120);
  project(lid, V(-.55, 2.4, .3), $("jaOut"), back(win(t, T.let + .2, T.let + .55)) * (1 - win(t, T.l08 - .45, T.l08 - .2)));

  bloom.strength = .55 + held * .25 + pulse(t, T.let + .2, .3) * .3;
  composer.render();
}

const ready = (async () => {
  try { await Promise.all([document.fonts.load("800 40px Mont"), document.fonts.load("700 40px Mont"), document.fonts.load("700 40px NotoJP", REPLY_JA + ASK_JA)]); } catch (e) { /* system font fallback */ }
  renderer.compile(scene, camera); renderAt(window.__hfThreeTime || 0);
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["scene"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
