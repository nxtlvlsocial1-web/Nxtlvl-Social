"""Score, sound design and the mastered mix for the AI Future reel (the dialogue version).

python3 build/audio.py      (from the project root, after build/voice.py and build/generate.py; needs numpy, scipy,
soundfile, ffmpeg)

Music: cues composed for this reel with ElevenLabs Music (assets/music/, instrumental, generated on the owner's
ElevenLabs account): A, a ticking felt-piano mystery for New York (its hit lands on "the next day"); B, a heist pulse that
breaks into brass when the ball lands; C, war drums that peak as the span hits the water; D, a heartbeat drone for the
door that dies with the phone. The end card brings back A's clock theme, so the end loops to the start. SFX:
ElevenLabs sound effects (assets/sfx/: street, casino, roulette ball, crowd, rain, thunder, horns, the bridge, knocks,
the door handle, the phone glitch) plus a few hits from HyperFrames' bundled library (Pixabay Content License). The
music ducks under every line of dialogue. Writes assets/audio/mix.wav, mastered to -14 LUFS, -1.5 dBTP.
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
L, E, CU = T["l"], T["e"], T["cuts"]
SR = 48000
DUR = T["end"]
N = int(DUR * SR)
LIB = os.path.join(os.path.dirname(ROOT), ".claude", "skills", "media-use", "audio", "assets", "sfx")


def load(path, mono=False):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1" if mono else "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).astype(np.float64)
    return x if mono else x.reshape(-1, 2)


def put(bus, x, t, g=1.0, a=0.0, b=None, fin=.02, fout=.05):
    """Mix clip x (stereo) into bus at time t, from clip time a to b, with short fades."""
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


def hit(x, lo, hi):
    """The time of the strongest rise in loudness between lo and hi s: where a cue's big hit lands."""
    m = x.mean(1); hop = int(.05 * SR)
    e = np.array([np.sqrt(np.mean(m[i:i + hop] ** 2) + 1e-12) for i in range(0, len(m) - hop, hop)])
    d = 20 * np.log10(e[1:] + 1e-9) - 20 * np.log10(e[:-1] + 1e-9)
    i0, i1 = int(lo / .05), min(len(d), int(hi / .05))
    return (i0 + int(np.argmax(d[i0:i1])) + 1) * .05


def place(m, x, t_hit, cue_hit, a_scene, b_scene, g=1.0, fin=.4, fout=.6):
    """Play cue x so its hit lands at t_hit, inside the scene [a_scene, b_scene]."""
    start = t_hit - cue_hit
    a = max(0.0, a_scene - start)
    put(m, x, start + a, g, a, b_scene - start, fin=fin, fout=fout)


def music():
    m = np.zeros((N, 2))
    M = lambda f: load(os.path.join(ROOT, "assets", "music", f))  # noqa: E731
    A2, B2, C2, D, E2, A = M("cueA2_newyork.mp3"), M("cueB2_vegas.mp3"), M("cueC2_miami.mp3"), M("cueD_door.mp3"), M("cueE_horror.mp3"), M("cueA_newyork.mp3")
    put(m, A2, 0, 1.0, 0, CU[0] + .3, fin=.3, fout=.6)                           # New York: its pulses land on the phone, the clock flip and "it's real"
    put(m, B2, CU[0] - .3, 1.0, 0, CU[1] - CU[0] + .8, fin=.3, fout=.6)         # Las Vegas: a heist groove under the table
    place(m, C2, T["tc"] + .72, hit(C2, 15, 26), CU[1] - .4, CU[2] + .6, fout=.8)  # Miami: on the span hitting the water
    put(m, D, CU[2] - .2, 1.0, 0, CU[3] - CU[2] + .5, fin=.3, fout=.5)          # the door
    put(m, E2, CU[3] - .1, 1.0, 0, T["out"] - CU[3] + .1, fin=.4, fout=.03)     # day 30, the horror; cut dead when the lights go
    put(m, A, CU[4] + .1, .9, 0, DUR - CU[4], fin=.8, fout=1.2)                 # the end: the clock theme again
    return m


def sfx():
    s = np.zeros((N, 2))
    S = lambda n: load(os.path.join(ROOT, "assets", "sfx", n + ".mp3"))  # noqa: E731
    lib = lambda n: load(os.path.join(LIB, n + ".mp3"))  # noqa: E731
    for t in CU:
        put(s, lib("whoosh-short"), t - .12, .35)
    street, casino, storm = S("ny_street"), S("casino_bed"), S("storm_bed")
    put(s, street, 0, .9, 0, 15, fin=.6, fout=.3); put(s, street, 14.7, .9, 0, CU[0] - 14.7, fin=.3, fout=.4)
    put(s, lib("notification"), L[0] - .3, .4)
    put(s, lib("key-press"), T["led"], .5, 0, .1)
    put(s, S("coffee_splash"), T["tr"] + .9, 1.1)
    put(s, casino, CU[0] - .2, .8, 0, 15, fin=.4, fout=.4); put(s, casino, CU[0] + 14.6, .8, 0, CU[1] - CU[0] - 14.4, fin=.3, fout=.4)
    put(s, lib("click"), E[4] + 1.6, .4)
    tl = T["tl"]
    put(s, S("roulette_ball"), tl - 4.2, 1.0)
    put(s, S("crowd_cheer"), tl + 1.75, 1.0)
    put(s, lib("chime"), tl + .7, .3)
    put(s, lib("impact-bass-2"), tl, .8)
    put(s, storm, CU[1] - .2, 1.0, 0, 17.8, fin=.4, fout=.5); put(s, storm, CU[1] + 17.3, 1.0, 0, CU[2] - CU[1] - 17.0, fin=.5, fout=.6)
    thunder = S("thunder")
    for a in (CU[1] + .5, L[8] + 1.6, E[9] - .2):
        put(s, thunder, a + .15, .8)
    horns, rogue = S("car_horns"), S("rogue_cars")
    put(s, horns, E[8] + 1.0, .6, 0, 1.2); put(s, horns, E[9] - .5, .6, 0, 1.2)
    rh = hit(rogue, 0, 8)
    put(s, rogue, T["rog"] + 3.1 - rh, 1.0, 0, 6.5, fout=.6)
    put(s, S("bridge_collapse"), T["tc"] + .2, 1.3)
    put(s, thunder, T["tc"] + .55, .6)
    put(s, lib("notification"), L[12] - .3, .4)
    put(s, S("knocks"), E[12] + .3, 1.3)
    put(s, lib("notification"), E[13] + .15, .45)
    put(s, lib("impact-bass-1"), E[13] + .2, .45)
    put(s, S("door_handle"), E[13] + 1.6, 1.6)
    put(s, S("phone_glitch"), L[15] + .2, .7, 0, E[15] - .3 - (L[15] + .2) + .4, fout=.08)
    put(s, lib("impact-bass-2"), E[15] - .3, .5)
    flick = S("light_flicker")
    for a in (E[15] - .2, E[15] + 1.7, E[15] + 3.6):
        put(s, flick, a, .7, 0, min(2.0, T["out"] - a), fout=.05)
    put(s, S("horror_sting"), E[15] + 2.7, 1.2)
    put(s, lib("impact-bass-1"), T["out"], .7)
    put(s, street, CU[4], .45, 0, DUR - CU[4], fin=1.0, fout=1.2)
    return s


def ffmpeg(*a):
    return subprocess.run(["ffmpeg", "-y", "-hide_banner", *a], capture_output=True, text=True, check=True)


def main():
    voice, vsr = sf.read(os.path.join(ROOT, "assets", "audio", "voice.wav"))
    assert vsr == SR
    v = np.zeros(N); v[: min(N, len(voice))] = voice[:N]
    rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)  # noqa: E731
    # duck under each line of dialogue (with a short lead and tail)
    tt = np.arange(N) / SR
    talk = np.zeros(N)
    for a, b in zip(L, E):
        talk = np.maximum(talk, np.clip((tt - (a - .25)) / .25, 0, 1) * np.clip(((b + .3) - tt) / .3, 0, 1))
    m, s = music(), sfx()
    sf.write(os.path.join(ROOT, "assets", "audio", "score.wav"), m.astype(np.float32), SR, subtype="PCM_24")
    m = m * (.11 / rms(m)) * (1 - .55 * talk)[:, None]
    s = s * (.09 / rms(s)) * (1 - .35 * talk)[:, None]
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
