"""Original music and sound design for the Idigitalpreneur Diwali ad, synthesized here so there are no rights issues.

python3 -I build/audio.py      (run from the project root; needs numpy and scipy)

128 bpm in A minor: riser into a drop on beat 4, four-on-the-floor kick, claps, hats, sidechained supersaw
chords, a pluck hook with a little sitar-like bend, plus hits, whooshes, glitch bursts, price-drop zaps and
sparkle chimes on the scene cuts. Writes assets/audio/music_raw.wav (loudnorm to music.wav with ffmpeg).
"""
import os
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 44100
BPM = 128
BEAT = 60 / BPM
BAR = BEAT * 4
DUR = 30.0
N = int(DUR * SR)
rng = np.random.default_rng(23)


def b(n):
    return n * BEAT


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
FX_L = np.zeros(N)  # effects bus, not sidechained
FX_R = np.zeros(N)


def put(x, t, g=1.0, pan=0.0, fx=False):
    i = int(t * SR)
    if i >= N or i < 0:
        return
    x = x[: N - i]
    l, r = (FX_L, FX_R) if fx else (L, R)
    l[i:i + len(x)] += x * g * np.sqrt(0.5 * (1 - pan))
    r[i:i + len(x)] += x * g * np.sqrt(0.5 * (1 + pan))


def tt(d):
    return np.arange(int(d * SR)) / SR


# ------------------------------------------------------------------ instruments
def kick(d=.45):
    t = tt(d)
    f = 48 + 140 * np.exp(-t * 32)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.5)
    x += .3 * hp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 300)
    return np.tanh(2.2 * x) * .5


def clap(d=.35):
    t = tt(d)
    n = bp(rng.standard_normal(len(t)), 900, 5000)
    env = np.zeros_like(t)
    for o in (0, .011, .022):
        env += np.where(t >= o, np.exp(-(t - o) * 120), 0)
    env += .5 * np.exp(-t * 14)
    return n * env * .16


def hat(d=.09, open_=False):
    t = tt(.3 if open_ else d)
    x = hp(rng.standard_normal(len(t)), 7500) * np.exp(-t * (14 if open_ else 70))
    return x * .07


def saw(f, t, voices=5, spread=.25):
    x = np.zeros_like(t)
    for v in range(voices):
        det = 1 + spread / 100 * (v - (voices - 1) / 2)
        ph = (f * det * t + v * .13) % 1
        x += 2 * ph - 1
    return x / voices


def chord(ms, d, bright=3200):
    t = tt(d)
    x = sum(saw(hz(m), t) for m in ms)
    x = lp(x, bright)
    env = np.clip(t / .02, 0, 1) * np.clip((d - t) / .08, 0, 1)
    return x * env * .07


def pluck(m, d=.4, bend=False):
    t = tt(d)
    f = hz(m) * (1 + (.06 * np.exp(-t * 18) if bend else 0))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sign(np.sin(ph)) * .4 + np.sin(ph) + .5 * np.sin(2 * ph)
    e = np.exp(-t * 10)  # filter closes after the attack
    x = lp(x, 6500) * e + lp(x, 2200) * (1 - e)
    return x * np.exp(-t * 7) * np.minimum(1, t / .002) * .07


def sub(m, d):
    t = tt(d)
    x = np.sin(2 * np.pi * hz(m) * t) + .2 * np.tanh(3 * np.sin(2 * np.pi * hz(m) * t))
    return x * np.clip(t / .005, 0, 1) * np.clip((d - t) / .03, 0, 1) * .2


def riser(d, f0=200, f1=3500, g=1.0):
    t = tt(d)
    n = rng.standard_normal(len(t))
    k = t / d
    seg = 20
    x = np.zeros_like(t)
    s = len(t) // seg
    for i in range(seg):
        lo = f0 * (f1 / f0) ** (i / seg)
        x[i * s:(i + 1) * s] = bp(n, lo, min(lo * 2.4, 16000))[i * s:(i + 1) * s]
    f = 120 * (8 ** k)
    x += .25 * np.sin(2 * np.pi * np.cumsum(f) / SR)
    return x * k ** 2 * .14 * g


def whoosh(d=.5, g=1.0):
    t = tt(d)
    n = rng.standard_normal(len(t))
    x = np.zeros_like(t)
    seg = 10
    s = len(t) // seg
    for i in range(seg):
        lo = 3000 * (.2 ** (i / seg))
        x[i * s:(i + 1) * s] = bp(n, lo, lo * 2.5)[i * s:(i + 1) * s]
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5
    return x * env * .12 * g


def impact(d=1.6):
    t = tt(d)
    f = 35 + 90 * np.exp(-t * 12)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.6)
    x += .4 * lp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 9)
    return np.tanh(2 * x) * .4


def glitch(d=.35):
    t = tt(d)
    x = np.zeros_like(t)
    s = int(.018 * SR)
    for i in range(0, len(t), s):
        kind = (i // s) % 3
        seg = t[i:i + s]
        if kind == 0:
            x[i:i + s] = np.sign(np.sin(2 * np.pi * (300 + 900 * rng.random()) * seg))
        elif kind == 1:
            x[i:i + s] = rng.standard_normal(len(seg))
    return hp(x, 400) * .06


def zap(d=.55, f0=1800, f1=90):
    """Falling sweep for the price drops."""
    t = tt(d)
    f = f1 + (f0 - f1) * np.exp(-t * 7)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + .3 * np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR))
    return lp(x, 4000) * np.exp(-t * 4) * .12


def chime(m, d=1.6):
    t = tt(d)
    f = hz(m)
    x = np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 4)
    return x * np.exp(-t * 3) * np.minimum(1, t / .002) * .07


def tick(d=.05):
    t = tt(d)
    return np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 120) * .08


# ------------------------------------------------------------------ the arrangement
# A minor: Am F C G
PROG = [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)]
ROOTS = [45, 41, 48, 43]
HOOK = [(0, 76), (.75, 72), (1.5, 74), (2, 76), (2.75, 79), (3.5, 77)]
DROP = 4  # beats: the riser lands here


def arrange():
    put(riser(b(DROP) - .02, g=1.2), 0.0, 1.0, fx=True)
    # intro: filtered chords only
    put(lp(chord(PROG[0], b(DROP), 900), 900), 0, .9)
    total = int(DUR / BEAT)
    for beat in range(DROP, total):
        t = b(beat)
        bar = (beat - DROP) // 4
        prog_i = bar % 4
        outro = beat >= 60
        breakdown = 44 <= beat < 46  # small lift before the dates
        if not breakdown:
            put(kick(), t, 1.0)
        if beat % 2 == 1 and not breakdown:
            put(clap(), t, 1.0, pan=.05)
        for h in range(2):
            put(hat(open_=h == 1), t + h * BEAT / 2, .7 if h == 0 else 1.0, pan=-.25 if h else .25)
        if (beat - DROP) % 4 == 0 and not outro:
            put(chord(PROG[prog_i], BAR - .02), t, 1.0)
            put(chord([m + 12 for m in PROG[prog_i]], BAR - .02, 5000), t, .35, pan=.3)
        # offbeat sub, pumping
        if not outro:
            put(sub(ROOTS[prog_i] - 12 + 12, BEAT / 2 - .02), t + BEAT / 2, 1.0)
        if beat >= 12 and (beat - DROP) % 4 == 0 and not outro:
            for pos, m in HOOK:
                put(pluck(m - (0 if prog_i < 2 else 2), .45, bend=pos == 0), t + pos * BEAT, 1.0, pan=-.15)
    put(chord(PROG[0], 3.0, 2500), b(60), 1.0)
    put(sub(33, 2.5), b(60), 1.2)
    put(riser(b(2), 400, 5000, .7), b(44), 1.0, fx=True)


def effects():
    SC = {"intro": 0, "words": 4, "logo": 8, "offer": 12, "drop": 16, "mix": 22, "fem": 28, "board": 34,
          "grid": 40, "dates": 46, "miss": 52, "end": 58}
    put(chime(88), .2, 1.0, fx=True)
    put(chime(93), .9, .8, fx=True)
    put(impact(), b(4), 1.0, fx=True)
    for i in range(4):  # one hit per word
        put(whoosh(.25, .6), b(4 + i) - .1, 1.0, pan=-.3 + .2 * i, fx=True)
    put(glitch(.45), b(8), 1.0, fx=True)
    put(glitch(.25), b(8) + 1.0, 1.0, pan=.3, fx=True)
    put(impact(1.2), b(8), .6, fx=True)
    put(whoosh(.6), b(12) - .3, 1.0, fx=True)
    for j, m in enumerate((84, 88, 91, 96)):
        put(chime(m), b(12) + .9 + j * .12, .9, pan=-.4 + .27 * j, fx=True)
    put(zap(.8), b(16) + .5, 1.0, fx=True)
    for s in ("mix", "fem"):
        a = b(SC[s])
        put(whoosh(.4), a - .15, .8, fx=True)
        put(zap(.4, 2400, 300), a + .9, .9, fx=True)  # red X slashes
        for k in range(8):
            put(tick(), a + 1.6 + k * .09, 1.0, pan=.2, fx=True)  # counter rolling
        put(impact(.9), a + 2.4, .55, fx=True)
        put(chime(91), a + 2.4, .8, fx=True)
    put(whoosh(.6), b(34) - .3, 1.0, fx=True)
    put(whoosh(.6), b(40) - .3, 1.0, fx=True)
    put(impact(), b(46), .8, fx=True)
    for k in range(4):
        put(tick(), b(46) + .5 + k * .25, 1.4, fx=True)
    put(glitch(.4), b(52) + b(1), 1.0, fx=True)
    put(whoosh(.6), b(58) - .3, 1.0, fx=True)
    put(impact(2.4), b(58), 1.0, fx=True)
    for j, m in enumerate((84, 88, 91, 96, 100)):
        put(chime(m, 2.4), b(58) + .2 + j * .1, .9, pan=-.4 + .2 * j, fx=True)


def sidechain():
    env = np.ones(N)
    for beat in range(DROP, 60):
        if 44 <= beat < 46:
            continue
        i = int(b(beat) * SR)
        k = np.arange(int(BEAT * SR)) / SR
        seg = 1 - .65 * np.exp(-k * 9)
        env[i:i + len(seg)] = np.minimum(env[i:i + len(seg)], seg[: N - i])
    return env


def reverb(x, secs=1.6, mix=.18, seed=0):
    r = np.random.default_rng(seed)
    t = np.arange(int(secs * SR)) / SR
    ir = lp(r.standard_normal(len(t)) * np.exp(-t * 4.0), 7000)
    ir /= np.sqrt(np.sum(ir ** 2))
    return x * (1 - mix) + fftconvolve(x, ir)[: len(x)] * mix * 1.5


def main():
    arrange()
    effects()
    sc = sidechain()
    l = reverb(L, seed=1) * (.55 + .45 * sc) + reverb(FX_L, seed=3, mix=.25)
    r = reverb(R, seed=2) * (.55 + .45 * sc) + reverb(FX_R, seed=4, mix=.25)
    env = np.ones(N)
    env[: int(.01 * SR)] = np.linspace(0, 1, int(.01 * SR))
    env[-int(1.2 * SR):] = np.linspace(1, 0, int(1.2 * SR)) ** 1.5
    st = np.tanh(np.stack([l * env, r * env], 1) * 1.2)
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
