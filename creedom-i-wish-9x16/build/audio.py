"""Music, Cree's gibberish voice, sound design and the mastered mix for the Creedom "I Wish..." reel.

Music (CC BY 3.0, Jamendo, found through Openverse; both instrumental, checked with faster-whisper): "Sad Piano" by
Alexander Blu under the creator's breakdown, then "Trip Around The World" by ANtarcticbreeze from Cree's hero entrance.
Cree never says real words: his voice is synthesised here (little pitched syllables with vowel formants, deterministic),
timed to build/chirps.json, while the speech clouds on screen say what he means. SFX: HyperFrames' bundled library
(Pixabay Content License) and an ElevenLabs room tone from the owner's earlier reels. Music ducks under the voice.
python3 build/audio.py      (from the project root, after build/voice.py and build/generate.py)
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(os.path.dirname(ROOT), ".claude", "skills", "media-use", "audio", "assets", "sfx")
SR = 48000
CU = json.load(open(os.path.join(ROOT, "build", "cues.json")))
CH = json.load(open(os.path.join(ROOT, "build", "chirps.json")))["chirps"]
DUR = CU["end"]
N = int(DUR * SR)
Ls = lambda k: CU["lines"][k][0]  # noqa: E731
Le = lambda k: CU["lines"][k][1]  # noqa: E731
Bs = lambda k: CU["beats"][k][0]  # noqa: E731
Be = lambda k: CU["beats"][k][1]  # noqa: E731


def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)


def put(bus, x, t, g=1.0, a=0.0, b=None, fin=.02, fout=.05):
    x = x[int(a * SR):int(b * SR) if b else None].copy()
    if len(x) == 0:
        return
    fi, fo = min(len(x), int(fin * SR)), min(len(x), int(fout * SR))
    if fi: x[:fi] *= np.linspace(0, 1, fi)[:, None]
    if fo: x[-fo:] *= np.linspace(1, 0, fo)[:, None]
    i = int(round(t * SR))
    if i < 0:
        x, i = x[-i:], 0
    x = x[: max(0, N - i)]
    bus[i:i + len(x)] += x * g


def lp(x, f, kind="low"):
    return np.stack([sosfilt(butter(2, f, kind, fs=SR, output="sos"), x[:, c]) for c in (0, 1)], 1)


def gibberish(dur, seed, base=640.0, happy=False):
    """Cree's voice: a run of tiny pitched syllables (a soft consonant tick, then a vowel), with a bouncy contour."""
    rng = np.random.default_rng(seed)
    out, t = [], 0.0
    VOW = [(800, 1200), (400, 2200), (300, 2600), (500, 900), (350, 800)]   # a e i o u formants
    while t < dur - .06:
        L = rng.uniform(.065, .12)
        n = int(L * SR); tt = np.arange(n) / SR
        f0 = base * (1 + rng.uniform(-.18, .22)) * (1.08 if happy else 1)
        glide = rng.uniform(-.25, .35)
        f = f0 * (1 + glide * tt / L)
        ph = 2 * np.pi * np.cumsum(f) / SR
        F1, F2 = VOW[rng.integers(0, 5)]
        s = np.zeros(n)
        for h in range(1, 14):
            fh = f0 * h
            w = np.exp(-((fh - F1) / 260) ** 2) + .7 * np.exp(-((fh - F2) / 420) ** 2) + .15 / h
            s += w * np.sin(h * ph)
        env = np.minimum(1, tt / .008) * np.exp(-tt / (L * .55)) * (1 - np.exp(-(L - tt) / .01))
        tick = rng.standard_normal(n) * np.exp(-tt / .004) * .25
        out.append((s / 6 + tick) * env)
        gap = rng.uniform(.012, .04)
        out.append(np.zeros(int(gap * SR)))
        t += L + gap
    y = np.concatenate(out)[: int(dur * SR)]
    y = sosfilt(butter(2, 220, "high", fs=SR, output="sos"), y)
    y = np.tanh(y * 1.6) / 1.6
    return np.stack([y, y], 1)


def buzz(dur):
    tt = np.arange(int(dur * SR)) / SR
    on = ((tt % .5) < .32).astype(float)
    y = np.sin(2 * np.pi * 150 * tt) * (.6 + .4 * np.sign(np.sin(2 * np.pi * 37 * tt))) * on
    y = sosfilt(butter(2, [90, 900], "band", fs=SR, output="sos"), y) * .5
    return np.stack([y, y], 1)


def music():
    m = np.zeros((N, 2))
    hero = Bs("hero")
    put(m, load(os.path.join(ROOT, "assets", "music", "sad_piano.mp3")), 0, 1.0, 1.5, 1.5 + hero + .2, fin=.4, fout=.35)
    up = load(os.path.join(ROOT, "assets", "music", "trip_world.mp3"))
    put(m, up * .55, hero + .05, 1.0, 0, DUR - hero + .2, fin=.05, fout=1.4)
    return m


def cree():
    c = np.zeros((N, 2))
    for k, (a, b) in enumerate(CH):
        happy = k in (1, 5, 6)
        put(c, gibberish(b - a, 11 + k * 7, base=700 if happy else 620, happy=happy), a, 1.0, fin=.01, fout=.04)
    return c


def sfx():
    s = np.zeros((N, 2))
    S = lambda n: load(os.path.join(ROOT, "assets", "sfx", n + ".mp3"))  # noqa: E731
    lib = lambda n: load(os.path.join(LIB, n + ".mp3"))  # noqa: E731
    reps = int(np.ceil(DUR * SR / len(S("room_tone")))) + 1
    put(s, lp(np.concatenate([S("room_tone")] * reps)[:N], 1400), 0, .3, fin=.05, fout=.8)
    put(s, lib("pop"), .45, .3)                                                        # 42 views
    put(s, lib("whoosh-short"), Le("01") + .1, .25)                                    # he slides off the chair
    put(s, lib("impact-bass-2"), Bs("thud") + .2, .35)                                 # face-down on the desk
    put(s, lib("click-soft"), Bs("thud") + 1.65, .3)                                    # the pen hits the floor
    for k in ("04", "05", "06"):
        put(s, lib("chime"), Ls(k) - .05, .12)                                         # the wish chips
    put(s, lp(lib("riser"), 1800), Bs("reveal1") - .8, .18)                            # reveal 1
    put(s, lib("whoosh-cinematic"), Bs("reveal1") + .1, .2)
    put(s, lib("impact-bass-2"), Bs("reveal2") + .35, .25)                             # reveal 2: feet land
    put(s, lib("sparkle"), Bs("reveal2") + .95, .3)                                    # the magnifier glints
    put(s, buzz(Le("06") - Ls("06") + .2), Ls("06") - .1, .12)                         # the phone buzzing on the bed
    put(s, lib("riser"), Bs("hero") - 1.6, .3)                                         # the hero entrance
    put(s, lib("impact-bass-1"), Bs("hero"), .5); put(s, lib("whoosh-cinematic"), Bs("hero") - .1, .35); put(s, lib("sparkle"), Bs("hero") + .3, .35)
    put(s, lib("pop"), Bs("fix1") + 1.75, .3); put(s, lib("ping"), Bs("fix1") + 1.85, .3)                  # tap, the tag
    put(s, lib("whoosh-short"), Bs("fix2") + .1, .25); put(s, lib("chime"), Bs("fix2") + 1.5, .3)          # the cards, gold
    put(s, lib("click"), Bs("fix3") + .8, .45); put(s, lib("ping"), Bs("fix3") + .9, .25)                  # the lever, the switch
    for i in range(6):
        put(s, lib("whoosh-short"), Bs("fix3") + 1.0 + i * .28, .12)                                       # paper planes
    put(s, lib("notification"), Bs("fix3") + 1.4, .2)
    put(s, lib("sparkle"), Ls("10") + .1, .2)                                                              # the hug
    put(s, lib("pop"), Bs("endin") + .15, .3); put(s, lib("typing"), Bs("endin") + .85, .25, 0, .9); put(s, lib("click"), Bs("endin") + 1.95, .35)
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
    for a, b in list(CU["lines"].values()) + CH:
        talk = np.maximum(talk, np.clip((tt - (a - .2)) / .2, 0, 1) * np.clip(((b + .3) - tt) / .3, 0, 1))
    m, c, s = music(), cree(), sfx()
    m = m * (.13 / rms(m)) * (1 - .6 * talk)[:, None]
    s = s * (.07 / rms(s))
    c = c * (.16 / rms(c[np.abs(c[:, 0]) > 1e-4]))
    mix = m + s + c + (v * (.17 / rms(v[v != 0])))[:, None]
    fade = np.ones(N); fade[-int(.5 * SR):] = np.linspace(1, 0, int(.5 * SR))
    mix *= fade[:, None]
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
