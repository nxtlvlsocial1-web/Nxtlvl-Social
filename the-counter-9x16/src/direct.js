// Direction toolkit: camera, lighting presets, poses. Every function is pure in (state, time).
import * as THREE from "three";
import { EXT, WED, INS } from "./world.js";
import { clamp, lerp, lerp3, ease, wobble, smooth, DEG } from "./util.js";

const _v = new THREE.Vector3(), _f = new THREE.Vector3(), _l = new THREE.Vector3();

export function makeDirector(ctx) {
  const { camera, W, C, pipe, renderer } = ctx;
  const L = W.lights;

  // cam({ p:[from,to], l:[from,to], fov, f:[from,to] focus points, ap, e, shake, roll }, u, d)
  function cam(o, u, d) {
    const e = (o.e || ease.inOut)(clamp(u / d));
    const p = o.p.length === 2 && Array.isArray(o.p[0]) ? lerp3(o.p[0], o.p[1], e) : o.p;
    const l = o.l.length === 2 && Array.isArray(o.l[0]) ? lerp3(o.l[0], o.l[1], e) : o.l;
    const sh = o.shake ?? 0.04;
    const wb = wobble(u + (o.seed || 0) * 3.1, o.seed || 1, sh);
    camera.position.set(p[0] + wb[0], p[1] + wb[1], p[2] + wb[2] * 0.5);
    _l.set(l[0] + wb[0] * 0.6, l[1] + wb[1] * 0.6, l[2]);
    if (o.up) camera.up.set(o.up[0], o.up[1], o.up[2]);
    camera.lookAt(_l);
    if (o.roll) camera.rotateZ(o.roll * DEG);
    camera.fov = Array.isArray(o.fov) ? lerp(o.fov[0], o.fov[1], e) : o.fov || 35;
    // focus distance measured along the view axis to the focus point
    let fp = o.f ? (o.f.length === 2 && Array.isArray(o.f[0]) ? lerp3(o.f[0], o.f[1], (o.fe || ease.inOut)(clamp(u / d))) : o.f) : l;
    camera.getWorldDirection(_f);
    _v.set(fp[0], fp[1], fp[2]).sub(camera.position);
    pipe.scenePass.focus = Math.max(0.2, _v.dot(_f));
    pipe.scenePass.aperture = o.ap ?? 10;
  }

  function sky(night, dawn, day) {
    W.props.sky.night.material.opacity = night;
    W.props.sky.dawn.material.opacity = dawn;
    W.props.sky.day.material.opacity = day;
  }

  function lights(name, k = 0, o = {}) {
    const { hemi, key, prac, glows } = L;
    glows.forEach((g) => (g.intensity = 0));
    prac.intensity = 0;
    renderer.toneMappingExposure = 1;
    const g = pipe.grade.uniforms;
    g.uLift.value.set(0, 0, 0);
    g.uGain.value.set(1, 1, 1);
    g.uSat.value = 1.05;
    g.uVignette.value = 0.4;
    pipe.bloom.strength = 0.35;
    const lampOn = o.lamp ?? 1;
    const lampP = W.props.lamp.pos;
    if (name === "night" || name === "dawn" || name === "day") {
      // night base
      hemi.color.set("#9aa6d6");
      hemi.groundColor.set("#6b4630");
      hemi.intensity = 1.5;
      key.color.set("#8ea6ff");
      key.intensity = 2.4;
      key.position.set(-8, 34, -52);
      key.target.position.set(6, 0, -2);
      prac.color.set("#ffb062");
      prac.intensity = 900 * lampOn;
      prac.angle = 1.25;
      prac.penumbra = 0.9;
      prac.position.set(lampP.x - 0.2, lampP.y - 0.3, lampP.z + 0.2);
      prac.target.position.set(8, 0, -2);
      glows[0].color.set("#ffa45a");
      glows[0].intensity = 220 * lampOn;
      glows[0].position.set(lampP.x, lampP.y + 0.4, lampP.z);
      // faint warm bounce from the hall side so the door corner isn't black
      glows[1].color.set("#c9935e");
      glows[1].intensity = 160;
      glows[1].position.set(-12, 9, 2);
      W.props.lamp.shadeMat.emissiveIntensity = 1.5 * lampOn;
      W.props.lamp.bulb.material.emissiveIntensity = 7 * lampOn;
      g.uGain.value.set(1.02, 0.99, 0.96);
      sky(1, 0, 0);
      renderer.toneMappingExposure = 1.25;
      if (name === "dawn") {
        // k: 0 = night .. 1 = full sunrise through the window
        const s = smooth(k);
        hemi.color.lerpColors(new THREE.Color("#9aa6d6"), new THREE.Color("#ffd0a4"), s);
        hemi.intensity = lerp(1.5, 2.2, s);
        key.color.lerpColors(new THREE.Color("#8ea6ff"), new THREE.Color("#ffb067"), s);
        key.intensity = lerp(2.4, 7.0, s);
        key.position.set(lerp(-8, -2, s), lerp(34, 12, s), -52);
        sky(1 - s, s, 0);
        glows[1].intensity = lerp(160, 60, s);
        renderer.toneMappingExposure = lerp(1.25, 1.1, s);
      } else if (name === "day") {
        hemi.color.set("#dbe7ff");
        hemi.groundColor.set("#6a4a30");
        hemi.intensity = 2.6;
        key.color.set("#fff0d8");
        key.intensity = 6.0;
        key.position.set(-6, 40, -46);
        prac.intensity = 0;
        glows[0].intensity = 0;
        glows[1].intensity = 120;
        renderer.toneMappingExposure = 1.1;
        W.props.lamp.shadeMat.emissiveIntensity = 0.15;
        W.props.lamp.bulb.material.emissiveIntensity = 0.3;
        sky(0, 0, 1);
        g.uSat.value = 1.08;
      }
      if (o.doorSpill) {
        // cold moonlight pouring through the open front door
        glows[2].color.set("#7f97ff");
        glows[2].intensity = 420 * o.doorSpill;
        glows[2].position.set(-24, 7, -6);
      }
    } else if (name === "street") {
      hemi.color.set("#5a6ab0");
      hemi.groundColor.set("#1c1a22");
      hemi.intensity = 1.4;
      key.color.set("#9fb4ff");
      key.intensity = 2.8;
      key.position.set(EXT.x - 70, 26, -40);
      key.target.position.set(EXT.x, 0, 6);
      prac.color.set("#ffc489");
      prac.intensity = 600;
      prac.angle = 1.0;
      prac.position.set(EXT.x + 2.6, 8.6, -8.4);
      prac.target.position.set(EXT.x + 1, 0, -4);
      glows[0].color.set("#ffbf78");
      glows[0].intensity = 1100;
      glows[0].position.set(EXT.x + 16, 15, 4.2);
      glows[1].color.set("#ffc489");
      glows[1].intensity = 260;
      glows[1].position.set(EXT.x - 23.4, 7.6, -8.4);
      glows[2].color.set("#ffc489");
      glows[2].intensity = 260;
      glows[2].position.set(EXT.x + 28.6, 7.6, -8.4);
      renderer.toneMappingExposure = 1.3;
      g.uGain.value.set(0.96, 0.99, 1.06);
    } else if (name === "wedding") {
      hemi.color.set("#ffd9a8");
      hemi.groundColor.set("#3a2418");
      hemi.intensity = 1.7;
      key.color.set("#ffe2b8");
      key.intensity = 3.0;
      key.position.set(WED.x + 20, 30, 20);
      key.target.position.set(WED.x, 0, -4);
      prac.color.set("#ffd8a0");
      prac.intensity = 1100;
      prac.angle = 0.7;
      prac.position.set(WED.x + 2, 16, 4);
      prac.target.position.set(WED.x + 2, 0, -2);
      glows[0].color.set("#ffc27a");
      glows[0].intensity = 700;
      glows[0].position.set(WED.x - 10, 10, -12);
      glows[1].color.set("#ffc27a");
      glows[1].intensity = 700;
      glows[1].position.set(WED.x + 12, 10, -10);
      pipe.bloom.strength = 0.55;
      g.uGain.value.set(1.04, 1.0, 0.94);
    } else if (name === "insert") {
      const at = o.at || INS;
      hemi.color.set("#7d86b0");
      hemi.groundColor.set("#2b1a10");
      hemi.intensity = 1.3;
      key.color.set(o.cool ? "#9fb4ff" : "#ffc58a");
      key.intensity = 2.6;
      key.position.set(at.x - 20, 30, at.z + 20);
      key.target.position.set(at.x, 0, at.z);
      prac.color.set("#ffb062");
      prac.intensity = 520;
      prac.angle = 0.8;
      prac.position.set(at.x + 4, 10, at.z + 3);
      prac.target.position.set(at.x, 0, at.z);
      renderer.toneMappingExposure = 1.0;
    }
    // optional subject key: a soft warm source placed per shot, like a film light just off camera
    if (o.fill) {
      glows[3].color.set(o.fillColor || "#ffd6ad");
      glows[3].position.set(o.fill[0], o.fill[1], o.fill[2]);
      glows[3].decay = 0;
      glows[3].distance = 26;
      glows[3].intensity = (o.fill[3] ?? 160) / 50;
    }
    key.target.updateMatrixWorld();
    prac.target.updateMatrixWorld();
  }

  // ---- poses -------------------------------------------------------------
  function place(c, x, y, z, ry = 0) {
    c.root.visible = true;
    c.root.position.set(x, y, z);
    c.root.rotation.y = ry;
  }
  function walk(a, phase, amp = 0.55) {
    const s = Math.sin(phase);
    a.j.legL.rotation.x = s * amp;
    a.j.legR.rotation.x = -s * amp;
    a.j.armL.rotation.x = -s * amp * 0.8;
    a.j.armR.rotation.x = s * amp * 0.8;
    a.j.pelvis.position.y = 2 + Math.abs(Math.cos(phase)) * 0.12;
  }
  function idle(a, t, k = 1) {
    a.j.torso.rotation.x = Math.sin(t * 1.6) * 0.012 * k;
    a.j.head.rotation.y = Math.sin(t * 0.7) * 0.05 * k;
    a.j.armL.rotation.z = -0.04 - Math.sin(t * 1.6) * 0.01;
    a.j.armR.rotation.z = 0.04 + Math.sin(t * 1.6) * 0.01;
  }
  // classic block sit: legs straight out, pelvis on the seat
  function sit(a, seatY, lean = 0) {
    a.j.pelvis.position.y = seatY + 0.5;
    a.j.legL.rotation.x = a.j.legR.rotation.x = -Math.PI / 2;
    a.j.torso.rotation.x = lean;
    a.j.armL.rotation.x = a.j.armR.rotation.x = -0.35;
  }
  // grandpa in his armchair (world placement of the chair)
  function grandpaInChair(t, { slump = 0.18, head = 0.25 } = {}) {
    const g = C.grandpa;
    const ch = W.props.chair;
    place(g, ch.position.x + Math.sin(ch.rotation.y) * -0.3, 0, ch.position.z + Math.cos(ch.rotation.y) * -0.3, ch.rotation.y + Math.PI);
    sit(g, 2.75, -slump);
    g.j.head.rotation.x = head + Math.sin(t * 1.3) * 0.02;
    g.j.head.rotation.z = 0.12;
    g.j.armL.rotation.x = -0.9;
    g.j.armR.rotation.x = -0.9;
    g.j.armL.rotation.z = 0.25;
    g.j.armR.rotation.z = -0.25;
    return g;
  }
  // floating Z's above a sleeping head
  function zzz(t, at, big = 1) {
    W.props.zs.forEach((z, i) => {
      const ph = (t * 0.55 + i / 3) % 1;
      z.visible = true;
      z.position.set(at[0] + ph * 1.6 + Math.sin(ph * 6 + i) * 0.25, at[1] + ph * 2.6, at[2] + ph * 0.4);
      const s = (0.5 + ph * 0.7) * big;
      z.scale.set(s, s, s);
      z.material.opacity = Math.sin(ph * Math.PI) * 0.95;
    });
  }
  // snore cycle: 0..1 inhale (closed), peak = mouth open
  function snoreFace(g, t, period = 2.2) {
    const ph = (t % period) / period;
    g.setFace(ph > 0.55 && ph < 0.85 ? "snore" : "sleep");
    const st = g.j.headTop.getObjectByName("stache");
    if (st) st.position.y = -0.06 + (ph > 0.55 && ph < 0.85 ? Math.sin((ph - 0.55) * 40) * 0.02 : 0);
    return ph;
  }

  // Counter standing tall, optional hunch & arm pose
  function counterStand(x, z, ry, { hunch = 0.12, neck = 0.25, armF = 0.15 } = {}) {
    const c = C.counter;
    place(c, x, 0, z, ry);
    c.j.torso.rotation.x = hunch;
    c.j.neck.rotation.x = neck;
    c.j.head.rotation.x = 0.1;
    c.j.upperL.rotation.x = c.j.upperR.rotation.x = -armF;
    c.j.foreL.rotation.x = c.j.foreR.rotation.x = -0.1;
    return c;
  }
  // count gesture: index finger pointing, others curled
  function point(c, side = "R", amount = 1) {
    const f = c.j.fingers[side];
    f.forEach((fg, i) => (fg.rotation.x = i === 1 ? -0.1 * amount : 1.6 * amount));
  }
  // bend: fold at the waist, knees bent
  function counterCrouch(c, k) {
    c.j.pelvis.position.y = lerp(6.2, 3.1, k);
    c.j.thighL.rotation.x = c.j.thighR.rotation.x = -1.3 * k;
    c.j.shinL.rotation.x = c.j.shinR.rotation.x = 2.2 * k;
    c.j.torso.rotation.x = lerp(0.1, 0.9, k);
    c.j.neck.rotation.x = lerp(0.2, -0.3, k);
  }

  // ---- rice & dust -------------------------------------------------------
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), e3 = new THREE.Euler(), sc = new THREE.Vector3(1, 1, 1), pv = new THREE.Vector3();
  function riceAt(i, x, y, z, rx, ry, rz, s = 1) {
    e3.set(rx, ry, rz);
    q.setFromEuler(e3);
    pv.set(x, y, z);
    sc.setScalar(s);
    m4.compose(pv, q, sc);
    W.rice.setMatrixAt(i, m4);
  }
  function riceDone(n) {
    W.rice.count = n;
    W.rice.instanceMatrix.needsUpdate = true;
  }
  function dustSet(fn, n) {
    const a = W.dust.geometry.attributes.position;
    for (let i = 0; i < n; i++) {
      const p = fn(i);
      a.setXYZ(i, p[0], p[1], p[2]);
    }
    a.needsUpdate = true;
    W.dust.geometry.setDrawRange(0, n);
    W.dust.visible = true;
  }

  // world position of a joint (+ local offset), after posing
  const _w = new THREE.Vector3();
  function wpos(obj, off = [0, 0, 0]) {
    obj.updateWorldMatrix(true, false);
    _w.set(off[0], off[1], off[2]);
    obj.localToWorld(_w);
    return [_w.x, _w.y, _w.z];
  }
  // detached Counter hand: wrist at `from`, fingers aimed at `to`; curl 0 = open, 1 = pointing
  const _d = new THREE.Vector3(), _down = new THREE.Vector3(0, -1, 0);
  function aimHand(i, from, to, curl = 1, roll = 0) {
    const h = W.props.hands[i];
    h.root.visible = true;
    h.root.position.set(from[0], from[1], from[2]);
    _d.set(to[0] - from[0], to[1] - from[1], to[2] - from[2]).normalize();
    h.root.quaternion.setFromUnitVectors(_down, _d);
    if (roll) h.root.rotateY(roll);
    h.fingers.forEach((f, k) => (f.rotation.x = k === 1 ? 0 : 1.7 * curl));
    return h;
  }
  // tip of the pointing finger is ~1.5 below the wrist along the aim: put the wrist that far back
  function pointAt(i, target, fromDir, dist = 1.6, curl = 1) {
    const n = Math.hypot(...fromDir);
    const f = fromDir.map((v) => v / n);
    return aimHand(i, [target[0] + f[0] * dist, target[1] + f[1] * dist, target[2] + f[2] * dist], target, curl);
  }
  function dogRun(t, speed = 9) {
    const g = C.dog;
    const ph = t * speed;
    g.j.legs.forEach((l, i) => (l.rotation.x = Math.sin(ph + (i < 2 ? 0 : Math.PI) + (i % 2) * 0.6) * 0.9));
    g.j.body.position.y = 1.35 + Math.abs(Math.sin(ph)) * 0.35;
    g.j.body.rotation.x = Math.sin(ph) * 0.08;
    g.j.tail.rotation.y = Math.sin(ph * 1.7) * 0.6;
    g.j.ears.forEach((e, i) => (e.rotation.x = -0.4 - Math.abs(Math.sin(ph)) * 0.5));
  }
  function dogSit(guilty = 0) {
    const g = C.dog;
    g.j.body.rotation.x = -0.5;
    g.j.body.position.y = 1.15;
    g.j.legs[2].rotation.x = g.j.legs[3].rotation.x = -1.1;
    g.j.legs[0].rotation.x = g.j.legs[1].rotation.x = 0.5;
    g.j.head.rotation.x = 0.4 + guilty * 0.35;
    g.j.tail.rotation.x = 0.2;
    g.j.ears.forEach((e, i) => (e.rotation.z = (i ? 1 : -1) * (0.25 + guilty * 0.5)));
  }
  // face an avatar toward a point (y ignored)
  function faceTo(c, x, z) {
    c.root.rotation.y = Math.atan2(x - c.root.position.x, z - c.root.position.z);
  }

  return { wpos, aimHand, pointAt, dogRun, dogSit, faceTo, cam, lights, sky, place, walk, idle, sit, grandpaInChair, zzz, snoreFace, counterStand, point, counterCrouch, riceAt, riceDone, dustSet };
}
