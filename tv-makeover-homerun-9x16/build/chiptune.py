"""Original 8-bit ballpark chiptune for the TV-makeover home-run reel.

Timed to the voiceover (seconds on the film's clock):
  3.05-4.08  snare roll + rising arpeggio into the bat hit
  4.08-7.70  anthem stabs (I-IV-V-I)
  7.70-23.7  running groove at 150 BPM, flourishes on each base touch
  22.9-24.0  riser into the slide
  24.0       home-run fanfare
  25.2-34.19 celebration groove, final chord at 33.6

Writes assets/audio/music.wav (44.1 kHz stereo). Run: python3 build/chiptune.py
"""
import wave
import numpy as np

SR = 44100
DUR = 34.19
N = int(SR * DUR)
mix = np.zeros(N)
rng = np.random.default_rng(7)


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env(n, a=0.005, d=0.08, s=0.6, r=0.04):
    t = np.arange(n) / SR
    e = np.ones(n) * s
    na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, max(na, 1))[:len(e[:na])]
    seg = e[na:na + nd]
    e[na:na + nd] = np.linspace(1, s, max(nd, 1))[:len(seg)]
    if nr and n > nr:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def square(f, n, duty=0.5):
    ph = (np.arange(n) * f / SR) % 1.0
    return np.where(ph < duty, 1.0, -1.0)


def tri(f, n):
    ph = (np.arange(n) * f / SR) % 1.0
    return 4 * np.abs(ph - 0.5) - 1


def place(sig, t0, gain):
    i = int(t0 * SR)
    if i >= N:
        return
    j = min(N, i + len(sig))
    mix[i:j] += sig[: j - i] * gain


def note(m, t0, dur, gain=0.18, duty=0.25, a=0.005, d=0.06, s=0.55, r=0.03):
    n = int(dur * SR)
    place(square(midi(m), n, duty) * env(n, a, d, s, r), t0, gain)


def bass(m, t0, dur, gain=0.32):
    n = int(dur * SR)
    place(tri(midi(m), n) * env(n, 0.003, 0.05, 0.8, 0.02), t0, gain)


def noise(t0, dur, gain, decay=30.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    place(rng.uniform(-1, 1, n) * np.exp(-t * decay), t0, gain)


def kick(t0, gain=0.5):
    n = int(0.16 * SR)
    t = np.arange(n) / SR
    f = 120 * np.exp(-t * 25) + 40
    ph = np.cumsum(f) / SR
    place(np.sin(2 * np.pi * ph) * np.exp(-t * 18), t0, gain)


def snare(t0, gain=0.22):
    noise(t0, 0.14, gain, 22)


def hat(t0, gain=0.06):
    noise(t0, 0.04, gain, 90)


def chord(ms, t0, dur, gain=0.09, duty=0.5):
    for m in ms:
        note(m, t0, dur, gain, duty, 0.004, 0.15, 0.5, 0.12)


def arp_up(t0, base=84, gain=0.12):
    for k, m in enumerate([base, base + 4, base + 7, base + 12]):
        note(m, t0 + k * 0.045, 0.06, gain, 0.125)


E8 = 0.2  # eighth note at 150 BPM
BAR = 1.6
C, F, G, Am = [60, 64, 67], [65, 69, 72], [67, 71, 74], [57, 60, 64]

# --- drum roll + rising arpeggio into the hit (3.05-4.08)
t = 3.05
k = 0
while t < 4.02:
    p = (t - 3.05) / 1.0
    snare(t, 0.05 + 0.16 * p)
    t += 0.11 - 0.07 * p
    k += 1
for k, m in enumerate([60, 64, 67, 72, 76, 79, 84]):
    note(m, 3.45 + k * 0.085, 0.09, 0.07 + 0.01 * k, 0.25)

# --- the hit: crash + big chord
noise(4.08, 1.2, 0.35, 3.5)
kick(4.08, 0.7)
chord(C + [72, 76], 4.08, 0.75, 0.1)
bass(36, 4.08, 0.75)
# anthem stabs
for t0, ch, b in [(4.88, F, 41), (5.68, G, 43), (6.48, C + [72], 48)]:
    chord(ch, t0, 0.7 if t0 < 6.4 else 1.15, 0.09)
    bass(b, t0, 0.7)
    kick(t0, 0.45)
    snare(t0 + 0.4, 0.14)
for k, m in enumerate([72, 76, 79, 84, 79, 76, 72, 76]):
    note(m, 6.5 + k * 0.14, 0.12, 0.07, 0.125)

# --- running groove (7.7 -> 23.7, 10 bars)
LEAD = [
    [76, None, 79, None, 84, None, 79, 76],
    [77, None, 81, None, 84, None, 81, 77],
    [79, 79, 83, None, 86, None, 83, 79],
    [84, None, 79, None, 76, None, 72, None],
    [81, None, 84, None, 88, None, 84, 81],
    [77, None, 81, None, 84, None, 86, 84],
    [83, None, 86, None, 79, None, 83, 86],
    [86, None, 83, None, 79, None, None, None],
]
ROOTS = [48, 41, 43, 48, 45, 41, 43, 43]
CHORDS = [C, F, G, C, Am, F, G, G]
g0 = 7.7
for b in range(10):
    bt = g0 + b * BAR
    idx = b % 8
    for s in range(8):
        st = bt + s * E8
        hat(st, 0.05 if s % 2 else 0.07)
        if s in (0, 4):
            kick(st, 0.45)
        if s in (2, 6):
            snare(st, 0.16)
        r = ROOTS[idx] + (12 if s % 2 else 0)
        bass(r, st, E8 * 0.9, 0.26)
        m = LEAD[idx][s]
        if m is not None:
            ln = E8 * (2 if s + 1 < 8 and LEAD[idx][s + 1] is None else 1) * 0.95
            note(m, st, ln, 0.11, 0.25)
    # offbeat chord pulses
    for s in (1, 3, 5, 7):
        chord(CHORDS[idx], bt + s * E8, 0.09, 0.035, 0.125)

# flourishes on each base touch
for tt in (10.3, 14.2, 19.3):
    arp_up(tt, 84, 0.12)
    noise(tt, 0.4, 0.12, 9)

# --- riser into the slide (22.9-24.0)
n = int(1.1 * SR)
tt = np.arange(n) / SR
f = 130 * 2 ** (tt / 1.1 * 3)
ph = np.cumsum(f) / SR
place(np.where(ph % 1 < 0.5, 1.0, -1.0) * np.linspace(0.02, 0.12, n), 22.9, 1.0)
t = 23.3
while t < 23.98:
    snare(t, 0.12 + 0.12 * (t - 23.3) / 0.7)
    t += 0.06

# --- fanfare on the home run (24.0)
noise(24.0, 1.6, 0.32, 2.8)
kick(24.0, 0.7)
for k in range(3):
    chord([67, 71, 74, 79], 24.0 + k * 0.12, 0.1, 0.09)
chord([72, 76, 79, 84], 24.36, 0.9, 0.1)
bass(36, 24.36, 0.9)

# --- celebration groove under the clean-up (25.2 -> 33.6), lighter, no lead
CEL = [C, F, G, C, Am, F]
CROOT = [48, 41, 43, 48, 45, 41]
c0 = 25.2
for b in range(6):
    bt = c0 + b * BAR
    if bt >= 33.6:
        break
    for s in range(8):
        st = bt + s * E8
        if st >= 33.6:
            break
        hat(st, 0.045)
        if s in (0, 4):
            kick(st, 0.38)
        if s in (2, 6):
            snare(st, 0.11)
        bass(CROOT[b] + (12 if s % 2 else 0), st, E8 * 0.9, 0.22)
        ch = CEL[b]
        note(ch[s % 3] + 12, st, E8 * 0.8, 0.05, 0.125)
# final cadence
chord([72, 76, 79, 84], 33.6, 0.59, 0.11)
bass(36, 33.6, 0.59)
noise(33.6, 0.59, 0.2, 4)
kick(33.6, 0.6)

# gentle one-pole low-pass to soften the squares, then normalise to -3 dBFS peak
y = np.zeros_like(mix)
a = 0.35
acc = 0.0
for i in range(N):
    acc += a * (mix[i] - acc)
    y[i] = acc
y /= max(1e-9, np.max(np.abs(y)))
y *= 10 ** (-3 / 20)
fade = int(0.08 * SR)
y[-fade:] *= np.linspace(1, 0, fade)
st = np.stack([y, y], axis=1)
pcm = (st * 32767).astype(np.int16)
with wave.open("assets/audio/music.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote assets/audio/music.wav", len(y) / SR, "s")
