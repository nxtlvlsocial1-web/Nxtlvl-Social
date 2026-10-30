// The pixel actors of the Reel: Rook, Vesper, Dash and the Claude crab, drawn cell by cell on a 2D canvas as a pure
// function of time t (HyperFrames' hf-seek). As in the reference, a character changes pose or place by breaking into
// pixels and reforming; it bobs, hops with squash and stretch, coin-spins, leaves a smear trail when it moves fast and
// flashes white when hit. The schedule (shots) and the pose maps come from window.CS_T (written by build/generate.py).
const T = window.CS_T;
const SP = T.sprites, ACT = T.actors;
const W = 1080, H = 1920;
const cv = document.getElementById("actors"); cv.width = W; cv.height = H;
const g = cv.getContext("2d");
const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lin = (t, a, b) => cl((t - a) / (b - a));
const eOut = (x) => 1 - Math.pow(1 - x, 3);
const eIn = (x) => x * x * x;
const eInOut = (x) => (x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const eBack = (x) => { const c1 = 2.2, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const IN = .32, OUT = .3;   // pixel assemble / dissolve durations

function greyOf(hex) {
  const r = parseInt(hex.slice(1, 3), 16), gg = parseInt(hex.slice(3, 5), 16), b = parseInt(hex.slice(5, 7), 16);
  const v = Math.round((.3 * r + .59 * gg + .11 * b) * .55 + 70);
  return `rgb(${v},${v},${v + 6})`;
}

// where the shot's feet are at time t (before bob/hop)
function basePos(s, t) {
  let x = s.x, y = s.y;
  if (s.mv) {
    const [m0, m1, x2, y2, ease] = s.mv;
    const k = ease === "lin" ? lin(t, m0, m1) : eInOut(lin(t, m0, m1));
    x += (x2 - s.x) * k; y += (y2 - s.y) * k;
  }
  if (s.enter === "drop") y -= 1100 * (1 - eOut(lin(t, s.a, s.a + .32)));
  if (s.enter === "slideL") x -= 900 * (1 - eOut(lin(t, s.a, s.a + .3)));
  if (s.enter === "slideR") x += 900 * (1 - eOut(lin(t, s.a, s.a + .3)));
  for (const [k0, dx, dy, dur = .38] of s.kicks || []) {      // a lunge (or a toss): out and back
    const k = lin(t, k0 - .08, k0 - .08 + dur);
    const f = k < .3 ? eOut(k / .3) : 1 - eInOut((k - .3) / .7);
    x += dx * f; y += dy * f;
  }
  return [x, y];
}

function drawShot(s, t, si) {
  const sp = SP[s.sp], cs = s.s, seed = si * 7.3;
  let amt = 0;
  if (s.enter === "px") amt = Math.max(amt, 1 - eOut(lin(t, s.a, s.a + IN)));
  if (s.exit === "px") amt = Math.max(amt, eIn(lin(t, s.b - OUT, s.b)));
  let [x, y] = basePos(s, t);
  const ground = y;
  let sx = 1, sy = 1, rot = (s.tilt || 0) * Math.PI / 180;
  // idle life: bob and breathe; hops with squash on landing
  if (s.hop) {
    const [amp, per] = s.hop, ph = ((t - s.a) % per) / per;
    y -= amp * Math.sin(Math.PI * ph);
    const land = Math.max(0, 1 - Math.min(ph, 1 - ph) / .14);
    sy *= 1 - .16 * land; sx *= 1 + .14 * land;
  } else if (s.bob !== 0) {
    y += Math.sin(t * 3.1 + seed) * cs * .18;
    sy *= 1 + .025 * Math.sin(t * 6.2 + seed);
  }
  rot += Math.sin(t * 2.1 + seed) * .03;
  if (s.enter === "pop") { const k = eBack(lin(t, s.a, s.a + .32)); sx *= k; sy *= k; }
  for (const ts of s.spins || []) {
    if (t >= ts && t < ts + .5) sx *= Math.cos(eInOut((t - ts) / .5) * Math.PI * 2);
  }
  for (const ts of s.shakes || []) {
    if (t >= ts && t < ts + .45) { const k = t - ts; x += Math.sin(k * 85) * 16 * Math.exp(-k * 9); rot += Math.sin(k * 60) * .08 * Math.exp(-k * 9); }
  }
  if (s.rolls) for (const ts of s.rolls) if (t >= ts && t < ts + .5) rot += eInOut((t - ts) / .5) * Math.PI * 2;
  let mono = s.mono || null;
  for (const ts of s.hits || []) if (t >= ts && t < ts + .07) mono = "#ffffff";
  const grey = s.grey !== undefined && t >= s.grey;
  const greyK = grey ? lin(t, s.grey, s.grey + .35) : 0;

  // contact shadow
  if (s.shadow !== false && !s.mono) {
    g.save();
    g.globalAlpha = .28 * (1 - amt) * (1 - cl((ground - y) / 400));
    g.fillStyle = "#000";
    g.beginPath(); g.ellipse(x, ground + cs * .2, sp.w * cs * .36, cs * .9, 0, 0, Math.PI * 2); g.fill();
    g.restore();
  }
  // smear trail on fast moves
  if (s.mv && t > s.mv[0] && t < s.mv[1] && !amt) {
    const [px1] = basePos(s, t - .05);
    if (Math.abs(px1 - x) > 25) {
      for (const [dt, al] of [[.05, .22], [.1, .1]]) {
        const [gx, gy] = basePos(s, t - dt);
        cells(sp, cs, gx, gy - (ground - y), sx, sy, rot, s.flip || 1, 0, al, s.smear || "#ffffff", false, 0, seed);
      }
    }
  }
  cells(sp, cs, x, y, sx, sy, rot, s.flip || 1, amt, 1, mono, grey, greyK, seed);
}

function cells(sp, cs, x, y, sx, sy, rot, flip, amt, alpha, mono, grey, greyK, seed) {
  g.save();
  g.translate(x, y); g.rotate(rot); g.scale(sx * flip, sy);
  const ax = sp.ax + .5, h = sp.h;
  const n = sp.cells.length;
  for (let i = 0; i < n; i++) {
    const [cx, cy, col] = sp.cells[i];
    let c = mono || col;
    if (grey && !mono) c = greyK >= 1 ? greyOf(col) : (greyK > hash(i + seed) ? greyOf(col) : col);
    g.fillStyle = c;
    const px0 = (cx - ax) * cs, py0 = (cy - h) * cs;
    if (amt <= .001) {
      g.globalAlpha = alpha;
      g.fillRect(px0, py0, cs + .6, cs + .6);
      continue;
    }
    // broken into 2x2 sub-pixels that fly apart (or fly back together)
    const half = cs / 2;
    for (let q = 0; q < 4; q++) {
      const k = i * 4 + q + seed * 100;
      const an = hash(k) * Math.PI * 2, d = (.35 + hash(k + .37)) * cs * 9 * Math.pow(amt, 1.2);
      const dx = Math.cos(an) * d, dy = Math.sin(an) * d * .75 - amt * cs * 5 * hash(k + .71);
      const sz = half * (1 - .5 * amt);
      g.globalAlpha = alpha * cl(1.15 - amt * amt);
      g.fillRect(px0 + (q % 2) * half + dx, py0 + (q >> 1) * half + dy, sz + .5, sz + .5);
    }
  }
  g.restore();
}

function renderAt(t) {
  g.clearRect(0, 0, W, H);
  ACT.forEach((shots, ai) => {
    shots.forEach((s, si) => {
      if (t < s.a || t >= s.b) return;
      drawShot(s, t, ai * 31 + si);
    });
  });
}

const ready = Promise.resolve().then(() => renderAt(window.__hfThreeTime || 0));
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["csactors"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
