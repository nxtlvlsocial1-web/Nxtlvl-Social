// Call From Inside the House, shot by shot. Times are seconds on audio/vo.wav (audio/vo-lines.json).
import * as THREE from "three";
import { makeDirector } from "./direct.js";
import { BED, HX, TOP } from "./world.js";
import { ease, win, lerp, lerp3, clamp } from "./util.js";

const PI = Math.PI;
const bump = (u, a, b) => (u <= a || u >= b ? 0 : Math.sin(((u - a) / (b - a)) * PI));
const CX = HX + 2.45, CZ = 3.6; // babysitter on the couch, facing the TV (+x)

export function buildShots(ctx) {
  const D = makeDirector(ctx);
  const { C, W, pipe } = ctx;
  const P = W.props;
  const S = [];
  const shot = (t0, t1, run) => S.push({ t0, t1, run });
  const kid = C.kid, st = C.stranger, ka = C.friendA, kb = C.friendB;

  // ---- posing -----------------------------------------------------------------------
  function sitter({ face = "flat", faceOpts, look = 0, lookUp = 0 } = {}) {
    D.place(kid, CX, 0, CZ, PI / 2);
    D.sit(kid, 1.65);
    kid.j.torso.rotation.x = -0.12;
    kid.setFace(face, faceOpts);
    kid.j.armL.rotation.set(-0.5, 0, 0.1);
    kid.j.armR.rotation.set(-0.5, 0, -0.1);
    kid.j.head.rotation.set(-lookUp, look, 0);
    return kid;
  }
  const kHead = () => D.wpos(kid.j.head, [0, 0.62, 0]);
  // cordless at the sitter's ear (right side)
  function onPhone(lines, lit = true) {
    kid.j.armR.rotation.set(-2.6, 0, -0.42);
    const c = P.cordless;
    c.group.visible = true;
    D.attach(c.group, kid.j.head, [0.9, 0.52, 0.2], [-0.35, -PI / 2, 0]);
    c.set(lines, lit);
  }
  function cradled(lines = ["", ""], lit = false, ring = false) {
    const c = P.cordless;
    c.group.visible = true;
    c.group.position.set(P.cradle[0], P.cradle[1] + 0.45, P.cradle[2]);
    c.group.rotation.set(-0.35, PI / 2 + 0.25, 0);
    c.set(lines, lit);
    c.ring(ring);
  }
  // the cell phone held up in front of the sitter (insert framing, sitter hidden)
  function cell(state, { buzz = 0, t = 0 } = {}) {
    sitter();
    kid.root.visible = false;
    const ph = P.phone;
    ph.grip.visible = true;
    ph.group.visible = true;
    const pos = [CX + 1.35 + Math.sin(t * 90) * 0.025 * buzz, 4.2, CZ + 0.15 + Math.cos(t * 77) * 0.02 * buzz];
    ph.group.position.set(pos[0], pos[1], pos[2]);
    ph.group.lookAt(CX - 1.4, 4.75, CZ + 0.1);
    if (buzz) ph.group.rotateZ(Math.sin(t * 83) * 0.05 * buzz);
    ph.draw(state);
    return pos;
  }
  const cellLights = (pp, t) => {
    D.lights("house", 0, { t, lamp: 0.5, fill: [pp[0] - 0.8, pp[1] + 0.3, pp[2], 10], fillColor: "#b9cdff" });
    pipe.grade.uniforms.uVignette.value = 0.72;
  };
  // the man at the top of the stairs
  function stranger(t, { tilt = 0, lower = 0, step = 0 } = {}) {
    D.place(st, TOP[0], TOP[1] - step * 0.68, TOP[2] + step * 0.62, 0);
    st.root.scale.setScalar(1.12);
    st.setFace("shadow");
    st.j.head.rotation.set(0.15, 0, tilt);
    st.j.armR.rotation.set(lerp(-2.6, -0.4, lower), 0, lerp(-0.42, -0.08, lower));
    st.j.armL.rotation.set(0, 0, 0.05);
    if (step) st.j.legR.rotation.x = -0.5 * bump(step, 0, 1);
    const c = P.strangerPhone;
    c.group.visible = true;
    if (lower < 0.5) D.attach(c.group, st.j.head, [0.9, 0.52, 0.2], [-0.35, -PI / 2, 0]);
    else D.attach(c.group, st.j.handR, [0, -0.3, 0.2], [0.3, 0, 0]);
    c.set(["LINE 2", "TALK"], true);
    return D.wpos(st.j.head, [0, 0.62, 0]);
  }
  function kidsAsleep(t) {
    for (const [k, x] of [[ka, -7.3], [kb, -4.7]]) {
      D.place(k, x, 3.64, -4.75, 0);
      k.root.rotation.x = -PI / 2;
      k.root.scale.setScalar(0.75);
      k.setFace("sleep");
      k.j.head.rotation.y = (x < -6 ? 0.2 : -0.2) + Math.sin(t * 0.6 + x) * 0.03;
    }
    P.blanket.position.set(BED.x + 0.3, 4.05, -4.55);
    P.blanket.scale.set(1.0, 1.0, 0.82);
  }
  const ringing = (t, a) => Math.floor((t - a) * 2.2) % 2 === 0;

  // ==========================================================================
  // S01 hook: the cordless ringing in the dark living room
  shot(0, 4.32, (u, d, t) => {
    cradled(["UNKNOWN", "CALLER"], true, ringing(t, 0));
    D.lights("house", 0, { t, lamp: 0.55 });
    const c = P.cradle;
    D.cam({ p: [[c[0] + 2.6, c[1] + 1.4, c[2] + 2.4], [c[0] + 1.6, c[1] + 0.8, c[2] + 1.4]], l: [c[0] - 0.4, c[1] + 0.2, c[2] - 0.6], f: [c[0], c[1] + 0.4, c[2]], fov: 40, ap: 6, seed: 1 }, u, d);
  });
  // S02a I was babysitting two kids.
  shot(4.32, 6.1, (u, d, t) => {
    sitter({ face: "smile" });
    cradled();
    D.lights("house", 0, { t });
    D.cam({ p: [[HX + 8.2, 5.8, 2.4], [HX + 7.6, 5.6, 2.8]], l: [CX - 0.4, 4.2, CZ - 0.4], f: [CX, 4.7, CZ], fov: 46, ap: 2.5, seed: 2 }, u, d);
  });
  // S02b …They were asleep upstairs by eight.
  shot(6.1, 8.28, (u, d, t) => {
    kidsAsleep(t);
    P.clock.set("8:47");
    D.lights("night", 0, { dark: true, fill: [-4, 9, -1, 26], fillColor: "#8fa6e6" });
    D.cam({ p: [[-3.4, 7.8, -3.6], [-3.7, 7.4, -4.1]], l: [-6.0, 3.7, -8.2], f: [-6.0, 4.0, -8.3], fov: 44, ap: 3, seed: 3 }, u, d);
  });
  // S03 At nine, the house phone rang. A man laughed, and hung up.
  shot(8.28, 12.15, (u, d, t) => {
    const picked = t > 9.55, hung = t > 11.45;
    sitter({ face: picked ? (hung ? "worried" : "flat") : "flat", look: picked ? 0 : 0.6 });
    P.setClock(9, 0);
    if (picked && !hung) onPhone(["CALL", "00:0" + Math.min(9, Math.floor(t - 9.55))]);
    else cradled(hung ? ["", ""] : ["UNKNOWN", "CALLER"], !hung, !picked && ringing(t, 8.3));
    D.lights("house", 0, { t });
    const h = kHead();
    D.cam({ p: [[h[0] + 5.2, h[1] + 0.5, h[2] - 1.9], [h[0] + 4.6, h[1] + 0.4, h[2] - 1.6]], l: [h[0], h[1] - 0.45, h[2] + 0.3], f: h, fov: 40, ap: 5, seed: 4 }, u, d);
  });
  // S04a At ten… (the clock)
  shot(12.15, 13.1, (u, d, t) => {
    P.setClock(10, Math.min(0, (t - 12.6) * 2));
    sitter({ face: "worried" });
    cradled(["UNKNOWN", "CALLER"], true, ringing(t, 12.2));
    D.lights("house", 0, { t });
    D.cam({ p: [[HX + 7.6, 7.6, 3.4], [HX + 8.0, 7.6, 3.3]], l: [HX + 11.95, 7.3, 3.0], f: [HX + 11.95, 8.0, 3.0], fov: 36, ap: 9, seed: 5 }, u, d);
  });
  // S04b …it rang again. He whispered,
  shot(13.1, 14.63, (u, d, t) => {
    sitter({ face: "worried" });
    P.setClock(10, 0);
    if (t > 13.6) onPhone(["CALL", "00:01"]);
    else cradled(["UNKNOWN", "CALLER"], true, ringing(t, 13.1));
    D.lights("house", 0, { t });
    const h = kHead();
    D.cam({ p: [[h[0] + 4.6, h[1] + 0.4, h[2] - 1.6], [h[0] + 4.1, h[1] + 0.35, h[2] - 1.4]], l: [h[0], h[1] - 0.45, h[2] + 0.3], f: h, fov: 40, ap: 5, seed: 6 }, u, d);
  });
  // S05 "Have you checked the children?"
  shot(14.63, 17.12, (u, d, t) => {
    sitter({ face: "scared", faceOpts: { sweat: true }, lookUp: win(t, 16.0, 16.8) * 0.35 });
    onPhone(["CALL", "00:04"]);
    D.lights("house", 0, { t });
    const h = kHead();
    D.cam({ p: [[h[0] + 3.9, h[1] + 0.35, h[2] - 1.3], [h[0] + 3.4, h[1] + 0.3, h[2] - 1.1]], l: [h[0], h[1] - 0.4, h[2] + 0.25], f: h, fov: 38, ap: 7, seed: 7 }, u, d);
  });
  // S06 I called the police… keep him on the line. We'll trace it.
  shot(17.12, 22.32, (u, d, t) => {
    const active = t > 18.6;
    const pp = cell({ screen: "call", outgoing: !active, active, name1: active ? "Police" : "911", name2: active ? "Dispatch" : "", sub: "calling…", icon: active ? "badge" : "dial", secs: (t - 18.6), time: "10:02" });
    cellLights(pp, t);
    D.phoneCam(P.phone, { dist: [2.6, 2.35], fov: 46, ly: -0.36, ap: 10, seed: 8 }, u, d);
  });
  // S07 He called again.
  shot(22.32, 23.79, (u, d, t) => {
    cradled(["UNKNOWN", "CALLER"], true, ringing(t, 22.35));
    D.lights("house", 0, { t, lamp: 0.7 });
    const c = P.cradle;
    D.cam({ p: [[c[0] + 1.6, c[1] + 0.9, c[2] + 1.5], [c[0] + 1.3, c[1] + 0.75, c[2] + 1.2]], l: [c[0], c[1] + 0.35, c[2]], f: [c[0], c[1] + 0.4, c[2]], fov: 38, ap: 8, seed: 9, shake: 0.02 }, u, d);
  });
  // S08 "Have you checked the children?" (wide: the dark staircase behind her)
  shot(23.79, 26.45, (u, d, t) => {
    sitter({ face: "scared" });
    onPhone(["CALL", "00:03"]);
    D.lights("house", 0, { t });
    D.cam({ p: [[HX + 9.6, 7.0, 5.6], [HX + 9.2, 6.9, 5.2]], l: [HX - 1.6, 6.2, 0.6], f: [CX, 4.7, CZ], fov: 54, ap: 1.8, seed: 10 }, u, d);
  });
  // S09 I kept him talking for a whole minute. (the call timer)
  shot(26.45, 28.8, (u, d, t) => {
    sitter({ face: "worried" });
    const secs = Math.min(60, 52 + Math.floor((t - 26.45) * 3.6));
    const c = P.cordless;
    kid.root.visible = false;
    c.group.visible = true;
    c.group.position.set(CX + 1.3, 4.3, CZ);
    c.group.lookAt(CX - 1.0, 4.9, CZ);
    c.set(["CALL", (secs >= 60 ? "01:00" : "00:" + secs)], true);
    D.lights("house", 0, { t, lamp: 0.5, fill: [CX + 0.6, 4.6, CZ, 6], fillColor: "#c8ffb0" });
    const g = c.group.position;
    D.cam({ p: [[CX - 0.2, 4.95, CZ + 0.05], [CX + 0.15, 4.85, CZ + 0.03]], l: [g.x, g.y + 0.25, g.z], f: [g.x, g.y + 0.3, g.z], fov: 30, ap: 10, seed: 11 }, u, d);
  });
  // S10 Then my cell phone buzzed. It was the police.
  shot(28.8, 31.7, (u, d, t) => {
    const buzz = t > 28.85 ? 0.6 + 0.4 * Math.max(0, Math.sin(t * 9)) : 0;
    const pp = cell({ screen: "call", name1: "Police", name2: "Dispatch", icon: "badge", ph: t * 0.9, time: "10:04" }, { buzz, t });
    cellLights(pp, t);
    D.phoneCam(P.phone, { dist: [2.55, 2.3], fov: 46, ly: -0.36, ap: 10, seed: 12, shake: 0.012 }, u, d);
  });
  // S11 Get out of the house. Now. The calls are coming from inside the house.
  shot(31.7, 35.34, (u, d, t) => {
    sitter({ face: "shock", faceOpts: { sweat: true } });
    kid.j.armL.rotation.set(-2.6, 0, 0.42);
    const ph = P.phone;
    ph.group.visible = true;
    D.attach(ph.group, kid.j.head, [-0.9, 0.52, 0.2], [-0.3, PI / 2, 0]);
    ph.draw({ screen: "call", active: true, name1: "Police", name2: "Dispatch", icon: "badge", secs: 3 + (t - 31.7), time: "10:04" });
    cradled();
    D.lights("house", 0, { t, tv: 0.6 });
    const h = kHead();
    D.cam({ p: [[h[0] + 4.2, h[1] + 0.35, h[2] + 0.4], [h[0] + 3.4, h[1] + 0.3, h[2] + 0.3]], l: [h[0], h[1] - 0.4, h[2]], f: h, fov: 38, ap: 7, seed: 13 }, u, d);
  });
  // S12 From the phone upstairs. (the caller ID)
  shot(35.34, 37.17, (u, d, t) => {
    const c = P.cordless;
    c.group.visible = true;
    c.group.position.set(CX + 1.3, 4.3, CZ);
    c.group.lookAt(CX - 1.0, 4.9, CZ);
    const blink = ((t - 35.34) * 2.5) % 1 < 0.72;
    c.set(blink ? ["LINE 2", "UPSTAIRS"] : ["LINE 2", ""], true);
    sitter();
    kid.root.visible = false;
    D.lights("house", 0, { t, lamp: 0.5, fill: [CX + 0.6, 4.6, CZ, 6], fillColor: "#c8ffb0" });
    const g = c.group.position;
    D.cam({ p: [[CX - 0.3, 4.95, CZ + 0.05], [CX - 0.05, 4.9, CZ + 0.04]], l: [g.x, g.y + 0.2, g.z], f: [g.x, g.y + 0.32, g.z], fov: 30, ap: 10, seed: 14, shake: 0.015 }, u, d);
  });
  // S13 I looked up the stairs.
  shot(37.17, 38.97, (u, d, t) => {
    D.place(kid, HX - 4.4, 0, 6.2, Math.atan2(TOP[0] - (HX - 4.4), TOP[2] - 6.2));
    kid.setFace("scared", { sweat: true });
    kid.j.head.rotation.x = -0.45 * win(t, 37.3, 38.2);
    D.lights("house", 0, { t });
    const h = kHead();
    D.cam({ p: [[h[0] + 3.6, h[1] - 1.6, h[2] + 2.9], [h[0] + 3.3, h[1] - 1.7, h[2] + 2.6]], l: [TOP[0] + 1.2, TOP[1] - 0.5, TOP[2] + 1.6], f: h, fov: 50, ap: 2.5, seed: 15 }, u, d);
  });
  // S14 Someone was standing at the top. Still holding the phone.
  shot(38.97, 42.93, (u, d, t) => {
    const sh = stranger(t);
    D.lights("house", 0, { t, night: 1.2 });
    D.cam({ p: [[HX - 6.4, 3.4, 9.2], [HX - 7.2, 4.6, 6.6]], l: [sh[0], sh[1] - 1.2, sh[2]], f: sh, fov: 40, ap: 3, seed: 16 }, u, d);
  });
  // S15 "Have you checked the children?" (from the top of the stairs, for real; he comes down)
  shot(42.93, 45.8, (u, d, t) => {
    const sh = stranger(t, { tilt: win(t, 43.0, 43.7) * 0.3, lower: win(t, 44.3, 44.9), step: win(t, 44.9, 45.6) });
    D.lights("house", 0, { t, night: 1.2 });
    D.cam({ p: [[HX - 7.6, 6.2, 4.6], [HX - 8.2, 7.0, 3.2]], l: [sh[0], sh[1] - 0.6, sh[2]], f: sh, fov: 36, ap: 4, seed: 17, shake: 0.02 }, u, d);
    pipe.grade.uniforms.uFade.value = win(t, 45.55, 45.8);
  });
  // END CARD: the empty stairs, the glow from the kids' door
  shot(45.8, 48.9, (u, d, t) => {
    D.lights("house", 0, { t, night: 1.2 });
    D.cam({ p: [[HX - 6.0, 4.0, 9.0], [HX - 6.3, 4.3, 8.4]], l: [TOP[0] + 1.5, TOP[1] - 0.5, TOP[2] + 1.0], f: [TOP[0], TOP[1] + 2, TOP[2]], fov: 44, ap: 3, seed: 18 }, u, d);
    pipe.grade.uniforms.uFade.value = lerp(1, 0.35, win(u, 0, 0.12));
  });

  // COVER (thumbnail still): she's on the phone, terrified; he's at the top of the stairs, on the phone too
  shot(200, 210, (u, d, t) => {
    sitter({ face: "scared", faceOpts: { sweat: true }, look: 0.25 });
    onPhone(["LINE 2", "UPSTAIRS"]);
    stranger(1.3);
    D.lights("house", 0, { t: 1.3, night: 1.4 });
    D.cam({ p: [HX + 9.6, 5.5, 5.6], l: [HX + 0.7, 7.95, 1.76], f: kHead(), fov: 56, ap: 0.8, shake: 0, seed: 99 }, 0, 1);
  });

  return S;
}
