// Stage: one three.js scene, every frame rebuilt from its timestamp (seek-safe, deterministic).
import * as THREE from "three";
import { createPipeline } from "./post.js";
import { buildWorld, PHOTO } from "./world.js";
import { makeRespawnCast } from "./chars.js";
import { buildShots } from "./shots.js";
import { makeDirector } from "./direct.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

const ready = window.__counterReady; // created by the inline head script

async function boot() {
  await document.fonts.load('800 100px "Poppins"');
  await document.fonts.load('700 40px "Poppins"');
  const vars = (window.__hyperframes && window.__hyperframes.getVariables && window.__hyperframes.getVariables()) || {};
  const qs = Number(new URLSearchParams(location.search).get("scale"));
  const SCALE = Number(vars.renderScale) > 0 ? Number(vars.renderScale) : qs > 0 ? qs : 1;
  const W = Math.round(1080 * SCALE), H = Math.round(1920 * SCALE);

  const canvas = document.getElementById("stage");
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, preserveDrawingBuffer: true, powerPreference: "high-performance" });
  renderer.setPixelRatio(1);
  renderer.setSize(W, H, false);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color("#050507");
  const camera = new THREE.PerspectiveCamera(35, W / H, 0.06, 1200);
  const world = buildWorld(scene);
  const P = world.props;
  const cast = makeRespawnCast();
  for (const a of [cast.driver, cast.lily, ...cast.crowd]) scene.add(a.root);
  const pmrem = new THREE.PMREMGenerator(renderer);
  const envTex = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.traverse((o) => {
    const mats = o.material ? (Array.isArray(o.material) ? o.material : [o.material]) : [];
    for (const m of mats) if (m.metalness > 0.25 || (m.transparent && m.roughness < 0.1)) { m.envMap = envTex; m.envMapIntensity = 0.7; }
  });
  const pipe = createPipeline(renderer, scene, camera, W, H, SCALE);
  const ctx = { THREE, scene, camera, renderer, W: world, C: cast, pipe, SCALE, hud: null };
  const D = makeDirector(ctx);

  function resetWorld() {
    for (const g of Object.values(world.sets)) g.visible = false;
    for (const a of [cast.driver, cast.lily, ...cast.crowd]) a.reset();
    cast.driver.setOutfit("shirt");
    cast.driver.bandage(false);
    for (const c of [P.car, P.cop, P.famCar]) {
      c.group.visible = false;
      c.group.position.set(0, -80, 0);
      c.group.rotation.set(0, 0, 0);
      c.body.position.set(0, 0, 0);
      c.body.rotation.set(0, 0, 0);
      c.wheels.forEach((w) => w.rotation.set(0, 0, 0));
    }
    P.car.radio.set("FM", "88.1");
    P.car.radio.screenM.emissiveIntensity = 1.1;
    P.car.visor.rotation.x = 0;
    P.famCar.visor.rotation.x = 0;
    P.cop.flash(0, 0);
    P.famCar.wipers.forEach((w) => (w.rotation.z = 0));
    for (const c of P.traffic) {
      c.group.visible = true;
      c.group.position.copy(c.home);
    }
    P.ceilM.opacity = 0;
    P.ecgSky.set(0);
    P.ecgSky.mesh.scale.setScalar(1);
    P.doorL.position.x = -2.5;
    P.doorR.position.x = 2.5;
    P.inside.color.set("#dbeefa").multiplyScalar(0.85);
    P.tlLamps.forEach((m) => (m.emissiveIntensity = 0));
    P.truck.group.position.set(0, 0, 400);
    P.truck.flare.material.opacity = 0;
    P.rain.mesh.visible = true;
    P.monitor.set(0, { bpm: 42 });
    P.sun.disc.visible = P.sun.halo.visible = true;
    scene.fog.density = 0;
    camera.fov = 35;
    pipe.scenePass.aperture = 0;
    const g = pipe.grade.uniforms;
    g.uFade.value = 0;
    g.uFadeColor.value.set(0, 0, 0);
    g.uGrain.value = 0.03;
    g.uSat.value = 1.05;
  }

  // the photo on the sun visor: Lily in a sunny backyard, rendered once into a texture
  {
    resetWorld();
    world.sets.photo.visible = true;
    D.lights("photo");
    L_photoTone();
    D.place(cast.lily, PHOTO[0], 0, PHOTO[2] + 2, 0);
    cast.lily.setFace("lilyHappy");
    cast.lily.j.armR.rotation.set(0, 0, 2.6);
    cast.lily.j.head.rotation.z = 0.12;
    const pcam = new THREE.PerspectiveCamera(30, 1.3, 0.1, 200);
    pcam.position.set(PHOTO[0] + 0.4, 3.0, PHOTO[2] + 14);
    pcam.lookAt(PHOTO[0], 2.6, PHOTO[2] + 2);
    const rt = new THREE.WebGLRenderTarget(520, 400, { samples: 4 });
    rt.texture.colorSpace = THREE.SRGBColorSpace;
    const tm = renderer.toneMapping;
    renderer.setRenderTarget(rt);
    renderer.render(scene, pcam);
    renderer.setRenderTarget(null);
    renderer.toneMapping = tm;
    for (const c of [P.car, P.famCar]) {
      c.photoM.map = rt.texture;
      c.photoM.needsUpdate = true;
    }
  }
  function L_photoTone() {
    world.lights.hemi.intensity = 1.1;
    world.lights.key.intensity = 2.2;
  }

  const shots = buildShots(ctx, D);
  function renderAt(t) {
    resetWorld();
    let shot = shots[0];
    for (const s of shots) if (t >= s.t0) shot = s;
    shot.run(t - shot.t0, shot.t1 - shot.t0, t);
    if (window.__dbgCam) { // dev only: look at the set from a fixed camera
      const c = window.__dbgCam;
      camera.position.set(...c.p);
      camera.up.set(0, 1, 0);
      camera.lookAt(...c.l);
      camera.fov = c.fov || 50;
      pipe.scenePass.aperture = 0;
      pipe.grade.uniforms.uFade.value = 0;
    }
    camera.updateProjectionMatrix();
    pipe.grade.uniforms.uTime.value = Math.floor(t * 24) / 24;
    pipe.composer.render();
  }
  window.__counter = { renderAt, ctx, shots };
  window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
  renderer.compile(scene, camera);
  renderAt(window.__hfThreeTime || 0);
}

boot().then(() => ready.resolve(), (err) => {
  console.error("stage boot failed", err);
  ready.resolve();
});
