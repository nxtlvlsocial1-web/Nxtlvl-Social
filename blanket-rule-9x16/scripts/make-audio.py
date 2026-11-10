#!/usr/bin/env python3
"""Synthesize the music bed and story SFX for The Blanket Rule (all original, generated here).

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
DUR = 61.6
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
sfx = np.zeros((N, 2))
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


def thump(f0=55, d=0.35):
    t = t_axis(d)
    f = f0 * (1 + 1.5 * np.exp(-t / 0.03))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_ad(d, 0.002, 0.09)


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




def pluck(f, d=0.35, bright=1.0):
    t = t_axis(d)
    s = sum(np.sin(2 * np.pi * f * h * t) * (0.6 ** (h - 1)) * np.exp(-t * (6 + h * 3)) for h in range(1, 6))
    return s * np.minimum(t / 0.002, 1) * bright


def boing(f0=420, f1=140, d=0.45):
    t = t_axis(d)
    f = f1 + (f0 - f1) * np.exp(-t / 0.08) * (1 + 0.25 * np.sin(2 * np.pi * 18 * t) * np.exp(-t / 0.2))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_ad(d, 0.003, 0.18)


def stab(notes, d=1.2, tau=0.35):
    t = t_axis(d)
    s = np.zeros_like(t)
    for n in notes:
        f = note(n)
        for h in range(1, 9):
            s += np.sin(2 * np.pi * f * h * t + h) / h ** 1.2
    return s * env_ad(d, 0.004, tau) / (len(notes) * 2.5)



def heartbeat(at, n, gap, gain=0.8):
    for i in range(n):
        place(music, thump(50, 0.4), at + i * gap, gain)
        place(music, thump(44, 0.35), at + i * gap + 0.22, gain * 0.7)


def cluster(notes, d, a=0.02, tau=0.8):
    t = t_axis(d)
    s = np.zeros_like(t)
    for n in notes:
        f = note(n)
        s += np.sin(2 * np.pi * f * t + n) + 0.3 * np.sin(2 * np.pi * f * 2.01 * t)
    return s * np.minimum(t / a, 1) * np.exp(-t / tau) / len(notes)


def drone(d, f=55, wob=0.15):
    t = t_axis(d)
    s = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.5 * t + 1) + 0.25 * np.sin(2 * np.pi * f * 2.02 * t)
    return s * (0.8 + 0.2 * np.sin(2 * np.pi * wob * t)) * np.minimum(t / 1.5, 1) * np.minimum((d - t) / 0.6, 1)


# uneasy lullaby, 0 - 10.2 (detuned music box, A minor)
lull = [76, 72, 69, 72, 76, 77, 76, 74, 72, 69, 71, 72]
for i, tt in enumerate(np.arange(0.15, 10.1, 0.62)):
    f = note(lull[i % len(lull)]) * (1 + 0.006 * np.sin(i * 1.7))
    place(music, musicbox(f, 1.4), tt, 0.2, pan=0.25 * np.sin(i))
place(music, pad([note(45), note(52), note(57)], 10.6, a=1.0, r=1.0, bright=3), 0.0, 0.35)
# 3:07: sub drop, then a low drone through the dread
place(music, thump(36, 1.2), 10.62, 1.0)
place(music, drone(17.0, 55), 10.6, 0.22)
# the grab
place(music, cluster([77, 78, 82, 83], 2.5, 0.01, 0.9), 15.45, 0.32)
place(sfx, noise_burst(1.6, 3000, 11000, 0.7, a=0.02), 15.4, 0.12)
place(sfx, grains(1.4, rate=500, lo=4000, hi=12000, decay=0.8, build=0.05), 15.45, 0.1)
# heartbeat under "pretended to be asleep", speeding up
heartbeat(18.0, 5, 1.0, 0.65)
heartbeat(23.0, 4, 0.85, 0.75)
# the head turns: creak, then the sting
place(music, load("riser.mp3")[int(7.4 * SR):] * 0.9, 25.3, 0.25)
place(sfx, creak(0.7, 70, 110), 27.95, 0.35, pan=0.5)
place(music, load("impact-bass-2.mp3"), 28.1, 0.4)
place(music, cluster([57, 58, 63, 64, 70], 3.0, 0.005, 1.2), 28.45, 0.4)
# once. twice.
for tt in (31.84, 32.48):
    place(music, thump(48, 0.6), tt, 1.0)
    place(sfx, creak(0.25, 160, 120), tt, 0.15)
# the whisper: near silence, one high eerie tone
t = t_axis(5.0)
eerie = np.sin(2 * np.pi * 1760 * t) * 0.3 + np.sin(2 * np.pi * 1767 * t) * 0.3
place(music, eerie * np.minimum(t / 1.5, 1) * np.minimum((5 - t) / 1.0, 1), 33.4, 0.05)
# realization: build
place(music, load("riser.mp3")[int(7.0 * SR):], 38.3, 0.3)
place(sfx, load("whoosh.mp3"), 41.32, 0.5)
place(sfx, load("whoosh-short.mp3"), 41.75, 0.35)
place(music, thump(40, 0.8), 41.38, 0.8)
# the clothes stand up and walk
d = 2.4
t = t_axis(d)
rust = fft_filter(rng.standard_normal(len(t)), 600, 5000) * (0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 3 * t))) * np.minimum(t / 0.2, 1) * np.minimum((d - t) / 0.4, 1)
place(sfx, rust, 43.6, 0.22, pan=0.4)
place(sfx, creak(0.9, 60, 95), 43.75, 0.3, pan=0.4)
for k, tt in enumerate((44.6, 45.0, 45.4)):
    place(sfx, footstep(1.1), tt, 0.6, pan=0.3 - k * 0.2)
for i, tt in enumerate(np.arange(43.3, 45.55, 0.28 - 0.0)):
    place(music, thump(55 + i, 0.3), tt, 0.35 + i * 0.03)
place(music, stab([33, 34, 40], 2.2, 0.9), 45.56, 0.55)
# all night: ticking time-lapse over a drone, terrified breathing
place(music, drone(2.8, 49, 0.4), 46.4, 0.22)
for tt in np.arange(46.45, 49.0, 0.11):
    place(music, tick(2400, 0.04, 0.008), tt, 0.1, pan=-0.4)
for tt in np.arange(46.5, 49.0, 0.42):
    place(sfx, noise_burst(0.3, 400, 3000, 0.12, a=0.08), tt, 0.08)
# sunrise resolve
place(music, pad([note(48), note(52), note(55), note(60), note(64)], 6.0, a=1.2, r=1.6, bright=6), 49.0, 0.7)
for i, n in enumerate([72, 76, 79, 84]):
    place(music, musicbox(note(n), 2.0), 49.3 + i * 0.3, 0.16, pan=-0.3 + i * 0.2)
for tt in (49.8, 50.0, 51.3, 52.9, 53.1, 54.6, 56.2):
    place(sfx, chirp_bird(), tt, 0.07, pan=0.7)
place(sfx, rust[: int(1.3 * SR)], 50.7, 0.18, pan=0.4)
# the note: paper, a gentle music box, the tiny snore
place(sfx, grains(0.5, rate=220, lo=1500, hi=7000, decay=0.25, build=0.03), 54.2, 0.3)
for i, tt in enumerate(np.arange(52.6, 58.2, 0.5)):
    n = [72, 76, 79, 77, 76, 74, 72, 74, 76, 79, 81][i % 11]
    place(music, musicbox(note(n), 1.2), tt, 0.13, pan=0.2)
for tt in (57.0, 58.1):
    place(sfx, snore(0.5) * 0.6, tt, 0.1)
place(music, pluck(note(60), 0.5) + pluck(note(67), 0.5), 57.62, 0.35)
# end card
for i, n in enumerate([72, 79, 76, 84]):
    place(music, musicbox(note(n), 1.6), 58.7 + i * 0.4, 0.15, pan=0.2)
place(music, pad([note(45), note(52), note(57), note(60)], 3.0, a=0.4, r=1.4, bright=3), 58.6, 0.35)
place(sfx, load("pop.mp3"), 58.85, 0.3)
# ambience: crickets through the open window, the fan's hum
crickets(0.0, 14.5)
crickets(17.8, 9.0)
t = t_axis(7.8)
fanhum = fft_filter(np.sin(2 * np.pi * 95 * t) + 0.5 * np.sin(2 * np.pi * 190 * t) + rng.standard_normal(len(t)) * 0.6, 80, 1500)
place(sfx, fanhum * np.minimum(t / 0.5, 1) * np.minimum((7.8 - t) / 0.8, 1) / np.abs(fanhum).max(), 6.4, 0.1)
place(sfx, load("whoosh-short.mp3"), 8.32, 0.35)
place(sfx, footstep(0.5), 8.8, 0.3)

# ============================== write ==============================
for name, buf, peak in (("music.wav", music, 0.5), ("sfx.wav", sfx, 0.8)):
    m = np.abs(buf).max()
    if m > peak:
        buf *= peak / m
    sf.write(proj / "audio" / name, buf.astype(np.float32), SR, subtype="PCM_16")
    print(name, f"{len(buf) / SR:.2f}s peak {np.abs(buf).max():.2f}")
