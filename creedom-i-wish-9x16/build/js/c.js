
// ================================================================= THE BEDROOM STUDIO (soft, rounded, like the reference stills)
// The desk faces the camera side (+z), the creator's chair behind it (z = -.7). Back wall z = -2.3 with the big window
// (left of centre) framed by fairy lights; the bed along the right; posters and a plant shelf on the right wall.
const SET = {};
const mkSet = (k) => { const g = new THREE.Group(); g.visible = false; scene.add(g); SET[k] = g; PARENT = g; return g; };
function v3(x, y, z) { return new THREE.Vector3(x, y, z); }
const RM = mkSet("room");
const SEAT = v3(-.1, 0, -.75), SITY = .52 - .71;
const DESKY = .8;
const rbox = (w, h, d, c, x, y, z, r = .03, o = {}) => box(w, h, d, c, x, y, z, { round: r, ...o });
const soft = (c, o = {}) => new THREE.MeshPhysicalMaterial({ color: c, roughness: .7, sheen: .6, sheenColor: new THREE.Color(0xffffff), sheenRoughness: .6, ...o });
{
  const plank = pix(256, 256, (g) => { px(g, "#7C5236", 0, 0, 256, 256); for (let j = 0; j < 8; j++) { const c = ["#80553A", "#764D33", "#86593C", "#7A5136"][j % 4]; px(g, c, 0, j * 32, 256, 32); px(g, "#5E3C27", 0, j * 32, 256, 2); px(g, "#5E3C27", (j * 97) % 256, j * 32, 2, 32); for (let k = 0; k < 6; k++) { g.fillStyle = "rgba(0,0,0,.05)"; g.fillRect((j * 37 + k * 41) % 256, j * 32 + 6 + k * 4, 60, 1); } } }, false);
  flat(9, 8, new THREE.MeshStandardMaterial({ map: rep(plank, 4, 4), roughness: .45, envMap: ENV, envMapIntensity: .15 }), 0, 0, 0);
  const wallM = mat(0xC9BBDD, { roughness: .95 }), trim = mat(0xEDE6F2, { roughness: .6 });
  // back wall with a window opening (centre x -1.05, y 1.8; 1.84 x 1.44)
  { const x0 = -1.05 - .92, x1 = -1.05 + .92, y0 = 1.8 - .72, y1 = 1.8 + .72;
    box(x0 + 4.5, 3.2, .2, wallM, (-4.5 + x0) / 2, 1.6, -2.4); box(4.5 - x1, 3.2, .2, wallM, (x1 + 4.5) / 2, 1.6, -2.4);
    box(x1 - x0, y0, .2, wallM, -1.05, y0 / 2, -2.4); box(x1 - x0, 3.2 - y1, .2, wallM, -1.05, (y1 + 3.2) / 2, -2.4); }
  box(.2, 3.2, 8, wallM, -3.4, 1.6, 1.5); box(.2, 3.2, 8, wallM, 3.5, 1.6, 1.5);
  box(9, .1, 8, mat(0xD6CCE6, { roughness: .95 }), 0, 3.2, 1.5, { cast: false });
  box(9, .1, .05, trim, 0, .05, -2.29); box(.05, .1, 8, trim, 3.39, .05, 1.5);
  // the window: two panes (they swing open for the entrance), frame, sill; the sky plane sits behind it
  RM.skyM = texMat("sky", { transparent: false }); RM.sky = plane(4.2, 3.2, RM.skyM, -1.0, 1.9, -3.2, 0);
  RM.clouds = []; for (let i = 0; i < 3; i++) { const m = texMat("cloud" + i); const p = plane(1.6, .5, m, -2 + i * 1.4, 2.4 - i * .25, -3.1 + i * .01, 0); p.material.opacity = .8; RM.clouds.push(p); }
  RM.win = new THREE.Group(); RM.win.position.set(-1.05, 1.8, -2.3); RM.add(RM.win);
  const wf = mat(0xF4F0F8, { roughness: .5 });
  for (const [w, h, x, y] of [[1.9, .07, 0, .72], [1.9, .07, 0, -.72], [.07, 1.5, -.92, 0], [.07, 1.5, .92, 0]]) box(w, h, .12, wf, x, y, 0, { parent: RM.win });
  box(2.1, .06, .26, wf, 0, -.78, .08, { parent: RM.win });
  RM.panes = [];
  for (const s of [-1, 1]) {
    const hinge = new THREE.Group(); hinge.position.set(s * .9, 0, .02); RM.win.add(hinge);
    const pane = new THREE.Group(); hinge.add(pane);
    for (const [w, h, x, y] of [[.9, .05, -s * .45, .69], [.9, .05, -s * .45, -.69], [.05, 1.4, 0, 0], [.05, 1.4, -s * .88, 0]]) box(w, h, .05, wf, x, y, 0, { parent: pane });
    const gl = new THREE.Mesh(new THREE.PlaneGeometry(.86, 1.36), new THREE.MeshPhysicalMaterial({ color: 0x8090B0, roughness: .05, transparent: true, opacity: .05, envMap: ENV, envMapIntensity: .08, depthWrite: false })); gl.position.x = -s * .45; pane.add(gl);
    RM.panes.push(hinge);
  }
  // sheer curtains (they blow in on the teasers)
  RM.curt = [];
  for (const s of [-1, 1]) { const g = new THREE.Group(); g.position.set(-1.05 + s * 1.12, 2.55, -2.2); RM.add(g); const cm2 = new THREE.MeshStandardMaterial({ color: 0xF6F0FA, roughness: .9, transparent: true, opacity: .55, side: THREE.DoubleSide }); const c = new THREE.Mesh(new THREE.PlaneGeometry(.45, 1.7, 1, 8), cm2); c.position.y = -.85; g.add(c); RM.curt.push(g); }
  // fairy lights around the window
  RM.fairy = [];
  const bulbM = [new THREE.MeshBasicMaterial({ color: 0xFFE2A8, toneMapped: false }), new THREE.MeshBasicMaterial({ color: 0xFFD08A, toneMapped: false })];
  const path = []; for (let i = 0; i <= 24; i++) { const u = i / 24; path.push(v3(-2.05 + 2.0 * u, 2.62 - .07 * Math.sin(u * Math.PI * 3) ** 2, -2.27)); }
  for (let i = 0; i <= 10; i++) { path.push(v3(-2.08, 2.55 - i * .15, -2.27)); path.push(v3(-.02 + .02, 2.55 - i * .15, -2.27)); }
  const wire = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(path.slice(0, 25)), 80, .004, 4), mat(0x3A3A3A)); RM.add(wire);
  path.forEach((p, i) => { const b = new THREE.Mesh(new THREE.SphereGeometry(.028, 12, 10), bulbM[i % 2]); b.position.copy(p).add(v3(0, -.03, .01)); RM.add(b); RM.fairy.push(b); });
  // posters, the plant shelf (right wall)
  RM.posterM = texMat("posters", { transparent: false }); const pp = plane(1.3, .95, RM.posterM, 3.38, 1.9, -1.2, -Math.PI / 2);
  rbox(.24, .04, .9, mat(0xC9A27A), 3.27, 1.55, -.1, .01);
  for (let k = 0; k < 3; k++) { cyl(.07, .055, .1, soft(0xF4F0EC), 3.27, 1.62, -.4 + k * .3, 16); for (let j = 0; j < 5; j++) { const l = new THREE.Mesh(new THREE.SphereGeometry(.05, 10, 8), mat(0x5E9C52)); l.position.set(3.27 + (hash(k * 7 + j) - .5) * .1, 1.7 + j * .03, -.4 + k * .3 + (hash(j * 3 + k) - .5) * .1); l.scale.set(1, 1.4, 1); add(l); } }
  // the desk: rounded top and legs, a drawer unit on the left
  rbox(1.9, .07, .9, mat(0x8A6044, { roughness: .45, envMap: ENV, envMapIntensity: .2 }), 0, DESKY - .035, 0, .02);
  for (const [x, z] of [[.88, .38], [.88, -.38], [-.2, .38], [-.2, -.38]]) rbox(.06, DESKY - .07, .06, mat(0x7A5238), x, (DESKY - .07) / 2, z, .015);
  rbox(.62, DESKY - .1, .8, mat(0x7A5238), -.6, (DESKY - .1) / 2 + .02, 0, .02);
  // laptop (plain lid), the pink lamp, the mug, the gorilla tripod with the phone
  const lap = new THREE.Group(); lap.position.set(-.25, DESKY, -.05); RM.add(lap);
  rbox(.44, .018, .3, metal(0x5A5A62, .35), 0, .009, 0, .006, { parent: lap });
  const lid = new THREE.Group(); lid.position.set(0, .015, -.15); lid.rotation.x = -.35; lap.add(lid); rbox(.44, .29, .014, metal(0x5A5A62, .35), 0, .145, 0, .006, { parent: lid });
  RM.lapScr = new THREE.MeshBasicMaterial({ color: 0x9FB2D8, toneMapped: false }); const ls = new THREE.Mesh(new THREE.PlaneGeometry(.4, .25), RM.lapScr); ls.position.set(0, .145, .008); lid.add(ls);
  RM.lampShade = new THREE.MeshPhysicalMaterial({ color: 0xF0B8C6, roughness: .45, clearcoat: .3 });
  { const L = new THREE.Group(); L.position.set(-.72, DESKY, -.15); RM.add(L); cyl(.09, .1, .025, soft(0xF0B8C6), 0, .012, 0, 24, { parent: L });
    const a1 = new THREE.Group(); a1.position.y = .03; a1.rotation.z = -.35; L.add(a1); cyl(.011, .011, .3, soft(0xF0B8C6), 0, .15, 0, 10, { parent: a1 });
    const a2 = new THREE.Group(); a2.position.y = .3; a2.rotation.z = 1.25; a1.add(a2); cyl(.011, .011, .26, soft(0xF0B8C6), 0, .13, 0, 10, { parent: a2 });
    const hd = new THREE.Group(); hd.position.y = .26; hd.rotation.z = -1.9; a2.add(hd); const sh = new THREE.Mesh(new THREE.CylinderGeometry(.04, .1, .13, 24, 1, true), RM.lampShade); sh.material.side = THREE.DoubleSide; hd.add(sh);
    RM.bulb = new THREE.Mesh(new THREE.SphereGeometry(.03, 12, 10), new THREE.MeshBasicMaterial({ color: 0xFFE6C8, toneMapped: false })); RM.bulb.position.y = -.04; hd.add(RM.bulb); RM.lampHead = hd; }
  { const m = new THREE.Group(); m.position.set(.62, DESKY, .2); RM.add(m); const mm = new THREE.MeshPhysicalMaterial({ color: 0xF6F2EC, roughness: .3, clearcoat: .6 }); cyl(.045, .042, .1, mm, 0, .05, 0, 24, { parent: m }); const hdl = new THREE.Mesh(new THREE.TorusGeometry(.027, .008, 8, 20), mm); hdl.position.set(.05, .055, 0); m.add(hdl); cyl(.04, .04, .005, mat(0x5A3A24), 0, .095, 0, 20, { parent: m }); }
  RM.tri = new THREE.Group(); RM.tri.position.set(.25, DESKY, .05); RM.add(RM.tri);
  for (let k = 0; k < 3; k++) { const a = k * 2.09 + .3; for (let j = 0; j < 6; j++) { const b = new THREE.Mesh(new THREE.SphereGeometry(.012, 8, 6), mat(0x1E1E22, { roughness: .4 })); b.position.set(Math.sin(a) * (.07 - j * .011), .01 + j * .022, Math.cos(a) * (.07 - j * .011)); RM.tri.add(b); } }
  RM.triPhone = new THREE.Group(); RM.triPhone.position.y = .2; RM.tri.add(RM.triPhone); rbox(.075, .15, .01, mat(0x2A2A30, { roughness: .3 }), 0, 0, 0, .008, { parent: RM.triPhone });
  RM.triScr = new THREE.MeshBasicMaterial({ color: 0xFFE3F1, toneMapped: false }); { const s = new THREE.Mesh(new THREE.PlaneGeometry(.066, .138), RM.triScr); s.position.z = -.006; s.rotation.y = Math.PI; RM.triPhone.add(s); }
  // the chair: white shell on a star base with wheels
  { const C2 = new THREE.Group(); C2.position.set(SEAT.x, 0, SEAT.z); RM.add(C2); const cw = soft(0xF4F2F6); rbox(.52, .07, .5, cw, 0, .5, -.02, .03, { parent: C2 }); rbox(.5, .5, .06, cw, 0, .8, -.27, .05, { parent: C2 }); cyl(.025, .025, .38, metal(0xC8C8D0, .3), 0, .3, 0, 10, { parent: C2 });
    for (let k = 0; k < 5; k++) { const a = k * 1.2566; const leg = rbox(.24, .025, .04, cw, Math.sin(a) * .12, .07, Math.cos(a) * .12, .012, { parent: C2 }); leg.rotation.y = a + Math.PI / 2; const w = new THREE.Mesh(new THREE.SphereGeometry(.03, 10, 8), mat(0x2A2A30)); w.position.set(Math.sin(a) * .24, .03, Math.cos(a) * .24); C2.add(w); } RM.chair = C2; }
  // the ring light, front left
  RM.ring = new THREE.Group(); RM.ring.position.set(-1.3, 0, .6); RM.ring.rotation.y = -.55; RM.add(RM.ring);
  cyl(.014, .014, 1.45, mat(0x1E1E22, { roughness: .4 }), 0, .72, 0, 10, { parent: RM.ring });
  for (let k = 0; k < 3; k++) { const l = cyl(.011, .011, .5, mat(0x1E1E22), Math.sin(k * 2.1) * .16, .18, Math.cos(k * 2.1) * .16, 8, { parent: RM.ring }); l.rotation.set(Math.cos(k * 2.1) * .75, 0, -Math.sin(k * 2.1) * .75); }
  const rh = new THREE.Mesh(new THREE.TorusGeometry(.25, .035, 12, 64), mat(0x1E1E22, { roughness: .4 })); rh.position.y = 1.58; RM.ring.add(rh);
  RM.ringM = new THREE.MeshBasicMaterial({ color: 0xFFF4EA, toneMapped: false }); const rg = new THREE.Mesh(new THREE.TorusGeometry(.25, .018, 10, 64), RM.ringM); rg.position.set(0, 1.58, .02); RM.ring.add(rg);
  // the bed along the right: frame, mattress, pink knitted blanket, pillows
  rbox(1.35, .3, 2.2, mat(0xD9C6A8), 2.75, .15, -1.15, .04); rbox(1.3, .2, 2.12, soft(0xF6F2F4), 2.75, .4, -1.15, .08);
  rbox(1.35, .7, .1, mat(0xD9C6A8), 2.75, .5, -2.28, .04);
  RM.knitM = texMat("knit", { transparent: false }); RM.knitM.toneMapped = true;
  { const kn = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .95 }); LATE.push([kn, "knit"]); rbox(1.38, .1, 1.3, kn, 2.75, .52, -.62, .05); rbox(.08, .45, 1.3, kn, 2.08, .32, -.62, .04); }
  rbox(.6, .16, .36, soft(0xF0B8C6), 2.55, .58, -1.95, .07); rbox(.55, .15, .34, soft(0xD8D2E4), 3.05, .58, -1.97, .07);
  // a rug, crumpled paper balls, a cable on the floor, a bin
  { const rug = new THREE.Mesh(new THREE.CircleGeometry(1.1, 48), soft(0xDCD4E4, { roughness: .95 })); rug.rotation.x = -Math.PI / 2; rug.scale.set(1.3, .8, 1); rug.position.set(1.4, .006, .2); add(rug, false, true); }
  for (let k = 0; k < 7; k++) { const b = new THREE.Mesh(new THREE.IcosahedronGeometry(.05, 1), soft(0xF8F6F2)); b.geometry.attributes.position.array.forEach((_, i, a) => { a[i] *= .8 + .4 * hash(i * 1.7 + k); }); b.geometry.computeVertexNormals(); b.position.set(.6 + hash(k) * 1.6, .045, -.1 + hash(k * 3) * 1.0); b.rotation.set(k, k * 2, k * 3); add(b); }
  { const pts = [v3(-1.3, .01, .6), v3(-.9, .01, .9), v3(-.2, .01, .75), v3(.5, .01, .95), v3(1.0, .01, .6)]; add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 60, .008, 6), mat(0xEDEDF0))); }
  // lights: warm lamp key, cool moon fill from the window, a soft violet fill, the ring light, rims for the characters
  RM.lamp = new THREE.PointLight(0xFFD2B0, 0, 4, 1.6); RM.lamp.position.set(-.55, 1.15, -.05); scene.add(RM.lamp);
  RM.moon = new THREE.PointLight(0x9DB8FF, 0, 7, 1.3); RM.moon.position.set(-1.05, 1.9, -1.9); scene.add(RM.moon);
  RM.fill = new THREE.PointLight(0xC8B0FF, 0, 10, 1.2); RM.fill.position.set(1.0, 2.6, 2.8); scene.add(RM.fill);
  RM.key = new THREE.PointLight(0xFFF0E6, 0, 5, 1.6); RM.key.position.set(-1.2, 1.55, .5); scene.add(RM.key);
  RM.rim = new THREE.PointLight(0xFF8CC6, 0, 3, 1.6); scene.add(RM.rim);
  RM.rim2 = new THREE.PointLight(0xFFE8D0, 0, 3, 1.6); scene.add(RM.rim2);
}
// ---------------------------------------------------------------- the reel-world props: film strip, reel cards, the DM machine, paper planes, papers, speed lines
const FX = {};
{
  FX.strip = new THREE.Group(); RM.add(FX.strip); FX.frames = [];
  for (let i = 0; i < 7; i++) {
    const f = new THREE.Group(); f.position.set(-.45 + i * .15, DESKY + .42, -.1 - .06 * Math.sin(i / 6 * Math.PI)); f.rotation.y = (3 - i) * .06; FX.strip.add(f);
    const fm = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .95 }); LATE.push([fm, "thumb" + (i % 4)]);
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.12, .2), fm); f.add(p);
    const edge = new THREE.Mesh(new THREE.PlaneGeometry(.135, .215), new THREE.MeshBasicMaterial({ color: 0xFFFFFF, transparent: true, opacity: .7 })); edge.position.z = -.002; f.add(edge);
    f.edge = edge; FX.frames.push(f);
  }
  FX.cards = new THREE.Group(); RM.add(FX.cards); FX.cardL = [];
  for (let i = 0; i < 5; i++) {
    const c = new THREE.Group(); FX.cards.add(c);
    const cmat = new THREE.MeshPhysicalMaterial({ color: i === 3 ? 0xFFE4A0 : 0xFFF2F8, roughness: .3, transparent: true, opacity: .9, emissive: i === 3 ? 0x8A5A00 : 0x000000, emissiveIntensity: 0, side: THREE.DoubleSide });
    c.add(new THREE.Mesh(new RoundedBoxGeometry(.17, .27, .008, 2, .015), cmat));
    const im = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .95 }); LATE.push([im, "thumb" + ((i + 1) % 4)]);
    const ip = new THREE.Mesh(new THREE.PlaneGeometry(.14, .19), im); ip.position.set(0, .02, .006); c.add(ip);
    c.cmat = cmat; FX.cardL.push(c);
  }
  FX.mach = new THREE.Group(); FX.mach.position.set(.42, DESKY, .2); RM.add(FX.mach);
  rbox(.22, .14, .16, new THREE.MeshPhysicalMaterial({ color: 0xF06BB4, roughness: .35, clearcoat: .6 }), 0, .07, 0, .035, { parent: FX.mach });
  rbox(.12, .016, .02, mat(0x5A1A3E), 0, .1, .081, .006, { parent: FX.mach });
  const piv = new THREE.Group(); piv.position.set(.115, .09, 0); FX.mach.add(piv); FX.lever = piv;
  cyl(.007, .007, .14, metal(0xD9D9DE, .3), 0, .07, 0, 8, { parent: piv }); const kn = new THREE.Mesh(new THREE.SphereGeometry(.022, 16, 12), new THREE.MeshPhysicalMaterial({ color: 0xFFC21A, roughness: .3, clearcoat: .7 })); kn.position.y = .15; piv.add(kn);
  FX.machLight = new THREE.Mesh(new THREE.SphereGeometry(.013, 10, 8), new THREE.MeshBasicMaterial({ color: 0x3A3A3A })); FX.machLight.position.set(-.07, .145, .05); FX.mach.add(FX.machLight);
  FX.planes = [];
  const pg = new THREE.BufferGeometry(); pg.setAttribute("position", new THREE.Float32BufferAttribute([0, 0, .06, -.04, 0, -.035, 0, .005, -.025, 0, 0, .06, .04, 0, -.035, 0, .005, -.025, 0, 0, .06, 0, -.018, -.03, 0, .005, -.025], 3)); pg.computeVertexNormals();
  for (let i = 0; i < 14; i++) { const p = new THREE.Mesh(pg, new THREE.MeshStandardMaterial({ color: 0xFFFFFF, roughness: .8, side: THREE.DoubleSide })); RM.add(p); FX.planes.push(p); }
  // loose papers that blow about on the teasers and the entrance
  FX.papers = [];
  for (let i = 0; i < 8; i++) { const p = new THREE.Mesh(new THREE.PlaneGeometry(.16, .21), new THREE.MeshStandardMaterial({ color: 0xFBFAF6, roughness: .9, side: THREE.DoubleSide })); RM.add(p); FX.papers.push(p); }
  // speed lines behind Cree when he flies (thin, soft white, no glow)
  const slT = pix(16, 256, (g) => { const gr = g.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, "rgba(255,255,255,0)"); gr.addColorStop(.5, "rgba(255,255,255,.85)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(6, 0, 4, 256); }, false);
  FX.speed = new THREE.Group(); scene.add(FX.speed);
  for (let i = 0; i < 10; i++) { const s = new THREE.Mesh(new THREE.PlaneGeometry(.05, 1), new THREE.MeshBasicMaterial({ map: slT, transparent: true, depthWrite: false, opacity: .7 })); s.position.set((hash(i) - .5) * .6, (hash(i * 3) - .5) * .5, -.4 - hash(i * 5) * .6); s.rotation.x = Math.PI / 2; s.scale.y = .5 + hash(i * 7); FX.speed.add(s); }
  // a soft pink trail ribbon for the far-off flyby (thin, matte)
  FX.trail = new THREE.Mesh(new THREE.PlaneGeometry(1, .04), new THREE.MeshBasicMaterial({ color: 0xFF9BCF, transparent: true, opacity: .7, depthWrite: false })); scene.add(FX.trail);
  // a soft shadow sweep (the flying shadow passing over the room)
  FX.shadow = new THREE.Mesh(new THREE.CircleGeometry(.6, 32), new THREE.MeshBasicMaterial({ color: 0x0A0614, transparent: true, opacity: .35, depthWrite: false })); FX.shadow.rotation.x = -Math.PI / 2; scene.add(FX.shadow);
}
PARENT = scene;

// ---------------------------------------------------------------- Cree, to his model sheet: as wide as tall (arms included), eyes 31% down,
// each eye 23% of his width, centres 36% apart, beak just below the eye line, arms at two thirds of his height, stubby oval feet.
// Built 1 unit tall; CREE.root is scaled to his size in the room.
const CREE = { root: new THREE.Group() };
scene.add(CREE.root);
{
  const R = CREE.root;
  const plush = CREE.plush = new THREE.MeshPhysicalMaterial({ color: 0xF343A2, roughness: .68, sheen: 1, sheenColor: new THREE.Color(0xFF8CC6), sheenRoughness: .45, envMap: ENV, envMapIntensity: .25 });
  const bod = new THREE.Group(); R.add(bod); CREE.bod = bod;
  const g = new THREE.SphereGeometry(.5, 80, 60); const pa = g.attributes.position;
  for (let i = 0; i < pa.count; i++) { const y = pa.getY(i) / .5; const w = .84 * (1 + .1 * (-y) - .05 * Math.max(0, y) ** 2); pa.setX(i, pa.getX(i) * w); pa.setZ(i, pa.getZ(i) * w * .95); pa.setY(i, pa.getY(i) * .94); }
  g.computeVertexNormals();
  const body = new THREE.Mesh(g, plush); body.position.y = .53; body.castShadow = true; body.receiveShadow = true; bod.add(body);
  // eyes: white with a pale pink rim, big black pupils, a large catchlight upper right and a small one lower left
  const sclM = CREE.sclM = new THREE.MeshPhysicalMaterial({ color: 0xFFFFFF, roughness: .12, clearcoat: 1, clearcoatRoughness: .04, envMap: ENV, envMapIntensity: .45 });
  const pupM = CREE.pupM = new THREE.MeshPhysicalMaterial({ color: 0x0B0B0B, roughness: .06, clearcoat: 1, clearcoatRoughness: .03, envMap: ENV, envMapIntensity: .8 });
  const catM = new THREE.MeshBasicMaterial({ color: 0xFFFFFF });
  const rimM = CREE.rimM = new THREE.MeshStandardMaterial({ color: 0xFFD3E6, roughness: .6 });
  CREE.eyes = []; CREE.pupils = []; CREE.cats = [];
  for (const s of [-1, 1]) {
    const eg = new THREE.Group(); eg.position.set(s * .18, .70, .355); eg.rotation.y = s * .36; eg.rotation.x = -.06; bod.add(eg);
    const rim = new THREE.Mesh(new THREE.SphereGeometry(.12, 36, 28), rimM); rim.scale.set(1, 1.04, .42); eg.add(rim);
    const scl = new THREE.Mesh(new THREE.SphereGeometry(.112, 36, 28), sclM); scl.scale.set(1, 1.04, .5); scl.position.z = .012; eg.add(scl);
    const pg = new THREE.Group(); pg.position.z = .05; eg.add(pg);
    const pup = new THREE.Mesh(new THREE.SphereGeometry(.078, 32, 24), pupM); pup.scale.set(1, 1.04, .45); pg.add(pup);
    const c1 = new THREE.Mesh(new THREE.SphereGeometry(.024, 14, 10), catM); c1.position.set(.026, .032, .036); c1.scale.z = .4; pg.add(c1);
    const c2 = new THREE.Mesh(new THREE.SphereGeometry(.011, 10, 8), catM); c2.position.set(-.028, -.03, .036); c2.scale.z = .4; pg.add(c2);
    const arc = new THREE.Mesh(new THREE.TorusGeometry(.085, .022, 10, 28, Math.PI), new THREE.MeshStandardMaterial({ color: 0x14080F, roughness: .5 })); arc.position.set(s * .18, .7, .385); arc.rotation.y = s * .36; arc.visible = false; bod.add(arc); eg.arc = arc;
    CREE.eyes.push(eg); CREE.pupils.push(pg); CREE.cats.push([c1, c2]);
  }
  CREE.brows = [];
  for (const s of [-1, 1]) { const b = new THREE.Mesh(new THREE.CapsuleGeometry(.007, .06, 4, 10), new THREE.MeshStandardMaterial({ color: 0xD0207E, roughness: .6 })); b.rotation.z = Math.PI / 2; const bg = new THREE.Group(); bg.position.set(s * .18, .845, .335); bg.rotation.y = s * .36; bg.add(b); bod.add(bg); CREE.brows.push(bg); }
  // beak: upper and lower halves, yellow-orange, red inside (#D81F3C); the lower half hinges open
  const beakM = new THREE.MeshPhysicalMaterial({ color: 0xFFC21A, roughness: .3, clearcoat: .5, clearcoatRoughness: .25, envMap: ENV, envMapIntensity: .3 });
  const beakM2 = CREE.beakM2 = new THREE.MeshPhysicalMaterial({ color: 0xF2A516, roughness: .35, clearcoat: .4, envMap: ENV, envMapIntensity: .25 });
  const up = new THREE.Mesh(new THREE.SphereGeometry(.058, 28, 18, 0, Math.PI * 2, 0, Math.PI / 2), beakM); up.scale.set(1.05, .8, 1.25); up.position.set(0, .612, .42); up.rotation.x = .38; bod.add(up);
  const mouth = new THREE.Mesh(new THREE.SphereGeometry(.042, 18, 12), new THREE.MeshStandardMaterial({ color: 0xD81F3C, roughness: .7 })); mouth.scale.set(1.05, .65, .6); mouth.position.set(0, .598, .405); bod.add(mouth);
  const lowG = new THREE.Group(); lowG.position.set(0, .605, .405); bod.add(lowG);
  const low = new THREE.Mesh(new THREE.SphereGeometry(.047, 24, 14, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), beakM2); low.scale.set(1.0, .8, 1.15); low.position.set(0, 0, .016); lowG.add(low);
  CREE.jaw = lowG;
  // wings: short rounded arms, the widest point of him (arms included) about a third of the way up
  CREE.wings = [];
  for (const s of [-1, 1]) {
    const pv = new THREE.Group(); pv.position.set(s * .4, .45, .02); bod.add(pv);
    const w = new THREE.Mesh(new THREE.SphereGeometry(.12, 24, 18), plush); w.scale.set(.62, 1.2, .8); w.position.set(s * .04, -.1, 0); w.castShadow = true; pv.add(w);
    const tip = new THREE.Group(); tip.position.set(s * .05, -.22, .02); pv.add(tip); pv.tip = tip;
    CREE.wings.push(pv);
  }
  CREE.feet = [];
  for (const s of [-1, 1]) { const f = new THREE.Mesh(new THREE.SphereGeometry(.1, 22, 14), beakM2); f.scale.set(1.0, .48, 1.45); const fg = new THREE.Group(); fg.position.set(s * .14, .045, .1); fg.add(f); f.castShadow = true; R.add(fg); CREE.feet.push(fg); }
  const mg = new THREE.Group(); CREE.mag = mg;
  mg.add(new THREE.Mesh(new THREE.TorusGeometry(.11, .012, 10, 40), goldM));
  mg.add(new THREE.Mesh(new THREE.CircleGeometry(.105, 36), new THREE.MeshPhysicalMaterial({ color: 0xEAF6FF, roughness: 0, transparent: true, opacity: .2, envMap: ENV, envMapIntensity: 1.2, side: THREE.DoubleSide })));
  const hd = new THREE.Mesh(new THREE.CylinderGeometry(.016, .02, .17, 12), mat(0x8A5A34, { roughness: .5 })); hd.position.y = -.2; mg.add(hd);
  const fer = new THREE.Mesh(new THREE.CylinderGeometry(.019, .019, .025, 12), goldM); fer.position.y = -.115; mg.add(fer);
  scene.add(mg);
}
// state -> pose. s: {x, y, z, ry, rx (pitch: forward flight ~ -1.2), roll, sc, sq, wl/wr: [rz, rx], eyes, look, jaw, brow, browY, mag, magAt, step, feetBack}
function placeCree(vis, s) {
  CREE.root.visible = !!vis; CREE.mag.visible = !!(vis && s.mag);
  if (!vis) return;
  const R = CREE.root, sc = s.sc ?? .34, sq = s.sq ?? 0;
  const dk = !!CREE.dark;
  CREE.plush.envMapIntensity = dk ? 0 : .25; CREE.sclM.color.set(dk ? 0x2A1A26 : 0xFFFFFF); CREE.rimM.color.set(dk ? 0x2A1424 : 0xFFD3E6);
  R.position.set(s.x, s.y, s.z); R.rotation.set(s.rx ?? 0, s.ry ?? 0, s.roll ?? 0, "YXZ"); R.scale.setScalar(sc);
  CREE.bod.scale.set(1 + sq * .5, 1 - sq, 1 + sq * .5);
  for (let k = 0; k < 2; k++) {
    const w = k ? s.wr : s.wl, sgn = k ? 1 : -1;
    CREE.wings[k].rotation.set(w ? w[1] : 0, 0, sgn * (w ? w[0] : .12));
    const e = s.eyes || "open", eg = CREE.eyes[k];
    let ey = 1; if (e === "closed") ey = .08; else if (e === "squint") ey = .55; else if (e === "wide") ey = 1.1;
    if (e === "open" && !s.noblink && blinkAt(3.3, NOW)) ey = .08;
    eg.scale.set(e === "wide" ? 1.08 : 1, ey, 1);
    const pg = CREE.pupils[k]; const lk = s.look || [0, 0];
    pg.position.set(lk[0] * .03, lk[1] * .03, .05); pg.scale.setScalar(e === "wide" ? .85 : 1);
    for (const c of CREE.cats[k]) c.visible = !(s.oneEye && k === 0);
    const h = e === "happy"; eg.visible = !h; eg.arc.visible = h;
    const b = CREE.brows[k]; b.rotation.z = sgn * (s.brow ?? 0); b.position.y = .86 + (s.browY ?? 0) + (e === "wide" ? .03 : 0);
  }
  CREE.jaw.rotation.x = (s.jaw ?? .35) * .9;
  for (let k = 0; k < 2; k++) { const f = CREE.feet[k]; f.position.y = .045 + (s.step && (k ? s.step > 0 : s.step < 0) ? Math.abs(s.step) * .07 : 0); f.position.z = .1 - (s.feetBack ?? 0) * .12; f.rotation.x = (s.feetBack ?? 0) * 1.0; }
  R.updateMatrixWorld(true);
  if (s.mag === "hand") { CREE.wings[1].tip.getWorldPosition(V); CREE.mag.position.copy(V).add(V2.set(0, .04 * sc / .34, .02)); CREE.mag.rotation.set(s.magRx ?? 0, s.ry ?? 0, s.magRz ?? .25); CREE.mag.scale.setScalar(sc / .34 * .55); }
  if (s.mag === "desk") { CREE.mag.position.copy(s.magAt); CREE.mag.rotation.set(-Math.PI / 2 + .1, 0, .6); CREE.mag.scale.setScalar(.55); }
}
// Cree "talks" (gibberish): the beak follows the loudness of his chirps (CT.creeEnv, 30 values per second)
const envAt = (arr, t) => { if (!arr) return 0; const i = t * 30, a = Math.floor(i), f = i - a; return lerp(arr[Math.min(arr.length - 1, Math.max(0, a))] || 0, arr[Math.min(arr.length - 1, Math.max(0, a + 1))] || 0, f); };
const creeJaw = (t) => .18 + .85 * envAt(C.creeEnv, t);

// ================================================================= THE CREATOR: a soft designer-toy figure with a face rig
// Same skeleton and pivots as the house characters (pose() / applyPose() drive him), but smooth: capsule limbs, a big round
// head, sphere eyes with lids, brows, a mouth that opens with the loudness of his voice, tears.
function makeToy(parent = scene) {
  const skinM = new THREE.MeshPhysicalMaterial({ color: 0xF2C7A6, roughness: .55, sheen: .4, sheenColor: new THREE.Color(0xFFD8C8), sheenRoughness: .5, envMap: ENV, envMapIntensity: .15 });
  const hoodM = new THREE.MeshPhysicalMaterial({ color: 0xEFE7D8, roughness: .85, sheen: 1, sheenColor: new THREE.Color(0xFFFFFF), sheenRoughness: .7 });
  const pantM = new THREE.MeshPhysicalMaterial({ color: 0x8C8A8E, roughness: .85, sheen: .8, sheenColor: new THREE.Color(0xD8D8DC), sheenRoughness: .7 });
  const shoeM = new THREE.MeshPhysicalMaterial({ color: 0xF6F6F4, roughness: .45, clearcoat: .2 });
  const hairM = new THREE.MeshPhysicalMaterial({ color: 0x1E1A1C, roughness: .5, sheen: .5, sheenColor: new THREE.Color(0x5A5060), sheenRoughness: .4 });
  const root = new THREE.Group(); parent.add(root);
  const hips = new THREE.Group(); hips.position.y = HIP; root.add(hips);
  const mk = (geo, m, par, x, y, z, sx = 1, sy = 1, sz = 1) => { const o = new THREE.Mesh(geo, m); o.position.set(x, y, z); o.scale.set(sx, sy, sz); o.castShadow = true; o.receiveShadow = true; par.add(o); return o; };
  const SPH = new THREE.SphereGeometry(1, 40, 30);
  const torso = new THREE.Group(); hips.add(torso);
  // hoodie: a soft rounded body, a hem band, the hood around the neck, two drawstrings
  mk(new THREE.CapsuleGeometry(.27, .2, 10, 24), hoodM, torso, 0, .33, 0, 1.08, 1, .7);
  const hood = mk(new THREE.TorusGeometry(.17, .05, 14, 32), hoodM, torso, 0, .6, -.07); hood.rotation.x = Math.PI / 2 - .35; hood.scale.set(1.15, 1, 1);
  for (const s of [-1, 1]) { const d = mk(new THREE.CylinderGeometry(.008, .008, .16, 6), mat(0xF6F2EA), torso, s * .05, .52, .2); }
  mk(new RoundedBoxGeometry(.54, .16, .3, 3, .07), pantM, hips, 0, -.04, 0);
  mk(new THREE.CylinderGeometry(.07, .075, .1, 16), skinM, torso, 0, .64, 0);
  const neck = new THREE.Group(); neck.position.y = .66; torso.add(neck);
  const head = new THREE.Group(); head.rotation.order = "YXZ"; neck.add(head);
  const HR = .255, HC = .28;          // head radius, centre height above the neck pivot
  { const hg = new THREE.SphereGeometry(1, 48, 36); const ha = hg.attributes.position; for (let i = 0; i < ha.count; i++) { const y = ha.getY(i); if (y < 0) { const k = 1 - .1 * (-y) ** 1.5; ha.setX(i, ha.getX(i) * k); ha.setZ(i, ha.getZ(i) * (1 - .04 * (-y))); } } hg.computeVertexNormals(); mk(hg, skinM, head, 0, HC, 0, HR, HR * 1.06, HR * .98); }
  const surfZ = (x, y) => HR * .98 * Math.sqrt(Math.max(0, 1 - (x / HR) ** 2 - ((y - HC) / (HR * 1.06)) ** 2));
  for (const s of [-1, 1]) mk(SPH, skinM, head, s * HR * .98, HC - .02, -.01, .045, .07, .055);
  mk(SPH, skinM, head, 0, HC - .06, surfZ(0, HC - .06) - .005, .034, .03, .03);
  // eyes: sclera, brown iris, pupil, a catchlight; skin lids that close over them; brows above
  const sclM = new THREE.MeshPhysicalMaterial({ color: 0xFFFFFF, roughness: .2, clearcoat: .8, envMap: ENV, envMapIntensity: .3 });
  const irisM = new THREE.MeshPhysicalMaterial({ color: 0x6A3A1E, roughness: .2, clearcoat: 1, envMap: ENV, envMapIntensity: .5 });
  const pupM = new THREE.MeshBasicMaterial({ color: 0x0A0606 }), catM = new THREE.MeshBasicMaterial({ color: 0xFFFFFF });
  const eyes = [], irises = [], lidsU = [], lidsL = [], brows = [], tears = [], lashes = [];
  for (const s of [-1, 1]) {
    const ex = s * .095, ey = HC + .02, ez = surfZ(ex, ey) - .03;
    const eg = new THREE.Group(); eg.position.set(ex, ey, ez); eg.rotation.y = s * .22; head.add(eg);
    mk(SPH, sclM, eg, 0, 0, 0, .062, .07, .045);
    const ig = new THREE.Group(); ig.position.z = .03; eg.add(ig);
    mk(SPH, irisM, ig, 0, 0, 0, .042, .046, .018); mk(SPH, pupM, ig, 0, 0, .008, .022, .024, .012); mk(SPH, catM, ig, .014, .016, .018, .01, .01, .005);
    const lu = new THREE.Group(); eg.add(lu); const lum = mk(new THREE.SphereGeometry(1, 28, 16, 0, Math.PI * 2, 0, Math.PI / 2), skinM, lu, 0, 0, 0, .064, .072, .062); lu.rotation.x = -1.35;
    const ll = new THREE.Group(); eg.add(ll); mk(new THREE.SphereGeometry(1, 28, 16, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), skinM, ll, 0, 0, 0, .063, .071, .06); ll.rotation.x = 1.45;
    const bg = new THREE.Group(); bg.position.set(s * .1, HC + .12, surfZ(s * .1, HC + .12) + .004); bg.rotation.y = s * .22; head.add(bg);
    const br = mk(new THREE.CapsuleGeometry(.017, .075, 4, 10), hairM, bg, 0, 0, 0); br.rotation.z = Math.PI / 2; br.scale.set(1, 1, .6);
    const tg = new THREE.Group(); tg.position.set(ex + s * .01, ey - .07, surfZ(ex, ey - .07) + .004); head.add(tg);
    const tmM = new THREE.MeshPhysicalMaterial({ color: 0x6CC0F5, roughness: .05, transparent: true, opacity: .85, clearcoat: 1, envMap: ENV, envMapIntensity: .6 });
    const tm = mk(new THREE.CapsuleGeometry(.007, .05, 4, 8), tmM, tg, 0, -.025, 0, 1, 1, .5); tm.castShadow = false; const td = mk(SPH, tmM, tg, 0, -.062, .003, .013, .017, .009); td.castShadow = false;
    const ck = mk(SPH, new THREE.MeshStandardMaterial({ color: 0xF59AA0, roughness: .8, transparent: true, opacity: .45 }), head, s * .14, HC - .08, surfZ(s * .14, HC - .08) - .006, .045, .028, .012); ck.castShadow = false;
    const lash = new THREE.Group(); lash.position.set(ex, ey, ez + .066); lash.rotation.y = s * .22; head.add(lash);
    const la = mk(new THREE.TorusGeometry(.046, .0075, 8, 24, Math.PI), new THREE.MeshStandardMaterial({ color: 0x2A1A18, roughness: .6 }), lash, 0, 0, 0); la.castShadow = false;
    lashes.push(lash);
    eyes.push(eg); irises.push(ig); lidsU.push(lu); lidsL.push(ll); brows.push(bg); tears.push(tg);
  }
  // the mouth: closed lines (smile / flat / frown / wobble) and an open mouth (dark, tongue, teeth) scaled by the voice
  const mY = HC - .135, mZ = surfZ(0, HC - .135);
  const mouthG = new THREE.Group(); mouthG.position.set(0, mY, mZ - .006); head.add(mouthG);
  const lipM = new THREE.MeshStandardMaterial({ color: 0x7A3A30, roughness: .6 });
  const curve = (k) => new THREE.TubeGeometry(new THREE.QuadraticBezierCurve3(v3(-.045, k, 0), v3(0, -k, .006), v3(.045, k, 0)), 16, .0065, 6);
  const lines = { smile: mk(curve(.014), lipM, mouthG, 0, 0, 0), flat: mk(curve(0), lipM, mouthG, 0, 0, 0), sad: mk(curve(-.014), lipM, mouthG, 0, 0, 0) };
  const wob = new THREE.TubeGeometry(new THREE.CatmullRomCurve3([v3(-.045, -.006, 0), v3(-.022, .004, .004), v3(0, -.004, .006), v3(.022, .004, .004), v3(.045, -.006, 0)]), 20, .0065, 6); lines.wavy = mk(wob, lipM, mouthG, 0, 0, 0);
  const open = new THREE.Group(); mouthG.add(open);
  mk(SPH, new THREE.MeshStandardMaterial({ color: 0x3A0E14, roughness: .8 }), open, 0, 0, 0, .045, .03, .012);
  mk(SPH, new THREE.MeshStandardMaterial({ color: 0xD8616A, roughness: .7 }), open, 0, -.014, .004, .028, .012, .008);
  const teeth = mk(SPH, new THREE.MeshStandardMaterial({ color: 0xFFFFFF, roughness: .4 }), open, 0, .021, .006, .034, .007, .006);
  // hair: soft wavy clumps on top and at the back, a swept fringe
  const HP = [[0, .5, -.02, .2, .1, .19], [-.13, .46, .02, .13, .1, .15], [.13, .47, .0, .13, .1, .15], [-.2, .37, -.04, .09, .12, .15], [.2, .38, -.05, .09, .12, .15], [0, .4, -.17, .2, .14, .12], [-.12, .33, -.2, .14, .12, .1], [.12, .33, -.2, .14, .12, .1],
    [-.06, .47, .15, .14, .065, .08], [.08, .46, .16, .12, .06, .07], [.17, .43, .12, .07, .06, .07], [-.18, .42, .1, .07, .07, .07], [0, .52, .05, .15, .06, .14], [.05, .55, -.08, .1, .05, .1]];
  for (const [x, y, z, sx, sy, sz] of HP) { const h = mk(SPH, hairM, head, x, y, z, sx, sy, sz); h.rotation.set(hash(x * 9 + y) * .6 - .3, hash(z * 7 + x) * .8, hash(y * 5) * .5 - .25); }
  // arms (hoodie sleeves with cuffs, soft hands) and legs (joggers with cuffs, white sneakers)
  const sh = [], el = [], hand = [], hip = [], knee = [];
  for (let k = 0; k < 2; k++) {
    const s = k ? 1 : -1;
    const a = new THREE.Group(); a.position.set(s * .31, .52, 0); torso.add(a); sh.push(a);
    mk(new THREE.CapsuleGeometry(.09, .2, 6, 16), hoodM, a, 0, -.13, 0);
    const e = new THREE.Group(); e.position.y = -.29; a.add(e); el.push(e);
    mk(new THREE.CapsuleGeometry(.082, .16, 6, 16), hoodM, e, 0, -.12, 0);
    mk(new THREE.CylinderGeometry(.075, .078, .05, 16), hoodM, e, 0, -.24, 0);
    const hd = new THREE.Group(); hd.position.y = -.31; e.add(hd);
    mk(SPH, skinM, hd, 0, -.01, 0, .062, .072, .042); mk(SPH, skinM, hd, s * -.045, .005, .02, .022, .032, .02);
    hand.push(hd);
    const h = new THREE.Group(); h.position.set(s * .13, 0, 0); hips.add(h); hip.push(h);
    mk(new THREE.CapsuleGeometry(.115, .24, 6, 16), pantM, h, 0, -.19, 0);
    const kn = new THREE.Group(); kn.position.y = -.4; h.add(kn); knee.push(kn);
    mk(new THREE.CapsuleGeometry(.098, .2, 6, 16), pantM, kn, 0, -.16, 0);
    mk(new THREE.CylinderGeometry(.085, .09, .05, 16), pantM, kn, 0, -.29, 0);
    mk(new RoundedBoxGeometry(.2, .12, .33, 4, .055), shoeM, kn, 0, -.37, .05);
    mk(new RoundedBoxGeometry(.21, .035, .34, 3, .015), mat(0xDCDCDA), kn, 0, -.425, .05);
  }
  return { root, hips, torso, head, sh, el, hand, hip, knee, eyes, irises, lidsU, lidsL, brows, tears, lashes, lines, open, teeth, seed: 1.7, toy: true };
}
// face: eyes 'open'|'wide'|'half'|'closed'|'happy'|'teary'|'cry'|'sob'; brows 'flat'|'up'|'high'|'worry'|'despair'|'angry'|'raise1';
// mouth 'smile'|'flat'|'sad'|'wavy'|'o'|'gasp'|'wail'|'rant'|'laugh'|'grin'; talk: the mouth opens with the voice (CT.voiceEnv)
function setToyFace(P, f) {
  let eyes = f.eyes || "open";
  const blink = (eyes === "open" || eyes === "wide" || eyes === "teary") && !f.noblink && blinkAt(P.seed, NOW);
  const LID = { open: [-1.35, 1.45], wide: [-1.6, 1.6], half: [-.55, 1.45], closed: [.14, -.06], happy: [.14, -.06], teary: [-1.2, 1.25], cry: [.14, -.06], sob: [.14, -.06] }[eyes] || [-1.35, 1.45];
  for (let k = 0; k < 2; k++) {
    P.lidsU[k].rotation.x = blink ? .14 : LID[0]; P.lidsL[k].rotation.x = blink ? -.06 : LID[1];
    const shut = blink || eyes === "closed" || eyes === "cry" || eyes === "happy" || eyes === "sob";
    P.lashes[k].visible = shut; P.lashes[k].rotation.z = (eyes === "happy" || eyes === "sob") ? 0 : Math.PI;    // up-curved when happy, down when crying
    P.lashes[k].position.y = .28 + .02 + ((eyes === "happy" || eyes === "sob") ? -.012 : .012);
    P.irises[k].scale.setScalar(1);
    const lk = f.look || [0, 0]; P.irises[k].position.set(lk[0] * .012, lk[1] * .012, .03);
    P.tears[k].visible = eyes === "teary" || eyes === "cry" || eyes === "sob";
    P.tears[k].scale.y = eyes === "teary" ? .35 : 1;
    const s = k ? 1 : -1, b = P.brows[k];
    const BR = { flat: [0, 0], up: [.02, 0], high: [.035, .05], worry: [.012, .35], despair: [.02, .55], angry: [-.012, -.45], raise1: [k ? 0 : .035, 0] }[f.brows || "flat"];
    b.position.y = .29 + .12 + BR[0]; b.rotation.z = s * -BR[1];
  }
  let mouth = f.mouth || "smile", amt = 0;
  if (f.talk) { amt = envAt(C.voiceEnv, NOW); }
  const OPEN = { o: [.55, .55], gasp: [.7, .9], wail: [1.2, 1.1], rant: [1.1, .8], laugh: [1.15, .75], grin: [1.0, .35] };
  let os = null;
  if (OPEN[mouth]) os = OPEN[mouth];
  if (f.talk && amt > .06) { const base = os || [.9, .5]; os = [base[0] * (.75 + .25 * amt), Math.max(.18, base[1] * (.3 + amt))]; }
  for (const k in P.lines) P.lines[k].visible = !os && k === (P.lines[mouth] ? mouth : "flat");
  P.open.visible = !!os;
  if (os) { P.open.scale.set(os[0], os[1], 1); P.teeth.visible = mouth !== "o" && mouth !== "gasp"; }
}
function placeToy(P, vis, p, f) { P.root.visible = !!vis; if (!vis) return; applyPose(P, p); setToyFace(P, f || {}); }
const LEO = makeToy(scene);
// his phone (in the right hand)
LEO.phone = new THREE.Group(); LEO.hand[1].add(LEO.phone); LEO.phone.position.set(0, -.04, .07);
rbox(.075, .15, .01, mat(0x2A2A30, { roughness: .3 }), 0, 0, 0, .008, { parent: LEO.phone, cast: false });
LEO.scr = new THREE.MeshBasicMaterial({ color: 0xDDE8FF, toneMapped: false }); { const sp = new THREE.Mesh(new THREE.PlaneGeometry(.066, .138), LEO.scr); sp.position.z = -.006; sp.rotation.y = Math.PI; LEO.phone.add(sp); }
const PEN = cyl(.007, .007, .13, mat(0xF343A2), 0, 0, 0, 8); PEN.rotation.z = Math.PI / 2;
