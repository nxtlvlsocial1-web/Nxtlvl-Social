// Halftone spheres, as in the reference: a planet of orange dots shaded by light and a slow-moving noise texture,
// with a dotted halo. Drawn on a 2D canvas as a pure function of time t (hf-seek). Schedule: window.AK_T.spheres
// [{a, b, x, y, r, fx: "squish" | "rise" | "halo", t0, color}].
const T = window.AK_T;
const W = 1920, H = 1080, STEP = 13;
const cv = document.getElementById("ht"); cv.width = W; cv.height = H;
const g = cv.getContext("2d");
const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lin = (t, a, b) => cl((t - a) / (b - a));
const eOut = (x) => 1 - Math.pow(1 - x, 3);
const eIn = (x) => x * x * x;
const eBack = (x) => { const c1 = 1.8, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const hash = (x, y) => { const s = Math.sin(x * 127.1 + y * 311.7) * 43758.5453; return s - Math.floor(s); };
function noise(x, y) {   // value noise
  const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
  const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
  const a = hash(xi, yi), b = hash(xi + 1, yi), c = hash(xi, yi + 1), d = hash(xi + 1, yi + 1);
  return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
}

function sphere(s, t) {
  const k = eBack(lin(t, s.a, s.a + .5)), out = eIn(lin(t, s.b - .25, s.b));
  let r = s.r * Math.max(0, k) * (1 - out);
  let cx = s.x, cy = s.y, sx = 1;
  if (s.fx === "squish" && t >= s.t0) sx = 1 - .45 * eOut(lin(t, s.t0, s.t0 + .35)) + .08 * Math.sin((t - s.t0) * 20) * Math.exp(-(t - s.t0) * 5);
  if (s.fx === "rise") cy = s.y + 420 * (1 - eOut(lin(t, s.a, s.b - .3)));
  const rot = t * .35;
  // halo dots
  const R2 = r * 1.75;
  for (let y = Math.floor((cy - R2) / STEP) * STEP; y < cy + R2; y += STEP) {
    for (let x = Math.floor((cx - R2 * sx * 1.2) / STEP) * STEP; x < cx + R2 * sx * 1.2; x += STEP) {
      const dx = (x - cx) / sx, dy = y - cy, d = Math.hypot(dx, dy);
      if (d < r) {
        const nx = dx / r, ny = dy / r, nz = Math.sqrt(Math.max(0, 1 - nx * nx - ny * ny));
        const lit = cl(.25 + .75 * (-.45 * nx - .55 * ny + .7 * nz));
        const tex = noise(nx * 3 + rot, ny * 3) * .6 + noise(nx * 7 - rot, ny * 7) * .4;
        const v = cl(lit * (.55 + .6 * tex));
        g.fillStyle = v > .72 ? "#ffb070" : v > .45 ? s.color : v > .25 ? "#b8340f" : "#5a1606";
        const rr = STEP * .5 * (.45 + .55 * v);
        g.beginPath(); g.arc(x, y, rr, 0, Math.PI * 2); g.fill();
      } else if (d < R2 && s.fx !== "nohalo") {
        const f = 1 - (d - r) / (R2 - r);
        if (hash(x, y) < f * .9) { g.fillStyle = s.color; g.globalAlpha = f; g.beginPath(); g.arc(x, y, STEP * .22 * f + 1, 0, Math.PI * 2); g.fill(); g.globalAlpha = 1; }
      }
    }
  }
}

function renderAt(t) {
  g.clearRect(0, 0, W, H);
  for (const s of T.spheres) if (t >= s.a && t < s.b) sphere(s, t);
}
const ready = Promise.resolve().then(() => renderAt(window.__hfThreeTime || 0));
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["akht"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
