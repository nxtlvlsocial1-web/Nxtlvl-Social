"""Score, sound design and the mastered mix for the Copycat reel (film noir).

python3 build/audio.py      (from the project root, after build/voice.py and build/generate.py; needs numpy, scipy,
soundfile, ffmpeg)

Music: instrumental Creative Commons tracks found through Openverse, all CC BY 3.0 from Jamendo, credited in the post
description (assets/music/CREDITS.json): "Gritty Noir" and "Unsolved Mystery" by Lilith Nyx, "Suspense and Tension
(stem 2)" by 3minutetunes and "Sfumato" by Zoop. Checked for vocals with faster-whisper: none. SFX: rain, storm, thunder,
footsteps, a door and a city street generated with ElevenLabs for the owner's earlier reels (assets/sfx/), and hits from
HyperFrames' bundled library (Pixabay Content License). Music ducks under dialogue. Writes assets/audio/mix.wav at about -14 LUFS.
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
M0, NT, A0, D0, TH, FR, OPEN = T["montage"], T["tools"], T["alert"], T["morning"], T["thu"], T["fri"], T["open"]
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
    gritty, mystery, tension, sax = M("gritty_noir.mp3"), M("unsolved_mystery.mp3"), M("suspense2.mp3"), M("sfumato.mp3")
    put(m, gritty, 0, 1.0, 0, M0 + .3, fin=.6, fout=.35)                               # midnight: slow noir piano
    put(m, mystery, M0 - .2, 1.0, 20.0, 20.0 + (A0 - M0) + .4, fin=.3, fout=.25)       # the case board
    put(m, tension, A0 - .4, 1.15, 0, D0 - A0 + .6, fin=.1, fout=.6)                   # 2 AM
    put(m, gritty, D0 - .2, .85, 60.0, 60.0 + (TH - D0) + .3, fin=.6, fout=.3)         # morning
    put(m, sax, TH - .3, 1.0, 62.0, 62.0 + (DUR - TH) + .3, fin=.25, fout=1.4)         # Thursday, Friday: the sax comes in
    return m


def sfx():
    s = np.zeros((N, 2))
    S = lambda n: load(os.path.join(ROOT, "assets", "sfx", n + ".mp3"))  # noqa: E731
    lib = lambda n: load(os.path.join(LIB, n + ".mp3"))  # noqa: E731
    rain, storm, thunder = S("rain_bed"), S("storm_bed"), S("thunder")
    put(s, loop(storm, OPEN + .3), 0, .9, fin=.3, fout=.3)                              # the street in the storm
    put(s, lp(loop(rain, D0 - OPEN), 1800), OPEN, .7, fin=.2, fout=.8)                  # inside: rain on the window
    put(s, lp(loop(rain, TH - D0), 1200), D0, .35, fin=.4, fout=.4)                     # morning drizzle
    put(s, loop(S("ny_street"), DUR - TH), TH, .55, fin=.3, fout=1.0)                   # Thursday, Friday on the street
    for b in T["bolts"]:
        put(s, thunder, b - .05, .8)
    put(s, S("footsteps"), OPEN + .5, .55)
    put(s, S("door"), OPEN + .05, .6)
    for n in NT:                                                                         # each card: a pin, the string, a whoosh
        put(s, lib("whoosh-short"), n - .35, .35)
        put(s, lib("impact-bass-1"), n, .45)
        put(s, lib("click"), n + .02, .5)
        put(s, lib("typing"), n + 1.45, .25, 0, 1.4)
    put(s, S("phone_buzz"), NT[3] + 1.5, .7)
    put(s, lib("riser"), A0 - 1.2, .35)
    put(s, lib("glitch-2"), A0 + .05, .45, 0, .6)
    for k in range(4):
        put(s, lib("error"), A0 + .15 + k * .5, .3)
    put(s, lib("notification"), L[4] - .4, .35)
    put(s, lib("chime"), TH + .3, .3)
    put(s, lib("whoosh-cinematic"), FR - .3, .35)
    put(s, lib("pop"), FR + .3, .3)
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
