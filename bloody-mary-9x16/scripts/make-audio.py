#!/usr/bin/env python3
"""Synthesize the music bed and story SFX for Bloody Mary (all original, generated here).

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
DUR = 48.3
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


def crackle(d, rate=9):
    out = np.zeros(int(d * SR))
    n = int(rate * d)
    for k in range(n):
        c = noise_burst(0.03, 1500, 9000, 0.004) * rng.uniform(0.3, 1.0)
        i = int(rng.uniform(0, d - 0.03) * SR)
        out[i:i + len(c)] += c
    return out


def giggle(d=1.2, muff=True):  # muffled kids' laughter through a door: pulsed formant noise
    t = t_axis(d)
    env = (0.5 + 0.5 * np.sin(2 * np.pi * 6.5 * t + rng.uniform(0, 3))) ** 3 * np.sin(np.pi * t / d)
    s = fft_filter(rng.standard_normal(len(t)), 700, 2200) * env
    s += 0.4 * np.sin(2 * np.pi * np.cumsum(520 + 80 * np.sin(2 * np.pi * 6.5 * t)) / SR) * env
    return muffle(s, 1300) if muff else s


def strike():  # match strike + flare
    a = noise_burst(0.25, 1800, 9000, 0.05, a=0.004)
    b = noise_burst(0.9, 200, 2500, 0.35, a=0.06) * 0.6
    out = np.zeros(int(1.0 * SR))
    out[: len(a)] += a
    out[int(0.08 * SR): int(0.08 * SR) + len(b)] += b[: len(out) - int(0.08 * SR)]
    return out


# ============================== the score ==============================
place(sfx, roomtone(48.3), 0.0, 0.04)
# hook: candle, a detuned lullaby, low drone
mary = [69, 72, 71, 69, 64, 65, 64, 62]
for i, tt in enumerate(np.arange(0.15, 3.0, 0.42)):
    place(music, musicbox(note(mary[i % 8]) * 0.992, 1.4), tt, 0.15, pan=0.2 * np.sin(i))
place(music, drone(3.2, 46, 0.2), 0.0, 0.2)
place(sfx, crackle(3.0), 0.0, 0.1, pan=0.3)
# sleepover: playful plucks in the hallway, a giggle
for i, tt in enumerate(np.arange(3.05, 6.6, 0.24)):
    n = [69, 72, 76, 72, 74, 71, 67, 71][i % 8]
    place(music, pluck(note(n), 0.3), tt, 0.22, pan=0.25 * np.sin(i * 1.3))
place(sfx, giggle(1.4, muff=False), 4.7, 0.16, pan=-0.3)
place(sfx, giggle(1.0, muff=False), 5.3, 0.14, pan=0.35)
# lights off, the match, the candle
place(sfx, load("click.mp3"), 7.1, 0.5)
place(sfx, strike(), 7.78, 0.35, pan=0.3)
place(sfx, crackle(7.0), 8.0, 0.1, pan=0.3)
place(music, drone(6.8, 41.2, 0.18), 8.0, 0.22)
place(music, pad([note(45), note(48), note(53)], 6.8, a=1.5, r=1.0, bright=3), 8.0, 0.22)
heartbeat(12.2, 3, 0.95, 0.5)
# the chant: a low boom and the flame shivering after each name
for tt in (15.72, 17.63):
    place(music, thump(36, 1.3), tt, 0.6)
    place(sfx, noise_burst(0.5, 300, 2500, 0.25, a=0.05), tt + 0.05, 0.12, pan=0.3)
place(sfx, crackle(5.0, 6), 15.0, 0.08, pan=0.3)
# I stopped: strings tighten, heart races
place(music, cluster([57, 58, 63], 3.1, 0.3, 2.5), 18.4, 0.22)
heartbeat(18.6, 4, 0.72, 0.6)
# giggles through the door
for tt, pn in ((21.6, -0.2), (22.4, 0.2), (23.0, -0.1)):
    place(sfx, giggle(1.1), tt, 0.3, pan=pn)
# the reflection: everything drops, a swell, the hit
place(music, load("riser.mp3")[int(6.0 * SR):], 24.6, 0.3)
place(music, load("impact-bass-2.mp3"), 26.7, 0.55)
place(sfx, load("glitch-1.mp3")[: int(0.35 * SR)], 26.7, 0.3)
place(music, cluster([56, 57, 62, 63, 69], 3.4, 0.005, 1.6), 26.72, 0.42)
t = t_axis(3.3)
eerie = (np.sin(2 * np.pi * 1975 * t) + np.sin(2 * np.pi * 1986 * t)) * 0.3
place(music, eerie * np.minimum(t / 0.6, 1) * np.minimum((3.3 - t) / 0.5, 1), 28.7, 0.05)
place(music, drone(3.3, 36.7, 0.5), 28.7, 0.3)
# out the door: bang, running feet
place(sfx, thump(60, 0.4), 32.12, 0.6)
place(sfx, creak(0.4, 120, 90), 32.14, 0.25)
for k, tt in enumerate(np.arange(32.2, 33.25, 0.2)):
    place(sfx, footstep(0.7), tt, 0.4, pan=0.1)
place(music, pad([note(45), note(48), note(52)], 5.9, a=0.5, r=1.0, bright=3), 32.2, 0.2)
heartbeat(33.4, 5, 0.85, 0.5)
# looking back
place(music, load("riser.mp3")[int(6.8 * SR):], 38.0, 0.24)
place(music, drone(5.2, 34.6, 0.4), 40.0, 0.3)
place(sfx, crackle(5.0, 5), 40.0, 0.08)
# the wave: one music-box note bending down; the candle goes out; silence
t = t_axis(1.6)
bend = np.sin(2 * np.pi * np.cumsum(note(76) * (1 - 0.06 * t / 1.6)) / SR) * np.exp(-t / 0.9)
place(music, bend, 43.65, 0.16)
place(sfx, noise_burst(0.35, 400, 3000, 0.12, a=0.01), 44.93, 0.3)
place(music, thump(34, 1.0), 44.95, 0.55)
for buf in (music, sfx):
    i0, i1 = int(45.05 * SR), int(45.3 * SR)
    buf[i0:i1] *= np.linspace(1, 0, i1 - i0)[:, None]
    buf[i1:int(45.35 * SR)] *= 0
# end card
for i, n in enumerate(mary[:6]):
    place(music, musicbox(note(n), 1.4), 45.4 + i * 0.42, 0.13, pan=0.2)
place(music, pad([note(45), note(52), note(57)], 2.9, a=0.3, r=1.3, bright=3), 45.35, 0.24)
place(sfx, load("pop.mp3"), 45.68, 0.3)

# ============================== write ==============================
for name, buf, peak in (("music.wav", music, 0.5), ("sfx.wav", sfx, 0.8)):
    m = np.abs(buf).max()
    if m > peak:
        buf *= peak / m
    sf.write(proj / "audio" / name, buf.astype(np.float32), SR, subtype="PCM_16")
    print(name, f"{len(buf) / SR:.2f}s peak {np.abs(buf).max():.2f}")
