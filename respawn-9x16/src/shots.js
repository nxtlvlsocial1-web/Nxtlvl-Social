// Respawn, shot by shot. Times are seconds on audio/vo.wav (audio/vo-lines.json, transcript.json).
import * as THREE from "three";
import { STEPS, LAND, DOORS, ICU, RAIN, SUN } from "./world.js";
import { ease, win, lerp, lerp3, clamp, hash } from "./util.js";

const PI = Math.PI;
const bump = (u, a, b) => (u <= a || u >= b ? 0 : Math.sin(((u - a) / (b - a)) * PI));
const _m = new THREE.Matrix4(), _x = new THREE.Vector3(), _h = new THREE.Vector3(), _fv = new THREE.Vector3();
const I = (p) => [ICU[0] + p[0], ICU[1] + p[1], ICU[2] + p[2]];
const R = (p) => [RAIN[0] + p[0], RAIN[1] + p[1], RAIN[2] + p[2]];

// top surface of the hospital steps at depth z (plaza 0.3, landing 4)
export function groundY(z) {
  if (z <= STEPS.z0) return stepY(z);
  if (z < -10.4) return 0.3;
  if (Math.abs(z) >= 6 && Math.abs(z) <= 10.4) return 0.32;
  return 0.01;
}
export function stepY(z) {
  if (z > STEPS.z0) return 0.3;
  if (z < STEPS.z0 - STEPS.n + 1) return LAND.y;
  return Math.min(STEPS.n, Math.floor(STEPS.z0 - z) + 1) * STEPS.rise;
}

export function buildShots(ctx, D) {
  const { C, W, pipe, camera } = ctx;
  const P = W.props;
  const dr = C.driver, lily = C.lily, crowd = C.crowd;
  const S = [];
  // every shot gets its progress u in 0..1 (d = 1) and the absolute time t; shake follows absolute time
  const shot = (t0, t1, run) => S.push({ t0, t1, run: (us, d, t) => { ctx.now = t; run(us / d, 1, t); } });
  const G = () => pipe.grade.uniforms;

  // ---- helpers ------------------------------------------------------------------
  // lay an avatar down: body centre c, head direction H, face direction F
  function lie(av, c, H, F) {
    _h.set(H[0], H[1], H[2]).normalize();
    _fv.set(F[0], F[1], F[2]).normalize();
    _x.crossVectors(_h, _fv).normalize();
    _fv.crossVectors(_x, _h).normalize();
    _m.makeBasis(_x, _h, _fv);
    av.root.visible = true;
    av.root.quaternion.setFromRotationMatrix(_m);
    const s = av.size || 1;
    av.root.scale.setScalar(s);
    av.root.position.set(c[0] - _h.x * 2.65 * s, c[1] - _h.y * 2.65 * s, c[2] - _h.z * 2.65 * s);
  }
  const head = (a, off = [0, 0.62, 0]) => D.wpos(a.j.head, off);
  // traffic flows in both lanes; o.keep(i) decides which cars are still in the city
  function traffic(t, keep = () => true) {
    P.traffic.forEach((c, i) => {
      const dir = c.home.z > 0 ? -1 : 1;
      let x = c.home.x + dir * 13 * t;
      x = ((x + 150) % 242 + 242) % 242 - 150;
      c.group.position.x = x;
      c.group.visible = keep(i, x);
    });
  }
  function city(t, o = {}) {
    D.on("city");
    D.lights("sunset", { t, ...o });
    traffic(t, o.keep);
  }
  // the driver sitting in a car's driver seat, hands on the wheel
  function inCar(car, { lookX = 0, lookY = 0, face = "flat", faceOpts } = {}) {
    const p = D.carPt(car, [2.3, 0, -3.0]);
    D.place(dr, p[0], p[1], p[2], car.group.rotation.y);
    D.sit(dr, 3.0);
    dr.j.armL.rotation.set(-1.3, 0, 0.12);
    dr.j.armR.rotation.set(-1.3, 0, -0.12);
    dr.j.head.rotation.set(lookY, lookX, 0);
    dr.setFace(face, faceOpts);
  }
  // camera in a car's local frame
  function camCar(car, o, u, d) {
    const conv = (v) => (Array.isArray(v[0]) ? v.map((q) => D.carPt(car, q)) : D.carPt(car, v));
    D.cam({ ...o, p: conv(o.p), l: conv(o.l), f: o.f ? conv(o.f) : undefined }, u, d);
  }
  function placeCar(car, x, z, yaw, y = 0) {
    car.group.visible = true;
    car.group.position.set(x, y, z);
    car.group.rotation.set(0, yaw, 0);
  }
  // the crowd: positions [x, z, facing], blank faces; heads can turn toward a point
  function people(spots, t, { face = "blank", turn = null, turnK = 0, sway = 0 } = {}) {
    crowd.forEach((a, i) => {
      if (i >= spots.length) return;
      const [x, z, ry] = spots[i];
      D.place(a, x, groundY(z), z, ry);
      a.setFace(face);
      a.j.armL.rotation.z = -0.05;
      a.j.armR.rotation.z = 0.05;
      if (sway) a.j.torso.rotation.z = Math.sin(t * 0.5 + i) * 0.01 * sway;
      if (turn && turnK > 0) {
        const want = Math.atan2(turn[0] - x, turn[1] - z) - ry;
        const ww = Math.atan2(Math.sin(want), Math.cos(want));
        a.j.head.rotation.y = ww * clamp(turnK * 1.4 - (i % 4) * 0.12);
      }
    });
  }
  const sidewalkSpots = [
    [-13, 8.6, PI], [-9.4, 9.4, PI], [-5.6, 8.4, PI], [-1.8, 9.6, PI], [2.2, 8.5, PI], [6.0, 9.3, PI],
    [10.2, 8.6, PI], [14.0, 9.5, PI], [-17.5, 9.2, PI], [18, 8.7, PI], [-21.5, 8.6, PI], [22, 9.4, PI],
  ];
  // stand on the steps / plaza
  function standAt(a, x, z, ry) {
    D.place(a, x, groundY(z), z, ry);
  }
  // white respawn flash: bright at k = 1
  const flashW = (k) => D.flash(k, [1, 1, 1]);

  // ================================================================================
  // S1 0.00-2.35  hook: the driver on his back on the landing; his eyes snap open (beep)
  shot(0, 2.35, (u, d, t) => {
    city(t, { focus: [0, 0, -30] });
    lie(dr, [-0.6, LAND.y + 0.5, -31.4], [-1, 0, 0], [0, 1, 0]);
    dr.j.head.rotation.y = u < 0.5 ? 0.0 : -0.35 * win(u, 0.5, 0.9);
    dr.setFace(u < 0.5 ? "sigh" : "shock");
    dr.j.armL.rotation.z = -0.25;
    dr.j.armR.rotation.z = 0.25;
    const hp = head(dr);
    // straight down on his face, face upright in frame (camera up = toward the top of his head)
    D.cam({ p: [[hp[0] + 1.6, hp[1] + 6.8, hp[2] + 0.2], [hp[0] + 1.2, hp[1] + 4.9, hp[2] + 0.15]], l: [hp[0] + 1.3, hp[1], hp[2]], up: [-1, 0, 0], fov: 40, ap: 5, shake: 0.03, e: ease.out }, u, d);
    flashW(0.5 * (1 - win(u, 0, 0.3, ease.out)) + bump(u, 0.48, 0.62) * 0.3);
  });
  // S2 2.35-4.75  wide: the steps, the hospital, he sits up and looks round
  shot(2.35, 4.75, (u, d, t) => {
    city(t, { focus: [0, 0, -25] });
    standAt(dr, -0.6, -29.6, 0);
    D.sit(dr, 0);
    dr.j.legL.rotation.x = dr.j.legR.rotation.x = -1.15;
    dr.j.torso.rotation.x = 0.15;
    dr.j.armL.rotation.set(0.5, 0, 0.3);
    dr.j.armR.rotation.set(0.5, 0, -0.3);
    dr.j.head.rotation.y = Math.sin(u * 1.8) * 0.4;
    dr.setFace("worried");
    people([[-14, 9, PI], [9, 8.6, PI], [20, 9.2, PI]], t);
    D.cam({ p: [[5, 5.5, 4], [3.5, 6.5, -1]], l: [[0, 11, -30], [0, 10, -30]], fov: 52, ap: 1.5, shake: 0.03 }, u, d);
  });
  // S3 4.75-5.80  "Car crash."  the getaway car swerves into a palm
  shot(4.75, 5.8, (u, d, t) => {
    city(t, { focus: [-45, 0, -6], keep: (i, x) => P.traffic[i].home.z > 0 && Math.abs(x + 30) > 34 });
    const k = win(u, 0, 0.62, ease.in);
    const x = lerp(-96, -50.5, k), z = lerp(-3, -5.6, win(u, 0.25, 0.62));
    placeCar(P.car, x, z, PI / 2 + 0.22 * win(u, 0.25, 0.62));
    const hit = win(u, 0.6, 0.78, ease.out);
    P.car.body.rotation.set(0.12 * hit, 0, -0.32 * hit);
    P.car.body.position.y = 0.9 * hit;
    P.car.wheels.forEach((w) => (w.rotation.x = u * 40));
    const palm = P.palms.find((p) => Math.abs(p.position.x + 41) < 1 && p.position.z < 0);
    if (palm) palm.rotation.z = -0.22 * hit;
    D.cam({ p: [-24, 4.0, 9], l: [[-62, 4, -5], [-46, 5, -6]], fov: 44, ap: 2, shake: 0.05 + 0.5 * bump(u, 0.6, 0.9) }, u, d);
    flashW(win(u, 0.82, 1.0));
  });
  // S4 5.80-6.80  "Police chase."  low, head-on: the car flat out, a cruiser on its tail
  shot(5.8, 6.8, (u, d, t) => {
    const x = lerp(-20, 22, u);
    city(t, { focus: [10, 0, -3], keep: (i, tx) => P.traffic[i].home.z > 0 && (tx < x - 40 || tx > x + 45) });
    placeCar(P.car, x, -3.4, PI / 2);
    placeCar(P.cop, x - 22, 1.2, PI / 2 - 0.06);
    P.cop.flash(t);
    for (const c of [P.car, P.cop]) c.wheels.forEach((w) => (w.rotation.x = t * 30));
    D.cam({ p: [[x + 36, 3.0, 2.2], [x + 33, 2.8, 2.0]], l: [x - 9, 3.6, -3], fov: 30, ap: 2, shake: 0.08 }, u, d);
    flashW(win(u, 0.8, 1.0));
  });
  // S5 6.80-9.20  "Doesn't matter. Same steps. Same sunset."  high angle: back on the landing
  shot(6.8, 9.2, (u, d, t) => {
    city(t, { focus: [0, 0, -25] });
    const up = win(u, 0.45, 0.85);
    if (up <= 0.0) {
      lie(dr, [1.0, LAND.y + 0.5, -31.6], [-1, 0, 0.2], [0, 1, 0]);
      dr.setFace("sigh");
    } else {
      standAt(dr, 0.6, -30.2, 0.2);
      D.sit(dr, 0);
      dr.j.legL.rotation.x = dr.j.legR.rotation.x = -1.15;
      dr.j.torso.rotation.x = lerp(-1.2, 0.18, up);
      dr.j.pelvis.position.y = 0.5 - 0.3 * (1 - up);
      dr.setFace("sigh");
    }
    D.cam({ p: [[14, 7.4, -23.5], [12, 6.9, -24.5]], l: [[0, 4.6, -31], [0, 5.0, -31]], fov: 46, f: [0.6, 4.8, -30.8], ap: 2, shake: 0.02 }, u, d);
    flashW(1 - win(u, 0, 0.35, ease.out));
  });
  // S6 9.20-12.35  "the city is emptier": from the top of the steps; the traffic blinks out car by car
  shot(9.2, 12.35, (u, d, t) => {
    const gone = (i) => 0.12 + i * 0.09;
    city(t, { focus: [10, 0, -10], dread: 0.25 * u, keep: (i) => u < gone(i) || (u < gone(i) + 0.03 && Math.floor(t * 30) % 2 === 0) });
    standAt(dr, -2.2, -30.4, PI * 0.72);
    D.idle(dr, t);
    dr.j.head.rotation.y = 0.15;
    D.cam({ p: [[-9.0, 10.8, -34.8], [-8.4, 10.2, -34.2]], l: [[26, 0, 4], [30, 0, 2]], fov: 50, f: [20, 2, 0], ap: 1.0, shake: 0.02 }, u, d);
  });
  // S7 12.35-13.45  "No traffic."  low on the empty road, the light blinking yellow
  shot(12.35, 13.45, (u, d, t) => {
    city(t, { focus: [-35, 0, 0], dread: 0.3, keep: () => false });
    P.tlLamps[1].emissiveIntensity = Math.floor(t * 1.6) % 2 ? 4.5 : 0.3;
    D.cam({ p: [[-16, 1.2, -1.5], [-18, 1.3, -1.2]], l: [-45, 7, 3], fov: 36, ap: 2, shake: 0.02 }, u, d);
  });
  // S8 13.45-14.70  "Empty beaches."  umbrellas, a lifeguard tower, nobody
  shot(13.45, 14.7, (u, d, t) => {
    city(t, { focus: [112, 0, -20], dread: 0.32, keep: () => false });
    D.cam({ p: [[106, 5.5, 44], [106.5, 5.3, 40]], l: [[114, 3, -20], [115, 3, -22]], fov: 44, ap: 1.5, shake: 0.02 }, u, d);
  });
  // S9 14.70-16.90  "the people who are left just stand there"  a slow dolly past blank faces
  shot(14.7, 16.9, (u, d, t) => {
    city(t, { focus: [0, 0, 6], dread: 0.4, keep: () => false });
    people(sidewalkSpots, t, { sway: 1 });
    const x = lerp(-14, -7, u);
    D.cam({ p: [[x, 5.3, 4.2], [x + 1, 5.3, 4.2]], l: [[x + 12, 4.6, 9.2], [x + 13, 4.6, 9.2]], fov: 46, f: [x + 7, 5, 9], ap: 4, shake: 0.02 }, u, d);
  });
  // S10 16.90-18.95  "Staring at the hospital."  behind them; then heads turn all the way round
  shot(16.9, 18.95, (u, d, t) => {
    city(t, { focus: [0, 0, -10], dread: 0.5, keep: () => false });
    const k = win(u, 0.62, 0.72, ease.out);
    // standing in the middle of the empty road, all facing the hospital
    const road = [[-1.8, 7.4], [2.4, 6.6], [0.4, 4.0], [-2.8, 1.8], [3.0, 0.2], [-0.8, -2.2], [1.8, -4.4], [-3.2, -7.6], [3.4, -8.6], [-1.2, -12.4], [1.4, -15.2], [-2.4, -18.0]];
    people(road.map(([x, z]) => [x, z, PI]), t, { turn: [0.5, 15], turnK: k });
    for (let i = 0; i < 6; i++) if (k > 0.05) crowd[i].setFace("blank");
    D.cam({ p: [[0.5, 7.0, 12.3], [0.5, 7.0, 11.9]], l: [[0, 3.6, -34], [0, 3.8, -34]], fov: 54, f: [-1.8, 5.4, 9.6], ap: 2, shake: 0.02 + bump(u, 0.62, 0.8) * 0.15 }, u, d);
  });
  // S11 18.95-21.95  "Then my car radio caught a voice in the static."  inside the car
  shot(18.95, 21.95, (u, d, t) => {
    city(t, { focus: [12, 0, -3], dread: 0.45, keep: () => false });
    placeCar(P.car, 12, -3, PI / 2);
    inCar(P.car, { face: "flat", lookX: -0.25 * win(u, 0.3, 0.6), lookY: 0.1 });
    dr.j.armR.rotation.set(-1.0, 0, -0.55 * win(u, 0.2, 0.5));
    const scan = (88.1 + Math.floor(u * 40) * 0.4).toFixed(1);
    P.car.radio.set(u < 0.55 ? "SCANNING" : "FM", u < 0.55 ? scan : "--.-", u < 0.55 ? 0.3 : 0.9, Math.floor(t * 12));
    camCar(P.car, { p: [[-2.7, 5.9, 0.5], [-2.5, 5.8, -0.1]], l: [[1.2, 5.2, -1.6], [1.4, 5.3, -2.0]], fov: 52, f: [2.3, 6.1, -3.0], ap: 3, shake: 0.02 }, u, d);
  });
  // S12 21.95-23.30  "Daddy... please wake up."  the radio display spells it out
  shot(21.95, 23.3, (u, d, t) => {
    city(t, { focus: [12, 0, -3], dread: 0.55, keep: () => false });
    placeCar(P.car, 12, -3, PI / 2);
    inCar(P.car, { face: "shock" });
    const us = t - 21.95; // word times from the transcript
    const word = us < 0.26 ? "· · ·" : us < 0.55 ? "DADDY" : us < 0.92 ? "PLEASE" : us < 1.16 ? "WAKE" : "UP";
    P.car.radio.set("RDS", word, 0.2 + 0.35 * (Math.floor(t * 10) % 2), Math.floor(t * 14));
    P.car.radio.screenM.emissiveIntensity = 1.3 + 0.3 * Math.sin(t * 40);
    camCar(P.car, { p: [[0.15, 5.15, -1.7], [0.1, 4.95, -1.15]], l: [0, 4.6, 1.26], fov: 55, ap: 4, shake: 0.015 }, u, d);
  });
  // S13 23.30-24.30  his face; outside, the sky flickers into a hospital ceiling
  shot(23.3, 24.3, (u, d, t) => {
    city(t, { focus: [12, 0, -3], dread: 0.6, keep: () => false });
    placeCar(P.car, 12, -3, PI / 2);
    inCar(P.car, { face: "scared", lookX: -0.4, lookY: -0.1 });
    P.car.radio.set("RDS", "WAKE UP", 0.6, Math.floor(t * 14));
    const fl = [0.18, 0.26, 0.5, 0.58, 0.64].some((a) => u > a && u < a + 0.05) ? 0.85 : 0;
    P.ceilM.opacity = fl;
    camCar(P.car, { p: [[-1.3, 6.1, 0.9], [-1.1, 6.15, 0.5]], l: [2.3, 6.2, -3.0], fov: 36, ap: 6, shake: 0.03 }, u, d);
  });
  // S14 24.30-26.00  "That's my daughter, Lily."  he pulls the sun visor down: her photo
  shot(24.3, 26.0, (u, d, t) => {
    city(t, { focus: [12, 0, -3], dread: 0.35, keep: () => false });
    placeCar(P.car, 12, -3, PI / 2);
    inCar(P.car, { face: "worried", lookY: -0.35 });
    const fl = win(u, 0.05, 0.3, ease.out);
    P.car.visor.rotation.x = -1.35 * fl;
    dr.j.armR.rotation.set(lerp(-1.3, -2.7, win(u, 0, 0.2)) + 0.5 * fl, 0, 0.15);
    camCar(P.car, { p: [[0.4, 6.5, -4.4], [0.7, 6.45, -3.6]], l: [2.6, 6.45, 1.95], fov: 34, f: [2.6, 6.45, 1.95], ap: 6, shake: 0.015 }, u, d);
  });
  // S15 26.00-28.05  "And she's never been to this city."  through his window; far off, they all face the car
  shot(26.0, 28.05, (u, d, t) => {
    city(t, { focus: [12, 0, -3], dread: 0.45, keep: () => false });
    placeCar(P.car, 12, -3, PI / 2);
    inCar(P.car, { face: "worried", faceOpts: { tear: u > 0.5 }, lookX: 0.5, lookY: 0.05 });
    P.car.visor.rotation.x = -1.35;
    people(sidewalkSpots.map(([x, z]) => [x + 10, z + 1, PI]), t, { turn: [12, -3], turnK: 1 });
    camCar(P.car, { p: [[9.5, 6.7, 0.2], [8.4, 6.5, -0.6]], l: [1.6, 5.9, -3.2], fov: 38, f: [2.3, 6.1, -3.0], ap: 3, shake: 0.02 }, u, d);
  });
  // S16 28.05-29.30  respawn: flash, eyes snap open (beep)
  shot(28.05, 29.3, (u, d, t) => {
    city(t, { focus: [0, 0, -30], dread: 0.5, keep: () => false });
    lie(dr, [-0.6, LAND.y + 0.5, -31.4], [-1, 0, 0], [0, 1, 0]);
    dr.setFace(u < 0.3 ? "sigh" : "shock");
    const hp = head(dr);
    D.cam({ p: [[hp[0] + 1.2, hp[1] + 5.6, hp[2] + 0.05], [hp[0] + 1.1, hp[1] + 4.6, hp[2] + 0.05]], l: [hp[0] + 1.0, hp[1], hp[2]], up: [-1, 0, 0], fov: 38, ap: 6, shake: 0.03 }, u, d);
    flashW(1 - win(u, 0, 0.25, ease.out));
  });
  // S17 29.30-30.85  his POV: a heartbeat line draws itself across the sunset sky
  shot(29.3, 30.85, (u, d, t) => {
    city(t, { focus: [0, 0, -20], dread: 0.55, keep: () => false });
    const camP = [-0.6, 4.9, -30.2], look = [0, 240, 40];
    const dir = new THREE.Vector3(look[0] - camP[0], look[1] - camP[1], look[2] - camP[2]).normalize();
    const at = [camP[0] + dir.x * 230, camP[1] + dir.y * 230, camP[2] + dir.z * 230];
    P.ecgSky.set(clamp(u * 1.05), [at[0], at[1] - 18, at[2]], camP);
    D.cam({ p: [camP, [camP[0], camP[1] + 0.3, camP[2]]], l: look, fov: 58, ap: 0, shake: 0.03 }, u, d);
  });
  // S18 30.85-33.00  "It was a heart monitor."  the real one; pull back to him in the bed
  shot(30.85, 33.0, (u, d, t) => {
    D.on("icu");
    D.lights("icu");
    P.monitor.set(t, { bpm: 41 });
    icuPatient(t, { eyes: "sigh" });
    const mon = I([6.2, 8.2, -8.4]);
    const back = win(u, 0.35, 1.0);
    D.cam({ p: I([lerp(4.7, -4.5, back), lerp(8.2, 9.2, back), lerp(-5.0, 3.5, back)]), l: I([lerp(6.2, 1.8, back), lerp(8.2, 5.2, back), lerp(-8.4, -5.0, back)]), fov: lerp(28, 46, back), f: I([lerp(6.2, 0.4, back), lerp(8.2, 5.0, back), lerp(-8.4, -5.6, back)]), ap: 4, shake: 0.012 }, u, d);
  });
  // S19 33.00-35.40  "There was only one crash. A real one."  rain, wipers, the road to school
  shot(33.0, 35.4, (u, d, t) => {
    D.on("rain");
    D.lights("rain", { focus: [0, 0, -40 + u * 20] });
    const z = R([0, 0, -60 + u * 26]);
    placeCar(P.famCar, -3, z[2], 0);
    inCar(P.famCar, { face: "flat" });
    dr.j.head.visible = false;
    P.famCar.wipers.forEach((w, i) => (w.rotation.z = -1.25 * Math.abs(Math.sin(t * 2.4 + i * 0.2))));
    P.rain.at(-3, -60 + u * 26, t);
    D.cam({ p: [D.carPt(P.famCar, [2.2, 6.7, -2.4]), D.carPt(P.famCar, [2.2, 6.65, -2.3])], l: [D.carPt(P.famCar, [1.6, 3.6, 30]), D.carPt(P.famCar, [1.4, 3.5, 30])], fov: 52, ap: 0, shake: 0.03 }, u, d);
  });
  // S20 35.40-37.85  "On my way to pick her up from school."  a truck drifts into the lane: headlights, white
  shot(35.4, 37.85, (u, d, t) => {
    D.on("rain");
    D.lights("rain", { focus: [0, 0, 0] });
    const cz = -34 + u * 22;
    placeCar(P.famCar, -3, R([0, 0, cz])[2], 0);
    inCar(P.famCar, { face: "shock" });
    dr.j.head.visible = false;
    P.famCar.wipers.forEach((w, i) => (w.rotation.z = -1.25 * Math.abs(Math.sin(t * 2.4 + i * 0.2))));
    P.rain.at(-3, cz, t);
    // the truck: oncoming lane, then across into ours
    const k = win(u, 0.1, 0.95, ease.in);
    const tz = lerp(cz + 120, cz + 14, k), tx = lerp(3.5, -2.0, win(u, 0.35, 0.9));
    P.truck.group.position.set(tx, 0, tz);
    P.truck.group.rotation.set(0, PI - 0.25 * win(u, 0.35, 0.8), 0);
    P.truck.flare.material.opacity = 0.15 + 0.85 * win(u, 0.55, 0.95);
    pipe.bloom.strength = 0.5 + 1.1 * win(u, 0.65, 0.95);
    D.cam({ p: [D.carPt(P.famCar, [2.2, 6.7, -2.4]), D.carPt(P.famCar, [2.2, 6.65, -2.3])], l: [D.carPt(P.famCar, [1.6, 3.6, 30]), D.carPt(P.famCar, [0.5, 3.4, 30])], fov: 52, ap: 0, shake: 0.03 + bump(u, 0.75, 1.0) * 0.4, roll: [0, -6 * win(u, 0.8, 1)] }, u, d);
    flashW(win(u, 0.9, 0.98));
  });
  // S21 37.85-41.45  "The city wanted me to stay. Here, nothing hurts."  golden; they close in, smiling
  shot(37.85, 41.45, (u, d, t) => {
    city(t, { focus: [0, 0, -12], dread: 0, exp: 1.05, keep: () => false });
    flashW(1 - win(u, 0, 0.3, ease.out));
    standAt(dr, 0, -19.5, 0);
    D.idle(dr, t);
    dr.setFace("worried");
    const ring = crowd.map((_, i) => {
      const a = -1.05 + (i / (crowd.length - 1)) * 2.1;
      const rr = lerp(11, 7.2, win(u, 0.1, 1));
      return [Math.sin(a) * rr, -19.5 + Math.cos(a) * rr, a + PI];
    });
    people(ring, t, { face: "forced" });
    crowd.forEach((a, i) => D.walk(a, t * 4 + i, 0.25 * (1 - win(u, 0.85, 1))));
    placeCar(P.car, 14, 2.8, PI / 2 + 0.3);
    D.cam({ p: [[2.4, 10.5, -30], [2.0, 9.4, -27.6]], l: [[-0.3, 2.0, -11], [-0.3, 2.4, -12]], fov: 46, f: [0, 4, -15], ap: 1.5, shake: 0.02 }, u, d);
  });
  // S22 41.45-43.60  "But Lily was holding my hand."  a small warm light closes round his hand
  shot(41.45, 43.6, (u, d, t) => {
    city(t, { focus: [0, 0, -12], dread: 0, keep: () => false });
    standAt(dr, 0, -19.5, 0);
    dr.setFace("cry", { tear: true });
    dr.j.armR.rotation.set(-0.9 - 0.2 * win(u, 0, 0.6), 0, -0.2);
    dr.j.head.rotation.set(0.45, -0.1, 0);
    const hp = D.wpos(dr.j.handR, [0, -0.2, 0.1]);
    const g = W.lights.glows[2];
    g.color.set("#ffe0a8");
    g.position.set(hp[0], hp[1] + 0.5, hp[2] + 0.6);
    g.distance = 10;
    g.intensity = 10 * win(u, 0.1, 0.6);
    handGlow(hp, win(u, 0.1, 0.6));
    people(crowd.map((_, i) => { const a = -1.05 + (i / (crowd.length - 1)) * 2.1; return [Math.sin(a) * 7.2, -19.5 + Math.cos(a) * 7.2, a + PI]; }), t, { face: "forced" });
    D.cam({ p: [[3.6, 5.0, -15.4], [3.0, 5.8, -15.6]], l: [hp, [0.2, 6.0, -19.3]], fov: 46, f: [hp, [0.2, 6.0, -19.3]], ap: 5, shake: 0.02 }, u, d);
  });
  // S23 43.60-46.60  "So for the first time... I went inside."  up the steps, the doors open, white
  shot(43.6, 46.6, (u, d, t) => {
    city(t, { focus: [0, 0, -25], dread: 0, keep: () => false });
    const z = lerp(-19.5, -35.0, win(u, 0.05, 0.95, ease.linear));
    standAt(dr, 0, z, PI);
    D.walk(dr, z * 2.2, 0.5);
    const op = win(u, 0.35, 0.7);
    P.doorL.position.x = -2.5 - 3.6 * op;
    P.doorR.position.x = 2.5 + 3.6 * op;
    P.inside.color.set("#ffffff").multiplyScalar(0.8 + 0.6 * op);
    pipe.bloom.strength = 0.6 + 0.15 * op;
    // they follow to the foot of the steps, no further
    people(crowd.map((_, i) => { const a = -1.05 + (i / (crowd.length - 1)) * 2.1; const rr = lerp(7.2, 3.5, win(u, 0, 0.5)); return [Math.sin(a) * rr * 1.6, -19.5 + Math.cos(a) * rr, PI]; }), t, { face: u > 0.5 ? "blank" : "forced" });
    D.cam({ p: [[0.8, 9.0, -12.5], [0.5, 9.6, -23.5]], l: [[0, 6.5, -32], [0, 8.0, -36]], fov: 46, f: D.wpos(dr.j.head), ap: 1.5, shake: 0.02 }, u, d);
    flashW(win(u, 0.72, 1.0, ease.in));
  });
  // S24 46.60-47.90  "Daddy?"  the real room, morning: Lily wakes beside the bed, holding his hand
  shot(46.6, 47.9, (u, d, t) => {
    D.on("icu");
    D.lights("morning", { k: 1 });
    P.monitor.set(t, { bpm: 72 });
    icuPatient(t, { eyes: "sigh" });
    lilyChair(t, { lift: win(u, 0.2, 0.7), face: u > 0.35 ? "momWorried" : "lilySleep" });
    flashW(1 - win(u, 0, 0.35, ease.out));
    D.cam({ p: [I([3.8, 7.6, 3.4]), I([3.4, 7.4, 2.8])], l: I([-4.6, 4.2, 0.6]), fov: 42, f: head(lily), ap: 4, shake: 0.015 }, u, d);
  });
  // S25 47.90-50.90  "I'm here, baby. I'm not going anywhere."  his eyes open; she hugs him
  shot(47.9, 50.9, (u, d, t) => {
    D.on("icu");
    D.lights("morning", { k: 1 });
    P.monitor.set(t, { bpm: 76 });
    icuPatient(t, { eyes: u < 0.12 ? "sigh" : "smile", tear: u >= 0.12, turn: 0.35 * win(u, 0.05, 0.3) });
    lilyChair(t, { hug: win(u, 0.25, 0.6), face: u > 0.3 ? "lilyHappy" : "lilyCry", tear: u < 0.6 });
    D.cam({ p: [I([-0.4, 8.9, 2.4]), I([-0.6, 8.6, 1.6])], l: I([-1.1, 4.85, -6.3]), fov: 34, f: I([-1.0, 4.9, -6.3]), ap: 4, shake: 0.012 }, u, d);
  });
  // S26 50.90-53.88  end card: a slow pull back, morning light across the room
  shot(50.9, 54.2, (u, d, t) => {
    D.on("icu");
    D.lights("morning", { k: 1 });
    P.monitor.set(t, { bpm: 76 });
    icuPatient(t, { eyes: "relief", turn: 0.45 });
    lilyChair(t, { hug: 1, face: "lilyHappy" });
    D.cam({ p: [I([7.0, 9.0, 6.5]), I([8.6, 9.8, 8.6])], l: I([-1.2, 4.4, -4.5]), fov: 46, ap: 1.5, shake: 0.01 }, u, d);
    G().uVignette.value = 0.55;
  });

  // COVER (t = 60, after the film): alone in the middle of the empty boulevard, the crowd behind him, a heartbeat in the sky
  shot(60, 61, (u, d, t) => {
    city(54, { focus: [0, 0, 0], dread: 0.12, keep: () => false });
    D.place(dr, -4, 0.01, 0.3, -PI / 2 + 0.12);
    dr.setFace("scared");
    dr.j.armL.rotation.set(0.1, 0, 0.18);
    dr.j.armR.rotation.set(-0.1, 0, -0.18);
    dr.j.head.rotation.set(-0.05, 0.08, 0);
    const behind = [[9, -4.6], [14, 4.4], [20, -3.2], [25, 5.2], [31, -5.4], [37, 2.8], [44, -4.0], [51, 4.6], [59, -2.2], [67, 3.6], [76, -4.4], [86, 1.8]];
    people(behind.map(([x, z]) => [x, z, -PI / 2]), t);
    const camP = [-23, 3.0, 0.6];
    // the heartbeat line on the cover is drawn by tools/cover.cjs (crisper at thumbnail size)
    D.cam({ p: camP, l: [40, 8.5, 0], fov: 50, f: [-4, 5, 0.3], ap: 1.6, shake: 0 }, u, d);
  });

  // ---- ICU blocking -----------------------------------------------------------------
  function icuPatient(t, { eyes = "sigh", tear = false, turn = 0 } = {}) {
    dr.setOutfit("gown");
    dr.bandage(true);
    lie(dr, I([0, 4.15, -4.6]), [0, 0.42, -1], [0, 1, 0.42]);
    dr.setFace(eyes, tear ? { tear: true } : undefined);
    dr.j.head.rotation.y = -turn;
    dr.j.armL.rotation.set(0, 0, -0.08);
    dr.j.armR.rotation.set(0, 0, 0.08);
    P.icuBlanket.position.set(0, 3.95, 1.9);
    P.icuBlanket.scale.set(1, 1, 0.78);
  }
  function lilyChair(t, { lift = 0, hug = 0, face = "lilySleep", tear = false } = {}) {
    lily.setOutfit("sweater");
    const s = lily.size;
    if (hug > 0) {
      // curled up on the bed beside him, head on his shoulder, arm across his chest
      lie(lily, I([lerp(-4.0, -2.5, hug), lerp(3.4, 4.0, hug), -4.3]), [0.15, 0.42, -1], [0.75, 0.3, 0.55]);
      lily.j.armL.rotation.set(-1.4 * hug, 0, -0.2);
      lily.j.armR.rotation.set(-0.2, 0, 0.1);
      lily.j.legL.rotation.x = 0.5;
      lily.j.legR.rotation.x = 0.35;
      lily.j.head.rotation.set(0.1, -0.3 * hug, 0);
    } else {
      // asleep in the chair, head down on the bed, then lifting
      D.place(lily, ...I([-5.6, 0, 1.0]), PI / 2);
      D.sit(lily, 2.75 / s);
      lily.j.torso.rotation.x = lerp(0.95, 0.35, lift);
      lily.j.head.rotation.set(lerp(0.3, -0.25, lift), lerp(0.4, 0.0, lift), 0);
      lily.j.armL.rotation.set(-1.4, 0, 0.1);
      lily.j.armR.rotation.set(-1.7, 0, -0.1);
    }
    lily.setFace(face, tear ? { tear: true } : undefined);
  }
  // a small warm light where a hand would be holding his
  let glowMesh = null;
  function handGlow(p, k) {
    if (!glowMesh) {
      glowMesh = new THREE.Mesh(new THREE.PlaneGeometry(1.3, 1.3), new THREE.MeshBasicMaterial({ map: haloTex(), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, fog: false }));
      ctx.scene.add(glowMesh);
    }
    glowMesh.visible = k > 0;
    glowMesh.position.set(p[0], p[1], p[2]);
    glowMesh.quaternion.copy(camera.quaternion);
    glowMesh.material.opacity = 0.8 * k;
  }
  const _hideGlow = S.map((s) => s.run);
  S.forEach((s, i) => {
    const run = _hideGlow[i];
    s.run = (u, d, t) => {
      if (glowMesh) glowMesh.visible = false;
      W.lights.glows[2].intensity = 0;
      run(u, d, t);
    };
  });
  return S;
}

function haloTex() {
  const c = document.createElement("canvas");
  c.width = c.height = 128;
  const g = c.getContext("2d");
  const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  gr.addColorStop(0, "rgba(255,240,210,1)");
  gr.addColorStop(0.35, "rgba(255,215,150,0.55)");
  gr.addColorStop(1, "rgba(255,200,120,0)");
  g.fillStyle = gr;
  g.fillRect(0, 0, 128, 128);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}
