// Deterministic helpers: seeded randomness, easing, interpolation. No clocks, no Math.random.

export function rng(seed) {
  let a = seed >>> 0;
  return function () {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
export const lerp = (a, b, t) => a + (b - a) * t;
export const invLerp = (a, b, v) => clamp((v - a) / (b - a));
export const smooth = (t) => {
  t = clamp(t);
  return t * t * (3 - 2 * t);
};
export const DEG = Math.PI / 180;

export const ease = {
  linear: (t) => clamp(t),
  in: (t) => clamp(t) ** 2,
  out: (t) => 1 - (1 - clamp(t)) ** 2,
  inOut: (t) => smooth(t),
  in3: (t) => clamp(t) ** 3,
  out3: (t) => 1 - (1 - clamp(t)) ** 3,
  inOut3: (t) => {
    t = clamp(t);
    return t < 0.5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2;
  },
  outBack: (t) => {
    t = clamp(t);
    const c1 = 1.70158, c3 = c1 + 1;
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2;
  },
};

// window of local time: 0 before a, 1 after b, eased between
export const win = (u, a, b, e = ease.inOut) => e(invLerp(a, b, u));

export function lerp3(a, b, t) {
  return [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)];
}

// piecewise track: [[t, value], ...] where value is a number or array. Eased per segment.
export function track(keys, u, e = ease.inOut) {
  if (u <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) {
    if (u <= keys[i][0]) {
      const [t0, v0] = keys[i - 1];
      const [t1, v1, segEase] = keys[i];
      const k = (segEase || e)((u - t0) / (t1 - t0));
      return Array.isArray(v0) ? v0.map((x, j) => lerp(x, v1[j], k)) : lerp(v0, v1, k);
    }
  }
  return keys[keys.length - 1][1];
}

// smooth deterministic "handheld" wobble
export function wobble(t, seed = 0, amp = 1) {
  const s = seed * 1.7;
  return [
    amp * (Math.sin(t * 1.3 + s) * 0.6 + Math.sin(t * 2.9 + s * 2.1) * 0.3 + Math.sin(t * 5.3 + s) * 0.1),
    amp * (Math.sin(t * 1.1 + s * 1.3) * 0.6 + Math.sin(t * 2.3 + s * 0.7) * 0.3 + Math.sin(t * 4.7 + s) * 0.1),
    amp * (Math.sin(t * 0.9 + s * 0.5) * 0.5 + Math.sin(t * 2.1 + s * 1.9) * 0.5),
  ];
}

export const hash = (n) => {
  const x = Math.sin(n * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};
