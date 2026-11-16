// Stage: one three.js scene, every frame rebuilt from its timestamp (seek-safe, deterministic).
import * as THREE from "three";
import { createPipeline } from "./post.js";
import { buildWorld, BED } from "./world.js";
import { makeCast } from "./chars.js";
import { buildShots } from "./shots.js";
import { drawHud } from "./hud.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

const ready = window.__counterReady; // created by the inline head script

async function boot() {
  await document.fonts.load('800 100px "Poppins"');
  await document.fonts.load('700 40px "Poppins"');
  const vars = (window.__hyperframes && window.__hyperframes.getVariables && window.__hyperframes.getVariables()) || {};
  const qs = Number(new URLSearchParams(location.search).get("scale"));
  const SCALE = Number(vars.renderScale) > 0 ? Number(vars.renderScale) : qs > 0 ? qs : 1;
  const W = Math.round(1920 * SCALE), H = Math.round(1080 * SCALE);

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
  const camera = new THREE.PerspectiveCamera(35, W / H, 0.06, 700);
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
  for (const k of ["grandpa", "cop", "wpc", "janet", "margaret", "peggy", "dad", "mom", "sister", "grandma"]) if (cast[k] && !cast[k].root.parent) scene.add(cast[k].root);
  cast.guests.forEach((gst) => scene.add(gst.root));
  const pmrem = new THREE.PMREMGenerator(renderer);
  const envTex = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.traverse((o) => {
    const mats = o.material ? (Array.isArray(o.material) ? o.material : [o.material]) : [];
    for (const m of mats) if (m.metalness > 0.25 || (m.transparent && m.roughness < 0.1)) { m.envMap = envTex; m.envMapIntensity = 0.6; }
  });
  const pipe = createPipeline(renderer, scene, camera, W, H, SCALE);
  const ctx = { THREE, scene, camera, renderer, W: world, C: cast, pipe, SCALE, hud: null };
  const hudCanvas = document.getElementById("hud");
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
    for (const k of ["grandpa", "cop", "wpc", "janet", "margaret", "peggy", "dad", "mom", "sister", "grandma"]) cast[k].reset();
    cast.guests.forEach((gst) => gst.reset());
    // long-form sets: everything hidden until a shot turns its set on
    for (const k of Object.keys(P.sets)) P.sets[k].visible = false;
    P.dioWatcher.visible = P.dioEnfield.visible = false;
    for (const sk of [P.wb.skyDay, P.wb.skyDusk, P.wb.skyNight, P.eo.skyDay, P.eo.skyNight]) sk.visible = false;
    P.reno.visible = false;
    P.roller.visible = false;
    P.wb.mailbox.door.rotation.x = 0;
    P.wb.mailbox.flag.rotation.z = 0;
    P.wb.mailEnv.visible = false;
    P.wb.saleM.map = P.wb.saleTex.sale;
    P.wb.sale.visible = false;
    P.wb.sil.material.opacity = 0;
    P.chest.position.set(...P.chestHome);
    P.chest.rotation.set(0, 0, 0);
    P.diningChair.position.set(...P.diningHome);
    P.diningChair.rotation.set(0, -0.6, 0);
    P.toys.forEach((ty) => { ty.position.copy(ty.userData.home); ty.rotation.set(0, 0, 0); });
    P.frames.forEach((f) => (f.rotation.z = 0));
    P.enfBeds.forEach((b) => b.rotation.set(0, 0, 0));
    P.reels.forEach((r) => (r.rotation.y = 0));
    P.spoon.visible = false;
    P.handset70.position.set(0, 0.66, 0);
    P.handset70.rotation.set(0, 0, 0);
    P.arc.geometry.setDrawRange(0, 0);
    P.globe.rotation.x = 0;
    P.blanket.visible = false;
    P.handset70.visible = true;
    for (const o of [P.props2.cruiser.group, P.props2.env, P.props2.paper, P.props2.camera, P.props2.notebook, P.props2.mic, P.props2.handset]) { o.visible = false; o.position.set(0, -80, 0); o.rotation.set(0, 0, 0); }
    P.props2.flashM.color.set("#ffffff").multiplyScalar(0.2);
    P.props2.cruiser.red.color.set("#ff2a2a").multiplyScalar(0.3);
    P.props2.cruiser.blue.color.set("#2a6aff").multiplyScalar(0.3);
    pipe.grade.uniforms.uSat.value = 1;
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
    P.bedDoor.rotation.y = 0;
    P.frontDoor.rotation.y = 0;
    P.voidWall.visible = false;
    P.lock.set(false);
    P.lantern.m.emissiveIntensity = 0;
    ctx.hud = null;
    pipe.grade.uniforms.uGrain.value = 0.035;
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
    drawHud(hudCanvas, ctx.hud);
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
