
// ---------------------------------------------------------------- cue times (window.CT, from build/generate.py)
const v = (x, y, z) => new THREE.Vector3(x, y, z);
const Ls = (k) => C.lines[k][0], Le = (k) => C.lines[k][1], Bs = (k) => C.beats[k][0], Be = (k) => C.beats[k][1];
const talking = (t, k) => t > Ls(k) - .03 && t < Le(k) + .05;
const wordT = (k, i) => { const ws = C.words.filter((w) => w.take === k); return ws[Math.min(i, ws.length - 1)].s; };
// a cut on (nearly) every line, as the skits guide says; the rant is cut into three angles
const SHOTS = [
  ["phone", 0], ["rantA", Ls("02") - .1], ["rantB", wordT("02", 4) - .08], ["rantC", wordT("02", 9) - .08], ["thud", Bs("thud")],
  ["window", Ls("04") - .1], ["teaser1", Bs("teaser1")], ["bed", Ls("05") - .1], ["teaser2", Bs("teaser2")], ["pillow", Ls("06") - .1],
  ["hush", Bs("hero")], ["rise", Bs("hero") + .7], ["burst", Bs("hero") + 1.55], ["dive", Bs("hero") + 2.45], ["landing", Bs("hero") + 2.9], ["whoa", Ls("07") - .1], ["say", Bs("say")],
  ["fix1", Bs("fix1")], ["fix2", Bs("fix2")], ["fix3", Bs("fix3")], ["hug", Ls("10") - .15], ["end", Bs("endin")],
];
const shotAt = (t) => { let k = 0; for (let i = 0; i < SHOTS.length; i++) if (t >= SHOTS[i][1]) k = i; return [SHOTS[k][0], t - SHOTS[k][1], (SHOTS[k + 1] ? SHOTS[k + 1][1] : DUR) - SHOTS[k][1]]; };
const DESKC = v(.05, DESKY, .14);
const seated = (o = {}) => pose({ x: SEAT.x, y: SITY, z: SEAT.z, ry: 0, l: [[1.5, 1.5], [1.5, 1.5]], a: [[.95, .18, 1.25], [.95, .18, 1.25]], hp: .08, ...o });
const standing = (o = {}) => pose({ a: [[.1, .1, .15], [.1, .1, .15]], ...o });
// ---------------------------------------------------------------- flight: he flies head-first along a curve, banking into turns,
// wings beating, feet tucked; a sparkle ribbon and sparks trail behind him
const curve = (pts) => new THREE.CatmullRomCurve3(pts.map((p) => v(...p)), false, "catmullrom", .5);
const PATH = {
  t1: curve([[-2.6, 1.7, -3.45], [-1.6, 2.15, -3.4], [-.9, 1.9, -3.35], [-.2, 2.25, -3.4], [.6, 2.0, -3.45]]),
  t2: curve([[-2.7, 1.75, -2.75], [-1.5, 1.95, -2.7], [-.4, 1.8, -2.72], [.9, 2.0, -2.78]]),
  in: curve([[-1.05, 1.85, -2.95], [-.95, 1.95, -2.15], [-.35, 2.15, -1.3], [.75, 2.1, -.75], [1.35, 1.85, .05], [.95, 2.0, .7], [.28, 2.12, .42]]),
};
function flyState(cv, k, o = {}) {
  const p = cv.getPointAt(clamp(k)), tg = cv.getTangentAt(clamp(k)), tg2 = cv.getTangentAt(clamp(k + .03));
  const hd = Math.atan2(tg.x, tg.z), el = Math.asin(clamp(tg.y, -1, 1));
  let dh = Math.atan2(tg2.x, tg2.z) - hd; dh = Math.atan2(Math.sin(dh), Math.cos(dh));
  return { x: p.x, y: p.y, z: p.z, ry: hd, rx: .5 - el * .45, roll: clamp(-dh * 6, -.5, .5), still: true, noblink: true, feetBack: .6,
    wl: [1.15, .15], wr: [1.15, .15], flap: [.75, 4.2], eyes: "joy", look: [0, .2], jaw: .6, sq: -.04, ...o };
}
function trail(cv, k, span, camP, w, sparkN = 46) {
  const pts = []; for (let j = 0; j <= 30; j++) { const kk = k - span * (1 - j / 30); if (kk >= 0) pts.push(cv.getPointAt(clamp(kk))); }
  if (pts.length > 1) ribbon(pts, camP, w);
  for (let i = 0; i < Math.min(sparkN, FX.sparks.length); i++) {
    const sp = FX.sparks[i], ke = (i + hash(i * 1.7)) / sparkN, age = (k - ke) / (span * 1.6);
    sp.visible = age > 0 && age < 1; if (!sp.visible) continue;
    const p = cv.getPointAt(clamp(ke)); sp.position.set(p.x + (hash(i * 3) - .5) * .25 * age, p.y + (hash(i * 5) - .5) * .2 * age - .12 * age * age, p.z + (hash(i * 7) - .5) * .25 * age);
    const sz = (i % 5 ? .06 : .12) * (1 - age * .7) * Math.max(.6, w / .05); sp.scale.set(sz, sz, 1); sp.material.opacity = (1 - age) * .9; sp.material.rotation = i + age * 3;
  }
}
const POST = [];   // things that need his posed body (eye glints): run after placeCree
const ease = (x) => x < .5 ? 2 * x * x : 1 - (-2 * x + 2) ** 2 / 2;
function papers(t0, t, origin, push, n = 8) {          // loose papers lifting and drifting (deterministic)
  for (let i = 0; i < FX.papers.length; i++) {
    const p = FX.papers[i], a = t - t0 - i * .05; p.visible = i < n && a > 0;
    if (!p.visible) continue;
    const k = Math.min(a, 2.5);
    p.position.set(origin.x + (hash(i) - .5) * .5 + push.x * k * (.6 + .5 * hash(i * 3)), origin.y + push.y * k - .25 * Math.max(0, k - .6) ** 2 + .05 * Math.sin(k * 6 + i), origin.z + (hash(i * 5) - .5) * .3 + push.z * k * (.6 + .5 * hash(i * 7)));
    p.rotation.set(-Math.PI / 2 + k * (2 + hash(i) * 3), k * (1 + hash(i * 2) * 2), k * (hash(i * 9) - .5) * 4);
    if (p.position.y < .01) p.position.y = .01;
  }
}

// ---------------------------------------------------------------- one frame
const CAM = { p: v(0, 1.5, 3), l: v(0, 1, 0), fov: 40, focus: 3, ap: .03 };
function shoot(t) {
  const [sh, u, len] = shotAt(t);
  RM.visible = true; CREE.dark = false;
  for (const k of ["strip", "cards", "mach", "speed", "trail", "shadow", "ring", "ribbon", "rays", "blast", "glint", "halo"]) FX[k].visible = false;
  for (const a of [FX.sparks, FX.shards, FX.dust]) for (const o of a) o.visible = false;
  POST.length = 0; let flash = 0;
  for (const p of FX.planes) p.visible = false; for (const p of FX.papers) p.visible = false; for (const p of FX.puffs) p.visible = false;
  PEN.visible = false; LEO.phone.visible = false;
  for (const h of RM.panes) h.rotation.y = 0; for (const c of RM.curt) c.rotation.set(0, 0, 0);
  for (let i = 0; i < RM.clouds.length; i++) RM.clouds[i].position.x = -2.2 + i * 1.4 + ((t * .05 + i * .3) % 1.2);
  scene.background = tmpC.set(0x14102A).clone(); scene.fog.color.set(0x14102A); scene.fog.near = 30; scene.fog.far = 90;
  hemi.color.set(0xB8A8E8); hemi.groundColor.set(0x3A2A3A); hemi.intensity = .55;
  sun.color.set(0xA8C0FF); sun.intensity = .5; sun.target.position.set(0, 0, -.5); sun.position.set(-2.5, 5, 3);
  const LAND = Bs("hero") + 2.75 + .3;
  const dim = ss(t, Ls("04") - .5, Bs("hero")) * (1 - ss(t, LAND + .1, LAND + .6));        // tension: 0 -> 1 through the wishes
  const warm = ss(t, LAND + .1, LAND + .6);                                                  // relief after the landing
  RM.lamp.intensity = 2.6 - 1.4 * dim + .8 * warm; RM.moon.intensity = 2.0 + .4 * dim; RM.fill.intensity = 1.3 - .6 * dim + .3 * warm; RM.key.intensity = 1.8 - 1.0 * dim + .4 * warm;
  hemi.intensity = .55 - .2 * dim + .1 * warm; RM.lamp.color.set(warm > .5 ? 0xFFD8B8 : 0xFFD2B0); RM.rim.intensity = 0; RM.rim2.intensity = 0;
  phoneL.intensity = 0; RM.triScr.color.set(0xFFE3F1); RM.lapScr.color.set(0x9FB2D8);
  for (const b of RM.fairy) b.visible = true; RM.bulb.visible = true;
  // the fairy lights twinkle gently
  RM.fairy.forEach((b, i) => b.scale.setScalar(.85 + .25 * (.5 + .5 * Math.sin(t * 2.2 + i * 1.7))));
  let bloomS = .12, vig = .3, dark = 0;
  let cree = null, leo = null, leoF = {}, leoRot = null;
  const cam = CAM; cam.ap = .03;

  if (sh === "phone") {             // 1. his phone's glow on his face: 42 views; he slumps
    const slump = ss(t, Le("01") - .2, Le("01") + .35);
    leo = seated({ lean: .05 + .12 * slump, hp: .12 + .15 * slump, hy: -.12, a: [[.4, .2, .5], [1.35, -.15, 1.85]] });
    leoF = { eyes: "teary", mouth: "wavy", brows: "despair", talk: talking(t, "01"), look: [-.4, -.3] };
    LEO.phone.visible = true; LEO.scr.color.set(0xDDE8FF);
    cam.p.set(.32, 1.68, 2.4 - .2 * ss(u, 0, len)); cam.l.set(.02, 1.48, -.7); cam.fov = 34; cam.focus = 3.0;
    RM.key.intensity = 1.1; phoneL.intensity = .45;
  } else if (sh === "rantA" || sh === "rantB" || sh === "rantC") {   // 2. the rant, three angles: arms up, counting, hands in his hair
    const x = .3 + .35 * Math.sin(t * 1.2), walkA = sh === "rantC" ? 0 : .6;
    let p = walk(standing({ x, z: .95, ry: Math.cos(t * 1.2) * .45 }), t * 3.2, walkA);
    if (sh === "rantA") p.a = [[2.9, .4, .25], [2.9, .4, .25]];
    if (sh === "rantB") p.a = [[.35, .2, .4], [1.55, .05, .45 + .25 * Math.sin(t * 9)]];
    if (sh === "rantC") { p.a = [[2.65, .75, 2.2], [2.65, .75, 2.2]]; p.hp = .12; }
    p.lean = -.06; leo = p;
    leoF = { eyes: "wide", mouth: "rant", brows: sh === "rantC" ? "despair" : "angry", talk: talking(t, "02"), noblink: true };
    if (sh === "rantA") { cam.p.set(.3, 1.4, 4.6 - .2 * u); cam.l.set(.3, 1.3, .9); cam.fov = 42; cam.focus = 3.7; }
    if (sh === "rantB") { cam.p.set(1.9, 1.55, 3.9); cam.l.set(.35, 1.35, .9); cam.fov = 38; cam.focus = 3.4; }
    if (sh === "rantC") { cam.p.set(.15, 1.7, 4.1 - .25 * ss(u, 0, len)); cam.l.set(.25, 1.5, .9); cam.fov = 34; cam.focus = 3.2; }
  } else if (sh === "thud") {     // 3. cheek on his arms on the desk, sobbing
    const drop = ss(u, 0, .25), bnc = .05 * Math.sin(clamp((u - .25) / .3) * Math.PI) * (u > .25 && u < .55 ? 1 : 0);
    leo = seated({ lean: .55 * drop - bnc, hp: -.05 * drop, hr: 1.05 * drop, hy: .05, a: [[.1 + 1.0 * drop, .55 * drop, 1.7 * drop], [.1 + 1.0 * drop, .55 * drop, 1.7 * drop]] });
    leoF = { eyes: u > .3 ? "cry" : "closed", mouth: talking(t, "03") ? "wail" : "sad", brows: "despair", talk: talking(t, "03") };
    PEN.visible = true; const pr = ramp(u, .25, 1.2), fall = Math.max(0, u - 1.2);
    PEN.position.set(.1 + .78 * pr + .2 * fall, Math.max(.008, DESKY + .008 - 2 * fall * fall), .28); PEN.rotation.set(u * 9, 0, Math.PI / 2);
    cam.p.set(.15, 1.3, 3.1); cam.l.set(-.2, .98, -.4); cam.fov = 30; cam.focus = 3.4;
  } else if (sh === "window") {   // 4. WISH 1: at the window, hands clasped, looking up at the moon
    leo = standing({ x: -.68, z: -1.35, ry: Math.PI, hp: -.3, hy: 0, a: [[1.45, -.25, 2.05], [1.45, -.25, 2.05]] });
    leoF = { eyes: "teary", mouth: talking(t, "04") ? "flat" : "smile", brows: "worry", talk: talking(t, "04"), look: [0, .8] };
    cam.p.set(-.66, 1.55, -3.6 + .15 * ss(u, 0, len)); cam.l.set(-.68, 1.62, -1.3); cam.fov = 48; cam.focus = 2.25;
    RM.moon.intensity = 3.2; RM.key.intensity = .8;
  } else if (sh === "teaser1") {  // 5. TEASER 1: the sky turns dramatic; a tiny pink hero arcs across it, rolls, and is gone (sparkle trail)
    const k = ramp(u, .15, 2.1);
    cam.p.set(-.55, 1.5, .2); cam.l.set(-1.0, 1.95, -3.0); cam.fov = 38 - 3 * ss(u, 0, len); cam.focus = 3.4;
    if (k > 0 && k < 1) { cree = flyState(PATH.t1, k, { sc: .2, eyes: "joy" }); trail(PATH.t1, k, .22, cam.p, .035, 30); }
    for (let i = 0; i < RM.clouds.length; i++) RM.clouds[i].position.x = -2.4 + i * 1.4 + u * .9;
    for (const c of RM.curt) c.rotation.z = .06 * Math.sin(u * 3);
    RM.lamp.intensity = 1.2; RM.key.intensity = .5; hemi.intensity = .35; RM.moon.intensity = 1.5;
  } else if (sh === "bed") {      // 6. WISH 2: hugging his knees on the bed
    leo = pose({ x: 2.35, y: -.17, z: -1.0, ry: -Math.PI / 2 + .4, l: [[2.15, 2.45], [2.15, 2.45]], a: [[1.2, .3, 1.5], [1.25, .25, 1.45]], lean: .12, hp: .1, hy: .25 });
    leoF = { eyes: "teary", mouth: talking(t, "05") ? "flat" : "sad", brows: "despair", talk: talking(t, "05"), look: [.3, 0] };
    LEO.phone.visible = true;
    cam.p.set(.05 + .1 * ss(u, 0, len), 1.42, 1.35); cam.l.set(2.3, 1.05, -1.0); cam.fov = 36; cam.focus = 3.2;
  } else if (sh === "teaser2") {  // 7. TEASER 2: closer: he streaks past the window in a blur of pink; curtains blow in, papers lift
    const k = ease(ramp(u, .25, 1.05));
    cam.p.set(.6, 1.35, 1.6); cam.l.set(-.8, 1.55, -2.3); cam.fov = 44; cam.focus = 3.4;
    if (k > 0 && k < 1) { cree = flyState(PATH.t2, k, { sc: .42, eyes: "joy", flap: [.85, 5] }); trail(PATH.t2, k, .3, cam.p, .07, 26);
      FX.speed.visible = true; FX.speed.position.set(cree.x - .3, cree.y, cree.z); FX.speed.rotation.set(0, Math.PI / 2, 0); }
    const gust = ss(u, .5, .8) * (1 - ss(u, 1.6, 2.2));
    RM.curt[0].rotation.x = -.6 * gust; RM.curt[1].rotation.x = -.5 * gust; RM.curt[0].rotation.z = .15 * gust;
    papers(Bs("teaser2") + .6, t, v(-.1, DESKY + .02, .0), v(.3, .35, .4), 5);
    FX.shadow.visible = k > 0 && k < 1; FX.shadow.position.set(lerp(-2.0, 1.5, k), .01, -.6); FX.shadow.scale.set(1.4, .6, 1);
    RM.lamp.intensity = 1.6; RM.key.intensity = .9;
  } else if (sh === "pillow") {   // 8. WISH 3: peeking over the pillow, pleading
    leo = pose({ x: 2.7, y: .72, z: -2.25, l: [[0, .1], [0, .1]], a: [[2.7, .35, .5], [2.7, .35, .5]], hp: -1.05, hy: .12 });
    leoRot = [Math.PI / 2, 0, 0];
    leoF = { eyes: "teary", mouth: talking(t, "06") ? "flat" : "sad", brows: "despair", talk: talking(t, "06") };
    RM.lamp.intensity = 3.0; RM.lamp.position.set(2.65, 1.25, .75);
    cam.p.set(2.6, 1.45, 2.3); cam.l.set(2.7, .82, -.6); cam.fov = 36; cam.focus = 2.7;
  } else if (sh === "hush") {     // 9. the hush: the lights flicker and die, one by one; a pink glow starts to rise outside
    leo = pose({ x: 2.7, y: .72, z: -2.25, l: [[0, .1], [0, .1]], a: [[2.7, .35, .5], [2.7, .35, .5]], hp: -1.05 - .2 * ss(u, .2, .6), hy: .12 + .3 * ss(u, .3, .7) });
    leoRot = [Math.PI / 2, 0, 0]; leoF = { eyes: "wide", mouth: "o", brows: "high", noblink: true };
    const fl = u < .45 ? (Math.floor(u * 40) % 3 === 0 ? .3 : 1) : 0;
    RM.lamp.intensity *= fl; RM.key.intensity *= fl * .6; RM.fill.intensity *= .5; hemi.intensity *= .5; RM.bulb.visible = fl > .5;
    RM.fairy.forEach((b, i) => b.visible = u < .1 + (i % 7) * .07);
    RM.rim.intensity = 2.2 * ss(u, .35, .7); RM.rim.color.set(0xFF7AC0); RM.rim.position.set(-1.05, 1.2, -2.9);
    cam.p.set(.55, 1.85, 2.7); cam.l.set(2.4, .85, -1.0); cam.fov = 44; cam.focus = 3.6;
    dark = .15 * ss(u, .4, .8);
  } else if (sh === "rise") {     // 10. his silhouette rises in the window against the moon, wings spread; his eyes glint; he tucks to launch
    for (const b of RM.fairy) b.visible = false;
    const up2 = ease(ramp(u, 0, .55)), tuck = ss(u, .62, .95);
    cree = { x: -1.05, y: 1.05 + .8 * up2 + .03 * Math.sin(u * 7), z: -2.95, ry: 0, sc: .36, still: true, noblink: true, eyes: "joy", look: [0, -.15],
      wl: [lerp(1.35, -.15, tuck), lerp(0, .7, tuck)], wr: [lerp(1.35, -.15, tuck), lerp(0, .7, tuck)], flap: [.28 * (1 - tuck), 2.4], sq: .16 * tuck, rx: -.12 * tuck, jaw: .2 };
    CREE.dark = false;
    FX.rays.visible = true; FX.rays.position.set(-1.05, cree.y + .15, -3.15); FX.rays.rotation.z = u * .25; FX.rays.children.forEach((r, i) => r.material.opacity = (.1 + .05 * Math.sin(u * 5 + i)) * ss(u, 0, .4));
    FX.halo.visible = true; FX.halo.position.set(-1.05, cree.y + .17, -3.05); FX.halo.scale.setScalar(.9 + .1 * Math.sin(u * 4)); FX.halo.material.opacity = .45 * ss(u, 0, .4);
    const gl = pulse(u, .5, .12);
    if (gl > .02) POST.push(() => { for (let k2 = 0; k2 < 2; k2++) { const sp = FX.sparks[k2]; CREE.eyes[k2].localToWorld(V.set(.03, .04, .16)); sp.visible = true; sp.position.copy(V); sp.scale.setScalar(.1 * gl); sp.material.opacity = gl; sp.material.rotation = u * 2; } });
    RM.bulb.visible = false; RM.lamp.intensity = 0; RM.key.intensity = 0; RM.fill.intensity = .3; hemi.intensity = .2; RM.moon.intensity = 2.6; RM.moon.position.set(-1.05, 2.2, -3.4);
    RM.rim.intensity = 2.2; RM.rim.color.set(0xFFB8DC); RM.rim.position.set(-1.05, cree.y + .2, -2.55);
    cam.p.set(-1.6, 1.0 + .12 * u, .3 - .3 * ss(u, 0, len)); cam.l.set(-1.05, 1.75, -2.7); cam.fov = 40 - 4 * ss(u, 0, len); cam.focus = 3.3;
  } else if (sh === "burst") {    // 11. the window blows open (flash, glass glints) and he rockets through the room: a climb, a barrel roll, a turn
    const open = ease(ramp(u, 0, .12));
    RM.panes[0].rotation.y = -1.85 * open; RM.panes[1].rotation.y = 1.85 * open;
    RM.curt[0].rotation.x = -.5 * open * (1 - .2 * Math.sin(u * 9)); RM.curt[1].rotation.x = -.45 * open * (1 - .2 * Math.sin(u * 8 + 1));
    for (const b of RM.fairy) b.visible = false;
    flash = .55 * Math.exp(-u * 9) * (u > 0 ? 1 : 0);
    FX.shards.forEach((sh2, i) => { const a = u - .02 * hash(i); sh2.visible = a > 0 && a < .7; if (!sh2.visible) return;
      sh2.position.set(-1.05 + (hash(i) - .5) * 1.5 + (hash(i * 2) - .5) * a * 1.6, 1.8 + (hash(i * 3) - .5) * 1.2 + a * (hash(i * 4) - .3) * 1.4 - 1.6 * a * a, -2.3 + a * (1.2 + 2.2 * hash(i * 5)));
      sh2.rotation.set(a * 9 * hash(i * 6), a * 7, a * 5); sh2.material.opacity = .9 * (1 - a / .7) * (.5 + .5 * Math.sin(a * 40 + i)); });
    const k = ease(ramp(u, .02, 1.0) * .92 + ramp(u, .02, 1.0) * .08);
    cam.p.set(.95 + .25 * u, 1.15 + .1 * u, 2.55); cam.fov = 52; cam.focus = 2.6;
    cree = flyState(PATH.in, k, { sc: .3, eyes: "joy", flap: [.8, 4.6] });
    cree.roll += .25 * Math.sin(k * 12);
    const lk = PATH.in.getPointAt(clamp(k - .05)); cam.l.set(lerp(-1.05, lk.x, ss(u, .05, .3)), lerp(1.8, lk.y - .35, ss(u, .05, .3)), lerp(-2.3, lk.z, ss(u, .05, .3)));
    trail(PATH.in, k, .2, cam.p, .06);
    papers(Bs("hero") + 1.7, t, v(-.3, DESKY + .02, -.1), v(.35, .45, .5), 8);
    RM.bulb.visible = false; RM.lamp.intensity = 0; RM.key.intensity = 0; RM.moon.intensity = 4.0; RM.fill.intensity = .55; hemi.intensity = .3;
    RM.rim.intensity = .6; RM.rim.color.set(0xFF8CC6); RM.rim.position.set(cree.x, cree.y - .3, cree.z + .2);
  } else if (sh === "dive") {     // 12. at the top he swings upright facing us and hangs (slow motion, wings flared, eyes on the desk)... then drops
    for (const b of RM.fairy) b.visible = false;
    const hang = ramp(u, 0, .3), drop = ramp(u, .3, .45), flip = ease(ramp(u, 0, .14));
    const top = v(.25, 2.0, .38), y = lerp(top.y + .05 * Math.sin(hang * Math.PI), DESKY + .55, drop * drop);
    cree = { x: lerp(top.x, DESKC.x + .05, ease(drop)), y, z: lerp(top.z, DESKC.z, ease(drop)), ry: lerp(-.9, .1, flip), rx: lerp(.5, .25, flip) + .1 * drop, roll: 0, sc: .32, still: true, noblink: true,
      eyes: "joy", look: [0, -.8], wl: [lerp(.9, 2.0, flip), lerp(.2, -.3, flip)], wr: [lerp(.9, 2.0, flip), lerp(.2, -.3, flip)], flap: [.22 * (1 - drop), 3], feetBack: 1 - flip, sq: -.14 * drop, jaw: .2 };
    FX.speed.visible = drop > 0; FX.speed.position.set(cree.x, cree.y + .35, cree.z); FX.speed.rotation.set(-Math.PI / 2, 0, 0);
    const pts = []; for (let j = 0; j <= 16; j++) { const q = j / 16; pts.push(v(lerp(top.x, cree.x, q), lerp(top.y + .2, cree.y + .08, q), lerp(top.z, cree.z, q))); }
    if (drop > 0) ribbon(pts, v(.1, 1.2, 1.75), .045);
    RM.bulb.visible = false; RM.lamp.intensity = 0; RM.key.intensity = .5; RM.moon.intensity = 3.6; RM.fill.intensity = .6; hemi.intensity = .32;
    RM.rim.intensity = .8; RM.rim.color.set(0xFF8CC6); RM.rim.position.set(cree.x, cree.y - .3, cree.z + .3);
    cam.p.set(.1, lerp(1.55, DESKY + .3, ss(u, .28, .45)), 1.75); cam.l.set(lerp(.24, .08, ss(u, .28, .45)), lerp(1.95, DESKY + .3, ss(u, .28, .45)), lerp(.38, .1, ss(u, .28, .45))); cam.fov = 42; cam.focus = 1.5;
  } else if (sh === "landing") {  // 13. the superhero landing: impact (flash, air blast, dust, shake), the lights come back in a wave; he rises proud
    const I = .13;                                                         // impact at Bs("hero") + 3.03, on the music's drop
    const fall = ramp(u, 0, I), crouch = u < I ? 0 : 1 - ss(u, .62, 1.0), rise = ss(u, .62, 1.0);
    const sqI = u > I ? .14 * Math.exp(-(u - I) * 8) * Math.cos((u - I) * 16) : -.1;
    cree = { x: DESKC.x + .05, y: lerp(DESKY + .55, DESKY, fall * fall), z: DESKC.z, ry: lerp(.1, -.08, rise), sc: .34, still: u < .9, noblink: u < .8,
      sq: u < I ? -.1 : sqI + .05 * crouch, rx: .22 * crouch - .08 * rise, roll: .05 * crouch,
      wl: [lerp(2.2, .5, rise), lerp(.75, .5, rise)], wr: [lerp(.15, .5, rise), lerp(-1.15, .5, rise)],
      eyes: u < .95 ? "joy" : "happy", look: [lerp(0, .25, rise), lerp(-.5, .25, rise)], jaw: u < .62 ? .2 : .2 + .5 * pulse(u, 1.0, .15), feetSplay: .25 * crouch };
    if (u > I) { const r = ramp(u, I, I + .6);
      FX.ring.visible = r < 1; FX.ring.position.set(DESKC.x + .05, DESKY + .005, DESKC.z); FX.ring.scale.setScalar(.05 + .75 * ease(r)); FX.ring.material.opacity = .75 * (1 - r);
      const rb = ramp(u, I, I + .35); FX.blast.visible = rb < 1; FX.blast.position.set(DESKC.x + .05, DESKY + .14, DESKC.z + .05); FX.blast.lookAt(cam.p); FX.blast.scale.setScalar(.06 + .9 * ease(rb)); FX.blast.material.opacity = .7 * (1 - rb);
      FX.dust.forEach((d, i) => { const a = i / FX.dust.length * 6.283, rr2 = .1 + .55 * ease(r) * (.7 + .3 * hash(i)); d.visible = r < 1; d.position.set(DESKC.x + .05 + Math.cos(a) * rr2, DESKY + .04 + .1 * r * hash(i * 3), DESKC.z + Math.sin(a) * rr2 * .6); d.scale.setScalar(.08 + .22 * r); d.material.opacity = .55 * (1 - r); });
      flash = .45 * Math.exp(-(u - I) * 14); }
    papers(Bs("hero") + 3.03, t, v(DESKC.x + .4, DESKY + .02, DESKC.z - .25), v(.6, .35, -.1), 6);
    // the lights come back in a wave: fairy lights left to right, then the lamp pops on
    const wave = ramp(u, .2, .55); RM.fairy.forEach((b, i) => b.visible = wave > i / RM.fairy.length);
    const lampOn = u > .42 ? 1 : 0; RM.bulb.visible = lampOn > 0; RM.lamp.intensity *= lampOn;
    RM.rim.intensity = 2.6; RM.rim.color.set(0xFF8CC6); RM.rim.position.set(DESKC.x, DESKY + .5, DESKC.z - .45); RM.rim2.intensity = 1.3; RM.rim2.position.set(DESKC.x + .4, DESKY + .3, DESKC.z + .3);
    if (u < I + .02) { RM.key.intensity = .2; hemi.intensity = .3; }
    const sh2 = u > I && u < .55 ? .022 * (1 - ramp(u, I, .55)) : 0;
    const orb = ss(u, .55, len);
    cam.p.set(.05 + .25 * orb + sh2 * Math.sin(u * 90), DESKY + .1 - .02 * orb + sh2 * Math.cos(u * 77), 2.15 - .45 * ss(u, .45, len)); cam.l.set(.06, DESKY + .2 + .04 * rise, DESKC.z); cam.fov = 34; cam.focus = 1.6;
    bloomS = .12 + .25 * Math.exp(-Math.max(0, u - I) * 6) * (u > I ? 1 : 0);
    const gl = pulse(u, 1.08, .09);
    if (gl > .02) POST.push(() => { CREE.eyes[1].localToWorld(V.set(.035, .045, .16)); FX.glint.visible = true; FX.glint.position.copy(V); FX.glint.scale.setScalar(.12 * gl); FX.glint.material.rotation = u * 1.5; FX.glint.material.opacity = gl; });
  } else if (sh === "whoa") {     // 9b. the creator turns: jaw drop
    const turn = ss(u, 0, .3);
    leo = pose({ x: 2.3, y: -.17, z: -1.0, ry: -Math.PI / 2 - .25 + .3 * turn, l: [[1.5, 1.5], [1.5, 1.5]], a: [[.45, .55, .3], [.45, .55, .3]], lean: -.15 * turn, hp: -.1, hy: .35 * turn });
    leoF = { eyes: "wide", mouth: talking(t, "07") ? "wail" : "gasp", brows: "high", noblink: true };
    cam.p.set(.6, 1.62, .1); cam.l.set(2.3, 1.42, -1.0); cam.fov = 34 - 4 * ss(u, 0, len); cam.focus = 2.0;
  } else if (sh === "say") {      // 11. "Say no more."
    const hopS = Math.max(0, Math.sin(clamp((u - 1.05) / .32) * Math.PI)) * .05;
    cree = { x: DESKC.x, y: DESKY + hopS, z: DESKC.z, ry: .2, sc: .34, rx: -.08, eyes: u < 1.0 ? "proud" : "joy", wink: u > 1.0 && u < 1.45 ? 1 : 0,
      wl: [.45, .5], wr: [lerp(.45, 1.6, ss(u, .1, .3)) - .9 * ss(u, .95, 1.1), lerp(.5, -.9, ss(u, .1, .3))], jaw: creeJaw(t), talk: true, look: [.4, .15], sq: hopS > 0 ? -.06 : .05 * pulse(u, .55, .1) };
    RM.rim.intensity = 2.0; RM.rim.position.set(DESKC.x, DESKY + .45, DESKC.z - .45);
    cam.p.set(-.4, DESKY + .42, 2.25); cam.l.set(DESKC.x, DESKY + .22, DESKC.z); cam.fov = 30; cam.focus = 2.25;
  } else if (sh === "fix1") {     // 12. the film strip: he walks it with his magnifier, taps second three
    FX.strip.visible = true;
    const walkU = ramp(u, .2, 1.6), x = lerp(.42, -.28, sm(walkU));
    const tap = ss(u, 1.65, 1.85) * (1 - ss(u, 2.3, 2.6));
    cree = { x, y: DESKY, z: .2, ry: -.35 + .35 * ss(u, 1.5, 1.7), sc: .3, eyes: tap > .5 ? (u > 2.1 ? "joy" : "wide") : (walkU > 0 && walkU < 1 ? "focus" : "curious"), wl: [.15 + 2.2 * tap, .3 * tap], wr: [1.9, .5], jaw: creeJaw(t), talk: true, look: [-.3, .9], mag: "hand", magRz: .2, step: walkU > 0 && walkU < 1 ? Math.sin(u * 14) : 0, roll: walkU > 0 && walkU < 1 ? .14 * Math.sin(u * 14) : 0 };
    if (walkU > 0 && walkU < 1) { cree.y += Math.abs(Math.sin(u * 14)) * .018; cree.wl = [cree.wl[0] + .25 * Math.sin(u * 14), cree.wl[1]]; cree.sq = -.04 * Math.abs(Math.cos(u * 14)); }
    for (let i = 0; i < FX.frames.length; i++) { const f = FX.frames[i], hot = i === 1 ? ss(u, 1.8, 2.0) : 0; f.position.y = DESKY + .42 + .012 * Math.sin(u * 2 + i); f.edge.material.color.set(hot > 0 ? 0xFF6A5A : 0xFFFFFF); f.scale.setScalar(1 + .2 * hot); }
    leo = standing({ x: -.35, z: -.8, ry: .1, lean: .3, hp: .22, hy: -.12, a: [[.5, .15, .9], [.5, .15, .9]] });
    leoF = { eyes: "wide", mouth: talking(t, "08") ? "o" : "o", brows: "high", talk: talking(t, "08") };
    cam.p.set(-.08, 1.36, 2.6 - .2 * ss(u, 0, len)); cam.l.set(-.12, 1.15, -.1); cam.fov = 40; cam.focus = 2.6;
  } else if (sh === "fix2") {     // 13. the reel cards: one glows gold
    FX.cards.visible = true;
    for (let i = 0; i < 5; i++) {
      const c = FX.cardL[i], a = (i - 2) * .42 * ss(u, .1, .7), flip = ss(u, .5 + i * .18, .75 + i * .18);
      c.position.set(DESKC.x + Math.sin(a) * .36, DESKY + .42 + Math.cos(a) * .1 - .08, DESKC.z - .12); c.rotation.set(0, Math.PI * (1 - flip) + a * -.3, -a * .5);
      const gold = i === 3 ? ss(u, 1.5, 1.8) : 0; c.cmat.emissiveIntensity = .5 * gold; c.scale.setScalar(1 + .2 * gold);
    }
    const hop2 = u > 1.6 ? Math.max(0, Math.sin((u - 1.6) * 10)) * .045 * (1 - ss(u, 2.2, 2.5)) : 0;
    cree = { x: DESKC.x, y: DESKY + hop2, z: DESKC.z + .05, ry: 0, sc: .3, eyes: u > 1.6 ? "happy" : "joy", wl: [.4 + (u > 1.6 ? 1.8 : 0), 0], wr: [1.2 + .9 * Math.sin(u * 4) * (u < 1.6 ? 1 : 0) + (u > 1.6 ? 1.0 : 0), .3], flap: u > 1.6 ? [.25, 5] : null, jaw: creeJaw(t), talk: true, look: [0, .8], sq: hop2 > 0 ? -.06 : 0 };
    leo = standing({ x: -.45, z: -.8, ry: .2, lean: .15, hp: .1, a: [[.3, .12, .3], [1.55 * ss(t, Ls("09") - .3, Ls("09")), .05, .1]] });
    leoF = { eyes: "wide", mouth: talking(t, "09") ? "laugh" : "o", brows: "high", talk: talking(t, "09") };
    cam.p.set(-.55, 1.42, 2.3); cam.l.set(.0, 1.15, -.1); cam.fov = 40; cam.focus = 2.35;
  } else if (sh === "fix3") {     // 14. the DM machine: he pulls the lever, paper planes stream out of the phone
    FX.mach.visible = true;
    const pull = ss(u, .7, .95);
    FX.lever.rotation.z = .5 - 1.1 * pull; FX.machLight.material.color.set(pull > .5 ? 0x5BE3B0 : 0x3A3A3A);
    const cheer = ss(u, 1.3, 1.5); const hop3 = cheer * Math.max(0, Math.sin((u - 1.3) * 9)) * .04;
    cree = { x: DESKC.x + .05, y: DESKY + hop3, z: .2, ry: .6 - .4 * cheer, sc: .3, eyes: cheer > .3 ? "happy" : (u < .95 ? "joy" : "joy"), flap: cheer > .3 ? [.3, 6] : null, wl: [lerp(.3, 2.6, cheer), 0], wr: [lerp(1.4 - .5 * pull, 2.6, cheer), lerp(.6 + .4 * pull, 0, cheer)], jaw: creeJaw(t), talk: true, look: [.6, .2], sq: .05 * Math.sin(u * 9) * (1 - pull) };
    RM.triScr.color.set(0xFFFFFF);
    for (let i = 0; i < FX.planes.length; i++) {
      const p = FX.planes[i], a = u - .95 - i * .13; p.visible = a > 0 && a < 1.6;
      if (!p.visible) continue;
      const k = a / 1.6, o = v(.25, DESKY + .2, .05);
      p.position.set(o.x - .35 * k + .25 * Math.sin(i * 1.7) * k, o.y + .5 * k + .1 * Math.sin(k * 6 + i), o.z + 1.6 * k * (.7 + .3 * hash(i)));
      p.lookAt(p.position.x - .35, p.position.y + .4, p.position.z + 1.6); p.scale.setScalar(1.5);
    }
    leo = standing({ x: -.4, z: -.8, ry: .1, lean: -.05, hp: -.1, a: u > 1.1 ? [[2.6, .75, 2.2], [2.6, .75, 2.2]] : [[.4, .4, .4], [.4, .4, .4]] });
    leoF = { eyes: u > 1.1 ? "happy" : "wide", mouth: u > 1.1 ? "laugh" : "gasp", brows: "high", noblink: true };
    cam.p.set(.85, 1.36, 2.3); cam.l.set(.1, 1.1, -.2); cam.fov = 42; cam.focus = 2.3;
  } else if (sh === "hug") {      // 15. he scoops Cree up: happy tears; Cree pats his head
    leo = standing({ x: -.1, z: .8, ry: .15, lean: .08, hp: .2, hr: .18, a: [[1.0, -.2, 1.95], [1.0, -.2, 1.95]] });
    leoF = { eyes: "sob", mouth: talking(t, "10") ? "laugh" : "grin", brows: "worry", talk: talking(t, "10") };
    cree = { x: 0, y: 0, z: 0, ry: -.3, sc: .34, eyes: talking(t, "10") || u < .6 ? "happy" : "soft", blush: .7, wl: [.4, .2], wr: [2.7, .3 + .35 * Math.sin(u * 9)], jaw: creeJaw(t), talk: true, noblink: true, attach: true, roll: .12 * Math.sin(u * 2.2) };
    cam.p.set(.3, 1.6, 3.4); cam.l.set(-.05, 1.42, .8); cam.fov = 36; cam.focus = 2.65;
  } else if (sh === "end") {      // 16. end card plate: Cree alone in a soft pink space, pointing up at the wordmark
    RM.visible = false; for (const b of RM.fairy) b.visible = false;
    scene.background = tmpC.set(0x3A1430).clone();
    const hop = Math.max(0, Math.sin(clamp((u - 1.2) / .45) * Math.PI)) * .06;
    cree = { x: 0, y: hop, z: 0, ry: -.15, sc: .34, eyes: u > 1.5 ? "happy" : "joy", wl: [.3, 0], wr: [2.75 + .25 * Math.sin(u * 8) * (u < 1.2 ? 1 : 0), -.25], jaw: creeJaw(t), talk: true, look: [.3, .9], sq: hop > 0 ? -.05 : .04 * pulse(u, 1.67, .08) };
    hemi.color.set(0xFFC8E4); hemi.groundColor.set(0x6A2050); hemi.intensity = .55; sun.intensity = .75; sun.color.set(0xFFF0F6); sun.position.set(1.5, 4, 3); sun.target.position.set(0, 0, 0);
    RM.lamp.intensity = 0; RM.moon.intensity = 0; RM.fill.intensity = 0; RM.key.intensity = 0; RM.rim.intensity = 3; RM.rim.position.set(0, .45, -.4);
    cam.p.set(0, .34, 2.1); cam.l.set(0, .5, 0); cam.fov = 32; cam.focus = 2.1;
  }

  if (leo) { placeToy(LEO, true, idle(leo, t, LEO.seed), leoF); if (leoRot) LEO.root.rotation.set(...leoRot); else LEO.root.rotation.x = LEO.root.rotation.z = 0; }
  else placeToy(LEO, false);
  LEO.root.updateMatrixWorld(true);
  if (cree && cree.attach) { LEO.torso.localToWorld(V.set(0, .32, .3)); cree.x = V.x; cree.y = V.y - .02; cree.z = V.z; }
  if (window.CREE_TEST) cree = { ...(cree || {}), ...window.CREE_TEST };     // portrait tests only (never set in the video)
  placeCree(!!cree, cree || {});
  for (const f of POST) f();
  if (LEO.phone.visible) { LEO.phone.getWorldPosition(V); phoneL.position.copy(V).add(V2.set(0, .05, .25)); }
  return { cam, bloomS, vig, dark, flash };
}

function renderAt(t) {
  if (!TEX.ready) return;
  NOW = t;
  const cv = window.CR_COVER;
  const r = shoot(cv ? cv.t : t);
  const cam = r.cam;
  camera.position.copy(cam.p); camera.fov = cam.fov;
  const look = cam.l.clone();
  if (cv && cv.cam) { camera.position.set(...cv.cam); look.set(...cv.look); camera.fov = cv.fov ?? camera.fov; }
  camera.updateProjectionMatrix(); camera.up.set(0, 1, 0); camera.lookAt(look);
  scene.updateMatrixWorld(true);
  cocPass.uniforms.uF.value = cam.focus; cocPass.uniforms.uAp.value = cam.ap;
  const gu = grade.uniforms;
  gu.uTime.value = t; gu.uWarm.value = .05; gu.uCool.value = 0; gu.uSat.value = 1.04; gu.uCon.value = .04; gu.uVig.value = r.vig; gu.uTint.value = 0;
  gu.uFlash.value = r.flash || 0; gu.uCA.value = 0; gu.uKeep.value = 0; gu.uGrain.value = 0; gu.uTop.value = 0; gu.uDark.value = r.dark;
  bloom.strength = r.bloomS;
  Object.assign(sun.shadow.camera, { left: -5, right: 5, top: 5, bottom: -5, near: 1, far: 30 }); sun.shadow.camera.updateProjectionMatrix();
  renderer.setRenderTarget(sceneRT); renderer.render(scene, camera); renderer.setRenderTarget(null);
  composer.render();
}
