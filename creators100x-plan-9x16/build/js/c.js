// ================================================================= THE STUDIO (Creators 100X colours: warm off-white, lime, hot pink, ink)
// A bright creator studio. The back wall (z = -2.3) holds the 30-day calendar board (6 x 5 slots); the desk with the laptop
// is front left, Jules's chair behind it; the pink couch, the side table and the kettle are right; a window on the left wall.
const SET = {};
const mkSet = (k) => { const g = new THREE.Group(); g.visible = false; scene.add(g); SET[k] = g; PARENT = g; return g; };
function v3(x, y, z) { return new THREE.Vector3(x, y, z); }
const RM = mkSet("room");
const DESKY = .78, DESK = v3(-1.3, DESKY, -.55), SEAT = v3(-1.3, 0, -1.15), SITY = .52 - .71;
const INKC = 0x101111, PINK = 0xFD0B68, LIME = 0xCCFB79, OFF = 0xFDF4F4;
const rbox = (w, h, d, c, x, y, z, r = .03, o = {}) => box(w, h, d, c, x, y, z, { round: r, ...o });
const soft = (c, o = {}) => new THREE.MeshPhysicalMaterial({ color: c, roughness: .7, sheen: .6, sheenColor: new THREE.Color(0xffffff), sheenRoughness: .6, ...o });
// the calendar board geometry (shared with the shots)
const CAL = { cx: .55, cy: 1.72, z: -2.22, cols: 6, rows: 5, sw: .48, sh: .36, gap: .06 };
CAL.x0 = CAL.cx - (CAL.cols * CAL.sw + (CAL.cols - 1) * CAL.gap) / 2 + CAL.sw / 2;
CAL.y0 = CAL.cy + (CAL.rows * CAL.sh + (CAL.rows - 1) * CAL.gap) / 2 - CAL.sh / 2;
const slotPos = (i) => v3(CAL.x0 + (i % CAL.cols) * (CAL.sw + CAL.gap), CAL.y0 - Math.floor(i / CAL.cols) * (CAL.sh + CAL.gap), CAL.z);
// the plan: which pillar each day gets (0 teach, 1 story, 2 proof), never more than twice in a row
const PLAN = [0, 1, 2, 0, 0, 1, 2, 1, 0, 2, 0, 1, 1, 2, 0, 2, 1, 0, 0, 2, 1, 0, 2, 2, 1, 0, 1, 2, 0, 1];
const PILLC = [LIME, PINK, INKC];
{
  const plank = pix(256, 256, (g) => { px(g, "#D9B38C", 0, 0, 256, 256); for (let j = 0; j < 8; j++) { const c = ["#DDB892", "#D4AD86", "#E0BC97", "#D7B089"][j % 4]; px(g, c, 0, j * 32, 256, 32); px(g, "#C19A73", 0, j * 32, 256, 2); px(g, "#C19A73", (j * 97) % 256, j * 32, 2, 32); } }, false);
  flat(10, 9, new THREE.MeshStandardMaterial({ map: rep(plank, 4, 4), roughness: .5, envMap: ENV, envMapIntensity: .15 }), 0, 0, 0);
  const wallM = mat(OFF, { roughness: .95 }), trim = mat(0xFFFFFF, { roughness: .6 });
  box(10, 3.4, .2, wallM, 0, 1.7, -2.4);                                                   // back wall
  // left wall with a window opening (centre z -.6, y 1.7; 1.5 x 1.3)
  { const z0 = -.6 - .75, z1 = -.6 + .75, y0 = 1.7 - .65, y1 = 1.7 + .65;
    box(.2, 3.4, z0 + 2.4, wallM, -3.2, 1.7, (-2.4 + z0) / 2); box(.2, 3.4, 4.5 - z1, wallM, -3.2, 1.7, (z1 + 4.5) / 2);
    box(.2, y0, z1 - z0, wallM, -3.2, y0 / 2, -.6); box(.2, 3.4 - y1, z1 - z0, wallM, -3.2, (y1 + 3.4) / 2, -.6);
    for (const [w, h, z, y] of [[.08, .08, 0, .65], [.08, .08, 0, -.65]]) box(.14, h, 1.56, trim, -3.12, 1.7 + y, -.6);
    box(.14, 1.38, .08, trim, -3.12, 1.7, -.6 - .76); box(.14, 1.38, .08, trim, -3.12, 1.7, -.6 + .76); box(.14, 1.38, .05, trim, -3.12, 1.7, -.6);
    RM.daylight = plane(1.5, 1.3, new THREE.MeshBasicMaterial({ color: 0xEAF6FF, toneMapped: false }), -3.3, 1.7, -.6, Math.PI / 2); }
  box(.2, 3.4, 9, wallM, 3.3, 1.7, 2);
  box(10, .1, 9, mat(0xFFFFFF, { roughness: .95 }), 0, 3.4, 2, { cast: false });
  box(10, .1, .04, trim, 0, .05, -2.29); box(.04, .1, 9, trim, 3.19, .05, 2);
  // a soft lime and pink glow painted on the back wall corners (the brand page look)
  { const gt = pix(256, 256, (g) => { const a = g.createRadialGradient(0, 0, 0, 0, 0, 256); a.addColorStop(0, "rgba(206,251,143,.85)"); a.addColorStop(1, "rgba(206,251,143,0)"); g.fillStyle = a; g.fillRect(0, 0, 256, 256); }, false);
    const pt = pix(256, 256, (g) => { const a = g.createRadialGradient(256, 0, 0, 256, 0, 256); a.addColorStop(0, "rgba(254,112,179,.7)"); a.addColorStop(1, "rgba(254,112,179,0)"); g.fillStyle = a; g.fillRect(0, 0, 256, 256); }, false);
    plane(3.2, 2.6, new THREE.MeshBasicMaterial({ map: gt, transparent: true, depthWrite: false }), -2.6, 2.3, -2.29);
    plane(3.2, 2.6, new THREE.MeshBasicMaterial({ map: pt, transparent: true, depthWrite: false }), 3.0, 2.3, -2.29); }
  // the calendar board: an ink frame, 30 empty slots with day numbers, a coloured block per slot that pops in
  rbox(3.42, 2.42, .06, gloss(INKC, { roughness: .4 }), CAL.cx, CAL.cy, CAL.z - .05, .05);
  rbox(3.42, .26, .07, gloss(INKC, { roughness: .4 }), CAL.cx, CAL.cy + 1.36, CAL.z - .04, .05);
  RM.slots = []; RM.blocks = [];
  RM.numM = texMat("calnums"); plane(3.3, 2.3, RM.numM, CAL.cx, CAL.cy, CAL.z + .021, 0);
  for (let i = 0; i < 30; i++) {
    const p = slotPos(i);
    RM.slots.push(rbox(CAL.sw, CAL.sh, .03, mat(0xF2ECEC, { roughness: .9 }), p.x, p.y, p.z, .025));
    const g = new THREE.Group(); g.position.set(p.x, p.y, p.z + .03); RM.add(g);
    const c = PILLC[PLAN[i]];
    const b = new THREE.Mesh(new RoundedBoxGeometry(CAL.sw - .02, CAL.sh - .02, .07, 3, .03), gloss(c, { roughness: .35, envMapIntensity: .35 })); b.castShadow = true; g.add(b);
    const icM = texMat("icon" + PLAN[i]); const ic = new THREE.Mesh(new THREE.PlaneGeometry(.22, .22), icM); ic.position.set(-.08, .02, .037); g.add(ic);
    const lnM = new THREE.MeshBasicMaterial({ color: PLAN[i] === 2 ? LIME : INKC, toneMapped: false }); for (let k = 0; k < 2; k++) { const ln = new THREE.Mesh(new THREE.PlaneGeometry(k ? .1 : .14, .025), lnM); ln.position.set(.1, .04 - k * .06, .037); g.add(ln); }
    g.visible = false; RM.blocks.push(g);
  }
  // three sticky notes on the board frame: the step cue (they light lime as each step starts)
  RM.notes = []; for (let k = 0; k < 3; k++) { const n = new THREE.Group(); n.position.set(CAL.cx + 1.95, CAL.cy + .7 - k * .55, CAL.z + .02); n.rotation.z = (k - 1) * .08; RM.add(n); const m = new THREE.MeshStandardMaterial({ color: 0xFFFFFF, roughness: .8 }); const pm = new THREE.Mesh(new RoundedBoxGeometry(.4, .4, .015, 2, .01), m); n.add(pm); const nm = texMat("note" + k); const np = new THREE.Mesh(new THREE.PlaneGeometry(.36, .36), nm); np.position.z = .009; n.add(np); n.paper = m; RM.notes.push(n); }
  // the logo poster (right of the board)
  RM.logoM = texMat("logo"); plane(.9, .9, RM.logoM, 2.55, 1.75, -2.29, 0);
  // the desk: rounded white top, ink legs, a drawer unit
  rbox(1.6, .06, .72, mat(0xFFFFFF, { roughness: .45, envMap: ENV, envMapIntensity: .2 }), DESK.x, DESKY - .03, DESK.z, .02);
  for (const [x, z] of [[.74, .3], [.74, -.3], [-.74, .3], [-.74, -.3]]) rbox(.05, DESKY - .06, .05, mat(INKC), DESK.x + x, (DESKY - .06) / 2, DESK.z + z, .015);
  // laptop (lid open toward the chair), a mug, a phone tripod
  const lap = new THREE.Group(); lap.position.set(DESK.x + .05, DESKY, DESK.z - .02); lap.rotation.y = Math.PI; RM.add(lap); RM.lap = lap;
  rbox(.44, .018, .3, metal(0xC9C9CF, .35), 0, .009, 0, .006, { parent: lap });
  const lid = new THREE.Group(); lid.position.set(0, .015, -.15); lid.rotation.x = -.3; lap.add(lid); rbox(.44, .29, .014, metal(0xC9C9CF, .35), 0, .145, 0, .006, { parent: lid });
  RM.lapScr = new THREE.MeshBasicMaterial({ color: 0xF6FFE6, toneMapped: false }); { const ls = new THREE.Mesh(new THREE.PlaneGeometry(.4, .25), RM.lapScr); ls.position.set(0, .145, .008); lid.add(ls); }
  { const m = new THREE.Group(); m.position.set(DESK.x + .55, DESKY, DESK.z + .12); RM.add(m); cyl(.045, .042, .1, gloss(PINK), 0, .05, 0, 24, { parent: m }); }
  // the chair
  { const C2 = new THREE.Group(); C2.position.set(SEAT.x, 0, SEAT.z); RM.add(C2); const cw = soft(0x101111); rbox(.52, .07, .5, cw, 0, .5, -.02, .03, { parent: C2 }); rbox(.5, .55, .06, cw, 0, .82, -.27, .05, { parent: C2 }); cyl(.025, .025, .38, metal(0xC8C8D0, .3), 0, .3, 0, 10, { parent: C2 });
    for (let k = 0; k < 5; k++) { const a = k * 1.2566; const leg = rbox(.24, .025, .04, cw, Math.sin(a) * .12, .07, Math.cos(a) * .12, .012, { parent: C2 }); leg.rotation.y = a + Math.PI / 2; } }
  // the ring light, front left
  { const R = new THREE.Group(); R.position.set(-2.4, 0, .4); R.rotation.y = .6; RM.add(R); cyl(.014, .014, 1.45, mat(INKC), 0, .72, 0, 10, { parent: R });
    const rh = new THREE.Mesh(new THREE.TorusGeometry(.25, .035, 12, 64), mat(INKC)); rh.position.y = 1.58; R.add(rh); const rg = new THREE.Mesh(new THREE.TorusGeometry(.25, .018, 10, 64), glow(0xFFF6EA)); rg.position.set(0, 1.58, .02); R.add(rg); }
  // the pink couch, a side table with the kettle, a plant
  { const Cc = new THREE.Group(); Cc.position.set(1.85, 0, -.9); Cc.rotation.y = -.35; RM.add(Cc); RM.couch = Cc; const pm = soft(0xFF5FA2);
    rbox(1.6, .38, .8, pm, 0, .3, 0, .1, { parent: Cc }); rbox(1.6, .55, .2, pm, 0, .62, -.32, .1, { parent: Cc }); for (const s of [-1, 1]) rbox(.2, .5, .8, pm, s * .8, .42, 0, .09, { parent: Cc });
    for (const s of [-1, 1]) rbox(.62, .14, .62, soft(0xFF7DB4), s * .36, .54, .04, .07, { parent: Cc }); rbox(.36, .3, .12, soft(LIME), -.45, .74, -.18, .06, { parent: Cc }); }
  { const T = new THREE.Group(); T.position.set(2.75, 0, .1); RM.add(T); cyl(.26, .26, .04, mat(0xFFFFFF, { roughness: .4 }), 0, .6, 0, 32, { parent: T }); cyl(.03, .03, .58, mat(INKC), 0, .3, 0, 10, { parent: T });
    const K = new THREE.Group(); K.position.set(0, .62, 0); T.add(K); RM.kettle = K; cyl(.1, .12, .2, gloss(0xFFFFFF), 0, .1, 0, 24, { parent: K }); cyl(.04, .06, .03, gloss(INKC), 0, .215, 0, 16, { parent: K });
    const sp = cyl(.018, .024, .12, gloss(0xFFFFFF), .12, .12, 0, 10, { parent: K }); sp.rotation.z = -1; const hd = new THREE.Mesh(new THREE.TorusGeometry(.07, .015, 8, 20, Math.PI), gloss(INKC)); hd.position.set(-.1, .14, 0); hd.rotation.z = Math.PI / 2; K.add(hd); }
  { const P = new THREE.Group(); P.position.set(-2.6, 0, -1.7); RM.add(P); cyl(.17, .13, .32, gloss(0xFFFFFF), 0, .16, 0, 20, { parent: P }); for (let j = 0; j < 9; j++) { const l = new THREE.Mesh(new THREE.SphereGeometry(.13, 10, 8), mat(0x5FAE57)); l.position.set((hash(j) - .5) * .3, .45 + hash(j * 3) * .55, (hash(j * 5) - .5) * .3); l.scale.set(.7, 1.3, .7); P.add(l); } }
  // a round rug
  { const rug = new THREE.Mesh(new THREE.CircleGeometry(1.2, 48), soft(0xE7F9C9, { roughness: .95 })); rug.rotation.x = -Math.PI / 2; rug.scale.set(1.4, .85, 1); rug.position.set(.55, .006, -.5); add(rug, false, true); }
  // lights: bright daylight; the shots tune them
  RM.sunL = new THREE.PointLight(0xFFF2E0, 0, 9, 1.2); RM.sunL.position.set(-2.6, 2.2, -.6); scene.add(RM.sunL);
  RM.key = new THREE.PointLight(0xFFF6EE, 0, 7, 1.4); RM.key.position.set(.3, 2.2, 2.2); scene.add(RM.key);
  RM.fill = new THREE.PointLight(0xF2F6FF, 0, 9, 1.2); RM.fill.position.set(2.4, 2.4, 1.6); scene.add(RM.fill);
  RM.rim = new THREE.PointLight(0xCCFB79, 0, 3.5, 1.6); scene.add(RM.rim);
  RM.pinkL = new THREE.PointLight(0xFD0B68, 0, 3.5, 1.6); scene.add(RM.pinkL);
}
// ---------------------------------------------------------------- the story props: the prompt card and its three input cards, the
// pillars, the temple roof that flips into a menu board, the Day 9 card, the clapperboard, the posting ticks
const FX = {};
{
  const card = (w, h, key, c = 0xFFFFFF) => { const g = new THREE.Group(); const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, .02, 3, .025), gloss(c, { roughness: .4, envMapIntensity: .3 })); m.castShadow = true; g.add(m); const fm = texMat(key); const f = new THREE.Mesh(new THREE.PlaneGeometry(w - .02, h - .02), fm); f.position.z = .011; g.add(f); g.visible = false; RM.add(g); return g; };
  FX.prompt = card(1.0, .62, "prompt");
  FX.inputs = [card(.62, .2, "in0"), card(.62, .2, "in1"), card(.62, .2, "in2")];
  FX.day9 = card(1.15, .82, "day9");
  FX.cols = []; const colC = [LIME, PINK, INKC];
  for (let k = 0; k < 3; k++) { const g = new THREE.Group(); RM.add(g); const m = gloss(colC[k], { roughness: .35, envMapIntensity: .35 });
    const sh = new THREE.Mesh(new THREE.CylinderGeometry(.16, .16, 1.0, 16, 1), m); sh.position.y = .5; sh.castShadow = true; g.add(sh);
    for (const y of [.03, .97]) { const cap = new THREE.Mesh(new RoundedBoxGeometry(.44, .07, .44, 2, .02), m); cap.position.y = y; cap.castShadow = true; g.add(cap); }
    for (let f = 0; f < 8; f++) { const a = f / 8 * Math.PI * 2; const fl = new THREE.Mesh(new THREE.BoxGeometry(.02, .9, .02), mat(shc(colC[k], k === 2 ? .25 : -.12))); fl.position.set(Math.sin(a) * .16, .5, Math.cos(a) * .16); g.add(fl); }
    const lm = texMat("pill" + k); const lp = new THREE.Mesh(new THREE.PlaneGeometry(.46, .14), lm); lp.position.set(0, .62, .2); g.add(lp);
    g.visible = false; FX.cols.push(g); }
  // the temple roof (a pediment) and the menu board it flips into
  FX.roof = new THREE.Group(); RM.add(FX.roof);
  { const sh = new THREE.Shape(); sh.moveTo(-.9, 0); sh.lineTo(.9, 0); sh.lineTo(0, .38); sh.lineTo(-.9, 0); const g = new THREE.ExtrudeGeometry(sh, { depth: .4, bevelEnabled: true, bevelThickness: .02, bevelSize: .02, bevelSegments: 2 }); g.translate(0, 0, -.2);
    const pm = gloss(0xFFFFFF, { roughness: .45 }); const r = new THREE.Mesh(g, pm); r.castShadow = true; FX.roof.add(r); const base = new THREE.Mesh(new RoundedBoxGeometry(1.9, .08, .5, 2, .02), pm); base.position.y = -.04; FX.roof.add(base); }
  FX.roof.visible = false;
  FX.menu = card(1.7, .9, "menu", INKC);
  // the clapperboard
  FX.clap = new THREE.Group(); RM.add(FX.clap);
  { const bm = gloss(INKC, { roughness: .4 }); const b = new THREE.Mesh(new RoundedBoxGeometry(.5, .36, .03, 2, .015), bm); b.castShadow = true; FX.clap.add(b); const fm = texMat("clap"); const f = new THREE.Mesh(new THREE.PlaneGeometry(.46, .26), fm); f.position.set(0, -.03, .016); FX.clap.add(f);
    const hinge = new THREE.Group(); hinge.position.set(-.25, .18, 0); FX.clap.add(hinge); FX.clapTop = hinge; const tm = texMat("claptop"); const top = new THREE.Mesh(new RoundedBoxGeometry(.5, .07, .03, 2, .01), bm); top.position.set(.25, .035, 0); hinge.add(top); const tp = new THREE.Mesh(new THREE.PlaneGeometry(.48, .05), tm); tp.position.set(.25, .035, .016); hinge.add(tp); }
  FX.clap.visible = false;
  // the posting ticks (lime check bubbles that pop over the board on the punchline)
  FX.ticks = []; for (let i = 0; i < 7; i++) { const tm = texMat("tick"); const t = new THREE.Mesh(new THREE.PlaneGeometry(.2, .2), tm); t.visible = false; RM.add(t); FX.ticks.push(t); }
  // the kettle's steam puffs
  FX.steam = []; for (let i = 0; i < 6; i++) { const s = new THREE.Mesh(new THREE.SphereGeometry(.05, 10, 8), new THREE.MeshStandardMaterial({ color: 0xFFFFFF, roughness: 1, transparent: true, opacity: .7 })); s.visible = false; RM.add(s); FX.steam.push(s); }
  // speed lines (reused from the house kit)
  const slT = pix(16, 256, (g) => { const gr = g.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, "rgba(255,255,255,0)"); gr.addColorStop(.5, "rgba(255,255,255,.85)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(6, 0, 4, 256); }, false);
  FX.speed = new THREE.Group(); scene.add(FX.speed); FX.speed.visible = false;
  for (let i = 0; i < 10; i++) { const s = new THREE.Mesh(new THREE.PlaneGeometry(.05, 1), new THREE.MeshBasicMaterial({ map: slT, transparent: true, depthWrite: false, opacity: .7 })); s.position.set((hash(i) - .5) * .6, (hash(i * 3) - .5) * .5, -.4 - hash(i * 5) * .6); s.rotation.x = Math.PI / 2; s.scale.y = .5 + hash(i * 7); FX.speed.add(s); }
  FX.ring = new THREE.Mesh(new THREE.RingGeometry(.9, 1, 64), new THREE.MeshBasicMaterial({ color: 0xFFFFFF, transparent: true, opacity: .6, depthWrite: false, side: THREE.DoubleSide })); FX.ring.rotation.x = -Math.PI / 2; FX.ring.visible = false; scene.add(FX.ring);
}
// ---------------------------------------------------------------- the hero FX: a sparkle ribbon behind him in flight, sparks,
// glass glints from the burst window, moon rays behind his silhouette, an air blast and dust on the landing, an eye glint
{
  const glowT = pix(64, 64, (g) => { const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(.3, "rgba(255,225,242,.75)"); gr.addColorStop(1, "rgba(255,150,205,0)"); g.fillStyle = gr; g.fillRect(0, 0, 64, 64); }, false);
  const starT = pix(128, 128, (g) => { g.translate(64, 64); for (const [L, W, a] of [[62, 5, 0], [62, 5, Math.PI / 2], [30, 3, Math.PI / 4], [30, 3, -Math.PI / 4]]) { g.save(); g.rotate(a); const gr = g.createLinearGradient(-L, 0, L, 0); gr.addColorStop(0, "rgba(255,255,255,0)"); gr.addColorStop(.5, "rgba(255,255,255,1)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.beginPath(); g.moveTo(-L, 0); g.lineTo(0, -W); g.lineTo(L, 0); g.lineTo(0, W); g.closePath(); g.fill(); g.restore(); } const gr = g.createRadialGradient(0, 0, 0, 0, 0, 16); gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(-16, -16, 32, 32); }, false);
  const add2 = (o) => { scene.add(o); o.visible = false; return o; };
  // the ribbon: 48 segments, rebuilt every frame from his flight path (see ribbon() in the shots)
  const RN = 48; const rg = new THREE.BufferGeometry();
  rg.setAttribute("position", new THREE.Float32BufferAttribute(new Float32Array(RN * 2 * 3), 3));
  rg.setAttribute("color", new THREE.Float32BufferAttribute(new Float32Array(RN * 2 * 4), 4));
  const idx = []; for (let i = 0; i < RN - 1; i++) { const a = i * 2; idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); } rg.setIndex(idx);
  FX.ribbon = add2(new THREE.Mesh(rg, new THREE.MeshBasicMaterial({ vertexColors: true, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, toneMapped: false })));
  FX.ribbon.frustumCulled = false; FX.ribbonN = RN;
  FX.sparks = []; for (let i = 0; i < 46; i++) { const m = new THREE.SpriteMaterial({ map: i % 5 ? glowT : starT, color: i % 3 ? 0xFFD6EC : 0xFFFFFF, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false }); FX.sparks.push(add2(new THREE.Sprite(m))); }
  // glass glints: small bright flecks thrown in from the window
  FX.shards = []; for (let i = 0; i < 26; i++) { const m = new THREE.Mesh(new THREE.PlaneGeometry(.035, .05), new THREE.MeshBasicMaterial({ color: 0xDDEBFF, transparent: true, opacity: .85, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, toneMapped: false })); FX.shards.push(add2(m)); }
  // moon rays: long soft wedges fanning out from behind him
  const rayT = pix(64, 256, (g) => { const gr = g.createLinearGradient(0, 256, 0, 0); gr.addColorStop(0, "rgba(220,230,255,.9)"); gr.addColorStop(1, "rgba(220,230,255,0)"); g.fillStyle = gr; g.beginPath(); g.moveTo(30, 256); g.lineTo(34, 256); g.lineTo(64, 0); g.lineTo(0, 0); g.closePath(); g.fill(); }, false);
  FX.rays = add2(new THREE.Group()); for (let i = 0; i < 9; i++) { const p = new THREE.Mesh(new THREE.PlaneGeometry(.55, 2.6), new THREE.MeshBasicMaterial({ map: rayT, transparent: true, opacity: .35, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false })); p.geometry.translate(0, 1.3, 0); p.rotation.z = (i - 4) * .36 + (hash(i) - .5) * .15; p.scale.x = .35 + hash(i * 3) * .5; FX.rays.add(p); }
  // the air blast: a bright ring that punches out from the landing, facing the camera
  FX.blast = add2(new THREE.Mesh(new THREE.RingGeometry(.86, 1, 72), new THREE.MeshBasicMaterial({ color: 0xFFE6F3, transparent: true, opacity: .6, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, toneMapped: false })));
  // the eye glint (a four-point star) and a soft halo for the silhouette
  FX.glint = add2(new THREE.Sprite(new THREE.SpriteMaterial({ map: starT, color: 0xFFFFFF, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false })));
  FX.halo = add2(new THREE.Sprite(new THREE.SpriteMaterial({ map: glowT, color: 0xFFB8DC, transparent: true, opacity: .5, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false })));
  // bigger dust puffs for the landing (soft sprites)
  FX.dust = []; for (let i = 0; i < 16; i++) FX.dust.push(add2(new THREE.Sprite(new THREE.SpriteMaterial({ map: glowT, color: 0xF8EEF6, transparent: true, opacity: .5, depthWrite: false }))));
}
// fill the ribbon from points (oldest first), facing the camera; width tapers to the tail
function ribbon(pts, camP, w, col = [1, .42, .74]) {
  const g = FX.ribbon.geometry, P = g.attributes.position.array, C = g.attributes.color.array, N = FX.ribbonN;
  FX.ribbon.visible = pts.length > 1;
  for (let i = 0; i < N; i++) {
    const k = Math.min(pts.length - 1, Math.round(i / (N - 1) * (pts.length - 1))), p = pts[k], q = pts[Math.min(pts.length - 1, k + 1)], o = pts[Math.max(0, k - 1)];
    V.copy(q).sub(o).normalize(); V2.copy(camP).sub(p).normalize(); const side = V.clone().cross(V2).normalize();
    const u = i / (N - 1), ww = w * Math.pow(u, .7);
    for (let s = 0; s < 2; s++) { const j = (i * 2 + s); P[j * 3] = p.x + side.x * ww * (s ? 1 : -1); P[j * 3 + 1] = p.y + side.y * ww * (s ? 1 : -1); P[j * 3 + 2] = p.z + side.z * ww * (s ? 1 : -1);
      const a = Math.pow(u, 1.8) * .5 * (s ? 1 : 1); const wh = Math.pow(u, 6) * .6; C[j * 4] = lerp(col[0], 1, wh); C[j * 4 + 1] = lerp(col[1], 1, wh); C[j * 4 + 2] = lerp(col[2], 1, wh); C[j * 4 + 3] = a; }
  }
  g.attributes.position.needsUpdate = true; g.attributes.color.needsUpdate = true;
}
PARENT = scene;
// ---------------------------------------------------------------- VOLT, the AI sidekick: the Creators 100X tile come to life. A glossy
// ink rounded cube with a lime face screen (friendly dark oval eyes with two shines, a smile that talks, pink cheeks), the
// brand's lightning bolt as an antenna (top half white, bottom half lime), two floating hands; he hovers. Built ~.42 m tall.
const VOLT = { root: new THREE.Group() };
scene.add(VOLT.root);
{
  const R = VOLT.root;
  const bod = new THREE.Group(); R.add(bod); VOLT.bod = bod;
  const ink = new THREE.MeshPhysicalMaterial({ color: INKC, roughness: .32, clearcoat: .8, clearcoatRoughness: .15, envMap: ENV, envMapIntensity: .6 });
  const body = new THREE.Mesh(new RoundedBoxGeometry(.36, .34, .3, 4, .09), ink); body.castShadow = true; bod.add(body);
  const scrM = new THREE.MeshStandardMaterial({ color: LIME, emissive: LIME, emissiveIntensity: .25, roughness: .4 });
  const scr = new THREE.Mesh(new RoundedBoxGeometry(.28, .22, .02, 3, .05), scrM); scr.position.set(0, .01, .15); bod.add(scr);
  const eyeM = new THREE.MeshBasicMaterial({ color: 0x101111 }), shM = new THREE.MeshBasicMaterial({ color: 0xFFFFFF });
  VOLT.eyes = []; VOLT.arcs = [];
  for (const s of [-1, 1]) {
    const eg = new THREE.Group(); eg.position.set(s * .058, .035, .162); bod.add(eg);
    const e = new THREE.Mesh(new THREE.SphereGeometry(1, 24, 16), eyeM); e.scale.set(.027, .036, .006); eg.add(e);
    const c1 = new THREE.Mesh(new THREE.CircleGeometry(.009, 12), shM); c1.position.set(.008, .012, .007); eg.add(c1);
    const c2 = new THREE.Mesh(new THREE.CircleGeometry(.0045, 10), shM); c2.position.set(-.008, -.011, .007); eg.add(c2);
    const arc = new THREE.Mesh(new THREE.TorusGeometry(.022, .006, 8, 20, Math.PI), eyeM); arc.position.set(s * .058, .028, .164); arc.visible = false; bod.add(arc);
    VOLT.eyes.push(eg); VOLT.arcs.push(arc);
  }
  const ckM = new THREE.MeshBasicMaterial({ color: 0xFF7DB4, transparent: true, opacity: .75 });
  for (const s of [-1, 1]) { const c = new THREE.Mesh(new THREE.CircleGeometry(.018, 16), ckM); c.position.set(s * .1, -.022, .1615); c.scale.y = .6; bod.add(c); }
  // mouth: a smile line, and an open mouth that scales with his voice
  VOLT.smile = new THREE.Mesh(new THREE.TorusGeometry(.024, .005, 8, 20, Math.PI), eyeM); VOLT.smile.position.set(0, -.03, .163); VOLT.smile.rotation.z = Math.PI; bod.add(VOLT.smile);
  VOLT.mouth = new THREE.Group(); VOLT.mouth.position.set(0, -.04, .162); bod.add(VOLT.mouth);
  { const mo = new THREE.Mesh(new THREE.SphereGeometry(1, 20, 14), eyeM); mo.scale.set(.028, .018, .004); VOLT.mouth.add(mo); const tg = new THREE.Mesh(new THREE.SphereGeometry(1, 16, 10), new THREE.MeshBasicMaterial({ color: PINK })); tg.scale.set(.015, .007, .003); tg.position.set(0, -.008, .002); VOLT.mouth.add(tg); }
  // the bolt antenna: a short stem, the upper half white and the lower half lime
  const stem = new THREE.Mesh(new THREE.CylinderGeometry(.012, .014, .06, 10), ink); stem.position.y = .2; bod.add(stem);
  const bolt = new THREE.Group(); bolt.position.set(0, .29, 0); bod.add(bolt); VOLT.bolt = bolt;
  const shp = (pts) => { const s = new THREE.Shape(); s.moveTo(pts[0][0], pts[0][1]); for (const p of pts.slice(1)) s.lineTo(p[0], p[1]); const g = new THREE.ExtrudeGeometry(s, { depth: .026, bevelEnabled: true, bevelThickness: .006, bevelSize: .006, bevelSegments: 2 }); g.translate(0, 0, -.013); return g; };
  const up = new THREE.Mesh(shp([[.012, .11], [-.06, .004], [.012, .004], [.05, .11]]), new THREE.MeshPhysicalMaterial({ color: 0xFFFFFF, roughness: .25, clearcoat: .6 }));
  const lo = new THREE.Mesh(shp([[-.03, .014], [.064, .014], [-.02, -.1]]), new THREE.MeshPhysicalMaterial({ color: LIME, roughness: .25, clearcoat: .6, emissive: LIME, emissiveIntensity: .2 }));
  up.castShadow = lo.castShadow = true; bolt.add(up, lo);
  // floating hands
  VOLT.hands = []; for (const s of [-1, 1]) { const h = new THREE.Mesh(new THREE.SphereGeometry(.05, 18, 14), ink); h.castShadow = true; R.add(h); VOLT.hands.push(h); }
  // a soft contact shadow
  VOLT.shadow = new THREE.Mesh(new THREE.CircleGeometry(.16, 24), new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: .22, depthWrite: false })); VOLT.shadow.rotation.x = -Math.PI / 2; scene.add(VOLT.shadow);
}
// s: {x, y, z (hover centre), ry, rx, roll, sc, eyes: open|happy|wide|closed|wink, look: [x, y], talk, hands: [[x,y,z],[x,y,z]] (body
//   space, metres at sc 1), sq, floorY (for the shadow), still}
function placeVolt(vis, s) {
  VOLT.root.visible = !!vis; VOLT.shadow.visible = !!vis && s.floorY !== undefined;
  if (!vis) return;
  const t = NOW, sc = s.sc ?? 1, still = !!s.still;
  const bob = still ? 0 : Math.sin(t * 2.6) * .025, tilt = still ? 0 : Math.sin(t * 1.7) * .05;
  const ta = s.talk ? envAt(C.voltEnv, t) : 0;
  VOLT.root.position.set(s.x, s.y + bob * sc + ta * .012 * sc, s.z); VOLT.root.rotation.set((s.rx ?? 0) - ta * .06, s.ry ?? 0, (s.roll ?? 0) + tilt + ta * .05 * Math.sin(t * 7), "YXZ"); VOLT.root.scale.setScalar(sc);
  const sq = (s.sq ?? 0) - ta * .05; VOLT.bod.scale.set(1 + sq * .5, 1 - sq, 1 + sq * .5);
  const e = s.eyes || "open", blink = (e === "open" || e === "wide") && !s.noblink && blinkAt(4.4, t);
  for (let k = 0; k < 2; k++) {
    const arcs = e === "happy" || (e === "wink" && k === 0);
    VOLT.eyes[k].visible = !arcs; VOLT.arcs[k].visible = arcs;
    const lk = s.look || [0, 0]; VOLT.eyes[k].position.x = (k ? 1 : -1) * .058 + lk[0] * .012; VOLT.eyes[k].position.y = .035 + lk[1] * .01;
    VOLT.eyes[k].scale.set(e === "wide" ? 1.18 : 1, blink || e === "closed" ? .12 : (e === "wide" ? 1.2 : 1), 1);
  }
  const open = ta > .06 || s.mouth === "o";
  VOLT.smile.visible = !open; VOLT.mouth.visible = open;
  if (open) VOLT.mouth.scale.set(.9 + .3 * ta, s.mouth === "o" ? 1.4 : .5 + 1.3 * ta, 1);
  VOLT.bolt.rotation.z = Math.sin(t * 3.1) * .08 + ta * .15 * Math.sin(t * 11);
  const hs = s.hands || [[-.27, -.06, .05], [.27, -.06, .05]];
  VOLT.root.updateMatrixWorld(true);
  for (let k = 0; k < 2; k++) { const h = hs[k]; V.set(h[0], h[1] + (still ? 0 : Math.sin(t * 2.6 + k * 1.3) * .015) + (s.talk ? ta * .04 * (k ? 1 : .6) * Math.sin(t * 8 + k) : 0), h[2]); VOLT.root.localToWorld(V); VOLT.hands[k].position.copy(V); VOLT.hands[k].scale.setScalar(sc); }
  if (s.floorY !== undefined) { VOLT.shadow.position.set(s.x, s.floorY + .005, s.z); const hgt = Math.max(.05, s.y - s.floorY); VOLT.shadow.scale.setScalar(sc * (1.1 - Math.min(.6, hgt * .25))); VOLT.shadow.material.opacity = .25 - Math.min(.15, hgt * .05); }
}
// lip sync: loudness envelopes per speaker, 30 values per second (build/audio.py -> CT.julesEnv, CT.voltEnv)
const envAt = (arr, t) => { if (!arr) return 0; const i = t * 30, a = Math.floor(i), f = i - a; return lerp(arr[Math.min(arr.length - 1, Math.max(0, a))] || 0, arr[Math.min(arr.length - 1, Math.max(0, a + 1))] || 0, f); };
// ================================================================= JULES, the creator (house blocky style): a fitness creator, hair in a bun,
// lime tee, ink leggings, white trainers; her pixel mouth follows the loudness of her voice
const JULES = makeChar({ id: "jules", skin: "#E7B48E", hair: "#3B2216", style: "bun", top: "#CCFB79", topStyle: "tee", pants: "#1A1A1C", shoe: "#FFFFFF", brow: "#3B2216" }, scene);
JULES.seed = 2.3;
function placeJules(vis, p, f) {
  f = { ...(f || {}) };
  if (f.talk) { const a = envAt(C.julesEnv, NOW); f.talk = false; f.mouth = a < .08 ? (f.mouth || "smile") : (a < .4 ? "talk" : (f.big ? (a > .7 ? "wail" : "rant") : "o")); }
  placeChar(JULES, vis, p, f);
}
// her phone (in the right hand)
JULES.phone = new THREE.Group(); JULES.hand[1].add(JULES.phone); JULES.phone.position.set(0, -.02, .1);
rbox(.075, .15, .01, mat(0x2A2A30, { roughness: .3 }), 0, 0, 0, .008, { parent: JULES.phone, cast: false });
JULES.scrM = texMat("phone"); { const sp = new THREE.Mesh(new THREE.PlaneGeometry(.066, .138), JULES.scrM); sp.position.z = -.006; sp.rotation.y = Math.PI; JULES.phone.add(sp); }
