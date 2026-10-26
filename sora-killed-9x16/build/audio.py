"""Original score and sound design for Why OpenAI Killed Sora, synthesized here so there are no rights issues.

python3 -I build/audio.py      (run from the project root, after build/vo.py and build/generate.py; needs numpy, scipy, soundfile, ffmpeg)

A dark 140 bpm trap beat (half-time kick and snare, rolling hats, gliding 808, a minor bell motif) that drops out for a
beat before "killed" and for the CTA tail; a riser into the first cut, a glitch and impact on the red X, coin blips as
the video tiles hit the GPU, three slams on EVERY / SINGLE / TIME, a down-sweep on LOSS, a stamp on DECLINED, a clunk
when the scale tips, a ding and click on FOLLOW and a whoosh on every scene cut. The music bus is ducked under the
voiceover (sidechain from vo.wav), then everything is written as assets/audio/music.wav; vo.wav is vo_raw.wav with the same lift.
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, resample_poly, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUES = json.load(open(os.path.join(ROOT, "build", "cues.json")))
T, TILES, SCENES = CUES["T"], CUES["TILES"], CUES["SCENES"]
SR = 44100
DUR = 30.0
N = int(DUR * SR)
BPM = 140
BEAT = 60 / BPM
GAIN_DB = 3.0   # lifts voice and bed together toward -14 LUFS for Shorts / Reels
rng = np.random.default_rng(11)


def lp(x, fc, o=2):
    return sosfilt(butter(o, fc, "low", fs=SR, output="sos"), x)


def hp(x, fc, o=2):
    return sosfilt(butter(o, fc, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, hi], "band", fs=SR, output="sos"), x)


def tt(d):
    return np.arange(int(d * SR)) / SR


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


BUS = {k: np.zeros((N, 2)) for k in ("music", "sfx")}


def put(x, t, g=1.0, pan=0.0, bus="sfx"):
    i = int(t * SR)
    if i >= N or i < 0:
        return
    x = x[: N - i]
    BUS[bus][i:i + len(x), 0] += x * g * np.sqrt(.5 * (1 - pan))
    BUS[bus][i:i + len(x), 1] += x * g * np.sqrt(.5 * (1 + pan))


# ---------------------------------------------------------------- beat
def kick(d=.45):
    t = tt(d)
    f = 48 + 140 * np.exp(-t * 30)
    return np.tanh(2.6 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)) * .55


def snare(d=.4):
    t = tt(d)
    return (bp(rng.standard_normal(len(t)), 1500, 9000) * np.exp(-t * 16) * .3 +
            np.sin(2 * np.pi * 200 * t) * np.exp(-t * 28) * .3 + clap() * .6)


def clap():
    t = tt(.4)
    n = bp(rng.standard_normal(len(t)), 900, 5000)
    env = sum(np.exp(-np.clip(t - o, 0, None) * 60) * (t >= o) for o in (0, .012, .024)) + .4 * np.exp(-t * 12)
    return n * env * .18


def hat(d=.05, g=1.0):
    t = tt(d)
    return hp(rng.standard_normal(len(t)), 7500) * np.exp(-t * 90) * .07 * g


def bass808(m, d, glide_to=None):
    t = tt(d)
    f0 = hz(m)
    f = f0 * np.ones_like(t)
    if glide_to is not None:
        f = f0 + (hz(glide_to) - f0) * np.clip((t - d * .55) / (d * .3), 0, 1)
    x = np.tanh(2.0 * np.sin(2 * np.pi * np.cumsum(f) / SR))
    return lp(x, 900) * np.clip((d - t) / .04, 0, 1) * np.minimum(1, t / .004) * np.exp(-t * .7) * .3


def bell(m, d=.9):
    t = tt(d)
    x = sum(a * np.sin(2 * np.pi * hz(m) * r * t) * np.exp(-t * k) for r, a, k in [(1, 1, 3), (2.0, .35, 5), (3.01, .2, 8), (4.2, .1, 11)])
    return x * np.minimum(1, t / .003) * .07


def pad(ms, d):
    t = tt(d)
    x = np.zeros_like(t)
    for m in ms:
        for det in (-.12, .12):
            x += np.sin(2 * np.pi * hz(m) * (1 + det / 100) * t + np.sin(2 * np.pi * .3 * t))
    return lp(x, 1400) * np.minimum(1, t / .6) * np.minimum(1, (d - t) / .6) * .012


# ---------------------------------------------------------------- sfx
def whoosh(d=.35, g=1.0, rev=False):
    t = tt(d)
    n = rng.standard_normal(len(t))
    s = len(t) // 12
    x = np.zeros_like(t)
    for i in range(12):
        lo = 250 * (10 ** (i / 11 * 1.3))
        x[i * s:(i + 1) * s] = bp(n, lo, min(lo * 2.4, 18000))[i * s:(i + 1) * s]
    x = x * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.6 * .16 * g
    return x[::-1] if rev else x


def impact(p=1.0):
    t = tt(1.2)
    body = np.sin(2 * np.pi * np.cumsum(38 + 110 * np.exp(-t * 22)) / SR) * np.exp(-t * 4.5)
    crack = bp(rng.standard_normal(len(t)), 700, 7000) * np.exp(-t * 35)
    return np.tanh(2.4 * (body + crack * .5)) * .5 * p


def riser(d=1.6):
    t = tt(d)
    f = 200 * 2 ** (t / d * 3)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * .25 + bp(rng.standard_normal(len(t)), 2000, 9000) * .4 * (t / d)
    return x * (t / d) ** 2 * .18


def glitch(d=.45):
    t = tt(d)
    x = np.zeros_like(t)
    seg = int(.025 * SR)
    for i in range(0, len(t), seg):
        k = (i // seg) % 5
        tone = np.sin(2 * np.pi * (300 + 900 * k) * t[i:i + seg]) if k % 2 else np.sign(np.sin(2 * np.pi * (80 + 40 * k) * t[i:i + seg]))
        x[i:i + seg] = tone[: len(x[i:i + seg])] * (.6 if k != 3 else 0)
    x += hp(rng.standard_normal(len(t)), 3000) * .3
    q = np.round(x * 6) / 6
    return q * np.exp(-t * 3) * .18


def coin():
    t = tt(.35)
    x = np.sin(2 * np.pi * hz(88) * t) * (t < .07) + np.sin(2 * np.pi * hz(95) * t) * (t >= .07)
    return x * np.exp(-t * 9) * np.minimum(1, t / .002) * .09


def downsweep(d=1.0):
    t = tt(d)
    f = 900 * 2 ** (-t / d * 3.5)
    return np.tanh(1.5 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 1.5) * .12


def stamp():
    t = tt(.5)
    thud = np.sin(2 * np.pi * np.cumsum(60 + 120 * np.exp(-t * 50)) / SR) * np.exp(-t * 14)
    slap = bp(rng.standard_normal(len(t)), 400, 3500) * np.exp(-t * 45)
    return np.tanh(2 * (thud + slap * .8)) * .45


def clunk():
    t = tt(.5)
    x = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in [(180, 14), (412, 20), (930, 30)])
    return (x * .3 + bp(rng.standard_normal(len(t)), 300, 2500) * np.exp(-t * 40) * .5) * .4


def ding():
    t = tt(1.4)
    x = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, a, k in [(1318.5, 1, 3), (2637, .4, 5), (1975.5, .3, 4)])
    return x * np.minimum(1, t / .002) * .09


def click():
    t = tt(.04)
    return bp(rng.standard_normal(len(t)), 2000, 8000) * np.exp(-t * 200) * .25


# ---------------------------------------------------------------- arrangement
def arrange():
    roots = [38, 38, 41, 36]           # D minor-ish: D, D, F, C (808 in octave 2)
    motif = [74, 77, 76, 72, 74, 69, 70, 72]
    nb = int(DUR / BEAT) + 1
    for b in range(nb):
        t = b * BEAT
        bar, pos = b // 4, b % 4
        drop = T["killed"] - BEAT * 1.0 < t < T["killed"] - .02      # one beat of air before KILLED
        tail = t > 28.6
        intro = t < 3.0
        if drop or tail:
            continue
        # half-time: kick on 1 and the "and" of 2, snare/clap on 3
        if pos == 0 or (pos == 1 and bar % 2 == 1):
            put(kick(), t, 1.0, bus="music")
        if pos == 1 and not intro:
            put(kick(), t + BEAT * .5, .8, bus="music")
        if pos == 2:
            put(snare(), t, .9 if not intro else .6, bus="music")
        # hats: 8ths, with 16th and triplet rolls at bar ends
        roll = pos == 3 and bar % 2 == 1 and not intro
        steps = ([k / 2 for k in range(2)] if not roll else [k / 6 for k in range(6)])
        for k, s in enumerate(steps):
            put(hat(g=1.2 if k == 0 else .8), t + s * BEAT, 1.0, pan=.25, bus="music")
        if pos == 0:
            r = roots[bar % 4]
            put(bass808(r, BEAT * 2.6, glide_to=r + (5 if bar % 4 == 3 else 0)), t, 1.0 if not intro else .7, bus="music")
        # bell motif on 8ths every other bar
        if bar % 2 == 0 and pos < 2:
            for k in range(4):
                put(bell(motif[(pos * 4 + k) % 8]), t + k * BEAT / 2, .9, pan=-.2, bus="music")
    for i, s in enumerate(range(0, 30, 4)):
        put(pad([62, 65, 69] if i % 2 == 0 else [60, 64, 67], 4.2), s, 1.0, bus="music")


def sfx():
    put(impact(.8), 0.0, 1.0)                    # cold open hit
    put(whoosh(.4, 1.0), 0.02, .8)
    for t in CUES["REACT"]:
        put(click(), t, .5, pan=(t * 7 % 2) - 1)
    put(impact(.7), T["viral"], 1.0)
    put(riser(1.5), SCENES[1] - 1.5, 1.0)
    for c in SCENES[1:-1]:
        put(whoosh(.36, 1.1), c - .22, 1.0)
    put(glitch(.3), 3.0, .9)
    put(glitch(.5), T["killed"], 1.0)
    put(impact(1.3), T["killed"] + .05, 1.0)
    put(stamp(), T["killed"] + .5, 1.0)
    for i, t in enumerate(TILES):
        put(whoosh(.25, .6), t - .3, .6, pan=-.4 if i % 2 == 0 else .4)
        put(coin(), t, 1.0, pan=(-.3 if i % 2 else .3))
    for t in (T["every2"], T["single"], T["time"]):
        put(impact(1.1), t, 1.0)
    put(downsweep(1.1), T["loss"] - .05, 1.0)
    put(impact(.9), T["loss"], .9)
    put(coin(), T["hype"], 1.0)
    put(clunk(), T["hype"] + .32, .6)
    put(stamp(), T["bills"], 1.1)
    put(impact(.8), T["hype2"], .9)
    put(clunk(), T["beats"], 1.0)
    put(ding(), T["cool"] + .1, .7)
    put(impact(.7), T["cool"] + .1, .8)
    put(ding(), T["follow"], 1.0)
    put(click(), T["tap"], 1.4)
    put(ding(), T["tap"] + .1, .6)


def reverb(x, secs=1.4, mix=.18, seed=0):
    r = np.random.default_rng(seed)
    t = np.arange(int(secs * SR)) / SR
    ir = lp(r.standard_normal(len(t)) * np.exp(-t * 4), 7000)
    ir /= np.sqrt(np.sum(ir ** 2))
    return x * (1 - mix) + fftconvolve(x, ir)[: len(x)] * mix * 1.4


def rms(x):
    return np.sqrt(np.mean(x ** 2) + 1e-12)


def sidechain(vo):
    """Gain curve for the music bus: down ~9 dB while the voice speaks (30 ms attack, 280 ms release)."""
    hop = int(.01 * SR)
    env = np.array([np.sqrt(np.mean(vo[i:i + hop] ** 2)) for i in range(0, N, hop)])
    on = np.clip(env / .03, 0, 1)
    g = np.ones_like(on)
    cur = 1.0
    for i, v in enumerate(on):
        target = 1 - .65 * v
        a = .3 if target < cur else .035
        cur += (target - cur) * a
        g[i] = cur
    return np.repeat(g, hop)[:N]


def main():
    arrange()
    sfx()
    raw = os.path.join(ROOT, "assets", "audio", "vo_raw.wav")
    vo_out = os.path.join(ROOT, "assets", "audio", "vo.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af",
                    f"aresample={SR},volume={GAIN_DB}dB,alimiter=limit=0.89:level=false", vo_out], check=True)
    vo, vsr = sf.read(vo_out)
    vo = resample_poly(vo, SR, vsr)[:N]
    vo = np.pad(vo, (0, N - len(vo)))
    m = BUS["music"]
    m = np.stack([reverb(m[:, 0], 1.6, .14, 1), reverb(m[:, 1], 1.6, .14, 2)], 1)
    s = np.stack([reverb(BUS["sfx"][:, 0], 1.1, .16, 3), reverb(BUS["sfx"][:, 1], 1.1, .16, 4)], 1)
    m *= .05 / rms(m)
    s *= .06 / rms(s)
    g = sidechain(vo)
    mix = m * g[:, None] + s * (1 - .25 * (1 - g))[:, None]
    fade = np.ones(N)
    fade[-int(1.0 * SR):] = np.linspace(1, 0, int(1.0 * SR)) ** 1.5
    mix *= fade[:, None] * 2.2 * 10 ** (GAIN_DB / 20)
    mix = np.tanh(mix / .9) * .9   # soft clip the transients instead of pulling the whole bed down
    out = os.path.join(ROOT, "assets", "audio", "music.wav")
    sf.write(out, mix.astype(np.float32), SR, subtype="PCM_16")
    o = subprocess.run(["ffmpeg", "-i", vo_out, "-i", out, "-filter_complex",
                        "[0]aresample=44100,pan=stereo|c0=c0|c1=c0[v];[v][1]amix=inputs=2:normalize=0,ebur128", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    print("wrote", out, "| mix", [ln.strip() for ln in o.splitlines() if ln.strip().startswith(("I:", "Peak"))][-2:])


if __name__ == "__main__":
    main()
