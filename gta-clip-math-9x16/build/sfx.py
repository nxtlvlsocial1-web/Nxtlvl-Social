"""Sound effects for gta-clip-math-9x16, synthesised here (no third-party audio, nothing to license).

python3 build/sfx.py      (from the project root; needs numpy)
Writes assets/sfx/<name>.wav (each effect once, for reuse) and assets/audio/mix.wav (40 s, 48 kHz stereo),
the track index.html plays. Cue times follow the animation events in index.html; keep them in sync when you
retime a scene. There is no voice or music: the effects sit at a moderate level so a voiceover can go on top.
"""
import os
import wave

import numpy as np

SR = 48000
DUR = 40.0
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(1234)


def env(n, a, d):
    """attack a seconds then exponential decay d (seconds to -60 dB-ish)"""
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-4), np.exp(-(t - a) * 6.9 / d))
    return e


def biquad_bp(x, f0, q):
    """time-varying band-pass (f0 may be an array)"""
    f0 = np.broadcast_to(np.asarray(f0, dtype=float), x.shape)
    y = np.zeros_like(x)
    x1 = x2 = y1 = y2 = 0.0
    for i in range(len(x)):
        w = 2 * np.pi * f0[i] / SR
        al = np.sin(w) / (2 * q)
        b0, b2, a0, a1, a2 = al, -al, 1 + al, -2 * np.cos(w), 1 - al
        yi = (b0 * x[i] + b2 * x2 - a1 * y1 - a2 * y2) / a0
        x2, x1, y2, y1 = x1, x[i], y1, yi
        y[i] = yi
    return y


def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def norm(x, peak=0.9):
    m = np.max(np.abs(x)) or 1
    return x / m * peak


def whoosh(d=0.38, f0=500, f1=5200):
    n = int(d * SR)
    t = np.linspace(0, 1, n)
    noise = rng.standard_normal(n)
    f = f0 * (f1 / f0) ** (np.sin(np.pi * t * 0.5) ** 1.2)
    y = biquad_bp(noise, f, 1.4)
    y *= np.sin(np.pi * t) ** 1.6
    return norm(y, 0.8)


def tick(f=2600, d=0.05):
    n = int(d * SR)
    t = np.arange(n) / SR
    y = np.sin(2 * np.pi * f * t) * env(n, 0.001, d) + 0.4 * rng.standard_normal(n) * env(n, 0.0005, 0.006)
    return norm(y, 0.7)


def pop(f0=320, f1=980, d=0.12):
    n = int(d * SR)
    t = np.arange(n) / SR
    f = f0 + (f1 - f0) * (1 - np.exp(-t / 0.02))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return norm(np.sin(ph) * env(n, 0.002, d), 0.75)


def impact(d=0.9, f0=140, f1=38, big=True):
    n = int(d * SR)
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t / 0.07)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * env(n, 0.002, d)
    click = lowpass(rng.standard_normal(n), 2500) * env(n, 0.0005, 0.05) * 3
    y = np.tanh((body * (1.6 if big else 1.0) + click) * 1.8)
    return norm(y, 0.95 if big else 0.7)


def zip_(d=0.16):
    n = int(d * SR)
    t = np.linspace(0, 1, n)
    y = biquad_bp(rng.standard_normal(n), 1800 + 6000 * t, 2.5) * np.sin(np.pi * t) ** 0.7
    return norm(y, 0.7)


def ding(f=1568, d=0.5):
    n = int(d * SR)
    t = np.arange(n) / SR
    y = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.01 * t) + 0.25 * np.sin(2 * np.pi * f * 3.02 * t)) * env(n, 0.002, d)
    return norm(y, 0.5)


def key(d=0.03):
    n = int(d * SR)
    y = biquad_bp(rng.standard_normal(n), 3200, 3) * env(n, 0.0005, d)
    return norm(y, 0.6)


def drain(d=0.95):
    n = int(d * SR)
    t = np.arange(n) / SR
    f = 900 * (0.25 ** (t / d))
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = (np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.sin(np.pi * t / d) ** 0.5
    return norm(y, 0.45)


FX = {
    "whoosh": whoosh(), "whoosh_short": whoosh(0.24, 900, 6000), "whoosh_long": whoosh(0.5, 300, 4200),
    "tick": tick(), "tick_lo": tick(1700, 0.045), "pop": pop(), "pop_hi": pop(520, 1500, 0.1),
    "impact": impact(), "impact_small": impact(0.5, 180, 60, big=False), "zip": zip_(), "ding": ding(), "key": key(), "drain": drain(),
}

# (time, effect, gain dB, pan -1..1)
CUES = []
add = lambda t, n, g=0.0, p=0.0: CUES.append((t, n, g, p))
# 1. counters spin (accelerating ticks), slam
for k in range(18):
    add(0.05 + 1.45 * (k / 18) ** 0.8, "tick", -16 + k * 0.3, (k % 2) * 0.3 - 0.15)
add(1.6, "whoosh_short", -12)
add(1.73, "impact", -3)
# 2. not $1,000
add(3.0, "whoosh_short", -10, -0.3)
add(3.08, "impact_small", -9)
add(3.69, "zip", -8, 0.2)
add(3.86, "impact_small", -8)  # the $1,000 splits along the strike
add(4.3, "pop", -10)
# 3. wipe, receipt, rows
add(4.86, "whoosh", -6, 0.4)
add(5.12, "whoosh_long", -14, -0.2)
for k, t in enumerate([5.46, 5.66, 5.86, 6.06]):
    add(t, "tick", -11, 0.15 * (k - 1.5))
add(6.28, "pop", -9)
# 4. rate
add(7.0, "impact_small", -8)
add(7.08, "whoosh_short", -12, 0.3)
add(7.2, "pop_hi", -14)
for k in range(14):
    add(7.5 + k * 0.25, "tick_lo", -20)
add(8.89, "pop", -14)
# 5. cap
add(11.0, "whoosh_short", -10, -0.3)
add(11.32, "impact_small", -6)
for k in range(6):
    add(11.1 + k * 0.24, "tick_lo", -19)
add(12.5, "impact", -4)
for k in range(16):
    add(12.6 + 2.3 * (k / 16) ** 0.7, "tick", -22, (k % 2) * 0.4 - 0.2)
# 6. fee
add(15.0, "impact_small", -9)
add(15.36, "zip", -6, 0.3)
add(15.5, "whoosh_short", -12, 0.5)
for k in range(5):
    add(16.0 + k * 0.1, "tick_lo", -16)
add(16.82, "pop", -11)
# 7. stops earning
add(18.0, "whoosh_short", -10)
add(18.12, "zip", -14, -0.4)
for k in range(6):
    add(18.6 + k * 0.13, "tick", -19)
add(19.4, "impact_small", -6)
add(19.86, "impact", -7)
# 8. pattern break
add(21.0, "impact", -4)
add(21.12, "whoosh_short", -11, 0.6)
add(21.4, "whoosh_short", -11, 0.6)
add(21.68, "impact_small", -5)
# 9. five cards
add(23.0, "whoosh_short", -11)
for k, p in enumerate([23.15, 23.7, 24.25, 24.8, 25.35]):
    add(p, "pop", -9, -0.6 + 0.3 * k)
    add(p + 0.6, "ding", -15, -0.6 + 0.3 * k)
add(26.3, "whoosh_short", -16)
# 10. stack, fee, split, 4x
add(28.0, "whoosh_long", -8)
add(28.5, "impact_small", -8)
add(29.08, "zip", -8, 0.4)
for k in range(5):
    add(29.2 + k * 0.1, "tick_lo", -16)
add(29.82, "impact_small", -5)
add(30.12, "whoosh", -9, 0.5)
add(31.1, "impact", -3)
for k in range(6):
    add(31.12 + k * 0.05, "ding", -18, -0.5 + 0.2 * k)  # coins burst from behind the 4x stamp
# 11. stop chasing
add(32.0, "impact_small", -9)
for k in range(5):
    add(32.06 + k * 0.05, "pop_hi", -16, -0.6 + 0.3 * k)
add(32.42, "whoosh_short", -11)
add(32.9, "whoosh_short", -14)
# 12. warning
add(34.02, "impact", -5)
add(34.55, "drain", -10)
add(35.48, "impact_small", -9)
add(35.9, "pop", -11)
# 13. comment MATH
add(37.0, "whoosh_short", -11, -0.4)
for k, t in enumerate([37.1, 37.18, 37.26]):
    add(t, "pop", -11, -0.3 + 0.3 * k)  # MATH drops in letter by letter
add(37.34, "impact_small", -6)
for t in [37.62, 37.76, 37.9, 38.04]:
    add(t, "key", -8, 0.2)
add(38.25, "pop", -10)
add(38.38, "whoosh_short", -14)
add(38.75, "pop_hi", -8)
add(39.48, "whoosh", -7, -0.4)


def write_wav(path, data):
    data = np.clip(data, -1, 1)
    pcm = (data * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2 if data.ndim == 2 else 1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def main():
    os.makedirs(os.path.join(ROOT, "assets", "sfx"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "assets", "audio"), exist_ok=True)
    for name, x in FX.items():
        write_wav(os.path.join(ROOT, "assets", "sfx", name + ".wav"), x)
    mix = np.zeros((int(DUR * SR), 2))
    for t, name, g, p in CUES:
        x = FX[name] * 10 ** (g / 20)
        i = int(round(t * SR))
        j = min(len(mix), i + len(x))
        l, r = np.sqrt((1 - p) / 2), np.sqrt((1 + p) / 2)
        mix[i:j, 0] += x[: j - i] * l * 1.414
        mix[i:j, 1] += x[: j - i] * r * 1.414
    peak = np.max(np.abs(mix))
    mix = mix / peak * 0.7 if peak > 0.7 else mix  # about -3 dBFS peaks
    write_wav(os.path.join(ROOT, "assets", "audio", "mix.wav"), mix)
    print(f"{len(CUES)} cues, peak {20 * np.log10(np.max(np.abs(mix))):.1f} dBFS")


if __name__ == "__main__":
    main()
