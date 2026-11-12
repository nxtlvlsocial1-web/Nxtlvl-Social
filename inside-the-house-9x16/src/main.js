// Stage: one three.js scene, every frame rebuilt from its timestamp (seek-safe, deterministic).
import * as THREE from "three";
import { createPipeline } from "./post.js";
import { buildWorld, BED } from "./world.js";
import { makeCast } from "./chars.js";
import { buildShots } from "./shots.js";
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
  scene.background = new THREE.Color("#030305");
  const camera = new THREE.PerspectiveCamera(35, W / H, 0.05, 200);
  const world = buildWorld(scene);
  const P0 = world.props;
  const cast = makeCast();
  scene.add(cast.kid.root);
  scene.add(cast.mom.root);
  scene.add(cast.mimic.root);
  scene.add(cast.dog.root);
  scene.add(cast.stranger.root);
  scene.add(cast.friendA.root);
  scene.add(cast.friendB.root);
  const pmrem = new THREE.PMREMGenerator(renderer);
  const envTex = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.traverse((o) => {
    const mats = o.material ? (Array.isArray(o.material) ? o.material : [o.material]) : [];
    for (const m of mats) if (m.metalness > 0.25 || (m.transparent && m.roughness < 0.1)) { m.envMap = envTex; m.envMapIntensity = 0.6; }
  });
  const pipe = createPipeline(renderer, scene, camera, W, H, SCALE);
  const ctx = { THREE, scene, camera, renderer, W: world, C: cast, pipe, SCALE };
  const shots = buildShots(ctx);
  const P = world.props;

  function resetWorld() {
    cast.kid.reset();
    cast.kid.j.head.visible = true;
    cast.kid.j.armR.visible = true;
    cast.mom.reset();
    cast.mom.setOutfit("scrubs");
    cast.mimic.reset();
    // blanket covering the bed by default
    P.blanket.visible = true;
    P.blanket.position.set(BED.x, 3.45, -4.4);
    P.blanket.rotation.set(0, 0, 0);
    P.blanket.scale.set(1, 1, 1);
    P.blanket.material.color.setScalar(1);
    P.closetDoor.rotation.y = -Math.PI / 2 + 0.22;
    for (const ph of [P.phone, P.momPhone]) {
      ph.group.visible = false;
      ph.group.position.set(0, -50, 0);
      ph.group.rotation.set(0, 0, 0);
      ph.mat.color.setScalar(1);
      ph.grip.visible = false;
    }
    cast.dog.reset();
    cast.twin.reset();
    cast.friendA.reset();
    cast.friendB.reset();
    cast.stranger.reset();
    cast.kid.setOutfit("hoodie");
    cast.friendA.root.scale.setScalar(1);
    cast.friendB.root.scale.setScalar(1);
    for (const c of [P.cordless, P.strangerPhone]) {
      c.group.visible = false;
      c.group.position.set(0, -50, 0);
      c.group.rotation.set(0, 0, 0);
      c.set(["", ""], false);
      c.ring(false);
    }
    P.setClock(9, 0);
    P.lamp.shadeM.emissiveIntensity = 0;
    P.deadbolt.rotation.z = 0;
    P.arm.visible = false;
    P.tongue.group.visible = false;
    P.under.face.visible = false;
    P.under.face.rotation.set(0, Math.PI / 2, 0);
    P.under.face.scale.setScalar(1);
    P.under.hand.visible = false;
    P.drops.forEach((d) => (d.visible = false));
    P.clock.set("12:03");
    P.fanBlades.rotation.z = 0;
    world.dust.visible = false;
    camera.fov = 35;
    camera.up.set(0, 1, 0);
    pipe.scenePass.aperture = 0;
    pipe.grade.uniforms.uFade.value = 0;
  }

  function renderAt(t) {
    resetWorld();
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
