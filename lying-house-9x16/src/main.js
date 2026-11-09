// Stage: one three.js scene, every frame rebuilt from its timestamp (seek-safe, deterministic).
import * as THREE from "three";
import { createPipeline } from "./post.js";
import { buildWorld } from "./world.js";
import { makeCast } from "./chars.js";
import { buildShots, T_DOOR48, T_DOOR49, T_POP1, T_OPEN48 } from "./shots.js";
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
  const camera = new THREE.PerspectiveCamera(35, W / H, 0.05, 600);
  const world = buildWorld(scene);
  const cast = makeCast();
  const everyone = [cast.kid, cast.mom, cast.dad, cast.sister, cast.grandma, cast.dog];
  for (const c of everyone) scene.add(c.root);
  const pmrem = new THREE.PMREMGenerator(renderer);
  const envTex = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.traverse((o) => {
    const mats = o.material ? (Array.isArray(o.material) ? o.material : [o.material]) : [];
    for (const m of mats) if (m.metalness > 0.25 || (m.transparent && m.roughness < 0.1)) { m.envMap = envTex; m.envMapIntensity = 0.9; }
  });
  const pipe = createPipeline(renderer, scene, camera, W, H, SCALE);
  const ctx = { THREE, scene, camera, renderer, W: world, C: cast, pipe, SCALE };
  const shots = buildShots(ctx);
  const P = world.props;

  function resetWorld(t) {
    for (const c of everyone) c.reset();
    cast.sister.j.handR.add(cast.sister.phone);
    cast.sister.phone.position.set(0, -0.1, 0.55);
    cast.sister.phone.rotation.set(-1.3, 0, 0);
    cast.sister.phone.visible = true;
    for (let n = 1; n <= 49; n++) {
      const d = P.doors[n];
      d.pivot.rotation.y = 0;
      d.root.scale.setScalar(1);
    }
    P.doors[48].root.visible = t >= T_DOOR48;
    P.doors[48].root.position.y = 0;
    P.doors[49].root.visible = t >= T_DOOR49;
    P.doors[49].root.position.x = 4.02;
    P.endPlug.visible = t < T_OPEN48;
    P.glow48.visible = false;
    P.rooms[12].spill.forEach((l) => (l.visible = false));
    P.rooms[30].sheets.forEach((s) => (s.visible = false));
    P.rooms[47].balloons.forEach(({ obj, a, b, c }, i) => {
      obj.visible = true;
      obj.position.set(-5.3 - a * 2.6, 0.6 + b * 2.4, -110.8 + (c - 0.5) * 1.6);
      obj.rotation.set(0, 0, 0);
    });
    P.rooms[47].nums.forEach((m) => (m.visible = false));
    P.popRooms[0].grp.scale.setScalar(t >= T_POP1 + 0.6 ? 1 : 0.0001);
    P.popRooms[1].grp.scale.setScalar(0.0001);
    scene.add(P.floret);
    P.floret.visible = false;
    P.floret.scale.setScalar(0.28);
    P.floret.rotation.set(0, 0, 0);
    P.avalanche.forEach((b) => (b.visible = false));
    P.plateBroc.forEach((b) => (b.visible = false));
    P.dadLoaf.visible = true;
    P.dinWinDay.material.opacity = 0;
    world.dust.visible = false;
    camera.fov = 35;
    camera.up.set(0, 1, 0);
    pipe.scenePass.aperture = 0;
    pipe.grade.uniforms.uFade.value = 0;
  }

  function renderAt(t) {
    resetWorld(t);
    let shot = shots[0];
    for (const s of shots) if (t >= s.t0) shot = s;
    shot.run(t - shot.t0, shot.t1 - shot.t0, t);
    camera.updateProjectionMatrix();
    pipe.grade.uniforms.uTime.value = Math.floor(t * 30) / 30;
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
