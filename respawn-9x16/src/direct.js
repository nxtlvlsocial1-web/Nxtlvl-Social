// Direction toolkit for Respawn: camera, lighting presets per set, poses. Pure in (state, time).
import * as THREE from "three";
import { ICU, RAIN, SUN } from "./world.js";
import { clamp, lerp, lerp3, ease, wobble, smooth, DEG } from "./util.js";

const _v = new THREE.Vector3(), _f = new THREE.Vector3(), _l = new THREE.Vector3();
const col = (a) => new THREE.Color(a);

export function makeDirector(ctx) {
  const { camera, W, pipe, renderer, scene } = ctx;
  const L = W.lights;
  const P = W.props;

  // cam({ p:[from,to], l:[from,to], fov, f focus, ap, e, shake, roll }, u, d)
  function cam(o, u, d) {
    const e = (o.e || ease.inOut)(clamp(u / d));
    const p = o.p.length === 2 && Array.isArray(o.p[0]) ? lerp3(o.p[0], o.p[1], e) : o.p;
    const l = o.l.length === 2 && Array.isArray(o.l[0]) ? lerp3(o.l[0], o.l[1], e) : o.l;
    const sh = o.shake ?? 0.04;
    const wb = wobble((ctx.now ?? u) + (o.seed || 0) * 3.1, o.seed || 1, sh);
    camera.position.set(p[0] + wb[0], p[1] + wb[1], p[2] + wb[2] * 0.5);
    _l.set(l[0] + wb[0] * 0.6, l[1] + wb[1] * 0.6, l[2]);
    if (o.up) camera.up.set(o.up[0], o.up[1], o.up[2]);
    else camera.up.set(0, 1, 0);
    camera.lookAt(_l);
    const roll = Array.isArray(o.roll) ? lerp(o.roll[0], o.roll[1], e) : o.roll || 0;
    if (roll) camera.rotateZ(roll * DEG);
    camera.fov = Array.isArray(o.fov) ? lerp(o.fov[0], o.fov[1], e) : o.fov || 35;
    let fp = o.f ? (o.f.length === 2 && Array.isArray(o.f[0]) ? lerp3(o.f[0], o.f[1], (o.fe || ease.inOut)(clamp(u / d))) : o.f) : l;
    camera.getWorldDirection(_f);
    _v.set(fp[0], fp[1], fp[2]).sub(camera.position);
    pipe.scenePass.focus = Math.max(0.2, _v.dot(_f));
    pipe.scenePass.aperture = o.ap ?? 8;
  }

  function on(...names) {
    for (const n of names) W.sets[n].visible = true;
  }

  // lighting presets. o.focus: where the key-light shadow box sits (world). o.dread 0..1 drains the colour.
  function lights(name, o = {}) {
    const { hemi, key, prac, glows } = L;
    glows.forEach((g) => { g.intensity = 0; g.decay = 2; g.distance = 0; });
    prac.intensity = 0;
    const g = pipe.grade.uniforms;
    const fog = scene.fog;
    pipe.bloom.strength = 0.45;
    const focus = o.focus || [0, 0, -15];
    g.uLift.value.set(0, 0, 0);
    if (name === "sunset") {
      const dread = o.dread ?? 0;
      hemi.color.set("#ffc29a").lerp(col("#9a8ab8"), dread * 0.6);
      hemi.groundColor.set("#6a4a5a");
      hemi.intensity = lerp(1.7, 1.25, dread);
      key.color.set("#ffb070");
      key.intensity = lerp(4.6, 3.2, dread);
      // low sun from the east end of the boulevard
      const dir = new THREE.Vector3(SUN[0], SUN[1] * 3.2, SUN[2] + 60).normalize();
      key.target.position.set(focus[0], 0, focus[2]);
      key.position.set(focus[0] + dir.x * 150, dir.y * 150, focus[2] + dir.z * 150);
      fog.color.set("#ef9a7e").lerp(col("#8a6a8a"), dread * 0.5);
      fog.density = o.fogD ?? 0.0032;
      renderer.toneMappingExposure = o.exp ?? 1.0;
      g.uGain.value.set(1.06, 0.99, 0.92);
      g.uSat.value = lerp(1.18, 0.72, dread);
      g.uVignette.value = lerp(0.38, 0.62, dread);
      pipe.bloom.strength = 0.62;
      for (const m of P.neons || []) m.emissiveIntensity = 1.6;
      for (const l of P.lamps) l.bulb.emissiveIntensity = 0.6;
      P.sea.offset.set((o.t || 0) * 0.004, (o.t || 0) * 0.002);
    }
    if (name === "icu" || name === "morning") {
      fog.density = 0;
      const m = name === "morning" ? smooth(o.k ?? 1) : 0;
      hemi.color.lerpColors(col("#7f9ec0"), col("#ffe6c8"), m);
      hemi.groundColor.set("#4a5552");
      hemi.intensity = lerp(1.05, 1.7, m);
      // light through the window (left wall, x = -12)
      key.color.lerpColors(col("#a8c4ff"), col("#ffd29a"), m);
      key.intensity = lerp(1.4, 4.2, m);
      key.target.position.set(ICU[0] + 2, 2, ICU[2] - 1);
      key.position.set(ICU[0] - 70, 46, ICU[2] + 14);
      glows[0].color.set("#5dff9a");
      glows[0].position.set(ICU[0] + 5.6, 8.0, ICU[2] - 7.4);
      glows[0].intensity = lerp(16, 6, m);
      glows[0].distance = 14;
      glows[1].color.set("#eaf4ff");
      glows[1].position.set(ICU[0], 10.4, ICU[2] + 2);
      glows[1].intensity = lerp(10, 30, m) * (o.panel ?? 1);
      glows[1].distance = 30;
      P.icuPanel.color.setScalar(lerp(0.5, 1.3, m));
      P.icuOut.color.lerpColors(col("#3a4a78"), col("#ffe2b8"), m).multiplyScalar(lerp(0.8, 1.0, m));
      renderer.toneMappingExposure = lerp(1.25, 0.9, m);
      g.uGain.value.set(lerp(0.95, 1.05, m), lerp(1.0, 1.0, m), lerp(1.08, 0.94, m));
      g.uSat.value = lerp(0.78, 1.08, m);
      g.uVignette.value = lerp(0.6, 0.4, m);
      pipe.bloom.strength = lerp(0.5, 0.4, m);
    }
    if (name === "rain") {
      hemi.color.set("#8a96a8");
      hemi.groundColor.set("#2a2c30");
      hemi.intensity = 2.3;
      key.color.set("#b8c4d8");
      key.intensity = 1.6;
      key.target.position.set(RAIN[0] + focus[0], 0, RAIN[2] + focus[2]);
      key.position.set(RAIN[0] + focus[0] - 40, 90, RAIN[2] + focus[2] + 30);
      fog.color.set("#7d8590");
      fog.density = 0.011;
      renderer.toneMappingExposure = 1.3;
      g.uGain.value.set(0.95, 1.0, 1.08);
      g.uLift.value.set(0.0, 0.006, 0.014);
      g.uSat.value = 0.5;
      g.uVignette.value = 0.55;
      pipe.bloom.strength = 0.5;
    }
    if (name === "photo") {
      fog.density = 0;
      hemi.color.set("#fff2dc");
      hemi.groundColor.set("#6a8a5a");
      hemi.intensity = 2.0;
      key.color.set("#fff0d8");
      key.intensity = 4.5;
      key.target.position.set(0, 0, 1400);
      key.position.set(30, 60, 1450);
      renderer.toneMappingExposure = 1.0;
    }
    key.target.updateMatrixWorld();
    prac.target.updateMatrixWorld();
  }

  // ---- poses -------------------------------------------------------------
  function place(c, x, y, z, ry = 0) {
    c.root.visible = true;
    c.root.position.set(x, y, z);
    c.root.rotation.y = ry;
    if (c.size) c.root.scale.setScalar(c.size);
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
  function sit(a, seatY, lean = 0) {
    a.j.pelvis.position.y = seatY + 0.5;
    a.j.legL.rotation.x = a.j.legR.rotation.x = -Math.PI / 2;
    a.j.torso.rotation.x = lean;
    a.j.armL.rotation.x = a.j.armR.rotation.x = -0.35;
  }
  function wpos(obj, off = [0, 0, 0]) {
    obj.updateWorldMatrix(true, false);
    const v = new THREE.Vector3(off[0], off[1], off[2]).applyMatrix4(obj.matrixWorld);
    return [v.x, v.y, v.z];
  }
  function faceTo(c, x, z) {
    c.root.rotation.y = Math.atan2(x - c.root.position.x, z - c.root.position.z);
  }
  // world point from a car's local coordinates
  function carPt(car, p) {
    car.group.updateWorldMatrix(true, true);
    const v = new THREE.Vector3(p[0], p[1], p[2]).applyMatrix4(car.body.matrixWorld);
    return [v.x, v.y, v.z];
  }
  function flash(k, color = [1, 1, 1]) {
    const g = pipe.grade.uniforms;
    g.uFadeColor.value.set(color[0], color[1], color[2]);
    g.uFade.value = clamp(k);
  }
  return { cam, on, lights, place, walk, idle, sit, wpos, faceTo, carPt, flash };
}
