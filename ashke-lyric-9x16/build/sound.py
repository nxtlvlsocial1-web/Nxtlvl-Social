"""The soundtrack, edited like a video edit: the song section reworked with edit moves, plus synthesized sound effects
on the picture's events. Everything is generated here (no stock sounds, no licences to check).

python3 build/sound.py      (from the project root; after build/generate.py, which writes plan/events.json; needs
numpy, scipy and ffmpeg)

Music edits on assets/audio/section.wav (60 s from 2:14):
  - the intro (before the first line) runs muffled through a low-pass, then opens on the first word
  - before each hit line: a reverse swell and a riser, the music cut out for a beat-eighth gap, then the hit lands
    with a sub boom
  - the two burst lines open on a stutter (the first eighth of a beat repeated)
  - a tape stop into the logo, then the logo's shimmer sting and a low hit over 3 s of tail
Effects (plan/events.json): typewriter clicks for typed letters, an impact for slams, an ink-stamp thud, pops for
stickers and labels, a marker squeak for circles, a camera shutter for prints and single frames, paper rustle,
whooshes for the camera whips, a glitch zap on the colour inverts, a flash pop, a click on the split frame, a paper
tear and a sparkle for the logo. Writes assets/audio/mix.wav (63 s, 48 kHz stereo, -14 LUFS).
"""
import json
import os
import subprocess
import sys

import numpy as np
from scipy import signal
from scipy.io import wavfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plan import line_times  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR, DUR, SONG = 48000, 63.0, 60.0
BEATS = json.load(open(os.path.join(ROOT, "plan", "beats_raw.json")))
PERIOD = 60 / BEATS["bpm"]
rng = np.random.default_rng(7)
HITS = [3, 12, 19, 26]          # the full-bleed hit lines
BURSTS = [7, 24]


def n(t):
    return int(round(t * SR))


def env(length, a=.002, d=.1):
    t = np.arange(length) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(d, 1e-4))


def bp(x, lo, hi, order=2):
    sos = signal.butter(order, [lo, hi], btype="band", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def hp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, btype="high", fs=SR, output="sos"), x)


def lp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, btype="low", fs=SR, output="sos"), x)


def noise(sec):
    return rng.standard_normal(n(sec))


# ------------------------------------------------------------------------------------------------ synthesized effects
def sfx_type():
    x = hp(noise(.03), 2500) * env(n(.03), .0005, .006) * .5
    x[: n(.003)] += .6 * rng.uniform(-1, 1, n(.003))
    tone = np.sin(2 * np.pi * rng.uniform(1700, 2300) * np.arange(n(.03)) / SR) * env(n(.03), .0005, .008) * .2
    return x + tone


def sfx_slam():
    L = n(.6)
    t = np.arange(L) / SR
    sub = np.sin(2 * np.pi * (70 * np.exp(-t * 3) + 38) * t) * np.exp(-t * 6)
    crack = lp(noise(.6), 3000) * env(L, .001, .05)
    return sub * .9 + crack * .5


def sfx_stamp():
    L = n(.3)
    t = np.arange(L) / SR
    return np.sin(2 * np.pi * 95 * t) * np.exp(-t * 18) * .8 + lp(noise(.3), 1500) * env(L, .001, .03) * .6


def sfx_pop():
    L = n(.09)
    t = np.arange(L) / SR
    f = 900 * np.exp(-t * 30) + 220
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(L, .001, .04) * .7


def sfx_tick():
    return sfx_pop()[: n(.05)] * .6


def sfx_marker():
    L = n(.34)
    t = np.arange(L) / SR
    x = bp(noise(.34), 2200, 5200) * (0.6 + .4 * np.sin(2 * np.pi * 26 * t)) * np.sin(np.pi * t / .34) ** .5
    return x * .35


def sfx_shutter():
    c = hp(noise(.02), 1500) * env(n(.02), .0003, .004)
    x = np.zeros(n(.12))
    x[: len(c)] += c
    x[n(.045): n(.045) + len(c)] += c * .8
    x += hp(noise(.12), 3000) * env(n(.12), .001, .03) * .25
    return x * .8


def sfx_paper():
    L = n(.28)
    crackle = (rng.random(L) < .02) * rng.uniform(-1, 1, L)
    x = hp(noise(.28) * .3 + crackle, 1800) * np.sin(np.pi * np.arange(L) / L) ** .7
    return x * .35


def sfx_whoosh():
    L = n(.42)
    t = np.arange(L) / SR
    x = noise(.42)
    out = np.zeros(L)
    for k in range(6):                                    # a band that sweeps up then down
        s, e = k * L // 6, (k + 1) * L // 6
        fc = 400 + 2600 * np.sin(np.pi * (k + .5) / 6)
        out[s:e] = bp(x, fc * .6, min(fc * 1.6, 20000))[s:e]
    shape = np.sin(np.pi * t / .42) ** 2
    return out * shape * .7


def sfx_glitch():
    L = n(.09)
    t = np.arange(L) / SR
    f = np.repeat(rng.uniform(200, 1400, 6), L // 6 + 1)[:L]
    sq = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR))
    sq = np.round(sq * 4) / 4
    return sq * env(L, .001, .06) * .35


def sfx_flash():
    x = hp(noise(.12), 2500) * env(n(.12), .001, .04) * .5
    p = sfx_pop()
    x[: len(p)] += p * .2
    return x


def sfx_click():
    return hp(noise(.03), 800) * env(n(.03), .0005, .006) * .8


def sfx_tear():
    L = n(.7)
    rip = (rng.random(L) < .06) * rng.uniform(-1, 1, L)
    x = hp(lp(rip + noise(.7) * .2, 6000), 500) * np.minimum(1, np.arange(L) / (SR * .1)) * np.exp(-np.arange(L) / (SR * .5))
    return x * .7


def sfx_sparkle():
    L = n(1.6)
    t = np.arange(L) / SR
    x = np.zeros(L)
    for k, f in enumerate([2093, 2637, 3136, 3951, 4699]):
        st = int(k * .06 * SR)
        x[st:] += np.sin(2 * np.pi * f * t[: L - st]) * np.exp(-t[: L - st] * 3.5) * .12
    return x


def sfx_logo():
    """Shimmer swell plus a soft low hit for the N drawing on."""
    L = n(2.6)
    t = np.arange(L) / SR
    pad = sum(np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) for f in (220, 277.2, 329.6, 440, 554.4)) / 5
    pad *= np.minimum(1, t / .9) * np.exp(-np.maximum(0, t - 1.2) * 1.4) * .32
    boom = np.sin(2 * np.pi * (48 * np.exp(-t * 2) + 34) * t) * np.exp(-t * 2.5) * .7
    shimmer = hp(noise(2.6), 6000) * np.minimum(1, t / 1.2) * np.exp(-np.maximum(0, t - 1.2) * 2) * .08
    return pad + boom + shimmer


def riser(sec=.8):
    L = n(sec)
    t = np.arange(L) / SR
    tone = np.sin(2 * np.pi * np.cumsum(200 + 1600 * (t / sec) ** 2) / SR) * .15
    hiss = hp(noise(sec), 2000) * .25
    return (tone + hiss) * (t / sec) ** 2


def rev_swell(sec=.6):
    L = n(sec)
    x = hp(noise(sec), 3000) * np.exp(-np.arange(L)[::-1] / (SR * .18))
    return x * .5


def sub_boom():
    L = n(.9)
    t = np.arange(L) / SR
    return np.sin(2 * np.pi * (60 * np.exp(-t * 4) + 36) * t) * np.exp(-t * 3) * .9


SFX = {"type": (sfx_type, .09), "slam": (sfx_slam, .5), "stamp": (sfx_stamp, .45), "pop": (sfx_pop, .28), "tick": (sfx_tick, .2),
       "marker": (sfx_marker, .35), "shutter": (sfx_shutter, .22), "paper": (sfx_paper, .3), "whoosh": (sfx_whoosh, .42),
       "glitch": (sfx_glitch, .3), "flash": (sfx_flash, .3), "click": (sfx_click, .35), "tear": (sfx_tear, .6),
       "sparkle": (sfx_sparkle, .55), "logo": (sfx_logo, .9)}


# ------------------------------------------------------------------------------------------------ the music edit
def load_song():
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(ROOT, "assets", "audio", "section.wav"), "-f", "f32le",
                          "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)


def edit_music(m):
    out = np.zeros((n(DUR), 2))
    out[: min(len(m), n(SONG))] = m[: n(SONG)]
    a0 = line_times(0)[0]
    # muffled intro opening on the first word (crossfaded over 60 ms)
    cut = n(a0)
    muff = np.stack([lp(out[:cut + n(.06), c], 650, 4) for c in range(2)], 1) * 1.15
    fade = np.linspace(1, 0, n(.06))[:, None]
    out[: cut] = muff[: cut]
    out[cut: cut + n(.06)] = muff[cut: cut + n(.06)] * fade + out[cut: cut + n(.06)] * (1 - fade)
    # hits: the music drops out for an eighth of a beat right before the line, riser and reverse swell lead in
    for li in HITS:
        a = line_times(li)[0]
        g0, g1 = n(a - PERIOD / 4), n(a - .01)
        ramp = np.linspace(1, 0, n(.02))[:, None]
        out[g0: g0 + len(ramp)] *= ramp
        out[g0 + len(ramp): g1] *= 0
    # bursts: stutter the first eighth of a beat four times
    for li in BURSTS:
        a = line_times(li)[0]
        sl = n(PERIOD / 4)
        piece = out[n(a): n(a) + sl].copy()
        win = np.hanning(sl)[:, None] ** .2
        for k in range(1, 4):
            out[n(a) + k * sl: n(a) + (k + 1) * sl] = piece * win * (1 - .12 * k)
    # tape stop into the logo
    ts, te = SONG - .45, SONG + .25
    seg = out[n(ts): n(te)].copy()
    L = len(seg)
    rate = np.linspace(1, 0, L) ** 1.4                          # playback speed falls to zero
    pos = np.cumsum(rate)
    pos = np.clip(pos, 0, L - 1)
    stopped = np.stack([np.interp(pos, np.arange(L), seg[:, c]) for c in range(2)], 1) * np.linspace(1, .2, L)[:, None]
    out[n(ts): n(te)] = stopped
    out[n(te):] = 0
    return out


def mix():
    out = edit_music(load_song())
    events = json.load(open(os.path.join(ROOT, "plan", "events.json")))
    cache = {}
    last = {}
    for t, kind in events:
        if kind == "type" and t - last.get("type", -1) < .05:
            continue
        if kind in ("paper", "shutter", "pop") and t - last.get(kind, -1) < .12:
            continue
        last[kind] = t
        fn, gain = SFX[kind]
        if kind not in cache or kind in ("type", "whoosh", "paper", "glitch"):
            cache[kind] = fn()
        x = cache[kind] * gain
        pan = rng.uniform(-.35, .35) if kind in ("type", "pop", "shutter", "paper", "tick") else 0
        st = n(max(0, t))
        en = min(len(out), st + len(x))
        out[st:en, 0] += x[: en - st] * (1 - pan)
        out[st:en, 1] += x[: en - st] * (1 + pan)
    for li in HITS:                                           # lead-ins and the landing for the hit lines
        a = line_times(li)[0]
        for x, start in ((riser(.8) * .55, a - .8), (rev_swell(.6) * .6, a - .6), (sub_boom() * .55, a)):
            st = n(start)
            out[st: st + len(x)] += x[:, None]
    for li in BURSTS:
        a = line_times(li)[0]
        x = riser(.6) * .4
        out[n(a - .6): n(a)] += x[:, None]
    raw = os.path.join(ROOT, "cache", "mix_raw.wav")
    wavfile.write(raw, SR, (np.clip(out, -4, 4) / 4).astype(np.float32))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", "volume=4,alimiter=limit=0.95:level=false,loudnorm=I=-14:TP=-1.0:LRA=11",
                    "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", os.path.join(ROOT, "assets", "audio", "mix.wav")], check=True)


if __name__ == "__main__":
    mix()
    print("wrote assets/audio/mix.wav")
