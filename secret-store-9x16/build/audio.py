"""Score, sound design and the mastered mix for the Secret Free Store reel.

python3 build/audio.py      (from the project root, after build/voice.py and build/generate.py; needs numpy, scipy,
soundfile, ffmpeg)

The arc follows the rarity: a sneaky cue in the mall (ElevenLabs Music, cueA_sneak), a choir hit when the vault opens,
light loot bells for the rare chests (synthesised here), a phonk bed from EPIC on (ElevenLabs Music, cueC_drop), the
lights going out to a low drone, a beat of silence, then the bass drop on the mythic chest (cueC_drop_b, which hits from
its first frame). SFX: ElevenLabs sound effects (assets/sfx/), a synthesised chest rattle, and hits from HyperFrames'
bundled library (Pixabay Content License). The music ducks under every word. Writes assets/audio/mix.wav at about -14 LUFS.
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
K, DUR = T["k"], T["end"]
PH, PE = T["ph"], T["pe"]
SR = 48000
N = int(DUR * SR)
LIB = os.path.join(os.path.dirname(ROOT), ".claude", "skills", "media-use", "audio", "assets", "sfx")
rng = np.random.default_rng(7)


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64).reshape(-1, 2)


def put(bus, x, t, g=1.0, a=0.0, b=None, fin=.01, fout=.05):
    x = x[int(a * SR):int(b * SR) if b else None].copy()
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    n = len(x)
    if n == 0:
        return
    fi, fo = min(n, int(fin * SR)), min(n, int(fout * SR))
    if fi: x[:fi] *= np.linspace(0, 1, fi)[:, None]
    if fo: x[-fo:] *= np.linspace(1, 0, fo)[:, None]
    i = int(round(t * SR))
    if i < 0:
        x, i = x[-i:], 0
    x = x[: max(0, N - i)]
    bus[i:i + len(x)] += x * g


def loop(x, dur):
    reps = int(np.ceil(dur * SR / len(x))) + 1
    return np.concatenate([x] * reps)[: int(dur * SR)]


def env(n, a=.002, d=.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)


def bell(f, dur=.6, d=.22):
    t = np.arange(int(dur * SR)) / SR
    x = np.sin(2 * np.pi * f * t) + .45 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 6) + .18 * np.sin(2 * np.pi * 4.07 * f * t) * np.exp(-t * 12)
    return x * env(len(t), .002, d)


def hat(n=.05):
    x = rng.standard_normal(int(n * SR)) * env(int(n * SR), .0005, .012)
    return sosfilt(butter(4, 7000, "high", fs=SR, output="sos"), x)


def kick():
    t = np.arange(int(.35 * SR)) / SR
    f = 45 + 110 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), .001, .11) * 1.6


def clap():
    x = rng.standard_normal(int(.18 * SR)) * env(int(.18 * SR), .001, .05)
    return sosfilt(butter(2, [900, 4000], "band", fs=SR, output="sos"), x) * 1.4


def riser(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n)
    out = np.zeros(n); seg = int(.05 * SR)
    for i in range(0, n, seg):         # a rising band of noise
        fc = 400 * (12 ** (i / n))
        out[i:i + seg] = sosfilt(butter(2, [fc * .7, min(fc * 1.4, 20000)], "band", fs=SR, output="sos"), x[i:i + seg])
    return out * (t / dur) ** 2


def loot_bells(t0, t1, k_on):
    """Light loot music for the rare chests: bell arpeggios at 140 bpm (C - Am - F - G), hats, a kick from k_on, a riser."""
    m = np.zeros((N, 2))
    step = 60 / 140 / 4
    chords = [[523.25, 659.25, 783.99, 1046.5], [440.0, 523.25, 659.25, 880.0], [349.23, 440.0, 523.25, 698.46], [392.0, 493.88, 587.33, 783.99]]
    pat = [0, 1, 2, 3, 2, 1, 2, 3]
    n, t = 0, t0
    while t < t1 - .02:
        ch = chords[(n // 16) % 4]
        b = bell(ch[pat[n % 8]] * (2 if n % 16 >= 12 else 1), .5, .16)
        pan = .5 + .25 * np.sin(n * .9)
        put(m, np.stack([b * (1 - pan), b * pan], 1), t, .55)
        if n % 2 == 0:
            put(m, hat(), t, .35 if n % 4 else .2)
        if t >= k_on and n % 4 == 0:
            put(m, kick(), t, .9)
        if t >= k_on and n % 8 == 4:
            put(m, clap(), t, .55)
        if n % 16 == 0:                      # a soft pad under each bar
            pad = sum(np.sin(2 * np.pi * f / 2 * np.arange(int(step * 16 * SR)) / SR) for f in ch) / 4
            pad *= np.minimum(1, np.arange(len(pad)) / (.2 * SR)) * np.linspace(1, .6, len(pad))
            put(m, pad, t, .22, fout=.15)
        n += 1; t += step
    put(m, riser(1.6), t1 - 1.6, .5, fout=.02)
    return m


def drone(t0, t1):
    n = int((t1 - t0) * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 41.2 * t) * .8 + np.sin(2 * np.pi * 82.4 * t + .3) * .25
    x += sosfilt(butter(2, 220, "low", fs=SR, output="sos"), rng.standard_normal(n)) * .6
    x *= np.minimum(1, t / .4) * (1 + .35 * np.sin(2 * np.pi * 1.1 * t))
    return x


def rattle(dur, rate=24):
    """A wooden chest rattling: clicks of filtered noise and small wood knocks."""
    n = int(dur * SR); out = np.zeros(n)
    t = 0.0; k = 0
    while t < dur:
        i = int(t * SR); m = int(.03 * SR)
        c = rng.standard_normal(m) * env(m, .0003, .006) * (.5 + rng.random())
        c = sosfilt(butter(2, [1200, 5200], "band", fs=SR, output="sos"), c)
        if k % 3 == 0:
            tt = np.arange(m) / SR; c += np.sin(2 * np.pi * (170 + 40 * rng.random()) * tt) * env(m, .0005, .012) * .8
        out[i:i + m] += c[: max(0, min(m, n - i))]
        t += 1 / rate * (.7 + .6 * rng.random()); k += 1
    return out * np.minimum(1, np.arange(n) / (.08 * SR)) * 1.2


def music():
    m = np.zeros((N, 2))
    M = lambda f: load(os.path.join(ROOT, "assets", "music", f))  # noqa: E731
    A, C, D = M("cueA_sneak.mp3"), M("cueC_drop.mp3"), M("cueC_drop_b.mp3")
    put(m, A, 0, 1.0, 0, K["door"] + .25, fin=.005, fout=.5)
    m += loot_bells(K["cE"], K["shakeE"] - .02, K["cG"])
    put(m, C, K["shakeE"] - .03, 1.0, 0, K["cJ1"] - K["shakeE"] + .35, fin=.01, fout=.35)
    put(m, drone(K["cJ1"], K["myth"] - .3), K["cJ1"], .55, fin=.3, fout=.12)
    put(m, D, K["myth"], 1.15, 0, DUR - K["myth"], fin=.003, fout=.6)
    return m


def sfx():
    s = np.zeros((N, 2))
    S = lambda n: load(os.path.join(ROOT, "assets", "sfx", n + ".mp3"))  # noqa: E731
    lib = lambda n: load(os.path.join(LIB, n + ".mp3"))  # noqa: E731
    # the mall: tiptoes
    put(s, loop(S("footsteps"), K["cC"] + 1.6), 0.05, .7, fin=.05, fout=.3)
    put(s, lib("pop"), .12, .35)                                   # psst
    # cuts
    for t in [K["cB"], K["cC"], K["cE"], K["cF"], K["cG"], K["cH1"], K["cH2"], K["cI1"], K["cI2"], K["cJ1"], K["cM"], K["cN"], K["cO"]]:
        put(s, lib("whoosh-short"), t - .1, .28)
    # the door and the vault
    put(s, S("door"), K["door"] - .15, 1.0)
    put(s, S("choir"), K["cE"] - .06, 1.0, fout=.2)
    put(s, S("choir_b"), K["cE"] + .02, .6, fout=.2)
    put(s, lib("sparkle"), K["cE"] + .05, .6)
    # the chests: rattles grow, then the pop and the reveal
    for a, b, g in [(K["shakeR1"], K["openR1"], .45), (K["shakeR2"], K["openR2"], .5), (K["shakeE"], K["openE1"], .6), (K["cH2"], K["openE2"], .6), (K["shakeG"], K["openG"], .75)]:
        put(s, rattle(b - a), a, g, fout=.02)
        put(s, S("chest_open"), b - .04, .95)
    put(s, lib("chime"), K["openE1"] + .1, .35); put(s, lib("chime"), K["openE2"] + .1, .35)
    put(s, S("legendary"), K["openG"] - .03, 1.0); put(s, S("legendary_b"), K["openG"] + .25, .6)
    put(s, S("coins"), K["openG"] + .3, .8)
    put(s, lib("impact-bass-2"), K["openG"] - .02, .5)
    # the mythic: the riser into silence, then the blast
    put(s, rattle(K["myth"] - .45 - K["lev"], 30), K["lev"], .5, fout=.05)
    put(s, lib("riser"), K["myth"] - 2.2, .45, b=1.85, fout=.02)
    put(s, S("mythic"), K["myth"] - .01, 1.2); put(s, S("mythic_b"), K["myth"] + .05, .9)
    put(s, lib("impact-bass-1"), K["myth"] - .01, 1.0)
    put(s, S("coins"), K["myth"] + .45, .7)
    # FREE stamps and the HUD
    for t in [PH[2][3], PH[3][2], PH[5][4], PH[7][3]]:
        put(s, lib("impact-bass-2"), t - .03, .35); put(s, lib("pop"), t - .02, .4)
    for t in [K["openR1"], K["openR2"], K["openE1"], K["openE2"], K["openG"], K["myth"]]:
        put(s, lib("click-soft"), t + .12, .3)
    # the secret chests: chains, then the end card
    put(s, S("chains"), K["rattle"] - .05, .9); put(s, S("chains"), K["rattle"] + .35, .6)
    put(s, lib("glitch-1"), K["cM"] + .1, .15)
    put(s, lib("sparkle"), K["wink"], .4)
    put(s, S("coins"), K["endc"] + .2, .75)
    put(s, lib("chime"), K["endc"] + .3, .45)
    return s


def ffmpeg(*a):
    return subprocess.run(["ffmpeg", "-y", "-hide_banner", *a], capture_output=True, text=True, check=True)


def main():
    voice, vsr = sf.read(os.path.join(ROOT, "assets", "audio", "voice.wav"))
    assert vsr == SR
    v = np.zeros(N); v[: min(N, len(voice))] = voice[:N]
    rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)  # noqa: E731
    tt = np.arange(N) / SR
    talk = np.zeros(N)
    for ph, pe in zip(PH, PE):
        for a, b in zip(ph, pe):
            talk = np.maximum(talk, np.clip((tt - (a - .15)) / .15, 0, 1) * np.clip(((b + .2) - tt) / .2, 0, 1))
    m, s = music(), sfx()
    sf.write(os.path.join(ROOT, "assets", "audio", "score.wav"), m.astype(np.float32), SR, subtype="PCM_24")
    m = m * (.12 / rms(m)) * (1 - .5 * talk)[:, None]
    s = s * (.1 / rms(s)) * (1 - .25 * talk)[:, None]
    mix = m + s + (v * (.2 / rms(v[v != 0])))[:, None]
    fade = np.ones(N); fade[-int(.35 * SR):] = np.linspace(1, 0, int(.35 * SR))
    mix *= fade[:, None]
    mix *= min(1, .98 / np.max(np.abs(mix)))
    raw = os.path.join(ROOT, "assets", "audio", "mix_raw.wav")
    sf.write(raw, mix.astype(np.float32), SR, subtype="FLOAT")
    o = ffmpeg("-i", raw, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-").stderr
    meas = json.loads(o[o.rindex("{"):o.rindex("}") + 1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
          f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:linear=true")
    out = os.path.join(ROOT, "assets", "audio", "mix.wav")
    ffmpeg("-i", raw, "-af", af + ",alimiter=limit=0.84:level=false:attack=1:release=60", "-ar", str(SR), "-c:a", "pcm_s24le", out)
    os.remove(raw)
    chk = ffmpeg("-i", out, "-af", "ebur128=peak=true", "-f", "null", "-").stderr
    summ = chk[chk.rindex("Summary:"):]
    print("wrote", out, " ".join(ln.strip() for ln in summ.splitlines() if ln.strip().startswith(("I:", "Peak:"))))


if __name__ == "__main__":
    main()
