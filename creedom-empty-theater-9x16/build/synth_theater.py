"""Theater one-shots made for this reel (no licence needed): an applause swell (many short band-passed noise claps, density
rising), a few soft footsteps, and a spotlight clunk.   /root/tts/.venv/bin/python build/synth_theater.py"""
import os, subprocess
import numpy as np
import soundfile as sf
SR = 48000
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "sfx")
rng = np.random.default_rng(11)


def bp(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


def clap():
    n = int(rng.uniform(.012, .03) * SR)
    c = rng.standard_normal(n) * np.exp(-np.linspace(0, 6, n))
    return bp(np.pad(c, (0, 256)), rng.uniform(700, 1100), rng.uniform(2500, 4200))


def save(name, y, st=None):
    if st is None:
        y = y / (np.max(np.abs(y)) + 1e-9) * .9
        st = np.stack([y, np.roll(y, 41)], 1)
    else:
        st = st / (np.max(np.abs(st)) + 1e-9) * .9
    p = os.path.join(OUT, name + ".wav")
    sf.write(p, st, SR)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", p, "-b:a", "192k", p[:-4] + ".mp3"], check=True)
    os.remove(p)


# applause: 5 s, density 4 -> 70 claps/s, stereo spread, a soft room tail
D = 5.0
L = np.zeros(int(D * SR) + 4000)
R = np.zeros_like(L)
t = 0.0
while t < D:
    dens = 4 + 66 * min(1, (t / 2.2)) ** 1.6 * (1 - max(0, t - 4.0) * .5)
    c = clap()
    i = int(t * SR)
    pan = rng.uniform(0, 1)
    L[i:i + len(c)] += c * (1 - pan) * rng.uniform(.4, 1)
    R[i:i + len(c)] += c * pan * rng.uniform(.4, 1)
    t += rng.exponential(1 / dens)
k = np.exp(-np.linspace(0, 8, int(.25 * SR))) * rng.standard_normal(int(.25 * SR)) * .02
L, R = np.convolve(L, k, "same") * 3 + L, np.convolve(R, k[::-1], "same") * 3 + R
env = np.minimum(1, np.linspace(0, 1, len(L)) * 3) * np.minimum(1, (len(L) - np.arange(len(L))) / (SR * .6))
save("applause", None, np.stack([L * env, R * env], 1))
# footsteps: 4 soft heel-toe thumps
y = np.zeros(int(1.6 * SR))
for s in range(4):
    i = int((.08 + .38 * s) * SR)
    n = int(.09 * SR)
    th = bp(rng.standard_normal(n) * np.exp(-np.linspace(0, 9, n)), 80, 900)
    y[i:i + n] += th
save("steps", y)
# spotlight clunk: a low thump plus a metallic tick
n = int(.5 * SR)
tt = np.arange(n) / SR
y = np.sin(2 * np.pi * (70 + 40 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 14)
y[:int(.02 * SR)] += bp(rng.standard_normal(int(.02 * SR)), 2000, 6000) * .6
save("clunk", y)
print("ok")
