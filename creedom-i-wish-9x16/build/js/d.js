
// ---------------------------------------------------------------- cue times (window.CT, from build/generate.py)
const v = (x, y, z) => new THREE.Vector3(x, y, z);
const Ls = (k) => C.lines[k][0], Le = (k) => C.lines[k][1], Bs = (k) => C.beats[k][0], Be = (k) => C.beats[k][1];
const talking = (t, k) => t > Ls(k) - .03 && t < Le(k) + .05;
const wordT = (k, i) => { const ws = C.words.filter((w) => w.take === k); return ws[Math.min(i, ws.length - 1)].s; };
// a cut on (nearly) every line, as the skits guide says; the rant is cut into three angles
const SHOTS = [
  ["phone", 0], ["rantA", Ls("02") - .1], ["rantB", wordT("02", 4) - .08], ["rantC", wordT("02", 9) - .08], ["thud", Bs("thud")],
  ["window", Ls("04") - .1], ["teaser1", Bs("teaser1")], ["bed", Ls("05") - .1], ["teaser2", Bs("teaser2")], ["pillow", Ls("06") - .1],
  ["flyin", Bs("hero")], ["landing", Bs("hero") + 1.45], ["whoa", Ls("07") - .1], ["say", Bs("say")],
  ["fix1", Bs("fix1")], ["fix2", Bs("fix2")], ["fix3", Bs("fix3")], ["hug", Ls("10") - .15], ["end", Bs("endin")],
];
const shotAt = (t) => { let k = 0; for (let i = 0; i < SHOTS.length; i++) if (t >= SHOTS[i][1]) k = i; return [SHOTS[k][0], t - SHOTS[k][1], (SHOTS[k + 1] ? SHOTS[k + 1][1] : DUR) - SHOTS[k][1]]; };
const DESKC = v(.05, DESKY, .14);
const seated = (o = {}) => pose({ x: SEAT.x, y: SITY, z: SEAT.z, ry: 0, l: [[1.5, 1.5], [1.5, 1.5]], a: [[.95, .18, 1.25], [.95, .18, 1.25]], hp: .08, ...o });
const standing = (o = {}) => pose({ a: [[.1, .1, .15], [.1, .1, .15]], ...o });
const FLY = { rx: -1.15, wl: [-.25, .35], wr: [2.85, .15], feetBack: 1, eyes: "open", noblink: true, brow: -.15 };
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
  for (const k of ["strip", "cards", "mach", "speed", "trail", "shadow"]) FX[k].visible = false;
  for (const p of FX.planes) p.visible = false; for (const p of FX.papers) p.visible = false;
  PEN.visible = false; LEO.phone.visible = false;
  for (const h of RM.panes) h.rotation.y = 0; for (const c of RM.curt) c.rotation.set(0, 0, 0);
  for (let i = 0; i < RM.clouds.length; i++) RM.clouds[i].position.x = -2.2 + i * 1.4 + ((t * .05 + i * .3) % 1.2);
  scene.background = tmpC.set(0x14102A).clone(); scene.fog.color.set(0x14102A); scene.fog.near = 30; scene.fog.far = 90;
  hemi.color.set(0xB8A8E8); hemi.groundColor.set(0x3A2A3A); hemi.intensity = .55;
  sun.color.set(0xA8C0FF); sun.intensity = .5; sun.target.position.set(0, 0, -.5); sun.position.set(-2.5, 5, 3);
  RM.lamp.intensity = 2.6; RM.moon.intensity = 2.0; RM.fill.intensity = 1.3; RM.key.intensity = 1.8; RM.rim.intensity = 0; RM.rim2.intensity = 0;
  phoneL.intensity = 0; RM.triScr.color.set(0xFFE3F1); RM.lapScr.color.set(0x9FB2D8);
  for (const b of RM.fairy) b.visible = true;
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
    RM.key.intensity = .9; phoneL.intensity = 1.4;
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
    leo = standing({ x: -1.05, z: -1.3, ry: Math.PI + .15, hp: -.38, hy: -.1, a: [[1.45, -.25, 2.05], [1.45, -.25, 2.05]] });
    leoF = { eyes: "teary", mouth: talking(t, "04") ? "flat" : "smile", brows: "worry", talk: talking(t, "04"), look: [0, .8] };
    cam.p.set(-.62, 1.42, -2.18); cam.l.set(-1.0, 1.82, -1.3); cam.fov = 48 - 3 * ss(u, 0, len); cam.focus = 1.0;
    RM.moon.intensity = 3.2; RM.key.intensity = .8;
  } else if (sh === "teaser1") {  // 5. TEASER 1: the sky turns dramatic; a pink streak shoots across, far away
    const k = ramp(u, .3, 1.9), px = lerp(-3.2, 1.6, ease(k));
    cree = { x: px, y: 1.95 + .15 * Math.sin(k * 3), z: -3.05, ry: -Math.PI / 2, ...FLY, sc: .22 };
    FX.trail.visible = k > 0 && k < 1; FX.trail.position.set(px - .45, cree.y, -3.06); FX.trail.scale.set(.9, 1, 1); FX.trail.rotation.set(0, 0, .08);
    for (let i = 0; i < RM.clouds.length; i++) RM.clouds[i].position.x = -2.4 + i * 1.4 + u * .9;
    for (const c of RM.curt) c.rotation.z = .06 * Math.sin(u * 3);
    RM.lamp.intensity = 1.2; RM.key.intensity = .5; hemi.intensity = .35; RM.moon.intensity = 1.5;
    cam.p.set(-.55, 1.5, .2); cam.l.set(-1.0, 1.95, -3.0); cam.fov = 38 - 3 * ss(u, 0, len); cam.focus = 3.4;
  } else if (sh === "bed") {      // 6. WISH 2: hugging his knees on the bed
    leo = pose({ x: 2.35, y: -.17, z: -1.0, ry: -Math.PI / 2 + .4, l: [[2.15, 2.45], [2.15, 2.45]], a: [[1.2, .3, 1.5], [1.25, .25, 1.45]], lean: .12, hp: .1, hy: .25 });
    leoF = { eyes: "teary", mouth: talking(t, "05") ? "flat" : "sad", brows: "despair", talk: talking(t, "05"), look: [.3, 0] };
    LEO.phone.visible = true;
    cam.p.set(.05 + .1 * ss(u, 0, len), 1.42, 1.35); cam.l.set(2.3, 1.05, -1.0); cam.fov = 36; cam.focus = 3.2;
  } else if (sh === "teaser2") {  // 7. TEASER 2: half of him whooshes past the window; curtains blow in, papers lift
    const k = ramp(u, .25, 1.0);
    cree = { x: lerp(-2.6, .6, ease(k)), y: 1.85, z: -2.75, ry: -Math.PI / 2, ...FLY, sc: .5 };
    FX.speed.visible = k > 0 && k < 1; FX.speed.position.set(cree.x - .3, 1.85, -2.75); FX.speed.rotation.set(0, Math.PI / 2, 0);
    const gust = ss(u, .5, .8) * (1 - ss(u, 1.6, 2.2));
    RM.curt[0].rotation.x = -.6 * gust; RM.curt[1].rotation.x = -.5 * gust; RM.curt[0].rotation.z = .15 * gust;
    papers(Bs("teaser2") + .6, t, v(-.1, DESKY + .02, .0), v(.3, .35, .4), 5);
    FX.shadow.visible = k > 0 && k < 1; FX.shadow.position.set(lerp(-2.0, 1.5, k), .01, -.6); FX.shadow.scale.set(1.4, .6, 1);
    RM.lamp.intensity = 1.6; RM.key.intensity = .9;
    cam.p.set(.6, 1.35, 1.6); cam.l.set(-.8, 1.55, -2.3); cam.fov = 44; cam.focus = 3.4;
  } else if (sh === "pillow") {   // 8. WISH 3: peeking over the pillow, pleading
    leo = pose({ x: 2.7, y: .72, z: -2.25, l: [[0, .1], [0, .1]], a: [[2.7, .35, .5], [2.7, .35, .5]], hp: -1.05, hy: .12 });
    leoRot = [Math.PI / 2, 0, 0];
    leoF = { eyes: "teary", mouth: talking(t, "06") ? "flat" : "sad", brows: "despair", talk: talking(t, "06") };
    RM.lamp.intensity = 3.0; RM.lamp.position.set(2.65, 1.25, .75);
    cam.p.set(2.6, 1.45, 2.3); cam.l.set(2.7, .82, -.6); cam.fov = 36; cam.focus = 2.7;
  } else if (sh === "flyin") {    // 9. HERO ENTRANCE: the window bursts open and he flies straight at us
    const open = ease(ramp(u, 0, .3));
    RM.panes[0].rotation.y = -1.75 * open; RM.panes[1].rotation.y = 1.75 * open;
    for (const c of RM.curt) c.rotation.x = -.8 * open * (1 - .3 * Math.sin(u * 6));
    const k = ease(ramp(u, .15, 1.4));
    const P0 = v(-1.05, 1.85, -3.0), P1 = v(-.15, 1.4, .9);
    cree = { x: lerp(P0.x, P1.x, k), y: lerp(P0.y, P1.y, k) + .08 * Math.sin(k * 3), z: lerp(P0.z, P1.z, k), ry: .25, ...FLY, rx: -1.0, sc: .34, look: [0, .4] };
    FX.speed.visible = k > .02; FX.speed.position.set(cree.x, cree.y, cree.z - .3); FX.speed.rotation.set(0, .25, 0);
    papers(Bs("hero") + .15, t, v(-.3, DESKY + .02, -.1), v(.5, .5, .9), 8);
    RM.moon.intensity = 3.5; RM.lamp.intensity = 2.0;
    cam.p.set(.1, 1.25, 1.75); cam.l.set(-.75, 1.62, -2.3); cam.fov = 44; cam.focus = 1.2 + 3 * (1 - k);
  } else if (sh === "landing") {  // 10. the superhero landing on the desk, then he rises, proud
    const k = ramp(u, 0, .28), y = DESKY + .9 * (1 - ease(k));
    const crouch = ss(u, .26, .32) * (1 - ss(u, .9, 1.3));
    const sq = u > .28 ? .25 * Math.exp(-(u - .28) * 6) * Math.cos((u - .28) * 18) : -.1;
    cree = { x: DESKC.x - .25 * (1 - ease(k)), y, z: DESKC.z, ry: -.1, sc: .34, sq: sq + .15 * crouch, rx: .35 * crouch - .5 * (1 - k), eyes: "open", noblink: true, brow: -.18,
      wl: [lerp(.9, -.35, ss(u, .9, 1.3)), lerp(.2, -.35, ss(u, .9, 1.3))], wr: [lerp(2.2, -.35, ss(u, .9, 1.3)), lerp(.9, -.35, ss(u, .9, 1.3))], look: [0, .3 + .3 * crouch] };
    papers(Bs("hero") + 1.2, t, v(DESKC.x + .5, DESKY + .02, DESKC.z - .3), v(.5, .2, -.1), 4);
    RM.rim.intensity = 2.5; RM.rim.position.set(DESKC.x, DESKY + .45, DESKC.z - .45); RM.rim2.intensity = 1.2; RM.rim2.position.set(DESKC.x + .4, DESKY + .3, DESKC.z + .3);
    cam.p.set(.05, DESKY + .12 + .03 * ss(u, 0, len), 1.95 - .2 * ss(u, .3, len)); cam.l.set(.05, DESKY + .22, DESKC.z); cam.fov = 34; cam.focus = 1.75;
  } else if (sh === "whoa") {     // 9b. the creator turns: jaw drop
    const turn = ss(u, 0, .3);
    leo = pose({ x: 2.3, y: -.17, z: -1.0, ry: -Math.PI / 2 - .25 + .3 * turn, l: [[1.5, 1.5], [1.5, 1.5]], a: [[.45, .55, .3], [.45, .55, .3]], lean: -.15 * turn, hp: -.1, hy: .35 * turn });
    leoF = { eyes: "wide", mouth: talking(t, "07") ? "wail" : "gasp", brows: "high", noblink: true };
    cam.p.set(.6, 1.62, .1); cam.l.set(2.3, 1.42, -1.0); cam.fov = 34 - 4 * ss(u, 0, len); cam.focus = 2.0;
  } else if (sh === "say") {      // 11. "Say no more."
    cree = { x: DESKC.x, y: DESKY, z: DESKC.z, ry: .2, sc: .34, eyes: u > 1.0 ? "happy" : "open", wl: [-.35, -.35], wr: [.4 + .25 * Math.sin(u * 5), .9], jaw: creeJaw(t), brow: -.1, look: [.4, .15], mag: "hand", magRz: -.4 };
    RM.rim.intensity = 2.0; RM.rim.position.set(DESKC.x, DESKY + .45, DESKC.z - .45);
    cam.p.set(-.4, DESKY + .42, 2.25); cam.l.set(DESKC.x, DESKY + .22, DESKC.z); cam.fov = 30; cam.focus = 2.25;
  } else if (sh === "fix1") {     // 12. the film strip: he walks it with his magnifier, taps second three
    FX.strip.visible = true;
    const walkU = ramp(u, .2, 1.6), x = lerp(.42, -.28, sm(walkU));
    const tap = ss(u, 1.65, 1.85) * (1 - ss(u, 2.3, 2.6));
    cree = { x, y: DESKY, z: .2, ry: -.35 + .35 * ss(u, 1.5, 1.7), sc: .3, eyes: tap > .5 ? "wide" : "open", wl: [.15 + 2.2 * tap, .3 * tap], wr: [1.9, .5], jaw: creeJaw(t), look: [-.3, .9], mag: "hand", magRz: .2, step: walkU > 0 && walkU < 1 ? Math.sin(u * 14) : 0, roll: walkU > 0 && walkU < 1 ? .08 * Math.sin(u * 14) : 0 };
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
    cree = { x: DESKC.x, y: DESKY, z: DESKC.z + .05, ry: 0, sc: .3, eyes: u > 1.6 ? "happy" : "open", wl: [.4, 0], wr: [1.2 + .9 * Math.sin(u * 4) * (u < 1.6 ? 1 : 0), .3], jaw: creeJaw(t), look: [0, .8] };
    leo = standing({ x: -.45, z: -.8, ry: .2, lean: .15, hp: .1, a: [[.3, .12, .3], [1.55 * ss(t, Ls("09") - .3, Ls("09")), .05, .1]] });
    leoF = { eyes: "wide", mouth: talking(t, "09") ? "laugh" : "o", brows: "high", talk: talking(t, "09") };
    cam.p.set(-.55, 1.42, 2.3); cam.l.set(.0, 1.15, -.1); cam.fov = 40; cam.focus = 2.35;
  } else if (sh === "fix3") {     // 14. the DM machine: he pulls the lever, paper planes stream out of the phone
    FX.mach.visible = true;
    const pull = ss(u, .7, .95);
    FX.lever.rotation.z = .5 - 1.1 * pull; FX.machLight.material.color.set(pull > .5 ? 0x5BE3B0 : 0x3A3A3A);
    cree = { x: DESKC.x + .05, y: DESKY, z: .2, ry: .6, sc: .3, eyes: pull > .5 ? "happy" : "open", wl: [.3, 0], wr: [1.4 - .5 * pull, .6 + .4 * pull], jaw: creeJaw(t), look: [.6, .2], sq: .05 * Math.sin(u * 9) * (1 - pull) };
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
    cree = { x: 0, y: 0, z: 0, ry: -.3, sc: .34, eyes: "happy", wl: [.4, .2], wr: [2.7, .3 + .35 * Math.sin(u * 9)], jaw: creeJaw(t), noblink: true, attach: true };
    cam.p.set(.3, 1.6, 3.4); cam.l.set(-.05, 1.42, .8); cam.fov = 36; cam.focus = 2.65;
  } else if (sh === "end") {      // 16. end card plate: Cree alone in a soft pink space, pointing up at the wordmark
    RM.visible = false; for (const b of RM.fairy) b.visible = false;
    scene.background = tmpC.set(0x3A1430).clone();
    const hop = Math.max(0, Math.sin(clamp((u - 1.2) / .45) * Math.PI)) * .06;
    cree = { x: 0, y: hop, z: 0, ry: -.15, sc: .34, eyes: u > 1.5 ? "happy" : "open", wl: [.2, 0], wr: [2.75, -.25], jaw: creeJaw(t), look: [.3, .9], sq: hop > 0 ? -.05 : .04 * pulse(u, 1.67, .08) };
    hemi.color.set(0xFFC8E4); hemi.groundColor.set(0x6A2050); hemi.intensity = 1.0; sun.intensity = .9; sun.color.set(0xFFE8F2); sun.position.set(1.5, 4, 3); sun.target.position.set(0, 0, 0);
    RM.lamp.intensity = 0; RM.moon.intensity = 0; RM.fill.intensity = 0; RM.key.intensity = 0; RM.rim.intensity = 3; RM.rim.position.set(0, .45, -.4);
    cam.p.set(0, .34, 2.1); cam.l.set(0, .5, 0); cam.fov = 32; cam.focus = 2.1;
  }

  if (leo) { placeToy(LEO, true, idle(leo, t, LEO.seed), leoF); if (leoRot) LEO.root.rotation.set(...leoRot); else LEO.root.rotation.x = LEO.root.rotation.z = 0; }
  else placeToy(LEO, false);
  LEO.root.updateMatrixWorld(true);
  if (cree && cree.attach) { LEO.torso.localToWorld(V.set(0, .32, .3)); cree.x = V.x; cree.y = V.y - .02; cree.z = V.z; }
  placeCree(!!cree, cree || {});
  if (LEO.phone.visible) { LEO.phone.getWorldPosition(V); phoneL.position.copy(V).add(V2.set(0, .03, -.1)); }
  return { cam, bloomS, vig, dark };
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
  gu.uFlash.value = 0; gu.uCA.value = 0; gu.uKeep.value = 0; gu.uGrain.value = 0; gu.uTop.value = 0; gu.uDark.value = r.dark;
  bloom.strength = r.bloomS;
  Object.assign(sun.shadow.camera, { left: -5, right: 5, top: 5, bottom: -5, near: 1, far: 30 }); sun.shadow.camera.updateProjectionMatrix();
  renderer.setRenderTarget(sceneRT); renderer.render(scene, camera); renderer.setRenderTarget(null);
  composer.render();
}
