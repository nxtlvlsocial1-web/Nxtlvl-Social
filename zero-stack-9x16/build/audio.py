"""Score, sound design and the mastered mix for the Zero Stack reel.

python3 build/audio.py      (from the project root, after build/voice.py and build/generate.py; needs numpy, scipy,
soundfile, ffmpeg)

Music: four instrumental cues composed for this reel with ElevenLabs Music (assets/music/, generated on the owner's
ElevenLabs account): A, a ticking dawn panic that turns hopeful when Noah shows up; B, an upbeat build for the swap
montages; C, a dark storm cue that falls silent and turns to wonder when the offline AI starts writing; D, a bright
launch-day finale. SFX: ElevenLabs sound effects (assets/sfx/) plus hits from HyperFrames' bundled library (Pixabay
Content License). The music ducks under every line of dialogue. Writes assets/audio/mix.wav at about -14 LUFS.
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
L, E, CU, SW = T["l"], T["e"], T["cuts"], T["sw"]
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


def loop(x, dur):
    reps = int(np.ceil(dur * SR / len(x))) + 1
    return np.concatenate([x] * reps)[: int(dur * SR)]


def music():
    m = np.zeros((N, 2))
    M = lambda f: load(os.path.join(ROOT, "assets", "music", f))  # noqa: E731
    A, B, C, D = M("cueA_dawn.mp3"), M("cueB_montage.mp3"), M("cueC_storm.mp3"), M("cueD_launch.mp3")
    put(m, A, 0, 1.0, 0, CU[0] + .4, fin=.05, fout=.6)
    put(m, B, CU[0] - .2, 1.0, 0, CU[2] - CU[0] + .6, fin=.25, fout=.8)
    c0 = max(0.0, 13.4 - (SW[7] + .1 - (CU[2] - .2)))           # C turns hopeful about 13.4 s in: land that on the offline AI
    put(m, C, CU[2] - .2, 1.0, c0, c0 + CU[3] - CU[2] + .4, fin=.3, fout=.4)
    put(m, D, CU[3] - .1, 1.0, 0, DUR - CU[3] + .1, fin=.05, fout=1.4)
    return m


def sfx():
    s = np.zeros((N, 2))
    S = lambda n: load(os.path.join(ROOT, "assets", "sfx", n + ".mp3"))  # noqa: E731
    lib = lambda n: load(os.path.join(LIB, n + ".mp3"))  # noqa: E731
    room, rain = S("room_tone"), S("rain_bed")
    put(s, loop(room, CU[2]), 0, .5, fin=.5, fout=.6)
    put(s, loop(room, DUR - CU[3]), CU[3], .5, fin=.4, fout=1.0)
    put(s, loop(rain, CU[3] - CU[2] + .3), CU[2] - .1, 1.0, fin=.3, fout=.5)
    for t in CU:
        put(s, lib("whoosh-short"), t - .12, .35)
    # the cancellations
    put(s, S("phone_buzz"), .2, .8)
    note = lib("notification")
    for t in [L[0] + .05] + [L[1] + .1 + .36 * k for k in range(7)]:
        put(s, note, t, .4)
    put(s, S("footsteps"), L[2] - .2, .9)
    put(s, lib("impact-bass-1"), L[2] + 2.75, .55)
    put(s, S("knock"), T["knock"] - .05, 1.2)
    put(s, S("door_open"), E[3] + .45, .9)
    # the swaps: the old tile bursts into voxels, the new one snaps together
    burst, form = S("voxel_burst"), S("voxel_form")
    for b in SW:
        put(s, burst, b - .03, 1.0)
        put(s, form, b + .45, .8)
    typing = lib("typing")
    for a, b in ((CU[0] + .2, CU[0] + 1.2), (CU[1] + .2, CU[1] + 1.0), (CU[2] + .2, T["cut"] - .2)):
        put(s, loop(typing, b - a), a, .25, fin=.1, fout=.2)
    # the storm
    thunder = S("thunder")
    put(s, thunder, T["flash"][0] + .1, .55)
    put(s, thunder, T["flash"][1] + .05, 1.1)
    put(s, thunder, T["flash"][2] + .2, .45)
    put(s, S("power_down"), T["cut"] - .15, 1.0)
    put(s, lib("glitch-1"), T["cut"] + .4, .3)
    # launch day
    ping = S("order_ping")
    for k in range(3):
        put(s, ping, CU[3] + .15 + k * .22, .55)
    put(s, lib("chime"), T["zero"], .45)
    put(s, lib("sparkle"), T["endc"] + .3, .4)
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
    sf.write(os.path.join(ROOT, "assets", "audio", "score.wav"), m.astype(np.float32), SR, subtype="PCM_24")
    m = m * (.11 / rms(m)) * (1 - .55 * talk)[:, None]
    s = s * (.085 / rms(s)) * (1 - .35 * talk)[:, None]
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
