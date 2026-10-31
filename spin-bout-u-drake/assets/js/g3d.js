// 3D renders for the Spin Bout U edit: one WebGL renderer, one scene per lyric line.
// window.G3D (plan/g3d.json, written by build/generate.py) lists the scenes: {id, kind, t0, t1, bg, cues}.
// build/render3d.cjs draws every 20 fps frame of each scene here and reads the canvas back (headless SwiftShader WebGL
// deadlocks with page screenshots, so the 3D is pre-rendered to assets/video/g3d/<id>.mp4, opaque on the scene's own
// background colour, and the composition plays those clips). Palette and kinds match the 2D design.
import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

const S = 1080, FPS = 20;
const MAG = 0xa3214c, MAR = 0x5f1b30, INK = 0x191919, WHT = 0xf0f2f2, RED = 0xe0242f;
const canvas = document.createElement("canvas");
canvas.width = S; canvas.height = S;
canvas.style.cssText = "position:absolute;inset:0;width:1080px;height:1080px";
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(S, S, false);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
const pmrem = new THREE.PMREMGenerator(renderer);
const ENV = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

function rng(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }
const ease = (u) => 1 - Math.pow(1 - Math.min(1, Math.max(0, u)), 3);
const back = (u) => { u = Math.min(1, Math.max(0, u)); const c = 1.7; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };

// ---------------------------------------------------------------- shared builders
function textGeo(str, size, depth, bevel = true) {
  const G = window.ANTON, k = size / G.upm, shapes = [];
  let x = 0;
  for (const ch of str) {
    const g = G.g[ch] || G.g[" "];
    const p = new THREE.ShapePath();
    for (const c of g.c) {
      if (c[0] === "m") p.moveTo(x + c[1] * k, c[2] * k);
      else if (c[0] === "l") p.lineTo(x + c[1] * k, c[2] * k);
      else if (c[0] === "q") p.quadraticCurveTo(x + c[1] * k, c[2] * k, x + c[3] * k, c[4] * k);
      else if (c[0] === "b") p.bezierCurveTo(x + c[1] * k, c[2] * k, x + c[3] * k, c[4] * k, x + c[5] * k, c[6] * k);
    }
    shapes.push(...p.toShapes());
    x += g.a * k;
  }
  const geo = new THREE.ExtrudeGeometry(shapes, { depth, bevelEnabled: bevel, bevelThickness: depth * 0.12, bevelSize: size * 0.012,
    bevelSegments: 2, curveSegments: 6 });
  geo.computeBoundingBox();
  const b = geo.boundingBox;
  geo.translate(-(b.max.x + b.min.x) / 2, -(b.max.y + b.min.y) / 2, -depth / 2);
  return geo;
}
function text3d(str, size, depth, face = WHT, side = MAG) {
  return new THREE.Mesh(textGeo(str, size, depth), [
    new THREE.MeshStandardMaterial({ color: face, roughness: 0.35, metalness: 0.1 }),
    new THREE.MeshStandardMaterial({ color: side, roughness: 0.5, metalness: 0.2 }),
  ]);
}
function lights(scene, warm = MAG) {
  scene.add(new THREE.AmbientLight(0xffffff, 0.45));
  const k = new THREE.DirectionalLight(0xffffff, 2.2); k.position.set(3, 5, 6); scene.add(k);
  const r = new THREE.PointLight(warm, 60, 30); r.position.set(-5, -2, 4); scene.add(r);
  return r;
}
function cam(fov = 35, z = 10) { const c = new THREE.PerspectiveCamera(fov, 1, 0.1, 200); c.position.set(0, 0, z); return c; }
function canvasTex(w, h, draw) {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  draw(c.getContext("2d"), w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
}
function roundRect(w, h, r) {
  const s = new THREE.Shape(), x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r); s.lineTo(x + w, y + h - r);
  s.quadraticCurveTo(x + w, y + h, x + w - r, y + h); s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r);
  s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y); return s;
}
function plane() {
  const g = new THREE.Group(), m = new THREE.MeshStandardMaterial({ color: WHT, roughness: 0.4, metalness: 0.3 });
  const body = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.07, 1.1, 10), m); body.rotation.z = Math.PI / 2; g.add(body);
  const wing = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.02, 1.1), m); g.add(wing);
  const tail = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.02, 0.42), m); tail.position.x = -0.48; g.add(tail);
  const fin = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.22, 0.02), m); fin.position.set(-0.48, 0.1, 0); g.add(fin);
  return g;
}

// ---------------------------------------------------------------- the scenes
const KINDS = {
  phone(c) {   // the ex calls: a phone turns to camera, declined, a red X slams on it
    const scene = new THREE.Scene(), camera = cam(32, 14); lights(scene);
    const g = new THREE.Group(); scene.add(g);
    const body = new THREE.Mesh(new THREE.ExtrudeGeometry(roundRect(2.4, 5, 0.42), { depth: 0.3, bevelEnabled: true, bevelThickness: 0.06, bevelSize: 0.06, bevelSegments: 3 }),
      new THREE.MeshStandardMaterial({ color: 0x222226, roughness: 0.25, metalness: 0.8, envMap: ENV }));
    body.position.z = -0.15; g.add(body);
    const scr = canvasTex(480, 1000, (x, w, h) => {
      x.fillStyle = "#1c1c1e"; x.fillRect(0, 0, w, h);
      x.fillStyle = "#fff"; x.textAlign = "center"; x.font = "600 92px Arial"; x.fillText("Ex", w / 2, 210);
      x.fillStyle = "#9a9a9a"; x.font = "500 34px Arial"; x.fillText("mobile", w / 2, 268);
      x.fillStyle = "#ff3b30"; x.beginPath(); x.arc(120, 800, 68, 0, 7); x.fill();
      x.fillStyle = "#34c759"; x.beginPath(); x.arc(360, 800, 68, 0, 7); x.fill();
      x.fillStyle = "#fff"; x.font = "500 30px Arial"; x.fillText("Decline", 120, 912); x.fillText("Accept", 360, 912);
    });
    const screen = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 4.6), new THREE.MeshBasicMaterial({ map: scr })); screen.position.z = 0.26; g.add(screen);
    const ring = new THREE.Mesh(new THREE.RingGeometry(0.3, 0.36, 40), new THREE.MeshBasicMaterial({ color: 0xff3b30, transparent: true }));
    ring.position.set(-0.55, -1.53, 0.27); g.add(ring);
    const xm = new THREE.MeshStandardMaterial({ color: RED, emissive: RED, emissiveIntensity: 0.4, roughness: 0.4 });
    const X = new THREE.Group(); [1, -1].forEach((s) => { const b = new THREE.Mesh(new THREE.BoxGeometry(5.6, 0.55, 0.4), xm); b.rotation.z = s * 0.95; X.add(b); });
    X.position.z = 0.8; g.add(X);
    return { scene, camera, update(t) {
      const u = ease(t / 0.4);
      g.rotation.y = (1 - u) * 1.6 + Math.sin(t * 2.2) * 0.12; g.rotation.x = -0.12 + Math.sin(t * 1.7) * 0.05;
      g.position.y = Math.sin(t * 6) * 0.04;                        // ringing buzz
      g.rotation.z = (t < c.hit ? Math.sin(t * 40) * 0.02 : 0);
      ring.scale.setScalar(1 + ((t * 2.5) % 1) * 1.6); ring.material.opacity = t < c.hit ? 1 - ((t * 2.5) % 1) : 0;
      const k = back((t - c.hit) / 0.25); X.scale.setScalar(t < c.hit ? 0.001 : Math.max(0.001, k)); X.rotation.z = (1 - Math.min(1, k)) * 0.8;
    } };
  },
  globe(c) {   // travel 'cross the globe: wireframe planet, orbit ring, planes and pins
    const scene = new THREE.Scene(), camera = cam(34, 15); lights(scene);
    const g = new THREE.Group(); scene.add(g); g.rotation.z = 0.35;
    g.add(new THREE.Mesh(new THREE.SphereGeometry(2.6, 48, 32), new THREE.MeshStandardMaterial({ color: INK, roughness: 0.9 })));
    const wire = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.IcosahedronGeometry(2.64, 3)), new THREE.LineBasicMaterial({ color: MAG }));
    g.add(wire);
    for (let k = -2; k <= 2; k++) { const r = 2.68 * Math.cos(k * 0.5); const ring = new THREE.Mesh(new THREE.TorusGeometry(r, 0.018, 6, 90), new THREE.MeshBasicMaterial({ color: WHT }));
      ring.rotation.x = Math.PI / 2; ring.position.y = 2.68 * Math.sin(k * 0.5); g.add(ring); }
    const pins = []; const R = rng(9);
    for (let k = 0; k < 7; k++) { const p = new THREE.Mesh(new THREE.ConeGeometry(0.12, 0.42, 12), new THREE.MeshStandardMaterial({ color: MAG, emissive: MAG, emissiveIntensity: 0.6 }));
      const th = R() * Math.PI * 2, ph = (R() - 0.5) * 2.2; p.position.setFromSphericalCoords(2.85, Math.PI / 2 - ph, th); p.lookAt(0, 0, 0); p.rotateX(-Math.PI / 2); g.add(p); pins.push(p); }
    const orbit = new THREE.Mesh(new THREE.TorusGeometry(4.1, 0.025, 6, 140), new THREE.MeshBasicMaterial({ color: WHT })); orbit.rotation.x = 1.25; scene.add(orbit);
    const planes = [0, 1, 2].map(() => { const p = plane(); p.scale.setScalar(0.9); scene.add(p); return p; });
    return { scene, camera, update(t) {
      const s = back(t / 0.45); g.scale.setScalar(Math.max(0.01, s)); g.rotation.y = t * 0.9;
      planes.forEach((p, k) => { const a = t * 1.3 + k * 2.094; const v = new THREE.Vector3(Math.cos(a) * 4.1, Math.sin(a) * 4.1, 0).applyEuler(orbit.rotation);
        const a2 = a + 0.05; const v2 = new THREE.Vector3(Math.cos(a2) * 4.1, Math.sin(a2) * 4.1, 0).applyEuler(orbit.rotation);
        p.position.copy(v); p.lookAt(v2); p.rotateY(-Math.PI / 2); });
      pins.forEach((p, k) => p.scale.setScalar(t > 0.3 + k * 0.12 ? 1 : 0.001));
      camera.position.set(Math.sin(t * 0.4) * 1.2, 0.6, 16 - t * 0.6); camera.lookAt(0, 0, 0);
    } };
  },
  road(c) {    // to the end of the road: driving at dusk, centre line rushing, a sign passes
    const scene = new THREE.Scene(), camera = cam(55, 0); scene.fog = new THREE.Fog(MAR, 10, 70);
    scene.add(new THREE.AmbientLight(0xffffff, 0.9));
    const sun = new THREE.Mesh(new THREE.CircleGeometry(9, 64), new THREE.MeshBasicMaterial({ color: MAG, fog: false })); sun.position.set(0, 5, -90); scene.add(sun);
    for (let k = 0; k < 6; k++) { const bar = new THREE.Mesh(new THREE.PlaneGeometry(20, 0.5 + k * 0.25), new THREE.MeshBasicMaterial({ color: MAR, fog: false }));
      bar.position.set(0, 2 - k * 1.5, -89); scene.add(bar); }
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(400, 400), new THREE.MeshBasicMaterial({ color: INK })); ground.rotation.x = -Math.PI / 2; scene.add(ground);
    const road = new THREE.Mesh(new THREE.PlaneGeometry(8, 400), new THREE.MeshBasicMaterial({ color: 0x2b2b2e })); road.rotation.x = -Math.PI / 2; road.position.y = 0.01; scene.add(road);
    [-3.7, 3.7].forEach((x) => { const e = new THREE.Mesh(new THREE.PlaneGeometry(0.18, 400), new THREE.MeshBasicMaterial({ color: WHT })); e.rotation.x = -Math.PI / 2; e.position.set(x, 0.02, 0); scene.add(e); });
    const dashes = []; for (let k = 0; k < 30; k++) { const d = new THREE.Mesh(new THREE.PlaneGeometry(0.25, 2.4), new THREE.MeshBasicMaterial({ color: WHT })); d.rotation.x = -Math.PI / 2; d.position.y = 0.03; scene.add(d); dashes.push(d); }
    const sign = new THREE.Group(); scene.add(sign);
    const post = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 4, 8), new THREE.MeshBasicMaterial({ color: 0x777777 })); post.position.y = 2; sign.add(post);
    const st = canvasTex(1024, 512, (x, w, h) => { x.fillStyle = "#a3214c"; x.fillRect(0, 0, w, h); x.strokeStyle = "#f0f2f2"; x.lineWidth = 22; x.strokeRect(24, 24, w - 48, h - 48);
      x.fillStyle = "#f0f2f2"; x.textAlign = "center"; x.font = "bold 150px Impact, Arial Black, sans-serif"; x.fillText("END OF", w / 2, 230); x.fillText("THE ROAD", w / 2, 400); });
    const board = new THREE.Mesh(new THREE.PlaneGeometry(3.6, 1.8), new THREE.MeshBasicMaterial({ map: st, side: THREE.DoubleSide })); board.position.y = 4.6; sign.add(board);
    sign.position.set(5.2, 0, -60);
    return { scene, camera, update(t) {
      const z = t * 22;
      dashes.forEach((d, k) => { d.position.z = -((k * 5 - z) % 150 + 150) % 150 + 5; });
      sign.position.z = -70 + t * 26; sign.rotation.y = -0.35;
      camera.position.set(Math.sin(t * 1.1) * 0.4, 1.6 + Math.sin(t * 7) * 0.02, 6); camera.lookAt(0, 1.4, -40);
    } };
  },
  words(c) {   // hook 1: the line as extruded 3D words, each popping on its sung word, the block turning in perspective
    const scene = new THREE.Scene(), camera = cam(36, 14); lights(scene);
    const g = new THREE.Group(); scene.add(g);
    const items = c.words.map((w, k) => { const m = text3d(w.t, w.s, w.s * 0.35, k % 2 ? MAG : WHT, k % 2 ? MAR : MAG); m.position.set(w.x, w.y, 0); g.add(m); return [m, w.at]; });
    return { scene, camera, update(t) {
      items.forEach(([m, at]) => { const k = back((t - at) / 0.2); m.scale.setScalar(t < at ? 0.001 : Math.max(0.001, k)); m.rotation.x = (1 - Math.min(1, k)) * -1.2; });
      g.rotation.y = -0.32 + t * 0.1; g.rotation.x = 0.14 - t * 0.025; camera.position.z = 16 - t * 0.3;
    } };
  },
  diamonds(c) {   // somethin' gettin' dropped: diamonds rain down and bounce, one big stone turning
    const scene = new THREE.Scene(), camera = cam(40, 12); lights(scene, 0xff3d7f); scene.environment = ENV;
    const mat = new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 1, roughness: 0.06, envMapIntensity: 1.6, flatShading: true });
    const big = new THREE.Mesh(new THREE.OctahedronGeometry(1.7, 0), mat); big.scale.y = 1.35; scene.add(big);
    const R = rng(4), drops = [];
    for (let k = 0; k < 16; k++) { const d = new THREE.Mesh(new THREE.OctahedronGeometry(0.28 + R() * 0.35, 0), k % 3 ? mat : new THREE.MeshStandardMaterial({ color: MAG, roughness: 0.2, metalness: 0.6, flatShading: true }));
      d.userData = { x: (R() - 0.5) * 9, z: (R() - 0.5) * 3, t0: c.drop + R() * 1.4, spin: R() * 6 }; scene.add(d); drops.push(d); }
    return { scene, camera, update(t) {
      big.rotation.y = t * 1.4; big.position.y = 0.4 + Math.sin(t * 2) * 0.15; big.scale.setScalar(t < c.drop ? 0.6 : 1); big.scale.y *= 1.35;
      drops.forEach((d) => { const u = t - d.userData.t0; if (u < 0) { d.visible = false; return; } d.visible = true;
        const fall = 7 - 0.5 * 30 * u * u; const y = fall > -3.2 ? fall : -3.2 + Math.abs(Math.sin((u - Math.sqrt(10.2 / 15)) * 9)) * 0.8 * Math.exp(-(u - 0.8) * 3);
        d.position.set(d.userData.x, y, d.userData.z); d.rotation.set(u * d.userData.spin, u * 3, 0); });
    } };
  },
  smoke(c) {      // smoke: 3D SMOKE inside rising, swelling smoke puffs
    const scene = new THREE.Scene(), camera = cam(36, 12); lights(scene);
    const word = text3d("SMOKE", 2.1, 0.8, WHT, 0x8a8487); scene.add(word);
    const tex = canvasTex(256, 256, (x, w, h) => { const g = x.createRadialGradient(128, 128, 10, 128, 128, 128); g.addColorStop(0, "rgba(220,220,225,.85)"); g.addColorStop(1, "rgba(220,220,225,0)"); x.fillStyle = g; x.fillRect(0, 0, w, h); });
    const R = rng(12), puffs = [];
    for (let k = 0; k < 26; k++) { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, depthWrite: false, opacity: 0.3 }));
      s.userData = { x: (R() - 0.5) * 9, z: (R() - 0.5) * 4, ph: R(), sp: 0.4 + R() * 0.6 }; scene.add(s); puffs.push(s); }
    return { scene, camera, update(t) {
      const u = ease(t / 0.6); word.scale.setScalar(0.6 + 0.4 * u); word.rotation.y = -0.3 + t * 0.15; word.position.y = 0.6 - t * 0.1;
      puffs.forEach((s) => { const p = (s.userData.ph + t * s.userData.sp * 0.35) % 1; s.position.set(s.userData.x + Math.sin(p * 6 + s.userData.ph * 9) * 0.6, -4 + p * 9, s.userData.z);
        s.scale.setScalar(1.2 + p * 3.5); s.material.opacity = Math.sin(p * Math.PI) * 0.28; });
    } };
  },
  city(c) {       // burn somebody block: a city block at night, flames flickering on the roofs, the camera circling
    const scene = new THREE.Scene(), camera = cam(40, 0); scene.fog = new THREE.Fog(INK, 30, 75);
    scene.add(new THREE.AmbientLight(0xffffff, 0.35));
    const fire = new THREE.PointLight(0xff5a1f, 160, 40); fire.position.set(0, 6, 0); scene.add(fire);
    const R = rng(21), flames = [];
    const RW = rng(77);                    // seeded: every render worker draws the same windows
    const win = canvasTex(64, 128, (x, w, h) => { x.fillStyle = "#1e1e22"; x.fillRect(0, 0, w, h); for (let yy = 6; yy < h; yy += 14) for (let xx = 6; xx < w; xx += 14) { x.fillStyle = RW() < 0.35 ? "#ffb347" : "#2c2c33"; x.fillRect(xx, yy, 7, 8); } });
    win.wrapS = win.wrapT = THREE.RepeatWrapping;
    for (let i = -3; i <= 3; i++) for (let j = -3; j <= 3; j++) { if (i === 0 && j === 0) continue;
      const h = 1.5 + R() * 6; const b = new THREE.Mesh(new THREE.BoxGeometry(1.6, h, 1.6), new THREE.MeshStandardMaterial({ map: win, emissiveMap: win, emissive: 0xffffff, emissiveIntensity: 0.35, roughness: 0.8 }));
      b.position.set(i * 2.4, h / 2, j * 2.4); scene.add(b);
      if (R() < 0.45) { const f = new THREE.Mesh(new THREE.ConeGeometry(0.6, 1.8, 9), new THREE.MeshBasicMaterial({ color: R() < 0.5 ? 0xff7a1a : MAG, transparent: true, opacity: 0.9 }));
        f.position.set(i * 2.4, h + 0.9, j * 2.4); f.userData = { h, ph: R() * 9 }; scene.add(f); flames.push(f); } }
    const ground = new THREE.Mesh(new THREE.CircleGeometry(9.6, 64), new THREE.MeshStandardMaterial({ color: 0x1a1216, emissive: 0x5f1b30, emissiveIntensity: 0.35 })); ground.rotation.x = -Math.PI / 2; scene.add(ground);
    return { scene, camera, update(t) {
      const a = 0.6 + t * 0.35; camera.position.set(Math.sin(a) * 30, 15 + Math.sin(t) * 0.5, Math.cos(a) * 30); camera.lookAt(0, 2.2, 0);
      flames.forEach((f) => { const n = 0.75 + 0.35 * Math.sin(t * 23 + f.userData.ph) * Math.sin(t * 17 + f.userData.ph * 2); f.scale.set(1, n * 1.4, 1); f.position.y = f.userData.h + 0.9 * n * 1.4; });
      fire.intensity = 130 + 50 * Math.sin(t * 19) * Math.sin(t * 7);
    } };
  },
  heart(c) {      // hook 2: a chrome heart, beating on the beat
    const scene = new THREE.Scene(), camera = cam(34, 16); lights(scene); scene.environment = ENV;
    const s = new THREE.Shape(); s.moveTo(0, -2.2); s.bezierCurveTo(-0.6, -1.5, -3, -0.4, -3, 1); s.bezierCurveTo(-3, 2.4, -1.4, 3, 0, 1.7);
    s.bezierCurveTo(1.4, 3, 3, 2.4, 3, 1); s.bezierCurveTo(3, -0.4, 0.6, -1.5, 0, -2.2);
    const geo = new THREE.ExtrudeGeometry(s, { depth: 1.1, bevelEnabled: true, bevelThickness: 0.5, bevelSize: 0.45, bevelSegments: 8, curveSegments: 32 }); geo.center();
    const heart = new THREE.Mesh(geo, new THREE.MeshPhysicalMaterial({ color: 0xff7aa6, metalness: 1, roughness: 0.12, clearcoat: 1, envMapIntensity: 2 })); scene.add(heart);
    return { scene, camera, update(t, T) {
      const lb = c.beats.filter((b) => b <= T).pop() ?? -9; const pulse = 1 + 0.12 * Math.exp(-(T - lb) / 0.12);
      heart.scale.setScalar(back(t / 0.4) * pulse); heart.rotation.y = t * 1.6; heart.rotation.x = Math.sin(t) * 0.15;
    } };
  },
  body(c) {       // comin' out my body: BODY in 3D, the letters burst apart on "out" and drift back
    const scene = new THREE.Scene(), camera = cam(36, 15); lights(scene);
    const R = rng(3), parts = [];
    let x0 = -3.15;
    for (const ch of "BODY") { const m = text3d(ch, 2.6, 0.9, WHT, MAG); m.position.x = x0; x0 += 2.1; scene.add(m);
      m.userData = { bx: m.position.x, dx: (R() - 0.5) * 8, dy: (R() - 0.5) * 6, dz: 2 + R() * 4, rx: (R() - 0.5) * 4, ry: (R() - 0.5) * 4 }; parts.push(m); }
    return { scene, camera, update(t) {
      const e = t < c.out ? 0 : Math.sin(Math.min(1, (t - c.out) / 1.6) * Math.PI) * ease((t - c.out) / 0.25);
      parts.forEach((m, k) => { const d = m.userData; m.position.set(d.bx + d.dx * e, d.dy * e + Math.sin(t * 2 + k) * 0.1, d.dz * e); m.rotation.set(d.rx * e, -0.2 + d.ry * e + t * 0.1, 0); });
      camera.position.x = Math.sin(t * 0.5) * 1.5; camera.lookAt(0, 0, 0);
    } };
  },
  tissue(c) {     // wipe him like he snotty: a tissue box, a tissue pulled out and waving
    const scene = new THREE.Scene(), camera = cam(34, 14); lights(scene);
    const g = new THREE.Group(); scene.add(g);
    const bt = canvasTex(512, 256, (x, w, h) => { x.fillStyle = "#a3214c"; x.fillRect(0, 0, w, h); x.fillStyle = "#f0f2f2"; for (let k = 0; k < 9; k++) { x.beginPath(); x.arc(30 + k * 60, 128 + Math.sin(k) * 50, 18, 0, 7); x.fill(); }
      x.font = "bold 70px Impact, Arial Black, sans-serif"; x.textAlign = "center"; x.fillText("SNOTTY", w / 2, 150); });
    const box = new THREE.Mesh(new THREE.BoxGeometry(4.2, 2.2, 2.4), [0, 1, 2, 3, 4, 5].map((k) => new THREE.MeshStandardMaterial(k === 4 || k === 5 ? { map: bt, roughness: 0.6 } : { color: k === 2 ? 0xe9e6e8 : MAG, roughness: 0.6 })));
    box.position.y = -1.4; g.add(box);
    const tg = new THREE.PlaneGeometry(2, 2.6, 16, 16), tissue = new THREE.Mesh(tg, new THREE.MeshStandardMaterial({ color: 0xffffff, side: THREE.DoubleSide, roughness: 0.9 }));
    const base = tg.attributes.position.array.slice(); g.add(tissue);
    return { scene, camera, update(t) {
      g.rotation.set(0.35, -0.6 + Math.sin(t * 0.8) * 0.25, 0);
      const pull = Math.min(1, Math.max(0, (t - c.wipe) / 0.3)); tissue.position.set(0, -0.2 + pull * 1.6, 0);
      const p = tg.attributes.position.array;
      for (let i = 0; i < p.length; i += 3) { const bx = base[i], by = base[i + 1]; const k = (by + 1.3) / 2.6;
        p[i + 2] = Math.sin(bx * 2 + t * 7) * 0.25 * k + Math.sin(by * 3 + t * 5) * 0.12 * k; p[i] = bx * (1 - 0.3 * (1 - k)); }
      tg.attributes.position.needsUpdate = true; tg.computeVertexNormals();
    } };
  },
  logo(c) {       // the end: SPIN / BOUT U in 3D, turning
    const scene = new THREE.Scene(), camera = cam(34, 18); lights(scene);
    const g = new THREE.Group(); scene.add(g);
    const a = text3d("SPIN", 2.6, 0.9, MAG, WHT); a.position.y = 1.5; g.add(a);
    const b = text3d("BOUT U", 2.2, 0.9, WHT, MAG); b.position.y = -1.3; g.add(b);
    return { scene, camera, update(t) {
      const k = back(t / 0.35); g.scale.setScalar(Math.max(0.001, k)); g.rotation.y = Math.sin(t * 0.9) * 0.6; g.rotation.x = 0.12 + Math.sin(t * 0.6) * 0.08;
    } };
  },
};

const built = {};
window.__g3dCanvas = canvas;
window.__g3dResize = (n) => renderer.setSize(n, n, false);
function draw(T) {
  T = Math.floor(T * FPS + 1e-6) / FPS;
  const e = (window.G3D || []).find((s) => T >= s.t0 && T < s.t1);
  if (!e) { canvas.style.display = "none"; return; }
  if (!built[e.id]) built[e.id] = KINDS[e.kind](e.cues || {});
  const holder = document.getElementById("g3-" + e.id);
  if (holder && canvas.parentNode !== holder) holder.appendChild(canvas);
  canvas.style.display = "block";
  const b = built[e.id];
  if (e.bg) renderer.setClearColor(new THREE.Color(e.bg), 1); else renderer.setClearColor(0x000000, 0);
  b.update(T - e.t0, T);
  renderer.render(b.scene, b.camera);
}
window.__g3dDraw = draw;
// pre-build every scene now, so the first frame of each is not slower or different
(window.G3D || []).forEach((e) => { if (!built[e.id]) built[e.id] = KINDS[e.kind](e.cues || {}); });
draw(window.__g3dT || 0);
