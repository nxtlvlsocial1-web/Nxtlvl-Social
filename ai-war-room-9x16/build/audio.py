"""Music, sound design and the mastered mix for the AI War Room reel.

python3 build/audio.py      (from the project root, after build/generate.py; needs numpy, scipy, soundfile, ffmpeg)

Music: the original war-room score in build/score.py (composed in code, no licence needed). SFX: recorded hits from
HyperFrames' bundled library (Pixabay Content License: commercial use, no credit needed;
.claude/skills/media-use/audio/assets/sfx/CREDITS.md) plus a synthesized fire crackle. The music and SFX duck under
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


def sfx():
    cut = [L[3] - .15, L[4] - .15, L[5] - .15, L[6] - .15, L[7] - .15]
    # hook
    for i, k in enumerate(("chatgpt", "claude", "gemini", "grok")):
        put(smp("whoosh-short"), T[k] - .15, .45, (i - 1.5) / 2)
        put(smp("pop"), T[k], .3, (i - 1.5) / 2)
    put(smp("click"), T["fifteen"] - .05, .5)
    put(smp("impact-bass-1"), T["humans"] - .08, .9)
    # setup and shortcuts
    put(smp("whoosh"), T["emergence"] - .2, .45)
    for j in range(10):
        put(smp("click-soft", 0, .15), T["ten"] - .1 + j * .045, .35, (j - 5) / 6)
    put(smp("chime", 0, 1.6), T["credits"] - .15, .35)
    for k in ("punch", "steal", "fire"):
        put(smp("click"), T[k] - .08, .55)
    put(smp("impact-bass-2"), T["banned"] - .05, .8)
    put(smp("error", 0, 1.0), T["banned"], .3)
    put(smp("whoosh-cinematic", 2.0, 3.4), T["who"] - .4, .5)
    # chapter cuts
    for t in cut:
        put(smp("whoosh-short"), t - .1, .5)
    # Grok
    for j in range(14):
        put(smp("pop"), T["assaults"] - .2 + j * (T["e183"] - T["assaults"]) / 14, .18, np.sin(j) * .6)
    put(crackle(2.5), T["six"] - .05, .7)
    put(smp("impact-bass-1"), T["e183"] - .05, .8)
    put(smp("impact-bass-2"), T["alive4"] - .05, .8)
    put(smp("glitch-1", 0, .7), T["alive4"] - .05, .4)
    # Gemini
    for j in range(18):
        put(smp("pop"), T["g683"] - .2 + j * (T["climbing"] - T["g683"]) / 18, .15, np.sin(j * 1.7) * .6)
    put(crackle(1.8), T["g683"] + .3, .55, .3)
    put(smp("impact-bass-1"), T["g683"] + .55, .6)
    put(smp("glitch-2", 0, .9), T["delete"] + .2, .35)
    # ChatGPT
    put(smp("pop"), T["two"] - .05, .35)
    put(smp("pop"), T["two"] + .2, .35)
    put(smp("impact-bass-2"), T["seven"] - .05, .55)
    # Claude
    put(smp("chime"), T["zero"] - .1, .45)
    put(smp("sparkle"), T["allten"] - .05, .5)
    # mixed world
    put(smp("whoosh-cinematic", 1.0, 3.2), T["oneworld"] - 1.1, .55)
    put(smp("glitch-1", 0, .6), T["stealing"] - .05, .4)
    put(smp("impact-bass-1"), T["drift"] - .1, .7)
    put(smp("sparkle"), T["drift"] - .05, .4)
    # CTA
    a = T["town"] - .12
    for i in range(4):
        put(smp("key-press", 0, .15), a + .05 + i * .08, .45, (i - 1.5) / 3)
    put(smp("ping"), E[8] + .1, .5)


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
