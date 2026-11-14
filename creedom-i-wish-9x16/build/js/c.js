
// ================================================================= THE BEDROOM STUDIO (one room at night)
// The desk faces the camera side (+z) with the creator's chair behind it (z = -.7). Back wall z = -2.3 with the window
// (left) and fairy lights; the bed in the back-right corner; a doorway in the left wall onto a dark hall.
const SET = {};
const mkSet = (k) => { const g = new THREE.Group(); g.visible = false; scene.add(g); SET[k] = g; PARENT = g; return g; };
function v3(x, y, z) { return new THREE.Vector3(x, y, z); }
const RM = mkSet("room");
const SEAT = v3(-.15, 0, -.7), SITY = .52 - .71;
const DESKY = .8;
{
  const plank = pix(64, 64, (g) => { px(g, "#7A5238", 0, 0, 64, 64); for (let j = 0; j < 8; j++) { px(g, j % 2 ? "#71492F" : "#83583C", 0, j * 8, 64, 8); px(g, "#5A3A26", 0, j * 8, 64, 1); px(g, "#5A3A26", (j * 23) % 64, j * 8, 1, 8); } }, false);
  flat(9, 8, new THREE.MeshStandardMaterial({ map: rep(plank, 5, 4), roughness: .55 }), 0, 0, 0);
  const wallM = mat(0x6E5A86), trim = mat(0x3A2C4A);
  box(9, 3.2, .2, wallM, 0, 1.6, -2.4);
  // left wall with a doorway (1 m wide, 2.1 m tall) at z = -1.0
  box(.2, 3.2, 2.9, wallM, -3.4, 1.6, 1.95); box(.2, 3.2, 1.0, wallM, -3.4, 1.6, -2.0); box(.2, 1.1, 1.0, wallM, -3.4, 2.65, -1.0);
  box(.24, 2.12, .08, trim, -3.36, 1.06, -1.52); box(.24, 2.12, .08, trim, -3.36, 1.06, -.48); box(.24, .08, 1.12, trim, -3.36, 2.12, -1.0);
  box(.2, 3.2, 8, wallM, 3.5, 1.6, 1.5);
  box(9, .12, 8, mat(0x4A3A5C), 0, 3.2, 1.5, { cast: false });
  box(9, .1, .05, trim, 0, .05, -2.29);
  // the hall behind the doorway: dark, with a pink glow far down it
  RM.hall = new THREE.Group(); RM.add(RM.hall);
  box(3, .05, 1.2, mat(0x2A2236), -4.9, .0, -1.0, { parent: RM.hall }); box(3, 2.4, .1, mat(0x2A2236), -4.9, 1.2, -1.6, { parent: RM.hall }); box(3, 2.4, .1, mat(0x2A2236), -4.9, 1.2, -.4, { parent: RM.hall });
  box(.1, 2.4, 1.2, mat(0x2A2236), -6.3, 1.2, -1.0, { parent: RM.hall });
  // window onto the night (back wall, left), with a sill
  box(1.5, 1.4, .06, trim, -1.55, 1.75, -2.28); RM.winM = texMat("night", { transparent: false }); plane(1.36, 1.26, RM.winM, -1.55, 1.75, -2.24, 0);
  box(.04, 1.26, .04, trim, -1.55, 1.75, -2.22); box(1.36, .04, .04, trim, -1.55, 1.75, -2.22); box(1.6, .06, .2, trim, -1.55, 1.02, -2.2);
  // fairy lights along the back wall, sagging between pins
  RM.fairy = [];
  const FC = [0xFFD27A, 0xFF8CC6, 0xFFE9B0, 0xF9A8D4];
  for (let i = 0; i < 46; i++) { const x = -3.2 + i * .1; const sag = .12 * Math.sin((i % 10) / 10 * Math.PI); const b = new THREE.Mesh(new THREE.SphereGeometry(.022, 8, 6), glow(FC[i % 4])); b.position.set(x, 2.55 - sag, -2.27); RM.add(b); RM.fairy.push(b); }
  // posters and a shelf
  RM.posterM = texMat("posters", { transparent: false }); plane(1.0, .7, RM.posterM, .45, 2.0, -2.28, 0);
  box(1.0, .04, .25, trim, .45, 1.45, -2.2); for (let k = 0; k < 4; k++) box(.1, .26, .18, mat(["#F343A2", "#F2C94C", "#5B7FC4", "#E8735A"][k]), .05 + k * .14, 1.6, -2.2);
  cyl(.07, .06, .12, mat(0xE8735A), .82, 1.53, -2.2, 12); for (let j = 0; j < 3; j++) box(.12 - j * .02, .12, .12 - j * .02, mat(0x5E9C52), .82, 1.65 + j * .09, -2.2);
  // the desk (laptop closed, a lamp, a mug, a plant, the phone on a mini tripod) and the chair
  box(1.9, .07, .9, mat(0x5A3E2A, { roughness: .4 }), 0, DESKY - .035, 0); for (const s of [-1, 1]) box(.07, .73, .8, mat(0x3E2A1E), s * .9, .37, 0);
  box(1.8, .55, .05, mat(0x3E2A1E), 0, .45, .42);
  box(.42, .03, .3, metal(0x9C9CA6, .35), -.35, DESKY + .015, -.05);
  RM.lampShade = mat(0xFFB8DA, { emissive: 0xFFB8DA, emissiveIntensity: .8, roughness: .4 });
  cyl(.08, .1, .03, metal(0x2A2A2E, .4), -.78, DESKY + .015, -.2, 14); cyl(.012, .012, .34, metal(0x2A2A2E, .4), -.78, DESKY + .19, -.2, 8); cyl(.07, .15, .14, RM.lampShade, -.78, DESKY + .38, -.15, 16);
  cyl(.045, .04, .1, mat(0xF4EFE6), .78, DESKY + .05, .2, 12);
  cyl(.06, .05, .09, mat(0xC9644E), .8, DESKY + .045, -.25, 10); box(.13, .15, .13, mat(0x4E8C48), .8, DESKY + .17, -.25);
  // the phone on its mini tripod (screen faces the chair)
  RM.tri = new THREE.Group(); RM.tri.position.set(.55, DESKY, -.05); RM.add(RM.tri);
  for (let k = 0; k < 3; k++) { const l = cyl(.006, .006, .16, metal(0x2A2A2E, .4), Math.sin(k * 2.1) * .04, .07, Math.cos(k * 2.1) * .04, 6, { parent: RM.tri }); l.rotation.set(Math.cos(k * 2.1) * .35, 0, -Math.sin(k * 2.1) * .35); }
  box(.09, .17, .012, mat(0x16141A, { roughness: .3 }), 0, .23, 0, { parent: RM.tri });
  RM.triScr = new THREE.MeshBasicMaterial({ color: 0xFFE3F1, toneMapped: false }); const ts = new THREE.Mesh(new THREE.PlaneGeometry(.08, .155), RM.triScr); ts.position.set(0, .23, -.007); ts.rotation.y = Math.PI; RM.tri.add(ts);
  box(.55, .08, .5, mat(0x2A2236), SEAT.x, .5, SEAT.z - .05); box(.55, .7, .1, mat(0x2A2236), SEAT.x, .9, SEAT.z - .32);
  // ring light on a stand, front-left of the desk, facing the chair
  RM.ring = new THREE.Group(); RM.ring.position.set(-1.25, 0, .55); RM.ring.rotation.y = -.75; RM.add(RM.ring);
  cyl(.012, .012, 1.45, metal(0x2A2A2E, .4), 0, .72, 0, 8, { parent: RM.ring }); for (let k = 0; k < 3; k++) { const l = cyl(.01, .01, .45, metal(0x2A2A2E, .4), Math.sin(k * 2.1) * .14, .17, Math.cos(k * 2.1) * .14, 6, { parent: RM.ring }); l.rotation.set(Math.cos(k * 2.1) * .7, 0, -Math.sin(k * 2.1) * .7); }
  RM.ringM = new THREE.MeshBasicMaterial({ color: 0xFFF1E6, toneMapped: false });
  const rg = new THREE.Mesh(new THREE.TorusGeometry(.22, .025, 10, 48), RM.ringM); rg.position.y = 1.55; RM.ring.add(rg);
  // the bed (back-right corner), pillow, blanket, a plant, a rug
  box(1.4, .32, 2.1, mat(0x3A2C4A), 2.7, .16, -1.25); box(1.36, .2, 2.04, mat(0xF4ECF4, { roughness: .9 }), 2.7, .42, -1.25);
  box(1.4, .9, .1, mat(0x3A2C4A), 2.7, .45, -2.3);
  box(.8, .14, .42, mat(0xFFF6FA, { roughness: .95 }), 2.7, .6, -1.98, { round: .06 }); box(.7, .14, .4, mat(0xFFE3F1, { roughness: .95 }), 2.7, .69, -.42, { round: .06 });
  box(1.38, .12, 1.25, mat(0xD9468F, { roughness: .95 }), 2.7, .56, -.8, { round: .05 });
  RM.bedPhone = new THREE.Group(); RM.bedPhone.position.set(2.25, .63, -1.35); RM.add(RM.bedPhone); box(.09, .012, .17, mat(0x16141A, { roughness: .3 }), 0, 0, 0, { parent: RM.bedPhone });
  RM.bedScr = new THREE.MeshBasicMaterial({ color: 0xFFE3F1, toneMapped: false }); const bs = new THREE.Mesh(new THREE.PlaneGeometry(.08, .155), RM.bedScr); bs.rotation.x = -Math.PI / 2; bs.position.y = .007; RM.bedPhone.add(bs);
  cyl(.22, .18, .4, mat(0xE8735A), -2.9, .2, -1.9, 12); for (let j = 0; j < 4; j++) box(.38 - j * .06, .34, .38 - j * .06, mat(j % 2 ? 0x4E7A3E : 0x5E8C48), -2.9, .55 + j * .3, -1.9);
  flat(3.2, 2.4, mat(0xB84A86, { roughness: .95 }), .3, .005, .2);
  // crumpled paper balls around the bin
  cyl(.15, .12, .32, mat(0x2A2236), 1.25, .16, -.5, 14); for (let k = 0; k < 6; k++) { const b = new THREE.Mesh(new THREE.IcosahedronGeometry(.05, 0), mat(0xF4F1EA)); b.position.set(1.0 + hash(k) * .5, .045, -.2 + hash(k * 3) * .5); b.rotation.set(k, k * 2, k * 3); add(b); }
  RM.key = new THREE.PointLight(0xFFE7F0, 0, 6, 1.5); RM.key.position.set(-1.1, 1.6, .4); scene.add(RM.key);      // the ring light
  RM.fill = new THREE.PointLight(0xB89CFF, 0, 9, 1.4); RM.fill.position.set(1.2, 2.6, 2.4); scene.add(RM.fill);
  RM.lamp = new THREE.PointLight(0xFFB8DA, 0, 3, 1.8); RM.lamp.position.set(-.78, 1.3, -.1); scene.add(RM.lamp);
  RM.moon = new THREE.PointLight(0x9CC4FF, 0, 4, 1.6); RM.moon.position.set(-1.55, 1.8, -1.6); scene.add(RM.moon);
  RM.hallL = new THREE.PointLight(0xFF4FAE, 0, 4, 1.4); RM.hallL.position.set(-5.4, .7, -1.0); scene.add(RM.hallL);
  RM.hero = new THREE.PointLight(0xFFB0D8, 0, 4, 1.5); scene.add(RM.hero);
  RM.gold = new THREE.PointLight(0xFFD27A, 0, 3, 1.6); scene.add(RM.gold);
}
// ---------------------------------------------------------------- the reel-world props: a glowing film strip, reel cards, the DM machine, paper planes
const glowTex = (inner, outer) => pix(128, 128, (g) => { const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, inner); gr.addColorStop(.35, outer); gr.addColorStop(1, "rgba(0,0,0,0)"); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); }, false);
const addM = (tx, c = 0xffffff) => new THREE.MeshBasicMaterial({ map: tx, color: c, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false });
const FX = {};
{
  // the film strip: 8 frames floating over the desk in an arc
  FX.strip = new THREE.Group(); RM.add(FX.strip);
  FX.frames = [];
  for (let i = 0; i < 8; i++) {
    const f = new THREE.Group(); f.position.set(-.85 + i * .24, DESKY + .42, -.12 - .1 * Math.sin(i / 7 * Math.PI)); f.rotation.y = (3.5 - i) * .05; FX.strip.add(f);
    const fm = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .92, toneMapped: false }); LATE.push([fm, "thumb" + (i % 4)]);
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.18, .3), fm); f.add(p);
    const edge = new THREE.Mesh(new THREE.PlaneGeometry(.21, .33), new THREE.MeshBasicMaterial({ color: 0xFFC7E3, transparent: true, opacity: .55, toneMapped: false })); edge.position.z = -.002; f.add(edge);
    f.edge = edge; f.pm = fm; FX.frames.push(f);
  }
  FX.track = new THREE.Mesh(new THREE.PlaneGeometry(2.0, .012), new THREE.MeshBasicMaterial({ color: 0xFF8CC6, toneMapped: false })); FX.track.position.set(0, DESKY + .22, -.16); FX.strip.add(FX.track);
  // reel cards: frosted glass, fanned out
  FX.cards = new THREE.Group(); RM.add(FX.cards); FX.cardL = [];
  for (let i = 0; i < 5; i++) {
    const c = new THREE.Group(); FX.cards.add(c);
    const cmat = new THREE.MeshPhysicalMaterial({ color: i === 3 ? 0xFFE7A8 : 0xFFE3F1, roughness: .25, transparent: true, opacity: .82, emissive: i === 3 ? 0xFFC24A : 0xFF8CC6, emissiveIntensity: i === 3 ? .9 : .25, side: THREE.DoubleSide });
    const m = new THREE.Mesh(new RoundedBoxGeometry(.2, .32, .01, 2, .02), cmat); c.add(m);
    const im = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .9, toneMapped: false }); LATE.push([im, "thumb" + ((i + 1) % 4)]);
    const ip = new THREE.Mesh(new THREE.PlaneGeometry(.16, .22), im); ip.position.set(0, .03, .007); c.add(ip);
    c.cmat = cmat; FX.cardL.push(c);
  }
  // the DM machine: a small pink box with a lever and a slot
  FX.mach = new THREE.Group(); FX.mach.position.set(.3, DESKY, .15); RM.add(FX.mach);
  box(.26, .16, .18, gloss(0xF06BB4), 0, .08, 0, { parent: FX.mach, round: .03 }); box(.14, .02, .02, mat(0x3A1A2E), 0, .12, .091, { parent: FX.mach });
  const piv = new THREE.Group(); piv.position.set(.135, .1, 0); FX.mach.add(piv); FX.lever = piv;
  cyl(.008, .008, .16, metal(0xD9D9DE, .3), 0, .08, 0, 8, { parent: piv }); const kn = new THREE.Mesh(new THREE.SphereGeometry(.025, 14, 10), gloss(0xF2C94C)); kn.position.y = .17; piv.add(kn);
  FX.machLight = new THREE.Mesh(new THREE.SphereGeometry(.015, 10, 8), glow(0x5BE3B0)); FX.machLight.position.set(-.08, .17, .05); FX.mach.add(FX.machLight);
  // paper planes
  FX.planes = [];
  const pg = new THREE.BufferGeometry(); pg.setAttribute("position", new THREE.Float32BufferAttribute([0, 0, .07, -.045, 0, -.04, 0, .006, -.03, 0, 0, .07, .045, 0, -.04, 0, .006, -.03, 0, 0, .07, 0, -.02, -.035, 0, .006, -.03], 3)); pg.computeVertexNormals();
  for (let i = 0; i < 12; i++) { const p = new THREE.Mesh(pg, new THREE.MeshBasicMaterial({ color: i % 3 ? 0xFFF4FA : 0xFFD6EC, side: THREE.DoubleSide, toneMapped: false })); RM.add(p); FX.planes.push(p); }
  // light: glow sprites and god rays for the hero entrance and the end card; dust motes
  FX.glow = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), addM(glowTex("rgba(255,214,236,1)", "rgba(243,67,162,.55)"))); scene.add(FX.glow);
  FX.glow2 = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), addM(glowTex("rgba(255,236,190,1)", "rgba(255,190,90,.4)"))); scene.add(FX.glow2);
  const rayT = pix(64, 256, (g) => { const gr = g.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, "rgba(255,220,240,0)"); gr.addColorStop(.25, "rgba(255,200,230,.7)"); gr.addColorStop(1, "rgba(255,200,230,0)"); g.fillStyle = gr; g.beginPath(); g.moveTo(26, 256); g.lineTo(38, 256); g.lineTo(64, 0); g.lineTo(0, 0); g.fill(); }, false);
  FX.rays = new THREE.Group(); scene.add(FX.rays);
  for (let i = 0; i < 9; i++) { const r = new THREE.Mesh(new THREE.PlaneGeometry(.5, 2.4), addM(rayT)); r.geometry.translate(0, 1.2, 0); r.rotation.z = (i - 4) * .33; r.ray = i; FX.rays.add(r); }
  const dg = new THREE.BufferGeometry(); const dp = [];
  for (let i = 0; i < 220; i++) dp.push(hash(i * 1.3) - .5, hash(i * 2.7), hash(i * 4.1) - .5);
  dg.setAttribute("position", new THREE.Float32BufferAttribute(dp, 3));
  FX.dust = new THREE.Points(dg, new THREE.PointsMaterial({ size: .012, map: glowTex("rgba(255,255,255,1)", "rgba(255,170,215,.6)"), color: 0xFFC2E2, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false })); scene.add(FX.dust);
  FX.base = dp;
  // the doorway glow (reveal 1)
  FX.door = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), addM(glowTex("rgba(255,120,200,1)", "rgba(243,67,162,.5)"))); scene.add(FX.door);
}
PARENT = scene;

// ---------------------------------------------------------------- Cree: Creedom's mascot, a soft magenta plush egg (to the character sheet)
// Built at 1 unit tall; CREE.root is scaled to his size in the room. Pivots: bod (squash), eyes, brows, beak, wings, feet.
const CREE = { root: new THREE.Group() };
scene.add(CREE.root);
{
  const R = CREE.root;
  const plush = new THREE.MeshPhysicalMaterial({ color: 0xF343A2, roughness: .62, sheen: 1, sheenColor: new THREE.Color(0xFF8CC6), sheenRoughness: .35, envMap: ENV, envMapIntensity: .35 });
  CREE.plush = plush;
  const bod = new THREE.Group(); R.add(bod); CREE.bod = bod;
  const g = new THREE.SphereGeometry(.5, 72, 54); const pa = g.attributes.position;
  for (let i = 0; i < pa.count; i++) { const y = pa.getY(i); const w = 1 + .12 * (-y / .5) - .04 * Math.max(0, y / .5) ** 2; pa.setX(i, pa.getX(i) * w); pa.setZ(i, pa.getZ(i) * w * .96); pa.setY(i, y * 1.02); }
  g.computeVertexNormals();
  const body = new THREE.Mesh(g, plush); body.position.y = .52; body.castShadow = true; body.receiveShadow = true; bod.add(body);
  // eyes: glossy white, big black pupils, two catchlights; a soft pink rim around each
  const sclM = CREE.sclM = new THREE.MeshPhysicalMaterial({ color: 0xFFFFFF, roughness: .15, clearcoat: 1, clearcoatRoughness: .05, envMap: ENV, envMapIntensity: .5 });
  const pupM = CREE.pupM = new THREE.MeshPhysicalMaterial({ color: 0x0B0B10, roughness: .08, clearcoat: 1, clearcoatRoughness: .03, envMap: ENV, envMapIntensity: .9 });
  const catM = new THREE.MeshBasicMaterial({ color: 0xFFFFFF, toneMapped: false });
  const rimM = CREE.rimM = new THREE.MeshStandardMaterial({ color: 0xFFC2DE, roughness: .6 });
  CREE.eyes = []; CREE.pupils = []; CREE.cats = [];
  for (const s of [-1, 1]) {
    const eg = new THREE.Group(); eg.position.set(s * .175, .62, .395); eg.rotation.y = s * .32; bod.add(eg);
    const rim = new THREE.Mesh(new THREE.SphereGeometry(.165, 32, 24), rimM); rim.scale.set(1, 1.1, .45); eg.add(rim);
    const scl = new THREE.Mesh(new THREE.SphereGeometry(.15, 32, 24), sclM); scl.scale.set(1, 1.1, .55); scl.position.z = .015; eg.add(scl);
    const pg = new THREE.Group(); pg.position.z = .06; eg.add(pg);
    const pup = new THREE.Mesh(new THREE.SphereGeometry(.105, 28, 20), pupM); pup.scale.set(1, 1.08, .5); pg.add(pup);
    const c1 = new THREE.Mesh(new THREE.SphereGeometry(.03, 12, 10), catM); c1.position.set(.035, .045, .05); c1.scale.z = .4; pg.add(c1);
    const c2 = new THREE.Mesh(new THREE.SphereGeometry(.014, 10, 8), catM); c2.position.set(-.035, -.04, .05); c2.scale.z = .4; pg.add(c2);
    const arc = new THREE.Mesh(new THREE.TorusGeometry(.085, .022, 10, 28, Math.PI), new THREE.MeshStandardMaterial({ color: 0x1A0A14, roughness: .5 })); arc.position.set(s * .175, .64, .445); arc.rotation.y = s * .32; arc.visible = false; bod.add(arc);
    eg.arc = arc;
    CREE.eyes.push(eg); CREE.pupils.push(pg); CREE.cats.push([c1, c2]);
  }
  // brows: thin darker pink arcs
  CREE.brows = [];
  for (const s of [-1, 1]) { const b = new THREE.Mesh(new THREE.CapsuleGeometry(.014, .1, 4, 10), new THREE.MeshStandardMaterial({ color: 0xB0106A, roughness: .6 })); b.rotation.z = Math.PI / 2; const bg = new THREE.Group(); bg.position.set(s * .175, .82, .405); bg.add(b); bod.add(bg); CREE.brows.push(bg); }
  // beak: upper and lower halves, yellow-orange, red inside; the lower half hinges open
  const beakM = new THREE.MeshPhysicalMaterial({ color: 0xFFC21A, roughness: .35, clearcoat: .6, clearcoatRoughness: .2, envMap: ENV, envMapIntensity: .4 });
  const beakM2 = new THREE.MeshPhysicalMaterial({ color: 0xF2A516, roughness: .4, clearcoat: .5, envMap: ENV, envMapIntensity: .3 });
  const up = new THREE.Mesh(new THREE.SphereGeometry(.085, 28, 18, 0, Math.PI * 2, 0, Math.PI / 2), beakM); up.scale.set(1.15, .7, 1.05); up.position.set(0, .495, .485); up.rotation.x = .25; bod.add(up);
  const mouth = new THREE.Mesh(new THREE.SphereGeometry(.06, 18, 12), new THREE.MeshStandardMaterial({ color: 0x9E1B2E, roughness: .7 })); mouth.scale.set(1.1, .6, .6); mouth.position.set(0, .48, .47); bod.add(mouth);
  const lowG = new THREE.Group(); lowG.position.set(0, .49, .46); bod.add(lowG);
  const low = new THREE.Mesh(new THREE.SphereGeometry(.07, 24, 14, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), beakM2); low.scale.set(1.05, .75, 1.0); low.position.set(0, 0, .02); lowG.add(low);
  CREE.jaw = lowG;
  // wings: short rounded arms, pivoting at the shoulder
  CREE.wings = [];
  for (const s of [-1, 1]) {
    const pv = new THREE.Group(); pv.position.set(s * .45, .5, .02); bod.add(pv);
    const w = new THREE.Mesh(new THREE.SphereGeometry(.13, 24, 18), plush); w.scale.set(.6, 1.15, .78); w.position.set(s * .03, -.11, 0); w.castShadow = true; pv.add(w);
    const tip = new THREE.Group(); tip.position.set(s * .04, -.24, .02); pv.add(tip); pv.tip = tip;
    CREE.wings.push(pv);
  }
  // feet: stubby yellow-orange ovals
  CREE.feet = [];
  for (const s of [-1, 1]) { const f = new THREE.Mesh(new THREE.SphereGeometry(.1, 22, 14), beakM2); f.scale.set(1.05, .5, 1.5); const fg = new THREE.Group(); fg.position.set(s * .15, .04, .14); fg.add(f); f.castShadow = true; R.add(fg); CREE.feet.push(fg); }
  // the magnifier: a clear lens, thin gold rim, wooden handle (held in the right wing, or lying on the desk)
  const mg = new THREE.Group(); CREE.mag = mg;
  const rim = new THREE.Mesh(new THREE.TorusGeometry(.11, .012, 10, 40), goldM); mg.add(rim);
  const lens = new THREE.Mesh(new THREE.CircleGeometry(.105, 36), new THREE.MeshPhysicalMaterial({ color: 0xEAF6FF, roughness: 0, transparent: true, opacity: .22, envMap: ENV, envMapIntensity: 1.5, side: THREE.DoubleSide })); mg.add(lens);
  const hd = new THREE.Mesh(new THREE.CylinderGeometry(.016, .02, .17, 12), mat(0x8A5A34, { roughness: .5 })); hd.position.y = -.2; mg.add(hd);
  const fer = new THREE.Mesh(new THREE.CylinderGeometry(.019, .019, .025, 12), goldM); fer.position.y = -.115; mg.add(fer);
  scene.add(mg);
}
// state -> pose. s: {x, y, z, ry, sc, sq (squash), lean, wl/wr: [rz, rx] wing angles, eyes ('open'|'happy'|'wide'|'squint'|'closed'),
// look: [x, y], jaw (0..1), brow (tilt), browY, mag ('hand'|'desk'|null), magAt (desk position), oneEye}
function placeCree(vis, s) {
  CREE.root.visible = !!vis; CREE.mag.visible = !!(vis && s.mag);
  if (!vis) return;
  const R = CREE.root, sc = s.sc ?? .34, sq = s.sq ?? 0;
  const dk = !!CREE.dark;      // silhouette: no environment light, dark eyes
  CREE.plush.envMapIntensity = dk ? 0 : .35; CREE.sclM.envMapIntensity = dk ? 0 : .5; CREE.sclM.color.set(dk ? 0x2A1A26 : 0xFFFFFF); CREE.rimM.color.set(dk ? 0x2A1424 : 0xFFC2DE); CREE.pupM.envMapIntensity = dk ? 0 : .9;
  R.position.set(s.x, s.y, s.z); R.rotation.set(s.lean ?? 0, s.ry ?? 0, s.roll ?? 0); R.scale.setScalar(sc);
  CREE.bod.scale.set(1 + sq * .5, 1 - sq, 1 + sq * .5);
  for (let k = 0; k < 2; k++) {
    const w = k ? s.wr : s.wl, sgn = k ? 1 : -1;
    CREE.wings[k].rotation.set(w ? w[1] : 0, 0, sgn * (w ? w[0] : .15));
    const e = s.eyes || "open", eg = CREE.eyes[k];
    let ey = 1; if (e === "closed") ey = .08; else if (e === "squint") ey = .5; else if (e === "wide") ey = 1.12;
    if (e === "open" && !s.noblink && blinkAt(3.3, NOW)) ey = .08;
    eg.scale.set(e === "wide" ? 1.1 : 1, ey, 1);
    const pg = CREE.pupils[k]; const lk = s.look || [0, 0];
    pg.position.set(lk[0] * .035, lk[1] * .035, .06); pg.scale.setScalar(e === "wide" ? .82 : (e === "happy" ? .01 : 1));
    for (const c of CREE.cats[k]) c.visible = !(s.oneEye && k === 0);
    const b = CREE.brows[k]; b.rotation.z = sgn * (s.brow ?? 0); b.position.y = .82 + (s.browY ?? 0) + (e === "wide" ? .04 : 0);
  }
  // happy eyes: the eyes close into dark upturned arcs
  for (const eg of CREE.eyes) { const h = s.eyes === "happy"; eg.visible = !h; eg.arc.visible = h; }
  CREE.jaw.rotation.x = (s.jaw ?? .25) * .9;
  for (let k = 0; k < 2; k++) { const f = CREE.feet[k]; f.position.y = .04 + (s.step && (k ? s.step > 0 : s.step < 0) ? Math.abs(s.step) * .08 : 0); f.rotation.x = 0; }
  R.updateMatrixWorld(true);
  if (s.mag === "hand") { const tip = CREE.wings[1].tip; tip.getWorldPosition(V); CREE.mag.position.copy(V).add(V2.set(0, .035 * sc / .34, .02)); CREE.mag.rotation.set(s.magRx ?? 0, s.ry ?? 0, s.magRz ?? .25); CREE.mag.scale.setScalar(sc / .34 * .55); }
  if (s.mag === "desk") { CREE.mag.position.copy(s.magAt); CREE.mag.rotation.set(-Math.PI / 2 + .1, 0, .6); CREE.mag.scale.setScalar(.55); }
}
// gibberish talk: the beak flaps while Cree "speaks" (times from CT.chirps)
const chirpAt = (t) => C.chirps.some(([a, b]) => t > a && t < b);
const creeJaw = (t) => chirpAt(t) ? .25 + .75 * Math.abs(Math.sin(t * 19)) * (.6 + .4 * Math.sin(t * 7.3)) : .2;

// ---------------------------------------------------------------- the creator
const LEO = makeChar({ id: "leo", skin: "#E2AE86", hair: "#2A1A12", style: "short", top: "#EFE6D6", topStyle: "hoodie", pants: "#6A6660", shoe: "#FFFDF8", brow: "#2A1A12" }, scene);
LEO.seed = 1.7;
// a phone in his right hand (shown when he's holding it)
LEO.phone = new THREE.Group(); LEO.hand[1].add(LEO.phone); LEO.phone.position.set(0, -.08, .1);
box(.1, .18, .014, mat(0x16141A, { roughness: .3 }), 0, 0, 0, { parent: LEO.phone, cast: false });
LEO.scr = new THREE.MeshBasicMaterial({ color: 0xDDE8FF, toneMapped: false }); { const sp = new THREE.Mesh(new THREE.PlaneGeometry(.088, .165), LEO.scr); sp.position.z = -.008; sp.rotation.y = Math.PI; LEO.phone.add(sp); }
// a pen that rolls off the desk on the thud
const PEN = cyl(.008, .008, .14, mat(0xF343A2), 0, 0, 0, 8); PEN.rotation.z = Math.PI / 2;
