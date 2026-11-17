#!/usr/bin/env python3
"""Synthesize the music bed and story SFX for Respawn (all original, generated here).

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
DUR = 54.0
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


# ---- extra synths for Respawn ---------------------------------------------------------
def siren(d, f_lo=640, f_hi=960, rate=0.55):
    t = t_axis(d)
    f = np.where((t / rate) % 2 < 1, f_lo, f_hi).astype(float)
    f = fft_filter(f, None, 30)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(2 * np.pi * 2 * np.cumsum(f) / SR)
    return s * np.minimum(t / 0.1, 1) * np.minimum((d - t) / 0.2, 1)


def engine(d, f0=55, f1=95):
    t = t_axis(d)
    f = np.interp(t, [0, d], [f0, f1])
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sign(np.sin(ph)) * 0.5 + np.sin(2 * ph) * 0.3 + fft_filter(rng.standard_normal(len(t)), 80, 600) * 0.4
    return fft_filter(s, 40, 1800) * np.minimum(t / 0.15, 1) * np.minimum((d - t) / 0.2, 1)


def screech(d=0.7):
    t = t_axis(d)
    f = 2600 + 500 * np.sin(2 * np.pi * 11 * t)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4 + fft_filter(rng.standard_normal(len(t)), 1800, 6000) * 0.6
    return s * np.minimum(t / 0.03, 1) * np.minimum((d - t) / 0.12, 1)


def crash(d=1.6):
    t = t_axis(d)
    glass = grains(d, 1400, 3000, 12000, 0.35, 0.002)
    metal = sum(np.sin(2 * np.pi * f * t) * np.exp(-t / tau) for f, tau in ((310, 0.25), (527, 0.18), (813, 0.12), (1190, 0.08)))
    body = noise_burst(d, 40, 900, 0.22) * 1.6
    th = np.zeros(len(t))
    k = thump(42, 0.8)
    th[: len(k)] = k[: len(t)]
    return body + glass * 0.7 + metal * 0.25 + th * 1.2


def rain(d):
    t = t_axis(d)
    s = fft_filter(rng.standard_normal(len(t)), 1200, 9000) * 0.6 + fft_filter(rng.standard_normal(len(t)), 200, 1200) * 0.3
    return s / (np.abs(s).max() + 1e-9) * np.minimum(t / 0.3, 1) * np.minimum((d - t) / 0.3, 1)


def waves(d):
    t = t_axis(d)
    s = fft_filter(rng.standard_normal(len(t)), 150, 2400) * (0.35 + 0.65 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.16 * t - 1.2)) ** 2)
    return s / (np.abs(s).max() + 1e-9) * np.minimum(t / 0.4, 1) * np.minimum((d - t) / 0.4, 1)


def gull(d=0.5):
    t = t_axis(d)
    f = np.interp(t, [0, 0.12, d], [1500, 2100, 1300])
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    return fft_filter(s, 600, 5000) * np.sin(np.pi * t / d) ** 2


def horn(d, f=330):
    t = t_axis(d)
    s = sum(np.sign(np.sin(2 * np.pi * ff * t)) * a for ff, a in ((f, 0.5), (f * 1.26, 0.4)))
    return fft_filter(s, 150, 2400) * np.minimum(t / 0.02, 1) * np.minimum((d - t) / 0.05, 1)


def ring(d, f=6400):
    t = t_axis(d)
    return np.sin(2 * np.pi * f * t) * np.minimum(t / 0.05, 1) * np.exp(-t / (d * 0.6))


def static(d, k=1.0):
    t = t_axis(d)
    s = fft_filter(rng.standard_normal(len(t)), 900, 7000) * 0.6 + grains(d, 500, 2000, 8000, 99, 0.01) * 0.6
    return s / (np.abs(s).max() + 1e-9) * k * np.minimum(t / 0.05, 1) * np.minimum((d - t) / 0.08, 1)


def tune_chirp(d=0.18, f0=900, f1=2400):
    t = t_axis(d)
    f = np.interp(t, [0, d], [f0, f1])
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d)


def whiteout(d):
    """the respawn: a bright reversed swell that snaps off"""
    t = t_axis(d)
    s = fft_filter(rng.standard_normal(len(t)), 2000, 12000) * (t / d) ** 2.2
    s += sum(np.sin(2 * np.pi * f * t) for f in (1568, 2093, 2637)) * 0.15 * (t / d) ** 3
    return s


def piano(f, d=2.4, bright=1.0):
    t = t_axis(d)
    s = sum(np.sin(2 * np.pi * f * h * t + h) * np.exp(-t * (0.9 + h * 0.7)) / h ** (1.2 / bright) for h in range(1, 7))
    return s * np.minimum(t / 0.004, 1) * 0.5


def synthwave(at, dur, chords, bpm=96, drums=True, lp=None, gain=1.0):
    """warm retro loop: pads, a bass pulse, a plucked arp, kick/snare/hats"""
    beat = 60 / bpm
    bar = 4 * beat
    buf = np.zeros((int((dur + 3) * SR), 2))
    for i, ch in enumerate(chords * 8):
        b0 = i * bar
        if b0 >= dur:
            break
        place(buf, pad([note(n) for n in ch], bar + 0.6, a=0.25, r=0.5, bright=4), b0, 0.55)
        for k in range(8):
            place(buf, pluck(note(ch[0] - 24), 0.3, 0.6), b0 + k * beat / 2, 0.45)
            arp = ch[[0, 1, 2, 1][k % 4]] + 12
            place(buf, pluck(note(arp), 0.25, 1.4), b0 + k * beat / 2 + beat / 4, 0.13, pan=0.35 * (1 if k % 2 else -1))
        if drums:
            for k in range(4):
                place(buf, thump(52, 0.35) * 1.3, b0 + k * beat, 0.5 if k % 2 == 0 else 0.0)
                if k % 2:
                    place(buf, noise_burst(0.22, 1200, 6000, 0.07), b0 + k * beat, 0.32)
                for h in range(2):
                    place(buf, tick(8000, 0.03, 0.008), b0 + k * beat + h * beat / 2, 0.06, pan=0.4)
    buf = buf[: int(dur * SR)]
    if lp:
        for c in range(2):
            buf[:, c] = fft_filter(buf[:, c], None, lp)
    t = np.arange(len(buf)) / SR
    fade = np.minimum(t / 0.05, 1) * np.minimum((dur - t) / 0.4, 1)
    buf *= fade[:, None] * gain
    i = int(at * SR)
    music[i:i + len(buf)] += buf[: len(music) - i]


AM, F_, C_, G_ = [57, 60, 64], [53, 57, 60], [48, 52, 55, 59], [55, 59, 62]
# 0.0 - 9.2  the city: a warm sunset groove under the respawns
synthwave(0.0, 9.25, [AM, F_, C_, G_], gain=0.9)
for tt in (0.55, 7.0):  # respawn: beep on waking
    place(sfx, beep(1046, 0.16), tt, 0.32)
place(sfx, load("whoosh-cinematic.mp3"), 0.0, 0.12)
place(sfx, waves(9.0), 0.0, 0.03, pan=0.6)
# 4.75 car crash into the palm
place(sfx, engine(0.75, 70, 120), 4.75, 0.5)
place(sfx, screech(0.5), 4.98, 0.32, pan=-0.2)
place(sfx, crash(1.4), 5.38, 0.75)
place(sfx, whiteout(0.25), 5.55, 0.35)
# 5.8 police chase
place(sfx, engine(1.0, 90, 130), 5.8, 0.55)
place(sfx, siren(1.0), 5.8, 0.24, pan=-0.3)
place(sfx, whiteout(0.22), 6.58, 0.35)
# 6.8 back on the steps
place(sfx, noise_burst(0.6, 200, 1500, 0.2), 6.85, 0.08)
# 9.2 the city empties: the groove drains away, cars blink out
place(music, drone(9.8, 41, 0.12), 9.2, 0.3)
place(music, pad([note(45), note(52), note(56)], 9.8, a=1.2, r=1.5, bright=3), 9.2, 0.18)
for i in range(9):
    place(sfx, load("glitch-3.mp3")[: int(0.12 * SR)], 9.2 + (0.12 + i * 0.09) * 3.15, 0.07, pan=rng.uniform(-0.6, 0.6))
place(sfx, wind(9.6), 9.3, 0.12)
for tt in np.arange(12.35, 13.45, 0.625):  # the yellow light's relay
    place(sfx, tick(1800, 0.05, 0.01), tt, 0.16)
place(sfx, waves(1.4), 13.4, 0.22, pan=0.4)
place(sfx, gull(0.5), 13.7, 0.06, pan=-0.5)
heartbeat(14.8, 4, 0.95, 0.42)
place(music, cluster([45, 46, 51], 4.2, 0.6, 2.4), 14.7, 0.16)
# 18.3 every head turns at once
place(music, load("impact-bass-2.mp3"), 18.22, 0.55)
place(sfx, load("glitch-2.mp3")[: int(0.3 * SR)], 18.2, 0.24)
place(music, cluster([57, 58, 63, 64], 1.6, 0.005, 1.0), 18.22, 0.3)
# 18.95 the radio: scanning static, tuning chirps
place(sfx, static(5.6, 1.0), 18.95, 0.13)
for tt in np.arange(19.1, 20.6, 0.21):
    place(sfx, tune_chirp(0.12, rng.uniform(700, 1200), rng.uniform(1800, 2800)), tt, 0.05)
place(music, drone(5.3, 36.7, 0.4), 18.95, 0.26)
# 23.3 the sky flickers into a ceiling
for a in (0.18, 0.26, 0.5, 0.58, 0.64):
    place(sfx, load("glitch-1.mp3")[: int(0.08 * SR)], 23.3 + a * 1.0, 0.14)
place(sfx, beep(1046, 0.16), 23.75, 0.12)
# 24.3 the visor, her photo: tender
place(sfx, load("click-soft.mp3"), 24.4, 0.3)
place(music, pad([note(48), note(55), note(62), note(64)], 3.9, a=0.5, r=1.2, bright=3), 24.3, 0.22)
for i, n in enumerate([76, 74, 72, 67, 69, 72]):
    place(music, piano(note(n), 2.2), 24.5 + i * 0.6, 0.12)
# 28.05 respawn, the heartbeat line across the sky
place(sfx, whiteout(0.3), 27.78, 0.3)
place(sfx, beep(1046, 0.16), 28.3, 0.3)
for tt in (29.44, 29.92, 30.42):
    place(sfx, beep(1046, 0.18), tt, 0.42)
place(music, cluster([62, 63, 69], 2.8, 0.4, 2.0), 28.05, 0.16)
# 30.85 the real monitor, the real room
place(sfx, roomtone(2.2), 30.85, 0.08)
for tt in (30.93, 32.39):
    place(sfx, beep(988, 0.16), tt, 0.34)
place(music, drone(2.2, 49, 0.1), 30.85, 0.18)
# 33.0 the real day: rain, wipers, the engine, then the truck
place(sfx, rain(4.65), 33.0, 0.22)
place(sfx, engine(4.65, 42, 46), 33.0, 0.16)
for tt in np.arange(33.0, 37.5, np.pi / 2.4):
    place(sfx, thump(120, 0.12) * 0.6, tt + 0.62, 0.12)
    place(sfx, noise_burst(0.1, 400, 2000, 0.03), tt + 0.62, 0.12)
place(music, pad([note(45), note(48), note(52)], 4.6, a=0.8, r=0.6, bright=2), 33.0, 0.14)
place(music, load("riser.mp3")[int(5.0 * SR):], 35.9, 0.22)
place(sfx, horn(1.3, 300), 36.2, 0.18)
place(sfx, horn(0.9, 300), 36.65, 0.34)
place(sfx, screech(0.6), 37.05, 0.4)
place(sfx, crash(1.0), 37.6, 0.85)
for buf in (music, sfx):  # the world drops out
    buf[int(37.72 * SR): int(38.1 * SR)] *= 0.0
place(sfx, ring(1.6), 37.7, 0.05)
# 37.85 the city wants him back: the groove, slowed and warm, no drums
synthwave(37.95, 3.6, [F_, C_], bpm=80, drums=False, lp=3500, gain=0.8)
for k in range(10):
    place(sfx, noise_burst(0.12, 200, 1800, 0.04), 38.2 + k * 0.32, 0.05, pan=rng.uniform(-0.7, 0.7))
# 41.45 her hand: warmth, then up the steps into the light
place(music, pad([note(48), note(55), note(60), note(64)], 5.4, a=1.6, r=0.6, bright=3), 41.45, 0.26)
for i, n in enumerate([72, 74, 76, 79, 76, 74, 72]):
    place(music, piano(note(n), 2.4), 41.6 + i * 0.66, 0.13)
place(sfx, load("whoosh.mp3"), 44.6, 0.14)
place(sfx, whiteout(1.9), 44.7, 0.32)
place(music, load("riser.mp3")[int(4.0 * SR):], 44.0, 0.2)
for buf in (music, sfx):
    buf[int(46.6 * SR): int(46.66 * SR)] *= np.linspace(1, 0, int(0.06 * SR))[:, None]
    buf[int(46.66 * SR): int(46.75 * SR)] *= 0
# 46.6 morning. the monitor at a steady 72, birds outside, a small piano theme
for tt in np.arange(46.6, 53.9, 60 / 72):
    place(sfx, beep(988, 0.13), tt + 0.196, 0.16)
for tt in (47.3, 48.1, 49.6, 51.0, 52.2):
    place(sfx, chirp_bird(), tt, 0.06, pan=-0.6)
chords = [[48, 55, 64], [43, 55, 62], [45, 52, 60], [41, 53, 60]]
for i, ch in enumerate(chords):
    place(music, pad([note(n) for n in ch], 2.2, a=0.4, r=0.8, bright=3), 47.0 + i * 1.8, 0.2)
for i, n in enumerate([76, 79, 76, 74, 72, 74, 76, 72]):
    place(music, piano(note(n), 2.6), 47.1 + i * 0.9, 0.14)
place(sfx, load("pop.mp3"), 51.2, 0.26)

# ============================== write ==============================
for name, buf, peak in (("music.wav", music, 0.5), ("sfx.wav", sfx, 0.8)):
    m = np.abs(buf).max()
    if m > peak:
        buf *= peak / m
    sf.write(proj / "audio" / name, buf.astype(np.float32), SR, subtype="PCM_16")
    print(name, f"{len(buf) / SR:.2f}s peak {np.abs(buf).max():.2f}")
