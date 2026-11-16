// Front Door Locked, shot by shot. Times are seconds on audio/vo.wav (audio/vo-lines.json).
import * as THREE from "three";
import { makeDirector } from "./direct.js";
import { BED, HX, FD, BD, PCAM } from "./world.js";
import { ease, win, lerp, lerp3, clamp } from "./util.js";

const PI = Math.PI;
const bump = (u, a, b) => (u <= a || u >= b ? 0 : Math.sin(((u - a) / (b - a)) * PI));
const pad = (n) => String(Math.floor(n)).padStart(2, "0");
const stamp = (s) => `03:12:${pad(s)} AM`;
const NOTIF_CAM = { screen: "lock", time: "3:12", app: "FRONT DOOR CAM", glyph: "cam", appColor: "#2f7cf6", title: "Front Door", msg: "Motion at front door" };
const NOTIF_LOCK = { screen: "lock", time: "3:12", app: "SMART LOCK", glyph: "lock", appColor: "#ff9f0a", title: "Front Door: Locked", msg: "Locked from inside", msg2: "No one in your home used a code" };

export function buildShots(ctx) {
  const D = makeDirector(ctx);
  const { C, W, pipe } = ctx;
  const P = W.props;
  const S = [];
  const kid = C.kid, st = C.stranger;
  // two faint pale eyes on the man's shadow face (only in the shots that turn them on)
  const eyeM = new THREE.MeshBasicMaterial({ color: "#e8e2d6" });
  eyeM.color.multiplyScalar(1.5);
  const eyes = [-0.18, 0.18].map((x) => {
    const e = new THREE.Mesh(new THREE.SphereGeometry(0.055, 10, 8), eyeM);
    e.position.set(x, 0.7, 0.6);
    e.visible = false;
    st.j.head.add(e);
    return e;
  });
  const eyesOn = (on = true) => eyes.forEach((e) => (e.visible = on));
  const shot = (t0, t1, run) => S.push({ t0, t1, run: (u, d, t) => { eyesOn(false); run(u, d, t); } });
  const G = () => pipe.grade.uniforms;

  // ---- the narrator ---------------------------------------------------------------
  function asleep(t) {
    kid.setOutfit("pjs");
    D.place(kid, BED.x, 3.72, -3.1, 0);
    kid.root.rotation.x = -PI / 2;
    kid.setFace("sleep");
    kid.j.head.rotation.y = 0.85 + Math.sin(t * 0.6) * 0.03;
    kid.j.armL.rotation.set(0, 0, 0.05);
    kid.j.armR.rotation.set(0, 0, -0.05);
    P.blanket.position.set(BED.x, 4.25, -3.95);
    P.blanket.scale.set(1.0, 1.0, 0.98);
  }
  // sitting up against the headboard, legs under the blanket
  function inBed({ face = "flat", faceOpts, look = 0, lookUp = 0 } = {}) {
    kid.setOutfit("pjs");
    D.place(kid, BED.x, 0, -8.15, 0);
    D.sit(kid, 3.15);
    kid.j.torso.rotation.x = -0.16;
    kid.setFace(face, faceOpts);
    kid.j.head.rotation.set(0.12 - lookUp, look, 0);
    kid.j.armL.rotation.set(-1.25, 0, 0.42);
    kid.j.armR.rotation.set(-1.25, 0, -0.42);
    P.blanket.position.set(BED.x, 4.0, -4.7);
    P.blanket.scale.set(1.0, 1.0, 0.9);
    return kid;
  }
  // morning: sitting on the edge of the bed
  function onEdge({ face = "flat", faceOpts, look = 0, lookUp = 0.25 } = {}) {
    kid.setOutfit("pjs");
    D.place(kid, BED.edgeX - 0.35, 0, -5.3, PI / 2);
    D.sit(kid, 3.05);
    kid.j.torso.rotation.x = 0.12;
    kid.setFace(face, faceOpts);
    kid.j.head.rotation.set(lookUp, look, 0);
    kid.j.armL.rotation.set(-1.15, 0, 0.42);
    kid.j.armR.rotation.set(-1.15, 0, -0.42);
    P.blanket.position.set(BED.x - 0.4, 3.45, -5.0);
    P.blanket.scale.set(0.9, 1.0, 0.9);
    return kid;
  }
  const kHead = () => D.wpos(kid.j.head, [0, 0.62, 0]);
  const phoneInHands = (state, { buzz = 0, t = 0 } = {}) => {
    const hl = D.wpos(kid.j.handL, [0, -0.25, 0]), hr = D.wpos(kid.j.handR, [0, -0.25, 0]);
    const ph = P.phone;
    ph.group.visible = true;
    const m = [(hl[0] + hr[0]) / 2, (hl[1] + hr[1]) / 2 + 0.25, (hl[2] + hr[2]) / 2];
    ph.group.position.set(m[0] + Math.sin(t * 90) * 0.02 * buzz, m[1], m[2] + Math.cos(t * 77) * 0.02 * buzz);
    const h = D.wpos(kid.j.head, [0, 0.55, 0.5]);
    ph.group.lookAt(h[0], h[1], h[2]);
    if (state) ph.draw(state);
    return m;
  };
  // insert: the phone held up in front of the narrator in bed (narrator hidden, grip hand shown)
  function insert(state, { buzz = 0, t = 0, at = [BED.x + 0.25, 5.9, -6.3] } = {}) {
    inBed();
    kid.root.visible = false;
    const ph = P.phone;
    ph.grip.visible = true;
    ph.group.visible = true;
    ph.group.position.set(at[0] + Math.sin(t * 90) * 0.025 * buzz, at[1], at[2] + Math.cos(t * 77) * 0.02 * buzz);
    ph.group.lookAt(BED.x - 0.1, 6.5, -8.7);
    if (buzz) ph.group.rotateZ(Math.sin(t * 83) * 0.05 * buzz);
    ph.draw(state);
    return at;
  }
  const insertLights = (pp, t, o = {}) => {
    D.lights(o.dawn ? "dawn" : "night", o.dawn ? 1 : 0, { dark: !o.dawn, fill: [pp[0] - 0.4, pp[1] + 0.4, pp[2] - 1.0, o.dawn ? 6 : 9], fillColor: o.dawn ? "#ffe2c0" : "#b9cdff" });
    G().uVignette.value = 0.72;
  };
  // ---- the porch camera -------------------------------------------------------------
  function porchCam(u, d, t, { open = 0, zoom = 0, sec = 4, live = false, motion = 0 } = {}) {
    P.frontDoor.rotation.y = -open * 1.25;
    P.voidWall.visible = true;
    D.lights("nv", 0, {});
    const z = ease.inOut(clamp(zoom));
    const look = lerp3([FD.x - 0.4, 3.0, FD.z + 1.4], [FD.x - 0.15, 3.9, FD.z], z);
    D.cam({ p: [PCAM, PCAM], l: [look, look], fov: lerp(76, 30, z), ap: 0, shake: 0, seed: 1 }, u, d);
    ctx.hud = { live, stamp: stamp(sec), motion, zoom: z > 0.05 ? (1 + z * 2.4).toFixed(1) + "x" : 0 };
  }
  // ---- the man ----------------------------------------------------------------------
  function stranger(x, z, ry, { turn = 0, armUp = 0 } = {}) {
    D.place(st, x, 0, z, ry);
    st.root.scale.setScalar(1.12);
    st.setFace("shadow");
    st.j.head.rotation.set(0.12, turn, 0);
    st.j.armR.rotation.set(lerp(0, -1.45, armUp), 0, lerp(-0.06, -0.25, armUp));
    st.j.armL.rotation.set(0, 0, 0.06);
    return D.wpos(st.j.head, [0, 0.62, 0]);
  }
  const doorStranger = (t, o = {}) => stranger(BD.x - 0.6, 11.7, PI - 0.25, o);

  // ==========================================================================
  // S01 hook: asleep; the phone on the nightstand lights up
  shot(0, 2.25, (u, d, t) => {
    asleep(t);
    const ph = P.phone;
    ph.group.visible = true;
    ph.group.position.set(-1.85, 2.86, -7.95);
    ph.group.rotation.set(-PI / 2, 0, 0.5);
    ph.draw({ ...NOTIF_CAM, notif: clamp((t - 0.45) * 3) });
    P.clock.set("3:12");
    D.lights("night", 0, { dark: true, phone: [-1.85, 3.6, -7.95, t > 0.45 ? 9 : 0, 7] });
    D.cam({ p: [[2.6, 10.0, -1.4], [1.9, 9.3, -2.4]], l: [-4.8, 3.5, -8.5], f: [-5.0, 3.8, -8.8], fov: 42, ap: 1.6, seed: 1 }, u, d);
  });
  // S02 …At exactly three twelve. (the LED clock flips)
  shot(2.25, 4.3, (u, d, t) => {
    asleep(t);
    P.clock.set(t < 3.32 ? "3:11" : "3:12");
    const ph = P.phone;
    ph.group.visible = true;
    ph.group.position.set(-1.85, 2.86, -7.95);
    ph.group.rotation.set(-PI / 2, 0, 0.5);
    ph.draw({ ...NOTIF_CAM, notif: 1 });
    D.lights("night", 0, { dark: true, phone: [-1.85, 3.6, -7.95, 7, 7] });
    D.cam({ p: [[-3.55, 4.5, -5.1], [-3.3, 4.35, -5.5]], l: [-1.6, 3.05, -8.1], f: [-1.5, 3.23, -8.1], fov: 34, ap: 6, seed: 2 }, u, d);
  });
  // S03 "Motion at front door."
  shot(4.3, 6.1, (u, d, t) => {
    const pp = insert({ ...NOTIF_CAM, notif: clamp((t - 4.35) * 4) });
    insertLights(pp, t);
    D.phoneCam(P.phone, { dist: [2.25, 2.02], fov: 46, ly: -0.3, ap: 10, seed: 3 }, u, d);
  });
  // S04 Every morning, I check the clip.
  shot(6.1, 8.0, (u, d, t) => {
    onEdge({ face: "flat", lookUp: 0.3 });
    phoneInHands({ screen: "cam", stamp: stamp(4), scrub: 0.15, frame: 3, time: "7:42" });
    P.clock.set("7:42");
    D.lights("dawn", 1, {});
    const h = kHead();
    D.cam({ p: [[h[0] + 9.0, h[1] - 0.2, h[2] + 3.4], [h[0] + 8.0, h[1] - 0.3, h[2] + 3.0]], l: [h[0], h[1] - 1.5, h[2]], f: h, fov: 42, ap: 3, seed: 4 }, u, d);
  });
  // S05 …And the porch is always empty. (the clip, full screen)
  shot(8.0, 10.15, (u, d, t) => {
    porchCam(u, d, t, { sec: 4 + (t - 8.0), motion: 1 });
  });
  // S06 Then I noticed something.
  shot(10.15, 11.95, (u, d, t) => {
    onEdge({ face: "worried", lookUp: 0.35 });
    kid.j.torso.rotation.x = 0.12 + win(t, 10.2, 11.2) * 0.12;
    phoneInHands({ screen: "cam", stamp: stamp(0), scrub: 0.02, door: 0.1, frame: 5, time: "7:43" });
    D.lights("dawn", 1, {});
    const h = kHead();
    D.cam({ p: [[h[0] + 6.4, h[1] - 0.3, h[2] - 2.8], [h[0] + 5.6, h[1] - 0.35, h[2] - 2.4]], l: [h[0], h[1] - 1.2, h[2]], f: h, fov: 40, ap: 4, seed: 6 }, u, d);
  });
  // S07 The clips don't start on the porch. (scrub back to the first second)
  shot(11.95, 13.7, (u, d, t) => {
    const k = win(t, 12.1, 13.2);
    const pp = insert({ screen: "cam", stamp: stamp(lerp(4, 0, k)), scrub: lerp(0.15, 0.0, k), door: lerp(0, 0.18, k), frame: Math.floor(t * 12), time: "7:43" });
    insertLights(pp, t, { dawn: true });
    D.phoneCam(P.phone, { dist: [2.15, 1.95], fov: 46, ly: -0.28, ap: 10, seed: 7 }, u, d);
  });
  // S08 They start with my front door opening.
  shot(13.7, 16.1, (u, d, t) => {
    porchCam(u, d, t, { open: ease.inOut(win(t, 13.95, 15.7)) * 0.85, sec: (t - 13.7) * 0.9 });
  });
  // S09 From the inside. (digital zoom into the black gap)
  shot(16.1, 17.9, (u, d, t) => {
    porchCam(u, d, t, { open: 0.85, zoom: win(t, 16.15, 17.1), sec: 2 + (t - 16.1) * 0.9 });
  });
  // S10 Someone had been walking out of my house every night. (inside: the door wide open, moonlight)
  shot(17.9, 20.4, (u, d, t) => {
    P.frontDoor.rotation.y = -1.25 + win(t, 18.6, 20.4) * 0.35;
    D.lights("entry", 0, { beam: 1 });
    D.cam({ p: [[HX + 0.2, 6.4, -1.8], [HX + 0.9, 6.0, -0.4]], l: [FD.x - 0.6, 3.0, FD.z - 1.0], f: [FD.x, 3.6, FD.z], fov: 46, ap: 2.5, seed: 10 }, u, d);
  });
  // S11 And coming back in before I woke up. (asleep; the bedroom door ajar)
  shot(20.4, 23.05, (u, d, t) => {
    asleep(t);
    P.bedDoor.rotation.y = -0.3;
    P.clock.set("3:12");
    D.lights("night", 0, { dark: true });
    D.cam({ p: [[-2.2, 6.8, -9.2], [-1.6, 6.5, -8.6]], l: [BD.x, 3.8, BD.z], f: [BD.x, 4, BD.z], fov: 34, ap: 3, seed: 11 }, u, d);
  });
  // S12 So last night, I stayed up and watched the live feed.
  shot(23.05, 26.45, (u, d, t) => {
    inBed({ face: "flat", lookUp: 0.15 });
    const pp = phoneInHands({ screen: "cam", live: true, stamp: stamp(0).replace("12:00", "08:51"), door: 0, frame: Math.floor(t * 12), time: "3:08" });
    D.lights("night", 0, { dark: true, phone: [pp[0], pp[1] + 0.4, pp[2] + 0.5, 5, 5] });
    const h = kHead();
    D.cam({ p: [[-0.8, 8.6, 6.6], [-2.0, 8.0, 3.8]], l: [h[0] + 0.3, h[1] - 1.5, h[2]], f: h, fov: 40, ap: 3, seed: 12 }, u, d);
  });
  // S13 Three eleven. Three twelve. (the clock)
  shot(26.45, 28.55, (u, d, t) => {
    inBed({ face: "worried" });
    P.clock.set(t < 27.66 ? "3:11" : "3:12");
    D.lights("night", 0, { dark: true, phone: [BED.x + 0.3, 5.8, -6.5, 6, 8] });
    D.cam({ p: [[-2.55, 4.9, -5.3], [-2.4, 4.75, -5.65]], l: [-1.6, 3.1, -8.1], f: [-1.5, 3.23, -8.1], fov: 32, ap: 6, seed: 13 }, u, d);
  });
  // S14 My phone buzzed.
  shot(28.55, 29.6, (u, d, t) => {
    const buzz = t > 28.6 ? 0.7 + 0.3 * Math.max(0, Math.sin(t * 9)) : 0;
    const pp = insert({ screen: "cam", live: true, stamp: stamp(1 + (t - 28.55)), door: 0, frame: Math.floor(t * 12), time: "3:12" }, { buzz, t });
    insertLights(pp, t);
    D.phoneCam(P.phone, { dist: [2.15, 2.0], fov: 46, ly: -0.3, ap: 10, seed: 14, shake: 0.012 }, u, d);
  });
  // S15 But it wasn't the camera. It was my smart lock.
  shot(29.6, 32.55, (u, d, t) => {
    inBed({ face: t < 30.9 ? "worried" : "scared", faceOpts: { sweat: t > 31.2 }, lookUp: 0.18 });
    const pp = phoneInHands({ ...NOTIF_LOCK, notif: 1 });
    D.lights("night", 0, { dark: true, phone: [pp[0], pp[1] + 0.4, pp[2] + 0.6, 5, 5], phoneColor: "#ffd9a8" });
    const h = kHead();
    D.cam({ p: [[h[0] + 3.8, h[1] + 0.4, h[2] + 8.0], [h[0] + 3.0, h[1] + 0.3, h[2] + 6.6]], l: [h[0], h[1] - 1.2, h[2]], f: h, fov: 40, ap: 4, seed: 15 }, u, d);
  });
  // S16 "Front door locked."
  shot(32.55, 34.15, (u, d, t) => {
    const pp = insert({ ...NOTIF_LOCK, notif: clamp((t - 32.6) * 4) });
    insertLights(pp, t);
    D.phoneCam(P.phone, { dist: [2.2, 1.98], fov: 46, ly: -0.3, ap: 10, seed: 16 }, u, d);
  });
  // S17 I never touched it. (the lock turns itself)
  shot(34.15, 35.65, (u, d, t) => {
    const k = ease.inOut(win(t, 34.25, 34.85));
    P.lock.set(k > 0.5, k);
    D.lights("entry", 0, { led: 1, ledColor: k > 0.5 ? "#ff3a2a" : "#3aff6a" });
    const lp = P.lock.pos;
    D.cam({ p: [[lp[0] - 2.3, lp[1] + 0.8, lp[2] - 4.4], [lp[0] - 1.9, lp[1] + 0.65, lp[2] - 3.7]], l: [lp[0] + 0.2, lp[1] - 0.4, lp[2]], f: [lp[0], lp[1], lp[2] - 0.1], fov: 36, ap: 8, seed: 17 }, u, d);
  });
  // S18 Whoever had been leaving every night didn't leave tonight.
  shot(35.65, 38.85, (u, d, t) => {
    P.lock.set(true);
    const sh = stranger(FD.x - 1.2, FD.z - 1.5, 0.15, { armUp: 1 - win(t, 36.2, 37.0), turn: win(t, 37.4, 38.4) * -1.1 });
    D.lights("entry", 0, { led: 1, ledColor: "#ff3a2a", rim: [FD.x + 1.6, 8.5, FD.z - 1.6, 32], boost: 1.3 });
    eyesOn(t > 37.6);
    D.cam({ p: [[HX + 1.0, 7.0, -3.2], [HX + 1.8, 6.6, -1.4]], l: [sh[0] - 0.4, sh[1] - 1.6, sh[2]], f: sh, fov: 44, ap: 3, seed: 18 }, u, d);
  });
  // S19 They locked the door. Not to keep anyone out. (in bed, the bedroom door creaks)
  shot(38.85, 42.15, (u, d, t) => {
    inBed({ face: "scared", faceOpts: { sweat: true }, look: 0.55 * win(t, 39.0, 39.8), lookUp: 0.1 });
    P.bedDoor.rotation.y = -0.16 * win(t, 40.2, 41.6);
    phoneInHands({ ...NOTIF_LOCK, notif: 1 });
    D.lights("night", 0, { dark: true, phone: [BED.x + 0.3, 5.9, -6.0, 5, 5], phoneColor: "#ffd9a8" });
    const h = kHead();
    D.cam({ p: [[h[0] + 3.4, h[1] + 0.4, h[2] + 8.2], [h[0] + 2.8, h[1] + 0.25, h[2] + 6.8]], l: [h[0] - 0.2, h[1] - 1.0, h[2]], f: h, fov: 40, ap: 3, seed: 19 }, u, d);
  });
  // S20 To keep me in. (his eyes: the lock notification in his hand, the bedroom door swings open, the man)
  const _v = new THREE.Vector3(), _r = new THREE.Vector3();
  const ots = (u, d, t, { open = 1, push = 0 } = {}) => {
    inBed({ face: "scared", look: 0.62 });
    const E = kHead();
    E[1] -= 0.25;
    kid.root.visible = false;
    P.bedDoor.rotation.y = -1.25 * open - 0.16 * (1 - open);
    const sh = doorStranger(t);
    const tgt = [sh[0], sh[1] - 1.9, sh[2]];
    _v.set(tgt[0] - E[0], tgt[1] - E[1], tgt[2] - E[2]).normalize();
    _r.set(_v.z, 0, -_v.x).normalize().multiplyScalar(-1);
    const ph = P.phone;
    ph.grip.visible = true;
    ph.group.visible = true;
    const pd = 3.0;
    ph.group.position.set(E[0] + _v.x * pd - _r.x * 0.34, E[1] + _v.y * pd - 0.58, E[2] + _v.z * pd - _r.z * 0.34);
    ph.group.lookAt(E[0], E[1] - 0.2, E[2]);
    ph.group.rotateZ(0.12);
    ph.draw({ ...NOTIF_LOCK, notif: 1 });
    eyesOn(true);
    D.lights("night", 0, { dark: true, hall: 0.3 + 0.7 * open, fill: [ph.group.position.x - _v.x * 0.8, ph.group.position.y + 0.3, ph.group.position.z - _v.z * 0.8, 5], fillColor: "#ffd9a8" });
    W.lights.key.intensity *= 0.45;
    const p0 = [E[0] + _v.x * push * 2.2, E[1] + _v.y * push * 2.2, E[2] + _v.z * push * 2.2];
    D.cam({ p: [E, p0], l: [tgt, tgt], f: sh, fov: 44, ap: 1.2, seed: 20, shake: 0.03 }, u, d);
    return sh;
  };
  shot(42.15, 43.6, (u, d, t) => {
    ots(u, d, t, { open: ease.out(win(t, 42.3, 42.95)) });
  });
  // END CARD: hold on him in the doorway, dimmed under the card
  shot(43.6, 47.0, (u, d, t) => {
    ots(u, d, t, { open: 1, push: 0 });
    G().uFade.value = lerp(0.0, 0.42, win(u, 0, 0.15));
  });

  // COVER (thumbnail still): the lock notification in his hands; the man in the open bedroom door
  shot(200, 210, (u, d, t) => {
    ots(1, 1, 1.0, { open: 1 });
    pipe.scenePass.aperture = 0.25;
  });

  return S;
}
