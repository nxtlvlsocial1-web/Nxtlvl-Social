"""Score, sound design and the mastered mix for the real estate what-if.

python3 build/audio.py      (from the project root, after build/voice.py and build/generate.py; needs numpy, scipy,
soundfile, ffmpeg)

Music: two instrumental Creative Commons tracks found through Openverse, CC BY 3.0 from Jamendo, credited in the post
description (assets/music/CREDITS.json): "808" by Shipititez tha Viruz (the empty office and the fix) and "Funk in my
Pocket" by OptiKill (from the blue check). Checked for vocals with faster-whisper: none. SFX: a city street, footsteps and a
door generated with ElevenLabs for the owner's earlier reels (assets/sfx/), and HyperFrames' bundled library (Pixabay
Content License). Music ducks under dialogue. Writes assets/audio/mix.wav at about -14 LUFS.
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
L, E = T["l"], T["e"]
IN0, CK, FL, NX, STEPS = T["inside"], T["check"], T["flip"], T["next"], T["steps"]
SR = 48000
DUR = T["end"]
N = int(DUR * SR)
LIB = os.path.join(os.path.dirname(ROOT), ".claude", "skills", "media-use", "audio", "assets", "sfx")


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64).reshape(-1, 2)


def put(bus, x, t, g=1.0, a=0.0, b=None, fin=.02, fout=.05):
    x = x[int(a * SR):int(b * SR) if b else None].copy()
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


def lp(x, f):
    return np.stack([sosfilt(butter(2, f, "low", fs=SR, output="sos"), x[:, c]) for c in (0, 1)], 1)


def loop(x, dur):
    reps = int(np.ceil(dur * SR / len(x))) + 1
    return np.concatenate([x] * reps)[: int(dur * SR)]


def music():
    m = np.zeros((N, 2))
    M = lambda f: load(os.path.join(ROOT, "assets", "music", f))  # noqa: E731
    lofi, funk = M("hiphop_808.mp3"), M("funk_in_my_pocket.mp3")
    put(m, lofi, 0, 1.0, 10.0, 10.0 + CK + .3, fin=.03, fout=.3)                       # the empty morning, the fix
    put(m, funk, CK + .55, 1.05, 15.0, 15.0 + (DUR - CK) + .3, fin=.05, fout=1.2)      # the blue check: the funk kicks in
    return m


def sfx():
    s = np.zeros((N, 2))
    S = lambda n: load(os.path.join(ROOT, "assets", "sfx", n + ".mp3"))  # noqa: E731
    lib = lambda n: load(os.path.join(LIB, n + ".mp3"))  # noqa: E731
    st = S("ny_street")
    put(s, loop(st, IN0), 0, .55, fin=.05, fout=.3)                                    # the street
    put(s, lp(loop(st, CK - IN0), 900), IN0, .3, fin=.2, fout=.2)                      # muffled from inside
    put(s, loop(st, DUR - CK), CK, .5, fin=.2, fout=1.0)
    for j in range(6):
        put(s, lib("notification"), .2 + j * .6, .22)                                  # phones everywhere
    put(s, lib("whoosh-short"), IN0 - .1, .35)
    for k, t0 in enumerate(STEPS):                                                      # each hologram step
        put(s, lib("sparkle") if k == 3 else lib("pop"), t0, .35)
        put(s, lib("key-press"), t0 + .15, .25)
    put(s, lib("riser"), CK - .9, .35)
    put(s, lib("impact-bass-2"), CK + .45, .6)                                          # the blue check slams on
    put(s, lib("sparkle"), CK + .55, .45)
    for j in range(12):
        put(s, lib("ping"), FL + .25 + j * .07, .14)                                    # the cards flip, one after another
    put(s, S("footsteps"), FL + .6, .45); put(s, S("footsteps"), FL + 2.0, .4)
    put(s, S("door"), NX - .3, .5)
    put(s, lib("chime"), NX + .1, .3)
    put(s, lib("sparkle"), T["endc"] + .3, .3)
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
    for a, b in zip(L, E):
        talk = np.maximum(talk, np.clip((tt - (a - .25)) / .25, 0, 1) * np.clip(((b + .3) - tt) / .3, 0, 1))
    m, s = music(), sfx()
    m = m * (.12 / rms(m)) * (1 - .6 * talk)[:, None]
    s = s * (.08 / rms(s)) * (1 - .35 * talk)[:, None]
    mix = m + s + (v * (.17 / rms(v[v != 0])))[:, None]
    fade = np.ones(N); fade[-int(.4 * SR):] = np.linspace(1, 0, int(.4 * SR))
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
