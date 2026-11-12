// Bloody Mary, shot by shot. Times are seconds on audio/vo.wav (line timings in audio/vo-lines.json).
import * as THREE from "three";
import { makeDirector } from "./direct.js";
import { HX, ZM, MX } from "./world.js";
import { ease, win, lerp, lerp3, clamp } from "./util.js";

const PI = Math.PI;
const bump = (u, a, b) => (u <= a || u >= b ? 0 : Math.sin(((u - a) / (b - a)) * PI));
const KZ = -2.6; // where the kid stands at the sink
const RZ = 2 * ZM - KZ; // where his reflection appears (world)
const MY = 5.4; // mirror centre height

export function buildShots(ctx) {
  const D = makeDirector(ctx);
  const { C, W, pipe } = ctx;
  const P = W.props;
  const S = [];
  const shot = (t0, t1, run) => S.push({ t0, t1, run });
  const kid = C.kid, twin = C.twin, fa = C.friendA, fb = C.friendB;

  // ---- posing ---------------------------------------------------------------------
  const talkFace = (t, a, b, open = "shock", shut = "worried") => (t > a && t < b && Math.sin(t * 17) > -0.1 ? open : shut);
  function kidAt(x, z, ry, face = "worried", faceOpts) {
    D.place(kid, x, 0, z, ry);
    kid.setFace(face, faceOpts);
    kid.j.armL.rotation.set(0, 0, -0.05);
    kid.j.armR.rotation.set(0, 0, 0.05);
    return kid;
  }
  // the reflection: same pose in the mirror world unless told otherwise
  function mirror({ face, faceOpts, copy = true } = {}) {
    D.place(twin, kid.root.position.x - HX, 0, kid.root.position.z, kid.root.rotation.y);
    if (copy) {
      for (const k of ["torso", "head", "armL", "armR", "legL", "legR"]) twin.j[k].rotation.copy(kid.j[k].rotation);
      twin.j.pelvis.position.copy(kid.j.pelvis.position);
    }
    twin.setFace(face || kid.faceName, faceOpts);
    return twin;
  }
  const kHead = () => D.wpos(kid.j.head, [0, 0.62, 0]);
  const rHead = () => D.wpos(twin.j.head, [0, 0.62, 0]);
  const door = (k) => (P.bathDoor.rotation.y = P.reflectDoor.rotation.y = lerp(0, -1.5, k));
  const dark = (t, o = {}) => D.lights("mary", 0, { candle: 1, t, ...o });
  function friends(t, { giggle = 0, look = 0, faceA = "grin", faceB = "grin", z = 11.2, dx = 1.6, turn = 0 } = {}) {
    D.place(fa, MX - dx, 0, z, PI + 0.25 + turn);
    D.place(fb, MX + dx + 0.1, 0, z + 0.6, PI - 0.3 - turn);
    fa.setFace(faceA);
    fb.setFace(faceB);
    for (const [f, ph] of [[fa, 0], [fb, 1.3]]) {
      const sh = Math.sin(t * 19 + ph) * 0.05 * giggle;
      f.j.torso.rotation.x = 0.08 * giggle + sh;
      f.j.armR.rotation.set(-2.3 * giggle, 0, -0.55 * giggle);
      f.j.head.rotation.y = look * (f === fa ? 0.3 : -0.3);
    }
  }
  // over the kid's shoulder into the mirror
  function overShoulder(u, d, { push = [0, 0.8], focus = null, fov = 34, seed = 1, side = 1 } = {}) {
    const k = lerp(push[0], push[1], ease.inOut(clamp(u / d)));
    const rh = rHead();
    D.cam({ p: [MX + 1.9 * side - 0.3 * k * side, 6.0 - 0.15 * k, KZ + 3.4 - 1.4 * k], l: [MX + 0.25 * side, MY - 0.15, ZM], f: focus || rh, fov, ap: 6, seed }, 0, 1);
  }

  // ==========================================================================
  // S01 hook: candlelight, the mirror, his reflection
  shot(0, 3.03, (u, d, t) => {
    door(0);
    kidAt(MX, KZ, PI, "flat");
    mirror({ face: t > 2.2 ? "smile" : "flat" });
    dark(t);
    overShoulder(u, d, { push: [0, 1], seed: 1 });
  });
  // S02 At my sleepover, my friends dared me to do Bloody Mary.
  shot(3.03, 6.72, (u, d, t) => {
    door(1);
    kidAt(MX, 12.2, PI, "nervous");
    kid.j.head.rotation.y = Math.sin(t * 1.4) * 0.15;
    friends(t, { giggle: bump(t, 4.6, 6.7), faceA: "grin", faceB: "grin", z: 13.2 });
    fa.j.armR.rotation.set(-1.55, 0, 0.25);
    D.lights("mary", 0, { hall: 1, t, fill: [MX + 0.5, 6.4, 8.6, 34], fillColor: "#ffd9a8" });
    D.cam({ p: [[MX + 1.0, 6.4, 7.0], [MX + 0.8, 6.2, 7.5]], l: [MX + 0.1, 4.0, 13.0], f: [MX, 4.6, 12.4], fov: 54, ap: 3, seed: 2 }, u, d);
  });
  // S03a Lights off.
  shot(6.72, 7.6, (u, d, t) => {
    door(0);
    const on = t < 7.12 ? 1 : 0;
    P.switchM.map = on ? P.switchOn : P.switchOff;
    D.lights("mary", 0, { room: on, candle: 0, t });
    D.cam({ p: [[HX - 2.45, 4.8, 5.4], [HX - 2.55, 4.75, 5.7]], l: [HX - 2.7, 4.55, 7.0], f: [HX - 2.7, 4.6, 6.98], fov: 36, ap: 9, seed: 3 }, u, d);
  });
  // S03b One candle. Just me and the mirror.
  shot(7.6, 10.0, (u, d, t) => {
    door(0);
    P.switchM.map = P.switchOff;
    kidAt(MX, KZ, PI, "worried");
    mirror();
    D.lights("mary", 0, { candle: win(t, 7.8, 8.15), t });
    D.cam({ p: [[HX + 1.2, 6.4, 4.8], [HX + 0.6, 6.2, 4.0]], l: [MX + 0.3, 4.2, -3.8], f: [MX, 4.8, KZ], fov: 48, ap: 3, seed: 4 }, u, d);
  });
  // S04 The rule is simple… she appears behind you (focus slides to the dark behind him in the glass)
  shot(10.0, 14.82, (u, d, t) => {
    door(0);
    kidAt(MX, KZ, PI, "worried");
    mirror();
    dark(t);
    const rh = rHead();
    overShoulder(u, d, { push: [0.1, 0.9], focus: lerp3(rh, [MX + 0.6, 4.6, 2 * ZM - 6.8], win(t, 13.2, 14.2)), seed: 5 });
  });
  // S05 "Bloody Mary." (his face in the candlelight)
  shot(14.82, 16.62, (u, d, t) => {
    door(0);
    kidAt(MX, KZ, PI, talkFace(t, 14.85, 15.7, "shock", "worried"));
    mirror();
    dark(t);
    const h = kHead();
    D.cam({ p: [[MX + 1.8, h[1] + 0.45, -5.5], [MX + 1.6, h[1] + 0.4, -5.35]], l: [h[0], h[1] - 0.4, h[2]], f: h, fov: 40, ap: 8, seed: 6 }, u, d);
  });
  // S06 "Bloody Mary." (the reflection says it with him)
  shot(16.62, 18.43, (u, d, t) => {
    door(0);
    kidAt(MX, KZ, PI, talkFace(t, 16.65, 17.6, "shock", "worried"));
    mirror();
    dark(t);
    overShoulder(u, d, { push: [0.9, 1.25], fov: 30, seed: 7 });
  });
  // S07 I stopped. I was not saying it a third time.
  shot(18.43, 21.54, (u, d, t) => {
    door(0);
    kidAt(MX, KZ + win(t, 18.5, 19.2) * 0.4, PI, "scared", { sweat: true });
    kid.j.head.rotation.y = Math.sin(t * 6) * 0.22 * bump(t, 18.9, 20.8);
    mirror();
    dark(t);
    const h = kHead();
    D.cam({ p: [[MX - 1.6, h[1] + 0.45, -5.5], [MX - 1.45, h[1] + 0.4, -5.35]], l: [h[0], h[1] - 0.4, h[2]], f: h, fov: 42, ap: 8, seed: 8 }, u, d);
  });
  // S08 My friends were giggling outside the door.
  shot(21.54, 24.23, (u, d, t) => {
    door(0);
    friends(t, { giggle: 1, z: 9.4, dx: 1.1, turn: 0.85 });
    D.lights("mary", 0, { hall: 1, t });
    D.cam({ p: [[MX + 2.4, 6.2, 16.4], [MX + 2.1, 6.0, 15.8]], l: [MX + 0.1, 4.3, 8.6], f: [MX, 4.6, 9.2], fov: 52, ap: 3, seed: 9 }, u, d);
  });
  // S09 Then my reflection said it for me. (the reflection's face changes; his doesn't)
  shot(24.23, 26.72, (u, d, t) => {
    door(0);
    kidAt(MX, KZ + 0.4, PI, "worried");
    const tw = mirror({ face: t > 25.35 ? "twin" : "worried" });
    tw.j.head.rotation.z = win(t, 25.35, 26.2) * 0.22;
    dark(t);
    overShoulder(u, d, { push: [0.6, 1.1], seed: 10 });
  });
  // S10 "BLOODY MARY." (the reflection, alone, mouth wide)
  shot(26.72, 28.77, (u, d, t) => {
    door(0);
    kidAt(MX, KZ + 0.4, PI, "worried");
    const talk = t > 26.75 && t < 28.0 ? 0.5 + 0.5 * Math.sin(t * 14) : 0;
    const tw = mirror({ face: "twin", faceOpts: { talk: Math.round(talk * 4) / 4 } });
    tw.j.head.rotation.z = 0.22;
    dark(t, { candle: 1 + 0.4 * Math.sin(t * 31) * bump(t, 26.7, 28.2) });
    const rh = rHead();
    D.cam({ p: [[MX + 1.25, rh[1] + 0.35, -0.6], [MX + 1.05, rh[1] + 0.3, -1.4]], l: [rh[0] + 0.15, rh[1] - 0.3, rh[2]], f: rh, fov: 24, ap: 6, seed: 11, shake: 0.02 }, u, d);
  });
  // S11a My lips never moved. (his mouth shut tight)
  shot(28.77, 30.3, (u, d, t) => {
    door(0);
    kidAt(MX, KZ + 0.4, PI, "scared", { sweat: true });
    kid.j.head.rotation.y = Math.sin(t * 9) * 0.04;
    mirror({ face: "twin" });
    dark(t);
    const h = kHead();
    D.cam({ p: [[MX + 1.6, h[1] + 0.45, -5.5], [MX + 1.45, h[1] + 0.4, -5.4]], l: [h[0], h[1] - 0.4, h[2]], f: h, fov: 40, ap: 8, seed: 12 }, u, d);
  });
  // S11b …But in the mirror, they did.
  shot(30.3, 32.08, (u, d, t) => {
    door(0);
    kidAt(MX, KZ + 0.4, PI, "scared", { sweat: true });
    const talk = t > 30.35 && t < 31.75 ? 0.5 + 0.5 * Math.sin(t * 13) : 0;
    const tw = mirror({ face: "twin", faceOpts: { talk: Math.round(talk * 4) / 4 } });
    tw.j.head.rotation.z = 0.22;
    dark(t);
    overShoulder(u, d, { push: [0.9, 1.3], fov: 30, seed: 20 });
  });
  // S12a I ran out.
  shot(32.08, 33.3, (u, d, t) => {
    const k = win(t, 32.1, 32.4, ease.out);
    door(k);
    const run = win(t, 32.15, 33.2, ease.out);
    kidAt(MX, lerp(5.6, 9.4, run), 0, "scared", { sweat: true });
    D.walk(kid, t * 16, 0.9 * (1 - run * 0.7));
    friends(t, { faceA: "shock", faceB: "shock", z: 11.6 });
    D.lights("mary", 0, { hall: 1, candle: 1, t });
    D.cam({ p: [[MX + 0.4, 5.0, 15.6], [MX + 0.3, 4.9, 15.2]], l: [MX, 3.6, 7.4], f: [MX, 4.3, lerp(5.6, 9.4, run)], fov: 48, ap: 3, seed: 13, shake: 0.05 }, u, d);
  });
  // S12b …My friends looked at me like I was crazy.
  shot(33.3, 35.58, (u, d, t) => {
    door(1);
    kidAt(MX, 9.4, 0, "scared");
    kid.root.visible = false;
    friends(t, { faceA: "flat", faceB: "eyeroll", z: 12.8, dx: 0.85 });
    fa.root.rotation.y = PI + 0.3;
    fb.root.rotation.y = PI - 0.35;
    D.lights("mary", 0, { hall: 1, candle: 1, t, fill: [MX, 6.0, 9.0, 34], fillColor: "#ffd9a8" });
    D.cam({ p: [[MX + 0.2, 5.2, 7.6], [MX + 0.15, 5.15, 8.0]], l: [MX + 0.1, 4.5, 13.0], f: [MX - 0.4, 4.6, 12.8], fov: 54, ap: 4, seed: 14 }, u, d);
  });
  // S13 They said, we heard two of you in there.
  shot(35.58, 38.01, (u, d, t) => {
    door(1);
    kidAt(MX, 9.4, 0, "scared");
    friends(t, { faceA: talkFace(t, 35.6, 37.5, "momTalk", "worried"), faceB: "worried", z: 12.8, dx: 0.85 });
    kid.root.visible = false;
    fa.root.rotation.y = PI + 0.3;
    fb.root.rotation.y = PI - 0.35;
    const h = D.wpos(fa.j.head, [0, 0.62, 0]);
    D.lights("mary", 0, { hall: 1, candle: 1, t, fill: [h[0] + 0.6, h[1] + 1.0, h[2] - 3.0, 36], fillColor: "#ffd9a8" });
    D.cam({ p: [[h[0] + 0.9, h[1] + 0.35, h[2] - 3.9], [h[0] + 0.75, h[1] + 0.3, h[2] - 3.4]], l: [h[0], h[1] - 0.4, h[2]], f: h, fov: 42, ap: 5, seed: 15 }, u, d);
  });
  // S14 I looked back into the bathroom. (over his shoulder, through the doorway: candle, mirror)
  shot(38.01, 40.12, (u, d, t) => {
    door(1);
    kidAt(MX + 0.4, 9.6, PI, "scared");
    kid.j.head.rotation.y = lerp(-0.6, 0, win(t, 38.1, 38.9));
    const tw = mirror({ copy: false, face: "twin" });
    D.place(twin, MX - HX, 0, KZ, PI);
    friends(t, { faceA: "worried", faceB: "worried", z: 12.4 });
    D.lights("mary", 0, { hall: 0.55, candle: 1, t });
    D.cam({ p: [[MX + 1.4, 6.0, 12.6], [MX + 1.2, 5.9, 12.2]], l: [MX - 0.1, 4.8, ZM], f: [MX, 5.0, ZM - 2], fov: 40, ap: 2.5, seed: 16 }, u, d);
  });
  // S15 My reflection was still in the mirror. Without me. (push through the doorway to the glass)
  shot(40.12, 43.63, (u, d, t) => {
    door(1);
    kidAt(MX + 0.4, 9.6, PI, "scared");
    const tw = mirror({ copy: false, face: "twin" });
    D.place(twin, MX - HX, 0, KZ, PI);
    tw.j.head.rotation.z = 0.22 * win(t, 41.5, 42.6);
    D.lights("mary", 0, { hall: 0.4, candle: 1, t });
    kid.root.visible = false;
    D.cam({ p: [[MX + 0.15, 5.1, 9.0], [MX + 0.1, 5.0, 2.4]], l: [MX, MY - 0.4, ZM], f: rHead(), fov: 36, ap: 4, seed: 17 }, u, d);
  });
  // S16 And it was waving. (then the candle goes out)
  shot(43.63, 45.2, (u, d, t) => {
    door(1);
    const tw = mirror({ copy: false, face: "twin" });
    D.place(twin, MX - HX, 0, KZ, PI);
    tw.j.head.rotation.z = 0.22;
    tw.j.armR.rotation.set(-2.7 * win(t, 43.65, 44.05), 0, 0.25 * Math.sin(t * 7) * win(t, 43.9, 44.1));
    const cand = t < 44.95 ? 1 : 0;
    D.lights("mary", 0, { candle: cand, t });
    D.cam({ p: [[MX + 0.1, 5.0, 3.6], [MX + 0.08, 4.95, 3.0]], l: [MX, MY - 0.4, ZM], f: rHead(), fov: 36, ap: 4, seed: 18 }, u, d);
  });
  // END CARD: the dark bathroom, a last glint in the glass
  shot(45.2, 48.3, (u, d, t) => {
    door(1);
    const tw = mirror({ copy: false, face: "twin" });
    D.place(twin, MX - HX, 0, KZ, PI);
    D.lights("mary", 0, { candle: 0.12, t });
    D.cam({ p: [[MX + 0.08, 4.95, 3.0], [MX + 0.06, 4.9, 2.7]], l: [MX, MY - 0.4, ZM], f: rHead(), fov: 36, ap: 4, seed: 19 }, u, d);
    pipe.grade.uniforms.uFade.value = 0.35;
  });

  // COVER (thumbnail still): over his shoulder, he's terrified; the reflection grins and waves
  shot(200, 210, (u, d, t) => {
    door(0);
    kidAt(MX + 0.5, KZ + 0.5, PI - 0.75, "scared", { sweat: true });
    const tw = mirror({ copy: false, face: "twin", faceOpts: { talk: 0.25 } });
    D.place(twin, MX - HX - 0.1, 0, KZ, PI);
    tw.j.head.rotation.z = 0.22;
    tw.j.armR.rotation.set(-2.7, 0, 0.2);
    dark(1.3, { candle: 1.2 });
    D.cam({ p: [MX + 2.7, 5.1, -0.6], l: [MX - 0.2, 4.6, ZM - 0.4], f: rHead(), fov: 44, ap: 1.4, shake: 0, seed: 99 }, 0, 1);
  });

  return S;
}
