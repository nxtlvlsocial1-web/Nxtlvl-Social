// ---------------------------------------------------------------- cue times (window.CT, from build/generate.py)
const v = (x, y, z) => new THREE.Vector3(x, y, z);
const Ls = (k) => C.lines[k][0], Le = (k) => C.lines[k][1];
const talking = (t, k) => t > Ls(k) - .03 && t < Le(k) + .05;
const wordT = (k, i) => { const ws = C.words.filter((w) => w.take === k); return ws[Math.min(i, ws.length - 1)].s; };
const wordAt = (k, txt) => { const w = C.words.find((x) => x.take === k && x.w.toLowerCase().replace(/[^a-z0-9]/g, "").startsWith(txt)); return w ? w.s : Ls(k); };
const SHOTS = [
  ["hook", 0], ["volt", Ls("02") - .12], ["react", Ls("03") - .1], ["step1", Ls("04") - .12], ["answer", Ls("05") - .1],
  ["step2", Ls("06") - .12], ["temple", Ls("07") - .1], ["menu", Ls("08") - .1], ["step3", Ls("09") - .12], ["day9", Ls("10") - .1],
  ["batch", Ls("11") - .12], ["couch", Ls("12") - .12], ["end", Ls("14") - .12],
];
const shotAt = (t) => { let k = 0; for (let i = 0; i < SHOTS.length; i++) if (t >= SHOTS[i][1]) k = i; return [SHOTS[k][0], t - SHOTS[k][1], (SHOTS[k + 1] ? SHOTS[k + 1][1] : DUR) - SHOTS[k][1]]; };
const ease = (x) => x < .5 ? 2 * x * x : 1 - (-2 * x + 2) ** 2 / 2;
const back = (x) => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2; };
const seated = (o = {}) => pose({ x: SEAT.x, y: SITY, z: SEAT.z, ry: 0, l: [[1.5, 1.5], [1.5, 1.5]], a: [[.95, .18, 1.25], [.95, .18, 1.25]], hp: .08, ...o });
const standing = (o = {}) => pose({ a: [[.1, .1, .15], [.1, .1, .15]], ...o });
const STAND = v(-.75, 0, -1.0);                      // Jules's spot in front of the board, left
const CARDP = v(.3, 1.6, -1.75);                    // where the prompt card floats
const POST = [];

// ---------------------------------------------------------------- one frame
const CAM = { p: v(0, 1.5, 3), l: v(0, 1, 0), fov: 40, focus: 3, ap: .03 };
function shoot(t) {
  const [sh, u, len] = shotAt(t);
  RM.visible = true; POST.length = 0;
  for (const k of ["prompt", "day9", "roof", "menu", "clap", "speed", "ring"]) FX[k].visible = false;
  for (const a of [FX.inputs, FX.cols, FX.ticks, FX.steam]) for (const o of a) o.visible = false;
  for (const k of ["ribbon", "rays", "blast", "glint", "halo"]) if (FX[k]) FX[k].visible = false;
  for (const a of [FX.sparks || [], FX.shards || [], FX.dust || []]) for (const o of a) o.visible = false;
  JULES.phone.visible = false;
  scene.background = tmpC.set(0xFDF4F4).clone(); scene.fog.color.set(0xFDF4F4); scene.fog.near = 30; scene.fog.far = 90;
  hemi.color.set(0xFFF8F2); hemi.groundColor.set(0xE8D8CC); hemi.intensity = .9;
  sun.color.set(0xFFF4E4); sun.intensity = 1.1; sun.target.position.set(0, 0, -.6); sun.position.set(-3, 5, 3);
  RM.sunL.intensity = 1.6; RM.key.intensity = 1.5; RM.fill.intensity = 1.0; RM.rim.intensity = 0; RM.pinkL.intensity = 0;
  RM.lapScr.color.set(0xF6FFE6);
  for (const sl of RM.slots) sl.material.color.set(0xF2ECEC);
  // the board: which blocks are filled by now (step three fills them in a wave; the hook shows it empty)
  const S3 = Ls("09"), fillT = (i) => S3 + .35 + i * .075;
  for (let i = 0; i < 30; i++) {
    const b = RM.blocks[i], ft = fillT(i), k = clamp((t - ft) / .22);
    b.visible = k > 0; if (b.visible) { const s = back(k); b.scale.set(s, s, 1); b.position.z = CAL.z + .03 + .05 * (1 - k); }
  }
  // the step notes light up as each step starts
  const stepT = [Ls("04"), Ls("06"), Ls("09")];
  RM.notes.forEach((n, k) => { const on = t >= stepT[k] - .05; n.paper.color.set(on ? 0xCCFB79 : 0xFFFFFF); n.scale.setScalar(1 + .25 * pulse(t, stepT[k] + .1, .12)); });
  let bloomS = .1, vig = .18, dark = 0, flash = 0;
  let volt = null, jules = null, julesF = {}, julesRot = null;
  const cam = CAM; cam.ap = .025;
  const seatedTalk = (k) => ({ talk: talking(t, k) });

  if (sh === "hook") {           // 1. two weeks without posting: slumped at the desk, phone in hand, the board empty behind her
    const slump = ss(u, .2, 1.2);
    jules = seated({ lean: .08 + .1 * slump, hp: .22 + .1 * slump, hy: -.12, a: [[.45, .2, .6], [.9, -.18, 1.45]] });
    julesF = { eyes: u > 2.4 ? "teary" : "open", mouth: "sad", brows: "despair", talk: talking(t, "01"), look: [-.3, -.4] };
    JULES.phone.visible = true;
    RM.sunL.intensity = .9; RM.key.intensity = 1.0; hemi.intensity = .7;
    cam.p.set(-.95, 1.5, 1.15 - .2 * ss(u, 0, len)); cam.l.set(-1.3, 1.5, -1.15); cam.fov = 54; cam.focus = 2.2;
    dark = .06;
  } else if (sh === "volt") {    // 2. Volt zips out of the laptop in a burst of sparkle: "What if one prompt planned your next thirty days?"
    const pop = clamp(u / .45), thirty = wordAt("02", "thirty");
    const lp = v(DESK.x + .05, DESKY + .25, DESK.z - .1);
    volt = { x: lerp(lp.x, -.55, ease(pop)), y: lerp(lp.y, 1.45, ease(pop)), z: lerp(lp.z, -.6, ease(pop)), sc: .2 + .8 * back(pop), ry: -.35, eyes: u < .5 ? "wide" : "happy", talk: talking(t, "02"), floorY: 0,
      hands: [[-.27, .05 + .1 * pulse(u, .6, .2), .08], [.3, .12 + .08 * Math.sin(u * 5), .08]] };
    if (u < .7) for (let i = 0; i < 18; i++) { const sp = FX.sparks[i], a = u - i * .015; sp.visible = a > 0 && a < .6; if (!sp.visible) continue; const an = i * 2.4; sp.position.set(lp.x + Math.cos(an) * a * 1.2, lp.y + .1 + Math.sin(an * 1.3) * a * .8 + a * .4, lp.z + Math.sin(an) * a * .5); const s2 = .08 * (1 - a / .6); sp.scale.set(s2, s2, 1); sp.material.opacity = 1 - a / .6; }
    // the board shimmers on "thirty": a lime wave runs across the empty slots
    RM.slots.forEach((sl, i) => { const w = pulse(t, thirty + .05 + (i % 6) * .03 + Math.floor(i / 6) * .02, .1); sl.material.color.setRGB(lerp(.95, .8, w), lerp(.93, .98, w), lerp(.93, .47, w)); });
    jules = seated({ lean: -.05, hp: -.12, hy: .45, a: [[.4, .2, .5], [.5, .2, .6]] });
    julesF = { eyes: "wide", mouth: "o", brows: "high", noblink: true };
    RM.lapScr.color.set(0xCCFB79);
    cam.p.set(-.35, 1.4, 1.75); cam.l.set(-.85, 1.25, -.75); cam.fov = 50; cam.focus = 2.6;
    flash = .25 * pulse(u, .12, .08);
  } else if (sh === "react") {   // 3. "Thirty?! I can't even plan lunch."
    jules = seated({ lean: -.08, hp: -.05, hy: .2, a: [[2.4, .5, .4], [2.4, .5, .4]] });
    julesF = { eyes: "wide", mouth: talking(t, "03") ? "rant" : "gasp", brows: "high", talk: talking(t, "03"), big: true, noblink: true };
    volt = { x: -.55, y: 1.45, z: -.6, ry: -.6, eyes: "happy", floorY: 0 };
    cam.p.set(-.95, 1.4, .35); cam.l.set(-1.2, 1.3, -1.15); cam.fov = 46; cam.focus = 1.5;
  } else if (sh === "step1") {   // 4. STEP 1: the prompt card floats up; Volt points at its three blanks
    const ap = ss(u, 0, .45);
    FX.prompt.visible = true; FX.prompt.position.set(CARDP.x, CARDP.y - .4 * (1 - ap), CARDP.z); FX.prompt.rotation.set(0, -.12, 0); FX.prompt.scale.setScalar(.6 + .4 * back(ap));
    FX.prompt.children[1].material.map = TEX.prompt; FX.prompt.children[1].material.needsUpdate = true;
    volt = { x: -.35, y: 1.5, z: -1.55, ry: .35, eyes: "open", look: [.6, .1], talk: talking(t, "04"), floorY: 0, hands: [[-.25, -.05, .06], [.32, .1 + .05 * Math.sin(u * 6), .1]] };
    jules = standing({ x: STAND.x - .25, z: STAND.z + .25, ry: .5, lean: .05, a: [[.3, .15, .5], [.3, .15, .5]] });
    julesF = { eyes: "open", mouth: "smile", brows: "up", look: [.6, .2] };
    cam.p.set(.0, 1.5, 1.45); cam.l.set(.0, 1.45, -1.6); cam.fov = 54; cam.focus = 3.1;
  } else if (sh === "answer") {  // 5. "Home workouts. Busy moms. More clients." Each answer flies into its blank
    FX.prompt.visible = true; FX.prompt.position.copy(CARDP); FX.prompt.rotation.set(0, -.12, 0); FX.prompt.scale.setScalar(1);
    const ws = [wordAt("05", "home"), wordAt("05", "busy"), wordAt("05", "more")];
    const allIn = t > ws[2] + .5;
    FX.prompt.children[1].material.map = allIn ? TEX.promptFilled : TEX.prompt; FX.prompt.children[1].material.needsUpdate = true;
    FX.prompt.scale.setScalar(1 + .06 * pulse(t, ws[2] + .5, .08));
    for (let k = 0; k < 3; k++) {
      const c = FX.inputs[k], a = clamp((t - ws[k] + .05) / .55); c.visible = a > 0 && a < 1;
      const from = v(STAND.x + .2, 1.45, STAND.z + .3), to = v(CARDP.x - .2 + k * .15, CARDP.y + .05 - k * .12, CARDP.z + .05), e2 = ease(a);
      c.position.set(lerp(from.x, to.x, e2), lerp(from.y, to.y, e2) + Math.sin(e2 * Math.PI) * .35, lerp(from.z, to.z, e2)); c.rotation.set(0, -.12, (1 - e2) * .4); c.scale.setScalar(1 - .35 * e2);
    }
    const cnt = ws.filter((w) => t > w).length;
    jules = standing({ x: STAND.x, z: STAND.z, ry: .55, lean: .02, a: [[.4, .2, .7], [cnt ? 1.5 : .4, .25, cnt ? .4 : .7]] });
    julesF = { eyes: "open", mouth: "smile", brows: "flat", talk: talking(t, "05"), look: [.5, .2] };
    volt = { x: CARDP.x - .1, y: 2.12, z: CARDP.z + .15, ry: -.2, eyes: allIn ? "happy" : "open", look: [-.6, 0], floorY: 0 };
    if (allIn && t < ws[2] + .9) for (let i = 0; i < 12; i++) { const sp = FX.sparks[i], a = t - ws[2] - .5 - i * .01; sp.visible = a > 0 && a < .4; if (!sp.visible) continue; const an = i * .52; sp.position.set(CARDP.x + Math.cos(an) * (.55 + a), CARDP.y + Math.sin(an) * (.35 + a * .7), CARDP.z + .05); const s2 = .07 * (1 - a / .4); sp.scale.set(s2, s2, 1); sp.material.opacity = 1 - a / .4; }
    cam.p.set(-.25, 1.45, 1.75); cam.l.set(-.2, 1.45, -1.4); cam.fov = 58; cam.focus = 3.0;
  } else if (sh === "step2" || sh === "temple" || sh === "menu") {   // 6-8. STEP 2: three pillars rise; "a temple?" the roof slams on; "a menu" it flips
    const ws = [wordAt("06", "teach"), wordAt("06", "story"), wordAt("06", "proof")];
    const rTemple = Ls("07") + .55, rMenu = Ls("08") + .1;
    const sink = ss(t, rMenu + .1, rMenu + .5);
    for (let k = 0; k < 3; k++) { const c = FX.cols[k], r = clamp((t - ws[k] + .1) / .4); c.visible = r > 0 && sink < 1; c.position.set(.05 + k * .5, -1.05 * (1 - back(r)) - 1.1 * sink, -1.55); c.scale.set(1, 1, 1); c.rotation.y = -.1; }
    const slam = clamp((t - rTemple) / .22);
    if (t > rTemple && t < rMenu + .45) {
      FX.roof.visible = true; const flip = ss(t, rMenu, rMenu + .4);
      FX.roof.position.set(.55, lerp(2.5, 1.06, slam * slam) + .5 * flip, -1.55); FX.roof.rotation.set(flip * Math.PI * .5, -.1, 0); FX.roof.scale.setScalar(1 - .6 * flip);
      if (slam >= 1) { const r2 = clamp((t - rTemple - .22) / .5); FX.dust.forEach((d, i) => { const an = i / FX.dust.length * 6.283; d.visible = r2 < 1; d.position.set(.55 + Math.cos(an) * (.4 + .9 * r2), 1.08 + .15 * r2, -1.55 + Math.sin(an) * .3 * r2); d.scale.setScalar(.1 + .25 * r2); d.material.opacity = .5 * (1 - r2); }); }
    }
    if (t > rMenu + .15) { const m = ss(t, rMenu + .15, rMenu + .55); FX.menu.visible = true; FX.menu.position.set(.55, 1.65 - .3 * (1 - m), -1.6); FX.menu.rotation.set((1 - m) * -1.2, -.08, 0); FX.menu.scale.setScalar(.5 + .5 * back(m)); }
    if (sh === "step2") {
      volt = { x: -.3, y: 1.75, z: -1.35, ry: .45, eyes: "open", look: [.5, -.2], talk: talking(t, "06"), floorY: 0, hands: [[-.27, -.04, .06], [.3, .14, .1]] };
      jules = standing({ x: STAND.x - .3, z: STAND.z + .3, ry: .45, a: [[.2, .12, .3], [.2, .12, .3]] });
      julesF = { eyes: "open", mouth: "smile", look: [.5, .1] };
      cam.p.set(.4, 1.35, 1.75); cam.l.set(.4, 1.1, -1.5); cam.fov = 56; cam.focus = 3.2;
    } else if (sh === "temple") {
      jules = standing({ x: -.3, z: -.9, ry: .45, hr: .2, a: [[.35, .5, 1.6], [.2, .12, .3]] });
      julesF = { eyes: t > rTemple + .2 ? "wide" : "side", mouth: talking(t, "07") ? "talk" : "smirk", brows: "raise1", talk: talking(t, "07"), look: [.4, .3] };
      volt = { x: .55, y: 1.95, z: -1.45, ry: -.1, eyes: t > rTemple + .2 ? "closed" : "open", floorY: 0 };
      const shk = slam > 0 && slam < 1.6 ? .02 * Math.exp(-(t - rTemple) * 8) : 0;
      cam.p.set(.05 + shk * Math.sin(t * 90), 1.45 + shk * Math.cos(t * 80), 2.35); cam.l.set(.12, 1.3, -1.3); cam.fov = 58; cam.focus = 2.9;
    } else {
      volt = { x: 1.25, y: 1.25, z: -1.1, ry: -.55, eyes: t > Ls("08") + .9 ? "happy" : "open", look: [-.5, 0], talk: talking(t, "08"), floorY: 0, hands: [[-.3, .12 + .06 * Math.sin(u * 5), .1], [.27, -.04, .06]] };
      jules = standing({ x: STAND.x - .3, z: STAND.z + .3, ry: .4, a: [[.2, .12, .3], [.2, .12, .3]] });
      julesF = { eyes: t > Ls("08") + .9 ? "happy" : "open", mouth: "grin", look: [.5, .1] };
      cam.p.set(.55, 1.5, 1.85); cam.l.set(.55, 1.45, -1.6); cam.fov = 56; cam.focus = 3.4;
    }
  } else if (sh === "step3") {   // 9. STEP 3: thirty days, each with a hook and a format: the board fills in a wave; the camera sweeps along it
    const k = ss(u, 0, len);
    volt = { x: 2.15, y: 1.7, z: -1.6, ry: -.7, eyes: "happy", talk: talking(t, "09"), floorY: 0, hands: [[-.3, .2 + .08 * Math.sin(u * 7), .1], [.3, .2 + .08 * Math.sin(u * 7 + 1), .1]] };
    jules = standing({ x: STAND.x, z: STAND.z + .1, ry: .7, a: [[.3, .2, .4], [.3, .2, .4]], hp: -.15 });
    julesF = { eyes: "wide", mouth: "o", brows: "high", look: [.6, .4], noblink: true };
    RM.rim.intensity = 1.2; RM.rim.position.set(CAL.cx, CAL.cy, CAL.z + .8);
    cam.p.set(lerp(-.2, 1.05, k), 1.6, lerp(1.9, 1.6, k)); cam.l.set(lerp(.15, .9, k), 1.6, CAL.z); cam.fov = 60; cam.focus = 3.6;
  } else if (sh === "day9") {    // 10. Day nine flies out of its slot; the kettle steams; "I'd watch that!"
    const o = ss(u, .05, .6), p9 = slotPos(8);
    FX.day9.visible = true; FX.day9.position.set(lerp(p9.x, -.35, o), lerp(p9.y, 2.11, o), lerp(p9.z + .1, -.7, o)); FX.day9.rotation.set(0, lerp(0, .12, o), (1 - o) * .3); FX.day9.scale.setScalar(lerp(.35, .61, back(o)));
    RM.blocks[8].visible = u < .1;
    const watch = wordAt("10", "id");
    jules = standing({ x: -1.05, z: -.35, ry: .55, hp: -.1, a: t > watch - .1 ? [[2.6, .6, .4], [2.6, .6, .4]] : [[.6, .3, 1.2], [.6, .3, 1.2]], y: t > watch ? Math.max(0, Math.sin(clamp((t - watch) / .35) * Math.PI)) * .12 : 0 });
    julesF = { eyes: t > watch ? "happy" : "wide", mouth: talking(t, "10") ? "laugh" : "grin", brows: "high", talk: talking(t, "10"), big: true };
    volt = { x: -.2, y: 1.42, z: -.6, ry: -.35, eyes: "happy", floorY: 0 };
    RM.kettle.rotation.z = .03 * Math.sin(t * 40) * ss(u, .8, 1.2);
    FX.steam.forEach((s, i) => { const a = ((u * .9 + i / 6) % 1); s.visible = u > .6; s.position.set(2.75 + .14 + a * .1, .82 + a * .45, .1 + Math.sin(a * 6 + i) * .04); s.scale.setScalar(.6 + a * 1.4); s.material.opacity = .65 * (1 - a); });
    cam.p.set(-.65, 1.6, 2.2); cam.l.set(-.65, 1.6, -.6); cam.fov = 58; cam.focus = 2.6;
  } else if (sh === "batch") {   // 11. one rule: film the whole week in one afternoon. The clapperboard snaps; the first week glows
    const aft = wordAt("11", "afternoon");
    FX.clap.visible = true; FX.clap.position.set(-.35, 1.95, -1.0); FX.clap.rotation.set(0, .1, 0); FX.clapTop.rotation.z = t < aft - .15 ? .55 : lerp(.55, 0, clamp((t - aft + .15) / .1));
    FX.clap.scale.setScalar(1 + .08 * pulse(t, aft, .06));
    for (let i = 0; i < 7; i++) { const b = RM.blocks[i]; b.scale.setScalar(1 + .12 * pulse(t, aft + .15 + i * .05, .1)); }
    RM.rim.intensity = 1.5 * pulse(t, aft + .3, .5); RM.rim.position.set(CAL.cx - .9, CAL.y0, CAL.z + .6);
    volt = { x: -.1, y: 1.35, z: -.8, ry: -.15, eyes: "open", talk: talking(t, "11"), floorY: 0, hands: [[-.22, .0, .2], [.22, .12, .22]], still: true };
    jules = standing({ x: -.95, z: -.55, ry: .4, a: [[.25, .15, .3], [.25, .15, .3]] });
    julesF = { eyes: "open", mouth: "smile", brows: "up", look: [.4, 0] };
    cam.p.set(-.6, 1.55, 1.9); cam.l.set(-.6, 1.55, -1.0); cam.fov = 56; cam.focus = 2.5;
  } else if (sh === "couch") {   // 12-13. "So I'm busy for one afternoon..." "...and posting all week." Feet up on the couch; the week ticks
    const cc = RM.couch.position, ry = RM.couch.rotation.y;
    jules = pose({ x: cc.x - .05, y: .57 - .71, z: cc.z + .12, ry, lean: -.22, hp: -.05, hy: .15, l: [[1.45, 1.4], [1.35, 1.25]], a: [[.3, 1.1, 2.3], [.3, 1.1, 2.3]] });
    julesF = { eyes: talking(t, "12") ? "open" : "happy", mouth: talking(t, "12") ? "talk" : "grin", talk: talking(t, "12"), look: [-.3, 0] };
    volt = { x: cc.x - 1.0, y: 1.3, z: cc.z + .5, ry: .6, eyes: t > Ls("13") ? "wink" : "open", talk: talking(t, "13"), floorY: 0, hands: [[-.27, -.05, .06], [.3, .18, .1]] };
    for (let i = 0; i < 7; i++) { const tk = FX.ticks[i], ta = Ls("13") + .1 + i * .12, p = slotPos(i); tk.visible = t > ta; if (tk.visible) { const s2 = back(clamp((t - ta) / .2)); tk.position.set(p.x + .17, p.y + .12, p.z + .11); tk.scale.setScalar(s2); } }
    cam.p.set(1.0, 1.35, 1.7); cam.l.set(1.45, 1.02, -.9); cam.fov = 58; cam.focus = 2.6;
  } else if (sh === "end") {     // 14-15. the end card plate: both in front of the full board, waving
    jules = standing({ x: -.2, z: -1.1, ry: .2, a: [[.2, .12, .3], [2.7 + .2 * Math.sin(u * 7), .3, .3]] });
    julesF = { eyes: talking(t, "14") ? "open" : "happy", mouth: talking(t, "14") ? "talk" : "grin", talk: talking(t, "14") };
    volt = { x: .6, y: 1.3, z: -1.0, ry: -.2, eyes: talking(t, "15") ? "open" : "happy", talk: talking(t, "15"), floorY: 0, hands: [[-.27, -.04, .06], [.3, .2 + .06 * Math.sin(u * 8), .1]] };
    cam.p.set(.2, 1.65, 2.3); cam.l.set(.2, 1.95, -1.4); cam.fov = 48; cam.focus = 3.4;
  }

  if (jules) { placeJules(true, idle(jules, t, JULES.seed), julesF); if (julesRot) JULES.root.rotation.set(...julesRot); else JULES.root.rotation.x = JULES.root.rotation.z = 0; }
  else placeJules(false);
  JULES.root.updateMatrixWorld(true);
  placeVolt(!!volt, volt || {});
  for (const f of POST) f();
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
  gu.uTime.value = t; gu.uWarm.value = .03; gu.uCool.value = 0; gu.uSat.value = 1.06; gu.uCon.value = .03; gu.uVig.value = r.vig; gu.uTint.value = 0;
  gu.uFlash.value = r.flash || 0; gu.uCA.value = 0; gu.uKeep.value = 0; gu.uGrain.value = 0; gu.uTop.value = 0; gu.uDark.value = r.dark;
  bloom.strength = r.bloomS;
  Object.assign(sun.shadow.camera, { left: -5, right: 5, top: 5, bottom: -5, near: 1, far: 30 }); sun.shadow.camera.updateProjectionMatrix();
  renderer.setRenderTarget(sceneRT); renderer.render(scene, camera); renderer.setRenderTarget(null);
  composer.render();
}
