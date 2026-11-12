// Humans Can Lick Too, shot by shot. Times are seconds on audio/vo.wav; word cues from src/captions-data.js.
import * as THREE from "three";
import { makeDirector } from "./direct.js";
import { BED, HX } from "./world.js";
import { ease, win, lerp, lerp3, clamp } from "./util.js";

const PI = Math.PI;
const bump = (u, a, b) => (u <= a || u >= b ? 0 : Math.sin(((u - a) / (b - a)) * PI));
const KX = BED.x + 0.6, KZ = -7.3; // kid sitting up in bed
const LX = -4.3, LZ = -3.25; // kid lying: feet end
const ARM = [-2.45, 3.4, -6.75]; // shoulder pivot of the hanging arm, at the mattress edge
const FACE_AT = [KX, 6.25, KZ + 0.7];

export function buildShots(ctx) {
  const D = makeDirector(ctx);
  const { C, W, pipe } = ctx;
  const P = W.props;
  const S = [];
  const shot = (t0, t1, run) => S.push({ t0, t1, run });
  const kid = C.kid, dog = C.dog;

  // ---- kid -----------------------------------------------------------------------
  function kidSit({ face = "smile", faceOpts, look = 0, lookUp = 0 } = {}) {
    D.place(kid, KX, 0, KZ, 0);
    D.sit(kid, 3.2);
    kid.j.torso.rotation.x = -0.06;
    kid.setFace(face, faceOpts);
    kid.j.armR.rotation.set(-0.5, 0, -0.1);
    kid.j.armL.rotation.set(-0.5, 0, 0.1);
    kid.j.head.rotation.set(0.05 - lookUp, look, 0);
    P.blanket.position.set(BED.x + 0.3, 4.45, -4.44);
    P.blanket.scale.set(1, 1.1, 0.8);
    return kid;
  }
  function lie({ face = "sleep", faceOpts, armOut = false } = {}) {
    D.place(kid, LX, 3.85, LZ, 0);
    kid.root.rotation.x = -PI / 2;
    kid.j.armL.rotation.z = -0.08;
    kid.j.armR.rotation.z = 0.08;
    kid.j.armR.visible = !armOut;
    kid.setFace(face, faceOpts);
    P.blanket.position.set(BED.x + 0.3, 4.45, -4.1);
    return kid;
  }
  const kHead = () => D.wpos(kid.j.head, [0, 0.62, 0]);
  // the hanging arm prop: k 0 = resting along the bed, 1 = hanging into the dark
  function arm(k, sway = 0) {
    P.arm.visible = true;
    P.arm.position.set(ARM[0], ARM[1], ARM[2]);
    P.arm.rotation.set(lerp(-1.35, 0.06, k), 0, lerp(0.05, 0.12, k) + sway);
    return D.wpos(P.arm, [0, -2.1, 0]);
  }
  // the tongue from under the bed: reach 0..1, lick phase 0..1 (curls up the palm)
  function tongue(hand, reach, lick = 0) {
    const tg = P.tongue;
    tg.group.visible = reach > 0.01;
    const base = [-3.7, 0.55, hand[2]];
    tg.group.position.set(base[0], base[1], base[2]);
    const dx = hand[0] - 0.15 - base[0], dy = hand[1] - 0.55 - base[1];
    const len = Math.hypot(dx, dy) * reach;
    tg.group.rotation.set(0, 0, Math.atan2(dy, dx) + Math.sin(lick * PI) * 0.55);
    tg.group.scale.set(Math.max(0.05, len), 1, 1);
    tg.tip.scale.set(1 / Math.max(0.05, len), 0.32, 1);
  }
  const lickAt = (t, times) => {
    for (const lt of times) if (t >= lt - 0.45 && t <= lt + 0.5) return { reach: bump(t, lt - 0.45, lt + 0.5) ** 0.6, lick: clamp((t - (lt - 0.15)) / 0.35) };
    return { reach: 0, lick: 0 };
  };
  // ---- the dog ------------------------------------------------------------------------
  function dogStand(x, z, ry, t, wag = 1) {
    D.place(dog, x, 0, z, ry);
    dog.j.tail.rotation.y = Math.sin(t * 12) * 0.6 * wag;
    return dog;
  }
  function dogLie(x, z, ry, t) {
    D.place(dog, x, 0, z, ry);
    dog.j.body.position.y = 0.42;
    dog.j.legs[0].rotation.x = dog.j.legs[1].rotation.x = -1.45;
    dog.j.legs[2].rotation.x = dog.j.legs[3].rotation.x = 1.45;
    dog.j.head.rotation.x = 0.12;
    dog.j.tail.rotation.set(0.1, Math.sin(t * 6) * 0.4, 0);
    return dog;
  }
  // ---- water drops ------------------------------------------------------------------
  function drips(t, times, from, toY, slot = 0) {
    let k = slot;
    for (const ti of times) {
      if (t < ti - 0.55 || t > ti + 0.02) continue;
      const d = P.drops[k++ % P.drops.length];
      d.visible = true;
      if (t < ti - 0.22) {
        const g = clamp((t - (ti - 0.55)) / 0.33);
        d.position.set(from[0], from[1] - 0.02 - g * 0.05, from[2]);
        d.scale.set(0.5 + g * 0.5, (0.5 + g * 0.5) * 1.3, 0.5 + g * 0.5);
      } else {
        const f = clamp((t - (ti - 0.22)) / 0.22);
        d.position.set(from[0], lerp(from[1] - 0.07, toY, f * f), from[2]);
        d.scale.set(0.9, 1.7, 0.9);
      }
    }
  }
  const DRIP_NIGHT = [18.62, 19.05, 19.7, 19.95, 20.6];
  const insertPhone = (state) => {
    kidSit();
    kid.root.visible = false;
    const ph = P.phone;
    ph.grip.visible = true;
    ph.group.visible = true;
    const INS = [KX + 0.55, 5.25, KZ + 1.45];
    ph.group.position.set(INS[0], INS[1], INS[2]);
    ph.group.lookAt(INS[0] - 0.1, INS[1] + 0.55, INS[2] - 3.0);
    P.blanket.material.color.setScalar(0.28);
    ph.draw(state);
    return INS;
  };

  // ==========================================================================
  // S01 hook: a hand hanging off the bed in the dark; something under the bed licks it
  shot(0, 4.7, (u, d, t) => {
    lie({ face: "sleep", armOut: true });
    const h = arm(1, Math.sin(t * 0.8) * 0.02);
    const lk = lickAt(t, [0.55, 1.7]);
    tongue(h, lk.reach, lk.lick);
    D.lights("night", 0, { dark: true, clockGlow: 0.15, fill: [h[0] + 2, h[1] + 1.5, h[2] + 2, 22], fillColor: "#8a9ee0" });
    const push = win(t, 2.8, 4.6);
    D.cam({ p: lerp3([2.2, 1.05, -1.4], [-0.4, 0.85, -4.4], push), l: lerp3([h[0] - 0.9, h[1] - 0.15, h[2] - 0.1], [-3.8, 0.8, h[2] - 0.2], push), f: lerp3(h, [-3.6, 0.8, h[2]], push), fov: 42, ap: 5, seed: 1 }, u, d);
  });
  // S02 My parents were gone for the night. It was just me and Max.
  shot(4.7, 8.24, (u, d, t) => {
    kidSit({ face: t > 7.3 ? "grin" : "smile", look: 0.35 });
    const dg = dogStand(-1.4, -5.6, -PI / 2 - 0.3, t);
    dg.j.head.rotation.x = -0.15;
    P.clock.set("8:47");
    D.lights("night", 0, { lamp: 1 });
    D.cam({ p: [[4.6, 6.4, 3.6], [3.8, 6.1, 2.6]], l: [-3.2, 3.6, -6.6], f: [-3.4, 4.5, -6.6], fov: 44, ap: 3, seed: 2 }, u, d);
  });
  // S03 Max always sleeps under my bed
  shot(8.24, 10.46, (u, d, t) => {
    kidSit({ face: "smile", look: 0.3 });
    const k = win(t, 8.3, 9.9, ease.inOut);
    const x = lerp(-1.2, -4.6, k);
    D.place(dog, x, 0, -5.4, -PI / 2);
    dog.j.body.position.y = lerp(1.35, 0.42, win(t, 8.9, 9.7));
    const walk = t * 9;
    dog.j.legs.forEach((l, i) => (l.rotation.x = Math.sin(walk + (i < 2 ? 0 : PI) + (i % 2) * 0.6) * 0.5 * (1 - k * 0.6)));
    dog.j.tail.rotation.set(0.5, Math.sin(t * 13) * 0.7, 0);
    P.clock.set("8:47");
    D.lights("night", 0, { lamp: 1 });
    D.cam({ p: [[1.4, 1.4, -2.6], [1.0, 1.25, -3.0]], l: [[-2.8, 1.0, -5.4], [-3.6, 0.8, -5.4]], f: [x + 0.8, 1.2, -5.4], fov: 40, ap: 5, seed: 3 }, u, d);
  });
  // S04 At midnight, my phone buzzed. A man had escaped from the prison nearby.
  shot(10.46, 15.13, (u, d, t) => {
    const buzz = t > 11.25 && t < 11.7 ? 1 : 0;
    const pp = insertPhone({ screen: "lock", time: "12:00", notif: win(t, 11.3, 11.6, ease.outBack), app: "NEWS", appLetter: "N", appColor: "#d93a3a",
      title: "Prison escape nearby", msg: "Suspect last seen 2 miles from", msg2: "Oak Hollow. Lock your doors." });
    if (buzz) P.phone.group.position.x += Math.sin(t * 90) * 0.025;
    P.clock.set("12:00");
    D.lights("night", 0, { dark: true, phone: [pp[0] - 0.1, pp[1] + 0.4, pp[2] - 0.7, 2.2, 3] });
    pipe.grade.uniforms.uVignette.value = 0.72;
    D.phoneCam(P.phone, { dist: [2.6, 2.38], fov: 46, ly: -0.36, ap: 10, seed: 4, shake: buzz ? 0.03 : 0.006 }, u, d);
  });
  // S05a I locked every door (the deadbolt turns)
  shot(15.13, 16.45, (u, d, t) => {
    P.deadbolt.rotation.z = lerp(0, PI / 2, win(t, 15.45, 15.62, ease.out));
    D.lights("night", 0, { dark: true, fill: [4.8, 5.4, 7.6, 14], fillColor: "#8aa0e0" });
    D.cam({ p: [[4.6, 4.9, 7.4], [4.85, 4.8, 7.75]], l: [5.9, 4.1, 9.7], f: [5.75, 4.4, 9.7], fov: 36, ap: 8, seed: 5 }, u, d);
  });
  // S05b …I turned off every light
  shot(16.45, 18.31, (u, d, t) => {
    const on = t < 17.5 ? 1 : 0;
    kidSit({ face: on ? "flat" : "worried", look: 0.45 });
    kid.j.armR.rotation.set(-1.2 * on - 0.3 * (1 - on), 0, -0.55 * on);
    P.clock.set("12:03");
    D.lights("night", 0, { lamp: on, dark: !on });
    D.cam({ p: [[3.4, 6.6, 1.6], [3.0, 6.4, 1.1]], l: [-3.0, 3.8, -7.4], f: [-3.4, 4.8, -7.2], fov: 44, ap: 3, seed: 6 }, u, d);
  });
  // S06 Then I heard it. Drip. Drip. Drip. (the bathroom faucet in the dark)
  shot(18.31, 21.04, (u, d, t) => {
    drips(t, DRIP_NIGHT, P.spout, P.basinY);
    D.lights("bath", 0, { fill: [HX - 3.8, 5.2, -3.0, 10], fillColor: "#8ea6e8" });
    D.cam({ p: [[HX - 3.6, 4.1, -2.9], [HX - 3.95, 4.0, -3.4]], l: [HX - 5.2, 3.45, -5.05], f: [HX - 5.2, 3.5, -5.1], fov: 34, ap: 9, seed: 7 }, u, d);
  });
  // S07a I was too scared to get up (eyes open in the dark, from above)
  shot(21.04, 22.4, (u, d, t) => {
    lie({ face: "scared", faceOpts: { sweat: true } });
    P.clock.set("12:03");
    const h = kHead();
    D.lights("night", 0, { dark: true, fill: [h[0] + 0.5, h[1] + 4, h[2] + 1.5, 26], fillColor: "#8fa6e6" });
    D.cam({ p: [[h[0] + 0.25, h[1] + 4.2, h[2] + 0.6], [h[0] + 0.2, h[1] + 3.7, h[2] + 0.5]], l: [h[0], h[1], h[2] + 0.3], up: [0, 0, -1], fov: 40, ap: 8, seed: 8 }, u, d);
  });
  // S07b …so I reached my hand under the bed
  shot(22.4, 24.9, (u, d, t) => {
    lie({ face: "scared", armOut: true });
    const h = arm(win(t, 22.5, 24.3, ease.inOut));
    D.lights("night", 0, { dark: true, fill: [h[0] + 2.2, 3.2, h[2] + 2.6, 16], fillColor: "#7f95d6" });
    D.cam({ p: [[1.6, 2.9, -3.4], [1.2, 2.5, -3.8]], l: [[-2.6, 2.6, -6.6], [-2.9, 1.4, -6.7]], f: h, fov: 42, ap: 5, seed: 9 }, u, d);
  });
  // S08a And Max licked it.
  shot(24.9, 26.0, (u, d, t) => {
    lie({ face: "scared", armOut: true });
    const h = arm(1);
    const lk = lickAt(t, [25.3, 25.85]);
    tongue(h, lk.reach, lk.lick);
    D.lights("night", 0, { dark: true, clockGlow: 0.15, fill: [h[0] + 1.8, h[1] + 1.2, h[2] + 1.8, 20], fillColor: "#8a9ee0" });
    D.cam({ p: [[1.9, 1.0, -1.8], [1.5, 0.95, -2.3]], l: [h[0] - 0.9, h[1] - 0.25, h[2] - 0.1], f: h, fov: 40, ap: 5, seed: 10 }, u, d);
  });
  // S08b …Like he always does. (relief)
  shot(26.0, 27.86, (u, d, t) => {
    lie({ face: t < 27.0 ? "relief" : "sleep", armOut: true });
    arm(1);
    const h = kHead();
    D.lights("night", 0, { dark: true, fill: [h[0] + 0.5, h[1] + 4, h[2] + 1.5, 24], fillColor: "#8fa6e6" });
    D.cam({ p: [[h[0] + 0.2, h[1] + 4.0, h[2] + 0.5], [h[0] + 0.15, h[1] + 3.5, h[2] + 0.4]], l: [h[0], h[1], h[2] + 0.3], up: [0, 0, -1], fov: 40, ap: 8, seed: 11 }, u, d);
  });
  // S09 Every time the dripping woke me up… (montage: the clock, the hand, the clock, the hand)
  const clockCam = (u, d, seed) => {
    D.lights("night", 0, { dark: true, fill: [-2.0, 3.6, -7.0, 8], fillColor: "#8090c8" });
    D.cam({ p: [[-3.6, 3.7, -5.6], [-3.35, 3.65, -5.95]], l: [-1.3, 2.6, -8.35], f: [-1.3, 3.22, -8.35], fov: 34, ap: 12, seed }, u, d);
  };
  const handCam = (u, d, t, times, seed, side = 1) => {
    lie({ face: "sleep", armOut: true });
    const h = arm(1, Math.sin(t) * 0.02);
    const lk = lickAt(t, times);
    tongue(h, lk.reach, lk.lick);
    drips(t, [], P.spout, P.basinY);
    D.lights("night", 0, { dark: true, clockGlow: 0.15, fill: [h[0] + 1.8, h[1] + 1.2, h[2] + 1.8 * side, 20], fillColor: "#8a9ee0" });
    D.cam({ p: [[1.8 + side * 0.6, 1.0, h[2] + 5.0 * side], [1.4 + side * 0.6, 0.95, h[2] + 4.5 * side]], l: [h[0] - 0.9, h[1] - 0.25, h[2]], f: h, fov: 40, ap: 5, seed }, u, d);
  };
  shot(27.86, 29.0, (u, d) => {
    P.clock.set("1:12");
    clockCam(u, d, 12);
  });
  shot(29.0, 30.0, (u, d, t) => handCam(u, d, t, [29.45], 13, 1));
  shot(30.0, 30.9, (u, d) => {
    P.clock.set("2:47");
    clockCam(u, d, 14);
  });
  shot(30.9, 31.6, (u, d) => {
    P.clock.set("4:05");
    clockCam(u, d, 15);
  });
  shot(31.6, 32.45, (u, d, t) => handCam(u, d, t, [31.95], 16, 0.5));
  // S10a In the morning…
  shot(32.45, 34.1, (u, d, t) => {
    kidSit({ face: "flat", look: 0.25 });
    P.clock.set("7:30");
    D.lights("dawn", 1);
    W.dust.visible = true;
    D.cam({ p: [[-1.2, 6.8, 5.6], [-1.0, 6.6, 4.6]], l: [0.6, 4.6, -8.0], f: [-4.4, 5.8, -7.2], fov: 48, ap: 2, seed: 17 }, u, d);
  });
  // S10b …the dripping was coming from the bathroom
  shot(34.1, 35.7, (u, d, t) => {
    drips(t, [34.6, 35.35], P.spout, P.basinY);
    dogStand(HX + 5.6, -4.0, 0.15, t, 0).root.position.y = 0.3;
    D.dogSit(1);
    dog.wet(1);
    D.lights("bath", 1);
    D.cam({ p: [[HX + 2.2, 5.6, 8.2], [HX + 2.4, 5.4, 6.6]], l: [HX + 2.8, 3.1, -3.0], f: [HX + 3.4, 3.4, -2.0], fov: 52, ap: 2.0, seed: 18 }, u, d);
  });
  // S11 Max was locked in the shower. Shaking.
  shot(35.7, 38.54, (u, d, t) => {
    const g = dogStand(HX + 5.6, -4.0, 0.1, t, 0);
    g.root.position.y = 0.3;
    D.dogSit(1);
    dog.wet(1);
    g.j.body.rotation.z = Math.sin(t * 46) * 0.05 * (t > 37.4 ? 1.4 : 0.7);
    g.j.head.rotation.y = Math.sin(t * 31) * 0.05;
    drips(t, [36.3, 37.1, 37.9], P.showerHead, 0.35);
    D.lights("bath", 0.85);
    D.cam({ p: [[HX + 6.8, 4.6, 3.0], [HX + 6.3, 4.1, 2.1]], l: [HX + 5.3, 1.9, -4.0], f: [HX + 5.6, 2.4, -3.6], fov: 42, ap: 4, seed: 19 }, u, d);
  });
  // S12 He'd been in there all night.
  shot(38.54, 40.6, (u, d, t) => {
    D.place(kid, HX + 1.0, 0, 1.4, 2.5);
    kid.setFace("shock");
    kid.j.armL.rotation.set(-0.4, 0, 0.2);
    kid.j.armR.rotation.set(-0.4, 0, -0.2);
    const g = dogStand(HX + 5.6, -4.0, 0.1, t, 0);
    g.root.position.y = 0.3;
    D.dogSit(1);
    dog.wet(1);
    g.j.body.rotation.z = Math.sin(t * 46) * 0.05;
    D.lights("bath", 1);
    const h = kHead();
    D.cam({ p: [[h[0] + 2.2, h[1] + 0.2, h[2] - 2.6], [h[0] + 1.8, h[1] + 0.1, h[2] - 2.2]], l: [h[0], h[1] - 0.75, h[2]], f: h, fov: 38, ap: 6, seed: 20 }, u, d);
  });
  // S13 And written on the foggy mirror… (over the shoulder, the writing comes into view)
  shot(40.6, 42.91, (u, d, t) => {
    P.mirror.mat.map = P.mirror.text;
    D.place(kid, HX - 4.2, 0, -1.4, PI - 0.15 + win(t, 40.6, 41.4) * 0.05);
    kid.setFace("shock");
    kid.j.head.rotation.x = -0.15;
    D.lights("bath", 1);
    D.cam({ p: [[HX - 2.6, 6.6, 2.6], [HX - 3.4, 6.5, 1.6]], l: [[HX - 3.6, 5.6, -3.0], [HX - 5.2, 6.2, -5.9]], f: [HX - 5.2, 6.4, -5.9], fov: 40, ap: 4, seed: 21 }, u, d);
  });
  // S14 Humans can lick too.
  shot(42.91, 45.34, (u, d, t) => {
    P.mirror.mat.map = P.mirror.text;
    D.lights("bath", 1, { fill: [HX - 5.2, 6.6, -2.0, 14], fillColor: "#fff0dc" });
    pipe.grade.uniforms.uVignette.value = 0.6;
    D.cam({ p: [[HX - 5.2, 5.8, 0.0], [HX - 5.2, 5.8, -0.7]], l: [HX - 5.2, 5.0, -5.9], f: [HX - 5.2, 6.4, -5.9], fov: 58, ap: 5, seed: 22, shake: 0.012 }, u, d);
  });
  // S15 So whatever was under my bed… (floor level, creeping toward the dark)
  shot(45.34, 47.48, (u, d, t) => {
    P.clock.set("7:30");
    D.lights("dawn", 0.55, { dark: true });
    D.cam({ p: [[1.6, 0.95, -5.0], [-0.9, 0.9, -5.6]], l: [-4.6, 0.85, -6.1], f: [-4.4, 0.9, -6.0], fov: 38, ap: 5, seed: 23 }, u, d);
  });
  // S16 …is still under my bed. (eyes open in the dark, a pale hand slides out)
  shot(47.48, 49.4, (u, d, t) => {
    P.clock.set("7:30");
    const U = P.under;
    U.face.visible = true;
    U.face.position.set(-4.3, 0.95, -6.05);
    U.faceM.color.setScalar(0.85 * win(t, 47.75, 48.0));
    U.hand.visible = true;
    U.hand.position.set(lerp(-4.2, -2.3, win(t, 48.35, 49.05, ease.out)), 0.16, -5.25);
    D.lights("dawn", 0.55, { dark: true });
    D.cam({ p: [[-0.9, 0.9, -5.6], [-1.5, 0.88, -5.8]], l: [-4.2, 0.85, -5.9], f: [-4.3, 0.95, -6.0], fov: 38, ap: 6, seed: 24, shake: 0.02 }, u, d);
    pipe.grade.uniforms.uFade.value = win(t, 49.2, 49.4);
  });
  // END CARD: the bed in morning light, the dark gap underneath
  shot(49.4, 52.5, (u, d, t) => {
    P.clock.set("7:30");
    D.lights("dawn", 0.7);
    P.blanket.position.set(BED.x + 0.3, 3.55, -4.6);
    D.cam({ p: [[2.4, 3.6, -1.0], [2.1, 3.5, -1.3]], l: [-4.0, 1.6, -6.2], f: [-3.4, 1.4, -6.0], fov: 46, ap: 3, seed: 25 }, u, d);
    pipe.grade.uniforms.uFade.value = lerp(1, 0.38, win(u, 0, 0.12));
  });

  // COVER (thumbnail still): the hand off the bed, the tongue reaching, the eyes in the dark behind it
  shot(200, 210, (u, d, t) => {
    lie({ face: "sleep", armOut: true });
    const h = arm(1);
    tongue(h, 0.95, 0.6);
    const U = P.under;
    U.face.visible = true;
    U.face.position.set(-3.6, 1.15, h[2] + 0.6);
    U.face.rotation.y = Math.atan2(2.0 - -3.6, h[2] + 4.6 - (h[2] + 0.6));
    U.face.scale.setScalar(1.15);
    U.faceM.color.setScalar(1.0);
    D.lights("night", 0, { clockGlow: 0.15, fill: [h[0] + 1.6, h[1] + 1.4, h[2] + 1.6, 26], fillColor: "#8aa0e0" });
    D.cam({ p: [2.0, 1.1, h[2] + 4.6], l: [-2.9, 1.6, h[2] - 0.3], f: [h[0] - 0.6, h[1] - 0.2, h[2]], fov: 44, ap: 1.2, shake: 0, seed: 99 }, 0, 1);
  });

  return S;
}
