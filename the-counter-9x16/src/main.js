// Stage: one three.js scene, every frame rebuilt from its timestamp (seek-safe, deterministic).
import * as THREE from "three";
import { createPipeline } from "./post.js";
import { buildWorld } from "./world.js";
import { makeCast } from "./chars.js";
import { buildShots } from "./shots.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

const ready = window.__counterReady; // created by the inline head script

async function boot() {
  await document.fonts.load('800 100px "Poppins"');
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
  scene.background = new THREE.Color("#050608");
  const camera = new THREE.PerspectiveCamera(35, W / H, 0.05, 500);
  const world = buildWorld(scene);
  const cast = makeCast();
  for (const c of [cast.kid, cast.grandpa, cast.mom, cast.dog, cast.counter, ...cast.guests]) scene.add(c.root);
  const pmrem = new THREE.PMREMGenerator(renderer);
  const envTex = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.traverse((o) => {
    const mats = o.material ? (Array.isArray(o.material) ? o.material : [o.material]) : [];
    for (const m of mats) if (m.metalness > 0.25 || (m.transparent && m.roughness < 0.1)) { m.envMap = envTex; m.envMapIntensity = 0.9; }
  });
  const pipe = createPipeline(renderer, scene, camera, W, H, SCALE);
  const ctx = { THREE, scene, camera, renderer, W: world, C: cast, pipe, SCALE };
  const shots = buildShots(ctx);

  const everyone = [cast.kid, cast.grandpa, cast.mom, cast.dog, cast.counter, ...cast.guests];
  function resetWorld() {
    for (const c of everyone) c.reset();
    const P = world.props;
    P.door.rotation.y = 0;
    P.jar.root.visible = true;
    P.jar.root.position.set(-18.4, 3.43, 0.6);
    P.jar.root.rotation.set(0, 0, 0);
    P.jar.root.scale.setScalar(0.7);
    P.jar.setFill(0.92);
    P.jar.lid.position.set(0, 2.05, 0);
    P.jar.lid.visible = true;
    P.jar.lid.rotation.set(0, 0, 0);
    const v = P.vacuum;
    scene.add(v.root);
    v.root.visible = true;
    v.root.position.set(13.9, 0, -1.6);
    v.root.rotation.set(0, 2.6, 0);
    v.root.scale.setScalar(0.65);
    for (const part of ["bag", "lid"]) {
      v.root.add(v[part]);
      v[part].position.copy(v.homes[part]);
      v[part].rotation.set(0, 0, 0);
      v[part].scale.setScalar(1);
      v[part].visible = true;
    }
    v.light.material.emissiveIntensity = 0.1;
    for (const o of [P.broom, P.bag, P.plug, P.moth.root, P.crumb, P.stool, ...P.hands.map((h) => h.root)]) {
      scene.add(o);
      o.visible = false;
      o.position.set(0, -50, 0);
      o.rotation.set(0, 0, 0);
      o.scale.setScalar(1);
    }
    P.cupHome();
    P.cup.visible = true;
    P.zs.forEach((z) => (z.visible = false));
    world.rice.count = 0;
    world.dust.visible = false;
    world.setClock(9.5);
    P.clock.pend.rotation.z = 0;
    P.sky.night.material.opacity = 1;
    P.sky.dawn.material.opacity = 0;
    P.sky.day.material.opacity = 0;
    P.lamp.shadeMat.emissiveIntensity = 1.4;
    P.lamp.bulb.material.emissiveIntensity = 6;
    camera.fov = 35;
    camera.up.set(0, 1, 0);
    P.hands.forEach((h) => h.fingers.forEach((f) => f.rotation.set(0, 0, 0)));
    P.streetJars.forEach((j) => j.root.scale.setScalar(0.7));
    pipe.scenePass.aperture = 0;
    pipe.grade.uniforms.uFade.value = 0;
  }

  let last = -1;
  function renderAt(t) {
    resetWorld();
    let shot = shots[0];
    for (const s of shots) if (t >= s.t0) shot = s;
    shot.run(t - shot.t0, shot.t1 - shot.t0, t);
    camera.updateProjectionMatrix();
    pipe.grade.uniforms.uTime.value = Math.floor(t * 30) / 30;
    pipe.composer.render();
    last = t;
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
