"""Music, sound design and the mastered mix for the AI Bank reel.

python3 build/audio.py      (from the project root, after build/generate.py; needs numpy, scipy, soundfile, ffmpeg)

Music: the original score in build/score.py (composed in code, no licence needed). SFX: recorded hits from
HyperFrames' bundled library (Pixabay Content License: commercial use, no credit needed;
.claude/skills/media-use/audio/assets/sfx/CREDITS.md) plus synthesized coins, stamps, robot beeps, ice, an
ATM, the vault door and its alarm. The music and SFX duck under the voice on a speech gate. Writes
assets/audio/mix.wav, mastered to -14 LUFS integrated, -1.5 dBTP.
"""
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
L, E = T["l"], T["e"]
SR = 48000
DUR = T["end"]
N = int(DUR * SR)
rng = np.random.default_rng(7)
SFX = np.zeros((N, 2))
LIB = os.path.join(os.path.dirname(ROOT), ".claude", "skills", "media-use", "audio", "assets", "sfx")
_S = {}


def smp(name, a=0.0, b=None):
    """A bundled SFX file as mono float at 48 kHz, optionally cut to [a, b] s."""
    if name not in _S:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(LIB, name + ".mp3"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                             capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.float32).astype(np.float64)
        _S[name] = x / (np.max(np.abs(x)) + 1e-9) * .5
    x = _S[name]
    return x[int(a * SR):int(b * SR) if b else None]


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, hi], "band", fs=SR, output="sos"), x)


def put(x, t, g=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= N:
        return
    if i < 0:
        x, i = x[-i:], 0
    x = x[: N - i]
    SFX[i:i + len(x), 0] += x * g * np.sqrt(.5 * (1 - pan))
    SFX[i:i + len(x), 1] += x * g * np.sqrt(.5 * (1 + pan))


def crackle(d=1.2):
    n = int(d * SR)
    t = np.arange(n) / SR
    x = bp(rng.standard_normal(n), 800, 6000) * .05
    for _ in range(int(d * 40)):
        i = rng.integers(0, n - 400)
        x[i:i + 400] += bp(rng.standard_normal(400), 1500, 9000) * np.exp(-np.arange(400) / 60) * .4
    return x * np.sin(np.pi * t / d)


def crowd(d, kind, seed=0):
    """A synthesized crowd: boo (low, vowel 'oo', slow swell), roar (bright, fast rise) or chant ('A-I' twice a second)."""
    r = np.random.default_rng(seed)
    n = int(d * SR)
    t = np.arange(n) / SR
    x = r.standard_normal(n)
    if kind == "boo":
        y = bp(x, 180, 520) * 1.4 + bp(x, 600, 900) * .4
        env = np.minimum(1, t / .6) * (.7 + .3 * np.sin(2 * np.pi * .7 * t)) * np.minimum(1, (d - t) / .8)
    elif kind == "roar":
        y = bp(x, 400, 3200) + bp(x, 1800, 5000) * .5
        env = np.minimum(1, t / .12) * np.exp(-np.maximum(0, t - .4) * 1.4)
    else:
        a, i = bp(x, 600, 1100), bp(x, 250, 420) + bp(x, 1900, 2600) * .7
        ph = (t * 2.0) % 1
        y = np.where(ph < .5, a, i) * 1.2
        env = (np.sin(np.pi * (ph % .5) / .5) ** .6) * np.minimum(1, t / .3) * np.minimum(1, (d - t) / .4)
    return y * env


def whistle(d=.5):
    t = np.arange(int(d * SR)) / SR
    f = 3100 + 120 * np.sin(2 * np.pi * 34 * t)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / .02) * np.minimum(1, (d - t) / .05) * .5


def lp(x, f, o=2):
    return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)


def engine(d, f0, f1, shifts=0, g=1.0):
    """A V6 hybrid scream: a saw-ish pulse at the firing frequency with harmonics, rising f0 -> f1 with gear shifts."""
    n = int(d * SR)
    t = np.arange(n) / SR
    u = t / d
    if shifts:
        seg = np.floor(u * (shifts + 1)); fr = (u * (shifts + 1)) % 1
        f = f0 + (f1 - f0) * (seg + fr ** .7) / (shifts + 1) - (f1 - f0) * .18 * (fr < .06) * (seg > 0)
    else:
        f = f0 + (f1 - f0) * u
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = sum(np.sin(k * ph + k) / k ** .8 for k in range(1, 9))
    x += bp(rng.standard_normal(n), 900, 5000) * .25
    x = bp(x, 120, 7000)
    return np.tanh(x * 1.5) * np.minimum(1, t / .05) * np.minimum(1, (d - t) / .08) * .35 * g


def flyby(d=.9, f=780, g=1.0):
    """A car passing close: pitch falls through the pass (doppler), loud at the middle."""
    n = int(d * SR)
    t = np.arange(n) / SR - d / 2
    fr = f * (1 + .22 * -np.tanh(t * 9))
    ph = 2 * np.pi * np.cumsum(fr) / SR
    x = sum(np.sin(k * ph) / k for k in range(1, 7)) + bp(rng.standard_normal(n), 1500, 7000) * .4
    env = 1 / (1 + (t * 7) ** 2)
    return np.tanh(x * 1.4) * env * .5 * g


def noise_bed(d, lo, hi, g=1.0, fade=.4):
    n = int(d * SR)
    t = np.arange(n) / SR
    return bp(rng.standard_normal(n), lo, hi) * np.minimum(1, t / fade) * np.minimum(1, (d - t) / fade) * g


def thunder(d=3.0):
    n = int(d * SR)
    t = np.arange(n) / SR
    x = lp(rng.standard_normal(n), 180, 2) * 3 + bp(rng.standard_normal(n), 200, 900) * np.exp(-t * 6) * 1.5
    return x * np.exp(-t * 1.1) * np.minimum(1, t / .02) * .6


def squeal(d=1.2, f0=2600, f1=1700):
    n = int(d * SR)
    t = np.arange(n) / SR
    f = f0 + (f1 - f0) * t / d + 80 * np.sin(2 * np.pi * 9 * t)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * .6 + bp(rng.standard_normal(n), 1800, 4000) * .5
    return x * np.minimum(1, t / .05) * np.minimum(1, (d - t) / .3) * .4


def crunch(d=.6):
    n = int(d * SR)
    t = np.arange(n) / SR
    x = bp(rng.standard_normal(n), 300, 5000) * np.exp(-t * 9)
    for _ in range(25):
        i = rng.integers(0, n - 600)
        x[i:i + 600] += bp(rng.standard_normal(600), 2000, 9000) * np.exp(-np.arange(600) / 90) * .8
    return x * .8


def squelch(d=.18):
    n = int(d * SR)
    t = np.arange(n) / SR
    return (bp(rng.standard_normal(n), 1200, 4500) * .7 + np.sin(2 * np.pi * 1400 * t) * .2) * np.minimum(1, (d - t) / .03) * .5


def boom(d=1.6):
    n = int(d * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * (60 + 40 * np.exp(-t * 10)) * t) * np.exp(-t * 3) + bp(rng.standard_normal(n), 300, 3000) * np.exp(-t * 7) * .5
    c = crackle(min(d, 1.2))
    x[:len(c)] += c * 1.5
    return x * .6


def heartbeat():
    """lub-dub: two low thumps."""
    n = int(.5 * SR)
    t = np.arange(n) / SR
    beat = lambda t0, f, g: np.where(t >= t0, np.sin(2 * np.pi * f * (t - t0)) * np.exp(-np.maximum(0, t - t0) * 18), 0) * g  # noqa: E731
    return lp(beat(0, 55, 1.0) + beat(.17, 48, .7), 220) * .9


def coin(seed=0):
    """One coin: a short bright ping with a little ring."""
    r = np.random.default_rng(seed)
    n = int(.35 * SR); t = np.arange(n) / SR
    f = 2600 + r.random() * 1400
    x = (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 2.76 * t) + .3 * np.sin(2 * np.pi * f * 5.4 * t)) * np.exp(-t * 18)
    return x * .3


def jingle(d=.8, k=10, seed=0):
    out = np.zeros(int((d + .4) * SR))
    r = np.random.default_rng(seed)
    for j in range(k):
        c = coin(seed * 31 + j); i = int(r.random() * d * SR)
        out[i:i + len(c)] += c * (.5 + .5 * r.random())
    return out


def beep(f, d=.08, g=.3):
    t = np.arange(int(d * SR)) / SR
    return np.sign(np.sin(2 * np.pi * f * t)) * .25 * np.minimum(1, (d - t) / .01) * g


def siren(d):
    t = np.arange(int(d * SR)) / SR
    f = np.where((t * 2.2) % 1 < .5, 760, 560)
    return bp(np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)), 300, 2500) * .22 * np.minimum(1, t / .1) * np.minimum(1, (d - t) / .2)


def hum(d, f=120, g=.2):
    t = np.arange(int(d * SR)) / SR
    return (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 3 * t)) * g * np.minimum(1, t / .3) * np.minimum(1, (d - t) / .3)


def ice(d=.9):
    n = int(d * SR); t = np.arange(n) / SR
    x = bp(rng.standard_normal(n), 3000, 12000) * .15 * np.exp(-t * 3)
    for _ in range(60):
        i = rng.integers(0, n - 300)
        x[i:i + 300] += bp(rng.standard_normal(300), 4000, 14000) * np.exp(-np.arange(300) / 40) * .6
    return x


def clunk():
    n = int(.9 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * (70 + 30 * np.exp(-t * 20)) * t) * np.exp(-t * 6) + bp(rng.standard_normal(n), 200, 2000) * np.exp(-t * 25) * .6) * .8


def sfx():
    cu = T["cuts"]
    for t in cu:
        put(smp("whoosh-short"), t - .1, .45)
    # day 1: the cards pop up, four stamps, the coins into the jar
    put(smp("sparkle"), T["ai"] - .1, .3)
    for k in range(4):
        put(smp("pop"), T["ai"] + .2 + k * .18, .25, (k - 1.5) * .4)
        tc = T["cancels"] + k * .32
        put(smp("impact-bass-2", 0, .4), tc, .35, (k - 1.5) * .4)
        put(smp("click", 0, .08), tc, .4, (k - 1.5) * .4)
        put(jingle(.6, 8, k), tc + .35, .55, (k - 1.5) * .3)
    # day 3: the flight, the argument, the robot gives in, the cash chime
    put(smp("whoosh"), cu[0] + .2, .45)
    for k in range(4):
        tb = T["argues"] - .5 + k * .5
        put(smp("pop"), tb, .3, -.5 if k % 2 == 0 else .5)
        if k % 2:
            for j in range(4):
                put(beep(900 + j * 140), tb + .05 + j * .08, .5, .5)
    put(beep(420, .25), T["drops"], .5, .5); put(beep(300, .35), T["drops"] + .25, .5, .5)
    put(smp("chime"), T["forty"] - .02, .5)
    put(jingle(.5, 6, 9), T["forty"] + .1, .45)
    # 2 AM: the phone, the cart, the freeze
    put(smp("notification"), T["shoes"] - .3, .25)
    put(smp("glitch-2", 0, .4), T["freezes"] - .05, .3)
    put(ice(1.0), T["freezes"], .8)
    put(smp("impact-bass-1"), T["freezes"], .5)
    # week 2: every coin from the cup to the tree, the leaves, the cheer
    for j in range(30):
        put(coin(100 + j), T["coffee"] + j * .1 + .85, .35, .4)
    put(smp("sparkle"), T["hundred"] - .1, .45)
    put(jingle(1.0, 14, 21), T["hundred"], .5)
    # day 21: night street hum, ATM beeps, the block, the rewind
    put(noise_bed(cu[4] - cu[3], 200, 900, .15, .6), cu[3], .4)
    put(hum(cu[4] - cu[3] - 1.5, 120, .12), cu[3] + 1.2, .4, -.3)
    for j in range(5):
        put(smp("key-press", 0, .1), T["tries"] - .6 + j * .12, .3)
    put(beep(600, .1), T["tries"] + .1, .3)
    put(smp("error", 0, .9), T["blocked"], .45)
    put(smp("impact-bass-2"), T["blocked"], .55)
    put(smp("whoosh-cinematic")[::-1].copy(), T["eleven"] - .6, .45)
    # day 30: the wheel, the door, the alarm, the gold rushing up the pipe, the portal
    for j in range(8):
        put(smp("click", 0, .08), cu[4] + .4 + j * .17, .3)
    put(clunk(), T["moves"] - .1, .9)
    put(squeal(1.2, 300, 180) * .7, T["moves"], .5)
    put(siren(T["where"] - T["moves"]), T["moves"] + .2, .55)
    put(noise_bed(T["go"] - T["savings"] + .8, 600, 4000, .45, .3), T["savings"], .6, .3)
    for j in range(24):
        put(coin(300 + j), T["savings"] + j * .1, .25, .3)
    put(hum(T["where"] - T["moves"], 55, .3), T["moves"], .5)
    put(smp("whoosh-cinematic"), T["go"] - .4, .5)
    # real world, the close
    put(smp("notification"), T["visa"] - .2, .35)
    for j in range(14):
        put(smp("key-press", 0, .1), T["forty2"] - .1 + j * .1, .2)
    put(smp("sparkle"), T["forty2"] + 1.4, .35)
    put(smp("pop"), T["trust"] - .45, .35)
    put(smp("ping"), T["follow"], .45)


def reverb(x, secs=1.0, mix=.15, seed=0):
    r = np.random.default_rng(seed)
    t = np.arange(int(secs * SR)) / SR
    ir = sosfilt(butter(2, 8000, "low", fs=SR, output="sos"), r.standard_normal(len(t)) * np.exp(-t * 3.8))
    ir /= np.sqrt(np.sum(ir ** 2))
    return x * (1 - mix) + fftconvolve(x, ir)[: len(x)] * mix * 1.4


def ffmpeg(*a):
    return subprocess.run(["ffmpeg", "-y", "-hide_banner", *a], capture_output=True, text=True, check=True)


def main():
    sfx()
    voice, vsr = sf.read(os.path.join(ROOT, "assets", "audio", "voice.wav"))
    assert vsr == SR
    v = np.zeros(N)
    v[: min(N, len(voice))] = voice[:N]
    rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)  # noqa: E731
    hop = int(.01 * SR)
    fr = np.sqrt(np.mean(v[: N // hop * hop].reshape(-1, hop) ** 2, axis=1))
    on = fr > .1 * np.percentile(fr[fr > 1e-4], 90)
    k = int(.15 / .01)
    on = np.convolve(on.astype(float), np.ones(2 * k + 1), "same") > 0
    ramp = np.convolve(on.astype(float), np.ones(3) / 3, "same")
    talk = np.clip(np.interp(np.arange(N) / hop, np.arange(len(ramp)), ramp), 0, 1)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from score import compose
    m = compose(T, N)
    sf.write(os.path.join(ROOT, "assets", "audio", "score.wav"), m.astype(np.float32), SR, subtype="PCM_24")
    sfxb = np.stack([reverb(SFX[:, c], 1.0, .15, c + 2) for c in (0, 1)], 1)
    # day 30: the world goes muffled under "and it won't tell you where", the voice stays clear
    tt = np.arange(N) / SR
    mw = (np.clip((tt - T["wont"] + .3) / .2, 0, 1) * np.clip((T["cuts"][5] - tt) / .3, 0, 1))[:, None]
    m = m * (1 - mw) + np.stack([lp(m[:, c], 600) for c in (0, 1)], 1) * mw * 1.2
    sfxb = sfxb * (1 - mw * .6) + np.stack([lp(sfxb[:, c], 900) for c in (0, 1)], 1) * mw * .6
    score = m * (.075 / rms(m)) * (1 - .45 * talk)[:, None] + sfxb * (.045 / rms(sfxb)) * (1 - .5 * talk)[:, None]
    fade = np.ones(N)
    fade[-int(.25 * SR):] = np.linspace(1, 0, int(.25 * SR))
    score *= fade[:, None]
    mix = score + (v * (.16 / rms(v[v != 0])))[:, None]
    mix *= min(1, .98 / np.max(np.abs(mix)))
    raw = os.path.join(ROOT, "assets", "audio", "mix_raw.wav")
    sf.write(raw, mix.astype(np.float32), SR, subtype="FLOAT")
    o = ffmpeg("-i", raw, "-af", "loudnorm=I=-13.7:TP=-2.0:LRA=11:print_format=json", "-f", "null", "-").stderr
    meas = json.loads(o[o.rindex("{"):o.rindex("}") + 1])
    af = (f"loudnorm=I=-13.7:TP=-2.0:LRA=11:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
          f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:linear=true")
    out = os.path.join(ROOT, "assets", "audio", "mix.wav")
    ffmpeg("-i", raw, "-af", af + ",alimiter=limit=0.78:level=false:attack=1:release=60", "-ar", str(SR), "-c:a", "pcm_s24le", out)
    os.remove(raw)
    chk = ffmpeg("-i", out, "-af", "ebur128=peak=true", "-f", "null", "-").stderr
    summ = chk[chk.rindex("Summary:"):]
    print("wrote", out, " ".join(ln.strip() for ln in summ.splitlines() if ln.strip().startswith(("I:", "Peak:"))))


if __name__ == "__main__":
    main()
