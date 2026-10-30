"""The mix: voice, the music bed and 8-bit sound effects, mastered to -14 LUFS.

python3 build/audio.py      (from the project root, after build/voice.py and build/generate.py; needs numpy, soundfile, ffmpeg)

Music: assets/audio/music-src.wav, the track the owner supplied (120 BPM). It starts at MUSIC_IN so its breakdown
(source 92.2 s) lands just after "Steam Deck" and its kick returns (source 96.35 s) on the word "console", then fades
out at the end. It sits under the voice and comes up in the gaps and on the end card. Sound effects are synthesised
here (no samples, so no licences): glitch cuts, label slams, letter pops, blips, typing, error buzzes and claps, from
the events build/generate.py wrote to build/cues.json. Writes assets/audio/mix.wav.
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
MUSIC_IN = 61.55
rng = np.random.default_rng(3)


def load(path, ch=2):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", str(ch), "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.float32).reshape(-1, ch).copy()


def env(n, a=.003, r=None):
    e = np.ones(n)
    na = max(1, int(a * SR))
    e[:na] = np.linspace(0, 1, na)
    nr = int((r or n / SR) * SR)
    e[-nr:] *= np.linspace(1, 0, nr) ** 2
    return e


def sq(f0, f1, d, duty=.5):
    n = int(d * SR)
    f = np.geomspace(f0, f1, n)
    ph = np.cumsum(f) / SR
    return np.where(ph % 1 < duty, 1.0, -1.0) * env(n)


def noise(d, lp=1.0):
    n = int(d * SR)
    x = rng.standard_normal(n)
    if lp < 1:
        y = np.zeros(n)
        for i in range(1, n):
            y[i] = y[i - 1] + lp * (x[i] - y[i - 1])
        x = y / (np.abs(y).max() + 1e-9)
    return x * env(n, .001)


def sine(f0, f1, d):
    n = int(d * SR)
    f = np.geomspace(f0, f1, n)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .002)


def mixp(*xs):
    """Sum sounds of different lengths."""
    out = np.zeros(max(len(x) for x in xs))
    for x in xs:
        out[:len(x)] += x
    return out


def crush(x, bits=5):
    q = 2 ** bits
    return np.round(x * q) / q


SFX = {
    "cut": lambda: mixp(.32 * crush(noise(.07, .35)), .12 * sq(1800, 300, .05)),
    "slam": lambda: mixp(.55 * np.tanh(2.5 * sine(110, 42, .22)), .2 * crush(noise(.05, .5))),
    "pop": lambda: .13 * sq(980, 620, .05, .25),
    "tick": lambda: .12 * sq(1480, 1480, .03, .25),
    "blip": lambda: .12 * sq(700, 1050, .045, .5),
    "thump": lambda: .6 * np.tanh(3 * sine(80, 38, .3)),
    "type": lambda: .1 * crush(noise(.018, .6), 4),
    "on": lambda: .12 * sq(220, 900, .12, .5),
    "msg": lambda: .13 * np.concatenate([sq(990, 990, .05, .5), sq(1320, 1320, .07, .5)]),
    "err": lambda: .16 * sq(150, 140, .2, .5),
    "check": lambda: .13 * np.concatenate([sq(660, 660, .06), sq(880, 880, .06), sq(1320, 1320, .12)]),
    "clap": lambda: .3 * np.concatenate([noise(.04, .7), np.zeros(int(.11 * SR)), noise(.04, .7), np.zeros(int(.13 * SR)), noise(.05, .7)]),
}


def main():
    cues = json.load(open(os.path.join(ROOT, "build", "cues.json")))
    dur = cues["dur"]
    N = int(dur * SR)
    voice = load(os.path.join(ROOT, "assets", "audio", "voice.wav"), 1)[:, 0]
    v = np.zeros(N)
    v[:min(N, len(voice))] = voice[:N]
    music = load(os.path.join(ROOT, "assets", "audio", "music-src.wav"))
    m = music[int(MUSIC_IN * SR):int(MUSIC_IN * SR) + N]
    m = np.pad(m, ((0, N - len(m)), (0, 0)))
    # music gain: under the voice, up in the gaps, up on the end card, faded out at the end
    words = json.load(open(os.path.join(ROOT, "build", "words.json")))
    speech = np.zeros(N)
    for w in words:
        speech[int(max(0, w["s"] - .08) * SR):int((w["e"] + .12) * SR)] = 1
    k = int(.12 * SR)
    speech = np.convolve(speech, np.ones(k) / k, mode="same")
    gain_db = -11.5 * speech - 5.0
    t = np.arange(N) / SR
    gain_db += np.where(t > words[-1]["e"] + .1, 4.0, 0.0)
    g = 10 ** (gain_db / 20)
    fade = np.clip((dur - t) / .9, 0, 1)
    m = m * (g * fade)[:, None]
    fx = np.zeros(N)
    for tt, kind in cues["ev"]:
        s = SFX[kind]()
        i = int(tt * SR)
        if i >= N:
            continue
        s = s[:N - i]
        fx[i:i + len(s)] += s
    vo = np.stack([v, v], 1)
    fxs = np.stack([fx, fx], 1) * .55
    mix = vo * 1.0 + m * .9 + fxs
    tmp = os.path.join(ROOT, "assets", "audio", "mix_raw.wav")
    sf.write(tmp, mix.astype(np.float32), SR, subtype="FLOAT")
    out = os.path.join(ROOT, "assets", "audio", "mix.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=8,alimiter=limit=0.89:level=false",
                    "-ar", str(SR), "-c:a", "pcm_s16le", out], check=True)
    os.remove(tmp)
    r = subprocess.run(["ffmpeg", "-i", out, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    lufs = [ln.strip() for ln in r.splitlines() if ln.strip().startswith("I:")][-1]
    print(f"wrote mix.wav {dur} s, {len(cues['ev'])} sound events, {lufs}")


if __name__ == "__main__":
    main()
