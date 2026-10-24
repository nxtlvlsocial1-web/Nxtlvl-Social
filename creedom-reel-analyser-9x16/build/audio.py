"""Original music bed and sound effects for the Creedom reel, synthesized here so there are no rights issues.

python3 -I build/audio.py      (run from the project root; needs numpy and scipy and ffmpeg on PATH)

A light, bouncy 100 bpm pop bed in F major (soft kick, clap on 2 and 4, shaker, warm chords, a marimba-ish pluck),
kept low under the voice, plus UI sound design on the visual events: pops, ticks, counter rattles, whooshes, a
sparkle, the dark "twist" drop, keyboard taps and a send ding. Writes assets/audio/music.wav (bed + SFX) and
assets/audio/vo.wav (the voiceover, lifted to about -15 LUFS); they play on separate tracks.
"""
import os
import subprocess
import sys
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timing import DUR, S_TWIST  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 44100
BPM = 100
BEAT = 60 / BPM
BAR = BEAT * 4
N = int(DUR * SR)
VO_GAIN_DB = 5.2  # the Nota 3 take measures -20.2 LUFS; lift voice and bed together to about -15
rng = np.random.default_rng(31)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def lp(x, fc, order=2):
    return sosfilt(butter(order, fc, "low", fs=SR, output="sos"), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


BUS = {k: (np.zeros(N), np.zeros(N)) for k in ("music", "sfx")}


def put(x, t, g=1.0, pan=0.0, bus="music"):
    i = int(t * SR)
    if i >= N or i < 0:
        return
    x = x[: N - i]
    l, r = BUS[bus]
    l[i:i + len(x)] += x * g * np.sqrt(0.5 * (1 - pan))
    r[i:i + len(x)] += x * g * np.sqrt(0.5 * (1 + pan))


def tt(d):
    return np.arange(int(d * SR)) / SR


# ------------------------------------------------------------------ instruments
def kick(d=.35):
    t = tt(d)
    f = 50 + 110 * np.exp(-t * 30)
    return np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)) * .45


def clap(d=.3):
    t = tt(d)
    env = sum(np.where(t >= o, np.exp(-(t - o) * 140), 0) for o in (0, .01, .02)) + .4 * np.exp(-t * 18)
    return bp(rng.standard_normal(len(t)), 1000, 4500) * env * .1


def shaker(d=.08):
    t = tt(d)
    return hp(rng.standard_normal(len(t)), 6500) * np.exp(-t * 60) * np.minimum(1, t / .01) * .05


def epiano(ms, d):
    t = tt(d)
    x = np.zeros_like(t)
    for m in ms:
        f = hz(m)
        x += (np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t) * np.exp(-t * 3)) * np.exp(-t * 1.4)
    env = np.minimum(1, t / .01) * np.clip((d - t) / .1, 0, 1)
    return lp(x, 3000) * env * .05


def marimba(m, d=.5):
    t = tt(d)
    f = hz(m)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * 9) + .4 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 30)
    return x * np.minimum(1, t / .002) * .07


def bass(m, d):
    t = tt(d)
    x = np.sin(2 * np.pi * hz(m) * t) + .15 * np.sin(4 * np.pi * hz(m) * t)
    return x * np.minimum(1, t / .006) * np.clip((d - t) / .04, 0, 1) * np.exp(-t * 1.2) * .2


# ------------------------------------------------------------------ sound design
def pop_(f0=900, d=.12):
    t = tt(d)
    f = f0 * (1 + 1.5 * np.exp(-t * 60))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 40) * .18


def tick_(d=.04, f=3200):
    t = tt(d)
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 150) * .12


def rattle(d, rate=24):
    out = np.zeros(int(d * SR))
    for k in range(int(d * rate)):
        x = tick_(.03, 2600 + 400 * (k % 3))
        i = int(k / rate * SR)
        out[i:i + len(x)] += x[: len(out) - i] * .6
    return out


def whoosh(d=.45, g=1.0, up=True):
    t = tt(d)
    n = rng.standard_normal(len(t))
    seg, s = 10, len(t) // 10
    x = np.zeros_like(t)
    for i in range(seg):
        k = i / seg if up else 1 - i / seg
        lo = 400 * (8 ** k)
        x[i * s:(i + 1) * s] = bp(n, lo, min(lo * 2.4, 16000))[i * s:(i + 1) * s]
    return x * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5 * .12 * g


def sparkle(d=1.2):
    t = tt(d)
    x = np.zeros_like(t)
    for j, m in enumerate((84, 88, 91, 96)):
        o = j * .06
        tj = np.clip(t - o, 0, None)
        x += np.where(t >= o, np.sin(2 * np.pi * hz(m) * tj) * np.exp(-tj * 5), 0)
    return x * .05


def thud(d=1.4):
    t = tt(d)
    f = 40 + 60 * np.exp(-t * 10)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3)
    return np.tanh(1.8 * x) * .35


def ding(d=1.0):
    t = tt(d)
    return (np.sin(2 * np.pi * 1318 * t) + .4 * np.sin(2 * np.pi * 1975 * t) * np.exp(-t * 6)) * np.exp(-t * 4) * .08


def key_(d=.05):
    t = tt(d)
    return bp(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t * 120) * .1


# ------------------------------------------------------------------ arrangement
PROG = [(65, 69, 72, 76), (62, 65, 69, 72), (58, 62, 65, 69), (60, 64, 67, 70)]  # Fmaj7 Dm7 Bbmaj7 C7
ROOTS = [41, 38, 46, 48]
HOOK = [(0, 77), (.5, 81), (1, 84), (1.75, 81), (2.5, 79), (3, 77)]


def arrange():
    nbeats = int(DUR / BEAT) + 1
    for beat in range(nbeats):
        t = beat * BEAT
        bar = beat // 4
        ci = bar % 4
        twist = S_TWIST[0] - .1 <= t < S_TWIST[1] - .2
        end = t > DUR - 1.6
        if end:
            continue
        if beat % 4 == 0:
            put(epiano(PROG[ci], BAR), t, .55 if twist else 1.0)
            if not twist:
                put(bass(ROOTS[ci], BAR * .5), t)
                put(bass(ROOTS[ci] + 7, BAR * .45), t + 2 * BEAT, .8)
            if not twist and bar % 2 == 1:
                for pos, m in HOOK:
                    put(marimba(m - (0 if ci < 2 else 3)), t + pos * BEAT, .8, pan=.2)
        if twist:
            continue
        if beat >= 1:
            put(kick(), t, 1.0)
        if beat % 2 == 1:
            put(clap(), t, .8, pan=.05)
        for k in range(2):
            put(shaker(), t + k * BEAT / 2, 1.0 if k else .6, pan=-.3)
    put(epiano(PROG[0], 2.5), DUR - 2.6, 1.0)


def sfx():
    s = "sfx"
    for t in (.15, .55, 5.7, 5.85, 10.55, 13.75, 14.15, 17.3, 17.8, 19.85, 26.45, 26.65, 30.0):
        put(pop_(), t, 1.0, bus=s)
    put(rattle(1.4, 22), .45, .8, bus=s)               # play counter rolls
    put(whoosh(.5), 1.05, 1.0, bus=s)
    put(sparkle(), 1.4, 1.0, bus=s)                    # 85x
    put(pop_(500, .25), 3.85, 1.0, bus=s)              # "?" bubble
    put(rattle(1.2, 10), 6.0, .6, bus=s)               # slow crawl to 3K
    put(thud(.6), 7.25, .4, bus=s)
    for i in range(6):
        put(pop_(700 + 60 * i, .1), 8.3 + i * .07, .6, bus=s)
    put(whoosh(.6, 1.2, False), 9.45, 1.0, bus=s)      # dashboard blurs
    put(whoosh(.45, 1.3), 10.1, 1.0, bus=s)            # pink wipe
    for t in (11.6, 12.25, 13.05, 18.15, 18.65, 19.15, 27.0, 27.45, 27.9):
        put(tick_(.06, 2400), t, 1.4, bus=s)
        put(pop_(1300, .08), t, .5, bus=s)
    put(rattle(.7, 14), 12.82, .6, bus=s)              # stopwatch to 20
    put(whoosh(.45, 1.0, False), 15.0, 1.0, bus=s)     # thumbs fold into the card
    put(rattle(1.0, 26), 15.37, .8, bus=s)             # 0 -> 82
    put(sparkle(1.4), 15.45, 1.2, bus=s)
    put(whoosh(.5), 19.6, 1.0, bus=s)
    put(thud(1.6), S_TWIST[0] - .05, 1.0, bus=s)       # lights go down
    put(whoosh(.5, .8), 21.6, .8, bus=s)
    put(pop_(400, .3), 23.4, 1.2, bus=s)               # "!" and BEST HOOK
    put(sparkle(1.0), 23.45, 1.0, bus=s)
    put(whoosh(.55, 1.4), 24.65, 1.0, bus=s)           # the hook flies to 0:00
    put(whoosh(.35, 1.0, False), 28.35, 1.0, bus=s)    # guesses struck out
    put(thud(.8), 29.75, .6, bus=s)                    # CREEDOM slams in
    put(whoosh(.4), 29.6, 1.0, bus=s)
    for i in range(7):
        put(key_(), 30.25 + i * .1, 1.2, pan=.2, bus=s)
    put(ding(), 31.05, 1.0, bus=s)
    put(sparkle(1.4), 32.25, 1.0, bus=s)


def reverb(x, secs=1.4, mix=.18, seed=0):
    r = np.random.default_rng(seed)
    t = np.arange(int(secs * SR)) / SR
    ir = lp(r.standard_normal(len(t)) * np.exp(-t * 4.5), 7000)
    ir /= np.sqrt(np.sum(ir ** 2))
    return x * (1 - mix) + fftconvolve(x, ir)[: len(x)] * mix * 1.5


def rms(x):
    return np.sqrt(np.mean(x ** 2) + 1e-12)


def main():
    arrange()
    sfx()
    ml, mr = (reverb(BUS["music"][0], seed=1), reverb(BUS["music"][1], seed=2))
    sl, sr = (reverb(BUS["sfx"][0], .8, .12, 3), reverb(BUS["sfx"][1], .8, .12, 4))
    # bed sits about 20 dB under a speech level, SFX around 10 dB under
    g_m = .02 / rms(ml + mr)
    g_s = .055 / rms(sl + sr)
    l, r = ml * g_m + sl * g_s, mr * g_m + sr * g_s
    env = np.ones(N)
    env[: int(.02 * SR)] = np.linspace(0, 1, int(.02 * SR))
    env[-int(1.0 * SR):] = np.linspace(1, 0, int(1.0 * SR)) ** 1.4
    st = np.stack([l * env, r * env], 1) * 10 ** (VO_GAIN_DB / 20)
    peak = np.max(np.abs(st))
    if peak > .95:
        st *= .95 / peak
    path = os.path.join(ROOT, "assets", "audio", "music.wav")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())
    print("wrote", path)
    src = os.path.join(ROOT, "assets", "audio", "vo.mp3")
    vo = os.path.join(ROOT, "assets", "audio", "vo.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af",
                    f"volume={VO_GAIN_DB}dB,alimiter=limit=0.95:level=false", "-ar", str(SR), vo], check=True)
    out = subprocess.run(["ffmpeg", "-i", vo, "-i", path, "-filter_complex", "amix=inputs=2:normalize=0,ebur128",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    print("mix loudness:", [ln.strip() for ln in out.splitlines() if ln.strip().startswith("I:")][-1:])


if __name__ == "__main__":
    main()
