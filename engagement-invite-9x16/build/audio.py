"""Original music for the engagement invite, synthesized here so there are no rights issues.

python3 -I build/audio.py      (run from the project root; needs numpy and scipy)

84 bpm in D major: tanpura drone, santoor arpeggios, a bansuri-style flute melody, soft dholak,
temple bells on the doors and chimes on the name reveals. Writes assets/audio/music.wav.
"""
import os
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 44100
BPM = 84
BEAT = 60 / BPM
BAR = BEAT * 4
DUR = 43.0
N = int(DUR * SR)
rng = np.random.default_rng(11)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def lp(x, fc, order=2):
    return sosfilt(butter(order, fc, "low", fs=SR, output="sos"), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


L = np.zeros(N)
R = np.zeros(N)


def put(x, t, g=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N:
        return
    x = x[: N - i]
    L[i:i + len(x)] += x * g * np.sqrt(0.5 * (1 - pan))
    R[i:i + len(x)] += x * g * np.sqrt(0.5 * (1 + pan))


def tt(d):
    return np.arange(int(d * SR)) / SR


# ------------------------------------------------------------------ instruments
def santoor(m, d=1.6):
    """Hammered string course: two slightly detuned strings, bright attack, steady decay."""
    t = tt(d)
    f = hz(m)
    x = np.zeros_like(t)
    for det in (-1.6, 1.6):
        for k, a in [(1, 1.0), (2, .5), (3, .32), (4, .16), (5, .1), (6, .05)]:
            fk = f * k * (1 + .0007 * k * k) + det
            x += a * np.sin(2 * np.pi * fk * t) * np.exp(-t * (2.4 + k * 1.1))
    x += .25 * hp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 90)
    return x * np.minimum(1, t / .002) * .22


def flute(m, d, prev=None):
    """Bansuri-like: sine body, a little 2nd and 3rd harmonic, breath, delayed vibrato, glide in."""
    t = tt(d + .25)
    f = hz(m)
    if prev is not None:
        glide = np.exp(-t / .06)
        f = f * (hz(prev) / f) ** glide
    vib = 1 + .006 * np.sin(2 * np.pi * 5.2 * t) * np.clip((t - .25) / .4, 0, 1)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    x = np.sin(ph) + .18 * np.sin(2 * ph) + .07 * np.sin(3 * ph)
    breath = bp(rng.standard_normal(len(t)), 1200, 4200) * .12
    env = np.clip(t / .07, 0, 1) * np.clip((d + .25 - t) / .25, 0, 1)
    env *= 1 - .15 * np.clip(t / max(d, .1), 0, 1)
    return (x + breath) * env * .2


def tanpura_pluck(m, d=3.2):
    t = tt(d)
    f = hz(m)
    x = np.zeros_like(t)
    for k in range(1, 14):  # jawari buzz: lots of slowly blooming upper partials
        bloom = np.clip(t / (.15 + k * .04), 0, 1)
        x += (1 / k ** 0.9) * np.sin(2 * np.pi * f * k * t + k) * bloom
    return lp(x, 2600) * np.exp(-t * 0.9) * np.minimum(1, t / .01) * .05


def pad(ms, d):
    t = tt(d)
    x = np.zeros_like(t)
    for m in ms:
        for det in (-.25, 0, .25):
            ph = 2 * np.pi * hz(m) * (1 + det / 100) * t
            x += 2 / np.pi * np.arctan(3 * np.sin(ph)) * .5 + .3 * np.sin(2 * ph)
    x = lp(x, 1100)
    env = np.clip(t / .8, 0, 1) * np.clip((d - t) / .9, 0, 1)
    return x * env * .018


def bass(m, d=1.2):
    t = tt(d)
    x = np.sin(2 * np.pi * hz(m) * t) + .3 * np.sin(4 * np.pi * hz(m) * t)
    return x * np.exp(-t * 3.2) * np.minimum(1, t / .005) * .22


def dha(d=.5):
    t = tt(d)
    f = 95 * (1 + .6 * np.exp(-t * 30))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
    x += .4 * np.sin(2 * np.pi * 330 * t) * np.exp(-t * 22)
    return x * .2


def ta(d=.25):
    t = tt(d)
    x = .6 * np.sin(2 * np.pi * 520 * t) * np.exp(-t * 35) + .5 * bp(rng.standard_normal(len(t)), 1500, 5000) * np.exp(-t * 60)
    return x * .16


def ghungroo(d=.18):
    t = tt(d)
    x = hp(rng.standard_normal(len(t)), 6000) * np.exp(-t * 40)
    for f in (5200, 6900, 8100):
        x += .3 * np.sin(2 * np.pi * f * t) * np.exp(-t * 30)
    return x * .035


def bell(f0=520, d=4.0, g=1.0):
    """Temple bell: inharmonic partials with beating."""
    t = tt(d)
    x = np.zeros_like(t)
    for r, a, dec in [(1, 1, .9), (2.0, .6, 1.3), (2.76, .5, 1.8), (5.4, .35, 2.6), (8.9, .2, 3.6), (1.003, .7, .9)]:
        x += a * np.sin(2 * np.pi * f0 * r * t) * np.exp(-t * dec)
    return x * np.minimum(1, t / .003) * .12 * g


def chime(m, d=2.2):
    t = tt(d)
    f = hz(m)
    x = np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 3)
    return x * np.exp(-t * 2.2) * np.minimum(1, t / .002) * .09


def whoosh(d=1.2):
    t = tt(d)
    n = rng.standard_normal(len(t))
    x = np.zeros_like(t)
    seg = len(t) // 12
    for i in range(12):  # sweep a band upwards in steps, crossfaded by the envelope
        lo = 300 + i * 220
        x[i * seg:(i + 1) * seg] = bp(n, lo, lo * 2.2)[i * seg:(i + 1) * seg]
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    return lp(x, 5000) * env * .12


# ------------------------------------------------------------------ the arrangement
CHORDS = ["D", "D", "A", "Bm", "G", "D", "G", "A", "D", "A", "Bm", "G", "Em", "A", "D"]
TONES = {"D": (62, 66, 69), "A": (57, 61, 64), "Bm": (59, 62, 66), "G": (55, 59, 62), "Em": (52, 55, 59)}
MELODY = {
    2: [(0, 1.5, 76), (1.5, .5, 78), (2, 2, 76)],
    3: [(0, 1, 74), (1, 1, 73), (2, 1, 71), (3, 1, 74)],
    4: [(0, 2, 71), (2, 1, 74), (3, 1, 79)],
    5: [(0, 3, 78), (3, .5, 76), (3.5, .5, 74)],
    6: [(0, 1.5, 79), (1.5, .5, 81), (2, 1, 83), (3, 1, 81)],
    7: [(0, 2, 76), (2, 1, 78), (3, 1, 81)],
    8: [(0, 1.5, 86), (1.5, .5, 85), (2, 2, 81)],
    9: [(0, 1, 81), (1, 1, 83), (2, 1, 81), (3, 1, 78)],
    10: [(0, 2, 78), (2, 1, 76), (3, 1, 74)],
    11: [(0, 1.5, 79), (1.5, .5, 78), (2, 2, 74)],
    12: [(0, 1, 71), (1, 1, 74), (2, 1, 76), (3, 1, 79)],
    13: [(0, 2, 78), (2, 1, 76), (3, 1, 73)],
    14: [(0, 4.5, 74)],
}


def arrange():
    # tanpura cycle Pa Sa Sa Sa, all the way through
    t, k = 0.0, 0
    while t < DUR - 1:
        put(tanpura_pluck([57, 62, 62, 50][k % 4]), t, 1.0, [-.3, .3, .1, -.1][k % 4])
        t += BEAT * 0.75
        k += 1
    for b, ch in enumerate(CHORDS):
        t0 = b * BAR
        r, th, fi = TONES[ch]
        last = b == len(CHORDS) - 1
        # santoor arpeggio, 8ths; softer once the flute is in
        pat = [r + 12, fi + 12, th + 12, fi + 12, r + 24, fi + 12, th + 24, fi + 12]
        g = 1.0 if b < 2 else .62
        if last:
            pat = [r + 12, fi + 12, th + 12, r + 24]
        for i, m in enumerate(pat):
            put(santoor(m), t0 + i * BEAT / 2, g * (1.1 if i == 0 else .9), pan=-.35 + .1 * (i % 4))
        if b == 0:  # sparkling run up into the door opening
            for i, m in enumerate([74, 78, 81, 86, 90, 93]):
                put(santoor(m, 1.2), .55 + i * .09, .5, pan=.4)
        if b >= 1:
            put(pad([r, th, fi, r + 12], BAR + (2.5 if last else .9)), t0, 1.0)
        if b >= 3:
            put(bass(r - 24), t0, 1.0)
            if not last:
                put(bass(r - 24 + 7 if ch != "Bm" else r - 24 + 7), t0 + 2 * BEAT, .8)
        if 3 <= b <= 13:  # soft dholak: dha . ta dha | . dha ta .
            for pos in (0, 1.5, 2.5):
                put(dha(), t0 + pos * BEAT, .9 if pos == 0 else .7)
            for pos in (1, 3):
                put(ta(), t0 + pos * BEAT, 1.0, pan=.15)
            for i in range(8):
                put(ghungroo(), t0 + i * BEAT / 2 + .01, 1.0 if i % 2 == 0 else .6, pan=.35)
        if last:
            put(dha(), t0, 1.0)
    # flute melody
    prev = None
    for b, notes in MELODY.items():
        for pos, ln, m in notes:
            put(flute(m, ln * BEAT, prev), b * BAR + pos * BEAT, 1.0, pan=.08)
            prev = m


def effects():
    put(bell(523, 5.0, 1.0), 0.04, 1.0, pan=-.1)          # temple bell on the first frame
    put(bell(784, 4.0, .6), 0.62, 1.0, pan=.2)            # second strike as the doors part
    put(whoosh(1.4), 0.5, 1.0)
    put(bell(1046, 3.0, .45), 2.3, 1.0)                    # Ganesh begins to draw
    chimes = [(3 * BAR + 1.8, 86), (5 * BAR + 1.7, 90), (5 * BAR + 2.85, 93), (7 * BAR + 1.7, 90),
              (7 * BAR + 2.85, 93), (9 * BAR + 1.1, 88), (11 * BAR + 1.0, 86), (13 * BAR + .6, 90),
              (13 * BAR + 2.8, 93)]
    for t, m in chimes:
        for j, dm in enumerate((0, 5, 12)):
            put(chime(m + dm - 12), t + j * .07, .9, pan=-.3 + .3 * j)
    for t in (3 * BAR - .35, 5 * BAR - .35, 7 * BAR - .35, 9 * BAR - .35, 11 * BAR - .35, 13 * BAR - .35):
        put(whoosh(.8), t, .55)
    put(bell(523, 6.0, .7), 14 * BAR, 1.0)                 # closing bell


def reverb(x, secs=2.4, mix=.28, seed=0):
    r = np.random.default_rng(seed)
    t = np.arange(int(secs * SR)) / SR
    ir = r.standard_normal(len(t)) * np.exp(-t * 3.0)
    ir = lp(ir, 6000)
    ir /= np.sqrt(np.sum(ir ** 2))
    wet = fftconvolve(x, ir)[: len(x)]
    return x * (1 - mix) + wet * mix * 1.6


def main():
    arrange()
    effects()
    l, r = reverb(L, seed=1), reverb(R, seed=2)
    # gentle fade in on the first 30 ms, fade out over the last 2 s
    env = np.ones(N)
    env[: int(.03 * SR)] = np.linspace(0, 1, int(.03 * SR))
    env[-int(2.0 * SR):] = np.linspace(1, 0, int(2.0 * SR)) ** 1.5
    st = np.stack([l * env, r * env], 1)
    st /= np.max(np.abs(st)) / 0.89
    path = os.path.join(ROOT, "assets", "audio", "music_raw.wav")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())
    print("wrote", path)


if __name__ == "__main__":
    main()
