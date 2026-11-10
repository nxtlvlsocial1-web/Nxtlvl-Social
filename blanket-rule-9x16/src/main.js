// Stage: one three.js scene, every frame rebuilt from its timestamp (seek-safe, deterministic).
import * as THREE from "three";
import { createPipeline } from "./post.js";
import { buildWorld, BED, CHAIR } from "./world.js";
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
  const cast = makeCast();
  scene.add(cast.kid.root);
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
    // blanket covering the bed by default
    P.blanket.visible = true;
    P.blanket.position.set(BED.x, 3.45, -4.4);
    P.blanket.rotation.set(0, 0, 0);
    P.blanket.scale.set(1, 1, 1);
    // the clothes heap, slumped on the chair
    const h = P.heap;
    h.root.visible = true;
    h.root.position.set(CHAIR.x, 0, CHAIR.z);
    h.root.rotation.set(0, -Math.PI / 2, 0);
    h.pose(0);
    h.eyeMat.emissiveIntensity = 0;
    // the helper under the bed (hidden in the dark until a shot shows it)
    const l = P.lint;
    l.root.visible = true;
    l.root.position.set(BED.edgeX - 1.6, 0, -4.2);
    l.root.rotation.set(0, Math.PI / 2, 0);
    l.root.scale.setScalar(1);
    l.faceMat.map = l.faceAwake;
    l.faceMat.emissiveMap = l.faceAwake;
    l.faceMat.emissiveIntensity = 0.7;
    l.mask.visible = false;
    l.shoulder.visible = false;
    l.fingers.forEach((f) => f.rotation.set(0, 0, 0));
    P.note.visible = false;
    P.clock.set("3:07");
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
