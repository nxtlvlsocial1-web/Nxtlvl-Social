// The Blanket Rule, shot by shot. Times are seconds on audio/vo.wav; word cues from src/captions-data.js.
import * as THREE from "three";
import { makeDirector } from "./direct.js";
import { BED, CHAIR } from "./world.js";
import { ease, win, lerp, lerp3, clamp } from "./util.js";

const PI = Math.PI;
const bump = (u, a, b) => (u <= a || u >= b ? 0 : Math.sin(((u - a) / (b - a)) * PI));
const KID_X = -4.3, KID_Z = -3.25; // feet end of the kid lying in bed
const HEAP_STOP = [-0.6, -4.9];

export function buildShots(ctx) {
  const D = makeDirector(ctx);
  const { C, W, pipe } = ctx;
  const P = W.props;
  const S = [];
  const shot = (t0, t1, run) => S.push({ t0, t1, run });
  const kid = C.kid;
  const _v = new THREE.Vector3(), _q = new THREE.Quaternion(), _down = new THREE.Vector3(0, -1, 0);

  // ---- kid in bed -------------------------------------------------------------
  function lie({ legOut = 0, face = "sleep", faceOpts } = {}) {
    D.place(kid, KID_X, 3.85, KID_Z, 0);
    kid.root.rotation.x = -PI / 2;
    kid.j.legR.rotation.order = "ZXY";
    kid.j.legR.rotation.set(0.95 * legOut, 0, 1.25 * legOut);
    kid.j.armL.rotation.z = -0.08;
    kid.j.armR.rotation.z = 0.08;
    kid.setFace(face, faceOpts);
    return kid;
  }
  const ankle = () => D.wpos(kid.j.legR, [0, -1.7, 0]);
  const kHead = () => D.wpos(kid.j.head, [0, 0.62, 0]);
  function blanketOn() {
    P.blanket.position.set(BED.x + 0.3, 4.45, -4.1);
  }
  function blanketFloor() {
    P.blanket.position.set(-0.4, 0.32, -0.8);
    P.blanket.rotation.set(0.08, 0.55, 0.05);
    P.blanket.scale.set(0.72, 1.4, 0.58);
  }
  function blanketLump(tremble = 0, t = 0) {
    P.blanket.position.set(BED.x + 0.7, 4.6, -6.4);
    P.blanket.rotation.set(0, 0.1, 0);
    P.blanket.scale.set(0.62 + Math.sin(t * 31) * 0.006 * tremble, 3.4, 0.6);
    kid.root.visible = false;
  }
  // ---- the helper's cold arm --------------------------------------------------
  function reach(target, ext = 1, grip = 1) {
    const l = P.lint;
    l.shoulder.visible = true;
    l.root.updateWorldMatrix(true, true);
    const sp = D.wpos(l.shoulder);
    _v.set(target[0] - sp[0], target[1] - sp[1], target[2] - sp[2]);
    const dist = Math.max(0.3, _v.length() * ext);
    _q.copy(l.root.quaternion).invert();
    _v.applyQuaternion(_q).normalize();
    l.shoulder.quaternion.setFromUnitVectors(_down, _v);
    l.arm.scale.y = dist;
    l.arm.position.y = -dist / 2;
    l.hand.position.y = -dist + 0.05;
    l.fingers.forEach((f) => (f.rotation.x = 1.5 * grip));
  }
  // ---- the clothes heap ------------------------------------------------------------
  function heap(x, z, s, walkPh = null) {
    const h = P.heap;
    h.root.position.set(x, 0, z);
    h.pose(s);
    if (walkPh !== null) {
      const sw = Math.sin(walkPh);
      h.j.legs[0].rotation.x = sw * 0.35;
      h.j.legs[1].rotation.x = -sw * 0.35;
      h.j.arms[0].rotation.x = -sw * 0.15;
      h.j.arms[1].rotation.x = sw * 0.15;
      h.j.pelvis.position.y += Math.abs(Math.cos(walkPh)) * 0.12;
    }
    return h;
  }
  const heapHead = () => D.wpos(P.heap.j.head, [0, 1.0, 0.6]);

  // ==========================================================================
  // F01 hook: the foot hanging off the bed; eyes open in the dark beneath
  shot(0, 4.01, (u, d) => {
    D.lights("night", 0, { fill: [-0.5, 3, 1.5, 70] });
    lie({ legOut: 1 });
    blanketFloor();
    const eyes = win(u, 3.35, 3.6);
    P.lint.faceMat.emissiveIntensity = 0.75 * eyes;
    P.lint.faceMat.opacity = 1;
    const a = ankle();
    D.cam({ p: [[1.6, 2.7, 1.2], [1.0, 2.55, 0.4]], l: [a[0] - 1.0, a[1] - 0.9, a[2] - 0.6], f: a, fov: 42, ap: 12, seed: 1 }, u, d);
  });
  // F02 I always thought it was just something kids say (cozy, tucked in)
  shot(4.01, 6.45, (u, d) => {
    D.lights("night", 0, { fill: [2, 8, 4, 60] });
    lie({ face: "sleep" });
    blanketOn();
    P.clock.set("11:48");
    P.lint.faceMat.emissiveIntensity = 0;
    D.cam({ p: [[9.0, 8.4, 7.4], [8.3, 8.0, 6.4]], l: [-3.5, 3.4, -5.6], fov: 48, ap: 4, seed: 2 }, u, d);
  });
  // F03a so hot: the fan whirs, the kid sweats
  shot(6.45, 8.2, (u, d, t) => {
    D.lights("night", 0, { fill: [1, 6, -4, 90] });
    lie({ face: "squeeze", faceOpts: { sweat: true } });
    blanketOn();
    P.clock.set("11:48");
    P.lint.faceMat.emissiveIntensity = 0;
    P.fanBlades.rotation.z = t * 22;
    const h = kHead();
    D.cam({ p: [[h[0] + 0.3, h[1] + 4.6, h[2] + 1.9], [h[0] + 0.25, h[1] + 4.1, h[2] + 1.7]], l: [h[0], h[1], h[2] + 1.2], up: [0, 0, -1], fov: 42, ap: 8, seed: 3 }, u, d);
  });
  // F03b …I kicked my blanket off (top-down)
  shot(8.2, 10.19, (u, d, t) => {
    D.lights("night", 0, { fill: [-4, 9, -3, 80] });
    const k = lie({ face: "squeeze", faceOpts: { sweat: true } });
    P.clock.set("11:48");
    P.lint.faceMat.emissiveIntensity = 0;
    const kick = win(u, 0.1, 0.6, ease.out);
    k.j.legL.rotation.x = -Math.abs(Math.sin(u * 14)) * 0.5 * (1 - win(u, 0.6, 0.8));
    k.j.legR.rotation.x = -Math.abs(Math.cos(u * 14)) * 0.5 * (1 - win(u, 0.6, 0.8));
    const pOn = [BED.x + 0.3, 4.45, -4.1], pOff = [-0.4, 0.32, -0.8];
    const pp = lerp3(pOn, pOff, kick);
    P.blanket.position.set(pp[0], pp[1] + Math.sin(kick * PI) * 2.5, pp[2]);
    P.blanket.rotation.set(kick * 0.08, kick * 0.55, kick * 0.05 + Math.sin(kick * PI) * 0.6);
    P.blanket.scale.set(lerp(1, 0.72, kick), lerp(1, 1.4, kick), lerp(1, 0.58, kick));
    D.cam({ p: [[-3.6, 10.5, -4.6], [-3.6, 10.2, -4.8]], l: [-3.4, 3.4, -5.2], up: [0, 0, -1], fov: 64, ap: 3, seed: 4 }, u, d);
  });
  // F04 3:07
  shot(10.19, 12.66, (u, d) => {
    D.lights("night", 0, { fill: [-2.6, 3.4, -6.4, 30] });
    lie({ legOut: 1 });
    blanketFloor();
    P.clock.set(u < 0.48 ? "3:06" : "3:07");
    D.cam({ p: [[-2.95, 3.35, -6.0], [-2.6, 3.3, -6.55]], l: [-1.5, 3.23, -8.1], f: [-1.5, 3.23, -8.1], fov: 30, ap: 16, seed: 5 }, u, d);
  });
  // F05 my foot was hanging off the bed
  shot(12.66, 14.72, (u, d) => {
    D.lights("night", 0, { fill: [0, 3, 2, 60] });
    lie({ legOut: 1 });
    blanketFloor();
    P.lint.faceMat.emissiveIntensity = 0;
    const a = ankle();
    D.cam({ p: [[3.2, 1.2, 1.8], [2.7, 1.15, 1.2]], l: [a[0] - 0.3, a[1] - 0.5, a[2]], f: a, fov: 40, ap: 10, seed: 6 }, u, d);
  });
  // F06 and something cold was holding my ankle
  shot(14.72, 17.83, (u, d) => {
    D.lights("night", 0, { fill: [-0.4, 2.2, -1.6, 60], fillColor: "#9fc0ff" });
    lie({ legOut: 1 });
    blanketFloor();
    P.lint.faceMat.emissiveIntensity = 0;
    const a = ankle();
    const ext = win(u, 0.2, 0.75, ease.out);
    reach(a, ext, win(u, 0.7, 0.95));
    D.cam({ p: [[0.2, 1.4, -0.9], [-0.1, 1.45, -1.3]], l: [a[0] - 0.5, a[1] - 0.3, a[2] - 0.3], f: a, fov: 36, ap: 14, seed: 7 }, u, d);
  });
  // F07 so I pretended to be asleep (top-down on the pillow)
  shot(17.83, 21.49, (u, d) => {
    D.lights("night", 0, { fill: [-4.4, 8, -7, 90] });
    lie({ legOut: 1, face: u > 2.0 && u < 2.9 ? "peek" : "squeeze", faceOpts: { sweat: true } });
    blanketFloor();
    const h = kHead();
    D.cam({ p: [[h[0] + 0.3, h[1] + 3.6, h[2] + 0.8], [h[0] + 0.25, h[1] + 3.1, h[2] + 0.7]], l: h, up: [0, 0, -1], fov: 34, ap: 12, seed: 8 }, u, d);
  });
  // F08 the pile of clothes on my chair looked like a person (kid's POV)
  shot(21.49, 25.41, (u, d) => {
    D.lights("night", 0, { fill: [5.5, 6.5, -6.5, 90], fillColor: "#9fb4ff" });
    lie({ legOut: 1 });
    blanketFloor();
    heap(CHAIR.x, CHAIR.z, 0).j.head.rotation.y = 0.7;
    const hh = heapHead();
    D.cam({ p: [[-4.0, 4.9, -7.6], [-3.7, 4.85, -7.4]], l: [hh[0], hh[1] - 1.6, hh[2]], f: hh, fov: 40, ap: 8, seed: 9 }, u, d);
  });
  // F09 like it always does
  shot(25.41, 27.13, (u, d) => {
    D.lights("night", 0, { fill: [5.5, 6.5, -6.5, 110], fillColor: "#9fb4ff" });
    heap(CHAIR.x, CHAIR.z, 0).j.head.rotation.y = 0.7;
    const hh = heapHead();
    D.cam({ p: [[1.6, 4.6, -2.6], [2.2, 4.6, -2.9]], l: [hh[0], hh[1] - 1.6, hh[2]], f: hh, fov: 38, ap: 8, seed: 10 }, u, d);
  });
  // F10 except tonight, it turned its head
  shot(27.13, 29.73, (u, d) => {
    D.lights("night", 0, { fill: [5.8, 6.5, -6.8, 120], fillColor: "#9fb4ff" });
    const h = heap(CHAIR.x, CHAIR.z, 0);
    const turn = win(u, 0.75, 1.5, ease.inOut);
    h.j.head.rotation.y = lerp(0.7, 0, turn);
    h.j.head.rotation.x = lerp(0.55, 0.05, turn);
    h.j.head.rotation.z = lerp(0.35, 0, turn);
    h.eyeMat.emissiveIntensity = 4 * win(u, 1.35, 1.6);
    const hh = heapHead();
    D.cam({ p: [[3.9, 5.4, -4.4], [4.5, 5.5, -4.6]], l: [hh[0], hh[1] - 0.3, hh[2]], f: hh, fov: 34, ap: 12, seed: 11, shake: 0.03 + bump(u, 1.35, 1.8) * 0.05 }, u, d);
  });
  // F11 the cold hand squeezed my ankle. Once. Twice.
  shot(29.73, 33.49, (u, d) => {
    D.lights("night", 0, { fill: [-0.6, 2.2, -1.4, 60], fillColor: "#9fc0ff" });
    lie({ legOut: 1 });
    blanketFloor();
    P.lint.faceMat.emissiveIntensity = 0;
    const sq = Math.max(bump(u, 2.03, 2.4), bump(u, 2.67, 3.04));
    const a = ankle();
    reach(a, 1, 1 + sq * 0.35);
    kid.j.legR.rotation.x += sq * 0.05;
    D.cam({ p: [[-0.4, 1.9, -1.6], [-0.6, 1.95, -1.8]], l: a, f: a, fov: 30, ap: 16, seed: 12 }, u, d);
  });
  // F12 then a tiny voice under my bed whispered (eyes open in the dark)
  shot(33.49, 36.0, (u, d) => {
    D.lights("night", 0, { dark: true, fill: [-1.5, 0.8, -4.0, 25], fillColor: "#7f9cff" });
    lie({ legOut: 1 });
    blanketFloor();
    const l = P.lint;
    const open = win(u, 0.9, 1.15);
    l.faceMat.map = l.faceMat.emissiveMap = open > 0.5 ? l.faceAwake : l.faceSleep;
    l.faceMat.emissiveIntensity = 0.25 + 0.6 * open;
    reach(ankle(), 1, 1);
    const lp = D.wpos(l.root, [0, 0.7, 0]);
    D.cam({ p: [[-0.6, 0.75, -4.0], [-1.2, 0.72, -4.1]], l: lp, f: lp, fov: 36, ap: 10, seed: 13 }, u, d);
  });
  // F13 "Pull your foot in. It's coming."
  shot(36.0, 38.17, (u, d) => {
    D.lights("night", 0, { dark: true, fill: [-1.8, 0.9, -4.0, 35], fillColor: "#7f9cff" });
    lie({ legOut: 1 });
    blanketFloor();
    const l = P.lint;
    l.root.position.y = Math.abs(Math.sin(u * 6)) * 0.06;
    l.root.rotation.z = Math.sin(u * 5) * 0.05;
    reach(ankle(), 1, 1);
    const lp = D.wpos(l.root, [0, 0.75, 0]);
    D.cam({ p: [[-0.9, 0.85, -3.5], [-1.2, 0.82, -3.65]], l: lp, f: lp, fov: 36, ap: 12, seed: 14 }, u, d);
  });
  // F14a the hand wasn't grabbing me… (eyes snap open)
  shot(38.17, 39.5, (u, d) => {
    D.lights("night", 0, { fill: [-4.4, 8, -7, 90] });
    lie({ legOut: 1, face: u < 0.12 ? "squeeze" : "shock", faceOpts: { sweat: true } });
    blanketFloor();
    const h = kHead();
    D.cam({ p: [[h[0] + 0.25, h[1] + 2.8, h[2] + 0.7], [h[0] + 0.22, h[1] + 2.5, h[2] + 0.62]], l: h, up: [0, 0, -1], fov: 34, ap: 12, seed: 15, shake: 0.03 + bump(u, 0.1, 0.4) * 0.05 }, u, d);
  });
  // F14b …it was warning me (the hand lets go)
  shot(39.5, 41.27, (u, d) => {
    D.lights("night", 0, { fill: [-0.4, 2.2, -1.6, 60], fillColor: "#9fc0ff" });
    lie({ legOut: 1 });
    blanketFloor();
    P.lint.faceMat.emissiveIntensity = 0;
    const a = ankle();
    reach(a, 1 - win(u, 0.6, 1.5, ease.in) * 0.85, 1 - win(u, 0.1, 0.5));
    D.cam({ p: [[0.2, 1.4, -0.9], [0.0, 1.42, -1.1]], l: [a[0] - 0.6, a[1] - 0.4, a[2] - 0.3], f: a, fov: 36, ap: 14, seed: 16 }, u, d);
  });
  // F15 I yanked my foot under the blanket
  shot(41.27, 43.26, (u, d, t) => {
    D.lights("night", 0, { fill: [2, 6, 3, 70] });
    const yank = win(u, 0.05, 0.25, ease.out);
    const k = lie({ legOut: 1 - yank, face: "scared", faceOpts: { sweat: true } });
    const fly = win(u, 0.25, 0.75, ease.inOut);
    if (fly < 1) {
      const from = [-0.4, 0.32, -0.8], to = [BED.x + 0.7, 4.6, -6.4];
      const pp = lerp3(from, to, fly);
      P.blanket.position.set(pp[0], pp[1] + Math.sin(fly * PI) * 2.2, pp[2]);
      P.blanket.rotation.set(0.08 * (1 - fly), 0.55 * (1 - fly) + 0.1 * fly, Math.sin(fly * PI) * 0.5);
      P.blanket.scale.set(lerp(0.72, 0.62, fly), lerp(1.4, 3.4, fly), lerp(0.58, 0.6, fly));
      if (fly > 0.85) k.root.visible = false;
    } else blanketLump(1, t);
    D.cam({ p: [[2.6, 6.2, 3.6], [2.3, 6.0, 3.1]], l: [-4.8, 3.8, -5.0], fov: 46, ap: 5, seed: 17, shake: 0.03 + bump(u, 0.05, 0.4) * 0.06 }, u, d);
  });
  // F16 the clothes stood up, walked to my bed, and stopped
  shot(43.26, 46.41, (u, d, t) => {
    D.lights("night", 0, { fill: [2, 7, 0, 50] });
    blanketLump(1, t);
    const s = win(u, 0.45, 1.05, ease.inOut);
    const w = win(u, 1.15, 2.3, ease.inOut);
    const h = heap(lerp(CHAIR.x, HEAP_STOP[0], w), lerp(CHAIR.z, HEAP_STOP[1], w), s, w > 0 && w < 1 ? u * 6.5 : null);
    h.eyeMat.emissiveIntensity = 4;
    if (u > 2.3) h.j.head.rotation.x = 0.35 * win(u, 2.3, 2.8);
    D.cam({ p: [[-3.4, 3.8, 2.2], [-3.2, 3.9, 1.8]], l: [[4.5, 4.6, -5], [1.0, 5.6, -4.8]], fov: 50, ap: 4, seed: 18 }, u, d);
  });
  // F17 it stood there all night. Watching. (time-lapse)
  shot(46.41, 49.07, (u, d, t) => {
    const k = u / d;
    D.lights("dawn", k * 0.3, { fill: [4, 7, 2, 40] });
    blanketLump(1, t);
    const h = heap(HEAP_STOP[0], HEAP_STOP[1], 1);
    h.eyeMat.emissiveIntensity = 4;
    h.j.head.rotation.x = 0.35;
    P.clock.set(["3:12", "3:48", "4:31", "5:14", "5:58"][Math.min(4, Math.floor(k * 5))]);
    D.cam({ p: [[10.5, 7.8, 6.5], [10.2, 7.6, 6.2]], l: [-2.0, 4.2, -5.0], fov: 52, ap: 3, seed: 19 }, u, d);
  });
  // F18 at sunrise, it folded itself back into a pile
  shot(49.07, 52.53, (u, d, t) => {
    const k = 0.3 + 0.7 * win(u, 0, 1.0);
    D.lights("dawn", k);
    W.dust.visible = true;
    blanketLump(0.4, t);
    P.clock.set("6:12");
    const back = win(u, 0.3, 1.5, ease.inOut);
    const sit = win(u, 1.6, 2.7, ease.inOut);
    const h = heap(lerp(HEAP_STOP[0], CHAIR.x, back), lerp(HEAP_STOP[1], CHAIR.z, back), 1 - sit, back > 0 && back < 1 ? u * 6 : null);
    h.root.rotation.y = back > 0 && back < 1 ? PI / 2 : -PI / 2;
    h.eyeMat.emissiveIntensity = 4 * (1 - win(u, 0.0, 0.5));
    if (sit > 0) h.j.head.rotation.y = 0.7 * sit;
    D.cam({ p: [[-3.6, 5.0, 2.6], [-3.3, 5.0, 2.2]], l: [5.5, 3.8, -5.2], fov: 46, ap: 4, seed: 20 }, u, d);
  });
  // F19 under my bed, I found a tiny note
  shot(52.53, 55.0, (u, d) => {
    D.lights("dawn", 1, { fill: [-1.2, 1.4, -4.4, 80], fillColor: "#ffd6ad" });
    P.clock.set("7:30");
    D.place(kid, -0.9, 0, -4.6, -PI / 2);
    kid.setFace("shock");
    kid.j.legL.rotation.x = kid.j.legR.rotation.x = 1.5;
    kid.j.pelvis.position.y = 0.95;
    kid.j.torso.rotation.x = 1.45;
    kid.j.head.rotation.x = -1.25;
    kid.j.armL.rotation.x = kid.j.armR.rotation.x = -2.6;
    P.note.visible = true;
    P.note.position.set(-3.3, 0.04, -4.5);
    P.note.rotation.set(-PI / 2, 0, 0.3);
    const l = P.lint;
    l.faceMat.map = l.faceMat.emissiveMap = l.faceSleep;
    l.mask.visible = true;
    l.root.position.z = -7.0;
    const h = kHead();
    D.cam({ p: [[-6.6, 0.7, -3.8], [-6.3, 0.7, -3.9]], l: [h[0] + 0.5, h[1] - 0.5, h[2]], f: h, fov: 42, ap: 6, seed: 21 }, u, d);
  });
  // F20a the note
  shot(55.0, 56.9, (u, d) => {
    D.lights("dawn", 1, { fill: [-1.2, 3, -4.4, 35], fillColor: "#ffe6c8" });
    P.note.visible = true;
    P.note.position.set(-1.2, 0.04, -4.4);
    P.note.rotation.set(-PI / 2, 0, 0);
    D.cam({ p: [[-1.18, 3.9, -4.32], [-1.18, 3.5, -4.35]], l: [-1.18, 0, -4.4], up: [0, 0, -1], fov: 40, ap: 3, f: [-1.2, 0.04, -4.4], seed: 22 }, u, d);
  });
  // F20b …some of us are trying to sleep
  shot(56.9, 58.25, (u, d) => {
    D.lights("dawn", 1, { fill: [-1.6, 0.9, -4.0, 60], fillColor: "#ffd6ad" });
    const l = P.lint;
    l.faceMat.map = l.faceMat.emissiveMap = l.faceSleep;
    l.mask.visible = true;
    l.root.scale.y = 1 + Math.sin(u * 4) * 0.03;
    P.note.visible = true;
    P.note.position.set(-3.0, 0.04, -4.5);
    const lp = D.wpos(l.root, [0, 0.7, 0]);
    D.cam({ p: [[-1.7, 0.8, -3.8], [-1.95, 0.78, -3.9]], l: lp, f: lp, fov: 36, ap: 12, seed: 23 }, u, d);
  });
  // END CARD: morning, feet tucked in
  shot(58.25, 61.6, (u, d) => {
    D.lights("dawn", 1);
    W.dust.visible = true;
    D.place(kid, KID_X, 0, -7.6, 0);
    D.sit(kid, 3.2);
    kid.j.torso.rotation.x = -0.1;
    kid.setFace("grin");
    P.blanket.position.set(BED.x + 0.3, 4.15, -3.9);
    P.clock.set("7:30");
    heap(CHAIR.x, CHAIR.z, 0).j.head.rotation.y = 0.7;
    pipe.grade.uniforms.uFade.value = 0.4 * win(u, 0.4, 0.8);
    D.cam({ p: [[3.6, 6.4, 1.6], [3.3, 6.3, 1.2]], l: [-4.2, 5.0, -7.4], fov: 50, ap: 3, seed: 24 }, u, d);
  });

  // COVER (thumbnail still, past the end)
  shot(200, 210, (u, d) => {
    D.lights("night", 0, { fill: [1.5, 4, -1, 80], fillColor: "#9fc0ff" });
    lie({ legOut: 1, face: "scared", faceOpts: { sweat: true } });
    blanketFloor();
    reach(ankle(), 1, 1);
    const h = heap(CHAIR.x - 3.5, CHAIR.z + 0.4, 1);
    h.eyeMat.emissiveIntensity = 4;
    const a = ankle();
    D.cam({ p: [1.6, 1.5, 0.8], l: [0.5, 4.6, -4.2], f: a, fov: 58, ap: 5, shake: 0, seed: 99 }, 0, 1);
  });

  return S;
}
