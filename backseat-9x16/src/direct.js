// Direction toolkit: camera, lighting presets, poses. Every function is pure in (state, time).
import * as THREE from "three";
import { BED, CLOSET, HX } from "./world.js";
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
    const g = pipe.grade.uniforms;
    pipe.bloom.strength = 0.4;
    const P = W.props;
    // night base: cold moonlight through the window, nightlight + red clock as practicals
    hemi.color.set("#4a5a8c");
    hemi.groundColor.set("#1a1410");
    hemi.intensity = 1.0;
    key.color.set("#9db4ff");
    key.intensity = 3.3;
    key.position.set(11, 22, -34);
    key.target.position.set(-3, 0, -2);
    glows[0].color.set("#ffa24a");
    glows[0].intensity = 22;
    glows[0].position.set(11.4, 1.3, -1.5);
    glows[1].color.set("#ff3020");
    glows[1].intensity = 3.5;
    glows[1].position.set(-1.0, 3.3, -7.9);
    P.sky.night.material.opacity = 1;
    P.sky.dawn.material.opacity = 0;
    P.starMat.emissiveIntensity = 1.6;
    renderer.toneMappingExposure = 1.55;
    g.uGain.value.set(0.94, 0.98, 1.08);
    g.uLift.value.set(0.0, 0.005, 0.02);
    g.uSat.value = 0.86;
    g.uVignette.value = 0.58;
    if (name === "dawn") {
      const s = smooth(k);
      hemi.color.lerpColors(new THREE.Color("#4a5a8c"), new THREE.Color("#ffd2a8"), s);
      hemi.intensity = lerp(1.0, 1.9, s);
      key.color.lerpColors(new THREE.Color("#9db4ff"), new THREE.Color("#ffb46a"), s);
      key.intensity = lerp(3.3, 6.5, s);
      key.position.set(lerp(11, 14, s), lerp(22, 10, s), -34);
      P.sky.night.material.opacity = 1 - s;
      P.sky.dawn.material.opacity = s;
      P.starMat.emissiveIntensity = lerp(1.6, 0.2, s);
      glows[0].intensity = lerp(22, 6, s);
      renderer.toneMappingExposure = lerp(1.55, 1.05, s);
      g.uGain.value.set(lerp(0.94, 1.05, s), lerp(0.98, 1.0, s), lerp(1.08, 0.93, s));
      g.uSat.value = lerp(0.86, 1.08, s);
      g.uVignette.value = lerp(0.58, 0.38, s);
      pipe.bloom.strength = lerp(0.4, 0.55, s);
    }
    if (name === "hospital") {
      hemi.color.set("#d6efe6");
      hemi.groundColor.set("#55625e");
      hemi.intensity = 1.55;
      key.color.set("#eefff7");
      key.intensity = 2.6;
      key.position.set(HX + 7, 30, 18);
      key.target.position.set(HX, 0, 0);
      glows[0].color.set("#7fd3ff");
      glows[0].intensity = 7;
      glows[0].position.set(HX + 2.2, 4.4, 0.9);
      glows[1].intensity = 0;
      renderer.toneMappingExposure = 0.98;
      g.uGain.value.set(0.97, 1.02, 0.99);
      g.uLift.value.set(0.0, 0.008, 0.008);
      g.uSat.value = 0.8;
      g.uVignette.value = 0.5;
      pipe.bloom.strength = 0.32;
    }
    if (name === "bath") {
      const s = smooth(k);
      hemi.color.lerpColors(new THREE.Color("#3a4a78"), new THREE.Color("#fff1dc"), s);
      hemi.groundColor.set("#2a2420");
      hemi.intensity = lerp(0.6, 1.2, s);
      key.color.lerpColors(new THREE.Color("#8fa6ff"), new THREE.Color("#fff0d8"), s);
      key.intensity = lerp(0.9, 2.3, s);
      key.position.set(HX + 8, 28, 22);
      key.target.position.set(HX, 0, -2);
      glows[0].color.lerpColors(new THREE.Color("#9fb8ff"), new THREE.Color("#ffd9a8"), s);
      glows[0].intensity = lerp(7, 24, s);
      glows[0].position.set(HX + 0.6, 8.0, -4.6);
      glows[1].intensity = 0;
      P.bathWindow.material.emissive.lerpColors(new THREE.Color("#9fb8ff"), new THREE.Color("#fff2d6"), s);
      P.bathWindow.material.emissiveIntensity = lerp(0.5, 2.4, s);
      renderer.toneMappingExposure = lerp(1.2, 0.82, s);
      g.uGain.value.set(lerp(0.94, 1.04, s), lerp(0.98, 1.0, s), lerp(1.08, 0.95, s));
      g.uSat.value = lerp(0.8, 1.0, s);
      g.uVignette.value = lerp(0.6, 0.42, s);
    }
    // the night road: moon, the car's headlight pool, dash glow; o.beam = truck high beams (0..1, at o.truck pos)
    if (name === "road") {
      hemi.color.set("#25304f");
      hemi.groundColor.set("#0c0c0a");
      hemi.intensity = 0.5;
      key.color.set("#8fa6e6");
      key.intensity = 0.9;
      const cp = o.at || [0, 0, 0];
      key.position.set(cp[0] - 40, 60, cp[2] - 40);
      key.target.position.set(cp[0], 0, cp[2]);
      glows[0].color.set("#fff2d6");
      glows[0].decay = 2;
      glows[0].distance = 0;
      glows[0].position.set(cp[0], 2.6, cp[2] - 13);
      glows[0].intensity = o.headlights === 0 ? 0 : 160;
      glows[1].color.set("#5ad1c8");
      glows[1].decay = 2;
      glows[1].distance = 4;
      glows[1].position.set(cp[0] - 1.45, 3.6, cp[2] - 1.4);
      glows[1].intensity = 4.5;
      if (o.truck) {
        const tp = o.truck, aim = o.aim || [cp[0] - 0.8, 4.2, cp[2]];
        const beam = o.beam ?? 0;
        prac.color.set("#fff6e2");
        prac.angle = lerp(0.42, 0.62, beam);
        prac.penumbra = 0.5;
        prac.decay = 2;
        prac.position.set(tp[0], 3.0, tp[2] - 6.8);
        prac.target.position.set(aim[0], aim[1], aim[2]);
        prac.intensity = lerp(220, 2800, beam);
        glows[2].color.set("#fff6e2");
        glows[2].decay = 2;
        glows[2].distance = 0;
        glows[2].position.set(tp[0], 2.8, tp[2] - 9);
        glows[2].intensity = lerp(25, 120, beam);
        P.truck.lamp(o.lamps ?? lerp(1.0, 2.0, beam));
        pipe.bloom.strength = lerp(0.55, 0.3, beam);
      }
      if (o.porch) {
        glows[3].color.set("#ffc27a");
        glows[3].decay = 2;
        glows[3].distance = 0;
        glows[3].position.set(P.porch[0], P.porch[1], P.porch[2]);
        glows[3].intensity = 120;
      }
      renderer.toneMappingExposure = 1.35;
      g.uGain.value.set(0.96, 0.98, 1.06);
      if (!o.truck) pipe.bloom.strength = 0.55;
      g.uLift.value.set(0.0, 0.004, 0.018);
      g.uSat.value = o.flash ? 0.45 : 0.86;
      g.uVignette.value = 0.6;
    }
    // the house at night: lamp by the couch, TV flicker, moon through the window, nightlight upstairs
    if (name === "house") {
      const tt = o.t ?? 0;
      hemi.color.set("#2e3656");
      hemi.groundColor.set("#140f0c");
      hemi.intensity = 0.55;
      key.color.set("#8fa2e0");
      key.intensity = 0.5;
      key.position.set(HX + 10, 30, 26);
      key.target.position.set(HX - 2, 0, -2);
      const lamp = o.lamp ?? 1;
      prac.color.set("#ffc27a");
      prac.angle = 1.35;
      prac.penumbra = 0.9;
      prac.decay = 2;
      prac.position.set(P.lampPos[0], P.lampPos[1] + 0.3, P.lampPos[2]);
      prac.target.position.set(P.lampPos[0] + 1, 0, P.lampPos[2] - 5);
      prac.intensity = 120 * lamp;
      P.lampShade.emissiveIntensity = 0.9 * lamp;
      const fl = 0.75 + 0.25 * Math.sin(tt * 11.0) * Math.sin(tt * 3.7 + 1.0);
      glows[0].color.set("#9fb4ff");
      glows[0].decay = 2;
      glows[0].distance = 0;
      glows[0].position.set(P.window[0], P.window[1], P.window[2]);
      glows[0].intensity = 18;
      glows[1].color.set("#7aa8ff");
      glows[1].decay = 2;
      glows[1].distance = 0;
      glows[1].position.set(P.tvPos[0], P.tvPos[1], P.tvPos[2]);
      glows[1].intensity = 30 * fl * (o.tv ?? 1);
      P.tvM.color.setRGB(0.48 * fl, 0.66 * fl, 1.0 * fl);
      glows[2].color.set("#ffb45a");
      glows[2].decay = 2;
      glows[2].distance = 0;
      glows[2].position.set(P.nightlight[0], P.nightlight[1], P.nightlight[2]);
      glows[2].intensity = 40 * (o.night ?? 1);
      renderer.toneMappingExposure = 1.45;
      g.uGain.value.set(0.98, 0.98, 1.04);
      g.uLift.value.set(0.0, 0.004, 0.015);
      g.uSat.value = 0.86;
      g.uVignette.value = 0.6;
      pipe.bloom.strength = 0.45;
    }
    // the sleepover bathroom: o.room (ceiling light 0..1), o.candle (0..1, flickers with o.t), o.hall (hallway light)
    if (name === "mary") {
      hemi.color.set("#2c2c48");
      hemi.groundColor.set("#120c0a");
      hemi.intensity = 0.38;
      key.color.set("#8090c0");
      key.intensity = 0.25;
      key.position.set(HX + 4, 26, 30);
      key.target.position.set(HX - 4, 0, 0);
      glows[1].intensity = 0;
      const room = o.room ?? 0, cand = o.candle ?? 0, tt = o.t ?? 0;
      glows[0].color.set("#fff1d8");
      glows[0].decay = 2;
      glows[0].distance = 0;
      glows[0].position.set(HX - 1.5, 10.2, 0.5);
      glows[0].intensity = 70 * room;
      glows[1].color.set("#fff1d8");
      glows[1].decay = 2;
      glows[1].distance = 0;
      glows[1].position.set(HX - 1.5, 10.2, 2 * ZM - 0.5);
      glows[1].intensity = 70 * room;
      const fl = 0.82 + 0.1 * Math.sin(tt * 23.0) * Math.sin(tt * 7.3 + 1.0) + 0.08 * Math.sin(tt * 41.0 + 2.0);
      const cp = P.candle;
      glows[2].color.set("#ffb45a");
      glows[2].decay = 2;
      glows[2].distance = 0;
      glows[2].position.set(cp[0], cp[1] + 0.15, cp[2] + 0.1);
      glows[2].intensity = 7.5 * cand * fl;
      glows[3].color.set("#ffb45a");
      glows[3].decay = 2;
      glows[3].distance = 0;
      glows[3].position.set(cp[0], cp[1] + 0.15, 2 * ZM - (cp[2] + 0.1));
      glows[3].intensity = 7.5 * cand * fl;
      P.flame.visible = P.reflectFlame.visible = cand > 0.02;
      P.flame.scale.set(0.9, 2.2 * (0.85 + 0.25 * fl), 0.9);
      P.reflectFlame.scale.copy(P.flame.scale);
      P.flame.material.color.setRGB(3.2 * fl, 2.6 * fl, 1.5 * fl);
      if (o.hall) {
        prac.color.set("#ffd9a0");
        prac.angle = 1.25;
        prac.penumbra = 0.8;
        prac.decay = 2;
        prac.position.set(HX - 5.25, 10.6, 12.2);
        prac.target.position.set(HX - 5.25, 0, 11.0);
        prac.intensity = 170 * o.hall;
        hemi.intensity += 0.5 * o.hall;
        hemi.color.lerp(new THREE.Color("#7a6248"), o.hall * 0.6);
      }
      renderer.toneMappingExposure = 1.5;
      g.uGain.value.set(1.02, 0.97, 0.96);
      g.uLift.value.set(0.01, 0.0, 0.01);
      g.uSat.value = 0.88;
      g.uVignette.value = 0.62;
      pipe.bloom.strength = 0.55;
    }
    // the bedside lamp on (warm evening), k 0..1
    if (o.lamp) {
      const k2 = o.lamp;
      prac.color.set("#ffc27a");
      prac.angle = 1.3;
      prac.penumbra = 0.9;
      prac.decay = 2;
      prac.position.set(-0.6, 4.4, -8.6);
      prac.target.position.set(-4, 0, -3);
      prac.intensity = 150 * k2;
      glows[2].color.set("#ffb46a");
      glows[2].decay = 2;
      glows[2].distance = 0;
      glows[2].position.set(-0.6, 4.3, -8.4);
      glows[2].intensity = 22 * k2;
      P.lamp.shadeM.emissiveIntensity = 1.4 * k2;
      hemi.color.lerp(new THREE.Color("#8a6a50"), 0.5 * k2);
      hemi.intensity += 0.4 * k2;
      renderer.toneMappingExposure = lerp(renderer.toneMappingExposure, 1.25, k2);
      g.uSat.value = lerp(g.uSat.value, 1.0, k2);
    }
    // light leaking from the closet (the phone inside); k 0..1
    if (o.closet) {
      const k = o.closet;
      prac.color.set("#cfdcff");
      prac.angle = 0.95;
      prac.penumbra = 0.55;
      prac.decay = 2;
      const src = o.closetAt || [CLOSET.inX - 1.0, 4.2, CLOSET.zc - 0.3];
      prac.position.set(src[0], src[1], src[2]);
      prac.target.position.set(4, 0, 2.2);
      prac.intensity = 260 * k;
      glows[2].color.set("#bcd2ff");
      glows[2].decay = 2;
      glows[2].distance = 7;
      glows[2].position.set(src[0] + 0.4, src[1] + 1.2, src[2]);
      glows[2].intensity = 9 * k;
    }
    // local cold glow from a phone screen: [x, y, z, intensity, distance]
    if (o.phone) {
      glows[3].decay = 2;
      glows[3].distance = o.phone[4] ?? 6;
      glows[3].color.set(o.phoneColor || "#b9cdff");
      glows[3].position.set(o.phone[0], o.phone[1], o.phone[2]);
      glows[3].intensity = o.phone[3] ?? 6;
    }
    if (o.clockGlow !== undefined) glows[1].intensity *= o.clockGlow;
    if (o.dark) {
      hemi.intensity *= 0.6;
      key.intensity *= 0.7;
    }
    if (o.fill) {
      glows[3].decay = 0;
      glows[3].distance = 22;
      glows[3].color.set(o.fillColor || "#b8c8ff");
      glows[3].position.set(o.fill[0], o.fill[1], o.fill[2]);
      glows[3].intensity = (o.fill[3] ?? 120) / 50;
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
  // put a free object at a parent's local offset/rotation (scale ignored)
  const _m = new THREE.Matrix4(), _m2 = new THREE.Matrix4(), _qq = new THREE.Quaternion(), _e = new THREE.Euler(), _one = new THREE.Vector3(1, 1, 1), _pp = new THREE.Vector3();
  function attach(obj, parent, off = [0, 0, 0], rot = [0, 0, 0]) {
    parent.updateWorldMatrix(true, false);
    _e.set(rot[0], rot[1], rot[2]);
    _qq.setFromEuler(_e);
    _pp.set(off[0], off[1], off[2]);
    _m.compose(_pp, _qq, _one);
    _m2.multiplyMatrices(parent.matrixWorld, _m);
    _m2.decompose(obj.position, obj.quaternion, obj.scale);
    obj.scale.set(1, 1, 1);
  }
  // a phone in an avatar's hand, screen turned to `at` (default: its own eyes)
  function holdPhone(av, ph, { side = "R", off = [0, -0.2, 0.3], at = null, state = null, buzz = 0, t = 0 } = {}) {
    const p = wpos(av.j[side === "R" ? "handR" : "handL"], off);
    ph.group.visible = true;
    ph.group.position.set(p[0] + Math.sin(t * 90) * 0.02 * buzz, p[1], p[2] + Math.cos(t * 77) * 0.02 * buzz);
    const h = at || wpos(av.j.head, [0, 0.62, 0.4]);
    ph.group.lookAt(h[0], h[1], h[2]);
    if (buzz) ph.group.rotateZ(Math.sin(t * 83) * 0.05 * buzz);
    if (state) ph.draw(state);
    return p;
  }
  // camera square to a phone screen: dist along its normal, look offset `ly` along its up (negative lifts it in frame)
  const _n = new THREE.Vector3(), _up = new THREE.Vector3(), _rt = new THREE.Vector3();
  function phoneCam(ph, o, u, d) {
    const e = (o.e || ease.inOut)(clamp(u / d));
    ph.group.updateWorldMatrix(true, false);
    _n.set(0, 0, 1).applyQuaternion(ph.group.quaternion);
    _up.set(0, 1, 0).applyQuaternion(ph.group.quaternion);
    _rt.set(1, 0, 0).applyQuaternion(ph.group.quaternion);
    const c = ph.group.position;
    const dist = Array.isArray(o.dist) ? lerp(o.dist[0], o.dist[1], e) : o.dist ?? 4.3;
    const ox = o.ox || 0, oy = o.oy || 0, ly = o.ly ?? -0.42;
    const p = [c.x + _n.x * dist + _rt.x * ox + _up.x * oy, c.y + _n.y * dist + _rt.y * ox + _up.y * oy, c.z + _n.z * dist + _rt.z * ox + _up.z * oy];
    const l = [c.x + _up.x * ly, c.y + _up.y * ly, c.z + _up.z * ly];
    cam({ p, l, up: [_up.x, _up.y, _up.z], f: o.f || [c.x, c.y, c.z], fov: o.fov || 30, ap: o.ap ?? 6, shake: o.shake ?? 0.006, seed: o.seed || 1, roll: o.roll }, u, d);
  }
  // face an avatar toward a point (y ignored)
  function faceTo(c, x, z) {
    c.root.rotation.y = Math.atan2(x - c.root.position.x, z - c.root.position.z);
  }

  return { attach, holdPhone, phoneCam, wpos, aimHand, pointAt, dogRun, dogSit, faceTo, cam, lights, sky, place, walk, idle, sit, grandpaInChair, zzz, snoreFace, counterStand, point, counterCrouch, riceAt, riceDone, dustSet };
}
