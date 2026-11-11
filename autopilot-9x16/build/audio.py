"""Score, sound design and the mastered mix for the Autopilot reel.

python3 build/audio.py      (from the project root, after build/voice.py and build/generate.py; needs numpy, scipy,
soundfile, ffmpeg)

Music: three Creative Commons tracks found through Openverse, all CC BY 3.0 from Jamendo, credited in the post
description (assets/music/CREDITS.json): "Lofy" by macouno for the night, "Night Voyage (Chill Mix)" by Screw-Jay for the
4:12 AM surge, "Rising Morning" by Lfete for the dawn. SFX: hits from HyperFrames' bundled library (Pixabay Content
License) and ElevenLabs sound effects generated for the owner's earlier reels (assets/sfx/). Music ducks under dialogue.
Writes assets/audio/mix.wav at about -14 LUFS.
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
M0, NT, V0, D0 = T["montage"], T["neon"], T["viral"], T["dawn"]
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
    night, voyage, dawn = M("night_lofy.mp3"), M("night_voyage.mp3"), M("dawn_risingmorning.mp3")
    # 11 PM: the lo-fi starts muffled (inside her tired head) and opens up when Theo speaks
    intro = lp(night[: int((M0 + .5) * SR)], 900)
    put(m, intro, 0, .9, fin=.3, fout=.4)
    put(m, night, M0 - .4, 1.0, M0 - .4, V0 + .2, fin=.4, fout=.25)
    put(m, voyage, V0 - .1, 1.1, 40.0, 40.0 + (D0 - V0) + .3, fin=.15, fout=.5)       # the surge
    put(m, dawn, D0 - .2, 1.0, 0, DUR - D0 + .2, fin=.4, fout=1.2)
    return m


def sfx():
    s = np.zeros((N, 2))
    S = lambda n: load(os.path.join(ROOT, "assets", "sfx", n + ".mp3"))  # noqa: E731
    lib = lambda n: load(os.path.join(LIB, n + ".mp3"))  # noqa: E731
    room = S("room_tone")
    put(s, lp(loop(room, D0), 700), 0, .45, fin=.4, fout=.4)                          # the night: a low city hum
    put(s, loop(room, DUR - D0), D0, .7, fin=.6, fout=1.0)                            # dawn: birds, a car
    put(s, S("phone_buzz"), .25, .7)
    for k in range(4):
        put(s, lib("notification"), .3 + k * .55, .35)
    put(s, lib("whoosh-short"), M0 - .15, .4)
    # each sign: a stream of light, a neon buzz, a success ping
    for n in NT:
        put(s, lib("sparkle"), n - .8, .35)
        put(s, lib("glitch-2"), n, .35, 0, .5)
        put(s, S("voxel_form"), n + .1, .45)
        put(s, lib("whoosh"), n - 1.0, .25)
    # the clock racing during its close-up
    for k in range(int((NT[5] - NT[5]) + 18)):
        put(s, lib("click-soft"), NT[5] + 1.4 + k * .17, .22)
    # 4:12 AM
    put(s, lib("riser"), V0 - 1.6, .5)
    put(s, lib("impact-bass-2"), V0 + 1.0, .8)
    for k in range(14):
        put(s, lib("notification") if k % 2 else S("order_ping"), V0 + .4 + k * .21, .3)
    put(s, lib("whoosh-cinematic"), D0 - .4, .45)
    # dawn: Theo comes in with two coffees
    put(s, S("door_open"), L[3] - 1.75, .7)
    put(s, lib("chime"), L[3] - 1.65, .35)
    put(s, lib("ping"), L[3] + .2, .35)
    put(s, lib("sparkle"), T["endc"] + .3, .35)
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
