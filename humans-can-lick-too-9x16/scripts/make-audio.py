#!/usr/bin/env python3
"""Synthesize the music bed and story SFX for Humans Can Lick Too (all original, generated here).

Usage: <python-with-numpy+soundfile> make-audio.py <project_dir> <bundled_sfx_dir>
Writes audio/music.wav and audio/sfx.wav (48 kHz stereo, film length).
Bundled accents (riser, impacts, glitch, pop, whoosh) come from media-use's Pixabay-licensed library.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 48000
proj, lib = Path(sys.argv[1]), Path(sys.argv[2])
DUR = 52.5
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


# ---- phone & hospital sounds (original synths) --------------------------------
def ping(f=1180, d=1.4):  # location "sonar" ping
    t = t_axis(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.18) + 0.4 * np.sin(2 * np.pi * f * 1.5 * t) * np.exp(-t / 0.08)
    tail = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.6) * 0.15
    return (s + tail) * np.minimum(t / 0.004, 1)


def ding(base=1318.5):  # incoming message: two bright notes
    a = bell(base, 0.9) * 1.2
    b = bell(base * 4 / 3, 1.1) * 1.2
    out = np.zeros(int(1.3 * SR))
    out[: len(a)] += a
    i = int(0.12 * SR)
    out[i:i + len(b)] += b[: len(out) - i]
    return out


def muffle(x, hi=1400):
    return fft_filter(x, None, hi)


def vibrate(d=0.45):  # phone buzz on a surface
    t = t_axis(d)
    s = np.sign(np.sin(2 * np.pi * 172 * t)) * 0.6 + np.sin(2 * np.pi * 344 * t) * 0.3
    s = fft_filter(s, 90, 2200)
    return s * np.minimum(t / 0.02, 1) * np.minimum((d - t) / 0.03, 1)


def beep(f=1046, d=0.16):  # patient monitor
    t = t_axis(d)
    return np.sin(2 * np.pi * f * t) * np.minimum(t / 0.004, 1) * np.minimum((d - t) / 0.01, 1)


def tap(bright=1.0):  # screen tap / key
    return tick(3200, 0.04, 0.006) * 0.6 * bright + noise_burst(0.04, 900, 6000, 0.005) * 0.4


def ringtone(at, until, gain=0.35):  # original 4-note marimba figure, repeating
    fig = [76, 79, 83, 79, 76, 72, 74, 79]
    tt, i = at, 0
    while tt < until:
        place(sfx, pluck(note(fig[i % 8]), 0.4, 1.0) + 0.3 * pluck(note(fig[i % 8] + 12), 0.4, 0.6), tt, gain)
        tt += 0.16 if i % 8 != 7 else 0.5
        i += 1


def hvac(d):
    t = t_axis(d)
    s = fft_filter(rng.standard_normal(len(t)), 80, 900) + 0.3 * np.sin(2 * np.pi * 60 * t)
    return s / (np.abs(s).max() + 1e-9) * np.minimum(t / 0.3, 1) * np.minimum((d - t) / 0.3, 1)


def roomtone(d):
    t = t_axis(d)
    s = fft_filter(rng.standard_normal(len(t)), 40, 400)
    return s / (np.abs(s).max() + 1e-9) * np.minimum(t / 0.6, 1) * np.minimum((d - t) / 0.6, 1)


def lick(d=0.22):  # wet tongue on skin
    t = t_axis(d)
    s = fft_filter(rng.standard_normal(len(t)), 500, 2400) * (np.sin(np.pi * t / d) ** 1.5)
    s += 0.35 * np.sin(2 * np.pi * np.cumsum(420 + 260 * np.sin(np.pi * t / d)) / SR) * np.sin(np.pi * t / d) ** 2
    return s / (np.abs(s).max() + 1e-9)


def plink(f=1500):  # water drop into a basin
    d = 0.9
    t = t_axis(d)
    fr = f * (1 + 0.6 * np.exp(-t / 0.012))
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.06)
    s += 0.25 * np.sin(2 * np.pi * f * 0.5 * t) * np.exp(-t / 0.35)
    return s * np.minimum(t / 0.001, 1)


def jingle(d=0.5, n=6):  # dog tags
    out = np.zeros(int(d * SR))
    for k in range(n):
        b = bell(rng.uniform(3200, 4600), 0.35) * rng.uniform(0.4, 1.0)
        i = int(rng.uniform(0, d - 0.35) * SR)
        out[i:i + len(b)] += b[: len(out) - i]
    return out


def whimper(d=0.9, f0=900, f1=560):
    t = t_axis(d)
    f = np.interp(t, [0, d], [f0, f1]) * (1 + 0.02 * np.sin(2 * np.pi * 7 * t))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(2 * np.pi * np.cumsum(2 * f) / SR)
    s += fft_filter(rng.standard_normal(len(t)), 600, 3000) * 0.25
    return s * np.sin(np.pi * t / d) ** 1.4 * 0.5


def alert():  # news alert: two urgent descending tones
    a = beep(1318, 0.18) * 0.9
    b = beep(988, 0.28) * 0.9
    out = np.zeros(int(0.6 * SR))
    out[: len(a)] += a
    out[int(0.2 * SR): int(0.2 * SR) + len(b)] += b
    return out


def rustle(d):
    t = t_axis(d)
    s = fft_filter(rng.standard_normal(len(t)), 1200, 6000) * (0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 2.2 * t)))
    return s * np.minimum(t / 0.1, 1) * np.minimum((d - t) / 0.2, 1)


def scrape(d):
    t = t_axis(d)
    s = fft_filter(rng.standard_normal(len(t)), 200, 1800) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t))
    return s * np.minimum(t / 0.05, 1) * np.minimum((d - t) / 0.15, 1)


# ============================== the score ==============================
place(sfx, roomtone(52.5), 0.0, 0.05)
# hook: low drone, two licks
place(music, drone(4.8, 49, 0.15), 0.0, 0.2)
place(music, pad([note(45), note(51), note(56)], 4.8, a=0.6, r=1.0, bright=3), 0.0, 0.24)
for tt in (0.45, 1.6):
    place(sfx, lick(), tt, 0.5, pan=-0.2)
place(music, thump(40, 1.0), 3.65, 0.5)
# evening: cozy music box, Max's tags, tail thumps
cozy = [72, 76, 79, 76, 74, 77, 81, 77, 72, 76, 79, 84]
for i, tt in enumerate(np.arange(4.75, 10.4, 0.46)):
    place(music, musicbox(note(cozy[i % 12]), 1.3), tt, 0.14, pan=0.2 * np.sin(i))
place(music, pad([note(48), note(52), note(55)], 5.8, a=0.8, r=1.2, bright=3), 4.7, 0.26)
place(sfx, jingle(0.5, 4), 7.6, 0.12, pan=0.3)
for tt in np.arange(8.35, 9.9, 0.3):
    place(sfx, footstep(0.25), tt, 0.12, pan=0.2)
place(sfx, jingle(1.4, 9), 8.4, 0.12, pan=0.1)
for tt in (9.95, 10.2):
    place(sfx, thump(70, 0.25), tt, 0.25)
# midnight: buzz + alert, the music turns
place(sfx, vibrate(0.4), 11.25, 0.32)
place(sfx, alert(), 11.3, 0.34)
place(music, drone(7.0, 46, 0.2), 11.4, 0.22)
place(music, thump(36, 1.2), 12.75, 0.45)
# deadbolt, lamp switch, darkness
place(sfx, load("click.mp3"), 15.45, 0.5)
place(sfx, tick(1800, 0.08, 0.02), 15.6, 0.3)
place(sfx, load("click-soft.mp3"), 17.48, 0.45)
# drip... drip... drip
for tt in (18.62, 19.05, 19.7, 19.95, 20.6, 21.9, 23.3, 24.7, 26.2, 27.6, 29.0, 30.4, 31.8):
    place(sfx, plink(1450 + rng.uniform(-60, 60)), tt, 0.32 if tt < 21 else 0.18, pan=0.35)
place(music, drone(15.0, 41.2, 0.25), 18.3, 0.22)
heartbeat(21.1, 4, 0.9, 0.55)
place(sfx, rustle(1.8), 22.5, 0.12)
# the licks; relief
for tt in (25.15, 25.7):
    place(sfx, lick(), tt, 0.5, pan=-0.2)
place(music, pad([note(48), note(52), note(55), note(60)], 2.0, a=0.3, r=1.2, bright=2), 26.0, 0.2)
# the montage: clock stingers + licks
for tt in (27.86, 30.0, 30.9):
    place(sfx, tick(2600, 0.06, 0.01), tt, 0.25)
    place(music, thump(44, 0.5), tt, 0.35)
for tt in (29.3, 31.8):
    place(sfx, lick(), tt, 0.45, pan=-0.2)
# morning
place(music, pad([note(52), note(55), note(59), note(64)], 3.4, a=0.8, r=1.2, bright=4), 32.45, 0.26)
for tt in (32.7, 33.1, 33.9):
    place(sfx, chirp_bird(), tt, 0.07, pan=0.6)
for tt in (34.6, 35.35):
    place(sfx, plink(1350), tt, 0.3, pan=0.1)
# the shower: Max whimpering and shaking, the drips echo
place(music, drone(5.0, 43.65, 0.3), 35.7, 0.24)
place(sfx, whimper(0.9), 36.0, 0.22, pan=0.3)
place(sfx, whimper(1.1, 820, 500), 37.5, 0.24, pan=0.3)
place(sfx, jingle(1.0, 10), 37.3, 0.14, pan=0.3)
for tt in (36.3, 37.1, 37.9):
    place(sfx, plink(1200), tt, 0.22, pan=0.4)
heartbeat(38.6, 3, 0.7, 0.6)
# the mirror: riser into the hit
place(music, load("riser.mp3")[int(6.5 * SR):], 40.4, 0.3)
place(music, load("impact-bass-2.mp3"), 42.88, 0.55)
place(sfx, load("glitch-1.mp3")[: int(0.3 * SR)], 42.88, 0.3)
place(music, cluster([57, 58, 63, 64, 70], 3.2, 0.005, 1.4), 42.9, 0.42)
# still under my bed
place(music, drone(3.9, 36.7, 0.5), 45.3, 0.3)
t = t_axis(2.0)
eerie = (np.sin(2 * np.pi * 1975 * t) + np.sin(2 * np.pi * 1984 * t)) * 0.3
place(music, eerie * np.minimum(t / 0.6, 1) * np.minimum((2.0 - t) / 0.4, 1), 45.5, 0.05)
place(music, thump(34, 1.2), 47.9, 0.6)
place(sfx, noise_burst(0.8, 500, 3000, 0.4, a=0.3), 47.85, 0.12)
place(sfx, scrape(0.75), 48.35, 0.28, pan=-0.2)
place(music, load("impact-bass-2.mp3"), 49.18, 0.55)
for buf in (music, sfx):
    i0, i1 = int(49.4 * SR), int(49.52 * SR)
    buf[i0:i1] *= 0
# end card
for i, n in enumerate([72, 79, 76, 84]):
    place(music, musicbox(note(n), 1.5), 49.6 + i * 0.4, 0.13, pan=0.2)
place(music, pad([note(45), note(52), note(57)], 2.9, a=0.3, r=1.3, bright=3), 49.55, 0.26)
place(sfx, load("pop.mp3"), 49.88, 0.3)

# ============================== write ==============================
for name, buf, peak in (("music.wav", music, 0.5), ("sfx.wav", sfx, 0.8)):
    m = np.abs(buf).max()
    if m > peak:
        buf *= peak / m
    sf.write(proj / "audio" / name, buf.astype(np.float32), SR, subtype="PCM_16")
    print(name, f"{len(buf) / SR:.2f}s peak {np.abs(buf).max():.2f}")
