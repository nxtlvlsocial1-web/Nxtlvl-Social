// UDAAN v2: the 3D world (three.js), rendered from HyperFrames time.
// A low-poly floating-island diorama: a girl flies a kite; night falls; walls drop and shatter; the kite climbs past
// three islands (ages 10-14, 15-17, 18-19); the community gathers; a sky full of kites rises.
// Everything is a pure function of t (seeded randomness, no clocks), so any frame can be rendered on its own.
import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { mergeGeometries } from "three/addons/utils/BufferGeometryUtils.js";

const W = 1080, H = 1920;
// ---------- key times (seconds, on the v2 voice track) ----------
const T = {
  dusk: 7.0, snap: 11.0, night: 11.4, silence: 18.0, hope: 20.2, lanterns: 24.14,
  wall1: 25.96, wall2: 27.31, wall3: 28.31, orb: 30.0, crack: 32.5, shatter: 35.40,
  stage1: 36.45, stage2: 41.9, stage3: 46.9, community: 52.0, future: 57.4, kites: 63.0, rise: 68.6, cta: 70.0, end: 74.0,
};

// ---------- helpers ----------
let seed = 20261125;
const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, k) => a + (b - a) * k;
const ss = (a, b, t) => { const k = clamp((t - a) / (b - a)); return k * k * (3 - 2 * k); };
const eo = (k) => 1 - Math.pow(1 - clamp(k), 3); // ease out cubic
const backOut = (k, s = 1.7) => { k = clamp(k) - 1; return k * k * ((s + 1) * k + s) + 1; };
const bounceOut = (k) => {
  k = clamp(k); const n = 7.5625, d = 2.75;
  if (k < 1 / d) return n * k * k;
  if (k < 2 / d) return n * (k -= 1.5 / d) * k + 0.75;
  if (k < 2.5 / d) return n * (k -= 2.25 / d) * k + 0.9375;
  return n * (k -= 2.625 / d) * k + 0.984375;
};
const C = (h) => new THREE.Color(h);
// keyframed values: [[t, v], ...] with v a number, an array or a THREE.Color; smoothstep between neighbours
function track(keys) {
  return (t) => {
    if (t <= keys[0][0]) return keys[0][1];
    for (let i = 1; i < keys.length; i++) {
      if (t <= keys[i][0]) {
        const [t0, a] = keys[i - 1], [t1, b] = keys[i];
        const k = ss(t0, t1, t);
        if (a instanceof THREE.Color) return a.clone().lerp(b, k);
        if (Array.isArray(a)) return a.map((x, j) => lerp(x, b[j], k));
        return lerp(a, b, k);
      }
    }
    return keys[keys.length - 1][1];
  };
}
const std = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.85, metalness: 0, flatShading: true, ...o });

// ---------- renderer ----------
const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: "high-performance", preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(W, H, false);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;

const scene = new THREE.Scene();
scene.fog = new THREE.Fog(0xf4a08f, 12, 55);
const camera = new THREE.PerspectiveCamera(40, W / H, 0.1, 200);

const composer = new EffectComposer(renderer);
composer.setPixelRatio(1);
composer.setSize(W, H);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), 0.42, 0.5, 0.9);
composer.addPass(bloom);
composer.addPass(new OutputPass());

// ---------- sky ----------
const skyU = {
  top: { value: C("#3b2a7a") }, mid: { value: C("#e0658f") }, bot: { value: C("#ffc28a") },
  sunDir: { value: new THREE.Vector3(0.2, 0.1, -1).normalize() }, glow: { value: C("#ffd9a0") }, glowAmt: { value: 1 },
};
const sky = new THREE.Mesh(
  new THREE.SphereGeometry(120, 32, 24),
  new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false, fog: false, uniforms: skyU,
    vertexShader: `varying vec3 vDir; void main(){ vDir = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }`,
    fragmentShader: `uniform vec3 top; uniform vec3 mid; uniform vec3 bot; uniform vec3 sunDir; uniform vec3 glow; uniform float glowAmt; varying vec3 vDir;
      void main(){ float y = vDir.y; vec3 c = mix(bot, mid, smoothstep(-0.15, 0.22, y)); c = mix(c, top, smoothstep(0.22, 0.85, y));
        float s = max(dot(normalize(vDir), normalize(sunDir)), 0.0); c += glow * (pow(s, 12.0) * 0.35 + pow(s, 90.0) * 0.6) * glowAmt;
        gl_FragColor = vec4(c, 1.0); }`,
  }),
);
sky.renderOrder = -1;
scene.add(sky);

// stars
const starGeo = new THREE.BufferGeometry();
{
  const p = [];
  for (let i = 0; i < 700; i++) {
    const th = rnd() * Math.PI * 2, y = 0.05 + rnd() * 0.95, r = Math.sqrt(1 - y * y);
    p.push(Math.cos(th) * r * 100, y * 100, Math.sin(th) * r * 100);
  }
  starGeo.setAttribute("position", new THREE.Float32BufferAttribute(p, 3));
}
const starMat = new THREE.PointsMaterial({ color: 0xffffff, size: 2.2, sizeAttenuation: false, transparent: true, opacity: 0, fog: false, depthWrite: false });
scene.add(new THREE.Points(starGeo, starMat));

// sun and moon
const sun = new THREE.Mesh(new THREE.SphereGeometry(2.4, 32, 16), new THREE.MeshBasicMaterial({ color: 0xfff0c8, fog: false }));
scene.add(sun);
const moon = new THREE.Mesh(new THREE.SphereGeometry(1.5, 32, 16), new THREE.MeshBasicMaterial({ color: 0xdfe6ff, fog: false, transparent: true }));
moon.position.set(-9, 16, -40);
scene.add(moon);

// lights
const hemi = new THREE.HemisphereLight(0xffd1b0, 0x4a2a5a, 1.1);
scene.add(hemi);
const key = new THREE.DirectionalLight(0xffd9a0, 2.2);
key.castShadow = true;
key.shadow.mapSize.set(2048, 2048);
key.shadow.camera.left = -6; key.shadow.camera.right = 6; key.shadow.camera.top = 6; key.shadow.camera.bottom = -6;
key.shadow.camera.near = 1; key.shadow.camera.far = 40;
key.shadow.bias = -0.002; key.shadow.normalBias = 0.06;
scene.add(key, key.target);
const warm = new THREE.PointLight(0xffb050, 0, 6, 1.5); // lanterns / dream glow
warm.position.set(0.6, 0.7, 1.5);
const front = new THREE.PointLight(0xd8d0ff, 0, 16, 1.0); // moonlight on the walls
front.position.set(0, 2.6, 6.8);
scene.add(front);
scene.add(warm);
const leak = new THREE.PointLight(0xffc060, 0, 9, 1.2); // light through the cracks
leak.position.set(0, 1.4, 1.2);
scene.add(leak);

// ---------- islands ----------
function makeIsland(r, depth, grassCol, rockCol, n = 28) {
  const g = new THREE.Group();
  const topGeo = new THREE.CylinderGeometry(r, r * 0.94, 0.32, n, 2);
  const pos = topGeo.attributes.position;
  // displacement is a function of position, so the duplicated cap/seam vertices move together (no creases)
  const nz = (x, z) => Math.sin(x * 3.1 + z * 1.7) * Math.cos(z * 2.7 - x * 1.3);
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i), y = pos.getY(i), z = pos.getZ(i), rr = Math.hypot(x, z);
    if (y > 0.1) pos.setY(i, y + nz(x, z) * 0.025 * clamp(rr / r));
    else { const j = 1 + nz(x * 2, z * 2) * 0.03; pos.setX(i, x * j); pos.setZ(i, z * j); }
  }
  topGeo.computeVertexNormals();
  const grass = new THREE.Mesh(topGeo, std(grassCol, { flatShading: false }));
  grass.position.y = -0.16; grass.receiveShadow = true; grass.castShadow = true;
  const rockGeo = new THREE.ConeGeometry(r * 0.94, depth, n, 4);
  const rp = rockGeo.attributes.position;
  for (let i = 0; i < rp.count; i++) {
    const y = rp.getY(i);
    if (y < depth / 2 - 0.01) { const j = 1 + (rnd() - 0.5) * 0.28; rp.setX(i, rp.getX(i) * j); rp.setZ(i, rp.getZ(i) * j); rp.setY(i, y + (rnd() - 0.5) * 0.12); }
  }
  rockGeo.computeVertexNormals();
  const rock = new THREE.Mesh(rockGeo, std(rockCol));
  rock.rotation.x = Math.PI; rock.position.y = -0.32 - depth / 2; rock.castShadow = true;
  const dirt = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.95, r * 0.94, 0.14, n), std("#8a5a44"));
  dirt.position.y = -0.36;
  g.add(grass, dirt, rock);
  g.userData.grass = grass.material;
  return g;
}
function makeTree(h, col) {
  const g = new THREE.Group();
  const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.06, h * 0.4, 6), std("#6b3f2a"));
  trunk.position.y = h * 0.2; trunk.castShadow = true;
  g.add(trunk);
  for (let i = 0; i < 3; i++) {
    const c = new THREE.Mesh(new THREE.ConeGeometry(h * (0.32 - i * 0.07), h * 0.42, 7), std(col));
    c.position.y = h * (0.42 + i * 0.2); c.castShadow = true;
    g.add(c);
  }
  return g;
}
const main = makeIsland(2.5, 3.2, "#7fbf6a", "#9a6a5a");
scene.add(main);
const trees = [makeTree(1.2, "#4f9a5a"), makeTree(0.9, "#5fae5f"), makeTree(0.7, "#3f8a50")];
trees[0].position.set(1.75, 0, -1.0); trees[1].position.set(-1.7, 0, -0.9); trees[2].position.set(2.0, 0, 0.3);
trees.forEach((t) => main.add(t));
// rocks and a little path of stones
for (let i = 0; i < 9; i++) {
  const s = new THREE.Mesh(new THREE.DodecahedronGeometry(0.06 + rnd() * 0.08, 0), std("#b8a3a0"));
  const a = rnd() * Math.PI * 2, r = 1.2 + rnd() * 1.1;
  s.position.set(Math.cos(a) * r, 0.02, Math.sin(a) * r); s.castShadow = true;
  main.add(s);
}
// flowers that bloom in the "future" scene
const flowers = [];
{
  const cols = ["#ff5a8f", "#ffb627", "#ffffff", "#ff7a1a", "#c77dff"];
  for (let i = 0; i < 46; i++) {
    const f = new THREE.Group();
    const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.14, 4), std("#3f8a50"));
    stem.position.y = 0.07;
    const bloomM = new THREE.Mesh(new THREE.IcosahedronGeometry(0.045, 0), std(cols[i % cols.length], { emissive: cols[i % cols.length], emissiveIntensity: 0.15 }));
    bloomM.position.y = 0.15;
    f.add(stem, bloomM);
    let a, r;
    do { a = rnd() * Math.PI * 2; r = 0.5 + rnd() * 1.85; } while (Math.abs(Math.cos(a) * r + 0.3) < 0.45 && Math.abs(Math.sin(a) * r - 0.3) < 0.45);
    f.position.set(Math.cos(a) * r, 0, Math.sin(a) * r);
    f.userData.t0 = T.future + 0.8 + rnd() * 3.0;
    f.scale.setScalar(0.0001);
    main.add(f);
    flowers.push(f);
  }
}

// clouds
const clouds = [];
{
  const cm = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 1, flatShading: true, transparent: true, opacity: 0.95 });
  for (let i = 0; i < 14; i++) {
    const parts = [];
    const n = 4 + Math.floor(rnd() * 3);
    for (let j = 0; j < n; j++) {
      const s = new THREE.IcosahedronGeometry(0.5 + rnd() * 0.5, 1);
      s.translate(j * 0.55 - n * 0.27, rnd() * 0.25, (rnd() - 0.5) * 0.4);
      parts.push(s);
    }
    const m = new THREE.Mesh(mergeGeometries(parts), cm);
    const side = i % 2 ? 1 : -1;
    m.position.set(side * (4 + rnd() * 6), 1.5 + rnd() * 24, -6 - rnd() * 12);
    m.scale.setScalar(0.8 + rnd() * 1.1);
    m.userData.speed = 0.05 + rnd() * 0.08;
    m.userData.x0 = m.position.x;
    scene.add(m);
    clouds.push(m);
  }
}

// ---------- characters ----------
function makeFigure({ dress = "#ff5a8f", skin = "#c98e68", hair = "#2a1614", h = 1, braid = true, kurta = false }) {
  const g = new THREE.Group();
  const parts = {};
  const legM = std("#3a2440");
  for (const x of [-0.06, 0.06]) {
    const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.042, 0.042, 0.28, 8), legM);
    leg.position.set(x, 0.14, 0); leg.castShadow = true; g.add(leg);
    const shoe = new THREE.Mesh(new THREE.SphereGeometry(0.05, 8, 6), std("#5a2a3a"));
    shoe.position.set(x, 0.02, 0.02); shoe.scale.set(1, 0.6, 1.4); g.add(shoe);
  }
  const body = new THREE.Mesh(kurta ? new THREE.CylinderGeometry(0.13, 0.17, 0.5, 12) : new THREE.CylinderGeometry(0.11, 0.27, 0.48, 14), std(dress));
  body.position.y = 0.27 + 0.24; body.castShadow = true; g.add(body);
  const belt = new THREE.Mesh(new THREE.CylinderGeometry(0.118, 0.118, 0.04, 14), std("#ffb627"));
  belt.position.y = 0.66; if (!kurta) g.add(belt);
  const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.04, 0.08, 8), std(skin));
  neck.position.y = 0.78; g.add(neck);
  const head = new THREE.Group();
  head.position.y = 0.92;
  const face = new THREE.Mesh(new THREE.SphereGeometry(0.15, 22, 16), std(skin, { flatShading: false, roughness: 0.7 }));
  face.castShadow = true;
  const hairCap = new THREE.Mesh(new THREE.SphereGeometry(0.158, 22, 16, 0, Math.PI * 2, 0, Math.PI * 0.56), std(hair, { flatShading: false }));
  hairCap.rotation.x = -0.42;
  head.add(face, hairCap);
  for (const x of [-0.052, 0.052]) {
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.017, 8, 6), new THREE.MeshStandardMaterial({ color: 0x1a0d10, roughness: 0.3 }));
    eye.position.set(x, -0.005, 0.138); head.add(eye);
    const cheek = new THREE.Mesh(new THREE.CircleGeometry(0.022, 10), new THREE.MeshStandardMaterial({ color: 0xff8a8a, roughness: 0.9, transparent: true, opacity: 0.6 }));
    cheek.position.set(x * 1.45, -0.045, 0.132); cheek.rotation.y = x * 4; head.add(cheek);
  }
  if (braid) {
    for (let i = 0; i < 4; i++) {
      const b = new THREE.Mesh(new THREE.SphereGeometry(0.052 - i * 0.007, 10, 8), std(hair));
      b.position.set(0, -0.06 - i * 0.075, -0.13 - i * 0.012); head.add(b);
    }
    const bow = new THREE.Mesh(new THREE.TorusGeometry(0.025, 0.01, 6, 10), std("#ff5a8f"));
    bow.position.set(0, -0.32, -0.17); head.add(bow);
  }
  g.add(head);
  parts.head = head;
  const armM = std(skin);
  for (const side of [-1, 1]) {
    const pivot = new THREE.Group();
    pivot.position.set(side * 0.12, 0.72, 0);
    const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.032, 0.03, 0.3, 8), kurta ? std(dress) : armM);
    arm.position.y = -0.15; arm.castShadow = true;
    const hand = new THREE.Mesh(new THREE.SphereGeometry(0.038, 8, 6), armM);
    hand.position.y = -0.31;
    pivot.add(arm, hand);
    pivot.rotation.z = side * 0.18;
    g.add(pivot);
    parts[side > 0 ? "armR" : "armL"] = pivot;
    parts[side > 0 ? "handR" : "handL"] = hand;
  }
  g.scale.setScalar(h);
  g.userData.parts = parts;
  return g;
}
const girl = makeFigure({ dress: "#ff5a8f" });
girl.position.set(-0.3, 0, 0.35);
girl.rotation.y = 0.35;
main.add(girl);
const GP = girl.userData.parts;
// dupatta: a ribbon that flows from her shoulders
const dupGeo = new THREE.PlaneGeometry(0.62, 0.1, 12, 1);
const dupBase = dupGeo.attributes.position.array.slice();
const dupatta = new THREE.Mesh(dupGeo, std("#ffb627", { side: THREE.DoubleSide, flatShading: false }));
dupatta.position.set(-0.3, 0.7, -0.08);
dupatta.castShadow = true;
dupatta.visible = false; // read as a stick in 3D; kept off

// community figures (appear around her)
const COMMUNITY = [
  { dress: "#2a9d8f", h: 1.45, kurta: true, braid: false, hair: "#1a1010", a: -2.3 },  // परिवार (parent)
  { dress: "#e9c46a", h: 1.4, kurta: false, braid: true, a: -1.45 },                    // शिक्षक (teacher)
  { dress: "#f4f1de", h: 1.5, kurta: true, braid: false, hair: "#d8d8d8", a: -0.55 },   // पंचायत (elder)
  { dress: "#3d5a80", h: 1.15, kurta: true, braid: false, a: 0.45 },                    // लड़के व पुरुष (boy)
  { dress: "#e76f51", h: 1.35, kurta: false, braid: true, a: 1.4 },                     // समुदाय
  { dress: "#7b2cbf", h: 1.3, kurta: true, braid: false, a: 2.4 },                      // और आप
];
const community = COMMUNITY.map((c, i) => {
  const f = makeFigure(c);
  const R = 1.35;
  f.position.set(girl.position.x + Math.sin(c.a) * R, 0, girl.position.z + Math.cos(c.a) * R * 0.85);
  f.lookAt(girl.position.x, 0, girl.position.z);
  f.rotation.y += 0; // face her
  f.userData.h = c.h;
  f.visible = false;
  main.add(f);
  return f;
});
const ringCurve = new THREE.EllipseCurve(0, 0, 1.35, 1.35 * 0.85, 0, Math.PI * 2, false, 0);
const ringPts = ringCurve.getPoints(160).map((p) => new THREE.Vector3(p.x, 0, p.y));
const ringGeo = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(ringPts, true), 200, 0.025, 6, true);
const ring = new THREE.Mesh(ringGeo, new THREE.MeshBasicMaterial({ color: 0xffc84a }));
ring.position.set(girl.position.x, 0.9, girl.position.z);
ring.visible = false;
main.add(ring);

// ---------- kite ----------
function makeKite(cols = ["#ffb627", "#ff3d7f", "#ff7a1a", "#e0245e"], s = 1) {
  const g = new THREE.Group();
  const P = { top: [0, 0.55, 0], right: [0.38, 0, 0], bottom: [0, -0.75, 0], left: [-0.38, 0, 0], c: [0, 0, 0.03] };
  const tri = (a, b, c, col) => {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute("position", new THREE.Float32BufferAttribute([...a, ...b, ...c], 3));
    geo.computeVertexNormals();
    return new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: col, side: THREE.DoubleSide, roughness: 0.6, emissive: col, emissiveIntensity: 0.18 }));
  };
  g.add(tri(P.top, P.c, P.right, cols[0]), tri(P.top, P.left, P.c, cols[1]), tri(P.left, P.bottom, P.c, cols[2]), tri(P.c, P.bottom, P.right, cols[3]));
  const sparM = std("#5a2a3a");
  const sp1 = new THREE.Mesh(new THREE.BoxGeometry(0.018, 1.3, 0.018), sparM); sp1.position.set(0, -0.1, 0.04);
  const sp2 = new THREE.Mesh(new THREE.BoxGeometry(0.76, 0.018, 0.018), sparM); sp2.position.set(0, 0, 0.04);
  g.add(sp1, sp2);
  g.children.forEach((m) => (m.castShadow = true));
  // tail
  const tailGeo = new THREE.BufferGeometry();
  tailGeo.setAttribute("position", new THREE.Float32BufferAttribute(new Array(20 * 3).fill(0), 3));
  const tail = new THREE.Line(tailGeo, new THREE.LineBasicMaterial({ color: 0xfff3e2 }));
  g.add(tail);
  const bows = [];
  for (let i = 0; i < 4; i++) {
    const b = new THREE.Mesh(new THREE.ConeGeometry(0.05, 0.1, 3), std(cols[i % 4]));
    b.rotation.z = Math.PI / 2; g.add(b); bows.push(b);
  }
  g.userData = { tail, bows };
  g.scale.setScalar(s);
  return g;
}
function animTail(k, t, ph = 0) {
  const { tail, bows } = k.userData;
  const p = tail.geometry.attributes.position;
  for (let i = 0; i < 20; i++) {
    const u = i / 19;
    p.setXYZ(i, Math.sin(t * 3.1 + u * 5 + ph) * 0.12 * u, -0.75 - u * 1.25, Math.sin(t * 2.3 + u * 4 + ph) * 0.05 * u);
  }
  p.needsUpdate = true;
  bows.forEach((b, i) => {
    const j = 4 + i * 4;
    b.position.set(p.getX(j), p.getY(j), p.getZ(j));
  });
}
const kite = makeKite(undefined, 0.92);
scene.add(kite);
const stringGeo = new THREE.BufferGeometry();
stringGeo.setAttribute("position", new THREE.Float32BufferAttribute(new Array(32 * 3).fill(0), 3));
const kiteString = new THREE.Line(stringGeo, new THREE.LineBasicMaterial({ color: 0xfff6ea, transparent: true, opacity: 0.9 }));
scene.add(kiteString);
function drawString(a, b, sag) {
  const p = stringGeo.attributes.position;
  for (let i = 0; i < 32; i++) {
    const u = i / 31;
    p.setXYZ(i, lerp(a.x, b.x, u), lerp(a.y, b.y, u) - Math.sin(u * Math.PI) * sag, lerp(a.z, b.z, u));
  }
  p.needsUpdate = true;
}

// a sky of kites for the ending
const KCOLS = [["#ffb627", "#ff3d7f", "#ff7a1a", "#e0245e"], ["#2cc7b6", "#ffffff", "#12968a", "#ffd25a"], ["#c77dff", "#ffb627", "#7b2cbf", "#ff5a8f"],
  ["#ff7a1a", "#ffe066", "#ff3d7f", "#ffb627"], ["#4cc9f0", "#ff5a8f", "#4361ee", "#ffffff"]];
const skyKites = [];
for (let i = 0; i < 34; i++) {
  const k = makeKite(KCOLS[i % KCOLS.length], 0.45 + rnd() * 0.4);
  k.userData.home = new THREE.Vector3((rnd() - 0.5) * 9, 1.8 + rnd() * 6.5, -0.6 - rnd() * 4);
  k.userData.t0 = T.kites + 0.2 + rnd() * 3.2;
  k.userData.ph = rnd() * 6;
  k.visible = false;
  scene.add(k);
  skyKites.push(k);
}

// ---------- dream objects (book, ball, cap) ----------
function glowSprite(col, size) {
  const c = document.createElement("canvas"); c.width = c.height = 128;
  const x = c.getContext("2d");
  const g = x.createRadialGradient(64, 64, 0, 64, 64, 64);
  g.addColorStop(0, "rgba(255,255,255,1)"); g.addColorStop(0.25, col); g.addColorStop(1, "rgba(255,255,255,0)");
  x.fillStyle = g; x.fillRect(0, 0, 128, 128);
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }));
  s.scale.setScalar(size);
  return s;
}
function makeBook() {
  const g = new THREE.Group();
  for (const s of [-1, 1]) {
    const cover = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.02, 0.34), std(s < 0 ? "#e0245e" : "#ff7a1a"));
    cover.position.set(s * 0.13, 0, 0); cover.rotation.z = -s * 0.25;
    const pages = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.03, 0.31), std("#fff8ec"));
    pages.position.set(s * 0.125, 0.025, 0); pages.rotation.z = -s * 0.25;
    g.add(cover, pages);
  }
  return g;
}
function makeBall() {
  const g = new THREE.Group();
  const geo = new THREE.IcosahedronGeometry(0.17, 1);
  const cols = [];
  const pos = geo.attributes.position;
  for (let i = 0; i < pos.count; i += 3) {
    const c = Math.floor(i / 3) % 5 === 0 ? [0.08, 0.6, 0.55] : [1, 1, 1];
    cols.push(...c, ...c, ...c);
  }
  geo.setAttribute("color", new THREE.Float32BufferAttribute(cols, 3));
  g.add(new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, roughness: 0.5 })));
  return g;
}
function makeCap(col = "#2a0f3d", s = 1) {
  const g = new THREE.Group();
  const board = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.03, 0.42), std(col));
  board.rotation.y = Math.PI / 4;
  const base = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.15, 0.12, 12), std(col));
  base.position.y = -0.07;
  const tassel = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.18, 4), std("#ffb627", { emissive: "#ffb627", emissiveIntensity: 0.3 }));
  tassel.position.set(0.2, -0.08, 0);
  const knob = new THREE.Mesh(new THREE.SphereGeometry(0.025, 8, 6), std("#ffb627"));
  knob.position.y = 0.025;
  g.add(board, base, tassel, knob);
  g.scale.setScalar(s);
  return g;
}
const dreams = [
  { obj: makeBook(), t0: 3.12, at: new THREE.Vector3(0.55, 1.55, 0.6), col: "rgba(255,120,150,.9)" },
  { obj: makeBall(), t0: 4.21, at: new THREE.Vector3(1.25, 1.05, 0.9), col: "rgba(90,230,210,.9)" },
  { obj: makeCap(), t0: 5.33, at: new THREE.Vector3(0.95, 2.0, 0.2), col: "rgba(255,200,90,.9)" },
];
dreams.forEach((d) => {
  const g = new THREE.Group();
  const halo = glowSprite(d.col, 0.5); halo.material.opacity = 0.7;
  g.add(halo, d.obj);
  g.visible = false;
  main.add(g);
  d.g = g;
});
// a dream orb that is stopped by the walls
const orb = new THREE.Group();
orb.add(new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 12), new THREE.MeshBasicMaterial({ color: 0xffe0a0 })), glowSprite("rgba(255,190,90,.9)", 1.1));
orb.visible = false;
scene.add(orb);

// silence rings
const rings = [0, 1, 2].map((i) => {
  const m = new THREE.Mesh(new THREE.TorusGeometry(0.6 + i * 0.45, 0.012, 6, 90), new THREE.MeshBasicMaterial({ color: 0xc9b6ff, transparent: true, opacity: 0 }));
  m.rotation.x = Math.PI / 2;
  m.position.set(girl.position.x, 0.55, girl.position.z);
  main.add(m);
  return m;
});
// lanterns and a protective ring of light
const lanterns = [];
for (let i = 0; i < 14; i++) {
  const g = new THREE.Group();
  const body = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.07, 0.12, 8), new THREE.MeshBasicMaterial({ color: 0xffd27a }));
  g.add(body, glowSprite("rgba(255,170,70,.9)", 0.32));
  const a = (i / 14) * Math.PI * 2;
  g.userData = { a, r: 1.05 + (i % 2) * 0.25, h: 0.9 + (i % 3) * 0.28, t0: T.lanterns - 0.2 + i * 0.06 };
  g.visible = false;
  main.add(g);
  lanterns.push(g);
}
const shieldGeo = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(new THREE.EllipseCurve(0, 0, 0.95, 0.95, 0, Math.PI * 2).getPoints(120).map((p) => new THREE.Vector3(p.x, 0, p.y)), true), 160, 0.03, 6, true);
const shield = new THREE.Mesh(shieldGeo, new THREE.MeshBasicMaterial({ color: 0xffc84a }));
shield.position.set(girl.position.x, 0.08, girl.position.z);
shield.visible = false;
main.add(shield);

// ---------- walls (text drawn on canvas with the Devanagari font) ----------
const WALLS = ["लैंगिक भेदभाव", "बाल विवाह", "शिक्षा से दूरी"];
const COLS = 6, ROWS = 2, WW = 3.1, WH = 0.86, WD = 0.34;
const wallY = [0.43, 1.33, 2.23];
const chunks = [];
const wallGroups = [];
function wallTextures(text, k) {
  const c = document.createElement("canvas"); c.width = 1024; c.height = 284;
  const x = c.getContext("2d");
  const g = x.createLinearGradient(0, 0, 0, 284);
  g.addColorStop(0, "#56456c"); g.addColorStop(0.55, "#342649"); g.addColorStop(1, "#22172f");
  x.fillStyle = g; x.fillRect(0, 0, 1024, 284);
  let s = 77 + k * 13;
  const r2 = () => ((s = (s * 16807) % 2147483647) / 2147483647);
  for (let i = 0; i < 900; i++) { x.fillStyle = `rgba(${r2() > 0.5 ? 255 : 0},${r2() > 0.5 ? 255 : 0},255,${0.03 + r2() * 0.05})`; x.fillRect(r2() * 1024, r2() * 284, 2 + r2() * 5, 2 + r2() * 5); }
  x.font = '800 150px "Baloo 2"';
  x.textAlign = "center"; x.textBaseline = "middle";
  x.shadowColor = "rgba(0,0,0,.55)"; x.shadowBlur = 18; x.shadowOffsetY = 6;
  x.fillStyle = "#f3e8fb";
  x.fillText(text, 512, 158);
  const map = new THREE.CanvasTexture(c);
  map.colorSpace = THREE.SRGBColorSpace;
  map.anisotropy = 4;
  // cracks (emissive)
  const e = document.createElement("canvas"); e.width = 1024; e.height = 284;
  const y = e.getContext("2d");
  y.fillStyle = "#000"; y.fillRect(0, 0, 1024, 284);
  y.strokeStyle = "#fff"; y.lineWidth = 7; y.lineJoin = "round"; y.lineCap = "round";
  y.shadowColor = "#fff"; y.shadowBlur = 14;
  for (let j = 0; j < 5; j++) {
    let px = 120 + j * 190 + r2() * 60, py = 0;
    y.beginPath(); y.moveTo(px, py);
    while (py < 284) { px += (r2() - 0.5) * 70; py += 30 + r2() * 40; y.lineTo(px, py); }
    y.stroke();
  }
  const emap = new THREE.CanvasTexture(e);
  return { map, emap };
}
function buildWalls() {
  WALLS.forEach((txt, k) => {
    const { map, emap } = wallTextures(txt, k);
    const grp = new THREE.Group();
    grp.position.set(0, wallY[k], 2.3);
    const sideM = std("#2e2242");
    for (let r = 0; r < ROWS; r++) {
      for (let c = 0; c < COLS; c++) {
        const w = WW / COLS, h = WH / ROWS;
        const m = map.clone(); m.repeat.set(1 / COLS, 1 / ROWS); m.offset.set(c / COLS, r / ROWS); m.needsUpdate = true;
        const em = emap.clone(); em.repeat.copy(m.repeat); em.offset.copy(m.offset); em.needsUpdate = true;
        const front = new THREE.MeshStandardMaterial({ map: m, emissiveMap: em, emissive: 0xffc060, emissiveIntensity: 0, roughness: 0.9 });
        const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, WD), [sideM, sideM, sideM, sideM, front, sideM]);
        const lx = -WW / 2 + w * (c + 0.5), ly = -WH / 2 + h * (r + 0.5);
        mesh.position.set(lx, ly, 0);
        mesh.castShadow = true; mesh.receiveShadow = true;
        mesh.userData = {
          p0: new THREE.Vector3(lx, ly, 0), front,
          v: new THREE.Vector3(lx * 1.9 + (rnd() - 0.5) * 1.8, 1.4 + rnd() * 2.4 + k * 0.4, 0.3 + rnd() * 1.6),
          w: new THREE.Vector3((rnd() - 0.5) * 9, (rnd() - 0.5) * 9, (rnd() - 0.5) * 9),
        };
        grp.add(mesh);
        chunks.push({ mesh, k });
      }
    }
    grp.visible = false;
    scene.add(grp);
    wallGroups.push(grp);
  });
}

// ---------- stage islands (ages) ----------
const STAGE_POS = [new THREE.Vector3(-1.6, 8, -2.5), new THREE.Vector3(1.7, 15, -3.5), new THREE.Vector3(-1.2, 22, -4.5)];
const stageIsl = STAGE_POS.map((p, i) => {
  const isl = makeIsland(1.35, 1.9, ["#8fd06a", "#6fc7a8", "#ffc46b"][i], "#9a6a5a", 20);
  isl.position.copy(p);
  scene.add(isl);
  return isl;
});
{
  // 10-14: a school and a big open book
  const school = new THREE.Group();
  const walls = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.42, 0.5), std("#fff1df")); walls.position.y = 0.21;
  const roof = new THREE.Mesh(new THREE.ConeGeometry(0.55, 0.32, 4), std("#e0245e")); roof.position.y = 0.58; roof.rotation.y = Math.PI / 4; roof.scale.set(1, 1, 0.75);
  const door = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.22, 0.02), std("#7a3a2a")); door.position.set(0, 0.11, 0.26);
  const flag = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.1, 0.01), std("#ff7a1a")); flag.position.set(0.08, 0.92, 0);
  const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.4, 4), std("#ddd")); pole.position.set(0, 0.86, 0);
  school.add(walls, roof, door, pole, flag);
  school.children.forEach((m) => (m.castShadow = true));
  school.position.set(0.35, 0, -0.25);
  stageIsl[0].add(school);
  const book = makeBook(); book.scale.setScalar(1.8); book.position.set(-0.5, 0.5, 0.35); book.rotation.x = 0.5;
  stageIsl[0].add(book); stageIsl[0].userData.float = book;
  const t1 = makeTree(0.7, "#4f9a5a"); t1.position.set(-0.8, 0, -0.5); stageIsl[0].add(t1);
  // 15-17: a laptop and a shield
  const lap = new THREE.Group();
  const baseL = new THREE.Mesh(new RoundedBoxGeometry(0.6, 0.04, 0.42, 2, 0.015), std("#3a3f55")); baseL.position.y = 0.02;
  const scr = new THREE.Mesh(new RoundedBoxGeometry(0.6, 0.4, 0.03, 2, 0.012), std("#3a3f55"));
  scr.position.set(0, 0.22, -0.2); scr.rotation.x = -0.25;
  const glowS = new THREE.Mesh(new THREE.PlaneGeometry(0.52, 0.32), new THREE.MeshBasicMaterial({ color: 0x5ff0dc }));
  glowS.position.set(0, 0.22, -0.18); glowS.rotation.x = -0.25;
  lap.add(baseL, scr, glowS); lap.position.set(-0.25, 0, 0.1); lap.rotation.y = 0.35;
  lap.children.forEach((m) => (m.castShadow = true));
  stageIsl[1].add(lap);
  const sh = new THREE.Shape();
  sh.moveTo(0, 0.3); sh.quadraticCurveTo(0.2, 0.28, 0.26, 0.22); sh.quadraticCurveTo(0.26, -0.12, 0, -0.32); sh.quadraticCurveTo(-0.26, -0.12, -0.26, 0.22); sh.quadraticCurveTo(-0.2, 0.28, 0, 0.3);
  const shieldM = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: 0.06, bevelEnabled: true, bevelSize: 0.02, bevelThickness: 0.02, bevelSegments: 2 }), std("#12968a", { emissive: "#12968a", emissiveIntensity: 0.25 }));
  shieldM.position.set(0.55, 0.75, 0.2); shieldM.castShadow = true;
  stageIsl[1].add(shieldM); stageIsl[1].userData.float = shieldM;
  const t2 = makeTree(0.6, "#3f8a50"); t2.position.set(0.8, 0, -0.5); stageIsl[1].add(t2);
  // 18-19: a graduation cap, coins and a briefcase
  const cap = makeCap("#2a0f3d", 2.1); cap.position.set(0.1, 0.95, 0.1);
  stageIsl[2].add(cap); stageIsl[2].userData.float = cap;
  for (let i = 0; i < 4; i++) {
    const coin = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 0.035, 16), std("#ffc23a", { metalness: 0.4, roughness: 0.4, emissive: "#ffb627", emissiveIntensity: 0.15 }));
    coin.position.set(-0.55, 0.02 + i * 0.037, 0.3); coin.castShadow = true; stageIsl[2].add(coin);
  }
  const brief = new THREE.Mesh(new RoundedBoxGeometry(0.4, 0.28, 0.14, 2, 0.03), std("#8a4b2a"));
  brief.position.set(0.55, 0.14, 0.15); brief.castShadow = true; stageIsl[2].add(brief);
  const handle = new THREE.Mesh(new THREE.TorusGeometry(0.06, 0.015, 6, 12, Math.PI), std("#5a2a1a"));
  handle.position.set(0.55, 0.29, 0.15); stageIsl[2].add(handle);
}

// ---------- camera ----------
// [time, position, target]; smooth between keys
const CAM = [
  [0.0, [1.6, 2.3, 8.2], [0.45, 1.3, 0]],
  [6.9, [1.2, 2.0, 7.2], [0.45, 1.3, 0]],
  [10.8, [-1.8, 1.7, 7.2], [0.2, 1.3, 0]],
  [14.2, [0.0, 4.5, 13.0], [0.0, 0.6, 0]],
  [17.5, [-0.8, 2.6, 9.0], [-0.2, 0.8, 0]],
  [20.0, [-0.3, 2.2, 7.6], [-0.3, 0.9, 0.3]],
  [25.4, [0.6, 2.3, 6.8], [-0.3, 0.95, 0.3]],
  [26.4, [0.0, 1.7, 11.2], [0.0, 1.35, 2.3]],
  [34.9, [0.0, 1.6, 10.2], [0.0, 1.35, 2.3]],
  [35.4, [0.0, 1.6, 10.0], [0.0, 1.4, 2.3]],
  [36.3, [0.4, 1.6, 8.5], [0.0, 3.2, 0.0]],
  // stages: islands sit in the upper half, the card below
  [37.3, [STAGE_POS[0].x + 1.4, STAGE_POS[0].y + 1.0, STAGE_POS[0].z + 8.2], [STAGE_POS[0].x + 0.1, STAGE_POS[0].y - 0.9, STAGE_POS[0].z]],
  [41.9, [STAGE_POS[0].x + 0.8, STAGE_POS[0].y + 1.2, STAGE_POS[0].z + 7.8], [STAGE_POS[0].x + 0.1, STAGE_POS[0].y - 0.9, STAGE_POS[0].z]],
  [42.8, [STAGE_POS[1].x - 1.4, STAGE_POS[1].y + 1.0, STAGE_POS[1].z + 8.2], [STAGE_POS[1].x - 0.1, STAGE_POS[1].y - 0.9, STAGE_POS[1].z]],
  [46.9, [STAGE_POS[1].x - 0.8, STAGE_POS[1].y + 1.2, STAGE_POS[1].z + 7.8], [STAGE_POS[1].x - 0.1, STAGE_POS[1].y - 0.9, STAGE_POS[1].z]],
  [47.8, [STAGE_POS[2].x + 1.4, STAGE_POS[2].y + 1.0, STAGE_POS[2].z + 8.2], [STAGE_POS[2].x + 0.1, STAGE_POS[2].y - 0.9, STAGE_POS[2].z]],
  [51.9, [STAGE_POS[2].x + 0.8, STAGE_POS[2].y + 1.3, STAGE_POS[2].z + 7.8], [STAGE_POS[2].x + 0.1, STAGE_POS[2].y - 0.9, STAGE_POS[2].z]],
  // community: high angle down onto the island
  [52.9, [0.2, 6.4, 9.2], [-0.3, 0.35, 0.3]],
  [57.2, [-0.4, 5.8, 8.6], [-0.3, 0.35, 0.3]],
  // future: low heroic angle
  [58.2, [2.0, 1.1, 6.6], [-0.1, 1.5, 0]],
  [62.8, [1.4, 1.3, 7.2], [-0.1, 1.7, 0]],
  // kites rising
  [64.0, [0.0, 2.4, 10.5], [0.0, 2.8, 0]],
  [68.4, [0.0, 3.2, 11.0], [0.0, 4.0, 0]],
  [70.2, [0.0, 4.6, 10.5], [0.0, 7.5, -2]],
  [74.0, [0.0, 6.0, 10.0], [0.0, 9.5, -3]],
];
const camPos = track(CAM.map(([t, p]) => [t, p]));
const camTgt = track(CAM.map(([t, , g]) => [t, g]));

// ---------- palette over time ----------
const PAL = {
  top: track([[0, C("#3b2a7a")], [6.5, C("#3b2a7a")], [9.8, C("#1b1440")], [11.6, C("#05040f")], [34.6, C("#070616")], [35.6, C("#3d2a8a")], [52, C("#3a5ab8")], [56, C("#3d2a8a")], [60, C("#4a2a7a")], [74, C("#3a1f66")]]),
  mid: track([[0, C("#e0658f")], [6.5, C("#e0658f")], [9.8, C("#6a3a78")], [11.6, C("#10102c")], [22, C("#141232")], [34.6, C("#1a1236")], [35.6, C("#ff6f91")], [52, C("#8fb8ff")], [56, C("#ff7a95")], [60, C("#ff7a7a")], [74, C("#ff6f91")]]),
  bot: track([[0, C("#ffc28a")], [6.5, C("#ffc28a")], [9.8, C("#c0687a")], [11.6, C("#1e1a40")], [22, C("#2a1e46")], [34.6, C("#3a2440")], [35.6, C("#ffd27a")], [52, C("#ffe7c2")], [56, C("#ffd27a")], [74, C("#ffcf70")]]),
  glow: track([[0, C("#ffd9a0")], [9.8, C("#ff9a70")], [11.6, C("#3a4a8a")], [34.6, C("#3a4a8a")], [35.6, C("#fff0c0")], [74, C("#ffe0a0")]]),
  keyCol: track([[0, C("#ffd9a0")], [9.8, C("#ff9a70")], [11.6, C("#9fb4ff")], [34.6, C("#9fb4ff")], [35.6, C("#fff0d0")], [74, C("#ffe8c0")]]),
  keyI: track([[0, 2.3], [9.8, 1.0], [11.6, 0.95], [34.6, 0.95], [35.6, 2.6], [74, 2.5]]),
  hemiS: track([[0, C("#ffd1b0")], [9.8, C("#a07ab0")], [11.6, C("#4a5a9a")], [34.6, C("#4a5a9a")], [35.6, C("#ffe0c0")], [74, C("#ffe0c0")]]),
  hemiG: track([[0, C("#4a2a5a")], [9.8, C("#2a1838")], [11.6, C("#0a0a18")], [34.6, C("#0a0a18")], [35.6, C("#6a3a5a")], [74, C("#6a3a5a")]]),
  hemiI: track([[0, 1.15], [9.8, 0.75], [11.6, 0.75], [34.6, 0.75], [35.6, 1.25], [74, 1.25]]),
  fog: track([[0, C("#f2a08f")], [9.8, C("#6a3a6a")], [11.6, C("#0c0b20")], [34.6, C("#1a1236")], [35.6, C("#ffb08a")], [52, C("#d8e4ff")], [56, C("#ffb08a")], [74, C("#ffb08a")]]),
  grass: track([[0, C("#7fbf6a")], [9.8, C("#4f7d5a")], [11.6, C("#24384a")], [34.6, C("#2c4050")], [35.6, C("#8fd06a")], [74, C("#8fd06a")]]),
  stars: track([[0, 0], [9.4, 0], [11.6, 1], [34.6, 1], [35.6, 0]]),
  moon: track([[0, 0], [10.4, 0], [11.8, 1], [34.6, 1], [35.4, 0]]),
  exposure: track([[0, 1.0], [11.6, 1.05], [35.6, 1.0], [74, 1.0]]),
};
// sun path: dawn low, sets at dusk, rises fast at the reveal
const sunPos = track([[0, [10, 2.6, -38]], [6.5, [10, 1.8, -38]], [10.4, [10, -9, -38]], [35.3, [0, -9, -38]], [36.4, [0, 6.5, -38]], [52, [6, 14, -38]], [56.5, [16, 3.4, -30]], [63, [16, 3.4, -30]], [64.5, [15, 4, -38]], [74, [15, 4, -38]]]);

// ---------- render ----------
const tmpV = new THREE.Vector3(), tmpA = new THREE.Vector3(), tmpB = new THREE.Vector3();
const labels = Array.from(document.querySelectorAll("[data-follow]"));
function project(obj, yOff) {
  obj.getWorldPosition(tmpV);
  tmpV.y += yOff;
  tmpV.project(camera);
  return [(tmpV.x + 1) / 2 * W, (1 - tmpV.y) / 2 * H];
}

function renderAt(t) {
  // palette
  skyU.top.value.copy(PAL.top(t)); skyU.mid.value.copy(PAL.mid(t)); skyU.bot.value.copy(PAL.bot(t)); skyU.glow.value.copy(PAL.glow(t));
  const sp = sunPos(t);
  sun.position.set(sp[0], sp[1], sp[2]);
  skyU.sunDir.value.set(sp[0], sp[1] + 2, sp[2]).normalize();
  skyU.glowAmt.value = clamp((sp[1] + 6) / 6);
  sun.visible = sp[1] > -3;
  moon.material.opacity = PAL.moon(t); moon.visible = moon.material.opacity > 0.01;
  starMat.opacity = PAL.stars(t);
  key.color.copy(PAL.keyCol(t)); key.intensity = PAL.keyI(t);
  const night = PAL.moon(t);
  tmpA.set(sp[0], Math.max(sp[1], 3), sp[2] * 0.3).lerp(new THREE.Vector3(-4, 9, 3), night);
  key.position.copy(tmpA).normalize().multiplyScalar(14);
  hemi.color.copy(PAL.hemiS(t)); hemi.groundColor.copy(PAL.hemiG(t)); hemi.intensity = PAL.hemiI(t);
  scene.fog.color.copy(PAL.fog(t));
  main.userData.grass.color.copy(PAL.grass(t));
  renderer.toneMappingExposure = PAL.exposure(t);

  clouds.forEach((c) => { c.position.x = c.userData.x0 + Math.sin(t * c.userData.speed) * 1.5 + t * c.userData.speed * 0.3; });

  // ---- girl ----
  const grown = 1 + 0.12 * ss(T.future, T.future + 3, t);
  girl.scale.setScalar(grown);
  // right arm: up holding the string, down at night, up again when the kite returns
  const armUp = 1 - ss(T.snap + 0.3, T.snap + 1.2, t) + ss(T.community - 0.2, T.community + 0.6, t);
  GP.armR.rotation.z = lerp(0.18, 2.45, clamp(armUp)) + Math.sin(t * 1.7) * 0.05 * armUp;
  GP.armL.rotation.z = -0.18 - 0.25 * ss(T.future, T.future + 1.5, t) - Math.sin(t * 1.3) * 0.03;
  GP.head.rotation.x = 0.28 * ss(15.5, 17.5, t) * (1 - ss(T.hope, T.hope + 1.5, t)) - 0.12 * clamp(armUp);
  girl.rotation.y = 0.35 + 0.25 * ss(T.community - 0.5, T.community + 0.5, t) * (1 - ss(T.future - 0.5, T.future + 0.5, t));
  {
    const p = dupGeo.attributes.position;
    for (let i = 0; i < p.count; i++) {
      const x0 = dupBase[i * 3], y0 = dupBase[i * 3 + 1];
      const u = (x0 + 0.31) / 0.62;
      p.setXYZ(i, -x0 * 0.9 - 0.25, y0 + Math.sin(t * 3 + u * 4) * 0.04 * u - u * 0.06, -0.05 - u * 0.25 + Math.sin(t * 2.2 + u * 3) * 0.05 * u);
    }
    p.needsUpdate = true; dupGeo.computeVertexNormals();
  }

  // ---- kite ----
  GP.handR.getWorldPosition(tmpB);
  let kiteVisible = true, stringOn = true, sag = 0.35;
  const bob = (s) => [Math.sin(t * 1.3) * 0.14 * s, Math.sin(t * 0.9 + 1) * 0.16 * s];
  if (t < T.snap) {
    const [bx, by] = bob(1);
    kite.position.set(1.95 + bx, 2.45 + by, -0.6);
    kite.rotation.set(0.12, -0.3, Math.sin(t * 1.1) * 0.14);
    if (t > 7.2) kite.rotation.z += Math.sin(t * 9) * 0.06 * ss(7.2, 9, t); // trembling at dusk
  } else if (t < T.snap + 2.4) {
    const k = (t - T.snap) / 2.4;
    kite.position.set(1.95 + k * 1.8, 2.45 - k * k * 7.5, -0.6 - k * 1.5);
    kite.rotation.set(0.12 + k * 3, -0.3 + k * 2, k * 5);
    stringOn = false;
  } else if (t < T.shatter) {
    kiteVisible = false; stringOn = false;
  } else if (t < T.stage1) {
    const k = eo((t - T.shatter) / 1.0);
    kite.position.set(lerp(0.4, 0.1, k), lerp(-1.5, 2.9, k), 1.6);
    kite.rotation.set(0.1, Math.sin(t * 1.4) * 0.15, Math.sin(t * 1.1) * 0.12);
    stringOn = false;
  } else if (t < T.community) {
    // climbs past the stage islands, staying just ahead of the camera
    const tg = camTgt(t);
    kite.position.set(tg[0] + 1.55 + Math.sin(t * 1.3) * 0.12, tg[1] + 2.2 + Math.sin(t * 0.9) * 0.15, tg[2] + 1.2);
    kite.rotation.set(0.12, -0.3, Math.sin(t * 1.1) * 0.14);
    stringOn = false;
  } else if (t < T.rise) {
    const [bx, by] = bob(1);
    const back = eo((t - T.community) / 1.2);
    kite.position.set(1.95 + bx, lerp(6, 2.55, back) + by, -0.6);
    kite.rotation.set(0.12, -0.3, Math.sin(t * 1.1) * 0.14);
    stringOn = t > T.community + 0.3;
    sag = 0.3;
  } else {
    const k = ss(T.rise, T.rise + 2.2, t);
    const [bx, by] = bob(1);
    kite.position.set(1.95 + bx - k * 1.2, 2.55 + by + k * 7.5, -0.6 - k * 2.5);
    kite.rotation.set(0.12 - k * 0.3, -0.3, Math.sin(t * 1.1) * 0.14);
    stringOn = k < 0.05;
  }
  kite.visible = kiteVisible;
  animTail(kite, t);
  kiteString.visible = stringOn && kiteVisible;
  if (kiteString.visible) {
    tmpA.set(0, -0.7, 0).applyMatrix4(kite.matrixWorld.copy(kite.matrix.compose(kite.position, kite.quaternion, kite.scale)));
    drawString(tmpB, tmpA, sag);
  }
  // broken string dangling from her hand right after the snap
  if (t >= T.snap && t < T.snap + 1.0) {
    kiteString.visible = true;
    tmpA.copy(tmpB).add(new THREE.Vector3(0.15, -0.6 * ss(T.snap, T.snap + 0.6, t) - 0.05, 0.05));
    drawString(tmpB, tmpA, 0.05);
    kiteString.material.opacity = 0.9 * (1 - ss(T.snap + 0.5, T.snap + 1.0, t));
  } else kiteString.material.opacity = 0.9;

  // ---- dream objects ----
  dreams.forEach((d, i) => {
    const a = t - d.t0;
    d.g.visible = a > 0 && t < 10.5;
    if (!d.g.visible) return;
    const s = backOut(a / 0.55) * (1 - ss(8.6, 10.2, t));
    d.g.scale.setScalar(Math.max(0.0001, s));
    d.g.position.set(d.at.x, d.at.y + Math.sin(t * 1.6 + i) * 0.06 - (1 - eo(a / 0.6)) * 0.8 + ss(8.6, 10.2, t) * 0.8, d.at.z);
    d.obj.rotation.set(0.3 + Math.sin(t + i) * 0.2, t * 0.7 + i, 0);
  });
  warm.intensity = 1.0 * clamp(ss(3.0, 3.6, t) * (1 - ss(8.6, 10, t))) + 3.5 * ss(T.lanterns - 0.3, T.lanterns + 0.8, t) * (1 - ss(25.6, 26.4, t));
  front.intensity = 9 * ss(T.wall1 - 0.3, T.wall1 + 0.3, t) * (1 - ss(T.shatter, T.shatter + 0.5, t));

  // ---- silence rings ----
  rings.forEach((r, i) => {
    const a = clamp((t - T.silence - i * 0.12) / 1.3);
    r.material.opacity = Math.sin(a * Math.PI) * 0.85;
    r.scale.setScalar(1.25 - a * 1.15);
    r.visible = a > 0 && a < 1;
  });

  // ---- lanterns + shield ----
  lanterns.forEach((l) => {
    const a = clamp((t - l.userData.t0) / 1.2);
    l.visible = a > 0 && t < 26.2;
    const ang = l.userData.a + t * 0.25;
    l.position.set(girl.position.x + Math.cos(ang) * l.userData.r, lerp(0.05, l.userData.h, eo(a)) + Math.sin(t * 2 + l.userData.a) * 0.05, girl.position.z + Math.sin(ang) * l.userData.r);
    l.scale.setScalar(Math.max(0.0001, eo(a * 2) * (1 - ss(25.6, 26.2, t))));
  });
  shield.visible = t > T.lanterns && t < 26.2;
  if (shield.visible) {
    const cnt = shieldGeo.index.count;
    shield.geometry.setDrawRange(0, Math.floor((cnt / 6) * ss(T.lanterns, T.lanterns + 1.2, t)) * 6);
    shield.scale.setScalar(1 + 0.04 * Math.sin(t * 4));
  }

  // ---- walls ----
  const WT = [T.wall1, T.wall2, T.wall3];
  wallGroups.forEach((g, k) => {
    const a = (t - WT[k]) / 0.5;
    g.visible = a > 0 && t < T.shatter + 2.2;
    g.position.y = wallY[k] + (1 - bounceOut(a)) * 5.5;
  });
  // camera shake on impacts
  let shake = 0;
  WT.forEach((w) => { const d = t - w - 0.18; if (d > 0 && d < 0.35) shake += (1 - d / 0.35) * 0.06; });
  // cracks glow, then everything flies apart
  const crackK = ss(T.crack, T.shatter - 0.15, t);
  const flick = 0.85 + 0.15 * Math.sin(t * 37);
  leak.intensity = 14 * crackK * flick * (1 - ss(T.shatter, T.shatter + 0.6, t));
  if (t > T.shatter - 0.6 && t < T.shatter) shake += 0.025 * Math.sin(t * 60);
  chunks.forEach(({ mesh }) => {
    const u = mesh.userData;
    u.front.emissiveIntensity = 3.2 * crackK * flick;
    const d = t - T.shatter;
    if (d <= 0) { mesh.position.copy(u.p0); mesh.rotation.set(0, 0, 0); return; }
    mesh.position.set(u.p0.x + u.v.x * d, u.p0.y + u.v.y * d - 4.5 * d * d, u.p0.z + u.v.z * d);
    mesh.rotation.set(u.w.x * d, u.w.y * d, u.w.z * d);
  });
  // the dream orb that cannot rise
  {
    const a = (t - T.orb) / 1.6;
    orb.visible = a > 0 && a < 1.4;
    const y = a < 0.55 ? lerp(0.35, 2.15, eo(a / 0.55)) : 2.15 - bounceOut((a - 0.55) / 0.5) * 1.5;
    orb.position.set(0.45, y, 2.62);
    orb.scale.setScalar(Math.max(0.0001, 1 - ss(0.9, 1.4, a)));
  }

  // ---- stage islands ----
  stageIsl.forEach((s, i) => {
    s.rotation.y = Math.sin(t * 0.25 + i) * 0.12;
    s.position.y = STAGE_POS[i].y + Math.sin(t * 0.8 + i) * 0.08;
    const f = s.userData.float;
    if (f) { f.position.y = (i === 2 ? 0.95 : i === 1 ? 0.75 : 0.5) + Math.sin(t * 1.5 + i) * 0.06; f.rotation.y = Math.sin(t * 0.8 + i) * 0.45; }
    s.visible = t > T.shatter && t < T.community + 1.5;
  });

  // ---- community ----
  community.forEach((f, i) => {
    const t0 = [52.27, 53.12, 54.08, 54.7, 55.76, 56.6][i];
    const a = (t - t0) / 0.5;
    f.visible = a > 0;
    f.scale.setScalar(Math.max(0.0001, backOut(a, 2.2) * f.userData.h * (1 - ss(57.3, 57.9, t))));
    if (t > 57.95) f.visible = false;
    const P = f.userData.parts;
    const hold = ss(56.6, 57.2, t);
    P.armL.rotation.z = -0.18 - hold * 0.9; P.armR.rotation.z = 0.18 + hold * 0.9;
  });
  ring.visible = t > 56.4 && t < 57.9;
  if (ring.visible) {
    ring.geometry.setDrawRange(0, Math.floor((ringGeo.index.count / 6) * ss(56.4, 57.4, t)) * 6);
  }

  // ---- flowers ----
  flowers.forEach((f) => { f.scale.setScalar(Math.max(0.0001, backOut((t - f.userData.t0) / 0.5, 2.4))); });

  // ---- sky of kites ----
  skyKites.forEach((k, i) => {
    const a = (t - k.userData.t0) / 2.6;
    k.visible = a > 0;
    if (!k.visible) return;
    const h = k.userData.home, up = ss(T.rise + i * 0.02, T.rise + 2.4, t);
    k.position.set(h.x + Math.sin(t * 0.9 + k.userData.ph) * 0.2, lerp(-4, h.y, eo(a)) + up * (5 + (i % 5)) + Math.sin(t * 1.2 + k.userData.ph) * 0.15, h.z);
    k.rotation.set(0.1, Math.sin(t * 0.7 + k.userData.ph) * 0.3, Math.sin(t * 1.1 + k.userData.ph) * 0.2);
    animTail(k, t, k.userData.ph);
  });

  // ---- camera ----
  const cp = camPos(t), ct = camTgt(t);
  camera.position.set(cp[0] + Math.sin(t * 47) * shake, cp[1] + Math.cos(t * 53) * shake, cp[2]);
  camera.lookAt(ct[0], ct[1], ct[2]);
  camera.updateMatrixWorld();

  // ---- HTML labels that follow 3D objects ----
  labels.forEach((el) => {
    const [kind, idx] = el.dataset.follow.split(":");
    const obj = kind === "dream" ? dreams[+idx].g : community[+idx];
    if (!obj.visible) { el.style.visibility = "hidden"; return; }
    const [x, y] = project(obj, kind === "dream" ? -0.32 : 1.25 * obj.userData.h);
    el.style.visibility = "visible";
    el.style.left = `${x}px`;
    el.style.top = `${y}px`;
  });

  composer.render();
}

// ---------- build, then render from HyperFrames time ----------
let built = false;
async function build() {
  await Promise.all([document.fonts.load('800 150px "Baloo 2"'), document.fonts.ready]);
  buildWalls();
  built = true;
  renderAt(window.__hfThreeTime || 0);
}
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["udaan-3d"] = build();
window.addEventListener("hf-seek", (e) => { if (built) renderAt(e.detail.time); });
window.__udaanRender = (t) => renderAt(t); // for local debugging only
