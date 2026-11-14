
// ---------------------------------------------------------------- cue times (window.CT, from build/generate.py)
const v = (x, y, z) => new THREE.Vector3(x, y, z);
const Ls = (k) => C.lines[k][0], Le = (k) => C.lines[k][1], Bs = (k) => C.beats[k][0], Be = (k) => C.beats[k][1];
const talking = (t, k) => t > Ls(k) - .03 && t < Le(k) + .03;
const wordT = (k, i) => { const ws = C.words.filter((w) => w.take === k); return ws[Math.min(i, ws.length - 1)].s; };
const SHOTS = [
  ["phone", 0], ["rant", Ls("02") - .15], ["thud", Bs("thud")], ["window", Ls("04") - .1], ["reveal1", Bs("reveal1")],
  ["bed", Ls("05") - .1], ["reveal2", Bs("reveal2")], ["pillow", Ls("06") - .1], ["hero", Bs("hero")], ["whoa", Ls("07") - .08],
  ["say", Bs("say")], ["fix1", Bs("fix1")], ["fix2", Bs("fix2")], ["fix3", Bs("fix3")], ["hug", Ls("10") - .15], ["end", Bs("endin")],
];
const shotAt = (t) => { let k = 0; for (let i = 0; i < SHOTS.length; i++) if (t >= SHOTS[i][1]) k = i; return [SHOTS[k][0], t - SHOTS[k][1], (SHOTS[k + 1] ? SHOTS[k + 1][1] : DUR) - SHOTS[k][1]]; };
const DESKC = v(.05, DESKY, .12);          // where Cree stands on the desk
const seated = (o = {}) => pose({ x: SEAT.x, y: SITY, z: SEAT.z, ry: 0, l: [[1.5, 1.5], [1.5, 1.5]], a: [[.95, .18, 1.25], [.95, .18, 1.25]], hp: .1, ...o });
const standing = (o = {}) => pose({ a: [[.1, .12, .15], [.1, .12, .15]], ...o });

// ---------------------------------------------------------------- one frame
const CAM = { p: v(0, 1.5, 3), l: v(0, 1, 0), fov: 40, focus: 3, ap: .05 };
function shoot(t) {
  const [sh, u, len] = shotAt(t);
  // defaults: the room at night, nothing special on
  CREE.dark = false;
  RM.visible = true; RM.hall.visible = true;
  for (const k of ["strip", "cards", "mach", "glow", "glow2", "rays", "dust", "door"]) FX[k].visible = false;
  for (const p of FX.planes) p.visible = false;
  PEN.visible = false; LEO.phone.visible = false;
  scene.background = tmpC.set(0x1A1224).clone(); scene.fog.color.set(0x1A1224); scene.fog.near = 30; scene.fog.far = 80;
  hemi.color.set(0x9C88D6); hemi.groundColor.set(0x2E1E2E); hemi.intensity = .55;
  sun.color.set(0x9CC4FF); sun.intensity = .45; sun.target.position.set(0, 0, -.5); sun.position.set(-3.2, 5, 3.5);
  RM.key.intensity = 3.2; RM.fill.intensity = 1.6; RM.lamp.intensity = 1.4; RM.moon.intensity = 0; RM.hallL.intensity = .6; RM.hero.intensity = 0; RM.gold.intensity = 0;
  phoneL.intensity = 0; RM.triScr.color.set(0xFFE3F1); RM.bedScr.color.set(0xFFE3F1); RM.lampShade.emissiveIntensity = .8;
  for (const b of RM.fairy) b.visible = true;
  let bloomS = .42, sat = 1.06, vig = .42, dark = 0;
  let cree = null, leo = null, leoF = {}, leoRot = null;
  const cam = CAM;

  if (sh === "phone") {             // 1. extreme close-up: the phone's glow on his face; then he slides off the chair
    const slide = ss(t, Le("01") + .05, Ls("02") - .2);
    leo = seated({ y: SITY - .75 * slide, z: SEAT.z + .1 * slide, hp: -.05 - .25 * slide, hy: -.18, a: [[.3, .15, .3], [1.55, -.15, 1.75]], lean: -.06 + .1 * slide });
    leoF = { eyes: "wide", mouth: talking(t, "01") ? (Math.floor(t * 7) % 2 ? "wavy" : "gasp") : "wavy", brows: "despair", noblink: true };
    LEO.phone.visible = true; LEO.scr.color.set(0xDDE8FF);
    cam.p.set(.05, 1.7, 1.75 - .2 * ss(u, 0, 3.2)); cam.l.set(-.02, 1.45 - .12 * slide, -.62); cam.fov = 36; cam.focus = 2.3; cam.ap = .06;
    RM.key.intensity = .9; RM.fill.intensity = .5; hemi.intensity = .3;
    phoneL.intensity = 1.4;
  } else if (sh === "rant") {     // 2. the rant: pacing, arms up, counting, hands in his hair
    const ph = u * 3.4, x = .3 + .55 * Math.sin(u * 1.1);
    const w1 = wordT("02", 1), w2 = wordT("02", 5), w3 = wordT("02", 9);
    const arms = kf(t, [[w1 - .5, { a0: .55, a1: .55, s0: .55, e0: .5 }], [w1 - .05, { a0: 2.9, a1: 2.9, s0: .35, e0: .2 }], [w2 - .3, { a0: 2.7, a1: 2.7, s0: .35, e0: .2 }],
      [w2, { a0: .4, a1: 1.6, s0: .2, e0: .5 }], [w3 - .3, { a0: .4, a1: 1.6, s0: .2, e0: .5 }], [w3, { a0: 2.6, a1: 2.6, s0: .75, e0: 2.25 }]]);
    const walkA = clamp(1 - ss(t, w3 - .1, w3 + .3)) * .8;
    let p = walk(standing({ x, z: 1.05, ry: Math.cos(u * 1.1) * .55 }), ph, walkA);
    p.a = [[arms.a0, arms.s0, arms.e0], [arms.a1, arms.s0, arms.e0]];
    p.hp = -.1; p.lean = -.05;
    leo = p; leoF = { eyes: "wide", mouth: "rant", brows: t > w3 ? "despair" : "angry", talk: talking(t, "02"), big: true, noblink: true };
    cam.p.set(.3 + .15 * Math.sin(u * .9), 1.45, 5.0 - .3 * ss(u, 0, len)); cam.l.set(.3 + .2 * Math.sin(u * 1.1), 1.25, .8); cam.fov = 44; cam.focus = 3.3; cam.ap = .04;
  } else if (sh === "thud") {     // 3. face-down on the desk, a pen rolls away
    const drop = ss(u, 0, .22), bnc = .06 * Math.sin(clamp((u - .22) / .3) * Math.PI) * (u > .22 && u < .52 ? 1 : 0);
    leo = seated({ lean: .5 * drop - bnc, hp: -.08 * drop, hy: .1 * Math.sin(u * .8) * drop, hr: 1.2 * drop, a: [[.05 + 1.0 * drop, .55 * drop, 1.6 * drop], [.05 + 1.0 * drop, .55 * drop, 1.6 * drop]] });
    leoF = { eyes: u > .3 ? "cry" : "closed", mouth: talking(t, "03") ? "wail" : "sad", brows: "despair", talk: talking(t, "03") };
    PEN.visible = true; const pr = ramp(u, .25, 1.4), fall = Math.max(0, u - 1.4);
    PEN.position.set(.15 + .75 * pr + .25 * fall, DESKY + .008 - 1.8 * fall * fall, .25); PEN.rotation.set(0, 0, Math.PI / 2); PEN.rotation.x = u * 9;
    cam.p.set(-.05, 1.12, 1.85); cam.l.set(-.25, 1.02, -.45); cam.fov = 32; cam.focus = 2.4; cam.ap = .05;
  } else if (sh === "window") {   // 4. at the window, looking up: the first wish
    leo = standing({ x: -1.5, z: -1.72, ry: Math.PI - .6, hp: -.28, hy: .6, a: [[1.75, .05, .5], [.1, .12, .15]] });
    leoF = { eyes: "teary", mouth: talking(t, "04") ? "talk" : "sad", brows: "worry", talk: talking(t, "04") };
    cam.p.set(.45 - .15 * ss(u, 0, len), 1.8, .55 - .15 * ss(u, 0, len)); cam.l.set(-1.45, 1.72, -2.0); cam.fov = 40; cam.focus = 3.1; cam.ap = .04;
    RM.moon.intensity = 2.2; RM.key.intensity = 1.6; hemi.intensity = .4;
  } else if (sh === "reveal1") {  // 5. HALF REVEAL: a small silhouette in the dark doorway, one eye catching the light
    cree = { x: -3.62, y: 0, z: -1.0, ry: Math.PI / 2 - .25, sc: .34, eyes: "open", oneEye: true, noblink: true, wl: [.12, 0], wr: [.12, 0], jaw: .1, look: [0, 0], roll: .12 * ss(u, 1.1, 1.6) * (1 - ss(u, 2.0, 2.4)) };
    CREE.dark = true;
    FX.door.visible = true; FX.door.position.set(-4.4, .55, -1.0); FX.door.lookAt(v(.6, .5, .2)); FX.door.scale.setScalar(1.8 + .1 * Math.sin(u * 2));
    RM.key.intensity = .12; RM.fill.intensity = .15; RM.lamp.intensity = .2; hemi.intensity = .06; sun.intensity = .08; RM.hallL.intensity = 4.5; RM.hallL.position.set(-4.4, .5, -1.0);
    RM.lampShade.emissiveIntensity = .1; for (const b of RM.fairy) b.visible = false;
    cam.p.set(1.5, .32, -.95); cam.l.set(-3.62, .3, -1.0); cam.fov = 27 - 4 * ss(u, 0, len); cam.focus = 5.1; cam.ap = .025;
    bloomS = .7; vig = .6;
  } else if (sh === "bed") {      // 6. hugging his knees on the bed: the second wish
    leo = pose({ x: 2.45, y: -.17, z: -1.05, ry: -Math.PI / 2 + .35, l: [[2.15, 2.5], [2.15, 2.5]], a: [[1.25, .28, 1.55], [1.25, .28, 1.55]], lean: .15, hp: .12, hy: .2 });
    leoF = { eyes: "teary", mouth: talking(t, "05") ? "talk" : "sad", brows: "despair", talk: talking(t, "05") };
    cam.p.set(-.1 + .15 * ss(u, 0, len), 1.45, 1.15); cam.l.set(2.45, 1.0, -1.08); cam.fov = 36; cam.focus = 3.4; cam.ap = .04;
  } else if (sh === "reveal2") {  // 7. HALF REVEAL: two feet land on the desk, dust, the magnifier glints; his face stays out of frame
    const land = ramp(u, 0, .35), y = DESKY + .9 * (1 - land) ** 2;
    const sq = u > .35 ? .22 * Math.exp(-(u - .35) * 7) * Math.cos((u - .35) * 22) : -.08 * land;
    cree = { x: DESKC.x, y, z: DESKC.z, ry: -.15, sc: .34, sq, eyes: "open", wl: [.2, 0], wr: [.2, 0], jaw: creeJaw(t), mag: "desk", magAt: v(.28, DESKY + .012, .26) };
    FX.dust.visible = true; FX.dust.position.set(DESKC.x, DESKY + .01, DESKC.z); const db = ramp(u, .33, 1.6); FX.dust.scale.set(.25 + .5 * db, .12 + .25 * db, .25 + .5 * db); FX.dust.material.opacity = (u > .33 ? 1 : 0) * (1 - db * .7);
    FX.glow2.visible = u > .8; FX.glow2.position.set(.28, DESKY + .03, .3); FX.glow2.lookAt(cam.p); FX.glow2.scale.setScalar(.06 * pulse(u, 1.0, .18) + .001);
    RM.hero.intensity = 2.5; RM.hero.position.set(DESKC.x, DESKY + .5, DESKC.z - .5);
    RM.key.intensity = 1.2; hemi.intensity = .3;
    cam.p.set(.22, DESKY + .01, 1.05); cam.l.set(.06, DESKY - .05, .12); cam.fov = 30; cam.focus = .93; cam.ap = .09;
  } else if (sh === "pillow") {   // 8. face-down in the pillow, the phone buzzing: the third wish
    const lift = ss(t, wordT("06", 9) - .5, wordT("06", 9) + .1);
    leo = pose({ x: 2.7, y: .72, z: -2.25, l: [[0, .1], [0, .1]], a: [[2.7, .35, .5], [2.7, .35, .5]], hp: -1.05 * lift, hy: .15 * lift });
    leoRot = [Math.PI / 2, 0, 0];
    leoF = { eyes: lift > .5 ? "teary" : "closed", mouth: talking(t, "06") ? "talk" : "sad", brows: "despair", talk: talking(t, "06") };
    RM.bedPhone.rotation.y = .06 * Math.sin(t * 60) * (Math.floor(t * 1.5) % 2); RM.bedScr.color.set(0xFFF4FA);
    phoneL.intensity = .35; phoneL.position.set(2.25, .8, -1.35);
    cam.p.set(2.62, 1.05, 1.15); cam.l.set(2.7, .78, -.45); cam.fov = 40; cam.focus = 1.4; cam.ap = .05;
  } else if (sh === "hero") {     // 9. HERO REVEAL: Cree on the desk, light flooding in behind him
    const fl = ss(u, 0, .9);
    cree = { x: DESKC.x, y: DESKY, z: DESKC.z, ry: 0, sc: .34, lean: -.06, eyes: "open", wl: [-.35, -.35], wr: [2.5 * ss(u, .6, 1.2), -.1], jaw: .3, brow: -.18, browY: -.02, look: [0, .1], mag: "hand", magRz: -.1 };
    FX.glow.visible = FX.rays.visible = FX.dust.visible = true;
    FX.glow.position.set(DESKC.x, DESKY + .2, DESKC.z - .35); FX.glow.lookAt(cam.p); FX.glow.scale.setScalar(.05 + .7 * fl);
    FX.rays.position.set(DESKC.x, DESKY + .1, DESKC.z - .5); FX.rays.lookAt(cam.p); FX.rays.rotation.z = u * .12; FX.rays.scale.setScalar(.35 * fl);
    for (const r of FX.rays.children) r.material.opacity = (.35 + .25 * Math.sin(u * 1.7 + r.ray * 1.9)) * fl;
    FX.dust.position.set(DESKC.x, DESKY, DESKC.z - .2); FX.dust.scale.set(1.2, .9, .6); FX.dust.rotation.y = u * .15; FX.dust.material.opacity = .8 * fl;
    RM.hero.intensity = 2.4 * fl; RM.hero.position.set(DESKC.x, DESKY + .35, DESKC.z - .35); RM.gold.intensity = 2 * fl; RM.gold.position.set(DESKC.x + .3, DESKY + .3, DESKC.z + .2);
    RM.key.intensity = 1.0; RM.fill.intensity = .6; hemi.intensity = .25;
    cam.p.set(.05, DESKY + .08 + .04 * ss(u, 0, len), 1.95 - .35 * ss(u, 0, len)); cam.l.set(.05, DESKY + .26, DESKC.z); cam.fov = 34; cam.focus = 1.4; cam.ap = .06;
    bloomS = .42 + .2 * fl;
  } else if (sh === "whoa") {     // 9b. he turns: jaw drop
    const turn = ss(u, 0, .3);
    leo = pose({ x: 2.3, y: -.17, z: -1.0, ry: -Math.PI / 2 - .2 + .25 * turn, l: [[1.5, 1.5], [1.5, 1.5]], a: [[.4, .5, .3], [.4, .5, .3]], lean: -.15 * turn, hp: -.12, hy: .3 * turn });
    leoF = { eyes: "wide", mouth: talking(t, "07") ? "wail" : "gasp", brows: "high", noblink: true };
    RM.hero.intensity = 3.5; RM.hero.position.set(1.4, 1.2, -.9);
    cam.p.set(.45, 1.6, .25); cam.l.set(2.3, 1.3, -1.0); cam.fov = 36 - 4 * ss(u, 0, len); cam.focus = 2.2; cam.ap = .05;
  } else if (sh === "say") {      // 9c. "Say no more."
    cree = { x: DESKC.x, y: DESKY, z: DESKC.z, ry: .25, sc: .34, eyes: u > 1.1 ? "happy" : "open", wl: [-.35, -.35], wr: [.4 + .3 * Math.sin(u * 5), .9], jaw: creeJaw(t), brow: -.1, look: [.4, .1], mag: "hand", magRz: -.4 };
    FX.glow.visible = true; FX.glow.position.set(DESKC.x, DESKY + .25, DESKC.z - .4); FX.glow.lookAt(cam.p); FX.glow.scale.setScalar(1.2);
    RM.hero.intensity = 3; RM.hero.position.set(DESKC.x, DESKY + .35, DESKC.z - .35);
    cam.p.set(-.3, DESKY + .36, 1.75); cam.l.set(DESKC.x, DESKY + .2, DESKC.z); cam.fov = 30; cam.focus = 1.7; cam.ap = .05;
  } else if (sh === "fix1") {     // 10. the film strip: Cree walks it with his magnifier, taps second three
    FX.strip.visible = true;
    const walkU = ramp(u, .2, 1.6), x = lerp(.5, -.36, sm(walkU));
    const tap = ss(u, 1.65, 1.85) * (1 - ss(u, 2.3, 2.6));
    cree = { x, y: DESKY, z: .18, ry: -.35 + .35 * ss(u, 1.5, 1.7), sc: .3, eyes: tap > .5 ? "wide" : "open", wl: [.15 + 2.2 * tap, .3 * tap], wr: [1.9, .5], jaw: creeJaw(t), look: [-.3, .9], mag: "hand", magRz: .2, step: walkU > 0 && walkU < 1 ? Math.sin(u * 14) : 0, roll: walkU > 0 && walkU < 1 ? .08 * Math.sin(u * 14) : 0 };
    for (let i = 0; i < FX.frames.length; i++) { const f = FX.frames[i], hot = i === 1 ? ss(u, 1.8, 2.0) : 0; f.position.y = DESKY + .42 + .015 * Math.sin(u * 2 + i); f.edge.material.color.set(hot > 0 ? 0xFF6A5A : 0xFFC7E3); f.edge.material.opacity = .55 + .45 * hot * (.6 + .4 * Math.sin(u * 12)); f.scale.setScalar(1 + .25 * hot); }
    leo = standing({ x: -.4, z: -.75, ry: .1, lean: .32, hp: .25, hy: -.15, a: [[.5, .15, .9], [.5, .15, .9]] });
    leoF = { eyes: "wide", mouth: talking(t, "08") ? "talk" : "o", brows: "high", talk: talking(t, "08") };
    RM.hero.intensity = 1.5; RM.hero.position.set(-.3, DESKY + .45, .2);
    cam.p.set(-.1, 1.35, 2.6 - .2 * ss(u, 0, len)); cam.l.set(-.16, 1.15, -.1); cam.fov = 40; cam.focus = 2.4; cam.ap = .04;
  } else if (sh === "fix2") {     // 11. the reel cards: one glows gold
    FX.cards.visible = true;
    for (let i = 0; i < 5; i++) {
      const c = FX.cardL[i], a = (i - 2) * .42 * ss(u, .1, .7), flip = ss(u, .5 + i * .18, .75 + i * .18);
      c.position.set(DESKC.x + Math.sin(a) * .38, DESKY + .42 + Math.cos(a) * .12 - .1, DESKC.z - .12); c.rotation.set(0, Math.PI * (1 - flip) + a * -.3, -a * .5);
      const gold = i === 3 ? ss(u, 1.5, 1.8) : 0; c.cmat.emissiveIntensity = i === 3 ? .25 + 1.4 * gold : .25; c.scale.setScalar(1 + .25 * gold);
    }
    cree = { x: DESKC.x, y: DESKY, z: DESKC.z + .05, ry: 0, sc: .3, eyes: u > 1.6 ? "happy" : "open", wl: [.4, 0], wr: [1.2 + .9 * Math.sin(u * 4) * (u < 1.6 ? 1 : 0), .3], jaw: creeJaw(t), look: [0, .8] };
    RM.gold.intensity = 2.5 * ss(u, 1.5, 1.8); RM.gold.position.set(DESKC.x + .2, DESKY + .5, DESKC.z);
    leo = standing({ x: -.45, z: -.75, ry: .2, lean: .15, hp: .1, a: [[.3, .12, .3], [1.55 * ss(t, Ls("09") - .3, Ls("09")), .05, .1]] });
    leoF = { eyes: "wide", mouth: talking(t, "09") ? "laugh" : "o", brows: "high", talk: talking(t, "09") };
    cam.p.set(-.55, 1.42, 2.25); cam.l.set(.0, 1.15, -.1); cam.fov = 40; cam.focus = 2.3; cam.ap = .04;
  } else if (sh === "fix3") {     // 12. the DM machine: Cree pulls the lever, paper planes stream out of the phone
    FX.mach.visible = true;
    const pull = ss(u, .7, .95);
    FX.lever.rotation.z = .5 - 1.1 * pull; FX.machLight.material.color.set(pull > .5 ? 0x5BE3B0 : 0x3A3A3A);
    cree = { x: DESKC.x - .02, y: DESKY, z: .17, ry: .65, sc: .3, eyes: pull > .5 ? "happy" : "open", wl: [.3, 0], wr: [1.4 - .5 * pull, .6 + .4 * pull], jaw: creeJaw(t), look: [.6, .2], sq: .06 * Math.sin(u * 9) * (1 - pull) };
    RM.triScr.color.set(0xFFFFFF);
    for (let i = 0; i < FX.planes.length; i++) {
      const p = FX.planes[i], a = u - .95 - i * .14; p.visible = a > 0 && a < 1.6;
      if (!p.visible) continue;
      const k = a / 1.6, o = v(.55, DESKY + .23, -.05);
      p.position.set(o.x - .4 * k + .25 * Math.sin(i * 1.7) * k, o.y + .55 * k + .12 * Math.sin(k * 6 + i), o.z + 1.6 * k * (.7 + .3 * hash(i)));
      p.lookAt(p.position.x - .4, p.position.y + .4, p.position.z + 1.6); p.scale.setScalar(1.6);
    }
    leo = standing({ x: -.4, z: -.75, ry: .1, lean: -.05, hp: -.1, a: u > 1.1 ? [[2.6, .75, 2.25], [2.6, .75, 2.25]] : [[.4, .4, .4], [.4, .4, .4]] });
    leoF = { eyes: u > 1.1 ? "happy" : "wide", mouth: u > 1.1 ? "laugh" : "gasp", brows: "high", noblink: true };
    cam.p.set(.85, 1.35, 2.3); cam.l.set(.15, 1.1, -.2); cam.fov = 42; cam.focus = 2.25; cam.ap = .04;
  } else if (sh === "hug") {      // 13. he scoops Cree up: happy tears; Cree pats his head
    leo = standing({ x: -.1, z: .75, ry: .15, lean: .05, hp: .18, hr: .2, a: [[1.25, .5, 1.75], [1.25, .5, 1.75]] });
    leoF = { eyes: "sob", mouth: talking(t, "10") ? "laugh" : "grin", brows: "worry", talk: talking(t, "10") };
    cree = { x: 0, y: 0, z: 0, ry: -.3, sc: .34, eyes: "happy", wl: [.4, .2], wr: [2.7, .3 + .35 * Math.sin(u * 9)], jaw: creeJaw(t), noblink: true, attach: true };
    cam.p.set(.35, 1.6, 3.75); cam.l.set(-.05, 1.35, .75); cam.fov = 36; cam.focus = 3.0; cam.ap = .04;
  } else if (sh === "end") {      // 14. end card plate: Cree alone in a pink glow, pointing up at the wordmark
    RM.visible = false; for (const b of RM.fairy) b.visible = false;
    scene.background = tmpC.set(0x2A0C22).clone();
    const hop = Math.max(0, Math.sin(clamp((u - 1.2) / .45) * Math.PI)) * .06;
    cree = { x: 0, y: hop, z: 0, ry: -.15, sc: .34, eyes: u > 1.5 ? "happy" : "open", wl: [.2, 0], wr: [2.75, -.25], jaw: creeJaw(t), look: [.3, .9], sq: hop > 0 ? -.05 : .04 * pulse(u, 1.67, .08) };
    FX.glow.visible = true; FX.glow.position.set(0, .3, -.4); FX.glow.lookAt(cam.p); FX.glow.scale.setScalar(1.5);
    FX.dust.visible = true; FX.dust.position.set(0, -.05, -.3); FX.dust.scale.set(1.6, .9, .4); FX.dust.material.opacity = .6;
    hemi.color.set(0xFFC2E2); hemi.groundColor.set(0x5A1A40); hemi.intensity = .9; sun.intensity = 0; RM.key.intensity = 0; RM.fill.intensity = 0; RM.lamp.intensity = 0; RM.hallL.intensity = 0;
    RM.hero.intensity = 4; RM.hero.position.set(0, .45, -.35); RM.gold.intensity = 1.5; RM.gold.position.set(.4, .5, .5);
    cam.p.set(0, .34, 2.1); cam.l.set(0, .5, 0); cam.fov = 32; cam.focus = 2.1; cam.ap = .03;
  }

  // the creator
  if (leo) { placeChar(LEO, true, idle(leo, t, LEO.seed), leoF); if (leoRot) LEO.root.rotation.set(...leoRot); else LEO.root.rotation.x = LEO.root.rotation.z = 0; }
  else placeChar(LEO, false);
  LEO.root.updateMatrixWorld(true);
  // Cree (in the hug he sits against the creator's chest)
  if (cree && cree.attach) { LEO.torso.localToWorld(V.set(0, .3, .34)); cree.x = V.x; cree.y = V.y - .02; cree.z = V.z; }
  placeCree(!!cree, cree || {});
  if (LEO.phone.visible) { LEO.phone.getWorldPosition(V); phoneL.position.copy(V).add(V2.set(0, .03, -.12)); }
  return { cam, bloomS, sat, vig, dark };
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
  for (const k of ["glow", "glow2", "door"]) if (FX[k].visible) FX[k].lookAt(camera.position);
  cocPass.uniforms.uF.value = cam.focus; cocPass.uniforms.uAp.value = cam.ap;
  const gu = grade.uniforms;
  gu.uTime.value = t; gu.uWarm.value = .08; gu.uCool.value = 0; gu.uSat.value = r.sat; gu.uCon.value = .06; gu.uVig.value = r.vig; gu.uTint.value = 0;
  gu.uFlash.value = 0; gu.uCA.value = .0008; gu.uKeep.value = 0; gu.uGrain.value = .02; gu.uTop.value = 0; gu.uDark.value = r.dark;
  bloom.strength = r.bloomS;
  sun.shadow.camera.left = -5; sun.shadow.camera.right = 5; sun.shadow.camera.top = 5; sun.shadow.camera.bottom = -5; sun.shadow.camera.near = 1; sun.shadow.camera.far = 30;
  sun.shadow.camera.updateProjectionMatrix();
  renderer.setRenderTarget(sceneRT); renderer.render(scene, camera); renderer.setRenderTarget(null);
  composer.render();
}
