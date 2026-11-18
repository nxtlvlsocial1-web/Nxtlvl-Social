"""Synthesised one-shots (ours, no licence needed) to sit beside the CC0 OpenGameArt packs: a long airy whoosh,
a riser into cuts, and a sub-bass hit under the stamps.  python3 build/synth_sfx.py  (writes assets/sfx/*.wav -> mp3)"""
import os, subprocess
import numpy as np
import soundfile as sf
SR = 48000
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "sfx")
rng = np.random.default_rng(7)


def bandsweep(n, f0, f1, q=6.0):
    """noise through a resonant band-pass whose centre glides from f0 to f1 (simple biquad, per-sample coefficients)"""
    x = rng.standard_normal(n)
    y = np.zeros(n)
    fc = np.geomspace(f0, f1, n)
    z1 = z2 = 0.0
    for i in range(n):
        w = 2 * np.pi * fc[i] / SR
        al = np.sin(w) / (2 * q)
        b0, a0, a1, a2 = al, 1 + al, -2 * np.cos(w), 1 - al
        v = (b0 * x[i] - a1 * z1 - a2 * z2) / a0      # direct form II, b1 = 0, b2 = -b0
        y[i] = v - z2 * 0 + (-b0 / a0) * 0
        y[i] = (b0 / a0) * x[i] + 0 * z1 - (b0 / a0) * (x[i - 2] if i > 1 else 0) - (a1 / a0) * (y[i - 1] if i > 0 else 0) - (a2 / a0) * (y[i - 2] if i > 1 else 0)
    return y


def env(n, a, peak_at):
    t = np.linspace(0, 1, n)
    e = np.where(t < peak_at, (t / peak_at) ** a, ((1 - t) / (1 - peak_at)) ** 1.6)
    return e


def save(name, y):
    y = y / (np.max(np.abs(y)) + 1e-9) * .9
    st = np.stack([y, np.roll(y, 37)], 1)
    p = os.path.join(OUT, name + ".wav")
    sf.write(p, st, SR)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", p, "-b:a", "192k", p[:-4] + ".mp3"], check=True)
    os.remove(p)


n = int(.75 * SR)
save("whoosh_big", bandsweep(n, 300, 3800, 3) * env(n, 2.2, .55) + bandsweep(n, 3800, 500, 4) * env(n, 2.5, .62) * .5)
n = int(1.3 * SR)
r = bandsweep(n, 200, 6000, 5) * env(n, 3.0, .97)
t = np.arange(n) / SR
r += .25 * np.sin(2 * np.pi * np.cumsum(np.geomspace(110, 440, n)) / SR) * env(n, 3, .97)
save("riser", r)
n = int(.7 * SR)
t = np.arange(n) / SR
f = 120 * np.exp(-t * 9) + 42
sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6)
sub += .35 * rng.standard_normal(n) * np.exp(-t * 60)
save("sub_hit", sub)
print("ok")
