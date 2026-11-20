"""One-shots made for "365 Days in One Room": a magic sparkle (Cree bursting out of the phone) and a soft notification ping.
python3 build/synth_room.py   -> assets/sfx/sparkle.mp3, assets/sfx/ping.mp3"""
import os, subprocess
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 44100
rng = np.random.default_rng(7)


def save(name, y):
    y = y / (np.abs(y).max() + 1e-9) * .9
    raw = os.path.join(ROOT, "assets", "sfx", f"{name}.f32")
    y.astype(np.float32).tofile(raw)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", raw, "-b:a", "192k",
                    os.path.join(ROOT, "assets", "sfx", f"{name}.mp3")], check=True)
    os.remove(raw)


def tone(f, d, decay):
    t = np.arange(int(SR * d)) / SR
    return np.sin(2 * np.pi * f * t) * np.exp(-t * decay)


# sparkle: a rising shower of bell partials with a soft whoosh under it
d = 1.4
y = np.zeros(int(SR * d))
for k in range(26):
    t0 = k * .04 + rng.uniform(0, .02)
    f = 1200 * 2 ** (k / 14) * rng.uniform(.97, 1.03)
    s = tone(f, .5, 9) + .35 * tone(f * 2.76, .5, 14)
    i = int(t0 * SR)
    y[i:i + len(s)] += s[:len(y) - i] * (1 - k / 34)
n = rng.standard_normal(len(y))
env = np.sin(np.linspace(0, np.pi, len(y))) ** 2
b = np.convolve(n, np.ones(60) / 60, mode="same")
y += .35 * (n - b) * env
save("sparkle", y)
# ping: two quick glassy notes
y = np.concatenate([tone(1568, .14, 18) + .3 * tone(3136, .14, 26), tone(2093, .5, 9) + .3 * tone(4186, .5, 14)])
save("ping", y)
