"""Music, sound design and the mastered mix for the AI Football Club reel.

python3 build/audio.py      (from the project root, after build/generate.py; needs numpy, scipy, soundfile, ffmpeg)

Music: the original score in build/score.py (composed in code, no licence needed). SFX: recorded hits from
HyperFrames' bundled library (Pixabay Content License: commercial use, no credit needed;
.claude/skills/media-use/audio/assets/sfx/CREDITS.md) plus synthesized crowd (boos, roars, the chant) and whistles. The music and SFX duck under
the voice on a speech gate. Writes assets/audio/mix.wav, mastered to -14 LUFS integrated, -1.5 dBTP.
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
rng = np.random.default_rng(5)
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


def sfx():
    G = T["goals_t"]
    cut = [L[1] - .12, L[2] - .12, L[3] - .12, L[4] - .12, L[5] - .12, L[6] - .12, L[7] - .12]
    for t in cut:
        put(smp("whoosh-short"), t - .08, .4)
    # hook: kick-off whistle, the boos, the BENCHED stamp
    put(whistle(.6), .05, .5)
    put(crowd(6.6, "boo", 1), .3, .9)
    put(smp("impact-bass-2"), T["benched"] - .05, .6)
    for j in range(7):
        put(smp("click-soft", 0, .12), T["thirty"] + j * .05, .25, (j - 3) / 4)
    # the montage: ball kicks and a roar per goal, the full-time whistle
    for k, g in enumerate(G[:4]):
        put(smp("click", 0, .1), g, .5, (k - 1.5) / 3)
        put(crowd(1.4, "roar", 10 + k), g + .25, .55)
    put(whistle(.35), T["fournil"] - .3, .45)
    put(whistle(.7), T["fournil"] + .05, .45)
    put(smp("ping"), T["tracking"] - .05, .3)
    # week 3: the signing card, the debut goal
    put(smp("pop"), T["signs"] - .05, .35)
    put(smp("key-press", 0, .12), T["seventeen"], .3)
    put(smp("click", 0, .1), G[4], .55)
    put(crowd(2.2, "roar", 20), E[2] - .05, .85)            # after "debut", so the word stays clear
    # half-time: the two away goals (quiet), the rewire, three home goals
    for k, g in enumerate(G[5:7]):
        put(smp("click", 0, .1), g, .35)
    put(whistle(.5), T["twonil"] + .9, .35)
    put(smp("glitch-1", 0, .6), T["rewires"] - .05, .35)
    for j in range(6):
        put(smp("click-soft", 0, .12), T["heart"] + j * .28, .3)
    for k, g in enumerate(G[7:10]):
        put(smp("click", 0, .1), g, .5)
        put(crowd(1.6, "roar", 30 + k), g + .35, .7)
    # Christmas: the table, the chant
    put(smp("whoosh"), T["top"] - .3, .35)
    put(smp("sparkle"), T["top"] + .3, .4)
    put(crowd(E[4] - T["chanting"] + .6, "chant", 40), T["chanting"] - .2, .8)
    # January: the stamp, the final, the winner, the silence
    put(smp("impact-bass-2"), T["sells"] - .05, .6)
    put(smp("error", 0, .9), T["warning"] - .05, .25)
    put(whistle(.5), T["cup"] - .1, .35)
    put(smp("click", 0, .1), G[10], .55)
    put(crowd(2.4, "roar", 50), T["winner"] + .5, .5, .7)
    # real world, the close
    put(smp("notification"), T["liverpool"] - .15, .35)
    put(smp("pop"), T["nine"] - .1, .4)
    put(smp("pop"), T["trust"] - .3, .35)
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
