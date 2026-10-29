"""Music, sound design and the mastered mix for the Hallmark noir.

python3 build/audio.py      (from the project root, after build/generate.py; needs numpy, scipy, soundfile, ffmpeg)

Music: "Noire #1" by Music By Pedro (royalty-free, YouTube; credited in the post), from its first note, spliced into
its own final phrase so it resolves under the CTA and "Case closed". Under it: rain on the window, wind in gusts, thunder
on world.js's lightning. SFX: every event generate.py logs (cues.json "ev"): the door, her heels, the laptop, the loupe,
the markers, the rotary dial, the card, the deal, the book, the ticks, the keys, the reveal, the stamp. Recorded hits
come from HyperFrames' bundled library (Pixabay Content License: commercial use, no credit needed); the rest is
synthesized. Writes assets/audio/mix.wav, mastered to -14 LUFS integrated, under -1.5 dBTP.
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
SR = 48000
DUR = T["end"]
N = int(DUR * SR)
rng = np.random.default_rng(29)
LIB = os.path.join(os.path.dirname(ROOT), ".claude", "skills", "media-use", "audio", "assets", "sfx")
MUSIC = os.path.join(ROOT, "assets", "audio", "src", "noire1.wav")
ENDING_SRC = 159.2          # the track's final phrase (after its last pause), in the source
ENDING_AT = T["cut"][13] - .8   # where that phrase lands in the film: under the CTA
_S = {}


def smp(name, d=None):
    if name not in _S:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(LIB, name + ".mp3"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                             capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.float32).astype(np.float64)
        _S[name] = x / (np.max(np.abs(x)) + 1e-9) * .5
    x = _S[name]
    return x[: int(d * SR)] if d else x


def lp(x, fc, o=2):
    return sosfilt(butter(o, min(fc, SR / 2 - 100), "low", fs=SR, output="sos"), x, axis=0)


def hp(x, fc, o=2):
    return sosfilt(butter(o, fc, "high", fs=SR, output="sos"), x, axis=0)


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, min(hi, SR / 2 - 100)], "band", fs=SR, output="sos"), x, axis=0)


def tt(d):
    return np.arange(int(d * SR)) / SR


def put(buf, x, t, g=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= N or i + len(x) <= 0:
        return
    if i < 0:
        x, i = x[-i:], 0
    x = x[: N - i]
    buf[i:i + len(x), 0] += x * g * np.sqrt(.5 * (1 - pan))
    buf[i:i + len(x), 1] += x * g * np.sqrt(.5 * (1 + pan))


def reverb(x, secs=1.6, mix=.25, seed=0):
    r = np.random.default_rng(seed)
    t = np.arange(int(secs * SR)) / SR
    ir = lp(r.standard_normal(len(t)) * np.exp(-t * 6.9 / secs), 5000)
    ir /= np.sqrt(np.sum(ir ** 2))
    return x * (1 - mix) + fftconvolve(x, ir)[: len(x)] * mix * 1.5


def noise(d):
    return rng.standard_normal(int(d * SR))


# ---------------------------------------------------------------- foley
def thump(g=1.0, f0=55, d=.35):
    t = tt(d)
    return np.tanh(1.5 * np.sin(2 * np.pi * np.cumsum(f0 + 60 * np.exp(-t * 30)) / SR) * np.exp(-t * 12)) * g


def knock(f=900, d=.08, g=.5):   # a hard tap: wood, plastic, a heel
    t = tt(d)
    return (bp(noise(d), f * .6, f * 2.5) * np.exp(-t * 60) + np.sin(2 * np.pi * f * .4 * t) * np.exp(-t * 45) * .6) * g


def creak(d=1.1):
    t = tt(d)
    f = 140 + 90 * np.sin(np.pi * t / d) + 25 * np.sin(2 * np.pi * 3.3 * t)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (rng.random(len(t)) > .55)
    return bp(x, 250, 2200) * np.sin(np.pi * t / d) * .09


def ratchet(d=.5, rate=22):    # the rotary dial running back
    x = np.zeros(int(d * SR))
    for k in range(int(d * rate)):
        c = knock(2600, .012, .35)
        i = int(k / rate * SR); x[i:i + len(c)] += c[: len(x) - i]
    return x


def paper(d=.25, g=.4):
    t = tt(d)
    return bp(noise(d), 1500, 9000) * np.sin(np.pi * t / d) ** .6 * (1 + .5 * np.sin(2 * np.pi * 30 * t)) * g * .25


def swell(d=1.4):
    t = tt(d)
    x = sum(np.sin(2 * np.pi * f * t + k) for k, f in enumerate((523.3, 659.3, 784.0, 987.8)))
    return x * np.minimum(1, t / .5) * np.exp(-t * 1.6) * .04


def thunder(d=3.4, g=1.0):
    t = tt(d)
    n = lp(noise(d), 380, 3) * 3
    crack = bp(noise(d), 800, 6000) * np.exp(-t * 16)
    env = np.minimum(1, t / .03) * np.exp(-t * 1.2) * (1 + .5 * np.sin(2 * np.pi * 2.6 * t) * np.exp(-t))
    return (n * env + crack * .5) * .5 * g


def sfx():
    buf = np.zeros((N, 2))
    s = smp
    for t, k in T["ev"]:
        if k == "door": put(buf, creak(1.2), t, 1.3, -.6)
        elif k == "doorclose": put(buf, thump(.5, 70, .3), t, 1, -.6); put(buf, knock(500, .1, .4), t, 1, -.6)
        elif k == "step": put(buf, knock(1400, .06, .5), t, 1, -.4 + .1 * (t - T["enter"]))
        elif k == "laptop": put(buf, thump(.35, 90, .2), t, 1); put(buf, knock(1800, .05, .3), t + .02)
        elif k == "chime": put(buf, s("chime"), t, .25)
        elif k == "loupe": put(buf, s("whoosh-short"), t, .25, .2)
        elif k == "marker": put(buf, knock(1100, .07, .55), t, 1, .3)
        elif k == "brim": put(buf, paper(.3, .6), t, 1)
        elif k == "handset": put(buf, knock(700, .09, .6), t, 1, .3); put(buf, thump(.2, 120, .15), t)
        elif k == "dial": put(buf, ratchet(.35), t + .1, 1, .3)
        elif k == "card": put(buf, paper(.35, .9), t, 1, .2)
        elif k == "deal": put(buf, paper(.12, 1.2), t, 1, (rng.random() - .5) * .6)
        elif k == "book": put(buf, thump(1.2, 50, .5), t, 1); put(buf, s("impact-bass-1"), t, .35)
        elif k == "tick": put(buf, paper(.08, 1.4), t, 1, .1)
        elif k == "key": put(buf, s("key-press", .1), t, .35, (rng.random() - .5) * .4)
        elif k == "reveal": put(buf, s("sparkle"), t, .3); put(buf, swell(1.8), t, 1)
        elif k == "warm": put(buf, swell(1.4), t, .6)
        elif k == "lift": put(buf, paper(.3, .5), t, 1)
        elif k == "stamp": put(buf, thump(1.1, 48, .45), t, 1); put(buf, knock(600, .12, .7), t); put(buf, s("impact-bass-2"), t, .35)
        elif k == "slam": put(buf, s("whoosh-cinematic", 1.2), t - .25, .25)
        elif k == "cut": put(buf, s("whoosh-short"), t - .08, .06, (rng.random() - .5) * .5)
    for at, k in T["lightning"]:
        put(buf, thunder(3.4, .9 * k), at + .15, 1, .25)
    return buf


def ambience():
    t = np.arange(N) / SR
    gust = .5 + .5 * np.sin(t * .7) * np.sin(t * .23 + 1)
    rain = np.stack([hp(bp(noise(DUR), 900, 9000), 600) for _ in range(2)], 1) * .5
    drops = np.zeros((N, 2))
    for i in range(int(DUR * 30)):
        put(drops, knock(2000 + rng.random() * 2500, .02, .12), rng.random() * DUR, 1, rng.random() * 1.6 - .8)
    wind = np.stack([bp(noise(DUR), 120 + 60 * c, 700) for c in range(2)], 1) * (.4 + 1.1 * gust)[:, None]
    return rain * (.8 + .3 * gust)[:, None] + drops + wind * .7


def music():
    x, sr = sf.read(MUSIC)
    assert sr == SR
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    first = x[: int((ENDING_AT + .6) * SR)]
    end = x[int(ENDING_SRC * SR): int(ENDING_SRC * SR) + N - int(ENDING_AT * SR)]
    out = np.zeros((N, 2))
    out[: len(first)] = first
    xf = int(.6 * SR)
    i = int(ENDING_AT * SR)
    ramp = np.linspace(0, 1, xf)[:, None]
    out[i:i + xf] = out[i:i + xf] * (1 - ramp) + end[:xf] * ramp
    out[i + xf:i + len(end)] = end[xf:len(end)][: N - i - xf]
    fade = int(1.2 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 1.5
    return out


def ffmpeg(*a):
    return subprocess.run(["ffmpeg", "-y", "-hide_banner", *a], capture_output=True, text=True, check=True)


def main():
    voice, vsr = sf.read(os.path.join(ROOT, "assets", "audio", "voice.wav"))
    assert vsr == SR
    v = np.zeros(N)
    v[: min(N, len(voice))] = voice[:N]
    rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)  # noqa: E731
    hop = int(.01 * SR)
    fr = np.sqrt(np.mean(v[: N // hop * hop].reshape(-1, hop) ** 2, axis=1))
    on = fr > .1 * np.percentile(fr[fr > 1e-4], 90)
    k = int(.2 / .01)
    on = np.convolve(on.astype(float), np.ones(2 * k + 1), "same") > 0
    talk = np.clip(np.interp(np.arange(N) / hop, np.arange(len(on)), np.convolve(on.astype(float), np.ones(9) / 9, "same")), 0, 1)
    m = music(); m = m * (.075 / rms(m)) * (1 - .45 * talk)[:, None]
    a = ambience(); a = a * (.018 / rms(a))
    fx = sfx(); fx = np.stack([reverb(fx[:, c], 1.2, .2, c + 5) for c in (0, 1)], 1)
    fx = fx * (.03 / rms(fx)) * (1 - .25 * talk)[:, None]
    vv = reverb(v, .8, .08, 9)
    mix = m + a + fx + (vv * (.16 / rms(v[v != 0])))[:, None]
    mix *= min(1, .98 / np.max(np.abs(mix)))
    raw = os.path.join(ROOT, "assets", "audio", "mix_raw.wav")
    sf.write(raw, mix.astype(np.float32), SR, subtype="FLOAT")
    o = ffmpeg("-i", raw, "-af", "loudnorm=I=-12.6:TP=-2.0:LRA=11:print_format=json", "-f", "null", "-").stderr
    meas = json.loads(o[o.rindex("{"):o.rindex("}") + 1])
    af = (f"loudnorm=I=-12.6:TP=-2.0:LRA=11:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
          f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:linear=true")
    out = os.path.join(ROOT, "assets", "audio", "mix.wav")
    ffmpeg("-i", raw, "-af", af + ",alimiter=limit=0.78:level=false:attack=1:release=60", "-ar", str(SR), "-c:a", "pcm_s24le", out)
    os.remove(raw)
    chk = ffmpeg("-i", out, "-af", "ebur128=peak=true", "-f", "null", "-").stderr
    summ = chk[chk.rindex("Summary:"):]
    print("wrote", out, " ".join(ln.strip() for ln in summ.splitlines() if ln.strip().startswith(("I:", "Peak:"))))


if __name__ == "__main__":
    main()
