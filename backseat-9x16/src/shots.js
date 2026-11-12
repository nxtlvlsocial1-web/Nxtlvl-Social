// Killer in the Backseat, shot by shot. Times are seconds on audio/vo.wav (audio/vo-lines.json).
import * as THREE from "three";
import { makeDirector } from "./direct.js";
import { DX } from "./world.js";
import { ease, win, lerp, lerp3, clamp } from "./util.js";

const PI = Math.PI;
const bump = (u, a, b) => (u <= a || u >= b ? 0 : Math.sin(((u - a) / (b - a)) * PI));
const SPEED = 15; // road units per second
const flashAt = (t, times, len = 0.42) => times.reduce((m, f) => Math.max(m, bump(t, f, f + len)), 0);

export function buildShots(ctx) {
  const D = makeDirector(ctx);
  const { C, W, pipe } = ctx;
  const P = W.props;
  const S = [];
  const shot = (t0, t1, run) => S.push({ t0, t1, run });
  const dad = C.dad, st = C.stranger, tk = C.trucker;
  const car = P.car, truck = P.truck;
  const V = new THREE.Vector3();

  // ---- the car and who is in it ----------------------------------------------------------
  function carAt(x, z, s = 0) {
    car.group.position.set(x, 0, z);
    car.wheels.forEach((w) => (w.rotation.x = -s / 1.05));
    return [x, 0, z];
  }
  const local = (c, v) => [c[0] + v[0], c[1] + v[1], c[2] + v[2]];
  function driver(c, { face = "flat", faceOpts, look = 0, lookUp = 0, shake = 0, t = 0 } = {}) {
    D.place(dad, c[0] - 1.45, 0, c[2] - 0.3, PI);
    D.sit(dad, 1.8);
    dad.setFace(face, faceOpts);
    dad.j.armL.rotation.set(-1.25, 0, 0.15);
    dad.j.armR.rotation.set(-1.25, 0, -0.15);
    dad.j.head.rotation.set(-lookUp + Math.sin(t * 31) * 0.02 * shake, look + Math.sin(t * 27) * 0.03 * shake, 0);
    return D.wpos(dad.j.head, [0, 0.62, 0]);
  }
  // the man in the back seat: up 0 = ducked below the windows, 1 = sitting up right behind the driver
  function backseat(c, up, { lean = 0, face = "shadow" } = {}) {
    D.place(st, c[0] - 1.45 + lean * 1.2, 0, c[2] + 2.6 - lean * 1.3, PI);
    D.sit(st, 1.8);
    st.root.scale.setScalar(1);
    st.setFace(face);
    st.j.pelvis.position.y = lerp(1.75, 2.85, up);
    st.j.torso.rotation.x = lerp(1.2, 0.05, up) + lean * 0.32;
    st.j.head.rotation.x = lerp(0.3, -0.05, up);
    st.j.armL.rotation.set(-0.6, 0, 0.1);
    st.j.armR.rotation.set(-0.6 - lean * 0.6, 0, -0.1);
    return D.wpos(st.j.head, [0, 0.62, 0]);
  }
  function truckAt(x, z) {
    truck.group.position.set(x, 0, z);
    return [x, 0, z];
  }
  function mirrorView(c) {
    car.mirrorOn = true;
    const m = local(c, [0, 5.55, -2.4]);
    car.mirrorCam.position.set(m[0], m[1], m[2]);
    car.mirrorCam.lookAt(c[0] - 0.75, 4.75, c[2] + 6);
    car.mirrorCam.updateMatrixWorld();
  }
  const road = (t, o = {}) => D.lights("road", 0, { at: [0, 0, 0], ...o });
  // through the windshield, long lens: his face lit by the dash, the back window behind him
  function mirrorPOV(u, d, c, { f = null, fov = 30, seed = 1, shake = 0.015, push = 0.12 } = {}) {
    const k = ease.inOut(clamp(u / d)) * push;
    D.cam({ p: local(c, [-0.55, 6.1, -11.5 + k * 3]), l: local(c, [-0.85, 5.15, 0.4]), f: f || local(c, [-1.45, 5.1, -0.3]), fov, ap: 2.5, seed, shake }, 0, 1);
  }
  // from outside the left side, both side windows in frame: driver in front, the back seat behind
  function sideView(u, d, c, { f = null, seed = 1 } = {}) {
    const k = ease.inOut(clamp(u / d));
    D.cam({ p: local(c, [-9.4 + k * 0.8, 5.4, 1.15]), l: local(c, [-1.4, 4.6, 1.15]), f: f || local(c, [-1.45, 5.0, 1.0]), fov: 48, ap: 1.6, seed, shake: 0.03 }, 0, 1);
  }
  // inside the cabin, from the dash looking back: the driver on the left, the back seat behind him
  function cabinCam(u, d, c, { f = null, fov = 50, seed = 1, shake = 0.02, push = 0.15 } = {}) {
    const k = ease.inOut(clamp(u / d)) * push;
    D.cam({ p: local(c, [0.95 - k * 0.5, 5.35, -2.45 + k]), l: local(c, [-1.45, 4.85, 1.15]), f: f || local(c, [-1.45, 5.1, -0.3]), fov, ap: 2.2, seed, shake }, 0, 1);
  }

  // ==========================================================================
  // S01 hook: high beams blasting through the back window; he squints
  shot(0, 6.26, (u, d, t) => {
    const s = SPEED * t;
    P.road.scroll(s);
    const c = carAt(0, 0, s);
    const beam = flashAt(t, [0.75, 2.45, 4.25]);
    driver(c, { face: beam > 0.3 ? "squeeze" : "worried", t });
    backseat(c, 0);
    const tp = truckAt(0, 19);
    road(t, { truck: tp, beam });
    mirrorPOV(u, d, c, { seed: 1 });
  });
  // S02 I was driving home late, on an empty country road.
  shot(6.26, 9.77, (u, d, t) => {
    const s = SPEED * t;
    P.road.scroll(s);
    const c = carAt(0, 0, s);
    driver(c, { face: "flat", t });
    backseat(c, 0);
    road(t);
    D.cam({ p: [[11, 9.5, 20], [8, 8.0, 16]], l: [0, 2.0, -10], f: [0, 3, 0], fov: 46, ap: 1.2, seed: 2 }, u, d);
  });
  // S03 A pickup truck pulled out behind me…
  shot(9.77, 14.21, (u, d, t) => {
    const s = SPEED * t;
    P.road.scroll(s);
    const c = carAt(0, 0, s);
    driver(c, { face: "worried", t });
    backseat(c, 0);
    const tz = lerp(70, 19, win(t, 10.0, 13.8, ease.out));
    const tp = truckAt(lerp(9, 0, win(t, 10.0, 11.6)), tz);
    truck.group.rotation.y = lerp(0.5, 0, win(t, 10.0, 11.6));
    road(t, { truck: tp, beam: 0 });
    D.cam({ p: [[-7.5, 3.0, -3.0], [-7.2, 3.1, -1.5]], l: [0.5, 2.6, 30], f: tp, fov: 40, ap: 2, seed: 3 }, u, d);
  });
  // S04 Every few minutes, it flashed its high beams. Right into my car.
  shot(14.21, 18.57, (u, d, t) => {
    const s = SPEED * t;
    P.road.scroll(s);
    const c = carAt(0, 0, s);
    const beam = flashAt(t, [15.5, 17.25]);
    driver(c, { face: beam > 0.3 ? "squeeze" : "worried", lookUp: 0.15, t });
    backseat(c, 0);
    const tp = truckAt(0, 17.5);
    road(t, { truck: tp, beam });
    mirrorPOV(u, d, c, { seed: 4, push: 0.2 });
  });
  // S05a I sped up. (the needle climbs)
  shot(18.57, 19.3, (u, d, t) => {
    const s = SPEED * t;
    P.road.scroll(s);
    const c = carAt(0, 0, s);
    car.needle.rotation.z = lerp(0.6, -0.9, win(t, 18.6, 19.25));
    driver(c, { t });
    road(t, { truck: truckAt(0, 17.5), beam: 0 });
    D.cam({ p: [[-1.35, 4.2, -0.6], [-1.4, 4.1, -0.75]], l: [-1.45, 3.3, -1.7], f: local(c, [-1.45, 3.35, -1.69]), fov: 30, ap: 10, seed: 5 }, u, d);
  });
  // S05b …It sped up. (side tracking, trees streaking)
  shot(19.3, 20.5, (u, d, t) => {
    const s = SPEED * 1.6 * t;
    P.road.scroll(s);
    const c = carAt(0, 0, s);
    driver(c, { face: "scared", t });
    backseat(c, 0);
    const tp = truckAt(0, 15.5);
    road(t, { truck: tp, beam: 0.15 });
    D.cam({ p: [[-15, 4.0, 6], [-15, 4.0, 3]], l: [0, 2.6, 6.5], f: [0, 3, 6], fov: 52, ap: 2, seed: 6, shake: 0.05 }, u, d);
  });
  // S06a By the time I pulled into my driveway…
  shot(20.5, 22.4, (u, d, t) => {
    const k = win(t, 20.5, 22.2, ease.out);
    const z = lerp(32, 2, k);
    const c = carAt(DX, z, (32 - z));
    driver(c, { face: "scared", t });
    backseat(c, 0);
    road(t, { at: c, porch: true, headlights: 1 });
    D.cam({ p: [[DX + 12, 5.0, -8], [DX + 11, 4.8, -7]], l: [DX, 2.5, z], f: c, fov: 44, ap: 1.5, seed: 7 }, u, d);
  });
  // S06b …I was shaking.
  shot(22.4, 23.92, (u, d, t) => {
    const c = carAt(DX, 2, 30);
    const h = driver(c, { face: "scared", faceOpts: { sweat: true }, shake: 1, t });
    backseat(c, 0);
    road(t, { at: c, porch: true, headlights: 0 });
    D.cam({ p: [[h[0] + 1.6, h[1] + 0.1, h[2] - 3.0], [h[0] + 1.4, h[1] + 0.05, h[2] - 2.6]], l: [h[0], h[1] - 0.45, h[2]], f: h, fov: 38, ap: 7, seed: 8 }, u, d);
  });
  // S07 The truck pulled in right behind me. (lights straight into the lens)
  shot(23.92, 26.25, (u, d, t) => {
    const c = carAt(DX, 2, 30);
    driver(c, { face: "scared", t });
    backseat(c, 0);
    const tp = truckAt(DX, lerp(48, 17, win(t, 23.95, 25.6, ease.out)));
    road(t, { at: c, porch: true, headlights: 0, truck: tp, beam: 0.3, aim: [DX, 2.5, 4] });
    D.cam({ p: [[DX + 5.0, 2.2, 5.0], [DX + 4.8, 2.3, 4.6]], l: [DX, 4.0, 20], f: tp, fov: 46, ap: 2, seed: 9 }, u, d);
  });
  // S08 The driver jumped out and ran at my car, yelling.
  shot(26.25, 29.25, (u, d, t) => {
    const c = carAt(DX, 2, 30);
    driver(c, { face: "scared", t });
    backseat(c, 0);
    const tp = truckAt(DX, 17);
    const k = win(t, 26.4, 28.6, ease.inOut);
    D.place(tk, lerp(DX - 4.4, DX - 5.2, k), 0, lerp(13.5, 0.6, k), PI + 0.15);
    D.walk(tk, t * 15, 0.9);
    tk.j.armL.rotation.set(-2.6 + Math.sin(t * 15) * 0.4, 0, 0.3);
    tk.setFace("shock");
    road(t, { at: c, porch: true, headlights: 0, truck: tp, beam: 0.25, aim: [DX, 2.5, 4] });
    D.cam({ p: [[DX - 13, 5.2, -6], [DX - 12, 5.0, -5]], l: [DX - 3.6, 3.2, 6], f: D.wpos(tk.j.head), fov: 46, ap: 2, seed: 10 }, u, d);
  });
  // S09 "Get out of the car! There's someone in your back seat!"
  shot(29.25, 31.92, (u, d, t) => {
    const c = carAt(DX, 2, 30);
    driver(c, { face: "shock", look: -0.9, t });
    backseat(c, 0);
    truckAt(DX, 17);
    D.place(tk, DX - 4.6, 0, 1.4, -PI / 2 + 0.25);
    tk.setFace(Math.sin(t * 16) > -0.2 ? "momTalk" : "shock");
    tk.j.armR.rotation.set(-1.55, 0, -0.4 + Math.sin(t * 8) * 0.15);
    tk.j.torso.rotation.x = 0.15;
    const th = D.wpos(tk.j.head, [0, 0.62, 0]);
    road(t, { at: c, porch: true, headlights: 0, truck: [DX, 0, 17], beam: 0.25, aim: [DX, 2.5, 4], fill: [th[0] + 2, th[1], th[2] - 1, 22], fillColor: "#ffd9a8" });
    D.cam({ p: [[DX - 9.5, 5.8, -5.5], [DX - 8.8, 5.6, -4.8]], l: [th[0] + 0.8, th[1] - 0.9, th[2]], f: th, fov: 44, ap: 2.5, seed: 11 }, u, d);
  });
  // S10 Every time he flashed his lights, the man in my back seat had been sitting up. (flashback)
  const FL = [32.45, 34.45];
  shot(31.92, 36.47, (u, d, t) => {
    const s = SPEED * t;
    P.road.scroll(s);
    const c = carAt(0, 0, s);
    const beam = flashAt(t, FL, 0.95);
    driver(c, { face: "worried", t });
    const sh = backseat(c, beam > 0.05 ? clamp(beam * 2.2) : 0);
    const tp = truckAt(0, 17.5);
    road(t, { truck: tp, beam, flash: true });
    sideView(u, d, c, { seed: 12, f: sh });
  });
  // S11 And every time, he ducked back down. (flashback)
  shot(36.47, 39.15, (u, d, t) => {
    const s = SPEED * t;
    P.road.scroll(s);
    const c = carAt(0, 0, s);
    const beam = flashAt(t, [36.3, 38.1], 0.75);
    driver(c, { face: "worried", t });
    const sh = backseat(c, clamp(beam * 2.0));
    const tp = truckAt(0, 17.5);
    road(t, { truck: tp, beam, flash: true });
    sideView(u, d, c, { seed: 13, f: sh });
  });
  // S12 I looked in the mirror. (what the mirror shows: his eyes; the dark back seat)
  shot(39.15, 41.06, (u, d, t) => {
    const c = carAt(DX, 2, 30);
    driver(c, { face: "worried", lookUp: 0.18, look: 0.0, t });
    backseat(c, 0);
    truckAt(DX, 17);
    road(t, { at: c, porch: true, headlights: 0, truck: [DX, 0, 17], beam: 0, lamps: 0.35, aim: [DX - 0.8, 4.2, 2], fill: [DX - 0.6, 5.4, 3.4, 9], fillColor: "#8fa2d8" });
    mirrorPOV(u, d, c, { seed: 14, push: 0.25 });
  });
  // S13 He wasn't ducking anymore. (he rises behind me and leans in between the seats)
  shot(41.06, 43.1, (u, d, t) => {
    const c = carAt(DX, 2, 30);
    driver(c, { face: "shock", faceOpts: { sweat: true }, lookUp: 0.18, look: 0.0, t });
    const up = win(t, 41.15, 41.65, ease.out);
    const lean = win(t, 41.7, 42.75, ease.inOut);
    const sh = backseat(c, up, { lean, face: lean > 0.15 ? "under" : "shadow" });
    truckAt(DX, 17);
    road(t, { at: c, porch: true, headlights: 0, truck: [DX, 0, 17], beam: 0, lamps: 0.35, aim: [DX - 0.8, 4.2, 2], fill: [DX - 0.2, 4.6, 0.2, 10 + 22 * lean], fillColor: "#9fd8d0" });
    mirrorPOV(u, d, c, { seed: 15, f: sh, push: 0.3, shake: 0.02 });
    pipe.grade.uniforms.uFade.value = win(t, 42.85, 43.1);
  });
  // END CARD: the car in the driveway, the truck's lights on it, porch light
  shot(43.1, 46.3, (u, d, t) => {
    const c = carAt(DX, 2, 30);
    backseat(c, 1);
    truckAt(DX, 17);
    road(t, { at: c, porch: true, headlights: 0, truck: [DX, 0, 17], beam: 0.2, aim: [DX, 2.5, 4] });
    D.cam({ p: [[DX + 12, 6.5, 12], [DX + 11.5, 6.4, 11]], l: [DX, 3.0, 1.0], f: c, fov: 44, ap: 1.5, seed: 16 }, u, d);
    pipe.grade.uniforms.uFade.value = lerp(1, 0.38, win(u, 0, 0.12));
  });

  // COVER (thumbnail still): the high beams flash; he's sitting up right behind the driver
  shot(200, 210, (u, d, t) => {
    P.road.scroll(40);
    const c = carAt(0, 0, 40);
    driver(c, { face: "scared", faceOpts: { sweat: true }, look: 0.25, t: 1 });
    const shh = backseat(c, 1, { lean: 0.85, face: "under" });
    const tp = truckAt(0, 17.5);
    road(1, { truck: tp, beam: 0.45, fill: [-0.2, 4.6, -1.8, 28], fillColor: "#9fd8d0" });
    D.cam({ p: [-0.55, 6.1, -10.6], l: [-0.85, 5.15, 0.4], f: shh, fov: 30, ap: 1.0, shake: 0, seed: 99 }, 0, 1);
  });

  return S;
}
