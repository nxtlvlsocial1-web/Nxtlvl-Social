// The film, shot by shot. Times are seconds on the narration track (audio/vo-lines.json).
// Every shot sets lights, camera and cast from its local time u (0..d), so any frame renders alone.
import * as THREE from "three";
import { makeDirector } from "./direct.js";
import { EXT, WED, INS } from "./world.js";
import { ease, win, lerp, lerp3, clamp, rng, smooth } from "./util.js";

const PI = Math.PI;
const bump = (u, a, b) => (u <= a || u >= b ? 0 : Math.sin(((u - a) / (b - a)) * PI));

export function buildShots(ctx) {
  const D = makeDirector(ctx);
  const { C, W, pipe, scene } = ctx;
  const P = W.props;
  const S = [];
  const shot = (t0, t1, run) => S.push({ t0, t1, run });

  // chair frame: CF = direction Grandpa faces, CR = his right
  const CF = [-0.7457, 0.6663], CR = [-0.6663, -0.7457];
  const ahead = (p, dir, dist, dy = 0, side = 0, sdir = CR) => [p[0] + dir[0] * dist + sdir[0] * side, p[1] + dy, p[2] + dir[1] * dist + sdir[1] * side];
  const gHead = () => D.wpos(C.grandpa.j.head, [0, 0.62, 0]);
  const kHead = () => D.wpos(C.kid.j.head, [0, 0.62, 0]);
  const cHead = () => D.wpos(C.counter.j.head, [0, 0.95, 0]);
  const C0 = [2.5, 0, -4.5]; // where the Counter counts the spilled rice
  const K0 = [1.5, 0, 6.5]; // the kid's hiding spot behind the couch

  function counterWalk(c, ph, amp = 0.32) {
    const s = Math.sin(ph);
    c.j.thighL.rotation.x = s * amp;
    c.j.thighR.rotation.x = -s * amp;
    c.j.shinL.rotation.x = Math.max(0, -s) * amp * 1.2;
    c.j.shinR.rotation.x = Math.max(0, s) * amp * 1.2;
    c.j.upperL.rotation.x = -s * 0.12;
    c.j.upperR.rotation.x = s * 0.12;
  }
  function kidHide(u, scared = true) {
    const k = C.kid;
    D.place(k, K0[0], 0, K0[2], 0);
    D.sit(k, 0);
    k.j.armL.rotation.x = k.j.armR.rotation.x = -0.6;
    k.j.head.rotation.y = Math.sin(u * 2.3) * 0.25;
    if (scared) k.setFace("scared", { sweat: true });
  }

  // ---- rice -----------------------------------------------------------------
  const R = rng(2024);
  const N_RAIN = 5200, N_CLUSTER = 1500;
  const BAG = [10.5, 12.6, -2.2], T_BURST = 94.95, G = 18;
  const rain = [];
  for (let i = 0; i < N_RAIN + N_CLUSTER; i++) {
    const cl = i >= N_RAIN;
    const vy = R() * 3, delay = R() * 0.3;
    const tl = (vy + Math.sqrt(vy * vy + 2 * G * (BAG[1] - 0.04))) / G;
    let tx, tz;
    if (cl) {
      const a = R() * PI * 2, d = Math.sqrt(R()) * 2.6;
      tx = C0[0] - 0.2 + Math.cos(a) * d;
      tz = C0[2] + 2.3 + Math.sin(a) * d * 0.8;
    } else {
      tx = BAG[0] - (1 + R() * 21);
      tz = BAG[2] + (R() - 0.5) * 16;
    }
    rain.push({ vx: (tx - BAG[0]) / tl, vz: (tz - BAG[2]) / tl, vy, delay, tl, ry: R() * PI * 2, spin: (R() - 0.5) * 20, tx, tz });
  }
  function riceRain(t) {
    const tau0 = t - T_BURST;
    let n = 0;
    if (tau0 <= 0) return D.riceDone(0);
    for (const g of rain) {
      const tau = tau0 - g.delay;
      if (tau <= 0) continue;
      if (tau >= g.tl) D.riceAt(n++, g.tx, 0.04, g.tz, PI / 2, g.ry, 0);
      else D.riceAt(n++, BAG[0] + g.vx * tau, BAG[1] + g.vy * tau - 0.5 * G * tau * tau, BAG[2] + g.vz * tau, tau * g.spin, g.ry, tau * g.spin * 0.7);
    }
    D.riceDone(n);
  }
  const dustSeeds = Array.from({ length: 2600 }, () => [R() * 2 - 1, R() * 2 - 1, R() * 2 - 1, 0.5 + R() * 1.3, R()]);
  function dustCloud(t) {
    const tau = t - T_BURST;
    if (tau <= 0) return;
    D.dustSet((i) => {
      const [a, b, c, fall, r] = dustSeeds[i];
      const spread = (1 - Math.exp(-tau * 1.6)) * (5 + r * 9);
      const y = BAG[1] + b * spread * 0.4 - fall * tau * 0.9;
      return [BAG[0] - 4 + a * spread * 1.4, Math.max(0.12 + r * 0.2, y), BAG[2] + c * spread];
    }, dustSeeds.length);
  }
  function dustHang(t, n = 900) {
    D.dustSet((i) => {
      const [a, b, c, , r] = dustSeeds[i];
      return [2 + a * 13 + Math.sin(t * 0.3 + i) * 0.4, 1 + (b * 0.5 + 0.5) * 9 + Math.sin(t * 0.5 + r * 9) * 0.3, -5 + c * 9];
    }, n);
  }
  // spill from the jar in the hall
  const spill = Array.from({ length: 2300 }, () => {
    const a = R() * PI * 2, d = 0.3 + R() ** 1.8 * 4.6;
    return { a, d, h: R(), ry: R() * PI * 2 };
  });
  const SPILL_O = [-16.4, 0.3, 1.7];
  function riceSpill(tau) {
    if (tau <= 0) return D.riceDone(0);
    let n = 0;
    const f = 1 - (1 - clamp(tau / 0.55)) ** 3;
    for (const g of spill) {
      const x = SPILL_O[0] + Math.cos(g.a) * g.d * f, z = SPILL_O[2] + Math.sin(g.a) * g.d * f;
      const y = 0.04 + Math.sin(PI * clamp(tau / 0.4)) * 0.9 * g.h * (1 - f * 0.6);
      D.riceAt(n++, x, y, z, PI / 2 + (1 - f) * g.ry, g.ry, 0);
    }
    D.riceDone(n);
  }
  function riceHeap(c, n, rad) {
    const r = rng(77);
    for (let i = 0; i < n; i++) {
      const a = r() * PI * 2, d = Math.sqrt(r()) * rad;
      const h = Math.max(0, (1 - d / rad)) * rad * 0.55 * r();
      D.riceAt(i, c[0] + Math.cos(a) * d, c[1] + 0.04 + h, c[2] + Math.sin(a) * d, r() * PI, r() * PI * 2, r() * PI);
    }
    D.riceDone(n);
  }
  function riceStream(from, to, u, n = 90, rate = 1.6, offset = 0) {
    const r = rng(5);
    for (let i = 0; i < n; i++) {
      const ph = (u * rate + i / n) % 1;
      const jx = (r() - 0.5) * 0.12, jz = (r() - 0.5) * 0.12;
      D.riceAt(offset + i, lerp(from[0], to[0], ph) + jx, from[1] + (to[1] - from[1]) * ph * ph, lerp(from[2], to[2], ph) + jz, ph * 9 + i, i, ph * 5);
    }
    D.riceDone(offset + n);
  }

  // ==========================================================================
  // F01 hook: the jar on the porch
  shot(0, 3.75, (u, d) => {
    D.lights("street", 0, { fill: [EXT.x + 4, 4, 0, 90] });
    const jar = [EXT.x + 1.2, 1.95, -4.7], door = [EXT.x, 4.6, -8.9];
    D.cam({ p: [[EXT.x + 5.0, 3.0, 1.6], [EXT.x + 4.0, 2.7, 0.0]], l: [[EXT.x + 1.2, 2.2, -4.7], [EXT.x + 0.9, 2.8, -5.6]], fov: 32, f: [jar, door], fe: (x) => win(x, 0.6, 0.95), ap: 22, seed: 1 }, u, d);
  });
  // F02 midnight street, a long shadow crosses the road
  shot(3.75, 6.93, (u, d) => {
    D.lights("street");
    const L = W.lights.key;
    L.position.set(EXT.x - 60, 28, 12);
    L.target.position.set(EXT.x, 0, 12);
    L.target.updateMatrixWorld();
    L.intensity = 7.5;
    W.lights.hemi.intensity = 0.8;
    W.lights.glows[0].intensity = 500;
    const c = C.counter;
    D.place(c, EXT.x - 30.5 + u * 1.1, 0, 12.5, PI / 2);
    counterWalk(c, u * 2.4);
    c.j.torso.rotation.x = 0.12;
    D.cam({ p: [[EXT.x - 2.5, 10.5, 31], [EXT.x - 2.0, 4.6, 27]], l: [[EXT.x, 6, -8], [EXT.x, 6.2, -10]], fov: 55, ap: 4, seed: 2 }, u, d);
  });
  // F03 folding through the door
  shot(6.93, 10.37, (u, d) => {
    D.lights("night", 0, { doorSpill: 1, lamp: 0.6 });
    P.door.rotation.y = 1.45;
    const c = C.counter;
    D.place(c, -27.5 + 7.5 * ease.inOut(u / d), 0, -6, PI / 2);
    c.j.torso.rotation.x = 1.42;
    c.j.neck.rotation.x = -0.45;
    c.j.head.rotation.x = -0.3;
    counterWalk(c, u * 2.2, 0.25);
    c.j.upperL.rotation.x = c.j.upperR.rotation.x = -1.2;
    D.cam({ p: [[-8.8, 2.3, 2.2], [-9.7, 2.1, 1.3]], l: [-20, 5.4, -6], fov: 48, ap: 7, seed: 3 }, u, d);
  });
  // F04 the dice head; every dot blinks on "eye"
  shot(10.37, 14.67, (u, d) => {
    D.lights("night", 0, { fill: [-2.5, 12, -1.5, 170] });
    const c = D.counterStand(-4, -6, 0.15, { hunch: 0.04, neck: 0.08 });
    c.setEyes(1, bump(u, 3.85, 4.15));
    const h = cHead();
    D.cam({ p: [[h[0] + 1.0, h[1] - 0.6, h[2] + 7.6], [h[0] + 0.5, h[1] - 0.4, h[2] + 5.6]], l: [h[0], h[1] - 0.2, h[2]], fov: 30, ap: 16, seed: 4 }, u, d);
  });
  // F05a he counts everything
  shot(14.67, 18.25, (u, d) => {
    D.lights("night", 0, { fill: [1.5, 9, 2, 170] });
    const c = D.counterStand(-3, -7, 0.5, { hunch: 0.25, neck: 0.4 });
    c.j.torso.rotation.y = Math.sin(u * 1.2) * 0.35;
    c.j.head.rotation.y = Math.sin(u * 1.2 + 0.4) * 0.45;
    c.j.upperR.rotation.x = -1.25 + Math.sin(u * 3) * 0.15;
    c.j.upperR.rotation.z = 0.25;
    c.j.foreR.rotation.x = -0.35;
    D.point(c, "R");
    c.j.fingers.R[1].rotation.x = Math.max(0, Math.sin(u * 13)) * 0.5;
    const h = cHead();
    D.cam({ p: [[7.6, 2.6, 2.2], [6.7, 2.4, 1.3]], l: [h[0], h[1] - 1.4, h[2]], f: h, fov: 42, ap: 10, seed: 5 }, u, d);
  });
  // F05b every spoon
  shot(18.25, 19.22, (u, d) => {
    D.lights("insert", 0, { at: P.insert.drawerAt });
    const tgt = [INS.x - 2.6 + (u / d) * 4.6, 0.45 + bump((u * 5) % 1, 0, 1) * 0.2, INS.z + 1.05];
    D.pointAt(0, tgt, [0.35, 1.3, 0.25], 1.5);
    D.cam({ p: [[INS.x + 1.1, 2.1, INS.z + 3.5], [INS.x + 0.8, 1.9, INS.z + 3.05]], l: [INS.x + 0.0, 0.35, INS.z + 0.8], f: tgt, fov: 34, ap: 20, seed: 6 }, u, d);
  });
  // F05c every sock
  shot(19.22, 19.86, (u, d) => {
    D.lights("insert", 0, { at: P.insert.socksAt });
    const tgt = [INS.x + 19.4 + (u / d) * 0.9, 1.15, INS.z + 0.7];
    D.pointAt(0, tgt, [-0.5, 1.2, 0.6], 1.5);
    D.cam({ p: [[INS.x + 21.7, 2.5, INS.z + 3.7], [INS.x + 21.4, 2.3, INS.z + 3.3]], l: [INS.x + 20, 0.9, INS.z + 0.3], f: tgt, fov: 36, ap: 16, seed: 7 }, u, d);
  });
  // F05d every single grain of rice
  shot(19.86, 21.9, (u, d) => {
    D.lights("insert", 0, { at: P.insert.riceAt });
    riceHeap([INS.x + 40, 0, INS.z], 1600, 1.5);
    const tgt = [INS.x + 40.15, 0.42 + (1 - win(u, 0.2, 1.5)) * 1.2, INS.z + 0.35];
    D.pointAt(0, tgt, [0.25, 1, 0.55], 1.5);
    D.cam({ p: [[INS.x + 41.1, 1.15, INS.z + 2.1], [INS.x + 40.8, 0.9, INS.z + 1.65]], l: [INS.x + 40.1, 0.3, INS.z + 0.25], fov: 28, ap: 26, seed: 8 }, u, d);
  });
  // F06 busy until sunrise, then he leaves
  shot(21.9, 26.13, (u, d) => {
    const k = win(u, 0.2, 2.6, ease.linear);
    D.lights("dawn", k, { fill: [9, 6, -4, 140 * (1 - k)] });
    riceHeap([3.0, 0, -10.2], 900, 1.25);
    const c = C.counter;
    const leave = win(u, 3.4, 4.23, ease.in);
    D.place(c, 6.0 + leave * 6, 0, -12.2 + leave * 0.5, 0);
    if (u < 3.4) D.faceTo(c, 3.0, -10.2);
    else c.root.rotation.y = PI / 2;
    D.counterCrouch(c, 1 - win(u, 2.8, 3.4));
    c.j.upperR.rotation.x = -0.9 + Math.sin(u * 26) * 0.18 * (1 - win(u, 2.6, 2.9));
    c.j.foreR.rotation.x = -0.5;
    D.point(c, "R");
    if (u > 3.4) counterWalk(c, u * 6);
    D.cam({ p: [[-3.2, 3.6, -1.6], [-2.4, 3.4, -2.6]], l: [4.8, 5.0, -12.6], fov: 44, ap: 6, seed: 9 }, u, d);
  });
  // F07 lose count, start over from one
  shot(26.13, 30.18, (u, d) => {
    D.lights("night", 0, { fill: [9.5, 8, -4.5, 160] });
    const c = D.counterStand(5.0, -11.4, 0.55, { hunch: 0.15, neck: 0.25 });
    const jerk = win(u, 0.95, 1.12, ease.out3) * (1 - win(u, 2.0, 2.6));
    c.j.head.rotation.y = jerk * 0.75;
    c.setEyes(1 + jerk * 0.15, 0, jerk * 0.3 * Math.sin(u * 40));
    const raise = win(u, 2.3, 2.7, ease.outBack);
    c.j.upperR.rotation.x = -1.0 - raise * 0.75 + (u < 0.9 ? Math.sin(u * 14) * 0.1 : 0);
    c.j.upperR.rotation.z = 0.25;
    c.j.foreR.rotation.x = -0.6;
    D.point(c, "R");
    // the cup slides off the side table and falls
    const f = win(u, 0.85, 1.35, ease.in);
    P.cup.position.set(8.2 + f * 1.1, 2.7 - Math.max(0, f - 0.25) * 3.5, -8.6 + f * 0.5);
    P.cup.position.y = Math.max(0.3, P.cup.position.y);
    P.cup.rotation.z = -f * 2.3;
    const h = cHead();
    D.cam({ p: [[9.6, 9.8, -2.8], [9.2, 10.0, -3.4]], l: [h[0], h[1] - 1.3, h[2]], f: h, fov: 40, ap: 12, seed: 10 }, u, d);
  });
  // F08 meet the kid: filling the jar
  shot(30.18, 33.16, (u, d) => {
    D.lights("night", 0, { fill: [-11.5, 7.5, 5.5, 240] });
    const k = C.kid;
    P.stool.visible = true;
    P.stool.position.set(-17.7, 0, -2.6);
    D.place(k, -17.7, 1.2, -2.6, 0);
    D.faceTo(k, -18.4, 0.6);
    k.j.armL.rotation.x = k.j.armR.rotation.x = -1.2;
    k.j.armL.rotation.z = -0.25;
    k.j.armR.rotation.z = 0.25;
    k.j.head.rotation.x = 0.3 - win(u, 1.4, 1.9) * 0.35;
    k.setFace(u > 1.6 ? "grin" : "smile");
    P.jar.lid.visible = false;
    P.jar.setFill(0.55 + 0.35 * (u / d));
    P.bag.visible = true;
    P.bag.position.set(-18.15, 5.15, -0.75);
    P.bag.rotation.set(1.35, 0, 0.1);
    riceStream([-18.2, 5.2, 0.05], [-18.4, 4.3, 0.6], u, 70);
    const h = kHead();
    D.cam({ p: [[-16.4, 5.9, 5.4], [-16.7, 5.85, 4.8]], l: [-17.9, 5.2, -1.2], f: h, fov: 38, ap: 12, seed: 11 }, u, d);
  });
  // F09 meet Grandpa: one crumb
  shot(33.16, 36.3, (u, d) => {
    D.lights("day", 0, { fill: [5, 3.5, 1.5, 220] });
    const g = C.grandpa;
    D.place(g, 1.4, 0, -6.2, 0);
    D.faceTo(g, 3.4, -2.6);
    g.setFace("stern");
    g.j.torso.rotation.x = 0.16;
    g.j.head.rotation.x = 0.32;
    g.j.head.rotation.y = Math.sin(Math.max(0, u - 1.6) * 11) * 0.12 * win(u, 1.6, 1.8) * (1 - win(u, 2.6, 2.9));
    g.j.armR.rotation.x = -0.75;
    g.j.armR.rotation.z = -0.2;
    P.crumb.visible = true;
    P.crumb.position.set(3.0, 0.06, -3.1);
    const h = gHead();
    D.cam({ p: [[4.7, 0.7, 1.7], [4.35, 0.65, 0.95]], l: [h[0], h[1] - 0.6, h[2]], f: h, fov: 36, ap: 14, seed: 12 }, u, d);
  });
  // vacuuming pose: Grandpa pushes the vacuum in front of him
  function vacuuming(g, base, ry, u, k = 1) {
    D.place(g, base[0], 0, base[2], ry);
    const osc = Math.sin(u * 5) * 0.55 * k;
    g.root.position.x += Math.sin(ry) * osc * 0.4;
    g.root.position.z += Math.cos(ry) * osc * 0.4;
    g.j.armL.rotation.x = g.j.armR.rotation.x = -1.05;
    g.j.torso.rotation.x = 0.12;
    g.setFace("determined");
    const v = P.vacuum;
    v.root.rotation.order = "YXZ";
    v.root.position.set(g.root.position.x + Math.sin(ry) * (2.6 + osc), 0, g.root.position.z + Math.cos(ry) * (2.6 + osc));
    v.root.rotation.set(-0.42, ry, 0);
    v.light.material.emissiveIntensity = 3;
  }
  // F10a after breakfast
  shot(36.3, 37.62, (u, d) => {
    D.lights("day", 0, { fill: [3, 5, 2.5, 160] });
    vacuuming(C.grandpa, [-3.0, 0, -4.2], PI / 2, u);
    D.cam({ p: [[5.0, 4.5, 3.8], [4.4, 4.3, 3.0]], l: [-0.8, 3.0, -4.2], fov: 40, ap: 8, seed: 13 }, u, d);
  });
  // F10b after lunch (low angle)
  shot(37.62, 38.58, (u, d) => {
    D.lights("day", 0, { fill: [-7, 3, -4, 140] });
    W.lights.key.color.set("#ffd9a8");
    vacuuming(C.grandpa, [-9.5, 0, -11.2], 0.25, u);
    D.cam({ p: [[-7.6, 0.55, -4.4], [-7.8, 0.6, -4.9]], l: [-8.8, 2.8, -9.5], fov: 46, ap: 10, seed: 14 }, u, d);
  });
  // F10c once, at a wedding
  shot(38.58, 39.9, (u, d) => {
    D.lights("wedding");
    const g = C.grandpa;
    g.setOutfit("suit");
    vacuuming(g, [WED.x + 1.6, 0, -0.6], -PI / 2, u);
    g.setFace("determined");
    [[-7, -8.5], [-2.6, -10.8], [4.2, -11.2], [10, -7.8]].forEach(([x, z], i) => {
      const a = C.guests[i];
      D.place(a, WED.x + x, Math.abs(Math.sin(u * 6 + i)) * 0.3, z, 0.3 - i * 0.2);
      a.j.armL.rotation.x = -2.6 + Math.sin(u * 6 + i) * 0.35;
      a.j.armR.rotation.x = -2.6 - Math.sin(u * 6 + i) * 0.35;
      if (i === 3) {
        D.faceTo(a, WED.x + 1.6, -0.6);
        a.j.armL.rotation.x = a.j.armR.rotation.x = 0;
        a.setFace("shock");
      }
    });
    const h = gHead();
    ctx.renderer.toneMappingExposure = 0.95;
    pipe.bloom.strength = 0.45;
    D.cam({ p: [[WED.x - 4.2, 5.2, 13.6], [WED.x - 3.6, 5.0, 12.5]], l: [WED.x + 1.6, 3.8, -3.2], f: h, fov: 42, ap: 14, seed: 15 }, u, d);
  });
  // F11 snores like a lawnmower
  shot(39.9, 42.75, (u, d) => {
    const g = D.grandpaInChair(u);
    const ph = D.snoreFace(g, u, 1.35);
    if (ph > 0.55 && ph < 0.85) g.j.head.rotation.z += Math.sin(u * 70) * 0.025;
    const h = gHead();
    D.lights("night", 0, { fill: ahead(h, CF, 4, 1.2, -1.5).map((v, i) => v).concat([150]) });
    D.zzz(u, [h[0] + 0.5, h[1] + 0.9, h[2]]);
    D.cam({ p: [ahead(h, CF, 4.4, -0.5, 0.9), ahead(h, CF, 3.4, -0.4, 0.7)], l: h, fov: 30, ap: 16, seed: 16 }, u, d);
  });
  // F12 Mom's night shift
  shot(42.75, 45.88, (u, d) => {
    D.lights("night", 0, { fill: [-13, 7.2, -1.5, 210] });
    const m = C.mom;
    D.place(m, -17.4, 0, -5.4, 0);
    m.root.rotation.y = lerp(-PI / 2, 0.8, win(u, 0.5, 1.5));
    m.j.armL.rotation.x = -1.5 * bump(u, 0.1, 1.7);
    m.j.armL.rotation.z = -0.2;
    m.j.head.rotation.y = Math.sin(u * 1.1) * 0.1;
    const h = D.wpos(m.j.head, [0, 0.62, 0]);
    D.cam({ p: [[-11.1, 4.9, -0.3], [-11.8, 4.8, -1.1]], l: [-17.4, 4.3, -5.5], f: h, fov: 34, ap: 14, seed: 17 }, u, d);
  });
  // F13 "Jar by the door. Lights out by eleven."
  shot(45.88, 48.89, (u, d) => {
    D.lights("night", 0, { fill: [-14.2, 7.6, -1.6, 230] });
    const m = C.mom, k = C.kid;
    D.place(m, -17.3, 0, -5.1, 0);
    D.faceTo(m, -13.3, -1.4);
    const talking = (u < 1.15 || (u > 1.75 && u < 2.85)) && Math.sin(u * 40) > 0;
    m.setFace(talking ? "momTalk" : "momSmile");
    const pointK = bump(u, 0.1, 1.5);
    m.root.rotation.y -= pointK * 0.6;
    m.j.armR.rotation.x = -1.5 * pointK;
    const wag = win(u, 1.7, 1.9) * (1 - win(u, 2.8, 3.0));
    m.j.armL.rotation.x = -2.4 * wag;
    m.j.armL.rotation.z = Math.sin(u * 15) * 0.25 * wag;
    const h = D.wpos(m.j.head, [0, 0.62, 0]);
    D.cam({ p: [[-12.9, 4.2, -1.0], [-13.2, 4.2, -1.3]], l: [h[0], h[1] - 0.6, h[2]], f: h, fov: 40, ap: 14, seed: 18 }, u, d);
  });
  // F14 the last bag of rice
  shot(48.89, 52.61, (u, d) => {
    D.lights("night", 0, { fill: [-15.2, 6.8, 3.6, 190] });
    const k = C.kid;
    P.stool.visible = true;
    P.stool.position.set(-17.7, 0, -2.6);
    D.place(k, -17.7, 1.2, -2.6, 0);
    D.faceTo(k, -18.4, 0.6);
    k.j.armL.rotation.x = k.j.armR.rotation.x = -1.25 + (u > 1.4 ? Math.sin(u * 22) * 0.12 : 0);
    k.j.head.rotation.x = 0.35;
    P.jar.lid.visible = false;
    P.jar.setFill(0.6 + 0.35 * win(u, 0, 1.06));
    P.bag.visible = true;
    const shake = u > 1.4 ? Math.sin(u * 22) : 0;
    P.bag.position.set(-18.15 + shake * 0.1, 5.3 + Math.abs(shake) * 0.1, -0.7);
    P.bag.rotation.set(1.4 + shake * 0.2, 0, 0.1);
    if (u < 1.2) riceStream([-18.2, 5.3, 0.1], [-18.4, 4.35, 0.6], u, 90);
    else riceStream([-18.2, 5.3, 0.1], [-18.4, 4.35, 0.6], u, 4, 0.9);
    D.cam({ p: [[-15.6, 5.9, 4.2], [-15.9, 5.75, 3.7]], l: [-18.2, 5.1, -0.2], f: [-18.4, 4.8, 0.6], fov: 36, ap: 14, seed: 19 }, u, d);
  });
  // F15a 11:55
  shot(52.61, 53.75, (u, d) => {
    D.lights("night", 0, { fill: [-15.4, 8.6, -11.6, 130] });
    W.setClock(11 + 55 / 60 + Math.floor(u) / 3600);
    P.clock.pend.rotation.z = Math.sin(u * PI * 2) * 0.16;
    D.cam({ p: [[-14.1, 8.1, -11.9], [-14.5, 8.15, -12.2]], l: [-17.88, 8.1, -13], fov: 32, ap: 10, seed: 20 }, u, d);
  });
  // F15b Biscuit chases a moth straight into the jar
  shot(53.75, 56.62, (u, d) => {
    D.lights("night", 0, { fill: [-10, 4.5, 6.5, 220] });
    const g = C.dog;
    const k = ease.in(win(u, 0, 2.45, ease.linear));
    const pos = lerp3([-4.5, 0, 5.8], [-16.3, 0, 1.3], k);
    D.place(g, pos[0], 0, pos[2], 0);
    D.faceTo(g, -18.4, 0.6);
    D.dogRun(u, 11);
    const leap = win(u, 2.3, 2.75, ease.out);
    g.j.body.position.y += leap * 1.4;
    g.j.body.rotation.x = -leap * 0.7;
    const m = P.moth;
    m.root.visible = true;
    const mk = clamp(k + 0.18);
    const mp = lerp3([-6.8, 4.2, 4.9], [-18.2, 5.3, 0.65], mk);
    m.root.position.set(mp[0], mp[1] + Math.sin(u * 9) * 0.35, mp[2] + Math.cos(u * 7) * 0.2);
    m.root.rotation.y = -1.2;
    m.wings[0].rotation.y = Math.sin(u * 45) * 0.9;
    m.wings[1].rotation.y = -Math.sin(u * 45) * 0.9;
    P.jar.root.rotation.z = -0.55 * win(u, 2.5, 2.87, ease.in);
    const b = D.wpos(g.j.body);
    D.cam({ p: [[-7.4, 1.3, 9.0], [-12.6, 1.5, 6.9]], l: [b[0] - 1.2, b[1] + 0.8, b[2]], f: b, fov: 42, ap: 9, seed: 21 }, u, d);
  });
  // jar knocked off the table: falls and lies on its side
  function jarFallen(tau) {
    const f = win(tau, -0.05, 0.35, ease.in);
    P.jar.root.position.set(lerp(-18.4, -16.6, f), lerp(3.43, 0.55, f) + Math.sin(f * PI) * 0.5, lerp(0.6, 1.5, f));
    P.jar.root.rotation.z = lerp(-0.55, -PI / 2, f);
    P.jar.setFill(0.92 * (1 - win(tau, 0.3, 0.6)));
    P.jar.lid.visible = tau < 0.35;
  }
  // F16 Rice. Everywhere.
  shot(56.62, 58.07, (u, d) => {
    D.lights("night", 0, { fill: [-15, 9.5, 2.5, 220] });
    jarFallen(u);
    riceSpill(u - 0.33);
    const g = C.dog;
    D.place(g, -13.6, 0, 3.4, 0);
    D.faceTo(g, -16.6, 1.5);
    D.dogSit(win(u, 0.6, 1.1));
    D.cam({ p: [[-15.4, 15.5, 2.0], [-15.5, 14.2, 1.95]], l: [-15.5, 0, 1.9], up: [-1, 0, 0], fov: 46, ap: 4, seed: 22 }, u, d);
  });
  // F17a Grandpa didn't say a word
  shot(58.07, 59.85, (u, d) => {
    D.lights("night", 0, { fill: [-14.6, 6.2, 0.8, 220] });
    jarFallen(5);
    riceSpill(5);
    const g = C.grandpa;
    D.place(g, -12.4, 0, -1.4, 0);
    D.faceTo(g, -15.8, 1.2);
    g.setFace(u > 0.95 && u < 1.08 ? "sigh" : "stern");
    g.j.head.rotation.x = 0.28;
    const h = gHead();
    const dir = [-0.78, 0.62];
    D.cam({ p: [ahead(h, dir, 3.6, -0.35), ahead(h, dir, 2.9, -0.3)], l: h, fov: 30, ap: 18, seed: 23 }, u, d);
  });
  // F17b he just plugged in the vacuum
  shot(59.85, 61.47, (u, d) => {
    D.lights("night", 0, { fill: [-17.2, 3.2, 6.6, 140] });
    jarFallen(5);
    riceSpill(5);
    const p = win(u, 0.1, 0.8, ease.out3);
    P.plug.visible = true;
    P.plug.position.set(lerp(-18.0, -19.66, p), 1.4, 4.5);
    D.cam({ p: [[-17.3, 2.05, 6.4], [-17.65, 1.9, 5.95]], l: [-19.6, 1.4, 4.5], f: [-19.7, 1.4, 4.5], fov: 28, ap: 20, seed: 24 }, u, d);
  });
  // F18 every grain was gone
  shot(61.47, 64.82, (u, d) => {
    D.lights("night", 0, { fill: [-12.2, 6.5, 6.6, 220] });
    P.jar.setFill(0);
    const k = C.kid;
    D.place(k, -10.9, 0, 5.9, 0);
    D.faceTo(k, -16.0, 1.4);
    k.j.armR.rotation.x = -0.55;
    k.setFace(u < 1.7 ? "shock" : "flat");
    const hp = D.wpos(k.j.handR);
    P.broom.visible = true;
    P.broom.position.set(hp[0], 0, hp[2]);
    P.broom.rotation.set(0, 0.4, 0.06);
    const v = P.vacuum;
    v.root.position.set(-15.6, 0, -1.8);
    v.root.rotation.set(0, 0.9, 0);
    v.light.material.emissiveIntensity = 3;
    const h = kHead();
    D.cam({ p: [[-16.3, 0.95, 1.3], [-16.0, 1.05, 1.85]], l: [h[0], h[1] - 1.0, h[2]], f: h, fov: 36, ap: 12, seed: 25 }, u, d);
  });
  // F19 asleep in his armchair, smiling, hugging the vacuum
  shot(64.82, 67.82, (u, d) => {
    const g = D.grandpaInChair(u, { slump: 0.22, head: 0.3 });
    g.setFace("sleep");
    g.j.armL.rotation.x = g.j.armR.rotation.x = -1.2;
    g.j.armL.rotation.z = -0.45;
    g.j.armR.rotation.z = 0.45;
    const v = P.vacuum;
    v.root.rotation.order = "YXZ";
    v.root.position.set(g.root.position.x + CF[0] * 2.3, 0, g.root.position.z + CF[1] * 2.3);
    v.root.rotation.set(-0.38, Math.atan2(CF[0], CF[1]), 0);
    v.light.material.emissiveIntensity = 2.5;
    const h = gHead();
    D.lights("night", 0, { fill: ahead(h, CF, 5, 1.5, -2).concat([170]) });
    D.zzz(u, [h[0] + 0.5, h[1] + 0.9, h[2]]);
    D.cam({ p: [ahead(h, CF, 6.6, -0.6, 1.3), ahead(h, CF, 5.4, -0.5, 1.0)], l: [h[0], h[1] - 0.7, h[2]], f: h, fov: 36, ap: 12, seed: 26 }, u, d);
  });
  // F20 the clock begins to chime
  shot(67.82, 70.4, (u, d) => {
    D.lights("night", 0, { fill: [-14, 3, -9, 170], lamp: 0.85 });
    W.setClock(11 + 59 / 60 + (u / d) * (0.9 / 60));
    P.clock.pend.rotation.z = Math.sin(u * PI * 2) * 0.16;
    D.cam({ p: [[-13.7, 1.0, -8.5], [-14.3, 1.2, -9.4]], l: [-18.2, 7.2, -13], fov: 40, ap: 8, seed: 27 }, u, d);
  });
  // F21 Twelve.
  shot(70.4, 71.64, (u, d) => {
    D.lights("night", 0, { fill: [-15.6, 8.4, -11.6, 150], lamp: 0.85 });
    W.setClock(12 - (1 - ease.outBack(win(u, 0.06, 0.24, ease.linear))) * (0.6 / 60));
    P.clock.pend.rotation.z = Math.sin(u * PI * 2) * 0.16;
    D.cam({ p: [[-12.9, 8.2, -12.8], [-13.4, 8.2, -12.85]], l: [-17.88, 8.2, -13], fov: 26, ap: 12, seed: 28, shake: 0.02 + bump(u, 0.06, 0.4) * 0.05 }, u, d);
  });
  // F22 the front door creaks open
  shot(71.64, 73.43, (u, d) => {
    const op = 1.25 * (0.45 * win(u, 0.1, 0.7) + 0.55 * win(u, 0.95, 1.7));
    P.door.rotation.y = op;
    D.lights("night", 0, { doorSpill: op / 1.25, lamp: 0.8 });
    D.cam({ p: [[-13.5, 0.55, -1.9], [-13.9, 0.55, -2.5]], l: [-20, 3.2, -6.4], fov: 42, ap: 10, seed: 29 }, u, d);
  });
  // F23 one long, pale hand. Then another.
  shot(73.43, 75.59, (u, d) => {
    P.door.rotation.y = 1.25;
    D.lights("night", 0, { doorSpill: 1, lamp: 0.8, fill: [-16, 7, -1.5, 90] });
    const a = win(u, 0.0, 0.8, ease.out);
    const w0 = lerp3([-22.6, 6.4, -4.4], [-20.9, 6.3, -4.2], a);
    D.aimHand(0, w0, [w0[0] + 1.3, w0[1] - 0.15, w0[2] + 0.9], 0.2 + a * 0.5);
    const b = win(u, 1.25, 2.0, ease.out);
    if (u > 1.2) {
      const w1 = lerp3([-22.6, 3.9, -4.5], [-20.9, 3.8, -4.25], b);
      D.aimHand(1, w1, [w1[0] + 1.3, w1[1] - 0.1, w1[2] + 0.9], 0.2 + b * 0.5);
    }
    D.cam({ p: [[-15.6, 5.8, -0.1], [-16.0, 5.7, -0.5]], l: [-20.0, 5.1, -3.8], f: [-19.8, 6.2, -3.4], fov: 40, ap: 10, seed: 30 }, u, d);
  });
  // F24 the Counter unfolds into the living room
  shot(75.59, 78.24, (u, d) => {
    P.door.rotation.y = 1.25;
    const flick = u > 0.5 && u < 1.6 && Math.sin(u * 37) > 0.55 ? 0.3 : 1;
    D.lights("night", 0, { doorSpill: 1, lamp: flick });
    const c = C.counter;
    const walkIn = win(u, 0, 1.2, ease.out);
    D.place(c, lerp(-19.6, -15.6, walkIn), 0, -6, PI / 2);
    const uf = win(u, 0.6, 2.1);
    c.j.torso.rotation.x = lerp(1.42, 0.06, uf);
    c.j.neck.rotation.x = lerp(-0.45, 0.25, uf);
    c.j.head.rotation.x = lerp(-0.3, 0.05, uf);
    if (u < 1.2) counterWalk(c, u * 3.2, 0.3);
    c.j.upperL.rotation.z = -0.1 - uf * 0.1;
    c.j.upperR.rotation.z = 0.1 + uf * 0.1;
    D.cam({ p: [[-3.6, 1.0, 0.9], [-4.1, 1.1, 0.3]], l: [[-15.5, 6.2, -6], [-15.5, 8.4, -6]], fov: 52, ap: 6, seed: 31 }, u, d);
  });
  // F25 I dove behind the couch
  shot(78.24, 79.92, (u, d) => {
    D.lights("night", 0, { fill: [1.5, 5.5, 11.5, 160] });
    const k = C.kid;
    const s = win(u, 0, 0.62, ease.linear);
    if (u < 0.62) {
      D.place(k, 1.5, 0, lerp(-0.6, 6.8, s), 0);
      k.root.position.y = lerp(2.9, 0, s) + Math.sin(PI * s) * 3.6;
      k.root.rotation.x = s * 1.25;
      k.j.armL.rotation.x = k.j.armR.rotation.x = -2.8;
      k.setFace("shock");
    } else {
      const land = win(u, 0.62, 0.95, ease.out);
      D.place(k, 1.5, 0, lerp(6.8, K0[2], land), 0);
      D.sit(k, 0);
      k.root.rotation.x = lerp(0.8, 0, land);
      k.j.armL.rotation.x = k.j.armR.rotation.x = lerp(-2.4, -0.6, land);
      k.j.head.rotation.y = Math.sin(u * 7) * 0.25 * win(u, 1.0, 1.2);
      k.setFace("scared", { sweat: true });
    }
    D.cam({ p: [[1.1, 1.75, 13.3], [1.0, 1.6, 12.6]], l: [1.4, 2.5, 6.4], fov: 42, ap: 10, seed: 32 }, u, d);
  });
  // F26 he looked at the empty jar, then he started counting
  shot(79.92, 82.76, (u, d) => {
    P.door.rotation.y = 1.25;
    D.lights("night", 0, { doorSpill: 1, fill: [-15.6, 8.2, 3.2, 190] });
    P.jar.setFill(0);
    const c = D.counterStand(-13.6, -2.4, 0, { hunch: 0.38, neck: 0.55 });
    D.faceTo(c, -18.4, 0.6);
    c.j.head.rotation.z = 0.32 * win(u, 0.7, 1.4) * (1 - win(u, 1.6, 1.9));
    const r = win(u, 1.5, 2.0, ease.outBack);
    c.j.upperR.rotation.x = -0.1 - r * 1.3;
    D.point(c, "R", r);
    D.cam({ p: [[-10.4, 6.6, 5.2], [-10.8, 6.6, 4.7]], l: [-16.0, 7.2, -0.8], f: [-17.0, 7.0, -0.6], fov: 58, ap: 8, seed: 33 }, u, d);
  });
  // F27 one lamp / two cushions / forty-one socks / three hundred books
  shot(82.76, 83.12, (u, d) => {
    D.lights("night", 0, { fill: [12, 8, -4.5, 120] });
    P.lamp.shadeMat.emissiveIntensity = 0.7;
    P.lamp.bulb.material.emissiveIntensity = 2.5;
    D.pointAt(0, [14.5, 7.4, -8.1], [-1, 0.3, 0.7], 1.6);
    D.cam({ p: [[10.4, 6.6, -3.2], [10.7, 6.65, -3.6]], l: [14.8, 7.0, -8.4], f: [15.5, 7.2, -9], fov: 34, ap: 14, seed: 34 }, u, d);
  });
  shot(83.12, 84.02, (u, d) => {
    D.lights("night", 0, { fill: [-1, 7, -4, 160] });
    const tgt = u < 0.45 ? [-4.6, 3.7, 3.5] : [-2.6, 2.95, 2.0];
    D.pointAt(0, tgt, [0.1, 1, -0.75], 1.6);
    D.cam({ p: [[-3.2, 5.8, -3.4], [-3.4, 5.6, -3.0]], l: [-3.6, 3.0, 2.8], f: tgt, fov: 44, ap: 10, seed: 35 }, u, d);
  });
  shot(84.02, 85.02, (u, d) => {
    D.lights("night", 0, { fill: [-6, 6, 3, 170] });
    D.pointAt(0, [-8.5, 2.3 - bump(u, 0.3, 0.6) * 0.25, 6.0], [0.4, 1, -0.6], 1.6);
    D.cam({ p: [[-11.8, 5.0, 2.6], [-11.5, 4.8, 3.0]], l: [-8.6, 1.8, 6.2], f: [-8.6, 2.0, 6.0], fov: 40, ap: 12, seed: 36 }, u, d);
  });
  shot(85.02, 86.28, (u, d) => {
    D.lights("night", 0, { fill: [-9, 8, -9, 170] });
    const tgt = [-7.8 - (u / d) * 6.4, 6.4 - (u / d) * 1.4, -14.1];
    D.pointAt(0, tgt, [0.5, 0.5, 1], 1.6);
    D.cam({ p: [[-8.8, 6.7, -8.6], [-9.3, 6.6, -9.0]], l: [-11, 6.0, -15.2], f: tgt, fov: 36, ap: 12, seed: 37 }, u, d);
  });
  // F28 getting closer to Grandpa (from behind his chair)
  shot(86.28, 89.91, (u, d) => {
    D.lights("night", 0, { fill: [6, 9, -1, 170] });
    const g = D.grandpaInChair(u);
    D.snoreFace(g, u, 2.4);
    const c = C.counter;
    const k = u / d;
    D.place(c, lerp(-4.5, 4.2, k), 0, lerp(-4.2, -2.8, k), 0);
    D.faceTo(c, 10.8, -4.8);
    counterWalk(c, u * 3.4);
    c.j.torso.rotation.x = 0.2;
    c.j.neck.rotation.x = 0.35;
    c.j.upperR.rotation.x = -1.2;
    c.j.upperR.rotation.y = Math.sin(u * 7) * 0.6;
    c.j.head.rotation.y = Math.sin(u * 7 + 0.5) * 0.4;
    D.point(c, "R");
    const h = cHead();
    D.cam({ p: [[14.8, 6.7, -8.5], [14.1, 6.3, -7.9]], l: [h[0], h[1] - 2.5, h[2]], f: h, fov: 44, ap: 10, seed: 38 }, u, d);
  });
  // F29 then I saw the vacuum
  shot(89.91, 91.42, (u, d) => {
    D.lights("night", 0, { fill: [11, 4.6, 1.2, 150] });
    D.grandpaInChair(u).setFace("sleep");
    D.cam({ p: [[7.4, 3.4, 2.7], [9.1, 3.1, 1.4]], l: [13.9, 2.4, -1.6], f: [[6.2, 2.6, 2.6], [13.9, 2.4, -1.6]], fe: (x) => win(x, 0.15, 0.6), fov: 30, ap: 18, seed: 39 }, u, d);
  });
  // F30a ripped off the lid
  const KV = [12.3, 0, 0.5];
  function kidAtVacuum(face = "determined") {
    const k = C.kid;
    D.place(k, KV[0], 0, KV[2], 0);
    D.faceTo(k, 13.9, -1.6);
    k.setFace(face);
    return k;
  }
  shot(91.42, 92.4, (u, d) => {
    D.lights("night", 0, { fill: [11.5, 6.5, 2.5, 200] });
    D.grandpaInChair(u).setFace("sleep");
    const k = kidAtVacuum();
    k.j.armL.rotation.x = k.j.armR.rotation.x = -1.35 - win(u, 0.3, 0.6) * 0.9;
    const v = P.vacuum;
    const pop = win(u, 0.3, 0.85, ease.out);
    v.lid.position.set(v.homes.lid.x + pop * 1.2, v.homes.lid.y + pop * 3.2, v.homes.lid.z + pop * 1.5);
    v.lid.rotation.set(pop * 2.5, 0, pop * 1.4);
    const lp = D.wpos(v.lid);
    D.cam({ p: [[lp[0] - 2.6, lp[1] + 0.6, lp[2] + 2.6], [lp[0] - 2.3, lp[1] + 0.5, lp[2] + 2.3]], l: [lp[0], lp[1] - 0.3, lp[2]], f: lp, fov: 34, ap: 16, seed: 40 }, u, d);
  });
  // F30b yanked out the bag
  shot(92.4, 93.5, (u, d) => {
    D.lights("night", 0, { fill: [11.5, 6.5, 2.5, 200] });
    D.grandpaInChair(u).setFace("sleep");
    const k = kidAtVacuum();
    const v = P.vacuum;
    v.lid.visible = false;
    const y = win(u, 0.15, 0.7, ease.out3);
    v.bag.position.set(v.homes.bag.x, v.homes.bag.y + y * 1.6, v.homes.bag.z + y * 3.4);
    v.bag.rotation.x = -y * 0.5;
    k.j.armL.rotation.x = k.j.armR.rotation.x = -1.3 + y * 0.4;
    k.j.torso.rotation.x = -y * 0.2;
    const bp = D.wpos(v.bag);
    D.cam({ p: [[bp[0] + 1.2, bp[1] + 0.5, bp[2] + 3.6], [bp[0] + 1.0, bp[1] + 0.4, bp[2] + 3.1]], l: bp, fov: 36, ap: 14, seed: 41 }, u, d);
  });
  // F30c threw it as high as I could (slow motion, low angle)
  shot(93.5, 95.1, (u, d) => {
    D.lights("night", 0, { fill: [12.5, 3, 3, 200] });
    D.grandpaInChair(u).setFace("sleep");
    const k = C.kid;
    D.place(k, 12.0, 0, 0.8, 0);
    D.faceTo(k, 5, -3);
    k.setFace("determined");
    const sw = win(u, 0, 0.45, ease.out);
    k.j.armL.rotation.x = k.j.armR.rotation.x = lerp(-0.6, -3.05, sw);
    k.j.torso.rotation.x = lerp(0.15, -0.15, sw);
    P.vacuum.lid.visible = false;
    const v = P.vacuum, b = v.bag;
    scene.add(b);
    b.scale.setScalar(0.65);
    const fl = win(u, 0.3, 1.5, ease.out);
    b.position.set(lerp(11.6, BAG[0], fl), lerp(5.6, BAG[1], fl), lerp(0.2, BAG[2], fl));
    b.rotation.set(fl * 5, fl * 2, fl * 3);
    if (u > 1.42) dustCloud(93.5 + u + 0.0);
    D.cam({ p: [[8.4, 1.5, -2.4], [8.6, 1.6, -2.1]], l: [[11.6, 4.6, 0.6], [11.0, 9.5, -1.2]], fov: 60, ap: 7, seed: 42 }, u, d);
  });
  // F31 rice and dust rain down over the whole room
  shot(95.1, 97.9, (u, d, t) => {
    D.lights("night", 0, { fill: [8, 10, 6, 130] });
    pipe.bloom.strength = 0.6;
    riceRain(t);
    dustCloud(t);
    D.grandpaInChair(u).setFace("sleep");
    const c = D.counterStand(C0[0], C0[2], 0.2, { hunch: 0.05, neck: -0.35 });
    c.j.head.rotation.x = -0.3;
    c.j.upperL.rotation.z = -0.5;
    c.j.upperR.rotation.z = 0.5;
    const k = C.kid;
    D.place(k, 8.6, 0, 1.6, 0);
    D.faceTo(k, 5, -6);
    k.j.head.rotation.x = -0.4;
    k.setFace("shock");
    D.cam({ p: [[15.6, 7.0, 11.2], [14.7, 6.6, 10.2]], l: [2, 4.6, -5], fov: 56, ap: 5, seed: 43 }, u, d);
  });
  // the Counter crouched over the rice, counting
  function counterCounting(u, tapTimes = [], speed = 0) {
    const c = C.counter;
    D.place(c, C0[0], 0, C0[2], 0.2);
    D.counterCrouch(c, 1);
    c.j.upperR.rotation.x = -0.75;
    c.j.foreR.rotation.x = -0.75;
    let tap = 0;
    tapTimes.forEach((tt, i) => (tap = Math.max(tap, bump(u, tt - 0.12, tt + 0.12))));
    c.j.upperR.rotation.x += tap * 0.18 + (speed ? Math.sin(u * speed) * 0.15 : 0);
    c.j.upperR.rotation.y = -0.2 + tapTimes.filter((tt) => u > tt).length * 0.12;
    D.point(c, "R");
    c.j.upperL.rotation.x = -0.5;
    return c;
  }
  // F32 the Counter froze; all six eyes went wide
  shot(97.9, 100.66, (u, d, t) => {
    D.lights("night", 0, { fill: [3.5, 11, 1, 170] });
    riceRain(t);
    dustCloud(t);
    D.grandpaInChair(u).setFace("sleep");
    const c = D.counterStand(C0[0], C0[2], 0.2, { hunch: 0.05, neck: 0.05 });
    const w = win(u, 1.85, 2.1, ease.outBack);
    c.setEyes(1 + w * 0.55, 0, w * 0.06 * Math.sin(u * 50));
    const h = cHead();
    D.cam({ p: [[h[0] + 1.2, h[1] - 1.4, h[2] + 8.0], [h[0] + 0.8, h[1] - 1.0, h[2] + 6.4]], l: [h[0], h[1] - 0.5, h[2]], fov: 32, ap: 14, seed: 44 }, u, d);
  });
  // F33 One. Two. Three.
  shot(100.66, 101.94, (u, d, t) => {
    D.lights("night", 0, { fill: [6.5, 3, -0.5, 170] });
    riceRain(t);
    const c = counterCounting(u, [0.05, 0.37, 0.74]);
    c.setEyes(1.2);
    const fp = D.wpos(c.j.handR, [0, -1.2, 0]);
    D.cam({ p: [[8.8, 4.2, 2.8], [8.4, 4.0, 2.4]], l: [fp[0] + 0.6, fp[1] + 2.6, fp[2] - 0.6], f: fp, fov: 44, ap: 10, seed: 45 }, u, d);
  });
  // F34 he got all the way to nine hundred (kid peeks over the couch)
  shot(101.94, 104.09, (u, d, t) => {
    D.lights("night", 0, { fill: [4.5, 6, 9.5, 190] });
    riceRain(t);
    dustHang(t, 500);
    counterCounting(u, [], 24);
    D.grandpaInChair(u).setFace("sleep");
    const k = C.kid;
    D.place(k, K0[0], 0, K0[2] + 0.1, PI);
    k.j.torso.rotation.x = 0.36;
    k.j.head.rotation.x = -0.32;
    k.j.armL.rotation.x = k.j.armR.rotation.x = -1.45;
    k.setFace(u < 1.2 ? "worried" : "determined");
    const h = kHead();
    D.cam({ p: [[5.4, 5.3, -0.6], [5.0, 5.2, -0.2]], l: [h[0], h[1] - 0.3, h[2]], f: h, fov: 34, ap: 12, seed: 46 }, u, d);
  });
  // big snore helper: peaks in the given windows
  function bigSnore(g, u, peaks) {
    const on = peaks.some(([a, b]) => u > a && u < b);
    g.setFace(on ? "bigSnore" : "sleep");
    const amt = Math.max(...peaks.map(([a, b]) => bump(u, a, b)));
    g.j.head.rotation.x -= amt * 0.25;
    const st = g.j.headTop.getObjectByName("stache");
    if (st) st.position.y = -0.06 + Math.sin(u * 60) * 0.025 * amt;
    return amt;
  }
  // F35 then Grandpa snored
  shot(104.09, 105.88, (u, d, t) => {
    riceRain(t);
    const g = D.grandpaInChair(u);
    const amt = bigSnore(g, u, [[1.15, 1.78]]);
    const h = gHead();
    D.lights("night", 0, { fill: ahead(h, CF, 4, 1.2, -1.6).concat([170]) });
    D.zzz(u, [h[0] + 0.6, h[1] + 0.8, h[2]], 1 + amt * 0.9);
    D.cam({ p: [ahead(h, CF, 3.2, -0.25, 0.4), ahead(h, CF, 2.7, -0.2, 0.3)], l: h, fov: 30, ap: 18, seed: 47, shake: 0.04 + amt * 0.06 }, u, d);
  });
  // F36 the Counter flinched; he'd lost count
  shot(105.88, 107.88, (u, d, t) => {
    D.lights("night", 0, { fill: [-2.5, 7, 2, 170] });
    riceRain(t);
    const c = counterCounting(u);
    const snap = win(u, 0.08, 0.22, ease.out3) * (1 - win(u, 1.2, 1.8));
    c.j.head.rotation.y = snap * 0.9;
    c.j.torso.rotation.x -= snap * 0.18;
    c.setEyes(1.12, 0, 0.25 * Math.sin(u * 31) * snap);
    D.point(c, "R", 1 - snap);
    c.j.upperR.rotation.y = Math.sin(u * 4) * 0.3 * snap;
    const h = cHead();
    D.cam({ p: [[-3.2, 6.0, 5.0], [-2.8, 6.1, 4.4]], l: [h[0], h[1] - 1.0, h[2]], f: h, fov: 42, ap: 10, seed: 48 }, u, d);
  });
  // F37 One. Two. Three. (again, from above)
  shot(107.88, 109.16, (u, d, t) => {
    D.lights("night", 0, { fill: [3.4, 6, -1.6, 150] });
    riceRain(t);
    const taps = [0.1, 0.42, 0.78];
    const n = taps.filter((tt) => u > tt - 0.12).length;
    const tgt = [3.0 + n * 0.32, 0.12 + (1 - Math.max(...taps.map((tt) => bump(u, tt - 0.14, tt + 0.14)))) * 0.45, -2.0 + n * 0.12];
    D.pointAt(0, tgt, [-0.35, 1, -0.55], 1.6);
    D.cam({ p: [3.4, 9.2, -1.9], l: [3.4, 0, -1.95], up: [0, 0, -1], fov: 40, ap: 8, f: [3.4, 0.1, -1.95], seed: 49 }, u, d);
  });
  // F38 every time he got close, Grandpa snored again
  shot(109.16, 112.14, (u, d, t) => {
    D.lights("night", 0, { fill: [13, 7, -1, 170] });
    riceRain(t);
    const g = D.grandpaInChair(u);
    const peaks = [[0.25, 0.75], [1.7, 2.3]];
    bigSnore(g, u, peaks);
    const c = counterCounting(u, [], 18);
    const fl = Math.max(...peaks.map(([a]) => bump(u, a + 0.08, a + 0.55)));
    c.j.torso.rotation.x -= fl * 0.35;
    c.j.upperL.rotation.x = -0.5 - fl * 0.9;
    c.j.upperR.rotation.x -= fl * 0.7;
    c.j.head.rotation.y = fl * 0.7;
    c.setEyes(1 + fl * 0.3);
    D.cam({ p: [[16.6, 7.6, -3.0], [16.3, 7.5, -3.2]], l: [4.8, 5.4, -4.7], f: [7.0, 5.6, -4.6], fov: 46, ap: 6, seed: 50 }, u, d);
  });
  // F39 All. Night. Long. (time-lapse)
  shot(112.14, 113.89, (u, d, t) => {
    const k = 0.12 + 0.68 * (u / d);
    D.lights("dawn", k);
    riceRain(t);
    W.setClock(1 + (u / d) * 4.5);
    counterCounting(u, [], 40);
    const g = D.grandpaInChair(u);
    D.snoreFace(g, u * 3, 1.2);
    kidHide(u, false);
    C.kid.setFace("sleep");
    C.kid.j.head.rotation.x = 0.4;
    D.cam({ p: [[17.2, 10.2, 12.8], [16.7, 9.9, 12.2]], l: [-3, 3.5, -8], fov: 62, ap: 3, seed: 51 }, u, d);
  });
  // F40a when the sun hit the window
  shot(113.89, 115.1, (u, d, t) => {
    D.lights("dawn", 0.8 + 0.2 * win(u, 0, 0.8));
    pipe.bloom.strength = 0.7;
    riceRain(t);
    dustHang(t, 1400);
    D.cam({ p: [[3.0, 3.0, -6.4], [3.3, 3.2, -7.4]], l: [4, 7.2, -16], fov: 44, ap: 6, seed: 52 }, u, d);
  });
  // F40b the Counter stood up
  shot(115.1, 116.5, (u, d, t) => {
    D.lights("dawn", 1, { fill: [1.5, 6, 3, 120] });
    riceRain(t);
    dustHang(t, 900);
    const c = counterCounting(u);
    D.counterCrouch(c, 1 - win(u, 0, 1.0));
    c.j.upperR.rotation.x = lerp(-0.75, -0.1, win(u, 0, 0.8));
    D.point(c, "R", 0);
    c.j.head.rotation.y = -0.3 * win(u, 0.9, 1.35);
    D.cam({ p: [[0.6, 1.2, 0.4], [0.7, 1.0, 0.9]], l: [[2.5, 5.5, -4.5], [2.5, 10.8, -4.5]], fov: 52, ap: 6, seed: 53 }, u, d);
  });
  // F40c stared at me with all six eyes
  shot(116.5, 118.1, (u, d, t) => {
    riceRain(t);
    dustHang(t, 700);
    const c = D.counterStand(C0[0], C0[2], 0, { hunch: 0.12, neck: 0.55 });
    D.faceTo(c, K0[0], K0[2]);
    c.j.head.rotation.x = 0.25;
    c.setEyes(1.1, 0);
    const h = cHead();
    const toKid = [K0[0] - h[0], 0, K0[2] - h[2]];
    const n = Math.hypot(toKid[0], toKid[2]);
    const dir = [toKid[0] / n, toKid[2] / n];
    D.lights("dawn", 1, { fill: [h[0] + dir[0] * 5, h[1] - 1, h[2] + dir[1] * 5, 240] });
    D.cam({ p: [ahead(h, dir, 6.8, -1.8, 0, [0, 0]), ahead(h, dir, 5.4, -1.5, 0, [0, 0])], l: [h[0], h[1] - 0.3, h[2]], fov: 30, ap: 16, seed: 54 }, u, d);
  });
  // F40d folded himself back out the door
  shot(118.1, 120.55, (u, d, t) => {
    D.lights("dawn", 1);
    riceRain(t);
    dustHang(t, 700);
    P.door.rotation.y = 1.25 * (1 - win(u, 1.75, 2.4, ease.inOut3));
    const c = C.counter;
    const go = win(u, 0, 1.75, ease.in);
    D.place(c, lerp(-12.6, -21.5, go), 0, -6, -PI / 2);
    c.j.torso.rotation.x = lerp(0.08, 1.42, win(u, 0.25, 1.0));
    c.j.neck.rotation.x = lerp(0.2, -0.4, win(u, 0.25, 1.0));
    counterWalk(c, u * 3.6, 0.3);
    c.root.visible = go < 0.995;
    D.cam({ p: [[-6.4, 3.0, 3.9], [-7.0, 3.1, 3.3]], l: [-17, 4.8, -6], fov: 44, ap: 6, seed: 55 }, u, d);
  });
  // F41 Grandpa woke up, looked at the floor, and sighed
  shot(120.55, 123.41, (u, d, t) => {
    riceRain(t);
    dustHang(t, 600);
    const g = D.grandpaInChair(u, { slump: 0.15, head: 0.1 });
    g.setFace(u < 0.35 ? "sleep" : u > 2.25 && u < 2.75 ? "sigh" : "flat");
    g.j.head.rotation.x = 0.1 + win(u, 0.9, 1.7) * 0.45 - win(u, 2.6, 2.86) * 0.1;
    const h = gHead();
    D.lights("dawn", 1, { fill: ahead(h, CF, 5, 1, -1.5).concat([200]) });
    D.cam({ p: [ahead(h, CF, 4.4, -0.6, 1.0), ahead(h, CF, 3.9, -0.5, 0.9)], l: [h[0], h[1] - 0.4, h[2]], f: h, fov: 34, ap: 12, seed: 56 }, u, d);
  });
  // F42 "Who made this mess?"
  shot(123.41, 124.87, (u, d, t) => {
    riceRain(t);
    dustHang(t, 500);
    const g = D.grandpaInChair(u, { slump: 0.15, head: 0.1 });
    g.setFace("flat");
    g.j.head.rotation.x = 0.05;
    g.j.head.rotation.y = -0.25 * win(u, 0.15, 0.55);
    const h = gHead();
    D.lights("dawn", 1, { fill: ahead(h, CF, 4, 0.8, -1).concat([210]) });
    D.cam({ p: [ahead(h, CF, 3.8, -0.3, 0.4), ahead(h, CF, 3.5, -0.25, 0.35)], l: [h[0], h[1] - 0.25, h[2]], fov: 30, ap: 16, seed: 57 }, u, d);
  });
  // F43 end card: the kid and Biscuit, dust-covered, behind the couch
  shot(124.87, 127.6, (u, d, t) => {
    D.lights("dawn", 1, { fill: [2.5, 5, 12, 200] });
    riceRain(t);
    dustHang(t, 500);
    kidHide(u, false);
    C.kid.setFace("wink");
    C.kid.j.head.rotation.y = 0.15;
    const g = C.dog;
    D.place(g, 4.6, 0, 7.6, 0);
    D.faceTo(g, 1.5, 6.5);
    D.dogSit(0);
    g.j.tail.rotation.y = Math.sin(u * 14) * 0.7;
    pipe.grade.uniforms.uFade.value = 0.42 * win(u, 0, 0.35);
    D.cam({ p: [[3.0, 3.4, 15.6], [3.0, 3.2, 15.0]], l: [3.0, 2.3, 6.9], fov: 42, ap: 10, seed: 58 }, u, d);
  });

  return S;
}
