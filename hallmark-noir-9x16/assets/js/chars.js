// The cast, built from low-poly primitives (flat-shaded facets, in the style of the references): the detective and the
// client. Each is a rig of nested groups whose bones hang along local -Y. Arms are placed by a two-bone IK solver (the
// wrist goes to a world point, the elbow bends toward a pole), hands by a world orientation, fingers by curl. Faces
// carry brows, blinking lids and a mouth that can smile. Everything is set from time by world.js; nothing animates on
// its own.
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";

const DOWN = new THREE.Vector3(0, -1, 0);
const _v = new THREE.Vector3(), _w = new THREE.Vector3(), _q = new THREE.Quaternion(), _m = new THREE.Matrix4();

export const mat = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: .78, metalness: 0, flatShading: true, ...o });
const mesh = (geo, m, x = 0, y = 0, z = 0) => { const o = new THREE.Mesh(geo, m); o.position.set(x, y, z); o.castShadow = o.receiveShadow = true; return o; };
const grp = (parent, x = 0, y = 0, z = 0) => { const g = new THREE.Group(); g.position.set(x, y, z); if (parent) parent.add(g); return g; };
const rb = (w, h, d, r = .01, s = 1) => new RoundedBoxGeometry(w, h, d, s, Math.min(r, w / 2 - 1e-4, h / 2 - 1e-4, d / 2 - 1e-4));
// a limb segment of length len hanging down from its joint, tapered, faceted
const limb = (len, r0, r1, m, seg = 7) => { const g = new THREE.CylinderGeometry(r0, r1, len, seg, 1).translate(0, -len / 2, 0); return mesh(g, m); };
const ball = (r, m, d = 1) => mesh(new THREE.IcosahedronGeometry(r, d), m);

// ---------------------------------------------------------------- hands: a palm, four two-joint fingers, a thumb
function hand(parent, side, skin, size = 1) {
  const h = { root: grp(parent), fingers: [], thumb: null };
  const s = size;
  h.root.add(mesh(rb(.082 * s, .09 * s, .036 * s, .014 * s, 2).translate(0, -.043 * s, 0), skin));
  h.root.add(mesh(new THREE.CylinderGeometry(.03 * s, .034 * s, .03 * s, 7).translate(0, .004 * s, 0), skin));
  const xs = [-.0285, -.0095, .0095, .0285], lens = [.036, .042, .04, .031];
  xs.forEach((x, i) => {
    const k = grp(h.root, x * s * side, -.086 * s, 0);
    k.add(mesh(rb(.0195 * s, (lens[i] + .006) * s, .021 * s, .009 * s, 2).translate(0, -lens[i] * s / 2 + .003 * s, 0), skin));
    const j = grp(k, 0, -lens[i] * s, 0);
    j.add(mesh(rb(.018 * s, lens[i] * .85 * s, .0195 * s, .0085 * s, 2).translate(0, -lens[i] * .38 * s, 0), skin));
    h.fingers.push([k, j]);
  });
  const t = grp(h.root, .038 * s * side, -.022 * s, .008 * s);
  t.add(mesh(rb(.024 * s, .042 * s, .024 * s, .01 * s, 2).translate(0, -.019 * s, 0), skin));
  const t2 = grp(t, 0, -.038 * s, 0);
  t2.add(mesh(rb(.021 * s, .032 * s, .021 * s, .009 * s, 2).translate(0, -.014 * s, 0), skin));
  h.thumb = [t, t2]; h.side = side;
  return h;
}
// curl: 0 open .. 1 fist; spread: fingers fan; thumb: 0 alongside .. 1 across the palm; point: index stays straight
export function setHand(h, curl = .15, o = {}) {
  const { spread = .035, thumb = .3, point = false, pinch = false } = o;
  h.fingers.forEach(([k, j], i) => {
    // i = 3 is the index finger (next to the thumb) on both hands, i = 0 the little finger
    const c = point && i === 3 ? .05 : pinch && i >= 2 ? curl * .75 : curl;
    k.rotation.set(-c * 1.45, 0, (i - 1.5) * spread * h.side);
    j.rotation.set(-c * 1.6, 0, 0);
  });
  h.thumb[0].rotation.set(-.25 - thumb * .5, 0, h.side * (.75 - thumb * .55));
  h.thumb[1].rotation.set(-.2 - thumb * .6, 0, 0);
}

// ---------------------------------------------------------------- the rig
function rig(o) {
  const P = { root: new THREE.Group(), o };
  const { skin, coat, coat2, shirt, pants, shoe, hipH = .92, sh = .19 } = o;
  P.hips = grp(P.root, 0, hipH, 0);
  P.spine = grp(P.hips, 0, .02, 0);
  P.chest = grp(P.spine, 0, .26, 0);
  P.neck = grp(P.chest, 0, .25, 0);
  P.head = grp(P.neck, 0, .06, 0); P.head.rotation.order = "YXZ";
  for (const s of [1, -1]) {
    const k = s > 0 ? "L" : "R";
    const shld = grp(P.chest, s * sh, .2, 0);
    const up = limb(.28, .052, .045, coat); shld.add(up);
    shld.add(ball(.058, coat, 1));
    const elb = grp(shld, 0, -.28, 0);
    elb.add(ball(.046, coat, 1));
    elb.add(limb(.25, .045, .04, coat));
    const cuff = mesh(new THREE.CylinderGeometry(.044, .046, .03, 7).translate(0, -.235, 0), coat2); elb.add(cuff);
    if (shirt) elb.add(mesh(new THREE.CylinderGeometry(.034, .036, .02, 7).translate(0, -.258, 0), shirt));
    const wr = grp(elb, 0, -.265, 0);
    P["shoulder" + k] = shld; P["elbow" + k] = elb; P["wrist" + k] = wr;
    P["hand" + k] = hand(wr, s, skin, o.handSize || 1);
    setHand(P["hand" + k]);
    // legs
    const th = grp(P.hips, s * .095, 0, 0);
    th.add(limb(.44, .075, .06, pants)); th.add(ball(.075, pants, 1));
    const kn = grp(th, 0, -.44, 0); kn.add(ball(.06, pants, 1));
    kn.add(limb(.43, .058, .045, pants));
    const an = grp(kn, 0, -.43, 0);
    an.add(mesh(rb(.09, .07, .24, .02, 2).translate(0, -.035, .06), shoe));
    P["thigh" + k] = th; P["knee" + k] = kn; P["ankle" + k] = an;
  }
  P.len = [.28, .265];
  return P;
}

// two-bone IK: put the wrist at world point T, the elbow bent toward world point pole; then give the hand world
// orientation q (or leave it)
function aimBone(bone, worldTarget) {
  bone.parent.updateMatrixWorld(true);
  const origin = bone.getWorldPosition(_v);
  const dir = _w.copy(worldTarget).sub(origin).normalize();
  bone.parent.getWorldQuaternion(_q).invert();
  dir.applyQuaternion(_q);
  bone.quaternion.setFromUnitVectors(DOWN, dir);
  bone.updateMatrixWorld(true);
}
export function reach(P, side, T, pole, handQ) {
  const shld = P["shoulder" + side], elb = P["elbow" + side], wr = P["wrist" + side];
  P.chest.updateMatrixWorld(true);
  const S = shld.getWorldPosition(new THREE.Vector3());
  const [a, b] = P.len;
  const d = Math.min(Math.max(T.distanceTo(S), 1e-3), (a + b) * .995);
  const u = T.clone().sub(S).normalize();
  const cosA = THREE.MathUtils.clamp((a * a + d * d - b * b) / (2 * a * d), -1, 1);
  const pv = pole.clone().sub(S); pv.sub(u.clone().multiplyScalar(pv.dot(u))).normalize();
  const E = S.clone().add(u.clone().multiplyScalar(a * cosA)).add(pv.multiplyScalar(a * Math.sqrt(1 - cosA * cosA)));
  aimBone(shld, E);
  aimBone(elb, S.clone().add(u.multiplyScalar(d)));
  if (handQ) {
    wr.parent.getWorldQuaternion(_q).invert();
    wr.quaternion.copy(_q).multiply(handQ);
  } else wr.quaternion.identity();
  wr.updateMatrixWorld(true);
}
// a world orientation for a hand: fingers point along f, palm faces n
export function handQ(f, n) {
  const Y = f.clone().normalize().negate();
  const Z = n.clone().sub(Y.clone().multiplyScalar(n.dot(Y))).normalize();
  const X = new THREE.Vector3().crossVectors(Y, Z);
  return new THREE.Quaternion().setFromRotationMatrix(_m.makeBasis(X, Y, Z));
}
// turn the head toward a world point (yaw, pitch limited)
export function look(P, target, k = 1, lim = [1.1, .6]) {
  P.neck.updateMatrixWorld(true);
  const l = P.neck.worldToLocal(target.clone());
  const yaw = THREE.MathUtils.clamp(Math.atan2(l.x, l.z), -lim[0], lim[0]);
  const pitch = THREE.MathUtils.clamp(-Math.atan2(l.y - .08, Math.hypot(l.x, l.z)), -lim[1], lim[1]);
  P.head.rotation.set(pitch * k, yaw * k, 0);
}

// ---------------------------------------------------------------- the face: eyes with lids, brows, nose, mouth
function face(P, o) {
  const H = P.head, f = {};
  const { skin, dark = 0x1a1210, brow = 0x2a1a12, lip, fem = false } = o;
  const eyeM = mat(0xf2ece2, { roughness: .4 }), pupM = mat(0x16100c, { roughness: .25 });
  const lidM = fem ? mat(0xb88c7c, { roughness: .5, flatShading: false }) : skin;
  const ER = fem ? .0255 : .019, EX = fem ? .043 : .045, EY = fem ? .094 : .095;
  for (const s of [1, -1]) {
    const e = grp(H, s * EX, EY, .118);
    e.add(mesh(new THREE.SphereGeometry(ER, 10, 8).scale(1, fem ? .72 : .8, .5), eyeM));
    const pu = mesh(new THREE.SphereGeometry(ER * .56, 8, 6).scale(1, 1, .5), pupM); pu.position.z = .008; e.add(pu);
    if (fem) { const glint = mesh(new THREE.SphereGeometry(.0028, 5, 4), mat(0xffffff, { emissive: 0xffffff, emissiveIntensity: .6 })); glint.position.set(.004, .004, .0125); e.add(glint); }
    const lid = mesh(new THREE.SphereGeometry(ER + .002, 10, 4, 0, Math.PI * 2, 0, Math.PI / 2).scale(1, .85, .62), lidM);
    lid.position.set(0, .001, .001); e.add(lid);
    let br;
    if (fem) {   // eyeliner along the upper lid with a small wing, and a softly arched brow
      const ink = mat(0x0a0707, { roughness: .35, flatShading: false });
      const liner = mesh(new THREE.TorusGeometry(ER * 1.02, .0028, 5, 16, Math.PI * .95), ink); liner.scale.set(1, .74, 1); liner.rotation.z = Math.PI * .025; liner.position.z = .006; e.add(liner);
      const wing = mesh(rb(.011, .0034, .005, .0015, 1), ink); wing.position.set(s * (ER + .004), .006, .006); wing.rotation.z = s * .55; e.add(wing);
      br = mesh(new THREE.TorusGeometry(.03, .0032, 5, 16, Math.PI * .7), mat(brow, { flatShading: false })); br.scale.set(1, .42, 1);
      br.rotation.z = Math.PI * .15 + (s > 0 ? -.12 : .12); br.position.set(s * .045, .118, .12); H.add(br);
    } else { br = mesh(rb(.05, .014, .016, .005, 1), mat(brow)); br.position.set(s * .045, .13, .122); H.add(br); }
    f["eye" + (s > 0 ? "L" : "R")] = { e, pu, lid, br, s, fem };
  }
  if (fem) {   // a small button nose
    const nose = mesh(rb(.015, .034, .018, .007, 2), skin); nose.position.set(0, .062, .126); nose.rotation.x = -.42; H.add(nose);
    H.add(mesh(new THREE.SphereGeometry(.0105, 10, 8).scale(1.15, .9, 1), skin, 0, .046, .136));
  } else {   // a faceted wedge
    const nose = mesh(rb(.034, .062, .04, .012, 2), skin);
    nose.position.set(0, .064, .135); nose.rotation.x = -.32; H.add(nose);
    H.add(mesh(rb(.046, .018, .03, .008, 1), skin, 0, .036, .14));
  }
  // mouth: two halves that tilt up for a smile (and, for her, a fuller lower lip and a cupid's bow)
  f.mouth = grp(H, 0, fem ? .016 : .005, .125);
  const mm = mat(lip || dark, { roughness: fem ? .3 : .5, flatShading: !fem });
  f.mL = mesh(fem ? new THREE.SphereGeometry(.0095, 10, 8).scale(1.4, .48, .5).translate(.0088, .0, 0) : rb(.03, .0065, .01, .004, 1).translate(.014, 0, 0), mm); f.mouth.add(f.mL);
  f.mR = mesh(fem ? new THREE.SphereGeometry(.0095, 10, 8).scale(1.4, .48, .5).translate(-.0088, .0, 0) : rb(.03, .0065, .01, .004, 1).translate(-.014, 0, 0), mm); f.mouth.add(f.mR);
  if (fem) {
    f.lower = mesh(new THREE.SphereGeometry(.0155, 12, 8).scale(1.1, .42, .42), mm); f.lower.position.set(0, -.0068, .0); f.mouth.add(f.lower);
    H.add(mesh(new THREE.SphereGeometry(.0028, 5, 4), mat(0x1a0e0c), .038, .032, .124));   // a beauty mark
  }
  // ears
  for (const s of [1, -1]) { const ear = mesh(new THREE.SphereGeometry(.026, 6, 5).scale(.45, 1, .8), skin); ear.position.set(s * .132, .07, .0); H.add(ear); }
  return f;
}
// expression: blink 0..1, brow -1 (furrow) .. 1 (raised), smile 0..1, gaze [x, y] in -1..1
export function express(P, { blink = 0, brow = 0, smile = 0, gaze = [0, 0] } = {}) {
  const f = P.face;
  for (const k of ["eyeL", "eyeR"]) {
    const e = f[k];
    e.lid.rotation.x = (e.fem ? -1.55 : -1.2) + Math.max(blink, P.squint || 0) * (e.fem ? 3.1 : 2.75);   // the lid comes down over the eye
    e.pu.position.x = gaze[0] * .006; e.pu.position.y = gaze[1] * .005;
    if (e.fem) { e.br.position.y = .118 + brow * .006; continue; }
    e.br.position.y = .13 + brow * .008;
    e.br.rotation.z = e.s * (brow < 0 ? brow * .35 : brow * .1);
  }
  const bow = 0;
  f.mL.rotation.z = bow + smile * (f.lower ? .22 : .32); f.mR.rotation.z = -bow - smile * (f.lower ? .22 : .32);
  f.mouth.position.y = (f.lower ? .016 : .005) + smile * .002;
  if (f.lower) f.lower.scale.set(1 + smile * .15, 1, 1);
}

// ---------------------------------------------------------------- the detective
export function detective() {
  const skin = mat(0xb07a5c, { roughness: .7 }), coat = mat(0x5e5850, { roughness: .85 }), coat2 = mat(0x48433d, { roughness: .85 }), shirt = mat(0xd8d2c4), pants = mat(0x26252a), shoe = mat(0x1c1512, { roughness: .45 });
  const P = rig({ skin, coat, coat2, shirt, pants, shoe, hipH: .5, sh: .2, handSize: 1.05 });
  P.skin = skin;
  // torso: the trench coat, double-breasted, a belt, an up-turned collar; a white shirt and a loosened tie
  const torso = mesh(new THREE.CylinderGeometry(.2, .17, .52, 8).translate(0, .26, 0), coat); torso.scale.set(1, 1, .72); P.spine.add(torso);
  P.spine.add(mesh(new THREE.CylinderGeometry(.182, .182, .045, 8).translate(0, .06, 0), coat2)).children.at(-1).scale.set(1, 1, .74);
  P.spine.add(mesh(rb(.05, .04, .02, .005, 1), mat(0x9c8a60, { metalness: .6, roughness: .35 }), 0, .06, .134));
  const vee = mesh(new THREE.ConeGeometry(.085, .3, 3).rotateZ(Math.PI).translate(0, .36, 0), shirt); vee.scale.set(1, 1, .3); vee.position.z = .118; P.spine.add(vee);
  const tie = mesh(new THREE.ConeGeometry(.032, .26, 4).rotateZ(Math.PI).translate(0, .37, 0), mat(0x6e1c20)); tie.scale.set(1, 1, .25); tie.position.z = .128; tie.rotation.z = .05; P.spine.add(tie);
  P.spine.add(mesh(rb(.04, .03, .02, .006, 1), mat(0x6e1c20), .002, .5, .122));
  for (const s of [1, -1]) {
    const lap = mesh(new THREE.BoxGeometry(.1, .3, .025).translate(0, -.15, 0), coat2); lap.position.set(s * .07, .52, .12); lap.rotation.set(-.12, s * .25, s * -.28); P.spine.add(lap);
    const col = mesh(new THREE.BoxGeometry(.12, .13, .03), coat); col.position.set(s * .1, .55, .02); col.rotation.set(.1, s * .9, s * .2); P.spine.add(col);
    for (const y of [.18, .3]) P.spine.add(mesh(new THREE.CylinderGeometry(.011, .011, .01, 6).rotateX(Math.PI / 2), mat(0x3a2c1c), s * .06, y, .14));
  }
  // shoulders padding, a skirt of coat over the lap
  P.chest.add(mesh(new THREE.SphereGeometry(.2, 8, 4, 0, Math.PI * 2, 0, Math.PI / 2).scale(1.08, .32, .74), coat, 0, .19, 0));
  P.skirt = mesh(new THREE.CylinderGeometry(.19, .23, .3, 8, 1, true).translate(0, -.15, 0), coat); P.skirt.material.side = THREE.DoubleSide; P.skirt.scale.set(1, 1, .8); P.hips.add(P.skirt);
  P.neck.add(mesh(new THREE.CylinderGeometry(.055, .06, .08, 7), skin, 0, .02, 0));
  // head: a square jaw, stubble, sideburns under the hat
  P.head.add(mesh(new THREE.IcosahedronGeometry(.135, 1).scale(1, 1.18, 1.02).translate(0, .09, 0), skin));
  const jaw = mesh(rb(.2, .1, .19, .04, 2).translate(0, .02, .015), skin); P.head.add(jaw);
  const stub = mesh(rb(.202, .05, .188, .03, 2).translate(0, .0, .018), mat(0x4a3428, { transparent: true, opacity: .3 })); stub.castShadow = false; P.head.add(stub);
  P.head.add(mesh(new THREE.IcosahedronGeometry(.138, 1).scale(1.02, .6, 1.03).translate(0, .16, -.02), mat(0x221812, { roughness: .6 })));
  for (const s of [1, -1]) P.head.add(mesh(rb(.014, .05, .035, .006, 1), mat(0x221812), s * .128, .11, -.01));
  P.face = face(P, { skin, brow: 0x1e140e });
  // the fedora: a pinched crown, a band, a brim that dips at the front
  P.hat = grp(P.head, 0, .205, -.005); P.hat.rotation.x = .12;
  const felt = mat(0x2c2a2e, { roughness: .9 });
  // the brim: a shallow cone, so it rolls down at the front and back
  const brim = mesh(new THREE.CylinderGeometry(.16, .24, .03, 16, 1, true), felt); brim.material = felt.clone(); brim.material.side = THREE.DoubleSide; brim.scale.set(1, 1, 1.12); brim.position.y = -.01; P.hat.add(brim);
  const crown = mesh(new THREE.CylinderGeometry(.12, .148, .12, 10).translate(0, .06, 0), felt); crown.scale.set(1, 1, 1.14); P.hat.add(crown);
  const dent = mesh(new THREE.CylinderGeometry(.05, .1, .028, 10).translate(0, .118, 0), mat(0x1e1c20)); dent.scale.set(.6, 1, 1.15); P.hat.add(dent);
  for (const s of [1, -1]) { const pinch = mesh(new THREE.BoxGeometry(.03, .07, .05), felt); pinch.position.set(s * .07, .075, .13); pinch.rotation.set(-.3, s * .5, 0); P.hat.add(pinch); }
  const band = mesh(new THREE.CylinderGeometry(.15, .15, .026, 10).translate(0, .016, 0), mat(0x111014)); band.scale.set(1, 1, 1.15); P.hat.add(band);
  // seated: thighs forward, shins down
  for (const k of ["L", "R"]) { P["thigh" + k].rotation.x = -1.5; P["knee" + k].rotation.x = 1.45; }
  P.root.rotation.order = "YXZ";
  P.squint = .42;
  return P;
}

// ---------------------------------------------------------------- the client
export function client() {
  const skin = mat(0xd8a890, { roughness: .55, flatShading: false }), coat = mat(0xa8222c, { roughness: .6 }), coat2 = mat(0x7e1820, { roughness: .6 }), glove = mat(0x18141a, { roughness: .45 });
  const pants = mat(0x1d1a20), shoe = mat(0x120e10, { roughness: .3 });
  const P = rig({ skin: glove, coat, coat2, pants, shoe, hipH: .92, sh: .16, handSize: .9 });
  P.skin = skin;
  const torso = mesh(new THREE.CylinderGeometry(.165, .14, .5, 8).translate(0, .25, 0), coat); torso.scale.set(1, 1, .7); P.spine.add(torso);
  P.spine.add(mesh(new THREE.CylinderGeometry(.15, .15, .05, 8).translate(0, .05, 0), mat(0x1a1416, { roughness: .4 }))).children.at(-1).scale.set(1, 1, .74);
  P.spine.add(mesh(rb(.045, .035, .02, .005, 1), mat(0xc8a860, { metalness: .7, roughness: .3 }), 0, .05, .112));
  for (const s of [1, -1]) {
    const lap = mesh(new THREE.BoxGeometry(.09, .26, .022).translate(0, -.13, 0), coat2); lap.position.set(s * .06, .49, .1); lap.rotation.set(-.12, s * .25, s * -.3); P.spine.add(lap);
  }
  P.chest.add(mesh(new THREE.SphereGeometry(.17, 8, 5, 0, Math.PI * 2, 0, Math.PI / 2).scale(1.02, .42, .72), coat, 0, .2, 0));
  // the coat flares to the knee
  P.skirt = mesh(new THREE.CylinderGeometry(.16, .26, .55, 9, 1, true).translate(0, -.27, 0), coat); P.skirt.material = coat.clone(); P.skirt.material.side = THREE.DoubleSide; P.skirt.scale.set(1, 1, .82); P.hips.add(P.skirt);
  P.neck.add(mesh(new THREE.CylinderGeometry(.038, .043, .1, 10), skin, 0, .02, 0));
  P.head.add(mesh(new THREE.IcosahedronGeometry(.118, 3).scale(.9, 1.17, 1.0).translate(0, .095, 0), skin));
  const chin = mesh(new THREE.SphereGeometry(.07, 14, 10).scale(1.15, .9, 1.05), skin); chin.position.set(0, .03, .03); P.head.add(chin);
  P.face = face(P, { skin, brow: 0x1e0e0a, lip: 0x9a1a26, fem: true });
  // hair: dark, pinned back off the face, side-parted 1940s waves to the shoulders
  const hair = mat(0x2a1410, { roughness: .45, flatShading: false });
  const cap = mesh(new THREE.SphereGeometry(.132, 18, 12, 0, Math.PI * 2, 0, 1.3), hair); cap.position.set(0, .115, -.012); cap.rotation.x = -.42; cap.scale.set(1.04, 1.06, 1.06); P.head.add(cap);
  const wave = mesh(new THREE.SphereGeometry(.06, 14, 10).scale(1.45, .5, .85), hair); wave.position.set(.05, .222, .015); wave.rotation.set(.25, .25, -.3); P.head.add(wave);
  for (const s of [1, -1]) {
    const side = mesh(new THREE.SphereGeometry(.062, 14, 10).scale(.62, 1.25, 1.05), hair); side.position.set(s * .118, .07, -.04); P.head.add(side);
    const fall = mesh(new THREE.SphereGeometry(.06, 14, 10).scale(.7, 1.3, 1.1), hair); fall.position.set(s * .105, -.02, -.055); P.head.add(fall);
  }
  P.head.add(mesh(new THREE.SphereGeometry(.105, 16, 10).scale(1.12, 1.05, .85), hair, 0, .03, -.075));
  // a victory roll at the nape: one smooth curl round the back of the neck
  const roll = mesh(new THREE.TorusGeometry(.1, .036, 10, 24, Math.PI * 1.15), hair); roll.position.set(0, -.045, -.035); roll.rotation.set(Math.PI / 2 + .25, 0, Math.PI * .92); P.head.add(roll);
  for (const s of [1, -1]) P.head.add(mesh(new THREE.SphereGeometry(.009, 10, 8), mat(0xf4efe4, { roughness: .15, flatShading: false }), s * .118, .025, .025));
  // a wide-brimmed hat, tilted back and to the side so it frames her face
  P.hat = grp(P.head, .035, .245, -.035); P.hat.rotation.set(-.22, 0, -.26);
  const hm = mat(0x1b1518, { roughness: .8 });
  P.hat.add(mesh(new THREE.CylinderGeometry(.24, .24, .01, 18), hm));
  P.hat.add(mesh(new THREE.CylinderGeometry(.11, .13, .085, 12).translate(0, .045, 0), hm));
  P.hat.add(mesh(new THREE.CylinderGeometry(.132, .132, .02, 12).translate(0, .015, 0), coat2));
  for (const k of ["L", "R"]) { P["thigh" + k].rotation.x = 0; P["knee" + k].rotation.x = 0; }
  P.root.rotation.order = "YXZ";
  return P;
}
