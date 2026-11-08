"""Music, sound design and the mastered mix for the AI Future reel ("what if your phone could see tomorrow").

python3 build/audio.py      (from the project root, after build/generate.py; needs numpy, scipy, soundfile, ffmpeg)

Music: the original score in build/score.py (composed in code, no licence needed). SFX: hits from HyperFrames' bundled
library (Pixabay Content License: commercial use, no credit needed; .claude/skills/media-use/audio/assets/sfx/CREDITS.md)
plus synthesized city traffic, a coffee splash, a roulette ball, coins, a crowd cheer, rain, thunder, car horns, a
bridge giving way, a phone buzz and three knocks. The music and SFX duck under the voice on a speech gate. Writes
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


def env_(n, a, r):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-3)) * np.exp(-t * r)


def splash(big=1.0):
    """Liquid hitting the ground: a wet noise burst and a soft thud."""
    n = int(.7 * SR); t = np.arange(n) / SR
    wet = bp(rng.standard_normal(n), 600, 6000) * np.exp(-t * 9) * (1 + .5 * np.sin(2 * np.pi * 35 * t))
    thud = np.sin(2 * np.pi * (90 + 60 * np.exp(-t * 30)) * t) * np.exp(-t * 18) * .6
    return (wet * .5 + thud) * .5 * big


def roll(d):
    """A roulette ball running round the track: a rattling band of noise."""
    n = int(d * SR); t = np.arange(n) / SR
    x = bp(rng.standard_normal(n), 1800, 7000) * (.6 + .4 * np.sin(2 * np.pi * 11 * t) ** 2)
    return x * .22 * np.minimum(1, t / .2) * np.minimum(1, (d - t) / .05)


def tickb(f=3800):
    n = int(.04 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) * np.exp(-t * 160) + bp(rng.standard_normal(n), 2000, 8000) * np.exp(-t * 220) * .5) * .4


def crowd(d, g=1.0, cheer=False):
    n = int(d * SR); t = np.arange(n) / SR
    x = sum(bp(rng.standard_normal(n), f0, f0 * 1.6) * (.6 + .4 * np.sin(2 * np.pi * (1.3 + k * .7) * t + k)) for k, f0 in enumerate((300, 520, 900, 1500)))
    e = np.minimum(1, t / (.15 if cheer else .5)) * np.minimum(1, (d - t) / .5)
    return x * e * .25 * g


def horn(d=.6, f=420):
    n = int(d * SR); t = np.arange(n) / SR
    x = np.sign(np.sin(2 * np.pi * f * t)) + np.sign(np.sin(2 * np.pi * f * 1.26 * t))
    return bp(x, 250, 2500) * .18 * np.minimum(1, t / .02) * np.minimum(1, (d - t) / .04)


def thunder(d=3.0):
    n = int(d * SR); t = np.arange(n) / SR
    crack = bp(rng.standard_normal(n), 800, 6000) * np.exp(-t * 14) * .6
    rumble = lp(rng.standard_normal(n), 160, 4) * np.exp(-t * 1.1) * (1 + .6 * np.sin(2 * np.pi * 2.3 * t)) * 3.0
    return (crack + rumble) * np.minimum(1, t / .01) * .5


def creak(d=.8):
    n = int(d * SR); t = np.arange(n) / SR
    f = 70 + 40 * np.sin(2 * np.pi * 1.7 * t)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (rng.random(n) > .6)
    return bp(x, 200, 1600) * .25 * np.minimum(1, t / .1) * np.minimum(1, (d - t) / .1)


def knock():
    n = int(.25 * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * (110 + 80 * np.exp(-t * 60)) * t) * np.exp(-t * 28)
    wood = bp(rng.standard_normal(n), 500, 2500) * np.exp(-t * 70) * .6
    return (body + wood) * .7


def sfx():
    cu = T["cuts"]
    for t in cu:
        put(smp("whoosh-short"), t - .1, .4)
    # New York: traffic, a horn, the phone, the LED sign flips, the coffee hits the pavement
    put(noise_bed(cu[0], 80, 700, .5, .8), 0, .5)
    put(noise_bed(cu[0], 700, 2500, .12, .8), 0, .4, .3)
    for k, tt in enumerate((1.4, 5.6, 9.2)):
        put(noise_bed(1.6, 120, 900, .5, .6), tt, .4, (k % 2 - .5) * 1.2)
    put(horn(.35, 470), 3.1, .25, -.6)
    put(smp("click-soft", 0, .12), T["tomorrow1"] - .7, .4)
    put(smp("notification"), T["tomorrow1"] - .05, .35, .2)
    put(smp("key-press", 0, .08), T["at3"] + .3, .45, .3)
    put(splash(), T["does"] + .08, .9, .25)
    # Las Vegas: the floor, the ball, the drop, the win
    put(crowd(cu[1] - cu[0], .5), cu[0], .5)
    for k in range(10):
        put(blip(900 + (k % 5) * 180, .07), cu[0] + .3 + k * .55, .12, (k % 3 - 1) * .7)
    put(smp("notification"), T["vegas"] + .1, .3, .2)
    for j in range(5):
        put(tickb(2200 + j * 100), T["number"] + .5 + j * .07, .5)
    tl = T["seventeen"]
    put(roll(tl - .5 - cu[0]), cu[0], .7)
    for j in range(6):
        put(tickb(3200 + (j % 3) * 400), tl - .5 + j * .09 * (1 + j * .15), .7 - j * .06, (j % 2 - .5) * .3)
    put(smp("impact-bass-1"), tl, .5)
    put(crowd(2.6, 1.0, True), tl + .15, .9)
    put(jingle(1.2, 18, 3), tl + .4, .6)
    put(jingle(1.0, 14, 5), tl + .9, .5)
    put(smp("whoosh"), max(T["walk"] - .1, tl + 1.1), .3)
    # Miami: rain, wind, thunder after each flash, horns and shouting, the bridge goes
    put(noise_bed(cu[2] - cu[1], 1500, 9000, .55, .5), cu[1], .55)
    put(noise_bed(cu[2] - cu[1], 120, 600, .35, .5), cu[1], .45, -.2)
    for a in (T["miami"] - .05, T["bridge7"] + .15, T["yells"] + .2, T["down"] + .05):
        put(thunder(3.0), a + .25, .7, .2)
    put(horn(.5, 430), T["block"] + .1, .35, -.3); put(horn(.8, 380), T["block"] + .5, .3, .4)
    put(horn(.4, 470), T["yells"] - .1, .35, .2); put(horn(.6, 400), T["yells"] + .5, .3, -.4)
    put(crowd(T["noon9"] - T["yells"] + .2, .9, True), T["yells"] - .2, .8)
    put(creak(.9), T["down"] - .9, .5)
    put(smp("impact-bass-2"), T["down"] - .4, .6)
    put(thunder(3.0), T["down"] + .3, .7)
    put(splash(3.0), T["down"] + .32, .8); put(noise_bed(2.2, 300, 4000, .6, .3), T["down"] + .32, .6)
    # home, day 21: room tone, the buzz, the message, three knocks
    put(noise_bed(cu[3] - cu[2], 60, 300, .2, .5), cu[2], .4)
    put(buzz(.6), cu[2] + .3, .5, .2); put(buzz(.5), cu[2] + 1.1, .4, .2)
    put(smp("ping"), T["open"] - .2, .35)
    for a in (0, .28, .56):
        put(knock(), T["knocks"] + a, 1.0, -.1)
    # home, day 30: a loading tick; the screen dies
    put(noise_bed(cu[4] - cu[3], 60, 300, .2, .5), cu[3], .4)
    for k in range(int((T["black"] - T["check"]) / .25)):
        put(blip(1400, .03), T["check"] + k * .25, .12)
    put(zap(.5, 1200, 120), T["black"] - .05, .35)
    # the real part, the end
    put(noise_bed(cu[5] - cu[4], 200, 1200, .15, .6), cu[4], .35)
    put(smp("whoosh-cinematic"), cu[4] - .2, .4)
    put(smp("sparkle"), T["deepmind"] - .1, .35)
    for k in range(10):
        put(blip(1100 + (k % 5) * 200, .05), T["ten"] - 1.1 + k * .13, .25, ((k % 5) - 2) * .3)
    put(smp("riser"), cu[5] - 1.6, .25)
    put(smp("ping"), T["follow"], .4)


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
    # the world goes muffled when the screen goes black; the voice stays clear
    tt = np.arange(N) / SR
    mw = (.85 * np.clip((tt - T["black"]) / .2, 0, 1) * np.clip((T["cuts"][4] - tt) / .3, 0, 1))[:, None]
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
