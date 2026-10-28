"""Music, sound design and the mastered mix for the haunted-house explainer.

python3 build/audio.py      (from the project root, after build/generate.py; needs numpy, scipy, soundfile, ffmpeg)

Music: original, composed here (no licence or credit needed): a slow music-box waltz in D minor (3/4, 76 bpm) over a
low drone, wind and the house creaking; a heartbeat under the deletion; near silence for the twist; the music box
returns, warmer, for the CTA. SFX: every visual event generate.py logs (cues.json "ev") gets a sound, plus thunder on
every lightning flash world.js draws. Recorded hits come from HyperFrames' bundled library (Pixabay Content License:
commercial use, no credit needed; .claude/skills/media-use/audio/assets/sfx/CREDITS.md); the rest is synthesized.
Writes assets/audio/mix.wav, mastered to -14 LUFS integrated, -1.5 dBTP.
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
SC = T["scenes"]
TW0, TW1 = SC[6]
CTA = SC[7][0]
rng = np.random.default_rng(13)
LIB = os.path.join(os.path.dirname(ROOT), ".claude", "skills", "media-use", "audio", "assets", "sfx")
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


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def put(buf, x, t, g=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= N or i + len(x) <= 0:
        return
    if i < 0:
        x, i = x[-i:], 0
    x = x[: N - i]
    buf[i:i + len(x), 0] += x * g * np.sqrt(.5 * (1 - pan))
    buf[i:i + len(x), 1] += x * g * np.sqrt(.5 * (1 + pan))


def reverb(x, secs=2.0, mix=.3, seed=0):
    r = np.random.default_rng(seed)
    t = np.arange(int(secs * SR)) / SR
    ir = lp(r.standard_normal(len(t)) * np.exp(-t * 6.9 / secs), 6000)
    ir /= np.sqrt(np.sum(ir ** 2))
    return x * (1 - mix) + fftconvolve(x, ir)[: len(x)] * mix * 1.5


def curve(pts):
    t, g = zip(*pts)
    return np.interp(np.arange(N) / SR, t, g)


# ---------------------------------------------------------------- voices
def mbox(m, d=2.4):
    t = tt(d)
    f = hz(m) * (1 + .005 * np.sin(2 * np.pi * .8 * t))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + .3 * np.sin(2 * np.pi * np.cumsum(f * 3.01) / SR) * np.exp(-t * 6) + .1 * np.sin(2 * np.pi * np.cumsum(f * 5.4) / SR) * np.exp(-t * 12)
    return x * np.exp(-t * 2.2) * np.minimum(1, t / .002) * .12


def thump(g=1.0):
    t = tt(.3)
    return np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(42 + 38 * np.exp(-t * 30)) / SR) * np.exp(-t * 14)) * g


def thunder(d=3.2, g=1.0):
    t = tt(d)
    n = lp(rng.standard_normal(len(t)), 400, 3) * 3
    crack = bp(rng.standard_normal(len(t)), 800, 6000) * np.exp(-t * 18)
    env = np.minimum(1, t / .03) * np.exp(-t * 1.4) * (1 + .5 * np.sin(2 * np.pi * 3 * t) * np.exp(-t))
    return (n * env + crack * .6) * .5 * g


def wail(d=1.4, f0=440):
    t = tt(d)
    f = f0 * (1 + .25 * np.sin(np.pi * t / d)) * (1 + .02 * np.sin(2 * np.pi * 6 * t))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + .4 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR)
    breath = bp(rng.standard_normal(len(t)), 600, 3000) * .5
    return (x * .5 + breath) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5 * .18


def shimmer(d=1.2):
    t = tt(d)
    x = sum(np.sin(2 * np.pi * hz(m) * t + k) for k, m in enumerate((86, 89, 93, 98)))
    return x * np.minimum(1, t / .05) * np.exp(-t * 2.5) * .05 + np.sin(2 * np.pi * 70 * t) * np.exp(-t * 2) * .2


def bong(m=50, d=2.5):
    t = tt(d)
    x = sum(np.sin(2 * np.pi * hz(m) * r * t) * a for r, a in ((1, 1), (2.01, .5), (2.76, .35), (5.4, .15)))
    return x * np.exp(-t * 1.6) * np.minimum(1, t / .003) * .3


def hammer():
    t = tt(.25)
    return (np.sin(2 * np.pi * np.cumsum(120 + 200 * np.exp(-t * 50)) / SR) * np.exp(-t * 25) + bp(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t * 60) * .6) * .5


def creak(d=.9):
    t = tt(d)
    f = 180 + 120 * np.sin(np.pi * t / d) + 30 * rng.random()
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (rng.random(len(t)) > .6)
    return bp(x, 300, 2500) * np.sin(np.pi * t / d) * .05


def whooshw(d=.5, g=1.0):
    t = tt(d)
    return bp(rng.standard_normal(len(t)), 300, 2500) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2 * .12 * g


def blip(f, d=.06, g=.15):
    t = tt(d)
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 50) * g


# ---------------------------------------------------------------- the sound design
def sfx():
    buf = np.zeros((N, 2))
    s = smp
    for t, k in T["ev"]:
        if k == "pop": put(buf, s("click-soft", .2), t, .35)
        elif k == "accent": put(buf, blip(hz(81), .2, .12), t, 1)
        elif k == "type": put(buf, s("key-press", .1), t, .35, .3)
        elif k == "press": put(buf, s("key-press", .2), t - .03, .9); put(buf, s("impact-bass-2"), t, .8)
        elif k == "stamp": put(buf, thump(.6), t); put(buf, s("click", .2), t, .4)
        elif k == "rattle":
            u = t
            while u < T["gone"]:
                put(buf, blip(1400 - (u - t) * 300, .03, .06), u, 1, .3); u += .06
        elif k == "thud": put(buf, thump(.8), t); put(buf, s("error", .5), t, .2)
        elif k == "whoosh": put(buf, whooshw(.5, .8), t - .1, 1)
        elif k == "sparkle": put(buf, s("sparkle"), t, .5); put(buf, shimmer(), t, .8)
        elif k == "tick": put(buf, mbox(81 + 3 * (round(t * 7) % 3), 1.0), t, 1.4)
        elif k == "slide": put(buf, whooshw(.4, 1.0), t, 1, -.3)
        elif k == "shutter": put(buf, s("click"), t, .8); put(buf, hp(rng.standard_normal(int(.1 * SR)), 2500) * np.exp(-tt(.1) * 30) * .4, t + .02)
        elif k == "ding": put(buf, mbox(86, 1.4), t, 1.6)
        elif k == "ghost": put(buf, wail(1.4, 420), t, 1.0, -.3)
        elif k == "ward": put(buf, shimmer(1.6), t, 1.4)
        elif k == "clang": put(buf, bong(45, 1.8), t, .8); put(buf, thump(.5), t)
        elif k == "alarm":
            for i in range(4):
                put(buf, bong(57 if i % 2 else 52, 1.6), t + i * .45, .8)
        elif k == "chime": put(buf, s("chime"), t, .4)
        elif k == "drop": put(buf, s("glitch-2", .3), t, .25)
        elif k == "board": put(buf, hammer(), t, .9, (rng.random() - .5) * .8)
        elif k == "lock": put(buf, s("click"), t, .9); put(buf, thump(.5), t)
        elif k == "bonk": put(buf, thump(.4), t); put(buf, blip(110, .15, .12), t)
        elif k == "slam": put(buf, s("impact-bass-1"), t, .6)
        elif k == "key": put(buf, s("key-press", .12), t, .5, (rng.random() - .5) * .6)
        elif k == "send": put(buf, whooshw(.4), t); put(buf, mbox(86, 1.2), t + .1, 1.4)
        elif k == "flip": put(buf, whooshw(.5, 1.2), t)
    # thunder on world.js's lightning flashes, and the ghost's burst on Enter
    for t, g in ((.35, .8), (T["press"], 1.0), (TW0, .9), (T["touch"], .7)):
        put(buf, thunder(3.2, g), t - .05, 1, .2)
    put(buf, wail(1.8, 360), T["press"] + .2, 1.2)
    for i, t in enumerate(np.arange(1.2, DUR, 3.3)):
        put(buf, creak(.8 + .4 * hash_(i)), t + hash_(i + 9), .8, hash_(i + 3) - .5)
    return buf


def hash_(i):
    v = np.sin(i * 127.1 + 311.7) * 43758.5453
    return v - np.floor(v)


# ---------------------------------------------------------------- the bed
THEME = [74, 77, 81, 80, 77, 74, 73, 76, 79, 77, 76, 73, 74, 77, 81, 86, 84, 81, 82, 79, 76, 74, None, None]


def bed():
    out = np.zeros((N, 2))
    t = np.arange(N) / SR
    # drone: D and A, slowly breathing; wind
    for c, det in enumerate((-.1, .12)):
        d = (np.sin(2 * np.pi * (hz(26) + det) * t) * .6 + np.sin(2 * np.pi * (hz(33) + det) * t) * .35 + np.sin(2 * np.pi * (hz(39) + det * 2) * t) * .12)
        out[:, c] += lp(d, 300) * (.8 + .2 * np.sin(2 * np.pi * .09 * t + c))
    wind = np.stack([bp(rng.standard_normal(N), 250, 1400) for _ in range(2)], 1)
    out += wind * (.25 + .2 * np.sin(2 * np.pi * .13 * t))[:, None]
    # heartbeat under the deletion
    hb = np.zeros((N, 2))
    u = T["press"] + .5
    while u < SC[2][0] - .3:
        put(hb, thump(.9), u); put(hb, thump(.6), u + .18)
        u += 60 / (88 + (u - T["press"]) * 4)
    out += hb * .9
    # the music box waltz: from the copy on, quarter = 60/76 s
    q = 60 / 76
    mb = np.zeros((N, 2))
    u, i = SC[2][0], 0
    while u < DUR:
        m = THEME[i % len(THEME)]
        if m is not None and not (TW0 <= u < TW1):
            put(mb, mbox(m + (12 if u >= CTA else 0) * 0), u, 1, .25 if i % 2 else -.25)
            if i % 3 == 0:
                put(mb, mbox(m - 24, 2.6) * .7, u, 1, 0)
        u += q; i += 1
    out += mb * 1.4
    g = curve([(0, .7), (T["press"], .7), (T["press"] + .2, 1.0), (TW0 - .05, 1.0), (TW0, .35), (TW1 - .1, .35), (TW1, .9), (DUR, .9)])
    out *= g[:, None]
    return np.stack([reverb(out[:, c], 2.6, .3, c + 3) for c in (0, 1)], 1)


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
    k = int(.15 / .01)
    on = np.convolve(on.astype(float), np.ones(2 * k + 1), "same") > 0
    talk = np.clip(np.interp(np.arange(N) / hop, np.arange(len(on)), np.convolve(on.astype(float), np.ones(3) / 3, "same")), 0, 1)
    m = bed()
    m = m * (.05 / rms(m)) * (1 - .35 * talk)[:, None]
    fx = sfx()
    fx = np.stack([reverb(fx[:, c], 1.6, .2, c + 5) for c in (0, 1)], 1)
    fx = fx * (.045 / rms(fx)) * (1 - .3 * talk)[:, None]
    fade = np.ones(N)
    fade[-int(.5 * SR):] = np.linspace(1, 0, int(.5 * SR))
    vv = reverb(v, 1.0, .1, 9)
    mix = (m + fx) * fade[:, None] + (vv * (.16 / rms(v[v != 0])))[:, None]
    mix *= min(1, .98 / np.max(np.abs(mix)))
    raw = os.path.join(ROOT, "assets", "audio", "mix_raw.wav")
    sf.write(raw, mix.astype(np.float32), SR, subtype="FLOAT")
    o = ffmpeg("-i", raw, "-af", "loudnorm=I=-13.4:TP=-2.0:LRA=11:print_format=json", "-f", "null", "-").stderr
    meas = json.loads(o[o.rindex("{"):o.rindex("}") + 1])
    af = (f"loudnorm=I=-13.4:TP=-2.0:LRA=11:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
          f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:linear=true")
    out = os.path.join(ROOT, "assets", "audio", "mix.wav")
    ffmpeg("-i", raw, "-af", af + ",alimiter=limit=0.78:level=false:attack=1:release=60", "-ar", str(SR), "-c:a", "pcm_s24le", out)
    os.remove(raw)
    chk = ffmpeg("-i", out, "-af", "ebur128=peak=true", "-f", "null", "-").stderr
    summ = chk[chk.rindex("Summary:"):]
    print("wrote", out, " ".join(ln.strip() for ln in summ.splitlines() if ln.strip().startswith(("I:", "Peak:"))))


if __name__ == "__main__":
    main()
