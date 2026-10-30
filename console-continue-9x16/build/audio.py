"""The mix: voice, the music bed and synthesised game-UI sound effects, mastered to -14 LUFS.

python3 build/audio.py      (from the project root, after build/voice.py and build/generate.py; needs numpy, soundfile, ffmpeg)

Music: assets/audio/music-src.wav, the track the owner supplied (120 BPM). It starts at MUSIC_IN so its breakdown
(source 92.2 s) lands after "Steam Deck" and its kick returns (source 96.35 s) on the word "console". During the
GAME OVER countdown it plays muffled (low-passed, like a game paused in another room) and opens up fully when Player 2
joins. It sits under the voice, comes up in the gaps and on the end card, and fades out at the end. Sound effects are
synthesised here (no samples, so no licences) from the events build/generate.py wrote to build/cues.json.
Writes assets/audio/mix.wav.
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
rng = np.random.default_rng(3)


def load(path, ch=2, af=None):
    cmd = ["ffmpeg", "-v", "error", "-i", path] + (["-af", af] if af else []) + ["-f", "f32le", "-ac", str(ch), "-ar", str(SR), "-"]
    pcm = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.float32).reshape(-1, ch).copy()


def env(n, a=.004, r=None):
    e = np.ones(n)
    na = max(1, int(a * SR))
    e[:na] = np.linspace(0, 1, na)
    nr = int((r or n / SR) * SR)
    e[-nr:] *= np.linspace(1, 0, nr) ** 2
    return e


def tone(f0, f1, d, kind="sine", a=.004):
    n = int(d * SR)
    f = np.geomspace(f0, f1, n)
    ph = np.cumsum(f) / SR
    if kind == "sine":
        x = np.sin(2 * np.pi * ph)
    elif kind == "tri":
        x = 2 * np.abs(2 * (ph % 1) - 1) - 1
    else:
        x = np.where(ph % 1 < .5, 1.0, -1.0)
    return x * env(n, a)


def noise(d, lp=1.0, a=.002):
    n = int(d * SR)
    x = rng.standard_normal(n)
    if lp < 1:
        y = np.zeros(n)
        for i in range(1, n):
            y[i] = y[i - 1] + lp * (x[i] - y[i - 1])
        x = y / (np.abs(y).max() + 1e-9)
    return x * env(n, a)


def mixp(*xs):
    out = np.zeros(max(len(x) for x in xs))
    for x in xs:
        out[:len(x)] += x
    return out


def seq(*parts, gap=0.0):
    out = []
    for p in parts:
        out.append(p)
        if gap:
            out.append(np.zeros(int(gap * SR)))
    return np.concatenate(out)


def bell(f, d=.5):
    return mixp(tone(f, f, d, "sine"), .4 * tone(f * 2.01, f * 2.01, d * .6, "sine"), .15 * tone(f * 3.02, f * 3.02, d * .3))


SFX = {
    "tick": lambda: .35 * mixp(tone(1900, 1500, .03, "tri"), .5 * noise(.012, .5)),
    "slam": lambda: mixp(.7 * np.tanh(2.2 * tone(120, 45, .26)), .25 * noise(.06, .4)),
    "whoosh": lambda: .35 * noise(.38, .08, a=.2),
    "swish": lambda: .3 * noise(.3, .12, a=.12),
    "land": lambda: mixp(.7 * np.tanh(2.5 * tone(150, 50, .22)), .2 * tone(600, 900, .08, "tri")),
    "chime": lambda: .22 * seq(bell(784, .18), bell(1047, .18), bell(1568, .5)),
    "blip": lambda: .2 * tone(880, 1320, .06, "tri"),
    "data": lambda: .1 * tone(1200 + 400 * rng.random(), 1600, .04, "sq"),
    "msg": lambda: .2 * seq(tone(1175, 1175, .06, "tri"), tone(1568, 1568, .1, "tri")),
    "item": lambda: .22 * seq(tone(659, 659, .07, "tri"), tone(880, 880, .07, "tri"), tone(1319, 1319, .2, "tri")),
    "err": lambda: .22 * tone(220, 200, .18, "sq"),
    "roar": lambda: mixp(.5 * np.tanh(3 * tone(70, 45, .9)), .25 * noise(.9, .05, a=.1)),
    "shot": lambda: .25 * tone(1800, 500, .16, "tri"),
    "hit": lambda: mixp(.5 * np.tanh(2 * tone(200, 70, .16)), .3 * noise(.08, .3)),
    "boom": lambda: mixp(.8 * np.tanh(3 * tone(90, 30, .9)), .4 * noise(.7, .06, a=.003)),
    "unlock": lambda: .24 * seq(bell(1047, .12), bell(1397, .35)),
    "stamp": lambda: mixp(.8 * np.tanh(3 * tone(100, 40, .25)), .3 * noise(.05, .5)),
    "burst": lambda: mixp(.3 * noise(.5, .25, a=.003), .25 * seq(bell(1047, .1), bell(1319, .1), bell(1568, .1), bell(2093, .5))),
    "press": lambda: mixp(.4 * tone(400, 200, .08, "tri"), .3 * noise(.03, .5)),
    "boing": lambda: .25 * tone(220, 660, .18, "tri"),
    "key": lambda: .12 * mixp(noise(.02, .6), tone(2400, 2000, .02, "tri")),
    "glitch": lambda: .3 * mixp(tone(80, 2000, .12, "sq"), noise(.12, .6)),
    "pix": lambda: .1 * np.concatenate([np.concatenate([tone(f, f * 1.3, .018, "sq"), np.zeros(int(.012 * SR))])
                                        for f in rng.uniform(1800, 4200, 7)]),
}


def main():
    cues = json.load(open(os.path.join(ROOT, "build", "cues.json")))
    words = json.load(open(os.path.join(ROOT, "build", "words.json")))
    dur = cues["dur"]
    burst = words[87]["s"]          # "console"
    music_in = 96.35 - burst
    N = int(dur * SR)
    voice = load(os.path.join(ROOT, "assets", "audio", "voice.wav"), 1)[:, 0]
    v = np.zeros(N)
    v[:min(N, len(voice))] = voice[:N]
    src = os.path.join(ROOT, "assets", "audio", "music-src.wav")
    full = load(src)
    muff = load(src, af="lowpass=f=420,lowpass=f=420")
    i0 = int(music_in * SR)
    m, mf = full[i0:i0 + N], muff[i0:i0 + N]
    m = np.pad(m, ((0, N - len(m)), (0, 0))); mf = np.pad(mf, ((0, N - len(mf)), (0, 0)))
    t = np.arange(N) / SR
    # muffled through the countdown, opens up as Player 2 joins
    open_t = words[11]["s"]
    x = np.clip((t - (open_t - .25)) / .5, 0, 1)[:, None]
    m = mf * 1.6 * (1 - x) + m * x
    speech = np.zeros(N)
    for wd in words:
        speech[int(max(0, wd["s"] - .08) * SR):int((wd["e"] + .12) * SR)] = 1
    k = int(.12 * SR)
    speech = np.convolve(speech, np.ones(k) / k, mode="same")
    gain_db = -11.5 * speech - 5.0 + np.where(t > words[-1]["e"] + .1, 4.0, 0.0)
    fade = np.clip((dur - t) / 1.0, 0, 1)
    m = m * (10 ** (gain_db / 20) * fade)[:, None]
    fx = np.zeros(N)
    for tt, kind in cues["ev"]:
        s = SFX[kind]()
        i = int(tt * SR)
        if i >= N:
            continue
        s = s[:N - i]
        fx[i:i + len(s)] += s
    mix = np.stack([v, v], 1) + m * .9 + np.stack([fx, fx], 1) * .6
    tmp = os.path.join(ROOT, "assets", "audio", "mix_raw.wav")
    sf.write(tmp, mix.astype(np.float32), SR, subtype="FLOAT")
    out = os.path.join(ROOT, "assets", "audio", "mix.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=8,alimiter=limit=0.89:level=false",
                    "-ar", str(SR), "-c:a", "pcm_s16le", out], check=True)
    os.remove(tmp)
    r = subprocess.run(["ffmpeg", "-i", out, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    lufs = [ln.strip() for ln in r.splitlines() if ln.strip().startswith("I:")][-1]
    print(f"wrote mix.wav {dur} s, music from {music_in:.2f} s, {len(cues['ev'])} sound events, {lufs}")


if __name__ == "__main__":
    main()
