// Two True Stories: The Watcher & The Enfield Poltergeist — shot by shot (landscape, 1920x1080).
// Times are seconds on audio/vo.wav (audio/vo-lines.json). Every shot is pure in (u, d, t).
import * as THREE from "three";
import { makeDirector } from "./direct.js";
import { HX, BED } from "./world.js";
import { WX, DESK, EX, EB, EL, GLOBE, DIO, NJ, LDN, lonLat } from "./sets.js";
import { ease, win, lerp, lerp3, clamp } from "./util.js";

const PI = Math.PI;
const bump = (u, a, b) => (u <= a || u >= b ? 0 : Math.sin(((u - a) / (b - a)) * PI));
const w = (x, y, z) => [WX + x, y, z];
const hx = (x, y, z) => [HX + x, y, z];
const dk = (x, y, z) => [DESK[0] + x, DESK[1] + y, DESK[2] + z];
const eo = (x, y, z) => [EX + x, y, z];
const eb = (x, y, z) => [EB[0] + x, y, EB[2] + z];
const el = (x, y, z) => [EL[0] + x, y, EL[2] + z];
const dio = (x, y, z) => [DIO[0] + x, DIO[1] + y, DIO[2] + z];

// the letters (only phrases widely reported from the real letters)
const L1 = ["Dearest new neighbor at 657 Boulevard,", "Allow me to welcome you to the neighborhood."];
const L2 = ["657 Boulevard has been the subject of my family for decades now."];
const L3 = ["My grandfather watched the house in the 1920s. My father watched in the 1960s. It is now my time."];
const L4 = ["Do you know what lies within the walls of 657 Boulevard?"];
const L5 = ["Who has the bedrooms facing the street? I'll know as soon as you move in."];

export function buildShots(ctx) {
  const D = makeDirector(ctx);
  const { C, W, pipe } = ctx;
  const P = W.props;
  const PR = P.props2;
  const G = () => pipe.grade.uniforms;
  const S = [];
  const shot = (t0, t1, run) => S.push({ t0, t1, run });
  const on = (...n) => n.forEach((k) => (P.sets[k].visible = true));
  const cam = (o, u, d) => D.cam({ ap: 0, shake: 0.03, ...o }, u, d);
  const head = (av) => D.wpos(av.j.head, [0, 0.62, 0]);

  // ---- people --------------------------------------------------------------------
  function stand(av, pos, ry, { face, scale = 1, t = null, outfit } = {}) {
    D.place(av, pos[0], pos[1] || 0, pos[2], ry);
    av.root.scale.setScalar(scale);
    if (outfit) av.setOutfit(outfit);
    if (face) av.setFace(face);
    if (t !== null) D.idle(av, t);
    return av;
  }
  function walkTo(av, a, b, k, t, { scale = 1, face, speed = 7, outfit } = {}) {
    const p = lerp3(a, b, clamp(k));
    stand(av, p, Math.atan2(b[0] - a[0], b[2] - a[2]), { face, scale, outfit });
    if (k > 0 && k < 1) D.walk(av, t * speed, 0.55);
    return av;
  }
  function lie(av, pos, { face = "sleep", scale = 0.75, outfit } = {}) {
    stand(av, pos, 0, { face, scale, outfit });
    av.root.rotation.x = -PI / 2;
    return av;
  }
  const holdUp = (av, side = "R", k = 1) => av.j["arm" + side].rotation.set(-1.2 * k, 0, side === "R" ? -0.2 * k : 0.2 * k);
  const family = (t, at = w(0, 0, 14), ry = PI) => {
    stand(C.dad, [at[0] - 1.6, 0, at[2]], ry, { face: "smile", t });
    stand(C.mom, [at[0] + 1.6, 0, at[2]], ry, { face: "momSmile", t: t + 1 });
    stand(C.kid, [at[0] - 4.2, 0, at[2] + 0.8], ry, { face: "smile", scale: 0.78, outfit: "hoodie", t: t + 2 });
    stand(C.sister, [at[0] + 4.0, 0, at[2] + 0.6], ry, { face: "smile", scale: 0.72, t: t + 3 });
    stand(C.friendA, [at[0] + 0.1, 0, at[2] + 1.6], ry, { face: "smile", scale: 0.6, t: t + 4 });
  };
  // ---- the letter desk ------------------------------------------------------------
  function letter(lines, k, { sign = false } = {}) {
    on("desk");
    const total = lines.join(" ").length;
    P.desk.drawLetter(lines, Math.floor(total * clamp(k)) + (k >= 1 ? 999 : 0), { sign });
  }
  const letterCam = (u, d, { push = 0.6, ox = 0 } = {}) => {
    const c = P.desk.letter.position;
    const base = dk(0.4 + ox, 3.27, 0.2);
    cam({ p: [[base[0] - 0.3, base[1] + 5.6, base[2] + 3.6], [base[0] - 0.1, base[1] + 5.6 - push * 2.4, base[2] + 3.6 - push * 1.6]], l: [base, [base[0], base[1], base[2] - 0.3]], f: base, fov: 38, ap: 3, shake: 0.015 }, u, d);
  };
  // ---- grading looks ---------------------------------------------------------------
  const sepia = () => {
    const g = G();
    g.uSat.value = 0.12;
    g.uGain.value.set(1.14, 0.98, 0.76);
    g.uLift.value.set(0.04, 0.03, 0.0);
    g.uGrain.value = 0.12;
    g.uVignette.value = 0.85;
  };
  const sixties = () => {
    const g = G();
    g.uSat.value = 0.55;
    g.uGain.value.set(1.1, 1.0, 0.84);
    g.uLift.value.set(0.03, 0.02, 0.0);
    g.uGrain.value = 0.09;
    g.uVignette.value = 0.7;
  };
  const fadeIn = (u, len = 0.5) => (G().uFade.value = 1 - clamp(u / len));
  const fadeOut = (u, d, len = 0.5) => (G().uFade.value = Math.max(G().uFade.value, clamp((u - (d - len)) / len)));

  // =====================================================================================
  // COLD OPEN
  // S001 In June 2014, a family bought their dream house in New Jersey.
  shot(0, 5.25, (u, d, t) => {
    on("watcher");
    D.lights("w_day");
    family(t, w(0, 0, 16));
    cam({ p: [[WX + 2, 4.5, 30], [WX + 1, 9, 36]], l: [[WX, 5, 10], [WX, 9, 0]], fov: 42 }, u, d);
    fadeIn(u, 0.8);
  });
  // S002 Days later, a letter arrived.
  shot(5.25, 7.4, (u, d, t) => {
    on("watcher");
    D.lights("w_dusk");
    P.wb.mailEnv.visible = true;
    P.wb.mailbox.door.rotation.x = -1.35 * win(u, 0.4, 1.4);
    P.wb.mailbox.flag.rotation.z = 0;
    const m = P.wb.mailbox.pos;
    cam({ p: [[m[0] - 3.2, m[1] + 1.4, m[2] - 6.4], [m[0] - 2.4, m[1] + 0.9, m[2] - 5.0]], l: [m[0], m[1] - 0.2, m[2] - 0.6], f: [m[0], m[1], m[2] - 1], fov: 34, ap: 4 }, u, d);
  });
  // S003 It was addressed to "The New Owner."
  shot(7.4, 9.55, (u, d, t) => {
    on("desk");
    D.lights("desk");
    const e = dk(-3.2, 3.28, 1.2);
    cam({ p: [[e[0] + 0.6, e[1] + 4.6, e[2] + 2.4], [e[0] + 0.3, e[1] + 3.2, e[2] + 1.5]], l: [e, e], f: e, fov: 36, ap: 3, shake: 0.012 }, u, d);
  });
  // S004 And it was signed... The Watcher.
  shot(9.55, 12.3, (u, d, t) => {
    letter(L2, 1, { sign: true });
    D.lights("desk", 0, { lamp: 1 - 0.5 * win(t, 11.0, 11.6) });
    const b = dk(0.75, 3.27, 1.3);
    cam({ p: [[b[0] + 0.2, b[1] + 3.6, b[2] + 2.4], [b[0] + 0.1, b[1] + 2.0, b[2] + 1.3]], l: [b, b], f: b, fov: 36, ap: 3, shake: 0.012 }, u, d);
  });
  // S005 Thirty-seven years earlier, in north London,
  shot(12.3, 15.4, (u, d, t) => {
    on("enfOut");
    D.lights("uk_night", 0, { lit: 1 });
    cam({ p: [[EX + 10, 4, 38], [EX + 6, 5, 32]], l: [[EX - 3, 6, 0], [EX - 4, 7, 0]], fov: 40 }, u, d);
    fadeIn(u, 0.4);
  });
  // S006 a mother called the police,
  shot(15.4, 17.6, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live", 0, { lamp: 0.8 });
    stand(C.peggy, el(-7.4, 0, 3.4), PI / 2 - 0.35, { face: "worried", t });
    C.peggy.j.armL.rotation.set(-2.5, 0, 0.5);
    P.handset70.visible = false;
    PR.handset.visible = true;
    D.attach(PR.handset, C.peggy.j.head, [-0.85, 0.5, 0.3], [0, 0, PI / 2]);
    const h = head(C.peggy);
    cam({ p: [[h[0] + 7.5, h[1] + 0.4, h[2] + 2.6], [h[0] + 6.6, h[1] + 0.3, h[2] + 2.2]], l: [h[0], h[1] - 1.0, h[2]], f: h, fov: 36, ap: 2 }, u, d);
  });
  // S007 because the furniture in her house was moving. By itself.
  shot(17.6, 21.0, (u, d, t) => {
    on("enfBed");
    D.lights("enf_bed", 0, {});
    const k = ease.inOut(win(t, 18.9, 20.6));
    P.chest.position.set(-0.8 * k + Math.sin(t * 40) * 0.03 * bump(t, 18.9, 20.6), 0, -6.6 + 3.2 * k);
    P.chest.rotation.y = 0.25 * k;
    cam({ p: [[EB[0] + 1.5, 4.8, EB[2] + 6.5], [EB[0] + 1.2, 4.3, EB[2] + 5.2]], l: [EB[0] - 0.4, 2.0, EB[2] - 4.6], fov: 44, ap: 2, shake: 0.02 }, u, d);
  });
  // S008 Both of these stories are real.
  shot(21.0, 23.3, (u, d, t) => {
    on("watcher");
    D.lights("w_night");
    P.wb.win[5].emissiveIntensity = 1.4;
    cam({ p: [[WX - 8, 5, 44], [WX - 6, 6, 38]], l: [WX, 11, 0], fov: 40 }, u, d);
  });
  // S009 And both are still unexplained.
  shot(23.3, 25.7, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live", 0, { lamp: 0.25, corner: 0.8 });
    const c = el(-8.2, 2.4, -6.2);
    cam({ p: [[c[0] + 7.5, 5.5, c[2] + 7.5], [c[0] + 6.0, 4.8, c[2] + 6.0]], l: c, f: c, fov: 38, ap: 2 }, u, d);
  });
  // S010 Stay until the end... where you're watching from. (the globe, both pins)
  shot(25.7, 31.6, (u, d, t) => {
    on("globe");
    D.lights("globe");
    P.arc.geometry.setDrawRange(0, Math.floor(P.arcCount * win(t, 27.0, 30.5)));
    const lon = lerp(-60, -30, win(u, 0, d)), lat = 38;
    const c = lonLat(lon, lat, 30);
    cam({ p: [GLOBE[0] + c.x, GLOBE[1] + c.y, GLOBE[2] + c.z], l: [GLOBE[0], GLOBE[1] + 2, GLOBE[2]], fov: 38, shake: 0.01 }, 0, 1);
  });
  // S011 title card over the two models (dim)
  shot(31.6, 35.2, (u, d, t) => {
    on("dio");
    P.dioWatcher.visible = P.dioEnfield.visible = true;
    D.lights("dio", 0, { spot: 0.5 });
    cam({ p: [dio(-6, 12, 40), dio(4, 12, 38)], l: dio(0, 4, 0), fov: 38, shake: 0.01 }, u, d);
    G().uFade.value = 0.5;
  });

  // =====================================================================================
  // CHAPTER ONE: THE WATCHER
  // S012 chapter card: the house at dusk
  shot(35.2, 38.3, (u, d, t) => {
    on("watcher");
    D.lights("w_dusk");
    cam({ p: [[WX - 24, 7, 52], [WX - 18, 8, 48]], l: [WX, 11, 0], fov: 42 }, u, d);
    G().uFade.value = 0.45;
  });
  // S013 Westfield... Big old trees.
  shot(38.3, 42.0, (u, d, t) => {
    on("watcher");
    D.lights("w_day");
    cam({ p: [[WX - 50, 6, 28], [WX - 36, 6, 28.5]], l: [[WX - 20, 6, 30], [WX - 6, 7, 30]], fov: 44 }, u, d);
  });
  // S014 Quiet streets. Good schools.
  shot(42.0, 45.95, (u, d, t) => {
    on("watcher");
    D.lights("w_day");
    walkTo(C.kid, w(-30, 0, 27.3), w(-12, 0, 27.3), win(t, 42.0, 45.9, (x) => x), t, { scale: 0.78, outfit: "hoodie", face: "smile" });
    cam({ p: [[WX + 6, 3.2, 44], [WX + 2, 3.6, 44.5]], l: [[WX - 20, 4, 26], [WX - 14, 4.5, 26]], fov: 36 }, u, d);
  });
  // S015 In 2014, Derek and Maria Broaddus bought a six-bedroom house there,
  shot(45.95, 50.6, (u, d, t) => {
    on("watcher");
    D.lights("w_day");
    P.wb.sale.visible = true;
    P.wb.saleM.map = P.wb.saleTex.sold;
    stand(C.dad, w(-2, 0, 17), 0.2, { face: "smile", t });
    stand(C.mom, w(1.5, 0, 17.4), -0.2, { face: "momSmile", t: t + 1 });
    C.dad.j.armL.rotation.set(-0.3, 0, 0.4);
    const h = head(C.dad);
    cam({ p: [[WX - 0.2, 6.2, 31], [WX - 0.2, 6.6, 28]], l: [[WX, 5.4, 14], [WX, 6.4, 10]], f: h, fov: 40, ap: 1.5 }, u, d);
  });
  // S016 at 657 Boulevard, for about $1.3 million. (crane up the facade)
  shot(50.6, 56.8, (u, d, t) => {
    on("watcher");
    D.lights("w_day");
    cam({ p: [[WX + 6, 3, 22], [WX + 4, 16, 26]], l: [[WX, 6, 0], [WX, 17, 0]], fov: 40, shake: 0.015 }, u, d);
  });
  // S017 They had three young kids. This was the house they were going to grow up in.
  shot(56.8, 61.6, (u, d, t) => {
    on("watcher");
    D.lights("w_day");
    const r = (ph, R) => w(Math.cos(ph) * R, 0, 13 + Math.sin(ph) * R * 0.6);
    const a = t * 0.9;
    for (const [av, off, sc] of [[C.kid, 0, 0.78], [C.sister, 2.1, 0.72], [C.friendA, 4.2, 0.6]]) {
      const p0 = r(a + off, 5), p1 = r(a + off + 0.05, 5);
      stand(av, p0, Math.atan2(p1[0] - p0[0], p1[2] - p0[2]), { face: "smile", scale: sc, outfit: av === C.kid ? "hoodie" : undefined });
      D.walk(av, t * 9 + off, 0.7);
    }
    stand(C.mom, w(-6, 0, 6), 0.5, { face: "momSmile", t });
    stand(C.dad, w(-4.4, 0, 5.4), 0.6, { face: "smile", t: t + 1 });
    cam({ p: [[WX + 14, 7, 30], [WX + 10, 7.5, 28]], l: [WX - 1, 3, 11], fov: 40, ap: 1 }, u, d);
  });
  // S018 Before moving in, Derek spent his days at the house, fixing it up.
  shot(61.6, 65.4, (u, d, t) => {
    on("house");
    P.reno.visible = true;
    D.lights("reno");
    stand(C.dad, hx(6.2, 0, -7.0), PI, { face: "flat" });
    const s = Math.sin(t * 4.2);
    C.dad.j.armR.rotation.set(-2.4 + s * 0.35, 0, -0.15);
    P.roller.visible = true;
    D.attach(P.roller, C.dad.j.handR, [0, 0.2, 0.3], [0.4, 0, 0]);
    cam({ p: [[HX + 1.0, 6.4, -1.0], [HX + 1.8, 6.0, -2.2]], l: [HX + 6.4, 4.6, -8.2], fov: 42, ap: 1.5 }, u, d);
  });
  // S019 One evening, he checked the mailbox.
  shot(65.4, 68.35, (u, d, t) => {
    on("watcher");
    D.lights("w_dusk");
    walkTo(C.dad, w(0.6, 0, 6), w(5.0, 0, 23.2), win(t, 65.5, 68.2, (x) => x), t, { face: "flat" });
    cam({ p: [[WX + 16, 5, 30], [WX + 14, 5, 31]], l: [[WX + 2, 4, 12], [WX + 5, 4, 21]], fov: 40 }, u, d);
  });
  // S020 Inside was an envelope,
  shot(68.35, 70.2, (u, d, t) => {
    on("watcher");
    D.lights("w_dusk");
    stand(C.dad, w(5.4, 0, 23.0), 0, { face: "flat" });
    C.dad.j.armR.rotation.set(-1.45, 0, -0.1);
    P.wb.mailbox.door.rotation.x = -1.35;
    P.wb.mailEnv.visible = u < 1.0;
    const m = P.wb.mailbox.pos;
    cam({ p: [[m[0] + 7.5, m[1] + 0.8, m[2] - 1.2], [m[0] + 6.4, m[1] + 0.6, m[2] - 1.4]], l: [m[0] - 0.4, m[1] - 0.4, m[2] - 1.2], fov: 38, ap: 2 }, u, d);
  });
  // S021 addressed to "The New Owner."
  shot(70.2, 72.1, (u, d, t) => {
    on("watcher");
    D.lights("w_dusk");
    stand(C.dad, w(5.4, 0, 22.6), PI - 0.3, { face: "worried" });
    C.dad.j.armR.rotation.set(-1.25, 0, 0.15);
    C.dad.j.head.rotation.x = 0.35;
    PR.env.visible = true;
    D.attach(PR.env, C.dad.j.handR, [0.1, -0.2, 0.5], [-PI / 2 + 0.5, 0, 0]);
    const h = head(C.dad);
    cam({ p: [[h[0] - 3.6, h[1] + 0.2, h[2] - 7.4], [h[0] - 3.0, h[1] + 0.1, h[2] - 6.4]], l: [h[0] - 0.2, h[1] - 1.6, h[2]], f: h, fov: 40, ap: 1.5 }, u, d);
  });
  // S022 The letter started out friendly. Welcome to the neighborhood. Then, it changed.
  shot(72.1, 77.5, (u, d, t) => {
    letter(L1, win(t, 72.4, 76.0, (x) => x));
    D.lights("desk", 0, { lamp: 1 - 0.55 * win(t, 76.2, 76.8) });
    letterCam(u, d, { push: 0.4 });
  });
  // S023 "657 Boulevard has been the subject of my family for decades now."
  shot(77.5, 83.15, (u, d, t) => {
    letter(L2, win(t, 77.9, 82.9, (x) => x));
    D.lights("desk", 0, { lamp: 0.5 });
    letterCam(u, d, { push: 0.7 });
  });
  // S024 "My grandfather watched the house in the 1920s." (sepia)
  shot(83.15, 86.9, (u, d, t) => {
    on("watcher");
    D.lights("w_day");
    sepia();
    ctx.hud = { mode: "year", text: "1920s", k: win(u, 0, 0.4) };
    cam({ p: [[WX - 6, 6, 50], [WX - 5, 6.4, 46]], l: [WX, 10, 0], fov: 40, shake: 0.02 }, u, d);
  });
  // S025 "My father watched in the 1960s." (faded colour)
  shot(86.9, 89.0, (u, d, t) => {
    on("watcher");
    D.lights("w_dusk");
    sixties();
    ctx.hud = { mode: "year", text: "1960s", k: win(u, 0, 0.4) };
    cam({ p: [[WX + 20, 5, 48], [WX + 18, 5.5, 45]], l: [WX, 10, 0], fov: 40, shake: 0.02 }, u, d);
  });
  // S026 "It is now my time." (now: night, from across the street)
  shot(89.0, 91.0, (u, d, t) => {
    on("watcher");
    D.lights("w_night");
    cam({ p: [[WX + 30, 9, 62], [WX + 30, 9, 60]], l: [WX, 10, 0], fov: 30, shake: 0.02 }, u, d);
  });
  // S027 "Do you know what lies within the walls of 657 Boulevard?"
  shot(91.0, 95.6, (u, d, t) => {
    on("house");
    P.reno.visible = true;
    D.lights("entry", 0, {});
    G().uSat.value = 0.6;
    G().uVignette.value = 0.85;
    cam({ p: [[HX + 1.0, 6.0, 4.0], [HX + 4.6, 5.0, -4.8]], l: [[HX + 6, 4.2, -10], [HX + 6.2, 4.0, -10]], fov: 44, ap: 1.5, shake: 0.02 }, u, d);
  });
  // S028 It was signed, "The Watcher."
  shot(95.6, 97.8, (u, d, t) => {
    letter(L4, 1, { sign: true });
    D.lights("desk", 0, { lamp: 0.55 });
    const b = dk(0.75, 3.27, 1.3);
    cam({ p: [[b[0] + 0.1, b[1] + 3.0, b[2] + 2.0], [b[0], b[1] + 2.0, b[2] + 1.3]], l: [b, b], f: b, fov: 36, ap: 3, shake: 0.012 }, u, d);
  });
  // S029 Derek called the police.
  shot(97.8, 99.7, (u, d, t) => {
    on("watcher");
    D.lights("w_night");
    const c = PR.cruiser;
    c.group.visible = true;
    c.group.position.set(WX + 10, 0, 33.2);
    c.group.rotation.y = PI / 2;
    const ph = Math.floor(t * 6) % 2;
    c.red.color.set("#ff2a2a").multiplyScalar(ph ? 4 : 0.3);
    c.blue.color.set("#2a6aff").multiplyScalar(ph ? 0.3 : 4);
    const L = W.lights.glows;
    L[2].color.set(ph ? "#ff3030" : "#3060ff"); L[2].decay = 2; L[2].distance = 0;
    L[2].position.set(WX + 10, 5.5, 33.2); L[2].intensity = 120;
    stand(C.cop, w(1.6, 1.4, 3.6), PI, { face: "flat", t });
    stand(C.dad, w(-0.6, 1.4, 2.0), 0.3, { face: "worried", t: t + 1 });
    holdUp(C.dad, "R", 0.8);
    PR.paper.visible = true;
    D.attach(PR.paper, C.dad.j.handR, [0, -0.3, 0.45], [-0.3, 0, 0]);
    cam({ p: [[WX + 6, 5.5, 18], [WX + 5, 5.2, 16]], l: [WX + 0.5, 4.6, 2.6], fov: 40, ap: 1.5 }, u, d);
  });
  // S030 The family told themselves it was a prank.
  shot(99.7, 102.6, (u, d, t) => {
    on("house");
    D.lights("reno", 0, { eve: 1 });
    stand(C.dad, hx(3.6, 0, 1.6), PI / 2 + 0.4, { face: "worried", t });
    stand(C.mom, hx(7.2, 0, 2.6), -PI / 2 - 0.3, { face: "momSmile", t: t + 1 });
    C.mom.setFace("worried");
    holdUp(C.dad, "R", 0.7);
    PR.paper.visible = true;
    D.attach(PR.paper, C.dad.j.handR, [0, -0.3, 0.45], [-0.3, 0, 0]);
    cam({ p: [[HX + 5.4, 6.4, 9.2], [HX + 5.4, 6.2, 8.4]], l: [HX + 5.4, 4.6, 2.0], fov: 44, ap: 1.2 }, u, d);
  });
  // S031 A bored neighbor. Someone with a sick sense of humor. (the houses across the street)
  shot(102.6, 106.05, (u, d, t) => {
    on("watcher");
    D.lights("w_dusk");
    cam({ p: [[WX - 4, 5, 22], [WX + 8, 5, 22]], l: [[WX - 30, 8, 64], [WX + 30, 8, 64]], fov: 34 }, u, d);
  });
  // S032 Then, about two weeks later, a second letter arrived.
  shot(106.05, 109.75, (u, d, t) => {
    on("watcher");
    D.lights("w_day");
    P.wb.mailEnv.visible = true;
    P.wb.mailbox.flag.rotation.z = -PI / 2 * (1 - win(t, 107.0, 107.6));
    P.wb.mailbox.door.rotation.x = -1.35 * win(t, 107.8, 108.8);
    const m = P.wb.mailbox.pos;
    cam({ p: [[m[0] - 4.6, m[1] + 1.0, m[2] - 5.4], [m[0] - 3.4, m[1] + 0.8, m[2] - 4.2]], l: [m[0], m[1] - 0.1, m[2] - 0.4], f: m, fov: 34, ap: 3 }, u, d);
  });
  // S033 This one knew more. It talked about the children. It called them "young blood."
  shot(109.75, 112.2, (u, d, t) => {
    letter(["████ █████ ███ ██████ ████", "... the young blood ...", "█████ ████ ███████ ███"], 1);
    D.lights("desk", 0, { lamp: 0.6 });
    letterCam(u, d, { push: 0.8 });
  });
  // S034 ...the children... (seen from across the street, through the hedge)
  shot(112.2, 114.7, (u, d, t) => {
    on("watcher");
    D.lights("w_dusk");
    for (const [av, x, sc] of [[C.kid, -4, 0.78], [C.sister, -1, 0.72], [C.friendA, 2, 0.6]]) {
      stand(av, w(x, 0, 12 + Math.sin(t + x) * 0.6), 0.4 + Math.sin(t * 2 + x) * 0.3, { face: "smile", scale: sc, outfit: av === C.kid ? "hoodie" : undefined });
      D.walk(av, t * 6 + x, 0.4);
    }
    cam({ p: [[WX + 26, 3.5, 60], [WX + 24, 3.6, 59]], l: [WX - 1, 2.4, 12], f: w(-1, 2.4, 12), fov: 16, ap: 2, shake: 0.04 }, u, d);
  });
  // S035 "Who has the bedrooms facing the street?" (the upstairs windows)
  shot(114.7, 117.3, (u, d, t) => {
    on("watcher");
    D.lights("w_night");
    cam({ p: [[WX - 14, 13, 30], [WX + 14, 13, 30]], l: [[WX - 10, 13.4, 0], [WX + 10, 13.4, 0]], fov: 32, shake: 0.02 }, u, d);
  });
  // S036 "I'll know as soon as you move in." (an empty kid's bedroom, the window)
  shot(117.3, 120.0, (u, d, t) => {
    on("bedroom");
    D.lights("night", 0, { dark: true });
    cam({ p: [[-2, 6.0, 6.0], [1.5, 6.0, 0.5]], l: [6, 6, -10], fov: 44, ap: 1.5, shake: 0.02 }, u, d);
  });
  // S037 Think about that. Someone wanted to know which room each child would be sleeping in.
  shot(120.0, 124.95, (u, d, t) => {
    on("watcher");
    D.lights("w_night");
    P.wb.win[4 + 3].emissiveIntensity = 0.9;
    cam({ p: [[WX + 2, 9, 60], [WX + 2, 10, 54]], l: [WX + 5, 13.4, 0], f: w(5, 13.4, 0), fov: lerp(22, 14, win(u, 0, d)), shake: 0.03 }, u, d);
  });
  // S038 The family stopped bringing the kids to the house.
  shot(124.95, 128.2, (u, d, t) => {
    on("watcher");
    D.lights("w_day");
    stand(C.mom, w(18.2, 0, 15.2), PI / 2 + 0.6, { face: "worried", t });
    for (const [av, z, sc] of [[C.kid, 14.4, 0.78], [C.sister, 16.0, 0.72], [C.friendA, 15.0, 0.6]]) {
      walkTo(av, w(14, 0, z), w(17.4, 0, z - 0.6), win(t, 125.2, 127.5, (x) => x), t, { scale: sc, outfit: av === C.kid ? "hoodie" : undefined, face: "flat" });
    }
    cam({ p: [[WX + 4, 5, 26], [WX + 6, 5, 25]], l: WX + 0 ? [WX + 16, 3, 14] : [WX + 16, 3, 14], fov: 40, ap: 1 }, u, d);
  });
  // S039 So, pause for a second... Would you still move in? (calm night wide under the prompt)
  shot(128.2, 134.0, (u, d, t) => {
    on("watcher");
    D.lights("w_night");
    cam({ p: [[WX - 18, 6, 50], [WX - 10, 6.5, 46]], l: [WX, 10, 0], fov: 40 }, u, d);
  });
  // S040 It got stranger... the previous owners had received a letter from The Watcher too,
  shot(134.0, 137.6, (u, d, t) => {
    letter(L1, 1);
    D.lights("desk", 0, { lamp: 0.8 });
    const e = dk(-3.2, 3.28, 1.2);
    cam({ p: [[e[0] + 4.5, e[1] + 6.5, e[2] + 6.0], [e[0] + 3.6, e[1] + 5.6, e[2] + 4.8]], l: [[e[0] + 2, e[1], e[2] - 0.6], [e[0] + 1.8, e[1], e[2] - 0.7]], f: e, fov: 38, ap: 1.5 }, u, d);
  });
  // S041 shortly before the sale. (FOR SALE -> SOLD, back then)
  shot(137.6, 142.2, (u, d, t) => {
    on("watcher");
    D.lights("w_day");
    sixties();
    P.wb.sale.visible = true;
    P.wb.saleM.map = t < 140.4 ? P.wb.saleTex.sale : P.wb.saleTex.sold;
    cam({ p: [[WX - 18, 4.2, 30], [WX - 16, 4.6, 28]], l: [[WX - 9, 4, 20], [WX - 6, 6, 8]], f: w(-9, 4, 20), fov: 40, ap: 1.2 }, u, d);
  });
  // S042 More letters came.
  shot(142.2, 144.9, (u, d, t) => {
    letter(L5, 1, { sign: true });
    D.lights("desk", 0, { lamp: 0.8 });
    letterCam(u, d, { push: 0.3, ox: -0.6 });
  });
  // S043 Police looked into it.
  shot(144.9, 147.6, (u, d, t) => {
    on("watcher");
    D.lights("w_dusk");
    stand(C.cop, w(-2, 0, 27.4), PI, { face: "flat", t });
    C.cop.j.head.rotation.x = -0.1;
    holdUp(C.cop, "L", 0.7);
    PR.notebook.visible = true;
    D.attach(PR.notebook, C.cop.j.handL, [0, -0.2, 0.4], [-0.6, 0, 0]);
    const h = head(C.cop);
    cam({ p: [[h[0] + 4, h[1] + 0.6, h[2] + 9], [h[0] + 3, h[1] + 0.4, h[2] + 7.5]], l: [[h[0], h[1] - 1, h[2]], [h[0] - 1, h[1] - 0.4, h[2] - 6]], f: h, fov: 38, ap: 1 }, u, d);
  });
  // S044 There were persons of interest, but no proof. No one was ever charged.
  shot(147.6, 150.0, (u, d, t) => {
    on("watcher");
    D.lights("w_night");
    cam({ p: [[WX + 20, 4, 30], [WX - 20, 4, 30]], l: [[WX + 30, 9, 64], [WX - 30, 9, 64]], fov: 30, shake: 0.02 }, u, d);
  });
  // S045 The Broadduses never spent a single night in the house.
  shot(150.0, 154.0, (u, d, t) => {
    on("watcher");
    D.lights("w_night");
    P.wb.lantern.emissiveIntensity = 0;
    cam({ p: [[WX + 2, 7, 30], [WX + 2, 9, 44]], l: [WX, 10, 0], fov: 40 }, u, d);
  });
  // S046 They tried to sell it.
  shot(154.0, 157.6, (u, d, t) => {
    on("watcher");
    D.lights("w_day");
    P.wb.sale.visible = true;
    P.wb.saleM.map = P.wb.saleTex.sale;
    const s = w(-9, 4.1, 20);
    cam({ p: [[s[0] + 5, 4.4, s[2] + 9], [s[0] + 3, 4.3, s[2] + 6]], l: s, f: s, fov: 38, ap: 1.5 }, u, d);
  });
  // S047 Buyers backed out once they heard the story.
  shot(157.6, 160.3, (u, d, t) => {
    on("watcher");
    D.lights("w_day");
    P.wb.sale.visible = true;
    const k = win(t, 157.8, 160.2, (x) => x);
    walkTo(C.guests[2], w(-0.6, 0, 8), w(-0.6, 0, 26), k, t, { face: "flat" });
    walkTo(C.guests[3], w(1.2, 0, 7.4), w(1.2, 0, 25.4), k, t + 0.3, { face: "flat" });
    cam({ p: [[WX + 10, 5, 38], [WX + 8, 5, 37]], l: [[WX, 4, 12], [WX, 4, 22]], fov: 40 }, u, d);
  });
  // S048 They even asked the town to let them tear it down. The town said no.
  shot(160.3, 163.3, (u, d, t) => {
    on("watcher");
    D.lights("w_day");
    G().uSat.value = 0.8;
    if (t > 162.0) ctx.hud = { mode: "stamp", text: "DENIED", sub: "REQUEST TO TEAR IT DOWN", k: win(t, 162.0, 162.25) };
    cam({ p: [[WX - 4, 9, 40], [WX - 3, 9.5, 38]], l: [WX, 10, 0], fov: 40 }, u, d);
  });
  // S049 In 2019, they finally sold it,
  shot(163.3, 167.0, (u, d, t) => {
    on("watcher");
    D.lights("w_dusk");
    P.wb.sale.visible = true;
    P.wb.saleM.map = t < 164.6 ? P.wb.saleTex.sale : P.wb.saleTex.sold;
    const s = w(-9, 4.1, 20);
    cam({ p: [[s[0] - 4, 4.6, s[2] + 7], [s[0] - 3, 4.4, s[2] + 5.5]], l: s, f: s, fov: 38, ap: 1.5 }, u, d);
  });
  // S050 for around $400,000 less than they paid.
  shot(167.0, 170.4, (u, d, t) => {
    on("watcher");
    D.lights("w_dusk");
    G().uFade.value = 0.35;
    ctx.hud = { mode: "price", k: win(u, 0, 0.3), k2: win(t, 167.1, 168.6, (x) => x) };
    cam({ p: [[WX - 20, 6, 50], [WX - 18, 6, 48]], l: [WX, 10, 0], fov: 40 }, u, d);
  });
  // S051 To this day, no one knows who The Watcher was.
  shot(170.4, 174.0, (u, d, t) => {
    on("watcher");
    D.lights("w_night");
    const m = P.wb.mailbox.pos;
    cam({ p: [[m[0] + 6, 3.2, m[2] + 8], [m[0] + 3, 3.4, m[2] + 7]], l: [[m[0], 3.8, m[2]], [WX, 9, 0]], f: m, fov: 38, ap: 1.2 }, u, d);
  });
  // S052 And from the windows of 657 Boulevard, you can see dozens of other windows.
  shot(174.0, 177.8, (u, d, t) => {
    on("watcher");
    D.lights("w_night");
    cam({ p: [[WX - 4, 13.4, 1.4], [WX + 4, 13.4, 1.6]], l: [[WX - 30, 10, 64], [WX + 30, 10, 64]], fov: 40, shake: 0.02 }, u, d);
  });
  // S053 Any one of them could have been his. (push into one window: someone is there)
  shot(177.8, 182.9, (u, d, t) => {
    on("watcher");
    D.lights("w_night", 0, { watch: win(t, 179.6, 180.6) });
    const tw = w(43, 12, 63.9);
    cam({ p: [w(5, 13.4, 1.6), w(5, 13.4, 1.6)], l: [w(20, 11, 64), tw], f: tw, fov: [30, 7], shake: 0.02, e: ease.inOut }, u, d);
    fadeOut(u, d, 0.5);
  });
  // S054 That was America. Now, let's go back in time, and across the ocean, to England.
  shot(182.9, 188.3, (u, d, t) => {
    on("globe");
    D.lights("globe");
    const k = win(t, 183.4, 187.8);
    P.arc.geometry.setDrawRange(0, Math.floor(P.arcCount * k));
    const lon = lerp(NJ[0] + 8, LDN[0] - 10, k), lat = lerp(36, 44, k);
    const c = lonLat(lon, lat, 27);
    cam({ p: [GLOBE[0] + c.x, GLOBE[1] + c.y, GLOBE[2] + c.z], l: [GLOBE[0], GLOBE[1] + 3, GLOBE[2]], fov: 40, shake: 0.01 }, 0, 1);
    fadeIn(u, 0.5);
  });
  // S055 hit that like button (zoom down onto London)
  shot(188.3, 194.1, (u, d, t) => {
    on("globe");
    D.lights("globe");
    P.arc.geometry.setDrawRange(0, P.arcCount);
    const k = win(u, 0, d);
    const c = lonLat(LDN[0] - 10 + k * 8, 44 + k * 6, lerp(27, 15, k));
    cam({ p: [GLOBE[0] + c.x, GLOBE[1] + c.y, GLOBE[2] + c.z], l: [GLOBE[0], GLOBE[1] + lerp(3, 6, k), GLOBE[2]], fov: 40, shake: 0.01 }, 0, 1);
    fadeOut(u, d, 0.6);
  });

  // =====================================================================================
  // CHAPTER TWO: THE ENFIELD POLTERGEIST
  // S056 chapter card: Green Street at night
  shot(194.1, 198.25, (u, d, t) => {
    on("enfOut");
    D.lights("uk_night", 0, { lit: 1 });
    cam({ p: [[EX - 26, 6, 40], [EX - 20, 6, 38]], l: [EX - 4, 8, 0], fov: 40 }, u, d);
    G().uFade.value = 0.45;
  });
  // S057 August 1977. Enfield, north London.
  shot(198.25, 201.3, (u, d, t) => {
    on("enfOut");
    D.lights("uk_day");
    cam({ p: [[EX + 30, 5, 30], [EX + 22, 5, 30]], l: [[EX + 6, 6, 12], [EX - 2, 6, 6]], fov: 42 }, u, d);
  });
  // S058 284 Green Street.
  shot(201.3, 204.4, (u, d, t) => {
    on("enfOut");
    D.lights("uk_day");
    const n = eo(-3.6, 7.3, 0.2);
    cam({ p: [[n[0] + 2, 6.0, 9], [n[0] + 1, 6.6, 6]], l: [[n[0], 5.4, 0], n], f: n, fov: 36, ap: 1.2 }, u, d);
  });
  // S059 Peggy Hodgson was a single mother,
  shot(204.4, 207.0, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live");
    stand(C.peggy, el(1.5, 0, 0.5), 0.3, { face: "momSmile", t });
    stand(C.margaret, el(-1.4, 0, 1.8), 0.4, { face: "smile", scale: 0.82, t: t + 1 });
    stand(C.janet, el(4.2, 0, 2.4), -0.2, { face: "smile", scale: 0.76, outfit: "day", t: t + 2 });
    stand(C.kid, el(-0.2, 0, 3.6), 0.2, { face: "smile", scale: 0.72, outfit: "pjs", t: t + 3 });
    stand(C.friendB, el(2.8, 0, 4.2), -0.1, { face: "smile", scale: 0.58, t: t + 4 });
    cam({ p: [[EL[0] + 1.5, 7.0, EL[2] + 8.4], [EL[0] + 1.5, 6.6, EL[2] + 8.0]], l: [EL[0] + 1.5, 3.2, EL[2] + 1.5], fov: 50, ap: 1 }, u, d);
  });
  // S060 raising four kids in a small council house.
  shot(207.0, 210.1, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live");
    stand(C.peggy, el(-4.5, 0, 4.0), PI / 2 - 0.3, { face: "momSmile", t });
    for (const [av, p, sc, o] of [[C.kid, [-1.5, 3.2], 0.72, "pjs"], [C.friendB, [0.5, 4.6], 0.58], [C.janet, [1.8, 2.6], 0.76, "day"], [C.margaret, [3.4, 4.2], 0.82]]) {
      stand(av, el(p[0], 0, p[1]), -0.6 + Math.sin(t + p[0]) * 0.2, { face: "smile", scale: sc, outfit: o, t });
    }
    P.toys.forEach((ty, i) => (ty.position.y = 0.23 + Math.max(0, Math.sin(t * 3 + i)) * 0.15));
    cam({ p: [[EL[0] + 7.5, 5.4, EL[2] + 8.2], [EL[0] + 6.5, 5.2, EL[2] + 8.0]], l: [EL[0] - 0.5, 2.0, EL[2] + 3.2], fov: 46, ap: 1.2 }, u, d);
  });
  // S061 One night, the children said their beds were shaking.
  shot(210.1, 213.4, (u, d, t) => {
    on("enfBed");
    D.lights("enf_bed");
    lie(C.janet, eb(-5.6, 2.55, -2.0), { face: "scared", scale: 0.74, outfit: "night" });
    lie(C.kid, eb(5.6, 2.55, -2.0), { face: "scared", scale: 0.72, outfit: "pjs" });
    const sh = win(t, 211.0, 211.4) * (1 - win(t, 213.0, 213.4));
    P.enfBeds.forEach((b, i) => { b.rotation.z = Math.sin(t * 31 + i) * 0.02 * sh; b.position.y = Math.abs(Math.sin(t * 23 + i * 2)) * 0.12 * sh; });
    C.janet.root.position.y += P.enfBeds[0].position.y;
    C.kid.root.position.y += P.enfBeds[1].position.y;
    cam({ p: [[EB[0], 6.4, EB[2] + 7.0], [EB[0], 6.0, EB[2] + 6.0]], l: [EB[0], 2.2, EB[2] - 3], fov: 46, shake: 0.03 + 0.03 * sh }, u, d);
  });
  // S062 Then came the knocking. Slow, heavy knocks, inside the walls.
  const knocks = [214.0, 215.0, 215.9, 216.6, 217.3];
  const knockAmt = (t) => knocks.reduce((m, k) => Math.max(m, t >= k && t < k + 0.25 ? 1 - (t - k) / 0.25 : 0), 0);
  shot(213.4, 218.0, (u, d, t) => {
    on("enfBed");
    D.lights("enf_bed");
    lie(C.janet, eb(-5.6, 2.55, -2.0), { face: "scared", scale: 0.74, outfit: "night" });
    C.janet.j.head.rotation.y = -0.5;
    const kk = knockAmt(t);
    P.frames.forEach((f, i) => (f.rotation.z = Math.sin(t * 50 + i) * 0.06 * kk));
    cam({ p: [[EB[0] - 1.0, 5.4, EB[2] + 2.5], [EB[0] - 1.6, 5.2, EB[2] + 2.0]], l: [EB[0] - 8.6, 5.2, EB[2] - 0.6], f: [EB[0] - 8.6, 5.6, EB[2] - 1], fov: 44, ap: 1.2, shake: 0.03 + kk * 0.12 }, u, d);
  });
  // S063 Peggy said she walked into the bedroom,
  shot(218.0, 221.0, (u, d, t) => {
    on("enfBed");
    D.lights("enf_bed", 0, { bulb: win(t, 218.3, 218.6) });
    walkTo(C.peggy, eb(8.2, 0, 5.6), eb(5.0, 0, 3.4), win(t, 218.6, 220.4, (x) => x), t, { face: "worried" });
    const h = head(C.peggy);
    cam({ p: [[EB[0] - 4, 6, EB[2] - 4.5], [EB[0] - 3.4, 5.8, EB[2] - 3.8]], l: [h[0], h[1] - 1.5, h[2]], f: h, fov: 40, ap: 1.2 }, u, d);
  });
  // S064 and watched a heavy chest of drawers slide across the floor. By itself.
  shot(221.0, 225.4, (u, d, t) => {
    on("enfBed");
    D.lights("enf_bed", 0, { bulb: 1 });
    const k = ease.inOut(win(t, 222.2, 224.6));
    P.chest.position.set(-0.6 * k, 0, -6.6 + 3.6 * k);
    P.chest.rotation.y = 0.2 * k;
    P.chest.position.x += Math.sin(t * 45) * 0.025 * bump(t, 222.2, 224.6);
    lie(C.janet, eb(-5.6, 2.55, -2.0), { face: "shock", scale: 0.74, outfit: "night" });
    C.janet.j.head.rotation.y = -0.6;
    cam({ p: [[EB[0] + 6.4, 4.0, EB[2] + 3.0], [EB[0] + 5.8, 3.8, EB[2] + 2.6]], l: [EB[0] - 0.4, 2.2, EB[2] - 4.4], f: [EB[0] - 0.4, 2.2, EB[2] - 4.4], fov: 44, ap: 1.2, shake: 0.02 }, u, d);
  });
  // S065 She pushed it back. She said it wouldn't move, like someone was pushing from the other side.
  shot(225.4, 230.9, (u, d, t) => {
    on("enfBed");
    D.lights("enf_bed", 0, { bulb: 1 });
    P.chest.position.set(-0.6 + Math.sin(t * 60) * 0.02, 0, -3.0);
    P.chest.rotation.y = 0.2;
    stand(C.peggy, eb(-0.1, 0, -0.6), PI + 0.2, { face: "worried" });
    C.peggy.j.armL.rotation.set(-1.5, 0, 0.1);
    C.peggy.j.armR.rotation.set(-1.5, 0, -0.1);
    C.peggy.j.torso.rotation.x = 0.25 + Math.sin(t * 8) * 0.03;
    if (t > 228.0) C.peggy.setFace("scared", { sweat: true });
    cam({ p: [[EB[0] - 6.8, 5.6, EB[2] + 4.6], [EB[0] - 6.0, 5.4, EB[2] + 4.0]], l: [EB[0] - 0.2, 3.4, EB[2] - 1.8], fov: 44, ap: 1, shake: 0.025 }, u, d);
  });
  // S066 She took the kids next door.
  shot(230.9, 233.6, (u, d, t) => {
    on("enfOut");
    D.lights("uk_night", 0, { lit: 1 });
    const k = win(t, 231.0, 233.5, (x) => x);
    const path = (dx) => [eo(-3.6 + dx, 0, 2.5), eo(3.6 + dx, 0, 2.6)];
    walkTo(C.peggy, ...path(0), k, t, { face: "worried" });
    walkTo(C.janet, ...path(-1.6), k, t + 0.2, { face: "scared", scale: 0.74, outfit: "night" });
    walkTo(C.margaret, ...path(-3.0), k, t + 0.4, { face: "scared", scale: 0.82 });
    walkTo(C.kid, ...path(-4.2), k, t + 0.6, { face: "scared", scale: 0.72, outfit: "pjs" });
    walkTo(C.friendB, ...path(-5.2), k, t + 0.8, { face: "scared", scale: 0.58 });
    cam({ p: [[EX, 5, 20], [EX + 1, 5, 19]], l: [EX, 3.5, 2], fov: 42 }, u, d);
  });
  // S067 The neighbours went in to check. And they heard the knocking too.
  const knocks2 = [234.6, 235.4, 236.2];
  shot(233.6, 236.8, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live", 0, { lamp: 0.6 });
    stand(C.guests[3], el(-2.0, 0, 1.0), -0.9, { face: "worried" });
    C.guests[3].j.head.rotation.y = -0.6;
    stand(C.grandma, el(0.8, 0, 2.2), -1.1, { face: "momSmile" });
    C.grandma.setFace("worried");
    const kk = knocks2.reduce((m, k) => Math.max(m, t >= k && t < k + 0.25 ? 1 - (t - k) / 0.25 : 0), 0);
    cam({ p: [[EL[0] + 6, 5.4, EL[2] + 7], [EL[0] + 5, 5.2, EL[2] + 6.2]], l: [EL[0] - 2.5, 4.2, EL[2] - 1], fov: 40, ap: 1.2, shake: 0.02 + kk * 0.1 }, u, d);
  });
  // S068 So they called the police.
  shot(236.8, 238.6, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live", 0, { lamp: 0.6 });
    const lift = win(t, 237.0, 237.5);
    P.handset70.position.set(0.2 * lift, 0.66 + 1.4 * lift, 0.3 * lift);
    P.handset70.rotation.z = 0.5 * lift;
    const ph = el(-9.0, 2.9, 2.6);
    cam({ p: [[ph[0] + 3.4, ph[1] + 2.2, ph[2] + 2.6], [ph[0] + 2.8, ph[1] + 1.8, ph[2] + 2.2]], l: ph, f: ph, fov: 38, ap: 2 }, u, d);
  });
  // S069 An officer came to the house,
  shot(238.6, 241.6, (u, d, t) => {
    on("enfOut");
    D.lights("uk_night", 0, { lit: 1 });
    walkTo(C.wpc, eo(-3.6, 0, 11.5), eo(-3.6, 0, 1.8), win(t, 238.7, 241.4, (x) => x), t, { face: "flat" });
    cam({ p: [[EX + 6, 4.5, 16], [EX + 4, 4.4, 14]], l: [[EX - 3.6, 4, 7], [EX - 3.6, 4.5, 2]], fov: 40 }, u, d);
  });
  // S070 and later reported seeing a chair wobble, and slide across the floor,
  shot(241.6, 245.0, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live", 0, { lamp: 0.7 });
    const wob = bump(t, 242.2, 243.4);
    const sl = ease.inOut(win(t, 243.3, 244.6));
    P.diningChair.position.set(3.5 - 3.0 * sl, 0, 1.0 + 0.8 * sl);
    P.diningChair.rotation.set(Math.sin(t * 30) * 0.06 * wob, -0.6 + 0.3 * sl, Math.cos(t * 26) * 0.06 * wob);
    stand(C.wpc, el(-4.4, 0, 6.0), PI - 0.6, { face: "worried" });
    const c = el(2.0, 2, 1.4);
    cam({ p: [[EL[0] - 2, 5.0, EL[2] + 8.2], [EL[0] - 1.4, 4.8, EL[2] + 7.8]], l: c, f: c, fov: 44, ap: 1, shake: 0.02 }, u, d);
  });
  // S071 with no explanation.
  shot(245.0, 247.0, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live", 0, { lamp: 0.7 });
    stand(C.wpc, el(-4.4, 0, 6.0), PI - 0.6, { face: "shock" });
    const h = head(C.wpc);
    cam({ p: [[h[0] + 3.6, h[1] + 0.2, h[2] - 4.4], [h[0] + 3.0, h[1] + 0.1, h[2] - 3.7]], l: [h[0], h[1] - 0.4, h[2]], f: h, fov: 36, ap: 2 }, u, d);
  });
  // S072 And that was only the beginning.
  shot(247.0, 249.5, (u, d, t) => {
    on("enfOut");
    D.lights("uk_night", 0, { lit: 0.6 + 0.6 * (Math.sin(t * 13) > 0.6 ? 1 : 0.3) });
    cam({ p: [[EX - 9, 6, 18], [EX - 9.2, 9, 12]], l: [EX - 9.5, 12, 0], fov: 38 }, u, d);
  });
  // S073 Over the next months, people reported toys flying across rooms.
  shot(249.5, 252.6, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live", 0, { lamp: 0.8 });
    P.toys.forEach((ty, i) => {
      const k = clamp((t - 249.9 - i * 0.28) / 0.9);
      const h = ty.userData.home;
      ty.position.set(h.x + k * (6 + i), h.y + Math.sin(k * PI) * (3 + i * 0.4), h.z - k * (4 + i * 0.5));
      ty.rotation.set(k * 6, k * 4, k * 3);
    });
    cam({ p: [[EL[0] - 7, 5.2, EL[2] + 8.0], [EL[0] - 6, 5.0, EL[2] + 7.6]], l: [EL[0] + 2, 2.8, EL[2] + 1], fov: 50, shake: 0.03 }, u, d);
  });
  // S074 Chairs knocked over.
  shot(252.6, 255.0, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live", 0, { lamp: 0.8 });
    const k = ease.in ? ease.in(win(t, 253.0, 253.5, (x) => x)) : win(t, 253.0, 253.5);
    P.diningChair.position.set(3.5, 0, 1.0);
    P.diningChair.rotation.set(-1.45 * k, -0.6, 0);
    const c = el(3.5, 1.5, 1.0);
    cam({ p: [[c[0] - 4, 3.0, c[2] + 5], [c[0] - 3.6, 2.8, c[2] + 4.5]], l: c, f: c, fov: 40, ap: 1.5, shake: 0.03 }, u, d);
  });
  // S075 A national newspaper covered the story for a year and a half.
  shot(255.0, 258.8, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live", 0, { lamp: 0.8 });
    stand(C.guests[0], el(-1.5, 0, 4.4), PI - 0.9, { face: "flat" });
    holdUp(C.guests[0], "R", 1);
    C.guests[0].j.armL.rotation.set(-1.3, 0, 0.5);
    PR.camera.visible = true;
    D.attach(PR.camera, C.guests[0].j.head, [0.0, 0.1, 1.2], [0, 0, 0]);
    stand(C.guests[2], el(1.8, 0, 6.0), PI - 0.5, { face: "flat", t });
    holdUp(C.guests[2], "L", 0.7);
    PR.notebook.visible = true;
    D.attach(PR.notebook, C.guests[2].j.handL, [0, -0.2, 0.4], [-0.6, 0, 0]);
    const fl = [255.9, 257.6].some((k) => t >= k && t < k + 0.12) ? 1 : 0;
    PR.flashM.color.set("#ffffff").multiplyScalar(fl ? 6 : 0.2);
    const L = W.lights.glows;
    L[3].color.set("#ffffff"); L[3].decay = 2; L[3].distance = 0;
    L[3].position.copy(PR.camera.position); L[3].intensity = fl * 400;
    cam({ p: [[EL[0] + 7, 5.4, EL[2] + 9], [EL[0] + 6, 5.2, EL[2] + 8]], l: [EL[0] - 1, 4.0, EL[2] + 2], fov: 42, ap: 1 }, u, d);
  });
  // S076 More than thirty people said they saw something.
  shot(258.8, 262.6, (u, d, t) => {
    on("enfOut");
    D.lights("uk_day");
    const crowd = [C.guests[0], C.guests[1], C.guests[2], C.guests[3], C.grandma, C.margaret, C.cop];
    crowd.forEach((av, i) => stand(av, eo(-14 + i * 2.6, 0, 11.6 + (i % 2) * 1.6), PI + (i - 3) * 0.08, { face: i % 3 ? "flat" : "worried", scale: av === C.margaret ? 0.82 : 1, t: t + i }));
    C.cop.root.visible = false;
    cam({ p: [[EX - 5, 5, 34], [EX - 4, 5.4, 31]], l: [EX - 5, 5, 6], fov: 40 }, u, d);
  });
  // S077 Two investigators, Maurice Grosse and Guy Lyon Playfair, came to the house.
  shot(262.6, 266.8, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live");
    stand(C.grandpa, el(4.4, 0, 3.6), 0.5, { face: "flat", outfit: "suit", t });
    stand(C.guests[1], el(8.4, 0, 3.4), -0.5, { face: "flat", t: t + 1 });
    P.reels.forEach((r, i) => (r.rotation.y = t * (i ? 3.4 : 2.8)));
    cam({ p: [[EL[0] + 2.0, 5.6, EL[2] + 8.2], [EL[0] + 2.8, 5.4, EL[2] + 7.8]], l: [EL[0] + 6, 3.6, EL[2] + 2], fov: 48, ap: 1 }, u, d);
  });
  // S078 They stayed for months, recording everything. (the reels)
  shot(266.8, 271.2, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live");
    P.reels.forEach((r, i) => (r.rotation.y = t * (i ? 3.4 : 2.8)));
    const tp = el(6.4, 3.6, 1.0);
    cam({ p: [[tp[0] - 2.6, tp[1] + 1.6, tp[2] + 2.4], [tp[0] - 1.8, tp[1] + 1.2, tp[2] + 1.8]], l: tp, f: tp, fov: 38, ap: 3 }, u, d);
  });
  // S079 Then, 11-year-old Janet began speaking in a deep, rough voice.
  shot(271.2, 275.0, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live", 0, { lamp: 0.55 });
    stand(C.janet, el(1.0, 0, 6.4), PI, { face: "flat", scale: 0.76, outfit: "night" });
    D.sit(C.janet, 1.9);
    C.janet.j.head.rotation.x = 0.35;
    stand(C.grandpa, el(1.6, 0, 2.2), 0.2, { face: "worried", outfit: "suit" });
    holdUp(C.grandpa, "R", 0.9);
    PR.mic.visible = true;
    D.attach(PR.mic, C.grandpa.j.handR, [0, -0.2, 0.3], [-1.2, 0, 0]);
    const h = head(C.janet);
    cam({ p: [[h[0] - 4.2, h[1] + 0.6, h[2] - 5.6], [h[0] - 3.4, h[1] + 0.4, h[2] - 4.6]], l: [h[0], h[1] - 0.6, h[2]], f: h, fov: 38, ap: 1.5 }, u, d);
  });
  // S080 It said it was an old man called Bill. (Janet close, lit from below)
  shot(275.0, 279.0, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live", 0, { lamp: 0.3, corner: 0.0 });
    stand(C.janet, el(1.0, 0, 6.4), PI, { face: "flat", scale: 0.76, outfit: "night" });
    D.sit(C.janet, 1.9);
    C.janet.j.head.rotation.set(0.1, 0, 0.12);
    C.janet.setFace("sleep");
    const h = head(C.janet);
    const L = W.lights.glows;
    L[3].color.set("#b8c8ff"); L[3].decay = 2; L[3].distance = 6;
    L[3].position.set(h[0], h[1] - 2.0, h[2] - 1.6); L[3].intensity = 16;
    cam({ p: [[h[0], h[1] + 0.1, h[2] - 4.2], [h[0], h[1], h[2] - 3.2]], l: [h[0], h[1] - 0.15, h[2]], f: h, fov: 34, ap: 2, shake: 0.015 }, u, d);
  });
  // S081 "I died in the chair, in the corner, downstairs."
  shot(279.0, 284.1, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live", 0, { lamp: 0.2, corner: 1, cornerColor: "#9fb4ff" });
    G().uSat.value = 0.45;
    const c = el(-8.2, 2.4, -6.2);
    cam({ p: [[c[0] + 6.6, 4.6, c[2] + 6.6], [c[0] + 3.6, 3.8, c[2] + 3.6]], l: c, f: c, fov: 40, ap: 1.5, shake: 0.015 }, u, d);
  });
  // S082 After the case was talked about on the radio,
  shot(284.1, 288.0, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live", 0, { lamp: 0.9 });
    const r = el(7.8, 3.6, 2.1);
    cam({ p: [[r[0] - 3, r[1] + 1.4, r[2] + 3], [r[0] - 2.2, r[1] + 1.0, r[2] + 2.2]], l: r, f: r, fov: 36, ap: 2.5 }, u, d);
  });
  // S083 a man contacted the investigators.
  shot(288.0, 291.0, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live", 0, { lamp: 0.9 });
    stand(C.grandpa, el(-7.4, 0, 3.4), -PI / 2 + 0.5, { face: "flat", outfit: "suit", t });
    C.grandpa.j.armL.rotation.set(-2.5, 0, 0.5);
    P.handset70.visible = false;
    PR.handset.visible = true;
    D.attach(PR.handset, C.grandpa.j.head, [-0.85, 0.5, 0.3], [0, 0, PI / 2]);
    const h = head(C.grandpa);
    cam({ p: [[h[0] + 5, h[1] + 0.3, h[2] + 4], [h[0] + 4.2, h[1] + 0.2, h[2] + 3.4]], l: [h[0], h[1] - 0.8, h[2]], f: h, fov: 36, ap: 2 }, u, d);
  });
  // S084 He said his father had died in that house, in 1963.
  shot(291.0, 294.8, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live", 0, { lamp: 0.25, corner: 0.6 });
    sepia();
    ctx.hud = { mode: "year", text: "1963", k: win(u, 0, 0.4) };
    const c = el(-8.2, 2.4, -6.2);
    cam({ p: [[c[0] + 9, 6, c[2] + 3], [c[0] + 8, 5.6, c[2] + 4]], l: c, f: c, fov: 40, ap: 1 }, u, d);
  });
  // S085 So, was it real?
  shot(294.8, 296.8, (u, d, t) => {
    on("enfBed");
    D.lights("enf_bed", 0, { bulb: 0.4 });
    stand(C.janet, eb(-3.2, 0, 2.2), 0.4, { face: "flat", scale: 0.76, outfit: "night" });
    const h = head(C.janet);
    cam({ p: [[h[0] + 1.0, h[1], h[2] + 3.4], [h[0] + 0.8, h[1], h[2] + 2.8]], l: h, f: h, fov: 36, ap: 2 }, u, d);
  });
  // S086 A hidden camera caught Janet bending spoons when she thought no one was watching.
  shot(296.8, 302.6, (u, d, t) => {
    on("enfBed");
    D.lights("enf_bed", 0, { bulb: 1 });
    G().uSat.value = 0.0;
    G().uGrain.value = 0.12;
    stand(C.janet, eb(-5.6, 0, 1.4), 0.1, { face: "flat", scale: 0.76, outfit: "night" });
    D.sit(C.janet, 1.95);
    C.janet.j.armL.rotation.set(-1.3, 0, 0.45);
    C.janet.j.armR.rotation.set(-1.3, 0, -0.45);
    C.janet.j.head.rotation.x = 0.45;
    P.spoon.visible = true;
    D.attach(P.spoon, C.janet.j.handR, [-0.3, -0.1, 0.4], [0, 0, 0.6 + 0.9 * win(t, 299.0, 301.5)]);
    ctx.hud = { mode: "cam", label: "HIDDEN CAMERA", stamp: "CAM 2" };
    cam({ p: [eb(7.6, 8.2, 6.8), eb(7.6, 8.2, 6.8)], l: [eb(-4.8, 2.2, 0.4), eb(-5.2, 2.6, 0.8)], fov: [44, 36], shake: 0 }, u, d);
  });
  // S087 The sisters admitted to journalists that some of it was faked.
  shot(302.6, 307.4, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live");
    stand(C.janet, el(0.4, 0, 6.6), PI, { face: "flat", scale: 0.76, outfit: "day" });
    D.sit(C.janet, 1.9);
    stand(C.margaret, el(2.4, 0, 6.6), PI, { face: "flat", scale: 0.82 });
    D.sit(C.margaret, 1.9);
    stand(C.guests[2], el(1.4, 0, 1.6), 0.0, { face: "flat", t });
    holdUp(C.guests[2], "L", 0.7);
    PR.notebook.visible = true;
    D.attach(PR.notebook, C.guests[2].j.handL, [0, -0.2, 0.4], [-0.6, 0, 0]);
    cam({ p: [[EL[0] - 5, 5.6, EL[2] - 2], [EL[0] - 4.2, 5.2, EL[2] - 1.2]], l: [EL[0] + 1.4, 3.2, EL[2] + 5], fov: 40, ap: 1 }, u, d);
  });
  // S088 And sceptics say the famous photo of Janet flying across her room
  shot(307.4, 311.0, (u, d, t) => {
    on("enfBed");
    D.lights("enf_bed", 0, { bulb: 1 });
    G().uSat.value = 0.0;
    G().uGrain.value = 0.1;
    stand(C.janet, eb(-4.4, 3.9, -1.0), 0.6, { face: "shock", scale: 0.76, outfit: "night" });
    C.janet.root.rotation.z = -0.3;
    C.janet.j.armL.rotation.set(-0.4, 0, 1.4);
    C.janet.j.armR.rotation.set(-0.4, 0, -1.2);
    C.janet.j.legL.rotation.x = 0.5;
    C.janet.j.legR.rotation.x = -0.4;
    const fl = t < 307.55 ? 1 : 0;
    G().uFade.value = 0;
    const L = W.lights.glows;
    L[3].color.set("#ffffff"); L[3].decay = 2; L[3].distance = 0;
    L[3].position.set(EB[0] + 3, 6, EB[2] + 5); L[3].intensity = 120 + fl * 600;
    ctx.hud = { mode: "photo", rot: -0.02, caption: "", k: 1 };
    cam({ p: [eb(1.5, 5.8, 7.4), eb(1.2, 5.7, 6.9)], l: eb(-4.4, 5.2, -1.0), fov: 46, shake: 0 }, u, d);
  });
  // S089 is just a girl jumping off her bed.
  shot(311.0, 314.7, (u, d, t) => {
    on("enfBed");
    D.lights("enf_bed", 0, { bulb: 1 });
    const ph = ((t - 311.0) % 1.2) / 1.2;
    const y = 2.55 + Math.sin(ph * PI) * 1.3;
    stand(C.janet, eb(-5.6 + 0.4 * Math.sin(ph * PI), y, -0.6), 0.6, { face: "smile", scale: 0.76, outfit: "night" });
    C.janet.j.armL.rotation.set(-0.3, 0, 0.9 * Math.sin(ph * PI));
    C.janet.j.armR.rotation.set(-0.3, 0, -0.9 * Math.sin(ph * PI));
    P.enfBeds[0].position.y = -0.12 * Math.max(0, Math.cos(ph * PI * 2));
    cam({ p: [eb(2.0, 5.6, 7.4), eb(1.6, 5.4, 6.8)], l: eb(-4.6, 4.6, -1.0), fov: 46, shake: 0.02 }, u, d);
  });
  // S090 But the investigators never changed their minds. They believed some of what they saw was genuine.
  shot(314.7, 321.2, (u, d, t) => {
    on("enfLive");
    D.lights("enf_live", 0, { lamp: 0.6, corner: 0.5 });
    stand(C.grandpa, el(-2.6, 0, 1.6), -PI * 0.75, { face: "flat", outfit: "suit", t });
    stand(C.guests[1], el(-0.6, 0, 0.4), -PI * 0.7, { face: "flat", t: t + 1 });
    P.reels.forEach((r, i) => (r.rotation.y = t * (i ? 3.4 : 2.8)));
    cam({ p: [[EL[0] + 3.5, 5.0, EL[2] + 7.5], [EL[0] + 2.5, 4.8, EL[2] + 6.5]], l: [EL[0] - 5.5, 3.4, EL[2] - 3.6], fov: 42, ap: 1 }, u, d);
  });
  // S091 By 1979, it had faded away.
  shot(321.2, 325.4, (u, d, t) => {
    on("enfOut");
    D.lights("uk_day");
    cam({ p: [[EX + 4, 4.5, 26], [EX + 2, 5, 24]], l: [EX - 3, 6, 0], fov: 40 }, u, d);
  });
  // S092 But the story never did. Decades later, it inspired the movie The Conjuring 2.
  shot(325.4, 330.6, (u, d, t) => {
    on("enfOut");
    D.lights("uk_night", 0, { lit: 0.8 });
    cam({ p: [[EX - 4, 6, 26], [EX - 4, 10, 52]], l: [EX - 4, 7, 0], fov: 40 }, u, d);
    fadeOut(u, d, 0.6);
  });

  // =====================================================================================
  // OUTRO
  // S093 So. Two families. Two houses. One in America, one in England.
  shot(330.6, 336.0, (u, d, t) => {
    on("dio");
    P.dioWatcher.visible = P.dioEnfield.visible = true;
    D.lights("dio", 0, { spot: win(u, 0.2, 1.4), left: win(t, 333.6, 334.2), right: win(t, 334.6, 335.2) });
    cam({ p: [dio(0, 22, 46), dio(0, 15, 38)], l: dio(0, 4, 0), fov: 38, shake: 0.01 }, u, d);
    fadeIn(u, 0.5);
  });
  // S094 One was watched from the outside.
  shot(336.0, 338.0, (u, d, t) => {
    on("dio");
    P.dioWatcher.visible = P.dioEnfield.visible = true;
    D.lights("dio", 0, { spot: 0.7, left: 1.4, right: 0.2 });
    cam({ p: [dio(-6, 7, 18), dio(-8, 6.6, 16)], l: dio(-12, 3, 0), fov: 38, ap: 2, shake: 0.01 }, u, d);
  });
  // S095 The other, from within.
  shot(338.0, 340.1, (u, d, t) => {
    on("dio");
    P.dioWatcher.visible = P.dioEnfield.visible = true;
    D.lights("dio", 0, { spot: 0.7, left: 0.2, right: 1.4 });
    cam({ p: [dio(6, 7, 18), dio(8, 6.6, 16)], l: dio(12, 3, 0), fov: 38, ap: 2, shake: 0.01 }, u, d);
  });
  // S096 Which one would you rather spend a night in?... (under the poll)
  shot(340.1, 350.5, (u, d, t) => {
    on("dio");
    P.dioWatcher.visible = P.dioEnfield.visible = true;
    D.lights("dio", 0, { spot: 0.8 });
    const a = lerp(-0.25, 0.25, win(u, 0, d));
    cam({ p: [DIO[0] + Math.sin(a) * 44, DIO[1] + 10, DIO[2] + Math.cos(a) * 44], l: dio(0, 1, 0), fov: 36, shake: 0.01 }, 0, 1);
    G().uFade.value = 0.25;
  });
  // S097 Subscribe, so you don't miss it.
  shot(350.5, 353.5, (u, d, t) => {
    on("dio");
    P.dioWatcher.visible = P.dioEnfield.visible = true;
    D.lights("dio", 0, { spot: 0.8 });
    cam({ p: [dio(0, 10, 42), dio(0, 9, 40)], l: dio(0, 1, 0), fov: 36, shake: 0.01 }, u, d);
    G().uFade.value = 0.25;
  });
  // S098 And tonight... maybe check your mailbox before bed. (the flag goes up by itself)
  shot(353.5, 356.4, (u, d, t) => {
    on("watcher");
    D.lights("w_night");
    P.wb.mailbox.flag.rotation.z = -PI / 2 * (1 - ease.out(win(t, 355.2, 355.6)));
    const m = P.wb.mailbox.pos;
    cam({ p: [[m[0] + 3.6, m[1] - 0.6, m[2] + 5.2], [m[0] + 2.8, m[1] - 0.5, m[2] + 4.0]], l: [m[0], m[1] + 0.2, m[2]], f: m, fov: 36, ap: 2 }, u, d);
  });
  // END SCREEN: the street at night, dimmed
  shot(356.4, 371, (u, d, t) => {
    on("watcher");
    D.lights("w_night", 0, { watch: 1 });
    cam({ p: [[WX - 10, 7, 50], [WX - 4, 7.5, 47]], l: [WX + 4, 10, 10], fov: 44, shake: 0.01 }, u, d);
    G().uFade.value = lerp(0, 0.55, win(u, 0, 0.6));
  });

  // THUMBNAIL STILLS
  shot(400, 401, (u, d, t) => {
    on("watcher");
    D.lights("w_night", 0, { watch: 1 });
    P.wb.win[5].emissiveIntensity = 1.6;
    P.wb.win[9].emissiveIntensity = 1.2;
    cam({ p: [WX - 9, 6, 40], l: [WX + 1, 11, 2], fov: 40, shake: 0 }, 0, 1);
  });
  shot(401, 402, (u, d, t) => {
    on("enfBed");
    D.lights("enf_bed", 0, { bulb: 0.6 });
    P.chest.position.set(-0.4, 0.7, -3.2);
    P.chest.rotation.set(0.12, 0.35, -0.15);
    stand(C.janet, eb(-5.2, 3.4, -1.0), 0.5, { face: "scared", scale: 0.76, outfit: "night" });
    C.janet.root.rotation.z = -0.25;
    C.janet.j.armL.rotation.set(-0.4, 0, 1.4);
    C.janet.j.armR.rotation.set(-0.4, 0, -1.2);
    cam({ p: eb(4.6, 5.6, 7.4), l: eb(-2.6, 4.0, -2.6), fov: 48, shake: 0 }, 0, 1);
  });

  return S;
}
