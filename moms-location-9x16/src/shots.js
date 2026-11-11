// Mom's Location, shot by shot. Times are seconds on audio/vo.wav; word cues from src/captions-data.js.
import * as THREE from "three";
import { makeDirector } from "./direct.js";
import { BED, CLOSET, HX } from "./world.js";
import { PLAN } from "./phone.js";
import { ease, win, lerp, lerp3, clamp, track } from "./util.js";

const PI = Math.PI;
const bump = (u, a, b) => (u <= a || u >= b ? 0 : Math.sin(((u - a) / (b - a)) * PI));
const KX = BED.x + 0.6, KZ = -7.3; // kid sitting up in bed
const FACE_AT = [KX, 6.25, KZ + 0.7]; // where the kid's phone screen points
const PH_OFF = [0.35, -0.15, 0.55];
const ME = [12, -12];
const GOODNIGHT = "Goodnight sweetie. Love you.";
const REPLY = "No sweetie. Still at work. Go to sleep.";
// type a string out between times a and b
const typed = (str, t, a, b) => str.slice(0, Math.round(clamp((t - a) / (b - a)) * str.length));

export function buildShots(ctx) {
  const D = makeDirector(ctx);
  const { C, W, pipe } = ctx;
  const P = W.props;
  const S = [];
  const shot = (t0, t1, run) => S.push({ t0, t1, run });
  const kid = C.kid, mom = C.mom, mim = C.mimic;

  // ---- kid sitting up in bed, phone in the right hand ----------------------------
  function kidBed({ face = "flat", faceOpts, look = 0, lookUp = 0, insert = false } = {}) {
    D.place(kid, KX, 0, KZ, 0);
    D.sit(kid, 3.2);
    kid.j.torso.rotation.x = -0.06;
    kid.setFace(face, faceOpts);
    kid.j.armR.rotation.set(-1.15, 0, -0.32);
    kid.j.armL.rotation.set(-0.85, 0, 0.42);
    kid.j.head.rotation.set(0.2 - lookUp, look, 0);
    P.blanket.position.set(BED.x + 0.3, 4.45, -4.44);
    P.blanket.scale.set(1, 1.1, 0.8);
    if (insert) {
      kid.root.visible = false;
      P.phone.grip.visible = true;
    }
    return kid;
  }
  const kidPhone = (state, o = {}) => D.holdPhone(kid, P.phone, { off: PH_OFF, at: FACE_AT, state, ...o });
  // screen insert: the phone in a fixed spot in front of the kid, hand gripping it
  const INS = [KX + 0.55, 5.25, KZ + 1.45];
  function insertPhone(state, { buzz = 0, t = 0 } = {}) {
    kidBed({ insert: true });
    const ph = P.phone;
    ph.group.visible = true;
    ph.group.position.set(INS[0] + Math.sin(t * 90) * 0.025 * buzz, INS[1], INS[2] + Math.cos(t * 77) * 0.02 * buzz);
    ph.group.lookAt(INS[0] - 0.1, INS[1] + 0.55, INS[2] - 3.0);
    P.blanket.material.color.setScalar(0.28);
    pipe.grade.uniforms.uVignette.value = 0.72;
    if (buzz) ph.group.rotateZ(Math.sin(t * 83) * 0.05 * buzz);
    ph.draw(state);
    return [INS[0], INS[1], INS[2]];
  }
  const insertLights = (pp, o = {}) => (D.lights("night", 0, { dark: true, phone: [pp[0] - 0.1, pp[1] + 0.4, pp[2] - 0.7, 2.2, 3], ...o }), (pipe.grade.uniforms.uVignette.value = 0.72));
  const kHead = () => D.wpos(kid.j.head, [0, 0.62, 0]);
  // a messages thread on the kid's phone (Mom's side on the left)
  const thread = (extra = [], o = {}) => ({
    screen: "msgs", name: "Mom", initial: "M", time: "2:14",
    items: [{ t: "day", text: "Yesterday 11:58 PM" }, { t: "them", text: GOODNIGHT }, { t: "day", text: "Today 2:14 AM" }, ...extra],
    ...o,
  });
  const mapState = (zoom, t, o = {}) => ({ screen: "map", zoom, ph: t * 0.7, me: ME, mom: PLAN.bedroom, where: "Home · Now", dist: "12 ft", time: "2:14", ...o });

  // ---- Mom at the nurses' station --------------------------------------------------------
  function momTyping(t) {
    D.place(mom, HX - 0.2, 0, -1.25, 0);
    mom.setFace("momSmile");
    mom.j.armR.rotation.set(-0.95 + Math.sin(t * 19) * 0.04, 0, -0.2);
    mom.j.armL.rotation.set(-0.95 + Math.sin(t * 23 + 1) * 0.04, 0, 0.2);
    mom.j.head.rotation.set(0.12, 0.42, 0);
    mom.j.torso.rotation.x = 0.06;
  }
  function momWhisper(t, talk) {
    D.place(mom, HX - 1.3, 0, -1.1, 0.3);
    mom.j.torso.rotation.x = 0.28;
    mom.j.head.rotation.set(0.1, -0.12, -0.14);
    mom.j.armR.rotation.set(-2.62, 0, -0.42);
    mom.j.armL.rotation.set(-2.15, 0, 0.62);
    const open = talk && Math.sin(t * 17) > -0.2;
    mom.setFace(open ? "momWhisper" : "momWorried");
    D.attach(P.handset, mom.j.head, [0.98, 0.52, 0.22], [-0.42, -PI / 2, 0]);
    const bottom = P.handset.localToWorld(new THREE.Vector3(0, -0.6, 0.05));
    P.setCord([P.cradle[0] + 0.3, P.cradle[1] - 0.1, P.cradle[2] + 0.1], [bottom.x, bottom.y, bottom.z]);
  }

  // ---- the thing: stretched, hunched, bare-footed --------------------------------------------
  function mimicPose({ x, z, ry, hunch = 0.2, headX = 0.4, headZ = 0.16, headY = 0, armF = 0.32, walkPh = null, duck = 0, talk = 0 }) {
    D.place(mim, x, 0, z, ry);
    mim.j.pelvis.position.y = mim.hipY;
    mim.j.torso.rotation.x = hunch + duck;
    mim.j.head.rotation.set(headX - duck * 0.7, headY, headZ);
    mim.j.armR.rotation.set(-armF, 0, -0.2);
    mim.j.armL.rotation.set(-armF * 0.9, 0, 0.3);
    if (walkPh !== null) {
      const s = Math.sin(walkPh);
      mim.j.legL.rotation.x = s * 0.3;
      mim.j.legR.rotation.x = -s * 0.3;
      mim.j.pelvis.position.y = mim.hipY - 0.12 + Math.abs(Math.cos(walkPh)) * 0.12;
    }
    mim.setFace("mimic", talk ? { talk: Math.round(talk * 4) / 4 } : undefined);
    return mim;
  }
  // its phone (Mom's lost one) in the right hand, screen to its face; fingers tapping
  function mimicPhone(t, state, tap = 1) {
    const at = D.wpos(mim.j.head, [0, 0.6, 0.5]);
    const p = D.holdPhone(mim, P.momPhone, { off: [0.32, -0.12, 0.36], at, state });
    mim.fingers.R.forEach((f, i) => (f.rotation.x = 0.55 + Math.max(0, Math.sin(t * 13 + i * 1.7)) * 0.45 * tap));
    mim.fingers.L.forEach((f, i) => (f.rotation.x = 0.35 + Math.max(0, Math.sin(t * 11 + i * 2.3)) * 0.3 * tap));
    return p;
  }
  const momThread = (draft, extra = []) => ({
    screen: "msgs", name: "Jamie", initial: "J", avatarColor: "#e8732a", time: "2:16",
    items: [{ t: "day", text: "Today 2:14 AM" }, { t: "them", text: "Are you home?" }, { t: "me", text: REPLY }, ...extra],
    draft,
  });
  const door = (k) => (P.closetDoor.rotation.y = -PI / 2 + lerp(0.22, 1.55, k));

  // ==========================================================================
  // S01 hook: the map, Mom's pin inside the house (2:14 on the status bar)
  shot(0, 2.3, (u, d, t) => {
    const pp = insertPhone(mapState(lerp(0.56, 0.63, u / d), t));
    insertLights(pp);
    D.phoneCam(P.phone, { dist: [2.60, 2.38], fov: 46, ly: -0.36, ap: 10, seed: 1 }, u, d);
  });
  // S02 …said she was in my bedroom (her face lit by the screen, eyes widen)
  shot(2.3, 5.05, (u, d, t) => {
    const wide = t > 4.2;
    kidBed({ face: wide ? "scared" : "flat", lookUp: win(u, 0.7, 0.85) * 0.25 });
    const pp = kidPhone(mapState(0.63, t));
    D.lights("night", 0, { dark: true, phone: [pp[0], pp[1] + 0.4, pp[2] + 0.2, 7, 6] });
    const h = kHead();
    D.cam({ p: [[h[0] + 1.6, h[1] - 0.2, h[2] + 4.6], [h[0] + 1.1, h[1] - 0.1, h[2] + 3.4]], l: [h[0], h[1] - 0.3, h[2]], f: h, fov: 32, ap: 9, seed: 2 }, u, d);
  });
  // S03 She works night shifts at the hospital
  shot(5.05, 8.1, (u, d, t) => {
    D.lights("hospital", 0, { fill: [HX + 1.5, 6.5, 3, 40], fillColor: "#e6fff4" });
    momTyping(t);
    D.cam({ p: [[HX + 3.3, 5.3, 5.4], [HX + 2.6, 5.1, 4.4]], l: [HX + 0.3, 3.75, -1.2], f: [HX - 0.2, 4.7, -1.1], fov: 36, ap: 6, seed: 3 }, u, d);
  });
  // S04 We share locations... (seen from beside the closet door: the door edge in the foreground)
  shot(8.1, 12.0, (u, d, t) => {
    const shrug = bump(t, 10.85, 11.75);
    kidBed({ face: "flat", look: -0.05 });
    kid.j.head.rotation.z = shrug * 0.18;
    kid.j.armL.rotation.z = 0.42 + shrug * 0.25;
    const pp = kidPhone(mapState(0.63, t));
    D.lights("night", 0, { phone: [pp[0] - 0.2, pp[1] + 0.7, pp[2] - 0.3, 7, 5] });
    const kh = kHead();
    D.cam({ p: [[11.2, 5.6, 3.1], [10.9, 5.5, 2.8]], l: [kh[0], kh[1] - 1.6, kh[2]], f: kh, fov: 34, ap: 3, seed: 4, shake: 0.02 }, u, d);
  });
  // S05 So I texted her. Are you home?
  shot(12.0, 14.25, (u, d, t) => {
    const sent = t >= 13.55;
    const k = win(t, 13.55, 13.75, ease.outBack);
    const st = thread(sent ? [{ t: "me", text: "Are you home?", k }, ...(t > 13.85 ? [{ t: "note", text: "Delivered" }] : [])] : [], { draft: sent ? "" : typed("Are you home?", t, 12.2, 13.35), ph: t * 1.2 });
    const pp = insertPhone(st);
    insertLights(pp);
    D.phoneCam(P.phone, { dist: [2.50, 2.44], fov: 46, ly: -0.36, ap: 10, seed: 5 }, u, d);
  });
  // S06 She replied right away (typing dots)
  shot(14.25, 15.95, (u, d, t) => {
    const st = thread([{ t: "me", text: "Are you home?" }, { t: "note", text: "Read 2:14 AM" }, { t: "typing", k: win(t, 14.35, 14.55, ease.outBack) }], { ph: t * 1.6 });
    const pp = insertPhone(st);
    insertLights(pp);
    D.phoneCam(P.phone, { dist: [2.44, 2.38], fov: 46, ly: -0.36, ap: 10, seed: 6 }, u, d);
  });
  // S07 No sweetie. Still at work. Go to sleep.
  shot(15.95, 18.55, (u, d, t) => {
    const st = thread([{ t: "me", text: "Are you home?" }, { t: "note", text: "Read 2:14 AM" }, { t: "them", text: REPLY, k: win(t, 15.97, 16.2, ease.outBack) }], { ph: t });
    const pp = insertPhone(st);
    insertLights(pp);
    D.phoneCam(P.phone, { dist: [2.38, 2.22], fov: 46, ly: -0.36, ap: 10, seed: 7 }, u, d);
  });
  // S08 But the second her text came in… (relief, then the eyes slide to the closet)
  shot(18.55, 20.7, (u, d, t) => {
    const turn = win(t, 19.9, 20.6);
    kidBed({ face: t < 19.75 ? "relief" : "worried", look: turn * 0.75 });
    const pp = kidPhone(thread([{ t: "them", text: REPLY }]));
    D.lights("night", 0, { dark: true, phone: [pp[0], pp[1] + 0.4, pp[2] + 0.2, 7, 6] });
    const h = kHead();
    D.cam({ p: [[h[0] - 1.2, h[1] - 0.1, h[2] + 3.6], [h[0] - 1.0, h[1] - 0.05, h[2] + 3.0]], l: [h[0] + 0.1, h[1] - 0.25, h[2]], f: h, fov: 32, ap: 9, seed: 8 }, u, d);
  });
  // S09 …my closet lit up
  shot(20.7, 22.25, (u, d, t) => {
    kidBed({ face: "worried", look: 0.75 });
    const fl = t < 21.3 ? 0 : t < 21.42 ? 1 : t < 21.5 ? 0.2 : t < 21.62 ? 1 : lerp(1, 0.55, win(t, 21.7, 22.25));
    mimicPose({ x: CLOSET.inX + 0.4, z: CLOSET.zc + 0.2, ry: -PI / 2, hunch: 0.1 });
    const mp = mimicPhone(t, momThread(""), 0);
    P.momPhone.mat.color.setScalar(fl > 0 ? 1 : 0);
    D.lights("night", 0, { dark: true, closet: fl * 1.2, closetAt: [mp[0] - 0.5, mp[1] + 0.3, mp[2]] });
    D.cam({ p: [[1.5, 5.4, -3.6], [2.3, 5.2, -2.6]], l: [11.6, 3.4, 4.2], f: [11.6, 3.4, 4.6], fov: 36, ap: 3, seed: 9 }, u, d);
  });
  // S10 I zoomed in on the map
  shot(22.25, 24.05, (u, d, t) => {
    const z = lerp(0.63, 1, win(t, 22.4, 23.8));
    const mp = lerp3([...PLAN.bedroom, 0], [...PLAN.closet, 0], win(t, 23.2, 23.9));
    const pp = insertPhone(mapState(z, t, { mom: [mp[0], mp[1]], dist: t > 23.6 ? "9 ft" : "12 ft" }));
    insertLights(pp);
    D.phoneCam(P.phone, { dist: [2.44, 2.22], fov: 46, ly: -0.36, ap: 10, seed: 10 }, u, d);
  });
  // S11 Her dot was inside my closet (rack focus from the screen to the door, from the kid's eyes)
  shot(24.05, 26.6, (u, d, t) => {
    kidBed({ insert: true });
    const E = new THREE.Vector3(KX, 6.35, KZ + 0.4), T = new THREE.Vector3(11.9, 3.7, 4.4);
    const dir = T.clone().sub(E).normalize();
    const right = new THREE.Vector3().crossVectors(dir, new THREE.Vector3(0, 1, 0)).normalize();
    const ph = E.clone().addScaledVector(dir, 1.35).addScaledVector(right, 0.42).add(new THREE.Vector3(0, -0.42, 0));
    P.phone.group.visible = true;
    P.phone.group.position.copy(ph);
    P.phone.group.lookAt(E.x, E.y - 0.1, E.z);
    P.phone.draw(mapState(1, t, { mom: PLAN.closet, dist: "9 ft", distColor: "#ff6a5a" }));
    mimicPose({ x: CLOSET.inX + 0.4, z: CLOSET.zc + 0.2, ry: -PI / 2, hunch: 0.1 });
    const mp = mimicPhone(t, momThread(""), 0);
    D.lights("night", 0, { dark: true, closet: 0.5, closetAt: [mp[0] - 0.5, mp[1] + 0.3, mp[2]], phone: [ph.x - dir.x * 0.4, ph.y + 0.4, ph.z - dir.z * 0.4, 2.5, 3] });
    const rack = win(t, 25.0, 25.9);
    const cp = E.clone().addScaledVector(dir, -0.6).addScaledVector(right, 0.15).add(new THREE.Vector3(0, 0.15, 0));
    D.cam({ p: [[cp.x, cp.y, cp.z], [cp.x + dir.x * 0.35, cp.y, cp.z + dir.z * 0.35]], l: [T.x, T.y + 0.6, T.z], f: lerp3([ph.x, ph.y, ph.z], [T.x, T.y, T.z], rack), fov: 40, ap: 10, seed: 11 }, u, d);
  });
  // S12 Then my phone rang. It was the hospital.
  shot(26.6, 29.3, (u, d, t) => {
    const active = t > 28.9;
    const buzz = active ? 0 : t > 26.65 ? 0.6 + 0.4 * Math.max(0, Math.sin(t * 9)) : 0;
    const pp = insertPhone({ screen: "call", active, secs: t - 28.9, ph: t * 0.9, time: "2:15" }, { buzz, t });
    insertLights(pp, { phoneColor: "#c6ffd8" });
    D.phoneCam(P.phone, { dist: [2.50, 2.32], fov: 46, ly: -0.36, ap: 10, seed: 12, shake: 0.01 }, u, d);
  });
  // S13 Baby, it's Mom. I lost my phone at home last week.
  shot(29.3, 32.25, (u, d, t) => {
    D.lights("hospital", 0, { fill: [HX + 0.5, 7, 3.5, 30], fillColor: "#e6fff4" });
    pipe.grade.uniforms.uVignette.value = 0.62;
    momWhisper(t, t > 29.4 && t < 31.95);
    const h = D.wpos(mom.j.head, [0, 0.6, 0]);
    D.cam({ p: [[h[0] - 0.4, h[1] + 0.25, h[2] + 5.0], [h[0] - 0.2, h[1] + 0.2, h[2] + 4.0]], l: [h[0] + 0.35, h[1] - 1.05, h[2]], f: h, fov: 36, ap: 8, seed: 13 }, u, d);
  });
  // S14 Who have you been texting? (phone to the ear, eyes going to the closet)
  shot(32.25, 34.2, (u, d, t) => {
    kidBed({ face: "scared", faceOpts: { sweat: true }, look: win(t, 32.8, 34.0) * 0.7 });
    kid.j.armR.rotation.set(-2.55, 0, -0.42);
    D.attach(P.phone.group, kid.j.head, [0.72, 0.5, 0.12], [-0.3, PI / 2, 0]);
    P.phone.group.visible = true;
    P.phone.draw({ screen: "call", active: true, secs: 4, time: "2:15" });
    const h = kHead();
    D.lights("night", 0, { dark: true, closet: 0.4, phone: [h[0] + 1.1, h[1] - 0.1, h[2] + 0.6, 1.6, 3] });
    D.cam({ p: [[h[0] - 1.5, h[1] + 0.3, h[2] + 4.6], [h[0] - 1.2, h[1] + 0.2, h[2] + 3.9]], l: [h[0] + 0.3, h[1] - 0.95, h[2]], f: h, fov: 36, ap: 9, seed: 14 }, u, d);
  });
  // S15 Every night this week, Mom had texted me goodnight (scrolling back through the week)
  shot(34.2, 37.65, (u, d, t) => {
    const days = ["Mon 11:52 PM", "Tue 11:58 PM", "Wed 11:49 PM", "Thu 12:03 AM", "Fri 11:57 PM", "Sat 11:55 PM", "Yesterday 11:58 PM"];
    const items = [];
    for (const dd of days) items.push({ t: "day", text: dd }, { t: "them", text: GOODNIGHT });
    items.push({ t: "day", text: "Today 2:14 AM" }, { t: "me", text: "Are you home?" }, { t: "them", text: REPLY });
    const sc = track([[0, 0], [0.12, 0], [0.85, 1220], [1, 1290]], u / d, ease.inOut);
    const pp = insertPhone({ screen: "msgs", name: "Mom", initial: "M", time: "2:15", items, scroll: sc, ph: t });
    insertLights(pp);
    D.phoneCam(P.phone, { dist: [2.50, 2.32], fov: 46, ly: -0.36, ap: 10, seed: 15 }, u, d);
  });
  // S16 And my closet door was opening
  shot(37.65, 40.05, (u, d, t) => {
    kidBed({ face: "scared", look: 0.85 });
    door(win(t, 37.8, 39.9, ease.inOut));
    mimicPose({ x: CLOSET.inX + 0.5, z: CLOSET.zc + 0.3, ry: -PI / 2, hunch: 0.15, headX: 0.5 });
    const mp = mimicPhone(t, momThread(""), 0.6);
    D.lights("night", 0, { dark: true, closet: 0.42, closetAt: [mp[0] - 0.3, mp[1] + 0.2, mp[2]] });
    D.cam({ p: [[-1.0, 6.4, -5.0], [0.4, 6.1, -3.9]], l: [11.8, 4.2, 4.4], f: [12, 4.2, 4.4], fov: 34, ap: 3, seed: 16, shake: 0.03 }, u, d);
  });
  // S17 Something stepped out wearing my mom's scrubs (it ducks under the door frame)
  shot(40.05, 42.95, (u, d, t) => {
    door(1);
    const k = win(t, 40.1, 42.5, ease.inOut);
    const x = lerp(CLOSET.inX + 0.5, 9.4, k);
    const duck = Math.max(0, 1 - Math.abs(x - 12.2) / 2.4) * 0.95;
    mimicPose({ x, z: lerp(CLOSET.zc + 0.3, 3.6, k), ry: -PI / 2 - 0.35 * k, walkPh: k * PI * 3, duck, hunch: 0.18 });
    const mp = mimicPhone(t, momThread(""), 0.6);
    D.lights("night", 0, { dark: true, closet: 0.3, closetAt: [CLOSET.inX, 4.0, CLOSET.zc], phone: [mp[0] - 0.9, mp[1] + 1.2, mp[2] - 0.8, 4, 6] });
    D.cam({ p: [[3.2, 4.4, -2.4], [3.6, 4.6, -2.0]], l: [[11.6, 4.4, 4.2], [10.4, 5.4, 3.8]], f: [x, 4.6, 3.9], fov: 46, ap: 3, seed: 17 }, u, d);
  });
  // S18 It was way too tall (low from the bed: the whole figure, head near the ceiling)
  const MX = 6.4, MZ = 0.8, MRY = Math.atan2(KX - 6.4, KZ - 0.8);
  function mimicTyping(t, draft, tap = 1) {
    const m = mimicPose({ x: MX, z: MZ, ry: MRY, hunch: 0.22, headX: 0.72, headZ: 0.22 });
    m.j.armR.rotation.set(-0.55, 0, -0.3);
    m.j.armL.rotation.set(-0.5, 0, 0.4);
    return mimicPhone(t, momThread(draft), tap);
  }
  shot(42.95, 44.7, (u, d, t) => {
    door(1);
    kidBed({ face: "scared", faceOpts: { sweat: true }, look: 0.7, lookUp: 0.2 });
    kid.j.head.visible = false;
    const pp = mimicTyping(t, "Go", 0.8);
    const fh = D.wpos(mim.j.head, [0, 0.6, 0.4]);
    D.lights("night", 0, { closet: 0.3, phone: [lerp(pp[0], fh[0], 0.5), lerp(pp[1], fh[1], 0.45), lerp(pp[2], fh[2], 0.5), 9, 6] });
    D.cam({ p: [[-3.4, 3.7, -5.0], [-3.0, 3.5, -4.6]], l: [[MX - 0.6, 4.6, MZ - 0.5], [MX - 0.5, 6.0, MZ - 0.4]], f: [MX, 5.5, MZ], fov: 56, ap: 2, seed: 18 }, u, d);
  });
  // S19 ...and it was still typing (insert: Mom's phone in the long pale fingers)
  shot(44.7, 46.45, (u, d, t) => {
    door(1);
    const ph = P.momPhone;
    ph.grip.visible = true;
    ph.group.visible = true;
    ph.group.position.set(7.2, 4.4, 2.2);
    ph.group.lookAt(4.0, 7.2, -0.6);
    ph.grip.userData.thumb.rotation.z = -0.12 + Math.max(0, Math.sin(t * 13)) * 0.22;
    ph.grip.userData.thumb.position.z = 0.05 + Math.max(0, Math.sin(t * 13)) * 0.02;
    ph.draw(momThread(typed("Go to sleep, sweetie", t, 44.85, 46.3), []));
    D.lights("night", 0, { dark: true, closet: 0.3, phone: [6.6, 5.0, 1.6, 3.2, 4] });
    D.phoneCam(ph, { dist: [3.6, 3.35], ap: 5, seed: 19 }, u, d);
  });
  // S20 My phone buzzed
  shot(46.45, 47.95, (u, d, t) => {
    const buzz = t > 46.55 && t < 46.95 ? 1 : 0;
    const pp = insertPhone({ screen: "lock", time: "2:16", notif: win(t, 46.58, 46.85, ease.outBack), msg: "Go to sleep, sweetie." }, { buzz, t });
    insertLights(pp);
    D.phoneCam(P.phone, { dist: [2.44, 2.27], fov: 46, ly: -0.36, ap: 10, seed: 20, shake: buzz ? 0.03 : 0.006 }, u, d);
  });
  // S21 "Go to sleep, sweetie." (it leans down over the bed; we are the kid)
  shot(47.95, 49.95, (u, d, t) => {
    door(1);
    kidBed({ face: "scared", faceOpts: { sweat: true }, look: 0.4, lookUp: 0.3 });
    kid.j.head.visible = false;
    const lean = win(t, 47.95, 49.3);
    const lunge = win(t, 49.5, 49.85, ease.in);
    const talk = t > 48.0 && t < 49.45 ? 0.5 + 0.5 * Math.sin(t * 15) : 0;
    const mx = lerp(0.6, -0.4, lean) - lunge * 1.6, mz = lerp(-3.1, -3.9, lean) - lunge * 1.2;
    mimicPose({ x: mx, z: mz, ry: Math.atan2(KX - mx, KZ - mz), hunch: lerp(0.62, 0.88, lean) + lunge * 0.2, headX: 0.1, headZ: lerp(0.12, 0.45, win(t, 48.5, 49.0)), talk });
    mim.j.armR.rotation.set(-0.5, 0, -0.25);
    mimicPhone(t, momThread("Go to sleep, sweetie"), 0);
    const fh = D.wpos(mim.j.head, [0, 0.62, 0.3]);
    D.lights("night", 0, { dark: true, phone: [fh[0] + 0.3, fh[1] - 1.7, fh[2] + 0.6, 4.5, 5] });
    const eye = [KX + 0.15, 6.4, KZ + 0.6];
    D.cam({ p: eye, l: [fh[0], fh[1] - 0.6, fh[2]], f: fh, fov: lerp(50, 40, lean), ap: 4, seed: 21, shake: 0.03 }, u, d);
    pipe.grade.uniforms.uFade.value = win(t, 49.72, 49.95);
  });
  // END CARD: the phone left on the blanket; both dots in the same room
  shot(49.95, 53.0, (u, d, t) => {
    door(1);
    P.blanket.position.set(BED.x + 0.3, 3.45, -4.4);
    P.phone.group.visible = true;
    P.phone.group.position.set(BED.x + 0.6, 3.75, -5.2);
    P.phone.group.rotation.set(-PI / 2, 0, 0.35);
    P.phone.draw(mapState(1, t, { me: [14, -10], mom: [17, -8], where: "Home · Now", dist: "0 ft", distColor: "#ff6a5a", time: "2:17" }));
    D.lights("night", 0, { dark: true, phone: [BED.x + 0.6, 4.6, -5.2, 5, 5] });
    D.cam({ p: [[BED.x + 0.6, 7.0, -4.45], [BED.x + 0.6, 6.7, -4.55]], l: [BED.x + 0.6, 3.75, -4.6], up: [0, 0, -1], f: [BED.x + 0.6, 3.75, -5.2], fov: 40, ap: 4, seed: 22 }, u, d);
    pipe.grade.uniforms.uFade.value = lerp(1, 0.35, win(u, 0, 0.12)) ;
  });

  // COVER (thumbnail still): from the kid's eyes, the thing leaning in with Mom's smile; the map in hand
  shot(200, 210, (u, d, t) => {
    door(1);
    kidBed({ insert: true });
    const mx = 0.2, mz = -3.6;
    mimicPose({ x: mx, z: mz, ry: Math.atan2(KX - mx, KZ - mz), hunch: 0.72, headX: 0.12, headZ: 0.32, talk: 0.25 });
    mim.j.armR.rotation.set(-0.5, 0, -0.25);
    mimicPhone(1.3, momThread("Go to sleep, sweetie"), 0);
    const fh = D.wpos(mim.j.head, [0, 0.62, 0.3]);
    const E = new THREE.Vector3(KX + 0.15, 6.3, KZ + 0.6);
    const F = new THREE.Vector3(fh[0], fh[1] - 0.6, fh[2]);
    const dir = F.clone().sub(E).normalize();
    const right = new THREE.Vector3().crossVectors(dir, new THREE.Vector3(0, 1, 0)).normalize();
    const ph = E.clone().addScaledVector(dir, 1.9).addScaledVector(right, 0.55).add(new THREE.Vector3(0, -1.05, 0));
    P.phone.group.visible = true;
    P.phone.group.position.copy(ph);
    P.phone.group.lookAt(E.x, E.y, E.z);
    P.phone.draw(mapState(1, 0.3, { mom: PLAN.bedroom, me: [16, -10], dist: "0 ft", distColor: "#ff6a5a" }));
    D.lights("night", 0, { phone: [fh[0] + 0.3, fh[1] - 1.7, fh[2] + 0.6, 6, 5] });
    D.cam({ p: [E.x, E.y - 0.3, E.z], l: [F.x, F.y + 0.3, F.z], f: fh, fov: 60, ap: 1.2, shake: 0, seed: 99 }, 0, 1);
  });

  return S;
}
