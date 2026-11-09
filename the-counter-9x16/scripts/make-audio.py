#!/usr/bin/env python3
"""Synthesize the music bed and story SFX for The Counter (all original, generated here).

Usage: <python-with-numpy+soundfile> make-audio.py <project_dir> <bundled_sfx_dir>
Writes audio/music.wav and audio/sfx.wav (48 kHz stereo, film length).
Bundled accents (whoosh, riser, impact, pop, sparkle) come from media-use's Pixabay-licensed library.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 48000
proj, lib = Path(sys.argv[1]), Path(sys.argv[2])
DUR = 126.92
N = int(DUR * SR)
rng = np.random.default_rng(7)


def t_axis(d):
    return np.arange(int(d * SR)) / SR


def fft_filter(x, lo=None, hi=None):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.ones_like(f)
    if lo:
        m *= 1 / (1 + (lo / np.maximum(f, 1)) ** 4)
    if hi:
        m *= 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * m, len(x))


def env_ad(d, a=0.005, tau=0.3):
    t = t_axis(d)
    return np.minimum(t / a, 1) * np.exp(-np.maximum(t - a, 0) / tau)


def place(buf, sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= len(buf):
        return
    sig = sig[: len(buf) - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[i:i + len(sig), 0] += sig * gain * l * 1.414
    buf[i:i + len(sig), 1] += sig * gain * r * 1.414


def load(name):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(lib / name), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(out, dtype=np.float32).astype(np.float64)


def note(n):  # MIDI -> Hz
    return 440 * 2 ** ((n - 69) / 12)


# ============================== MUSIC ==============================
music = np.zeros((N, 2))


def pad(freqs, d, a=1.6, r=1.8, bright=6):
    t = t_axis(d)
    s = np.zeros_like(t)
    for f in freqs:
        for det in (-0.12, 0.0, 0.11):
            ff = f * 2 ** (det / 12)
            for h in range(1, bright + 1):
                s += np.sin(2 * np.pi * ff * h * t + h * 1.3) / (h ** 1.6)
    e = np.minimum(t / a, 1) * np.minimum((d - t) / r, 1)
    s *= np.clip(e, 0, 1) * (1 + 0.15 * np.sin(2 * np.pi * 0.23 * t))
    return s / (len(freqs) * 3 * 2.2)


def musicbox(f, d=1.8):
    t = t_axis(d)
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2 * t) + 0.12 * np.sin(2 * np.pi * f * 4.17 * t)
    return s * env_ad(d, 0.003, 0.55)


# A: cozy-curious, 0 - 67.8
prog = [[57, 60, 64], [53, 57, 60], [48, 52, 55, 60], [55, 59, 62]]  # Am F C G
t0 = 0.0
k = 0
while t0 < 67.8:
    ch = prog[k % 4]
    d = min(8.4, 68.6 - t0)
    place(music, pad([note(n - 12) for n in ch], d), t0, 0.55, pan=-0.1)
    place(music, pad([note(ch[0] - 24)], d, bright=3), t0, 0.5)
    t0 += 8.0
    k += 1
melody = [76, 79, 81, 79, 76, 74, 72, 74, 76, 72, 69, 72, 74, 76, 79, 76]
for i in range(60):
    tt = 2.0 + i * 1.08
    if tt > 66:
        break
    if i % 8 in (3, 7):
        continue
    place(music, musicbox(note(melody[i % len(melody)])), tt, 0.16, pan=0.3 * np.sin(i))

# B: midnight tension, 67.8 - 113.9
d = 113.9 - 67.8
t = t_axis(d)
drone = (np.sin(2 * np.pi * 55 * t) + 0.6 * np.sin(2 * np.pi * 82.4 * t) + 0.25 * np.sin(2 * np.pi * 110.3 * t))
drone *= (0.75 + 0.25 * np.sin(2 * np.pi * 0.18 * t)) * np.minimum(t / 2.5, 1) * np.minimum((d - t) / 1.5, 1)
wind = fft_filter(rng.standard_normal(len(t)), 120, 700) * 0.35 * np.minimum(t / 4, 1) * np.minimum((d - t) / 1.5, 1)
place(music, drone * 0.22 + wind * 0.12, 67.8)
# dissonant high cluster that creeps in toward the reveal
cl = pad([note(81), note(82)], 75.6 - 69.0, a=5, r=0.6, bright=2)
place(music, cl, 69.0, 0.12, pan=0.2)


def thump(f0=55, d=0.35):
    t = t_axis(d)
    f = f0 * (1 + 1.5 * np.exp(-t / 0.03))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_ad(d, 0.002, 0.09)


tt = 76.2
while tt < 94.6:
    place(music, thump(), tt, 0.5)
    place(music, thump(50), tt + 0.26, 0.35)
    tt += 1.05
# counting motif: soft plucks every 0.5 s while he counts
for i, tt in enumerate(np.arange(98.0, 113.6, 0.5)):
    place(music, musicbox(note([69, 72, 69, 71][i % 4] - 12), 0.6) * 0.8, tt, 0.13, pan=-0.2)
# rain shimmer
d = 4.0
sh = sum(np.sin(2 * np.pi * note(n) * t_axis(d) + n) for n in (88, 91, 93, 95, 98)) / 5
sh *= np.minimum(t_axis(d) / 0.6, 1) * np.exp(-np.maximum(t_axis(d) - 1.6, 0) / 1.2) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t_axis(d)))
place(music, sh, 95.0, 0.12)

# C: sunrise resolve, 113.9 - 120.6 (A major)
place(music, pad([note(57 - 12), note(61 - 12), note(64 - 12), note(69 - 12)], 7.6, a=1.2, r=2.2, bright=7), 113.8, 0.75)
for i, n in enumerate([81, 85, 88, 93]):
    place(music, musicbox(note(n), 2.5), 114.0 + i * 0.32, 0.18, pan=-0.4 + i * 0.25)

# D: playful button, 120.5 - end
phrase = [(120.7, 84), (121.0, 81), (121.3, 79), (121.6, 76), (122.4, 79), (122.7, 77), (123.0, 76), (123.3, 74),
          (124.95, 72), (125.1, 76), (125.25, 79), (125.4, 84)]
for tt, n in phrase:
    place(music, musicbox(note(n), 1.6), tt, 0.17, pan=0.2)
place(music, pad([note(48), note(52), note(55), note(60)], 2.0, a=0.05, r=1.2, bright=5), 124.9, 0.5)

# ============================== SFX ==============================
sfx = np.zeros((N, 2))


def crickets(at, d):
    for tt in np.arange(at, at + d, 0.62):
        for k in range(3):
            c = np.sin(2 * np.pi * (4300 + rng.uniform(-150, 150)) * t_axis(0.018)) * np.hanning(int(0.018 * SR))
            place(sfx, c, tt + k * 0.045 + rng.uniform(0, 0.05), 0.06, pan=rng.uniform(-0.8, 0.8))


def creak(d, f0=110, f1=170):
    t = t_axis(d)
    f = np.interp(t, [0, d], [f0, f1]) * (1 + 0.25 * np.sin(2 * np.pi * 7 * t) + 0.1 * rng.standard_normal(len(t)).cumsum() / np.sqrt(len(t)))
    ph = np.cumsum(f) / SR
    pulses = (np.mod(ph, 1) < 0.08).astype(float)
    s = fft_filter(pulses, 500, 2600)
    s *= np.minimum(t / 0.05, 1) * np.minimum((d - t) / 0.08, 1)
    return s / (np.abs(s).max() + 1e-9)


def footstep(heavy=1.0):
    d = 0.5
    t = t_axis(d)
    body = np.sin(2 * np.pi * np.cumsum(70 * (1 + np.exp(-t / 0.02))) / SR) * env_ad(d, 0.002, 0.12)
    click = fft_filter(rng.standard_normal(len(t)), 800, 4000) * env_ad(d, 0.001, 0.015)
    return body * heavy + click * 0.4


def tick(f=2600, d=0.06, tau=0.012):
    t = t_axis(d)
    return (np.sin(2 * np.pi * f * t) + fft_filter(rng.standard_normal(len(t)), 1500, 7000) * 0.5) * env_ad(d, 0.0005, tau)


def bell(f=330, d=4.0, bright=1.0):
    t = t_axis(d)
    parts = [(0.5, 0.5, 2.5), (1.0, 1.0, 1.8), (1.19, 0.5, 1.2), (1.5, 0.4, 1.0), (2.0, 0.6, 0.8), (2.51, 0.3, 0.5), (2.66, 0.25, 0.45), (3.01, 0.2, 0.35)]
    s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / (tau * 1.4)) for r, a, tau in parts)
    return s * np.minimum(t / 0.002, 1) / 2.5


def noise_burst(d, lo, hi, tau, a=0.002):
    t = t_axis(d)
    return fft_filter(rng.standard_normal(len(t)), lo, hi) * env_ad(d, a, tau)


def grains(d, rate=900, lo=2500, hi=9000, decay=0.6, build=0.02):
    t = t_axis(d)
    imp = np.zeros(len(t))
    n = int(rate * d)
    idx = rng.integers(0, len(t), n)
    imp[idx] = rng.uniform(0.3, 1, n) * np.where(rng.random(n) < 0.5, -1, 1)
    s = fft_filter(imp, lo, hi) + fft_filter(rng.standard_normal(len(t)), lo, hi) * 0.15
    return s * np.minimum(t / build, 1) * np.exp(-t / decay)


def vacuum(d, a=0.4, r=0.6, spin_up=False, spin_down=False):
    t = t_axis(d)
    f = np.full(len(t), 118.0)
    if spin_up:
        f = 118 * np.minimum(0.25 + t / 0.8, 1)
    if spin_down:
        f = 118 * np.maximum(1 - t / d, 0.2)
    ph = np.cumsum(f) / SR
    hum = sum(np.sin(2 * np.pi * ph * h) / h for h in range(1, 12))
    air = fft_filter(rng.standard_normal(len(t)), 900, 5000) * 0.6
    s = (fft_filter(hum, 60, 3000) * 0.35 + air) * (1 + 0.08 * np.sin(2 * np.pi * 5 * t))
    e = np.minimum(t / a, 1) * np.minimum((d - t) / r, 1)
    return s * np.clip(e, 0, 1) * (np.maximum(f / 118, 0.2) if (spin_up or spin_down) else 1)


def snore(d=0.55, big=False):
    t = t_axis(d)
    rate = 34 if big else 26
    buzz = (np.mod(t * rate, 1) < 0.25).astype(float)
    s = fft_filter(buzz, 70, 1400) * 0.8 + fft_filter(rng.standard_normal(len(t)), 250, 1100) * 0.5
    e = np.sin(np.pi * np.clip(t / d, 0, 1)) ** (0.7 if big else 1.2)
    return s * e / (np.abs(s).max() + 1e-9)


def chirp_bird():
    d = 0.16
    t = t_axis(d)
    f = 3200 + 1600 * np.sin(np.pi * t / d)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.hanning(len(t))


crickets(0.0, 7.0)
place(sfx, creak(1.2, 90, 130), 6.95, 0.18, pan=-0.6)
for k, tt in enumerate(np.arange(7.3, 10.3, 0.95)):
    place(sfx, footstep(1.0), tt, 0.5, pan=-0.5)
# rules montage: drawer rattle, sock soft, rice sprinkle
place(sfx, grains(0.9, rate=120, lo=1500, hi=6000, decay=0.4), 18.25, 0.3)
place(sfx, grains(1.6, rate=400, decay=0.8), 19.9, 0.25)
for tt in np.arange(22.0, 24.6, 0.11):  # fast counting ticks
    place(sfx, tick(1900, tau=0.008), tt, 0.08, pan=0.2)
for k in range(3):
    place(sfx, footstep(0.8), 25.35 + k * 0.4, 0.35, pan=0.5)
# cup slides then smashes
place(sfx, noise_burst(0.4, 1500, 6000, 0.2, a=0.05), 26.98, 0.08)
place(sfx, tick(3400, 0.25, 0.06) + noise_burst(0.25, 2000, 9000, 0.05), 27.47, 0.45, pan=0.3)
place(sfx, grains(0.6, rate=200, lo=2500, hi=9000, decay=0.2), 27.5, 0.25, pan=0.3)
# filling the jar
place(sfx, grains(2.9, rate=700, lo=2000, hi=8000, decay=3.0, build=0.1), 30.3, 0.22)
# vacuum montage
place(sfx, vacuum(3.6, 0.3, 0.3), 36.3, 0.2)
# snores like a lawnmower
for tt in (40.64, 41.99):
    place(sfx, snore(0.45, big=True), tt, 0.32)
# rice pouring to the top + shake
place(sfx, grains(1.2, rate=900, decay=2.0, build=0.05), 48.9, 0.25)
for tt in np.arange(50.4, 52.4, 0.25):
    place(sfx, grains(0.12, rate=60, decay=0.08), tt, 0.25)
# clock ticks at 11:55
for k, tt in enumerate(np.arange(52.65, 53.75, 0.5)):
    place(sfx, tick(2300 if k % 2 else 1700, 0.08, 0.02), tt, 0.25, pan=-0.3)
# dog paws
for tt in np.arange(53.85, 56.3, 0.14):
    place(sfx, tick(900, 0.05, 0.01), tt, 0.12, pan=np.clip((tt - 55) * 0.5, -0.6, 0.6))
place(sfx, tick(3800, 0.3, 0.08), 56.33, 0.25)  # jar knocked
# jar hits the floor; rice everywhere
place(sfx, footstep(1.0), 56.93, 0.5)
place(sfx, tick(3000, 0.4, 0.1) + noise_burst(0.4, 1800, 8000, 0.08), 56.95, 0.35)
place(sfx, grains(1.6, rate=2400, lo=2500, hi=10000, decay=0.5, build=0.01), 56.95, 0.5)
# plug in, vacuum spins up, runs, spins down
place(sfx, tick(1500, 0.12, 0.03), 60.62, 0.5, pan=-0.4)
place(sfx, vacuum(0.85, 0.05, 0.05, spin_up=True), 60.7, 0.22)
place(sfx, vacuum(3.4, 0.05, 0.4), 61.5, 0.12)
place(sfx, vacuum(1.0, 0.01, 0.2, spin_down=True), 64.85, 0.12)
place(sfx, snore(0.6), 65.6, 0.12)
place(sfx, snore(0.6), 67.2, 0.12)
# clock: ticks then chimes, the twelfth one big
for tt in np.arange(67.9, 70.4, 0.5):
    place(sfx, tick(2000, 0.08, 0.02), tt, 0.18, pan=-0.4)
for tt in (68.25, 69.15, 69.95):
    place(sfx, bell(330, 3.0), tt, 0.22, pan=-0.4)
place(sfx, bell(262, 5.0), 70.42, 0.5, pan=-0.3)
place(sfx, load("impact-bass-1.mp3"), 70.4, 0.35)
# door creaks open in two pulls
place(sfx, creak(0.6, 120, 160), 71.74, 0.3, pan=-0.6)
place(sfx, creak(0.75, 150, 95), 72.59, 0.34, pan=-0.6)
place(sfx, fft_filter(rng.standard_normal(int(2.0 * SR)), 200, 1200) * np.linspace(0, 1, int(2.0 * SR)) ** 2 * 0.3, 71.7, 0.15)
place(sfx, load("riser.mp3"), 65.6, 0.16)
# the Counter steps in and unfolds
for tt in (75.75, 76.45):
    place(sfx, footstep(1.3), tt, 0.6, pan=-0.5)
place(sfx, load("impact-bass-2.mp3"), 75.9, 0.28)
place(sfx, load("whoosh-short.mp3"), 78.28, 0.35)
place(sfx, footstep(0.6), 78.86, 0.35)
# counting list ticks
for tt in (82.75, 83.15, 84.05, 85.05):
    place(sfx, tick(1700, 0.08, 0.02), tt, 0.25)
for tt in np.arange(86.4, 89.8, 0.85):
    place(sfx, footstep(1.0), tt, 0.45, pan=-0.2)
for tt in (87.6,):
    place(sfx, snore(0.6), tt, 0.12, pan=0.4)
# lid pop, bag rip, throw
place(sfx, load("pop.mp3"), 91.72, 0.45, pan=0.3)
rip = noise_burst(0.5, 600, 6000, 0.3) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 38 * t_axis(0.5))))
place(sfx, rip, 92.55, 0.35, pan=0.3)
place(sfx, load("whoosh.mp3"), 93.55, 0.4)
place(sfx, noise_burst(0.8, 300, 4000, 0.3, a=0.01), 94.95, 0.3)  # bag bursts
# rice and dust rain down
place(sfx, grains(4.0, rate=3200, lo=2500, hi=11000, decay=1.4, build=0.5), 95.05, 0.42)
place(sfx, grains(3.0, rate=1500, lo=1200, hi=5000, decay=1.2, build=0.6), 95.4, 0.2, pan=-0.4)
# six eyes go wide: dissonant stab
st = (np.sin(2 * np.pi * 220 * t_axis(1.2)) + np.sin(2 * np.pi * 233 * t_axis(1.2)) + 0.5 * np.sin(2 * np.pi * 466 * t_axis(1.2))) * env_ad(1.2, 0.01, 0.4)
place(sfx, st, 99.83, 0.14)
# counting taps
for tt in (100.71, 101.03, 101.40, 107.98, 108.30, 108.66):
    place(sfx, tick(1400, 0.08, 0.02), tt, 0.35)
# the big snore, flinch, more snores
place(sfx, snore(0.6, big=True), 105.3, 0.55, pan=0.3)
place(sfx, load("whoosh-short.mp3"), 105.9, 0.18)
for tt in (109.42, 110.88):
    place(sfx, snore(0.5, big=True), tt, 0.35, pan=0.3)
# time-lapse whoosh of ticks
for tt in np.arange(112.2, 113.8, 0.06):
    place(sfx, tick(2200, 0.04, 0.008), tt, 0.06, pan=-0.3)
# sunrise sparkle + birds
place(sfx, load("sparkle.mp3"), 113.9, 0.3)
for tt in (114.6, 114.8, 116.1, 117.9, 118.1, 119.6, 121.2, 121.4, 123.0):
    place(sfx, chirp_bird(), tt, 0.07, pan=0.7)
# out the door, door shuts
for tt in np.arange(118.2, 119.8, 0.8):
    place(sfx, footstep(1.0), tt, 0.4, pan=-0.6)
place(sfx, footstep(1.6) + noise_burst(0.5, 100, 900, 0.12), 120.42, 0.55, pan=-0.6)
place(sfx, load("pop.mp3"), 125.1, 0.35)

# ============================== write ==============================
for name, buf, peak in (("music.wav", music, 0.5), ("sfx.wav", sfx, 0.8)):
    m = np.abs(buf).max()
    if m > peak:
        buf *= peak / m
    sf.write(proj / "audio" / name, buf.astype(np.float32), SR, subtype="PCM_16")
    print(name, f"{len(buf) / SR:.2f}s peak {np.abs(buf).max():.2f}")
