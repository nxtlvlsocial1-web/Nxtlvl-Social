#!/usr/bin/env python3
"""Synthesize the music bed and story SFX for The Lying House (all original, generated here).

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
DUR = 58.3
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


T_POP1, T_DOOR49 = 2.95, 53.6

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


# A: sneaky-comedy groove, 0 - 20.37 (C minor, 112 bpm)
BEAT = 60 / 112
bass = [36, 36, 43, 43, 39, 39, 41, 43]
mel = [72, 75, 79, 77, 75, 72, 70, 72, 75, 74, 72, 70, 67, 70, 72, 0]
for i in range(int(20.3 / BEAT)):
    tt = 0.12 + i * BEAT
    if tt > 20.2:
        break
    place(music, pluck(note(bass[i % 8]), 0.4), tt, 0.55, pan=-0.2)
    if i % 2 == 1:
        place(music, pluck(note(bass[i % 8] + 19), 0.25, 0.7), tt, 0.28, pan=0.3)
    m = mel[i % 16]
    if m and i % 2 == 0:
        place(music, musicbox(note(m), 0.9), tt, 0.13, pan=0.25)
    if i % 4 == 0:
        place(music, tick(5200, 0.05, 0.01), tt, 0.25)
    if i % 4 == 2:
        place(music, noise_burst(0.12, 2500, 9000, 0.03), tt, 0.12)
# B: mystery, 20.37 - 33.2
d = 33.2 - 20.37
t = t_axis(d)
drone = (np.sin(2 * np.pi * 65.4 * t) + 0.5 * np.sin(2 * np.pi * 98 * t)) * np.minimum(t / 1.5, 1) * np.minimum((d - t) / 0.4, 1)
place(music, drone * 0.2, 20.37)
place(music, bell(392, 3.5), 23.72, 0.18, pan=0.2)
for i, tt in enumerate(np.arange(25.3, 33.1, BEAT)):  # tiptoe pizzicato for the family meeting
    n = [48, 51, 55, 51, 48, 51, 56, 55][i % 8]
    place(music, pluck(note(n), 0.25), tt, 0.32, pan=-0.1 + 0.2 * (i % 2))
# riser to the door opening
place(music, load("riser.mp3")[: int(3.0 * SR)] * np.linspace(0.3, 1, int(3.0 * SR)), 33.0, 0.3)
# C: wonder swell at the reveal (major), then a comic "wah" on broccoli
place(music, pad([note(48), note(52), note(55), note(60), note(64)], 4.9, a=0.25, r=1.2, bright=8), 35.96, 0.8)
wah = sum(np.sin(2 * np.pi * note(n) * t_axis(1.2) * (1 - 0.06 * t_axis(1.2))) for n in (43, 47, 50)) * env_ad(1.2, 0.02, 0.5)
place(music, wah, 38.6, 0.25)
# D: the turn: two low hits
for tt in (41.3, 41.9):
    place(music, thump(48, 0.6), tt, 0.9)
    place(music, stab([36, 42], 0.8, 0.3), tt, 0.35)
# E: dreamy flashback waltz, 42.97 - 48.4
for i, tt in enumerate(np.arange(43.0, 48.3, 0.42)):
    n = [72, 76, 79, 76, 74, 77, 81, 77, 72, 76, 79, 84][i % 12]
    place(music, musicbox(note(n), 1.4), tt, 0.16, pan=0.3 * np.sin(i))
place(music, pad([note(60), note(64), note(67)], 5.4, a=0.6, r=1.0, bright=4), 42.97, 0.35)
# F: held tension under Mom's question, comic pluck on "No"
place(music, pad([note(59), note(65)], 2.2, a=0.3, r=0.5, bright=3), 48.44, 0.35)
place(music, pluck(note(38), 0.5) + pluck(note(39), 0.5), 50.6, 0.6)
# G: Room 49 sting, then the outro groove
place(music, stab([48, 55, 60, 63, 67], 1.6, 0.6), 53.62, 0.9)
place(music, thump(45, 0.8), 53.62, 1.0)
for i in range(int((58.2 - 55.2) / BEAT)):
    tt = 55.2 + i * BEAT
    place(music, pluck(note(bass[i % 8]), 0.4), tt, 0.55, pan=-0.2)
    if i % 2 == 0:
        place(music, musicbox(note(mel[i % 16] or 72), 0.9), tt, 0.14, pan=0.25)
place(music, stab([48, 55, 60, 64], 1.2, 0.5), 57.4, 0.5)

# ============================== SFX ==============================
# the house grows a room
place(sfx, creak(0.5, 140, 90), 2.8, 0.25)
place(sfx, footstep(1.6) + noise_burst(0.5, 100, 900, 0.1), T_POP1, 0.6)
place(sfx, boing(), T_POP1 + 0.05, 0.35)
place(sfx, load("whoosh-short.mp3"), 4.05, 0.3)
# room 12: creak and meatloaf thuds
place(sfx, creak(0.45, 120, 170), 5.92, 0.3, pan=0.4)
for k, tt in enumerate((6.18, 6.33, 6.5)):
    place(sfx, footstep(0.7) + noise_burst(0.5, 200, 1200, 0.05), tt, 0.4, pan=0.3)
place(sfx, boing(300, 200, 0.3), 7.95, 0.15)
# room 30: creak + paper
place(sfx, creak(0.45, 130, 180), 9.25, 0.3, pan=0.4)
place(sfx, grains(1.4, rate=180, lo=1500, hi=7000, decay=0.8, build=0.1), 9.45, 0.35, pan=0.3)
for tt in (10.95, 11.15, 11.32):
    place(sfx, tick(2600, 0.04, 0.01), tt, 0.25)
# tiny door squeak; Grandma wink sparkle
place(sfx, creak(0.3, 300, 420), 12.95, 0.18, pan=-0.4)
place(sfx, load("sparkle.mp3"), 15.9, 0.18)
# closet bursts with balloons
place(sfx, footstep(1.0) + noise_burst(0.5, 300, 2500, 0.06), 16.98, 0.45, pan=-0.3)
place(sfx, load("whoosh.mp3"), 17.0, 0.3)
for k, tt in enumerate((17.1, 17.25, 17.45, 17.7)):
    place(sfx, boing(900 + k * 120, 700 + k * 100, 0.18), tt, 0.12, pan=-0.3 + k * 0.2)
# door 48 rises out of the floor
rum = fft_filter(rng.standard_normal(int(2.6 * SR)), 30, 220)
rum *= np.minimum(t_axis(2.6) / 0.3, 1) * np.minimum((2.6 - t_axis(2.6)) / 0.5, 1)
place(sfx, rum / np.abs(rum).max(), 21.0, 0.55)
place(sfx, grains(2.2, rate=250, lo=800, hi=4000, decay=1.5, build=0.3), 21.1, 0.25)
place(sfx, footstep(1.6), 23.05, 0.55)
# light flicker buzz on "Room 48"
bz = np.sign(np.sin(2 * np.pi * 120 * t_axis(1.2))) * 0.3 * (np.sin(2 * np.pi * 7 * t_axis(1.2)) > 0)
place(sfx, fft_filter(bz, 100, 2000), 24.2, 0.08)
# family meeting: chairs, oath whooshes
place(sfx, creak(0.4, 90, 70), 25.4, 0.15)
for tt in (26.9, 28.25, 29.55):
    place(sfx, load("whoosh-short.mp3"), tt, 0.12)
# Biscuit's innocent whine
t = t_axis(0.7)
wh = np.sin(2 * np.pi * np.cumsum(900 + 500 * np.sin(np.pi * t / 0.7)) / SR) * np.hanning(len(t))
place(sfx, wh, 31.9, 0.12)
# the door opens
place(sfx, tick(1200, 0.15, 0.03), 34.0, 0.4)
place(sfx, creak(1.2, 80, 140), 34.55, 0.4)
place(sfx, load("sparkle.mp3"), 35.2, 0.22)
place(sfx, load("impact-bass-1.mp3"), 38.58, 0.32)
# avalanche
place(sfx, rum[: int(1.3 * SR)] / np.abs(rum).max(), 39.55, 0.35)
for tt in np.arange(39.7, 40.8, 0.13):
    place(sfx, footstep(0.5), tt, 0.25, pan=0.3)
place(sfx, load("whoosh-short.mp3"), 41.25, 0.3)
# flashback harp-ish gliss
for i, n in enumerate(range(60, 86, 3)):
    place(sfx, musicbox(note(n), 0.6), 42.95 + i * 0.035, 0.08)
# Biscuit gulps it
gulp = boing(220, 90, 0.25)
place(sfx, gulp, 47.35, 0.35)
place(sfx, grains(0.3, rate=200, lo=1500, hi=6000, decay=0.12), 47.4, 0.25)
# arms crossed swish; "No" gulp
place(sfx, noise_burst(0.3, 800, 5000, 0.1, a=0.04), 48.45, 0.2)
place(sfx, boing(260, 120, 0.22), 50.95, 0.18)
# the house rumbles
rr = fft_filter(rng.standard_normal(int(1.7 * SR)), 25, 180)
rr *= np.minimum(t_axis(1.7) / 0.15, 1) * np.minimum((1.7 - t_axis(1.7)) / 0.3, 1)
place(sfx, rr / np.abs(rr).max(), 51.95, 0.7)
for tt in np.arange(52.0, 53.5, 0.09):
    place(sfx, tick(rng.uniform(1500, 4000), 0.05, 0.01), tt, 0.12, pan=rng.uniform(-0.6, 0.6))
# door 49 slams out of the wall
place(sfx, footstep(1.8) + noise_burst(0.5, 80, 900, 0.15), T_DOOR49, 0.75, pan=0.4)
place(sfx, load("impact-bass-1.mp3"), T_DOOR49, 0.35)
place(sfx, boing(380, 130, 0.5), T_DOOR49 + 0.06, 0.3, pan=0.4)
# end card: another room pops on the roof; button pop
place(sfx, footstep(1.4), 55.2, 0.45)
place(sfx, boing(), 55.25, 0.3)
place(sfx, load("pop.mp3"), 55.62, 0.35)

# ============================== write ==============================
for name, buf, peak in (("music.wav", music, 0.5), ("sfx.wav", sfx, 0.8)):
    m = np.abs(buf).max()
    if m > peak:
        buf *= peak / m
    sf.write(proj / "audio" / name, buf.astype(np.float32), SR, subtype="PCM_16")
    print(name, f"{len(buf) / SR:.2f}s peak {np.abs(buf).max():.2f}")
