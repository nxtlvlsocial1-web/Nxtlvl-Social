"""Original fight-night score and sound design, synthesized here so there are no rights issues.

python3 -I build/audio.py      (run from the project root; needs numpy, scipy and ffmpeg)

A heavy 92 bpm hip-hop beat (kick, snare, hats, 808 bass, a minor brass-ish stab) that drops out for the hush before
the knockout; an arena crowd bed that swells on hits and roars on the K.O.; ring bells for the rounds and the
finish; punch impacts, whooshes on every cut, a K.O. boom, keyboard taps for the CTA. Writes assets/audio/music.wav
and the lifted voiceover assets/audio/vo.wav (from the sped-up commentator take, kept in the scratchpad as vo_fast.wav).
"""
import json
import os
import subprocess
import sys
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate as G  # noqa: E402

SR = 44100
DUR = G.DUR
N = int(DUR * SR)
T = G.T
BPM = 92
BEAT = 60 / BPM
rng = np.random.default_rng(5)
VO_GAIN_DB = 5.0


def lp(x, fc, o=2):
    return sosfilt(butter(o, fc, "low", fs=SR, output="sos"), x)


def hp(x, fc, o=2):
    return sosfilt(butter(o, fc, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, hi], "band", fs=SR, output="sos"), x)


def tt(d):
    return np.arange(int(d * SR)) / SR


BUS = {k: (np.zeros(N), np.zeros(N)) for k in ("music", "sfx", "crowd")}


def put(x, t, g=1.0, pan=0.0, bus="sfx"):
    i = int(t * SR)
    if i >= N or i < 0:
        return
    x = x[: N - i]
    l, r = BUS[bus]
    l[i:i + len(x)] += x * g * np.sqrt(.5 * (1 - pan))
    r[i:i + len(x)] += x * g * np.sqrt(.5 * (1 + pan))


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


# ---------------------------------------------------------------- beat
def kick(d=.5):
    t = tt(d)
    f = 45 + 120 * np.exp(-t * 28)
    return np.tanh(2.4 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6)) * .5


def snare(d=.35):
    t = tt(d)
    return (bp(rng.standard_normal(len(t)), 1200, 7000) * np.exp(-t * 18) * .25 +
            np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25) * .25)


def hat(d=.06):
    t = tt(d)
    return hp(rng.standard_normal(len(t)), 8000) * np.exp(-t * 80) * .06


def bass808(m, d):
    t = tt(d)
    f = hz(m) * (1 + .5 * np.exp(-t * 30))
    x = np.tanh(1.8 * np.sin(2 * np.pi * np.cumsum(f) / SR))
    return x * np.clip((d - t) / .05, 0, 1) * np.exp(-t * 1.2) * .28


def stab(ms, d=.32):
    t = tt(d)
    x = np.zeros_like(t)
    for m in ms:
        for det in (-.3, .3):
            ph = (hz(m) * (1 + det / 100) * t) % 1
            x += 2 * ph - 1
    return lp(x, 2600) * np.exp(-t * 7) * np.minimum(1, t / .01) * .05


# ---------------------------------------------------------------- arena
def bell(d=1.6):
    t = tt(d)
    x = sum(a * np.sin(2 * np.pi * 820 * r * t) * np.exp(-t * dec)
            for r, a, dec in [(1, 1, 2.5), (2.32, .6, 3.5), (4.25, .4, 5), (5.4, .25, 7)])
    return x * np.minimum(1, t / .002) * .16


def punch(p=1.0):
    t = tt(.4)
    body = np.sin(2 * np.pi * np.cumsum(70 + 90 * np.exp(-t * 40)) / SR) * np.exp(-t * 14)
    crack = bp(rng.standard_normal(len(t)), 900, 6000) * np.exp(-t * 60)
    return np.tanh(2.5 * (body * .8 + crack * .6)) * .45 * p


def whoosh(d=.35, g=1.0):
    t = tt(d)
    n = rng.standard_normal(len(t))
    s = len(t) // 10
    x = np.zeros_like(t)
    for i in range(10):
        lo = 300 * (10 ** (i / 10))
        x[i * s:(i + 1) * s] = bp(n, lo, min(lo * 2.5, 16000))[i * s:(i + 1) * s]
    return x * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5 * .14 * g


def boom(d=2.5):
    t = tt(d)
    x = np.sin(2 * np.pi * np.cumsum(30 + 70 * np.exp(-t * 6)) / SR) * np.exp(-t * 1.6)
    x += .5 * lp(rng.standard_normal(len(t)), 900) * np.exp(-t * 4)
    return np.tanh(2 * x) * .6


def key(d=.05):
    t = tt(d)
    return bp(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t * 120) * .12


def crowd_bed():
    """Arena murmur: band-limited noise with slow random swells, louder on hits and a roar on the K.O."""
    n = rng.standard_normal(N)
    x = bp(n, 250, 2800) * .5 + bp(rng.standard_normal(N), 800, 4000) * .25
    t = np.arange(N) / SR
    env = .35 + .1 * np.sin(t * 1.3) + .08 * np.sin(t * 3.7 + 1)
    for ht, _, p in G.HITS:
        env += .5 * p * np.exp(-np.clip(t - ht, 0, None) * 3) * (t >= ht)
    env += 2.2 * np.exp(-np.clip(t - T["knock"], 0, None) * .9) * (t >= T["knock"])
    env += .8 * np.exp(-np.clip(t - .2, 0, None) * 1.5) * (t >= .2)
    env *= np.where((t > T["yes"]) & (t < T["red"]), .25, 1)          # the quiet room
    env *= np.where((t > T["belt"]), .6, 1)
    env *= 1 - .7 * ((t > T["ko"] + .05) & (t < T["knock"]))             # hush before the punch
    return x * env


def arrange():
    total = int(DUR / BEAT) + 1
    roots = [33, 33, 36, 31]
    for b in range(total):
        t = b * BEAT
        bar = b // 4
        hush = T["ko"] < t < T["knock"] - .05 or T["yes"] < t < T["red"] - .2
        end = t > DUR - 1.2
        if hush or end:
            continue
        if b % 4 in (0, 2) or b % 8 == 7:
            put(kick(), t, 1.0, bus="music")
        if b % 4 in (1, 3):
            put(snare(), t, .9, bus="music")
        for k in range(4):
            put(hat(), t + k * BEAT / 4, .8 if k % 2 else 1.1, pan=.3, bus="music")
        if b % 4 == 0:
            put(bass808(roots[bar % 4], BEAT * 1.6), t, 1.0, bus="music")
            put(bass808(roots[bar % 4] + 3, BEAT * .9), t + BEAT * 2.5, .9, bus="music")
        if b % 8 == 0:
            for j, m in enumerate((69, 72, 76)):
                put(stab([m - 12, m]), t + j * .02, .9, pan=-.2, bus="music")
        if b % 8 == 6:
            put(stab([67, 72, 75]), t, .8, pan=.2, bus="music")


def sfx():
    put(bell(), .05, 1.0)
    put(bell(), .45, .8)
    for t in (T["fight"] + .05, 16.5):
        put(bell(1.0), t, .9)
    for t in (T["ref"], T["ref"] + .35, T["ref"] + .7):
        put(bell(1.0), t, .8)
    for ht, who, p in G.HITS:
        put(punch(p), ht, 1.0, pan=.3 if who == "r" else -.3)
        put(whoosh(.18, .8), ht - .14, .7)
    put(punch(1.6), T["knock"], 1.4)
    put(boom(), T["knock"], 1.0)
    put(whoosh(.5, 1.3), T["knock"] - .45, 1.0)
    put(punch(.6), T["touch"], .8)
    for t in (T["ring"], T["yes"], T["red"], T["blue"], T["fight"], T["judges"], T["screen"], T["verdict"], T["ko"], T["ref"], T["belt"]):
        put(whoosh(.32, 1.0), t - .2, .9)
    for i, t in enumerate(T["named"]):
        put(punch(.25), t, .6)
    for i in range(3):
        put(whoosh(.15, .6), T["verdict"] + .15 + i * .25, .8)
        put(punch(.3), T["verdict"] + .3 + i * .25, .6)
    for i in range(5):
        put(key(), 33.55 + i * .1, 1.2)
    put(bell(1.4), T["belt"] + .05, .6)


def reverb(x, secs=1.6, mix=.2, seed=0):
    r = np.random.default_rng(seed)
    t = np.arange(int(secs * SR)) / SR
    ir = lp(r.standard_normal(len(t)) * np.exp(-t * 3.5), 7000)
    ir /= np.sqrt(np.sum(ir ** 2))
    return x * (1 - mix) + fftconvolve(x, ir)[: len(x)] * mix * 1.5


def rms(x):
    return np.sqrt(np.mean(x ** 2) + 1e-12)


def main():
    arrange()
    sfx()
    c = crowd_bed()
    put(c, 0, 1.0, bus="crowd")
    ml, mr = BUS["music"]
    sl, sr_ = reverb(BUS["sfx"][0], 1.2, .18, 1), reverb(BUS["sfx"][1], 1.2, .18, 2)
    cl, cr = reverb(BUS["crowd"][0], 2.5, .4, 3), reverb(BUS["crowd"][1], 2.5, .4, 4)
    gm, gs, gc = .03 / rms(ml + mr), .06 / rms(sl + sr_), .018 / rms(cl + cr)
    l = ml * gm + sl * gs + cl * gc
    r = mr * gm + sr_ * gs + cr * gc
    env = np.ones(N)
    env[-int(.8 * SR):] = np.linspace(1, 0, int(.8 * SR)) ** 1.4
    st = np.stack([l * env, r * env], 1) * 10 ** (VO_GAIN_DB / 20)
    pk = np.max(np.abs(st))
    if pk > .95:
        st *= .95 / pk
    out = os.path.join(ROOT, "assets", "audio", "music.wav")
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())
    src = "/tmp/claude-0/-home-user-Nxtlvl-Social/e31f97b8-b375-54da-91f5-cccc2674e3c4/scratchpad/vo_fast.wav"
    vo = os.path.join(ROOT, "assets", "audio", "vo.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", f"volume={VO_GAIN_DB}dB,alimiter=limit=0.95:level=false",
                    "-ar", str(SR), vo], check=True)
    o = subprocess.run(["ffmpeg", "-i", vo, "-i", out, "-filter_complex", "amix=inputs=2:normalize=0,ebur128", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    print("wrote", out, "| mix", [ln.strip() for ln in o.splitlines() if ln.strip().startswith("I:")][-1:])


if __name__ == "__main__":
    main()
