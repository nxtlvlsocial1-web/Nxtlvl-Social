#!/usr/bin/env python3
"""Synthesize the score and SFX for Two True Stories: The Watcher & The Enfield Poltergeist (all original).

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
DUR = 370.0
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


def cordless_ring(at, until, gain=0.3):  # electronic trill bursts
    tt = at
    while tt < until:
        d = 0.9
        t = t_axis(d)
        trill = np.sign(np.sin(2 * np.pi * 18 * t))
        f = np.where(trill > 0, 1180, 940)
        s_ = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(t / 0.01, 1) * np.minimum((d - t) / 0.02, 1)
        place(sfx, fft_filter(s_, 300, 5000), tt, gain, pan=0.15)
        tt += 2.2


def dtmf(key, d=0.16):
    rows = {"1": (697, 1209), "9": (852, 1477), "0": (941, 1336)}
    a, b = rows[key]
    t = t_axis(d)
    return (np.sin(2 * np.pi * a * t) + np.sin(2 * np.pi * b * t)) * 0.4 * np.minimum(t / 0.005, 1) * np.minimum((d - t) / 0.01, 1)


def dial_tone(d):
    t = t_axis(d)
    return (np.sin(2 * np.pi * 350 * t) + np.sin(2 * np.pi * 440 * t)) * 0.3 * np.minimum(t / 0.02, 1) * np.minimum((d - t) / 0.05, 1)


def ringback(at, n=2):
    for k in range(n):
        t = t_axis(1.2)
        s_ = (np.sin(2 * np.pi * 440 * t) + np.sin(2 * np.pi * 480 * t)) * 0.25
        place(sfx, muffle(s_, 2400), at + k * 1.6, 0.18)


def chuckle(d=1.3):  # low, breathy laugh over the phone
    t = t_axis(d)
    env = (0.5 + 0.5 * np.sin(2 * np.pi * 4.2 * t)) ** 4 * np.sin(np.pi * t / d)
    s_ = fft_filter(rng.standard_normal(len(t)), 250, 1600) * env
    s_ += 0.5 * np.sin(2 * np.pi * np.cumsum(140 + 30 * np.sin(2 * np.pi * 4.2 * t)) / SR) * env
    return fft_filter(s_, 300, 3200)


def tv_murmur(d):
    t = t_axis(d)
    env = 0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 2.7 * t) * np.sin(2 * np.pi * 0.9 * t + 1))
    s_ = fft_filter(rng.standard_normal(len(t)), 300, 2600) * env
    return s_ / (np.abs(s_).max() + 1e-9) * np.minimum(t / 0.3, 1) * np.minimum((d - t) / 0.3, 1)


# ============================== the score ==============================
def whirr(d=0.55):  # smart-lock motor
    t = t_axis(d)
    f = 210 + 60 * np.minimum(t / d, 1)
    sq = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR))
    return fft_filter(sq, 150, 2600) * np.minimum(t / 0.03, 1) * np.minimum((d - t) / 0.05, 1) * 0.5


def clunk():
    out = np.zeros(int(0.5 * SR))
    a = thump(95, 0.3) * 0.9
    b = noise_burst(0.12, 600, 5000, 0.02) * 0.6
    out[: len(a)] += a
    out[: len(b)] += b
    return out


def ding_dong(at, gain=0.2, slow=1.0, detune=0.0):  # a doorbell, the film's motif
    place(music, bell(note(76) * 2 ** (detune / 12), 3.2), at, gain, pan=-0.1)
    place(music, bell(note(72) * 2 ** (detune / 12), 4.0), at + 0.62 * slow, gain, pan=0.1)


def wind(d):
    t = t_axis(d)
    s = fft_filter(rng.standard_normal(len(t)), 120, 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.31 * t) * np.sin(2 * np.pi * 0.13 * t + 1))
    return s / (np.abs(s).max() + 1e-9) * np.minimum(t / 0.6, 1) * np.minimum((d - t) / 0.6, 1)


def cam_hiss(d):  # the camera feed's noise floor
    t = t_axis(d)
    s = fft_filter(rng.standard_normal(len(t)), 2500, 9000) * 0.5 + 0.2 * np.sin(2 * np.pi * 60 * t)
    return s / (np.abs(s).max() + 1e-9) * np.minimum(t / 0.05, 1) * np.minimum((d - t) / 0.05, 1)



def piano(f, d=2.4, bright=1.0):
    t = t_axis(d)
    s = sum(np.sin(2 * np.pi * f * h * t + h) * (0.55 ** (h - 1)) * np.exp(-t * (1.4 + h * 0.9)) for h in range(1, 7))
    return s * np.minimum(t / 0.004, 1) * bright * 0.6


def motif(at, notes, step=0.62, gain=0.16, d=2.6, oct=0, pan=0.0):
    for i, n in enumerate(notes):
        if n is None:
            continue
        place(music, piano(note(n + oct), d), at + i * step, gain, pan=pan + 0.15 * np.sin(i))


def bed(at, dur, chord, gain=0.2, bright=3, a=2.0, r=2.0):
    place(music, pad([note(n) for n in chord], dur, a=a, r=r, bright=bright), at, gain)


def birds(at, dur, every=1.6, gain=0.06):
    for tt in np.arange(at, at + dur, every):
        place(sfx, chirp_bird(), tt + rng.uniform(0, 0.8), gain, pan=rng.uniform(-0.7, 0.7))


def knock(at, gain=0.8, pan=-0.3):
    place(sfx, thump(78, 0.4) * 0.9 + noise_burst(0.4, 300, 2500, 0.05) * 0.5, at, gain, pan=pan)


def typing(at, until, rate=11, gain=0.12):
    for tt in np.arange(at, until, 1 / rate):
        place(sfx, tick(rng.uniform(1700, 2400), 0.04, 0.006) + noise_burst(0.04, 1500, 6000, 0.008) * 0.4, tt + rng.uniform(0, 0.03), gain)


def footsteps(at, until, every=0.42, gain=0.3, heavy=1.0, pan=0.0):
    for tt in np.arange(at, until, every):
        place(sfx, footstep(heavy), tt, gain, pan=pan)


def static(d):
    t = t_axis(d)
    s = fft_filter(rng.standard_normal(len(t)), 900, 7000) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 0.7 * t)))
    tone = np.sin(2 * np.pi * np.cumsum(600 + 500 * np.sin(2 * np.pi * 0.35 * t)) / SR) * 0.15
    return (s / (np.abs(s).max() + 1e-9) + tone) * np.minimum(t / 0.05, 1) * np.minimum((d - t) / 0.1, 1)


def uk_ring(at, n=2, gain=0.22):  # British double ring
    for k in range(n):
        for j in (0, 0.6):
            t = t_axis(0.4)
            s_ = (np.sin(2 * np.pi * 400 * t) + np.sin(2 * np.pi * 450 * t)) * 0.5 * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 20 * t)))
            place(sfx, fft_filter(s_, 300, 4000) * np.minimum(t / 0.01, 1), at + k * 3.0 + j, gain, pan=-0.3)


def whoop(at, gain=0.25):  # a short police chirp
    t = t_axis(0.7)
    f = 700 + 900 * np.sin(np.pi * t / 0.7)
    place(sfx, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.7), at, gain, pan=0.3)


def flash(at, gain=0.3):
    place(sfx, load("pop.mp3"), at, gain)
    t = t_axis(0.9)
    place(sfx, np.sin(2 * np.pi * np.cumsum(2500 + 3500 * t) / SR) * np.exp(-t / 0.3) * 0.15, at + 0.05, gain)


def tape_hiss(d):
    t = t_axis(d)
    s = fft_filter(rng.standard_normal(len(t)), 3000, 10000) * 0.6 + 0.25 * np.sin(2 * np.pi * 50 * t)
    return s / (np.abs(s).max() + 1e-9) * np.minimum(t / 0.2, 1) * np.minimum((d - t) / 0.2, 1)


def sting(at, gain=0.5, notes=(57, 58, 63, 64)):
    place(music, load("impact-bass-2.mp3"), at, gain)
    place(music, cluster(list(notes), 2.6, 0.005, 1.3), at + 0.02, 0.3)


W_MOTIF = [62, 65, 69, 68, None, 65, 64, 62]       # the Watcher: D F A G#  F E D
E_MOTIF = [74, 72, 71, 67, None, 69, 71, 64]       # Enfield: a 70s music-box turn
place(sfx, roomtone(370.0), 0.0, 0.04)

# ---------------- COLD OPEN (0-35) ----------------
birds(0.0, 5.2, 1.2, 0.07)
bed(0.0, 12.5, [50, 57, 62, 65], 0.18)
motif(0.4, W_MOTIF[:4], 0.9, 0.14)
place(sfx, creak(0.6, 140, 210), 5.85, 0.16, pan=0.2)
place(sfx, rustle(0.6), 7.5, 0.12)
place(music, load("riser.mp3")[int(7.6 * SR):], 9.6, 0.2)
sting(11.0, 0.5)
place(sfx, wind(9.0), 12.3, 0.12)
place(music, drone(9.2, 41.2, 0.2), 12.3, 0.26)
place(sfx, scrape(1.8), 18.9, 0.45, pan=-0.1)
sting(20.62, 0.45, (56, 57, 62, 63))
bed(21.0, 10.6, [45, 52, 57, 60], 0.18)
place(sfx, load("whoosh-cinematic.mp3"), 25.5, 0.14)
motif(26.2, W_MOTIF, 0.62, 0.11, pan=-0.2)
motif(30.0, E_MOTIF[:4], 0.5, 0.08, oct=-12, pan=0.2)
place(music, load("riser.mp3")[int(5.5 * SR):], 31.4, 0.24)
place(music, load("impact-bass-1.mp3"), 35.2, 0.5)
place(music, thump(36, 1.4), 35.2, 0.5)
# ---------------- CHAPTER 1: THE WATCHER ----------------
bed(35.2, 3.4, [38, 45, 50], 0.2)
# Westfield by day: warm piano, birds
birds(38.3, 23.0, 1.7, 0.06)
bed(38.0, 12.0, [50, 57, 62, 66], 0.16, a=1.5)
bed(49.5, 12.0, [47, 54, 59, 62], 0.16, a=1.5)
bed(61.0, 11.4, [43, 50, 55, 59], 0.15, a=1.5)
for i, at in enumerate(np.arange(38.6, 71.5, 4.8)):
    motif(at, [74, 69, 66, 62] if i % 2 == 0 else [71, 66, 62, 59], 0.6, 0.075, pan=0.15)
for tt in np.arange(61.8, 65.3, 0.48):
    place(sfx, rustle(0.4), tt, 0.06, pan=0.2)
footsteps(65.6, 68.2, 0.45, 0.22)
place(sfx, creak(0.5, 160, 230), 68.5, 0.14, pan=0.2)
place(sfx, rustle(0.5), 69.6, 0.12)
# the first letter: everything drops away, a ticking clock, typewriter keys
bed(72.1, 11.0, [50, 53, 57, 60], 0.17)
place(music, drone(28, 36.7, 0.3), 72.2, 0.24)
typing(72.4, 76.0, 12, 0.1)
place(music, thump(40, 1.0), 76.6, 0.42)
typing(77.9, 82.9, 9, 0.08)
heartbeat(78.0, 6, 0.95, 0.35)
place(sfx, crackle(5.9, 6), 83.15, 0.06)
motif(83.4, W_MOTIF, 0.9, 0.1, oct=-12)
place(sfx, wind(3.0), 89.0, 0.12)
place(music, cluster([50, 51, 56], 4.6, 0.6, 3.0), 91.0, 0.22)
sting(96.1, 0.42)
whoop(97.9, 0.22)
whoop(98.9, 0.18)
# a prank? unease, a pulse
place(music, drone(34, 43.65, 0.25), 99.7, 0.22)
for k, at in enumerate(np.arange(100.0, 133.0, 0.857)):
    place(music, thump(46, 0.35), at, 0.16 if k % 4 else 0.24)
bed(99.7, 12.0, [46, 53, 58, 61], 0.15)
bed(111.4, 12.0, [44, 51, 56, 59], 0.15)
bed(123.0, 11.0, [46, 53, 58, 62], 0.14)
place(sfx, creak(0.3, 200, 260), 107.05, 0.18, pan=0.2)
place(sfx, creak(0.5, 160, 230), 107.85, 0.14, pan=0.2)
place(sfx, rustle(0.5), 109.8, 0.1)
place(sfx, giggle(2.2, True), 112.4, 0.12, pan=0.4)
place(music, cluster([55, 56, 61], 4.0, 0.4, 2.6), 114.8, 0.2)
place(sfx, load("click.mp3"), 127.3, 0.28)
motif(128.6, W_MOTIF, 0.7, 0.08)
# investigation and the sale
bed(134.0, 16.0, [50, 53, 57, 62], 0.15)
bed(150.0, 13.0, [46, 50, 53, 58], 0.15)
bed(163.0, 11.0, [43, 50, 55, 58], 0.15)
for i, at in enumerate(np.arange(134.4, 172.0, 5.0)):
    motif(at, W_MOTIF[:4] if i % 2 == 0 else [65, 64, 62, None], 0.62, 0.07, pan=-0.1)
footsteps(157.8, 160.2, 0.44, 0.2)
place(music, load("impact-bass-1.mp3"), 162.0, 0.4)
place(sfx, load("click.mp3"), 162.0, 0.3)
place(sfx, load("whoosh-short.mp3"), 164.5, 0.12)
place(sfx, load("pop.mp3"), 167.1, 0.22)
place(sfx, load("pop.mp3"), 167.85, 0.22)
place(music, drone(13, 38.9, 0.4), 170.4, 0.26)
place(music, load("riser.mp3")[int(6.0 * SR):], 178.0, 0.24)
sting(180.0, 0.55, (57, 58, 63, 64, 70))
place(sfx, load("glitch-1.mp3")[: int(0.3 * SR)], 180.0, 0.18)
# across the ocean
place(sfx, load("whoosh-cinematic.mp3"), 182.9, 0.2)
bed(182.9, 11.5, [50, 57, 62, 66, 69], 0.16, bright=4, a=1.0)
for i, at in enumerate(np.arange(183.2, 193.0, 0.31)):
    place(music, piano(note([62, 66, 69, 74, 78, 74, 69, 66][i % 8]), 1.2), at, 0.05, pan=0.3 * np.sin(i))
place(sfx, tap(1.0), 189.4, 0.2)
place(sfx, tap(1.0), 189.75, 0.2)
# ---------------- CHAPTER 2: ENFIELD ----------------
place(music, load("impact-bass-1.mp3"), 194.1, 0.5)
place(music, thump(36, 1.4), 194.1, 0.5)
bed(194.1, 4.2, [40, 47, 52], 0.2)
birds(198.3, 6.0, 1.6, 0.05)
place(sfx, wind(12.0), 198.25, 0.08)
bed(198.2, 12.0, [52, 59, 64, 67], 0.15, a=1.2)
for i, at in enumerate(np.arange(198.6, 209.5, 2.6)):
    for j, n in enumerate(E_MOTIF[:4] if i % 2 == 0 else E_MOTIF[5:]):
        place(music, musicbox(note(n) * 2 ** (-0.15 / 12), 1.4), at + j * 0.42, 0.09, pan=0.2)
# night: the beds, the knocks, the chest
place(music, drone(39, 41.2, 0.2), 210.1, 0.28)
bed(210.1, 21.0, [45, 48, 52, 56], 0.14)
place(sfx, crackle(2.4, 14), 211.0, 0.12)
place(sfx, fft_filter(rng.standard_normal(int(2.4 * SR)), 30, 200) * 0.5, 211.0, 0.3)
for k in (214.0, 215.0, 215.9, 216.6, 217.3):
    knock(k, 0.75, pan=-0.5)
place(sfx, load("click.mp3"), 218.35, 0.25)
footsteps(218.7, 220.4, 0.48, 0.24, pan=0.4)
place(sfx, scrape(2.5), 222.2, 0.55)
sting(224.6, 0.38, (56, 57, 62))
for at in (226.0, 227.2, 228.6, 229.8):
    place(sfx, scrape(0.5), at, 0.3)
    place(sfx, creak(0.4, 80, 110), at + 0.1, 0.16)
footsteps(231.1, 233.4, 0.36, 0.2, pan=0.2)
for k in (234.6, 235.4, 236.2):
    knock(k, 0.6, pan=0.4)
place(sfx, load("click.mp3"), 237.05, 0.3)
for tt in np.arange(237.6, 238.5, 0.07):
    place(sfx, tick(1800, 0.03, 0.006), tt, 0.12)
footsteps(238.8, 241.4, 0.5, 0.22, heavy=1.1)
place(sfx, crackle(1.2, 20), 242.2, 0.18)
place(sfx, scrape(1.3), 243.3, 0.35)
place(music, cluster([57, 58, 63], 3.0, 0.2, 2.0), 245.0, 0.22)
sting(247.3, 0.45)
# the months that followed: a driving pulse, toys, chairs, flashes
place(music, drone(21, 38.9, 0.5), 249.5, 0.22)
for k, at in enumerate(np.arange(249.6, 271.0, 0.5)):
    place(music, thump(44, 0.3), at, 0.2 if k % 2 == 0 else 0.1)
bed(249.5, 11.0, [45, 52, 57, 60], 0.14)
bed(260.5, 11.0, [43, 50, 55, 58], 0.14)
for i in range(6):
    place(sfx, load("whoosh-short.mp3"), 249.9 + i * 0.28, 0.1, pan=0.3)
    place(sfx, tick(900, 0.08, 0.03), 250.8 + i * 0.28, 0.25)
place(sfx, thump(70, 0.5) + noise_burst(0.5, 400, 4000, 0.1), 253.45, 0.6)
flash(255.9, 0.32)
flash(257.6, 0.32)
place(sfx, tv_murmur(3.8), 258.8, 0.08)
place(sfx, hvac(8.4), 262.8, 0.05)
# Bill
place(music, drone(13, 36.7, 0.6), 271.2, 0.3)
t_ = t_axis(12.8)
place(music, (np.sin(2 * np.pi * 1975 * t_) + np.sin(2 * np.pi * 1987 * t_)) * 0.3 * np.minimum(t_ / 1.0, 1) * np.minimum((12.8 - t_) / 1.0, 1), 271.2, 0.05)
place(sfx, tape_hiss(5.2), 279.0, 0.08)
place(music, thump(34, 1.4), 279.2, 0.45)
place(sfx, static(3.6), 284.2, 0.12)
uk_ring(288.1, 1, 0.22)
place(sfx, load("click.mp3"), 289.3, 0.25)
place(sfx, crackle(3.8, 6), 291.0, 0.06)
motif(291.2, E_MOTIF, 0.5, 0.07, oct=-12)
sting(295.1, 0.32, (57, 62, 63))
# the sceptics: lighter, ticking
bed(296.8, 18.0, [48, 55, 60, 64], 0.13)
for tt in np.arange(297.0, 314.6, 0.5):
    place(sfx, tick(2300, 0.04, 0.008), tt, 0.07)
place(sfx, hvac(5.8), 296.8, 0.06)
flash(307.42, 0.35)
for at in (311.05, 312.25, 313.45):
    place(sfx, boing(300, 120, 0.5), at, 0.18)
bed(314.7, 7.0, [45, 52, 57, 61], 0.15)
motif(315.0, W_MOTIF[:4], 0.8, 0.07)
motif(318.4, E_MOTIF[:4], 0.6, 0.07)
# it faded away
birds(321.3, 4.0, 1.4, 0.05)
bed(321.2, 9.4, [50, 57, 62, 66], 0.14)
place(sfx, wind(5.0), 325.5, 0.1)
# ---------------- OUTRO ----------------
bed(330.6, 13.0, [50, 57, 62, 65], 0.15)
bed(343.5, 13.0, [46, 53, 58, 62], 0.15)
place(sfx, load("click.mp3"), 333.6, 0.22)
place(sfx, load("click.mp3"), 334.6, 0.22)
motif(331.2, W_MOTIF, 0.62, 0.09, pan=-0.3)
motif(336.2, E_MOTIF, 0.55, 0.08, pan=0.3)
place(sfx, load("pop.mp3"), 340.3, 0.2)
place(sfx, load("pop.mp3"), 340.45, 0.2)
motif(345.4, W_MOTIF[:4], 0.62, 0.07)
place(sfx, load("click-soft.mp3"), 352.0, 0.3)
place(sfx, bell(1318.5, 1.2), 352.6, 0.1)
place(sfx, creak(0.45, 220, 300), 355.2, 0.22, pan=0.2)
place(music, thump(38, 1.2), 355.6, 0.45)
place(music, load("impact-bass-1.mp3"), 355.6, 0.35)
# end screen: a slow doorbell, then fade
ding_dong(356.6, 0.16, slow=1.6, detune=-0.4)
bed(356.4, 13.4, [50, 57, 62], 0.15, a=1.0, r=4.0)
motif(359.0, W_MOTIF, 0.8, 0.07)

# ============================== write ==============================
for name, buf, peak in (("music.wav", music, 0.5), ("sfx.wav", sfx, 0.8)):
    m = np.abs(buf).max()
    if m > peak:
        buf *= peak / m
    sf.write(proj / "audio" / name, buf.astype(np.float32), SR, subtype="PCM_16")
    print(name, f"{len(buf) / SR:.2f}s peak {np.abs(buf).max():.2f}")
