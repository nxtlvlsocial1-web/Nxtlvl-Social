// The Lying House, shot by shot. Times are seconds on audio/vo.wav; word cues from src/captions-data.js.
import * as THREE from "three";
import { makeDirector } from "./direct.js";
import { EXT, DIN, BRC, END_Z, HALL_H, doorZ } from "./world.js";
import { ease, win, lerp, lerp3, clamp, rng } from "./util.js";

const PI = Math.PI;
const bump = (u, a, b) => (u <= a || u >= b ? 0 : Math.sin(((u - a) / (b - a)) * PI));
export const T_POP1 = 2.95; // "grows"
export const T_DOOR48 = 20.37; // "then last night, a new door appeared"
export const T_OPEN48 = 33.19; // the kid opens it
export const T_DOOR49 = 53.6; // "Room 49"

export function buildShots(ctx) {
  const D = makeDirector(ctx);
  const { C, W, pipe, scene } = ctx;
  const P = W.props;
  const S = [];
  const shot = (t0, t1, run) => S.push({ t0, t1, run });
  const head = (a) => D.wpos(a.j.head, [0, 0.62, 0]);
  const dogHead = () => D.wpos(C.dog.j.head, [0, 0.3, 0.5]);

  // ---- poses -----------------------------------------------------------------
  function oath(a, k = 1) {
    a.j.armR.rotation.z = 2.75 * k;
    a.j.armR.rotation.x = -0.15 * k;
    a.j.armL.rotation.x = -1.3 * k;
    a.j.armL.rotation.z = 0.65 * k;
  }
  function armsCrossed(a, k = 1) {
    a.j.armL.rotation.x = a.j.armR.rotation.x = -1.45 * k;
    a.j.armL.rotation.z = 0.95 * k;
    a.j.armR.rotation.z = -0.95 * k;
  }
  function seat(a, who) {
    const c = P.chairs[who];
    D.place(a, c.x, 0, c.z, c.ry);
    D.sit(a, 2.2);
    a.j.armL.rotation.x = a.j.armR.rotation.x = -1.2;
    return a;
  }
  function door(n, k) {
    P.doors[n].pivot.rotation.y = 1.35 * k;
  }
  function dust(fn, n) {
    const a = W.dust.geometry.attributes.position;
    for (let i = 0; i < n; i++) {
      const p = fn(i);
      a.setXYZ(i, p[0], p[1], p[2]);
    }
    a.needsUpdate = true;
    W.dust.geometry.setDrawRange(0, n);
    W.dust.visible = true;
  }
  const DR = rng(9);
  const dseed = Array.from({ length: 1500 }, () => [DR() * 2 - 1, DR(), DR() * 2 - 1, DR()]);
  // a puff of dust from a point: spreads and settles over ~2 s
  function puff(at, tau, spread = 3, n = 500) {
    if (tau <= 0) return;
    dust((i) => {
      const [a, b, c, r] = dseed[i];
      const k = 1 - Math.exp(-tau * 2.2);
      return [at[0] + a * spread * k, Math.max(0.1, at[1] + b * spread * 0.6 * k - tau * 0.5 * r), at[2] + c * spread * 0.6 * k];
    }, n);
  }
  // dust falling from the ceiling (rumble)
  function ceilingDust(z0, tau, n = 700) {
    dust((i) => {
      const [a, b, c, r] = dseed[i];
      const y = HALL_H - ((tau * (1.2 + r * 1.5) + b * 3) % HALL_H);
      return [a * 3.8, y, z0 + c * 10];
    }, n);
  }
  // family standing in a row (used in the hallway and in the broccoli hall)
  function family(base, ry, { lookUp = 0 } = {}) {
    const spots = [[-2.3, 0.9, C.dad], [-0.75, -0.3, C.mom], [0.85, 0.5, C.sister], [2.35, -0.2, C.grandma]];
    for (const [dx, dz, a] of spots) {
      D.place(a, base[0] + Math.cos(ry) * dx + Math.sin(ry) * dz, 0, base[2] - Math.sin(ry) * dx + Math.cos(ry) * dz, ry);
      a.j.head.rotation.x = -lookUp;
      D.idle(a, base[0] + dx);
    }
  }

  // ==========================================================================
  // F01 hook: the house grows a new room
  shot(0, 4.03, (u, d, t) => {
    D.lights("ext");
    const pr = P.popRooms[0];
    const k = win(t, T_POP1, T_POP1 + 0.55, ease.outBack);
    pr.grp.scale.setScalar(Math.max(0.0001, k));
    puff([EXT.x + pr.x, pr.y - 2, pr.z + 1], t - T_POP1, 4, 400);
    const shake = bump(t, T_POP1, T_POP1 + 0.4) * 0.15;
    D.cam({ p: [[EXT.x - 5, 4.5, 62], [EXT.x - 4, 6.0, 54]], l: [[EXT.x + 0.5, 13.5, 0], [EXT.x + 1.0, 14.5, 0]], fov: 50, ap: 3, shake: 0.03 + shake, seed: 1 }, u, d);
  });
  // F02 we have 47 rooms: endless hallway
  shot(4.03, 5.87, (u, d) => {
    const cz = lerp(6, -16, ease.inOut(u / d));
    D.lights("hall", 0, { camZ: cz });
    D.cam({ p: [[0, 4.6, 6], [0, 4.3, -16]], l: [[0, 4.2, -60], [0, 4.0, -80]], fov: 52, ap: 4, seed: 2 }, u, d);
  });
  // F03a room 12 showed up: the door opens on meatloaf
  shot(5.87, 6.85, (u, d) => {
    const z = doorZ(12);
    D.lights("hall", 0, { camZ: z + 5, at: [2.5, 0, z], fill: [-2, 5, z + 4, 140] });
    door(12, win(u, 0.05, 0.5, ease.out));
    P.rooms[12].spill.forEach((l, i) => {
      const f = win(u, 0.25 + i * 0.07, 0.75 + i * 0.07, ease.in);
      l.visible = true;
      l.position.set(lerp(5.2, 2.2 - i * 0.6, f), Math.max(0.45, lerp(2.5 + i * 0.9, 0.45, f) + Math.sin(f * PI) * 0.8), z + (i - 1) * 0.9);
      l.rotation.set(f * 1.5 * (i - 1), i, f * 2.2);
    });
    D.cam({ p: [[-2.6, 4.3, z + 5.6], [-2.2, 4.1, z + 4.8]], l: [3.5, 3.0, z], fov: 44, ap: 8, seed: 3 }, u, d);
  });
  // F03b when Dad said he loved Mom's meatloaf
  shot(6.85, 9.21, (u, d) => {
    D.lights("dining", 0, { fill: [DIN.x + 2.4, 6.5, 3.5, 110] });
    const dad = seat(C.dad, "dad");
    seat(C.mom, "mom").setFace("momSmile");
    seat(C.grandma, "grandma");
    dad.setFace(u > 0.9 ? "forced" : "smile", u > 0.9 ? { sweat: true } : {});
    const thumbs = win(u, 1.0, 1.3, ease.outBack);
    dad.j.armR.rotation.x = -1.2 - thumbs * 0.6;
    dad.j.armR.rotation.z = -thumbs * 0.2;
    dad.j.head.rotation.y = -0.25 * win(u, 0.2, 0.6);
    C.mom.j.head.rotation.y = 0.5;
    const h = head(dad);
    D.cam({ p: [[DIN.x + 1.6, 5.8, 4.2], [DIN.x + 1.8, 5.6, 3.5]], l: [h[0] - 0.6, h[1] - 0.6, h[2]], f: h, fov: 40, ap: 12, seed: 4 }, u, d);
  });
  // F04 room 30: homework towers
  shot(9.21, 10.89, (u, d) => {
    const z = doorZ(30);
    D.lights("hall", 0, { camZ: z + 5, fill: [-2, 5, z + 4, 70] });
    door(30, win(u, 0.05, 0.5, ease.out));
    P.rooms[30].sheets.forEach((sh, i) => {
      const f = win(u, 0.3 + (i % 5) * 0.06, 1.6, ease.out);
      sh.visible = f > 0;
      sh.position.set(lerp(5.5, 1.5 - (i % 4) * 0.6, f), 2 + (i % 7) * 0.6 + Math.sin(u * 3 + i) * 0.3 * f, z + ((i % 5) - 2) * 0.7);
      sh.rotation.set(Math.sin(u * 2 + i) * 0.8, i, Math.cos(u * 3 + i) * 0.6);
    });
    D.cam({ p: [[-2.6, 4.4, z + 5.8], [-2.2, 4.2, z + 4.9]], l: [3.5, 3.4, z], fov: 44, ap: 8, seed: 5 }, u, d);
  });
  // F05 "I already did my homework!"
  shot(10.89, 12.71, (u, d) => {
    const z = doorZ(30);
    D.lights("hall", 0, { camZ: z + 4, fill: [-1.5, 6, z + 7, 110] });
    const s = C.sister;
    D.place(s, 0.9, 0, z + 2.6, 0);
    D.faceTo(s, -1.6, z + 7.4);
    s.setFace(u < 0.35 ? "flat" : "eyeroll");
    s.j.armR.rotation.x = -1.5;
    s.j.armR.rotation.z = -0.2;
    s.j.head.rotation.z = 0.12 * win(u, 0.3, 0.6);
    s.j.head.rotation.x = -0.08;
    const h = head(s);
    D.cam({ p: [[-1.8, 5.0, z + 8.6], [-1.6, 5.0, z + 7.9]], l: [h[0], h[1] - 1.1, h[2]], f: h, fov: 38, ap: 12, seed: 6 }, u, d);
  });
  // F06a room 47 is a tiny closet
  shot(12.71, 15.05, (u, d) => {
    const z = doorZ(47);
    D.lights("hall", 0, { camZ: z + 4, at: [-2.5, 0, z], fill: [1, 3, z + 4, 130] });
    D.cam({ p: [[3.0, 3.2, z + 8.2], [2.7, 3.0, z + 7.2]], l: [-4, 2.6, z + 1.4], fov: 46, ap: 6, seed: 7 }, u, d);
  });
  // F06b that's Grandma, telling everyone…
  shot(15.05, 16.95, (u, d) => {
    const z = doorZ(47);
    D.lights("hall", 0, { camZ: z + 4, fill: [1.5, 6, z + 7, 120] });
    const g = C.grandma;
    D.place(g, -1.4, 0, z + 3.2, 0);
    D.faceTo(g, 1.4, z + 7.4);
    g.setFace(u > 0.9 && u < 1.5 ? "wink" : "momSmile");
    g.j.armL.rotation.z = -0.6;
    g.j.armL.rotation.x = -0.2;
    g.j.armR.rotation.x = -1.0;
    g.j.armR.rotation.z = -0.4;
    g.j.head.rotation.z = -0.1;
    const h = head(g);
    D.cam({ p: [[1.5, 4.8, z + 7.4], [1.3, 4.8, z + 6.8]], l: [h[0], h[1] - 0.8, h[2]], f: h, fov: 34, ap: 14, seed: 8 }, u, d);
  });
  // F06c …she's 39: the closet bursts with balloons
  shot(16.95, 18.13, (u, d) => {
    const z = doorZ(47);
    D.lights("hall", 0, { camZ: z + 4, at: [-2.5, 0, z + 1], fill: [1.5, 4, z + 5, 160] });
    door(47, win(u, 0.0, 0.3, ease.out3));
    const f = win(u, 0.15, 1.18, ease.out);
    P.rooms[47].balloons.forEach(({ obj, a, b, c }) => {
      obj.position.set(lerp(-5.3 - a * 2.6, -3 + a * 6, f), lerp(0.6 + b * 2.4, 2 + b * 6.5, f) + Math.sin(u * 3 + a * 9) * 0.15, lerp(z + (c - 0.5) * 1.6, z + 1 + (c - 0.2) * 5, f));
      obj.rotation.z = Math.sin(u * 2 + c * 7) * 0.3;
    });
    P.rooms[47].nums.forEach((m, i) => {
      m.visible = true;
      m.position.set(lerp(-5.5, -1.6 + i * 1.5, f), lerp(1.6, 4.6, f) + Math.sin(u * 2.4 + i) * 0.12, lerp(z, z + 2.4, f));
      m.rotation.y = lerp(PI / 2, 0.15, f) + Math.sin(u * 2 + i) * 0.1;
    });
    D.cam({ p: [[2.7, 3.2, z + 6.2], [2.4, 3.6, z + 5.6]], l: [[-2.5, 3.0, z + 0.5], [-1.2, 4.0, z + 1.5]], fov: 48, ap: 6, seed: 9 }, u, d);
  });
  // F07 and every new room is full of the lie
  shot(18.13, 20.37, (u, d) => {
    D.lights("hall", 0, { camZ: -20 });
    door(12, 1);
    door(30, 1);
    P.rooms[12].spill.forEach((l, i) => {
      l.visible = true;
      l.position.set(2.2 - i * 0.6, 0.45, doorZ(12) + (i - 1) * 0.9);
      l.rotation.set(1.5 * (i - 1), i, 2.2);
    });
    P.rooms[30].sheets.forEach((sh, i) => {
      sh.visible = true;
      sh.position.set(1.5 - (i % 4) * 0.6, 0.05 + (i % 3) * 0.02, doorZ(30) + ((i % 5) - 2) * 0.7 + 1);
      sh.rotation.set(-PI / 2, 0, i);
    });
    D.cam({ p: [[-2.0, 6.3, -12], [-1.8, 6.1, -17]], l: [[1.2, 2.2, -40], [1.4, 2.2, -48]], fov: 46, ap: 5, seed: 10 }, u, d);
  });
  // F08 last night, a new door appeared at the end of the hallway
  shot(20.37, 23.66, (u, d, t) => {
    const rise = win(u, 0.7, 2.7, ease.out);
    P.doors[48].root.position.y = lerp(-7.8, 0, rise);
    const quake = (rise > 0 && rise < 1 ? 1 : 0) * 0.08;
    D.lights("hall", 0, { night: true, camZ: END_Z + 20, fill: [0, 5, END_Z + 12, 90] });
    puff([0, 0.3, END_Z + 0.8], u - 0.7, 4, 600);
    D.cam({ p: [[0.9, 1.25, END_Z + 21], [0.9, 1.35, END_Z + 18.5]], l: [0, 3.6, END_Z], fov: 40, ap: 6, shake: 0.03 + quake, seed: 11 }, u, d);
  });
  // F09 Room 48.
  shot(23.66, 25.28, (u, d) => {
    const fl = Math.sin(u * 31) > 0.7 && u > 0.5 ? 0.4 : 1;
    D.lights("hall", 0, { night: true, camZ: END_Z + 6, flicker: fl, fill: [0.4, 7.6, END_Z + 5, 45 * fl] });
    D.cam({ p: [[0.35, 7.7, END_Z + 3.4], [0.3, 7.72, END_Z + 2.7]], l: [0, 7.72, END_Z], fov: 34, ap: 10, seed: 12 }, u, d);
  });
  // F10 so we had a family meeting
  shot(25.28, 26.82, (u, d) => {
    D.lights("dining", 0, { fill: [DIN.x - 6, 7, 6, 120] });
    P.dadLoaf.visible = false;
    for (const [a, w] of [[C.kid, "kid"], [C.mom, "mom"], [C.dad, "dad"], [C.sister, "sister"], [C.grandma, "grandma"]]) seat(a, w);
    C.dad.j.head.rotation.y = 0.4 * Math.sin(u * 2);
    C.mom.j.head.rotation.y = -0.4 * Math.sin(u * 2 + 1);
    C.sister.j.head.rotation.y = 0.5 * Math.sin(u * 1.6 + 2);
    C.grandma.j.head.rotation.y = 0.3 * Math.sin(u * 1.8);
    for (const a of [C.dad, C.mom, C.sister, C.kid]) a.setFace("worried");
    C.grandma.setFace("flat");
    D.place(C.dog, DIN.x - 4.6, 0, DIN.z + 4.4, 0.4);
    D.dogSit(0);
    D.cam({ p: [[DIN.x - 0.5, 10.5, 11.0], [DIN.x - 0.4, 10.0, 10.2]], l: [DIN.x + 0.8, 3.2, -0.4], fov: 48, ap: 4, seed: 13 }, u, d);
  });
  // F11 Dad swore / Mom swore / Sister swore on her phone
  function meetingCU(a, who, u, d, seed, side = 1) {
    D.lights("dining", 0, { fill: [P.chairs[who].x + side * 1.5, 7, P.chairs[who].z + (P.chairs[who].z > 0 ? -4 : 4), 110] });
    for (const [b, w] of [[C.kid, "kid"], [C.mom, "mom"], [C.dad, "dad"], [C.sister, "sister"], [C.grandma, "grandma"]]) seat(b, w);
    P.dadLoaf.visible = false;
    const h = head(a);
    const front = P.chairs[who].z > 0 ? -1 : 1;
    D.cam({ p: [[h[0] + side * 0.8, h[1] + 0.1, h[2] + front * 6.4], [h[0] + side * 0.7, h[1] + 0.05, h[2] + front * 5.8]], l: [h[0], h[1] - 0.2, h[2]], f: h, fov: 40, ap: 12, seed }, u, d);
  }
  shot(26.82, 28.18, (u, d) => {
    meetingCU(C.dad, "dad", u, d, 14);
    oath(C.dad, win(u, 0.05, 0.35, ease.outBack));
    C.dad.setFace("determined");
  });
  shot(28.18, 29.48, (u, d) => {
    meetingCU(C.mom, "mom", u, d, 15, -1);
    oath(C.mom, win(u, 0.05, 0.35, ease.outBack));
    C.mom.setFace("momSmile");
  });
  shot(29.48, 31.24, (u, d) => {
    meetingCU(C.sister, "sister", u, d, 16);
    const s = C.sister;
    const k = win(u, 0.05, 0.4, ease.outBack);
    s.j.armR.rotation.x = -1.2 - k * 0.5;
    s.j.armL.rotation.x = -1.2 - k * 0.6;
    s.j.armL.rotation.z = 0.55 * k;
    s.setFace(u > 0.8 ? "eyeroll" : "flat");
  });
  // F12 even Biscuit looked innocent (with a floret in his mouth: the clue)
  shot(31.24, 33.17, (u, d) => {
    D.lights("dining", 0, { fill: [DIN.x - 3.2, 3.2, 8.5, 200] });
    for (const [b, w] of [[C.kid, "kid"], [C.mom, "mom"], [C.dad, "dad"], [C.sister, "sister"]]) seat(b, w);
    const g = C.dog;
    D.place(g, DIN.x - 4.4, 0, DIN.z + 5.2, 0.35);
    D.dogSit(0);
    g.j.head.rotation.x = 0.1;
    g.j.head.rotation.z = 0.22 * win(u, 0.4, 0.9);
    g.j.tail.rotation.y = Math.sin(u * 10) * 0.5;
    g.j.head.add(P.floret);
    P.floret.visible = true;
    P.floret.scale.setScalar(0.42);
    P.floret.position.set(0.18, -0.05, 1.12);
    P.floret.rotation.set(PI / 2, 0, 0.5);
    const h = dogHead();
    D.cam({ p: [[h[0] + 0.9, h[1] + 0.35, h[2] + 5.0], [h[0] + 0.6, h[1] + 0.25, h[2] + 3.6]], l: h, f: h, fov: 32, ap: 16, seed: 17 }, u, d);
  });
  // F13 but somebody lied. So I opened the door.
  shot(33.17, 35.96, (u, d) => {
    const open = win(u, 1.35, 2.5, ease.inOut);
    door(48, open * 0.95);
    P.glow48.visible = true;
    D.lights("hall", 0, { night: true, camZ: END_Z + 8, fill: [0, 4.5, END_Z + 1.5, 40 + open * 240], fillColor: "#c8ff9a" });
    const k = C.kid;
    D.place(k, 0.6, 0, END_Z + 2.6, PI);
    k.j.armR.rotation.x = -1.35 * win(u, 0.3, 1.0);
    k.j.armR.rotation.z = -0.25;
    D.cam({ p: [[3.8, 6.8, END_Z + 11.5], [3.3, 6.4, END_Z + 10.2]], l: [0.2, 3.6, END_Z], fov: 42, ap: 6, seed: 18 }, u, d);
  });
  // in the broccoli hall: kid at the doorway, family behind him
  const BD = [BRC.x, 0, BRC.z + 54.5]; // kid's spot just inside the doorway
  function kidInDoor(face = "shock") {
    const k = C.kid;
    D.place(k, BD[0], 0, BD[2], PI);
    k.setFace(face);
    return k;
  }
  // F14 room 48 was huge
  shot(35.96, 37.61, (u, d) => {
    D.lights("broc");
    kidInDoor();
    C.kid.j.head.rotation.x = -0.4;
    D.cam({ p: [[BRC.x - 9, 30, BRC.z + 8], [BRC.x - 7, 25, BRC.z + 15]], l: [BRC.x, 3, BRC.z + 56], fov: 50, ap: 3, seed: 19 }, u, d);
  });
  // F15 and it was full of broccoli
  shot(37.61, 39.53, (u, d) => {
    D.lights("broc");
    kidInDoor();
    C.kid.j.head.rotation.x = -0.35;
    C.kid.j.armL.rotation.z = -0.4;
    C.kid.j.armR.rotation.z = 0.4;
    D.cam({ p: [[BRC.x + 1.4, 5.0, BRC.z + 59], [BRC.x + 1.2, 6.5, BRC.z + 58.4]], l: [[BRC.x - 1, 12, BRC.z - 10], [BRC.x - 1, 16, BRC.z - 20]], fov: 56, ap: 4, seed: 20 }, u, d);
  });
  // F16 mountains of it (crane up a peak; a little avalanche)
  shot(39.53, 40.81, (u, d) => {
    D.lights("broc");
    P.avalanche.forEach((b, i) => {
      const r0 = (i * 37) % 24 / 24;
      const f = clamp((u - r0 * 0.6) / 1.0);
      b.visible = true;
      const s = 1.2 + r0;
      b.scale.setScalar(s);
      b.position.set(BRC.x + 4 + (r0 - 0.5) * 8, Math.max(0.4, lerp(18, 1, f)), BRC.z - 10 + lerp(0, 14, f) + (i % 3));
      b.rotation.set(f * 8 + i, i, f * 5);
    });
    D.cam({ p: [[BRC.x + 12, 6, BRC.z + 16], [BRC.x + 10, 20, BRC.z + 12]], l: [[BRC.x + 8, 12, BRC.z - 18], [BRC.x + 12, 30, BRC.z - 28]], fov: 50, ap: 3, seed: 21 }, u, d);
  });
  // F17 everyone turned and looked at me
  shot(40.81, 42.97, (u, d) => {
    D.lights("broc", 0, { fill: [BRC.x, 6, BRC.z + 50, 90] });
    family([BRC.x, 0, BRC.z + 57.6], PI, { lookUp: 0.45 });
    const turn = win(u, 0.4, 0.75, ease.out3);
    [C.dad, C.mom, C.sister, C.grandma].forEach((a, i) => {
      a.j.head.rotation.x = lerp(-0.45, 0.12, turn);
      a.j.head.rotation.y = lerp([0.5, -0.4, 0.6, -0.5][i], 0, turn);
      a.setFace(turn > 0.5 ? (a === C.grandma || a === C.mom ? "momStern" : "stern") : "shock");
    });
    D.place(C.dog, BRC.x + 2.2, 0, BRC.z + 56.6, PI + 0.3);
    D.dogSit(0);
    D.cam({ p: [[BRC.x - 0.2, 4.9, BRC.z + 47.0], [BRC.x - 0.2, 4.8, BRC.z + 47.8]], l: [BRC.x, 3.9, BRC.z + 58], fov: 52, ap: 5, seed: 22, shake: 0.03 + bump(u, 0.4, 0.8) * 0.06 }, u, d);
  });
  // F18 flashback: at dinner Mom asked if I ate my broccoli. I said yes.
  shot(42.97, 46.75, (u, d) => {
    D.lights("dining", 0, { flashback: true, fill: [DIN.x - 2.6, 6.5, -2, 110] });
    for (const [a, w] of [[C.kid, "kid"], [C.mom, "mom"], [C.dad, "dad"], [C.sister, "sister"], [C.grandma, "grandma"]]) seat(a, w);
    P.dadLoaf.visible = false;
    P.plateBroc.forEach((b) => (b.visible = true));
    const m = C.mom, k = C.kid;
    m.setFace(u < 1.7 && Math.sin(u * 36) > 0 ? "momTalk" : "momSmile");
    m.j.head.rotation.y = 0.3;
    const nod = bump(u, 3.0, 3.35) + bump(u, 3.35, 3.7);
    k.j.head.rotation.x = nod * 0.25;
    k.setFace(u > 2.8 ? "grin" : "smile");
    k.j.head.rotation.y = -0.15;
    const kh = head(k);
    D.cam({ p: [[DIN.x - 1.2, 6.1, -7.4], [DIN.x - 1.3, 6.0, -6.8]], l: [kh[0], kh[1] - 0.9, kh[2]], f: kh, fov: 38, ap: 10, seed: 23 }, u, d);
  });
  // F19 I fed it to Biscuit (under the table)
  shot(46.75, 48.44, (u, d) => {
    D.lights("dining", 0, { flashback: true, fill: [DIN.x - 7, 2.5, 6, 130] });
    for (const [a, w] of [[C.kid, "kid"], [C.mom, "mom"]]) seat(a, w);
    const k = C.kid;
    k.j.armL.rotation.x = -0.2;
    k.j.armL.rotation.z = -0.45;
    const g = C.dog;
    D.place(g, DIN.x - 4.7, 0, DIN.z + 4.4, -0.6);
    D.dogSit(0);
    g.j.head.rotation.x = -0.25;
    const hand = D.wpos(k.j.handL);
    const mouth = D.wpos(g.j.head, [0, 0.0, 1.15]);
    const f = win(u, 0.2, 0.75, ease.inOut);
    if (u < 0.95) {
      P.floret.visible = true;
      P.floret.scale.setScalar(0.32);
      const p = lerp3(hand, mouth, f);
      P.floret.position.set(p[0], p[1], p[2]);
      P.floret.rotation.set(0.4, u, PI / 2);
    }
    g.j.head.rotation.x += bump(u, 0.75, 1.05) * 0.35 + bump(u, 1.05, 1.35) * 0.25;
    g.j.tail.rotation.y = Math.sin(u * 14) * 0.6;
    D.cam({ p: [[DIN.x - 11.5, 2.8, 8.6], [DIN.x - 11.0, 2.75, 8.3]], l: [DIN.x - 3.4, 2.6, 3.9], f: mouth, fov: 44, ap: 8, seed: 24 }, u, d);
  });
  // F20 "Did you feed your broccoli to the dog?"
  shot(48.44, 50.53, (u, d) => {
    D.lights("broc", 0, { fill: [BRC.x - 0.8, 6, BRC.z + 52, 100] });
    family([BRC.x, 0, BRC.z + 57.6], PI);
    const m = C.mom;
    armsCrossed(m);
    m.setFace(Math.sin(u * 34) > 0 && u < 1.75 ? "momSternTalk" : "momStern");
    for (const a of [C.dad, C.sister, C.grandma]) a.setFace(a === C.grandma ? "momStern" : "stern");
    const h = head(m);
    D.cam({ p: [[h[0] + 0.3, h[1] - 0.4, h[2] - 4.4], [h[0] + 0.25, h[1] - 0.35, h[2] - 3.8]], l: [h[0], h[1] - 0.7, h[2]], f: h, fov: 34, ap: 14, seed: 25 }, u, d);
  });
  // F21 "No," I said.
  shot(50.53, 51.91, (u, d) => {
    D.lights("broc", 0, { fill: [BRC.x, 6, BRC.z + 58, 100] });
    const k = kidInDoor("nervous");
    k.root.rotation.y = 0;
    k.setFace("nervous", { sweat: true });
    k.j.head.rotation.z = 0.1 * Math.sin(u * 6);
    const h = head(k);
    D.cam({ p: [[h[0] + 0.3, h[1] + 0.1, h[2] + 4.2], [h[0] + 0.25, h[1] + 0.05, h[2] + 3.6]], l: [h[0], h[1] - 0.6, h[2]], f: h, fov: 34, ap: 16, seed: 26 }, u, d);
  });
  // F22 the house rumbled
  shot(51.91, 53.6, (u, d) => {
    const fl = Math.sin(u * 40) > 0.5 ? 0.55 : 1;
    door(48, 0.95);
    P.glow48.visible = true;
    D.lights("hall", 0, { night: true, camZ: END_Z + 10, flicker: fl, fill: [0, 5, END_Z + 2, 160], fillColor: "#c8ff9a" });
    family([0.2, 0, END_Z + 7.2], 0);
    for (const [a, i] of [[C.dad, 0], [C.mom, 1], [C.sister, 2], [C.grandma, 3]]) {
      a.j.head.rotation.y = Math.sin(u * 5 + i * 2) * 0.6;
      a.j.head.rotation.x = -0.3;
      a.setFace("shock");
      a.root.position.x += Math.sin(u * 30 + i) * 0.05;
    }
    const k = C.kid;
    D.place(k, 1.6, 0, END_Z + 3.8, 0.3);
    k.setFace("scared", { sweat: true });
    ceilingDust(END_Z + 8, u);
    D.cam({ p: [[-0.4, 6.0, END_Z + 16.5], [-0.3, 5.9, END_Z + 15.6]], l: [0.6, 3.6, END_Z + 4], fov: 46, ap: 5, shake: 0.18, seed: 27 }, u, d);
  });
  // F23 Room 49. (slams out of the wall right next to the kid)
  shot(53.6, 54.95, (u, d, t) => {
    D.lights("hall", 0, { night: true, camZ: END_Z + 8, fill: [-1, 5, END_Z + 7, 170] });
    door(48, 0.95);
    P.glow48.visible = true;
    const pop = win(u, 0.0, 0.28, ease.outBack);
    P.doors[49].root.position.x = lerp(4.9, 4.02, pop);
    P.doors[49].root.scale.setScalar(lerp(0.6, 1, pop));
    puff([3.6, 3.0, END_Z + 2.9], u - 0.05, 3, 500);
    const k = C.kid;
    D.place(k, 1.4, 0, END_Z + 4.2, 0);
    D.faceTo(k, 3.5, END_Z + 2.9);
    k.root.rotation.y += -0.9 * win(u, 0.1, 0.35);
    k.root.position.y = bump(u, 0.08, 0.4) * 0.6;
    k.setFace(u > 0.1 ? "shock" : "nervous", { sweat: true });
    D.cam({ p: [[-1.6, 5.0, END_Z + 11.5], [-1.5, 4.9, END_Z + 10.8]], l: [2.0, 4.0, END_Z + 3.4], fov: 44, ap: 6, shake: 0.03 + bump(u, 0.0, 0.35) * 0.2, seed: 28 }, u, d);
  });
  // F24 end card: another room pops onto the roof
  shot(54.95, 58.3, (u, d) => {
    D.lights("ext");
    const pr = P.popRooms[1];
    pr.grp.scale.setScalar(Math.max(0.0001, win(u, 0.25, 0.75, ease.outBack)));
    puff([EXT.x + pr.x, pr.y - 1.8, pr.z + 1], u - 0.25, 4, 400);
    pipe.grade.uniforms.uFade.value = 0.42 * win(u, 0.5, 0.9);
    D.cam({ p: [[EXT.x - 2, 7, 60], [EXT.x - 2, 7.5, 57]], l: [EXT.x, 15, 0], fov: 52, ap: 2, seed: 29, shake: 0.03 + bump(u, 0.25, 0.6) * 0.12 }, u, d);
  });

  // COVER (thumbnail still; past the end of the film)
  shot(200, 210, (u, d) => {
    D.lights("broc", 0, { fill: [BRC.x + 0.5, 6, BRC.z + 59.5, 230] });
    const k = C.kid;
    D.place(k, BRC.x, 0, BRC.z + 54.5, 0);
    k.setFace("nervous", { sweat: true });
    k.j.armL.rotation.x = k.j.armR.rotation.x = -0.5;
    k.j.armL.rotation.z = -0.7;
    k.j.armR.rotation.z = 0.7;
    const h = head(k);
    D.cam({ p: [BRC.x + 0.6, 3.6, BRC.z + 61], l: [BRC.x, 9.5, BRC.z + 40], f: h, fov: 58, ap: 4, shake: 0, seed: 99 }, 0, 1);
  });

  return S;
}
