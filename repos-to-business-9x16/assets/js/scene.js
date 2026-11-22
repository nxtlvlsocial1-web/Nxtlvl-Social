// AI.NXTLVL "6 free GitHub projects you can turn into businesses" (9:16). The 3D scene is a pure function of time t,
// rendered on HyperFrames' hf-seek. Beats come from window.RB_T (build/generate.py, from the voice's word timings).
//   hook:  six repo cubes tumble into a 3x2 grid
//   items: each repo cube drops in, its lid flips open and a small diorama grows out of it; on the business line the
//          cube glows; then it shrinks away to its slot in the shelf (HTML, top)
//            1 AutoClip     a long film strip feeds in, three vertical phone clips pop out of it
//            2 Remotion     code bars stack up, then a conveyor prints video cards
//            3 OpenHands    a laptop types code, three app tiles pop around it
//            4 PersonaLive  a photo card drives a low-poly avatar head in a ring light, LIVE badge
//            5 RedInk       an ink drop falls and splashes into a post card that fills in
//            6 MuMuAINovel  a book opens, pages fan, chapter cards rise
//   close: the six cubes drop into a shipping box; the flaps shut on "packaging"; a price tag swings out
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";

const W = 1080, H = 1920;
const T = window.RB_T;
const ACC = [0xff4d6d, 0x3d8bff, 0x9b5cff, 0x22d3ee, 0xff3b30, 0xf5b941];   // per repo
const VIOLET = 0x7a2ffb, LAV = 0xb687f9, NIGHT = 0x07050f;
const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H, false); renderer.setPixelRatio(1); renderer.setClearColor(NIGHT, 1);
renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping;
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(32, W / H, .1, 80);
const composer = new EffectComposer(renderer);
composer.setSize(W, H);
composer.addPass(new RenderPass(scene, camera));
composer.addPass(new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), .55, .5, .45));
composer.addPass(new OutputPass());
scene.add(new THREE.HemisphereLight(0xe8dcff, 0x140828, 1.1));
const key = new THREE.DirectionalLight(0xffffff, 2.4); key.position.set(3, 6, 7); scene.add(key);
const fill = new THREE.PointLight(VIOLET, 40, 16); fill.position.set(-4, 2, 3); scene.add(fill);
const accLight = new THREE.PointLight(0xffffff, 0, 12); accLight.position.set(2.5, -.5, 3.5); scene.add(accLight);

// ---------------------------------------------------------------- helpers
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const win = (t, a, b) => clamp((t - a) / (b - a));
const ease = (x) => 1 - Math.pow(1 - clamp(x), 3);
const easeIO = (x) => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const back = (x) => { x = clamp(x); const c = 1.8; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const lerp = (a, b, x) => a + (b - a) * x;
const pop = (t, a, d = .35) => back(win(t, a, a + d));
const std = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: .35, metalness: .25, ...o });
const glow = (color, ei = 1.2) => new THREE.MeshStandardMaterial({ color, emissive: color, emissiveIntensity: ei, roughness: .4 });
const rbox = (w, h, d, r = .06, m) => new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 4, r), m);
function show(o, s) { o.visible = s > .002; o.scale.setScalar(Math.max(.002, s)); }

// background: a far plane painted with the brand's violet glows
function bgTexture() {
  const c = document.createElement("canvas"); c.width = 540; c.height = 960; const g = c.getContext("2d");
  g.fillStyle = "#07050f"; g.fillRect(0, 0, 540, 960);
  for (const [x, y, r, col] of [[60, 120, 420, "rgba(127,27,248,.55)"], [500, 860, 460, "rgba(96,8,242,.5)"], [270, 520, 300, "rgba(122,47,251,.18)"]]) {
    const rg = g.createRadialGradient(x, y, 0, x, y, r); rg.addColorStop(0, col); rg.addColorStop(1, "rgba(7,5,15,0)");
    g.fillStyle = rg; g.fillRect(0, 0, 540, 960);
  }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
const bg = new THREE.Mesh(new THREE.PlaneGeometry(28, 50), new THREE.MeshBasicMaterial({ map: bgTexture(), fog: false }));
bg.position.z = -14; scene.add(bg);
// dust
const DN = 140, dust = new Float32Array(DN * 3);
const dustGeo = new THREE.BufferGeometry(); dustGeo.setAttribute("position", new THREE.BufferAttribute(dust, 3));
scene.add(new THREE.Points(dustGeo, new THREE.PointsMaterial({ color: LAV, size: .03, transparent: true, opacity: .6 })));
const rnd = (i, k = 1) => { const s = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return s - Math.floor(s); };

// ---------------------------------------------------------------- repo cubes (face label: number + accent)
function faceTex(n, col) {
  const c = document.createElement("canvas"); c.width = c.height = 256; const g = c.getContext("2d");
  g.fillStyle = "#120a24"; g.fillRect(0, 0, 256, 256);
  g.strokeStyle = "#" + col.toString(16).padStart(6, "0"); g.lineWidth = 10; g.strokeRect(14, 14, 228, 228);
  g.fillStyle = "#" + col.toString(16).padStart(6, "0"); g.font = "800 120px Mont, sans-serif"; g.textAlign = "center"; g.textBaseline = "middle";
  g.fillText(String(n).padStart(2, "0"), 128, 118);
  g.fillStyle = "#b687f9"; g.font = "700 26px Mono, monospace"; g.fillText("GITHUB", 128, 205);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
const cubes = [];
function makeCube(k) {
  const g = new THREE.Group(); scene.add(g);
  const body = rbox(1, .82, 1, .08, std(0x1a1030, { metalness: .5, roughness: .3, emissive: ACC[k], emissiveIntensity: .08 }));
  body.position.y = -.09; g.add(body);
  const face = new THREE.Mesh(new THREE.PlaneGeometry(.78, .64), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .5 }));
  face.position.set(0, -.09, .505); g.add(face);
  const hinge = new THREE.Group(); hinge.position.set(0, .32, -.5); g.add(hinge);
  const lid = rbox(1.02, .16, 1.02, .06, std(ACC[k], { emissive: ACC[k], emissiveIntensity: .25 })); lid.position.set(0, 0, .5); hinge.add(lid);
  const rim = new THREE.Mesh(new THREE.TorusGeometry(.72, .015, 8, 64), new THREE.MeshBasicMaterial({ color: ACC[k], transparent: true, opacity: .6 }));
  rim.rotation.x = Math.PI / 2; rim.position.y = -.5; g.add(rim);
  const c = { g, body, face, hinge, lid, rim, k }; cubes.push(c); return c;
}
for (let k = 0; k < 6; k++) makeCube(k);

// ---------------------------------------------------------------- dioramas
const D = [];
// 1 AutoClip: film strip + three phone clips
{
  const g = new THREE.Group(); scene.add(g);
  const strip = new THREE.Group(); g.add(strip);
  strip.add(rbox(4.4, .42, .05, .02, std(0x101018)));
  for (let i = 0; i < 18; i++) {
    const f = rbox(.2, .26, .02, .02, glow([0xff4d6d, 0xffb020, 0x3d8bff, 0x22d3ee][i % 4], .55)); f.position.set(-2.05 + i * .24, 0, .04); strip.add(f);
  }
  const phones = [0, 1, 2].map((i) => {
    const p = new THREE.Group(); g.add(p);
    p.add(rbox(.52, .94, .06, .07, std(0x0d0d14, { metalness: .6 })));
    const scr = rbox(.46, .84, .02, .05, glow([0xff4d6d, 0xffb020, 0x3d8bff][i], .7)); scr.position.z = .04; p.add(scr);
    const tri = new THREE.Mesh(new THREE.CircleGeometry(.12, 3), new THREE.MeshBasicMaterial({ color: 0xffffff })); tri.position.z = .06; p.add(tri);
    return p;
  });
  D.push({ g, strip, phones });
}
// 2 Remotion: code bars + conveyor of video cards
{
  const g = new THREE.Group(); scene.add(g);
  const bars = []; for (let i = 0; i < 6; i++) { const w = .5 + rnd(i, 3) * .9; const b = rbox(w, .12, .12, .04, glow([0x3d8bff, 0x9b5cff, 0x22d3ee][i % 3], .8)); b.userData.w = w; g.add(b); bars.push(b); }
  const belt = rbox(3.6, .1, .7, .04, std(0x1c1636, { metalness: .6 })); belt.position.y = -.95; g.add(belt);
  const cards = []; for (let i = 0; i < 5; i++) {
    const c = new THREE.Group(); g.add(c);
    c.add(rbox(.62, .4, .04, .04, std(0xf4f0ff)));
    const im = rbox(.54, .28, .02, .03, glow([0x3d8bff, 0xff4d6d, 0xf5b941, 0x22d3ee, 0x9b5cff][i], .6)); im.position.z = .03; c.add(im);
    cards.push(c);
  }
  D.push({ g, bars, cards });
}
// 3 OpenHands: laptop + typing lines + app tiles
{
  const g = new THREE.Group(); scene.add(g);
  const base = rbox(1.7, .07, 1.1, .03, std(0x2a2440, { metalness: .7 })); g.add(base);
  const sh = new THREE.Group(); sh.position.set(0, .03, -.55); g.add(sh);
  const scr = rbox(1.7, 1.08, .05, .04, std(0x0b0817)); scr.position.set(0, .54, 0); sh.add(scr);
  const lines = []; for (let i = 0; i < 6; i++) {
    const l = rbox(1, .06, .01, .02, glow(i % 2 ? 0x9b5cff : 0x22d3ee, .9)); l.position.set(-.6, .92 - i * .13, .035); sh.add(l); lines.push(l);
  }
  const tiles = [0xff4d6d, 0xf5b941, 0x3d8bff].map((c) => { const tl = rbox(.46, .46, .08, .09, glow(c, .55)); g.add(tl); return tl; });
  D.push({ g, sh, lines, tiles });
}
// 4 PersonaLive: photo card -> low-poly head in a ring light, LIVE badge
{
  const g = new THREE.Group(); scene.add(g);
  const photo = new THREE.Group(); g.add(photo);
  photo.add(rbox(.72, .9, .03, .03, std(0xf4f0ff)));
  const ph = rbox(.6, .66, .02, .02, std(0x22d3ee, { emissive: 0x22d3ee, emissiveIntensity: .3 })); ph.position.set(0, .07, .02); photo.add(ph);
  const head = new THREE.Group(); g.add(head);
  head.add(new THREE.Mesh(new THREE.IcosahedronGeometry(.48, 1), new THREE.MeshStandardMaterial({ color: 0xf2c6a6, flatShading: true, roughness: .6 })));
  const hair = new THREE.Mesh(new THREE.IcosahedronGeometry(.5, 1), new THREE.MeshStandardMaterial({ color: 0x2b1a3d, flatShading: true }));
  hair.scale.set(1.03, .5, 1.03); hair.position.set(0, .3, -.04); head.add(hair);
  const eyes = [-1, 1].map((s) => { const e = new THREE.Mesh(new THREE.SphereGeometry(.055, 12, 8), new THREE.MeshBasicMaterial({ color: 0x14062e })); e.position.set(.17 * s, .02, .43); head.add(e); return e; });
  const mouth = rbox(.16, .04, .02, .015, new THREE.MeshBasicMaterial({ color: 0x8a2a3a })); mouth.position.set(0, -.2, .45); head.add(mouth);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(.78, .05, 12, 80), glow(0x22d3ee, 1.4)); g.add(ring);
  const live = rbox(.5, .2, .05, .05, glow(0xff2d55, 1.3)); g.add(live);
  D.push({ g, photo, head, eyes, mouth, ring, live });
}
// 5 RedInk: ink drop, splash ring, post card filling in
{
  const g = new THREE.Group(); scene.add(g);
  const drop = new THREE.Mesh(new THREE.SphereGeometry(.16, 24, 16), glow(0xff3b30, 1)); g.add(drop);
  const splash = new THREE.Mesh(new THREE.TorusGeometry(.3, .03, 8, 48), new THREE.MeshBasicMaterial({ color: 0xff3b30, transparent: true })); splash.rotation.x = -Math.PI / 2; g.add(splash);
  const card = new THREE.Group(); g.add(card);
  card.add(rbox(1.15, 1.5, .04, .06, std(0xfff7f2)));
  const img = rbox(1, .72, .02, .04, std(0xff3b30, { emissive: 0xff3b30, emissiveIntensity: .25 })); img.position.set(0, .3, .03); card.add(img);
  const txt = [0, 1, 2].map((i) => { const b = rbox(.9 - i * .2, .07, .01, .02, new THREE.MeshBasicMaterial({ color: 0x3a2a30 })); b.position.set(-(.2 * i) / 2, -.26 - i * .14, .03); card.add(b); return b; });
  const heart = new THREE.Mesh(new THREE.SphereGeometry(.07, 12, 8), glow(0xff3b30, 1.2)); heart.position.set(.42, -.6, .04); card.add(heart);
  D.push({ g, drop, splash, card, img, txt, heart });
}
// 6 MuMuAINovel: a book that opens, pages fan, chapter cards rise
{
  const g = new THREE.Group(); scene.add(g);
  const spine = rbox(.1, 1.2, .2, .03, std(0xf5b941)); g.add(spine);
  const lc = new THREE.Group(), rc = new THREE.Group(); g.add(lc); g.add(rc);
  const coverL = rbox(.85, 1.2, .05, .03, std(0x2a1a4a, { emissive: 0xf5b941, emissiveIntensity: .12 })); coverL.position.x = -.43; lc.add(coverL);
  const coverR = coverL.clone(); coverR.position.x = .43; rc.add(coverR);
  const pages = []; for (let i = 0; i < 6; i++) { const pg = new THREE.Group(); g.add(pg); const p = rbox(.8, 1.12, .01, .01, std(0xfffbf0)); p.position.x = .41; pg.add(p); pages.push(pg); }
  const chaps = [0, 1, 2].map((i) => { const c = rbox(.7, .22, .03, .05, glow(0xf5b941, .5)); g.add(c); return c; });
  D.push({ g, lc, rc, pages, chaps });
}
// ---------------------------------------------------------------- the shipping box (close)
const box = new THREE.Group(); scene.add(box);
const boxMat = std(0xc89a5c, { roughness: .8, metalness: 0 });
box.add(rbox(1.9, 1.3, 1.5, .03, boxMat));
const flaps = [];
for (const [x, z, ry] of [[0, .75, 0], [0, -.75, Math.PI], [.95, 0, -Math.PI / 2], [-.95, 0, Math.PI / 2]]) {
  const hg = new THREE.Group(); hg.position.set(x, .65, z); hg.rotation.y = ry; box.add(hg);
  const f = rbox(ry === 0 || ry === Math.PI ? 1.9 : 1.5, .03, .72, .01, boxMat); f.position.set(0, 0, -.36); hg.add(f); flaps.push(hg);
}
const tape = rbox(.3, .012, 1.52, .005, std(0xb687f9, { emissive: VIOLET, emissiveIntensity: .4 })); tape.position.y = .67; box.add(tape);
const tag = new THREE.Group(); box.add(tag); tag.position.set(1.0, .55, .78);
const tagCard = rbox(.62, .36, .03, .05, glow(0x7a2ffb, .9)); tagCard.position.set(.32, -.26, 0); tag.add(tagCard);

// ---------------------------------------------------------------- per frame
const v3 = new THREE.Vector3();
function cubeAt(c, x, y, z, s, lidOpen, spin, glowAmt) {
  show(c.g, s); c.g.position.set(x, y, z); c.g.rotation.set(.18, spin, 0);
  c.hinge.rotation.x = -lidOpen * 2.0;
  c.body.material.emissiveIntensity = .08 + glowAmt * .9;
  c.rim.material.opacity = .25 + glowAmt * .75;
}
function renderAt(t) {
  const cam = Math.sin(t * .3) * .12;
  camera.position.set(Math.sin(cam) * 13, 1.5, Math.cos(cam) * 13); camera.lookAt(0, -.5, 0); camera.updateMatrixWorld();
  for (let i = 0; i < DN; i++) {
    dust[i * 3] = (rnd(i) - .5) * 9; dust[i * 3 + 2] = (rnd(i, 2) - .5) * 6 - 2;
    dust[i * 3 + 1] = ((rnd(i, 3) * 9 + t * (.1 + rnd(i, 4) * .2)) % 9) - 4.5;
  }
  dustGeo.attributes.position.needsUpdate = true;
  cubes.forEach((c) => (c.g.visible = false));
  D.forEach((d) => (d.g.visible = false));
  box.visible = false;
  accLight.intensity = 0;

  // ---- hook: six cubes tumble into a 3x2 grid, then clear for item 1
  const L = T.lines;
  if (t < L[1][0] + .3) {
    const out = win(t, L[1][0] - .35, L[1][0] + .1);
    for (let k = 0; k < 6; k++) {
      const t0 = .05 + k * .09, land = t0 + .5;
      const gx = ((k % 3) - 1) * 1.05, gy = k < 3 ? .25 : -.8;
      let y = t < land ? lerp(6, gy, Math.pow(win(t, t0, land), 2)) : gy + Math.abs(Math.sin((t - land) * 10)) * .18 * Math.exp(-(t - land) * 7);
      const spin = (1 - ease(win(t, t0, land + .3))) * 4 + Math.sin(t * 1.2 + k) * .25;
      cubeAt(cubes[k], gx * (1 - out), lerp(y, 5.5, out * out), 0, t > t0 ? .64 * (1 - out * .7) : 0, 0, spin, .4 + .4 * Math.sin(t * 3 + k));
    }
  }

  // ---- items
  for (let k = 0; k < 6; k++) {
    const a = L[k + 1][0], b = L[k + 2][0];                       // this item runs from its line to the next line
    if (t < a - .3 || t > b + .1) continue;
    const c = cubes[k], d = D[k], u = t - a;
    const drop = ease(win(t, a - .3, a + .25));
    const out = easeIO(win(t, b - .4, b));
    const lidOpen = easeIO(win(t, a + .2, a + .6));
    const fly = easeIO(win(t, a + .65, a + 1.15));                 // the opened cube flies up into its shelf slot
    const bizGlow = Math.exp(-Math.pow((t - T.biz[k] - .2) / .35, 2)) + (t > T.biz[k] ? .35 : 0);
    const slotX = -1.62 + k * .58;
    if (fly < 1) cubeAt(c, lerp(0, slotX, fly), lerp(lerp(5, -.45, drop), 4.15, fly * fly), lerp(0, 1.5, fly), lerp(.95, .18, fly), lidOpen, Math.sin(u * .9) * .35 + (1 - drop) * 3, .3);
    accLight.intensity = 26 * (1 - out) * (.6 + .4 * clamp(bizGlow)); accLight.color.setHex(ACC[k]);
    // diorama grows out of the open cube, then shrinks away before the next repo
    const grow = back(win(t, a + .5, a + 1.05)) * (1 - out) * .95;
    show(d.g, grow); d.g.position.set(0, lerp(-1.0, -.42, ease(win(t, a + .5, a + 1.05))), 0);
    d.g.rotation.set(0, Math.sin(u * .7) * .18, 0);
    if (k === 0) {
      d.strip.position.set(1.2 - ((u * 1.1) % 1.2), .75, 0);
      d.phones.forEach((p, i) => { const s = pop(t, a + 1.1 + i * .45); show(p, s); p.position.set((i - 1) * .72, -.3 + Math.sin(u * 2 + i) * .04, .2); p.rotation.y = (i - 1) * -.25; });
    } else if (k === 1) {
      d.bars.forEach((bb, i) => { const s = pop(t, a + .9 + i * .12, .3); show(bb, s); bb.position.set(-1.0 + bb.userData.w / 2 + (i % 2) * .2, 1.0 - i * .17, 0); });
      d.cards.forEach((cd, i) => { const ph = (u - 1.4 - i * .55); const s = ph > 0 ? 1 : 0; show(cd, s * Math.min(1, ph * 4)); cd.position.set(-1.6 + Math.min(ph, 3.2) * 1.0, -.62, .1); cd.rotation.x = -.15; });
    } else if (k === 2) {
      d.sh.rotation.x = lerp(-1.4, -.18, ease(win(t, a + .7, a + 1.2)));
      d.lines.forEach((l, i) => { const w = clamp((u - 1.1 - i * .25) / .3); l.scale.x = Math.max(.001, w * (.5 + rnd(i, 9) * .5)); l.position.x = -.65 + l.scale.x * .5; l.visible = w > 0; });
      d.tiles.forEach((tl, i) => { const s = pop(t, T.biz[k] + i * .15); show(tl, s); const ang = -.6 + i * .6; tl.position.set(Math.sin(ang) * 1.35, .95 + Math.cos(ang * 2) * .1, .4); tl.rotation.set(0, -ang * .6, 0); });
      d.g.position.y -= .25;
    } else if (k === 3) {
      d.photo.position.set(-.95, .1, 0); d.photo.rotation.y = .35;
      d.head.position.set(.55, .15, 0);
      d.head.rotation.set(Math.sin(u * 2.6) * .12, Math.sin(u * 1.7) * .35, Math.sin(u * 2.1) * .08);
      d.mouth.scale.y = 1 + Math.max(0, Math.sin(u * 9)) * 2.2;
      const blink = Math.exp(-Math.pow(((u % 2.3) - 1.8) / .05, 2)); d.eyes.forEach((e) => (e.scale.y = Math.max(.1, 1 - blink)));
      d.ring.position.set(.55, .15, -.12);
      show(d.live, pop(t, a + 1.2)); d.live.position.set(.55, -.85, .2); d.live.material.emissiveIntensity = 1 + Math.sin(u * 6) * .5;
    } else if (k === 4) {
      const fall = win(t, a + .7, a + 1.25);
      d.drop.visible = fall < 1; d.drop.position.set(0, lerp(2.2, .1, fall * fall), .3); d.drop.scale.set(1, 1 + fall * .6, 1);
      const sp = win(t, a + 1.25, a + 1.9); d.splash.visible = sp > 0 && sp < 1; d.splash.position.set(0, .1, .3); d.splash.scale.setScalar(.5 + sp * 3); d.splash.material.opacity = 1 - sp;
      show(d.card, ease(win(t, a + 1.2, a + 1.55)));
      d.card.position.set(0, -.1, 0);
      const fillp = win(t, a + 1.4, a + 2.4);
      d.img.scale.y = Math.max(.01, fillp); d.img.position.y = .3 - (1 - fillp) * .36;
      d.txt.forEach((b2, i) => { b2.scale.x = Math.max(.01, clamp(fillp * 3 - i)); });
      d.heart.scale.setScalar(Math.max(.01, pop(t, T.biz[k]) * (1 + Math.max(0, Math.sin(u * 7)) * .3)));
    } else if (k === 5) {
      const op = easeIO(win(t, a + .75, a + 1.3));
      d.lc.rotation.y = lerp(0, .25, op);                              // left cover stays, right cover swings open
      d.rc.rotation.y = -lerp(Math.PI - .05, .25, op);
      d.pages.forEach((pg, i) => { const f = clamp((u - 1.3 - i * .14) / .5); pg.rotation.y = -lerp(Math.PI - .1, .3 + i * .45, easeIO(f)); pg.visible = op > .5; });
      d.chaps.forEach((ch, i) => { const s = pop(t, T.biz[k] - .2 + i * .18); show(ch, s); ch.position.set((i - 1) * .2, 1.0 + i * .3 + Math.sin(u * 2 + i) * .04, .4); ch.rotation.set(0, 0, (i - 1) * .1); });
      d.g.rotation.x = -.35;
    }
  }

  // ---- close: cubes drop into the box, flaps shut on "packaging", the tag swings out
  const c0 = T.close;
  if (t > c0 - .2) {
    const bIn = back(win(t, c0 - .2, c0 + .35));
    const up = easeIO(win(t, T.cta - .2, T.cta + .4));
    show(box, bIn * lerp(.78, .6, up)); box.position.set(0, lerp(-.75, .05, up), 0); box.rotation.set(.12, -.5 + Math.sin(t * .5) * .1, 0);
    const shut = easeIO(win(t, T.pack, T.pack + .6));
    flaps.forEach((f, i) => { f.rotation.x = lerp(-2.1 - (i % 2) * .1, 0, shut) * (i < 2 ? 1 : 1); f.rotation.z = 0; });
    tape.visible = shut > .95;
    const tg = pop(t, T.pack + .55, .5); show(tag, tg); tag.rotation.z = Math.sin((t - T.pack) * 4) * .3 * Math.exp(-(t - T.pack) * 1.5);
    accLight.intensity = 30; accLight.color.setHex(VIOLET);
    for (let k = 0; k < 6; k++) {
      const t0 = c0 + .1 + k * .14, land = t0 + .45;
      const f = win(t, t0, land);
      const into = shut > .02;
      const gx = ((k % 3) - 1) * .5, gz = k < 3 ? .3 : -.3;
      v3.set(gx, lerp(5, 0, f * f), gz);
      const s = t > t0 && !into ? .38 : 0;
      cubeAt(cubes[k], v3.x * .78, v3.y * .78 - .75 + .2, v3.z * .78, s * .78, 0, (1 - f) * 5 + k, .6);
    }
  }
  composer.render();
}

const ready = (async () => {
  try { await document.fonts.load("800 120px Mont"); await document.fonts.load("700 26px Mono"); } catch (e) { /* fonts optional */ }
  cubes.forEach((c, k) => { c.face.material.map = faceTex(k + 1, ACC[k]); c.face.material.needsUpdate = true; });
  tagCard.material = new THREE.MeshStandardMaterial({ map: (() => {
    const cv = document.createElement("canvas"); cv.width = 256; cv.height = 150; const g = cv.getContext("2d");
    g.fillStyle = "#7a2ffb"; g.fillRect(0, 0, 256, 150); g.fillStyle = "#fff"; g.font = "800 92px Mont, sans-serif"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("$$$", 128, 80);
    const tx = new THREE.CanvasTexture(cv); tx.colorSpace = THREE.SRGBColorSpace; return tx; })(), emissive: 0x7a2ffb, emissiveIntensity: .35 });
  renderer.compile(scene, camera); renderAt(window.__hfThreeTime || 0);
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["scene"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
