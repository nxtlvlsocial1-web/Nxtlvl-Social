#!/usr/bin/env python3
"""Synthesize the music bed and story SFX for Mom's Location (all original, generated here).

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
DUR = 53.0
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


# ============================== the score ==============================
# bed under the whole night: low room tone + a slow drone that thickens
place(sfx, roomtone(53.0), 0.0, 0.05)
place(music, drone(5.0, 55, 0.12), 0.0, 0.16)
# hook: the location ping on the map, a soft minor pad
for tt in (0.05, 1.45):
    place(sfx, ping(1180), tt, 0.32)
place(music, pad([note(45), note(52), note(60)], 5.2, a=0.8, r=1.2, bright=3), 0.0, 0.32)
place(music, thump(40, 1.0), 4.22, 0.55)  # "bedroom"
# hospital 1: monitor beeps + HVAC
place(sfx, hvac(3.1), 5.05, 0.1)
for tt in np.arange(5.25, 8.05, 0.86):
    place(sfx, beep(1046), tt, 0.12, pan=0.5)
for tt in np.arange(5.4, 8.0, 0.21):
    place(sfx, tap(0.4), tt + rng.uniform(0, 0.05), 0.1, pan=-0.2)
# "we share locations": calm, an uneasy music-box figure
box_fig = [69, 72, 76, 74, 72, 69, 67, 69]
for i, tt in enumerate(np.arange(8.15, 12.0, 0.48)):
    place(music, musicbox(note(box_fig[i % 8]) * (1 + 0.007 * np.sin(i)), 1.3), tt, 0.13, pan=0.2 * np.sin(i))
place(music, pad([note(45), note(48), note(52)], 8.0, a=1.0, r=1.4, bright=3), 8.1, 0.26)
# texting: key taps, send swoosh
for i in range(13):
    place(sfx, tap(), 12.2 + i * (1.15 / 13), 0.32)
place(sfx, load("whoosh-short.mp3"), 13.5, 0.18)
# the reply lands: ding on the kid's phone... and a muffled one from the closet (right)
place(sfx, ding(), 15.97, 0.38)
place(sfx, muffle(ding(), 1300), 16.04, 0.2, pan=0.85)
# relief, then the drop
place(music, pad([note(48), note(52), note(55)], 3.0, a=0.3, r=1.2, bright=2), 16.2, 0.2)
heartbeat(19.0, 3, 0.95, 0.55)
# "lit up": electric hum + bass hit
t = t_axis(1.0)
hum = fft_filter(np.sign(np.sin(2 * np.pi * 120 * t)), 100, 2500) * np.exp(-t / 0.5)
place(sfx, hum, 21.32, 0.14, pan=0.6)
place(music, load("impact-bass-1.mp3"), 21.33, 0.42)
place(music, drone(31.0, 49, 0.2), 21.4, 0.2)
# zoom: accelerating pings + riser into "closet"
for k, tt in enumerate((22.3, 22.95, 23.45, 23.8, 24.05, 24.25)):
    place(sfx, ping(1180 + k * 40, 0.9), tt, 0.22 + k * 0.03)
place(music, load("riser.mp3")[int(6.5 * SR):], 23.0, 0.28)
place(music, cluster([57, 58, 63, 64, 69], 2.8, 0.005, 1.1), 25.95, 0.4)
heartbeat(24.6, 2, 0.8, 0.6)
# the call: vibration + original ringtone, answered at 28.9
for tt in np.arange(26.65, 28.85, 1.0):
    place(sfx, vibrate(0.55), tt, 0.3)
ringtone(26.7, 28.85, 0.24)
place(sfx, tap(1.2), 28.9, 0.4)
# hospital 2, heard close: beeps faster now, her whisper over the line
place(sfx, hvac(3.0), 29.3, 0.08)
for tt in np.arange(29.45, 32.2, 0.62):
    place(sfx, beep(1046), tt, 0.1, pan=0.4)
place(music, drone(5.0, 41, 0.3), 29.3, 0.24)
# who have you been texting -> heartbeat
heartbeat(32.4, 3, 0.62, 0.7)
# scrolling back through the week: haptic ticks + a sour version of the ding motif
for tt in np.arange(34.55, 37.2, 0.11):
    place(sfx, tick(2000, 0.03, 0.005), tt, 0.05, pan=-0.2)
for i, tt in enumerate(np.arange(34.3, 37.6, 0.55)):
    place(music, bell(note(84 - (i % 4)) * 0.985, 1.6) , tt, 0.05, pan=0.3)
# the door: long creak, low riser
place(sfx, creak(2.2, 70, 120), 37.78, 0.42, pan=0.55)
place(music, load("riser.mp3")[int(5.5 * SR):], 37.7, 0.26)
# it steps out: heavy bare-foot steps, floor groans, the sting on "scrubs"
for k, tt in enumerate((40.55, 41.35, 42.15)):
    place(sfx, footstep(1.25), tt, 0.62, pan=0.4 - k * 0.15)
    place(sfx, creak(0.5, 55, 75), tt + 0.05, 0.16, pan=0.4)
place(music, stab([33, 34, 40], 2.6, 1.0), 42.28, 0.5)
# way too tall: sub impact, everything else drops away
place(music, load("impact-bass-2.mp3"), 43.0, 0.45)
place(music, drone(3.4, 36.7, 0.5), 43.0, 0.3)
# still typing: soft irregular taps
for i in range(20):
    place(sfx, tap(0.8), 44.88 + i * 0.072 + rng.uniform(0, 0.02), 0.26, pan=0.25)
# silence... then the buzz and the same ding
place(sfx, vibrate(0.35), 46.56, 0.34)
place(sfx, vibrate(0.25), 46.98, 0.28)
place(sfx, ding(), 46.6, 0.4)
# "go to sleep, sweetie": sub drone + a thin high tone, breath swell on "sweetie"
place(music, drone(1.8, 33, 0.8), 47.95, 0.35)
t = t_axis(1.9)
eerie = (np.sin(2 * np.pi * 1975 * t) + np.sin(2 * np.pi * 1983 * t)) * 0.3
place(music, eerie * np.minimum(t / 0.6, 1) * np.minimum((1.9 - t) / 0.4, 1), 47.95, 0.05)
place(sfx, noise_burst(1.0, 500, 4000, 0.5, a=0.4), 48.4, 0.1)
# the lunge: riser into a hard hit, then nothing
place(music, load("riser.mp3")[int(8.2 * SR):], 49.25, 0.3)
place(music, load("impact-bass-2.mp3"), 49.74, 0.6)
place(sfx, load("glitch-1.mp3")[: int(0.22 * SR)], 49.74, 0.38)
# end card: both dots in one room — a last ping, a cold pad, the follow pop
place(sfx, ping(1180), 50.15, 0.3)
place(sfx, ping(1180), 51.55, 0.2)
place(music, pad([note(45), note(52), note(55), note(60)], 2.9, a=0.3, r=1.4, bright=3), 50.1, 0.28)
place(sfx, load("pop.mp3"), 50.42, 0.3)

# hard silence between the hit and the end card
for buf in (music, sfx):
    i0, i1 = int(49.95 * SR), int(50.08 * SR)
    buf[i0:i1] *= 0
    buf[i1:i1 + int(0.03 * SR)] *= np.linspace(0, 1, int(0.03 * SR))[:, None]

# ============================== write ==============================
for name, buf, peak in (("music.wav", music, 0.5), ("sfx.wav", sfx, 0.8)):
    m = np.abs(buf).max()
    if m > peak:
        buf *= peak / m
    sf.write(proj / "audio" / name, buf.astype(np.float32), SR, subtype="PCM_16")
    print(name, f"{len(buf) / SR:.2f}s peak {np.abs(buf).max():.2f}")
