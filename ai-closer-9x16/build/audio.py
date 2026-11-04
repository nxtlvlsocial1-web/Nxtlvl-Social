"""Music, sound design and the mastered mix for the AI Closer reel.

python3 build/audio.py      (from the project root, after build/generate.py; needs numpy, scipy, soundfile, ffmpeg)

Music: the original score in build/score.py (composed in code, no licence needed). SFX: recorded hits from
HyperFrames' bundled library (Pixabay Content License: commercial use, no credit needed;
.claude/skills/media-use/audio/assets/sfx/CREDITS.md) plus synthesized blips, coins, a phone buzz, a cash register
and the robot's hover hum. The music and SFX duck under the voice on a speech gate. Writes
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


def lp(x, f, o=2):
    return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)


def noise_bed(d, lo, hi, g=1.0, fade=.4):
    n = int(d * SR)
    t = np.arange(n) / SR
    return bp(rng.standard_normal(n), lo, hi) * np.minimum(1, t / fade) * np.minimum(1, (d - t) / fade) * g


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


def zap(d=.5, f0=300, f1=2400):
    """The clone printing in: a rising sweep with a fizz."""
    n = int(d * SR); t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / d)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * .5 + bp(rng.standard_normal(n), 2000, 9000) * .3) * np.minimum(1, t / .02) * np.minimum(1, (d - t) / .08) * .5


def blip(f=1200, d=.06):
    t = np.arange(int(d * SR)) / SR
    return np.sign(np.sin(2 * np.pi * f * t)) * .2 * np.exp(-t * 30)


def buzz(d=.6):
    """A phone vibrating on a desk."""
    n = int(d * SR); t = np.arange(n) / SR
    x = np.sign(np.sin(2 * np.pi * 150 * t)) * (np.sin(2 * np.pi * 9 * t) > -.2)
    return bp(x, 100, 1200) * .35 * np.minimum(1, (d - t) / .05)


def till(seed=0):
    """A cash-register ding: a bright bell with a little drawer rattle."""
    n = int(.6 * SR); t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * 2093 * t) + .5 * np.sin(2 * np.pi * 3136 * t)) * np.exp(-t * 7)
    x[: int(.08 * SR)] += bp(rng.standard_normal(int(.08 * SR)), 1500, 6000) * .3
    return x * .3


def hum(d, f=110, g=.2):
    t = np.arange(int(d * SR)) / SR
    return (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * f * 2.01 * t)) * g * np.minimum(1, t / .3) * np.minimum(1, (d - t) / .3)


def sfx():
    cu = T["cuts"]
    for t in cu:
        put(smp("whoosh-short"), t - .1, .45)
    # 3 AM: the night, the phone buzzing, a ding per sale
    put(noise_bed(cu[0], 200, 900, .12, .6), 0, .35)
    put(buzz(.7), T["buzzing"] - .2, .55, .2); put(buzz(.6), T["buzzing"] + .7, .45, .2)
    for k in range(7):
        put(till(k), T["buzzing"] - .2 + k * .27, .5, (k % 2 - .5) * .5)
    put(jingle(.8, 12, 1), T["seven"], .5)
    put(hum(cu[0] - 1, 110, .12), .5, .3, .3)
    # day 1: the comment, the flight, the DM lands
    put(smp("pop"), T["price"] - .05, .35, .3)
    put(smp("whoosh"), T["scroll"] - .6, .45, -.2)
    put(zap(.6, 400, 1600), T["scroll"] + .5, .35)
    put(smp("notification"), T["already"] + .2, .45, .3)
    put(smp("sparkle"), T["dms"] - .1, .3)
    # day 4: the message, the story, the sale
    put(smp("notification"), T["expensive"] - .5, .3)
    put(zap(.8, 200, 900), T["story"] - .3, .3)
    put(till(9), T["buys"], .6); put(jingle(1.0, 16, 4), T["buys"] + .05, .5)
    # day 10: the scan, a day passing, the follow-ups, two come back
    for j in range(10):
        put(blip(1000 + (j % 4) * 200, .05), T["clicked"] + j * .12, .3, ((j % 3) - 1) * .5)
    put(smp("whoosh-cinematic"), T["later"] - .4, .35)
    for j in range(8):
        put(smp("pop"), T["follows"] - .1 + j * .12, .22, ((j % 3) - 1) * .5)
    put(till(3), T["half"], .5, -.3); put(till(5), T["half"] + .05, .5, .3)
    # day 18: midnight street, the payment screen, the no
    put(noise_bed(cu[4] - cu[3], 150, 700, .12, .6), cu[3], .35)
    put(smp("click-soft", 0, .1), T["pay"] - .2, .4)
    put(smp("glitch-2", 0, .3), T["no"] - .05, .25)
    put(smp("impact-bass-2"), T["no"], .5)
    # day 30: the billboard rolls, the cheer, the return
    for j in range(12):
        put(smp("key-press", 0, .08), T["two"] - .2 + j * .08, .25)
    put(smp("chime"), T["two"] + .3, .45)
    put(smp("sparkle"), T["she"] - .1, .4)
    # real world, the close
    put(smp("whoosh-cinematic"), cu[5] - .2, .4)
    for j in range(16):
        put(blip(1100 + (j % 4) * 220, .05), T["business"] + j * .2, .3, ((j % 3) - 1) * .6)
    put(smp("sparkle"), T["week"] - .1, .4)
    put(smp("pop"), T["setup"] - .2, .35)
    put(smp("ping"), T["follow"], .45)
    put(smp("pop"), T["commentk"], .4)
    put(till(11), T["closek"] + .1, .45)


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
    # the world goes muffled after the AI says no; the voice stays clear
    tt = np.arange(N) / SR
    mw = (.85 * np.clip((tt - T["no"] - .2) / .2, 0, 1) * np.clip((T["cuts"][4] - tt) / .3, 0, 1))[:, None]
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
