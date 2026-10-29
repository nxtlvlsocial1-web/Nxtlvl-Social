"""Music, sound design and the mastered mix for the Vitonnix Biotin reel.

python3 build/audio.py      (from the project root, after build/generate.py; needs numpy, scipy, soundfile, ffmpeg)

Music: an original track composed here in code (no licence or credit needed). 120 BPM, F#m - D - A - E, house-pop:
  hook        muffled groove under "Still swallowing biotin pills?"
  build       snare roll, noise riser and opening filter into the reveal, half a beat of silence, then
  drop        on "Vitonnix Biotin": four-on-the-floor kick, claps, hats, offbeat bass, pumping supersaw pad, pluck hook
  lift        half-time under the trust scenes (certified, doctors) with shimmer bells, a second build into the CTA
  CTA drop    full groove again, ending on one ringing chord
SFX: HyperFrames' bundled library (Pixabay Content License, commercial use, no credit; see
.claude/skills/media-use/audio/assets/sfx/CREDITS.md) plus synthesized ones (capsule crack, spray hiss, stamps,
slot ticks, shimmer). Voice sits on top; music is ducked under it. Mastered to -14 LUFS, -1.5 dBTP.
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, sosfilt, sosfilt_zi

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
L, E = T["l"], T["e"]
SR = 48000
DUR = T["end"]
N = int((DUR + 1) * SR)
rng = np.random.default_rng(5)
LIB = os.path.join(os.path.dirname(ROOT), ".claude", "skills", "media-use", "audio", "assets", "sfx")
_S = {}

BPM = 120
BEAT = 60 / BPM
BAR = 4 * BEAT
DROP = L[2]                       # "Vitonnix Biotin" reveal
LIFT = L[7]                       # certified: half-time section
DROP2 = L[9]                      # CTA
END_HIT = round(DROP2 + 2 * BAR, 3)   # last chord
# bar grid anchored on the drop
GRID0 = DROP - 2 * BAR


def bars(t0, t1):
    k0 = int(np.floor((t0 - GRID0) / BAR))
    k = k0
    while GRID0 + k * BAR < t1:
        yield k, GRID0 + k * BAR
        k += 1


def smp(name):
    if name not in _S:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(LIB, name + ".mp3"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                             capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.float32).astype(np.float64)
        _S[name] = x / (np.max(np.abs(x)) + 1e-9) * .5
    return _S[name]


def sos(kind, f, o=2):
    if kind == "band":
        return butter(o, [max(20, f[0]), min(f[1], SR / 2 - 200)], "band", fs=SR, output="sos")
    return butter(o, min(max(f, 20), SR / 2 - 200), kind, fs=SR, output="sos")


def lp(x, f, o=2):
    return sosfilt(sos("low", f, o), x, axis=0)


def hp(x, f, o=2):
    return sosfilt(sos("high", f, o), x, axis=0)


def bp(x, lo, hi, o=2):
    return sosfilt(sos("band", (lo, hi), o), x, axis=0)


def tt(d):
    return np.arange(int(d * SR)) / SR


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def put(buf, x, t, g=1.0, pan=0.0):
    i = int(round(t * SR))
    if x.ndim == 1:
        lg, rg = np.sqrt(.5 * (1 - pan)) * 1.414, np.sqrt(.5 * (1 + pan)) * 1.414
        x = np.stack([x * lg, x * rg], -1)
    if i < 0:
        x, i = x[-i:], 0
    n = min(len(x), len(buf) - i)
    if n > 0:
        buf[i:i + n] += x[:n] * g


def sweep_lp(x, f0, f1, curve=2.0, chunk=512):
    """Time-varying low-pass (f0 -> f1), chunked with carried filter state."""
    out = np.zeros_like(x)
    n = len(x)
    zi = None
    for i in range(0, n, chunk):
        p = (i / max(1, n - 1)) ** curve
        f = f0 * (f1 / f0) ** p
        s = sos("low", f, 2)
        if zi is None:
            zi = np.stack([sosfilt_zi(s) * 0 for _ in range(x.shape[1])], -1) if x.ndim == 2 else sosfilt_zi(s) * 0
        seg = x[i:i + chunk]
        if x.ndim == 2:
            y = np.zeros_like(seg)
            for c in range(x.shape[1]):
                y[:, c], zi[..., c] = sosfilt(s, seg[:, c], zi=zi[..., c])
        else:
            y, zi = sosfilt(s, seg, zi=zi)
        out[i:i + chunk] = y
    return out


# ------------------------------------------------------------------ instruments
def kick(g=1.0):
    t = tt(.42)
    f = 52 + 120 * np.exp(-t * 32)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5)
    click = hp(rng.normal(0, 1, len(t)) * np.exp(-t * 400), 2500) * .25
    return np.tanh((body + click) * 1.6) * g


def clap():
    t = tt(.35)
    x = np.zeros_like(t)
    for d in (0, .011, .022):
        i = int(d * SR)
        x[i:] += rng.normal(0, 1, len(t) - i) * np.exp(-(t[:len(t) - i]) * 60)
    tail = rng.normal(0, 1, len(t)) * np.exp(-t * 14) * .35
    return bp(x + tail, 900, 5500) * .9


def snare(g=1.0):
    t = tt(.2)
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * .6
    nz = bp(rng.normal(0, 1, len(t)), 1200, 9000) * np.exp(-t * 28)
    return (tone + nz) * g


def hat(open_=False):
    t = tt(.25 if open_ else .05)
    return hp(rng.normal(0, 1, len(t)) * np.exp(-t * (14 if open_ else 90)), 7500) * (.55 if open_ else .4)


def saw(f, t, phase=0.0):
    return 2 * ((f * t + phase) % 1) - 1


def supersaw(notes, d, cutoff=2600):
    t = tt(d)
    x = np.zeros((len(t), 2))
    for m in notes:
        f = hz(m)
        for j, det in enumerate((-.0019, -.0011, -.0004, .0004, .0011, .0019)):
            pan = -1 if j % 2 else 1
            v = saw(f * (1 + det), t, rng.uniform(0, 1))
            x[:, 0 if pan < 0 else 1] += v * .5
            x[:, 1 if pan < 0 else 0] += v * .2
    att = np.minimum(1, t / .02)
    rel = np.minimum(1, (d - t) / .12)
    x *= (att * rel)[:, None] / (len(notes) * 4)
    return lp(x, cutoff, 2)


def pluck(m, d=.45, bright=1.0):
    t = tt(d)
    f = hz(m)
    env = np.exp(-t * 9) * (1 - np.exp(-t * 1500))
    x = (np.sin(2 * np.pi * f * t) + .5 * bright * saw(f, t) * np.exp(-t * 18) + .2 * np.sin(2 * np.pi * 2 * f * t)) * env
    return lp(x, 5200 * bright)


def bell(m, d=1.6):
    t = tt(d)
    f = hz(m)
    x = (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 4) + .2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 7))
    return x * np.exp(-t * 2.6) * (1 - np.exp(-t * 2000))


def bass(m, d):
    t = tt(d)
    f = hz(m)
    x = np.sin(2 * np.pi * f * t) + .35 * lp(saw(f, t), 600) + .5 * np.sin(2 * np.pi * f / 2 * t)
    env = np.minimum(1, t / .006) * np.minimum(1, (d - t) / .03)
    return np.tanh(x * env * 1.3)


def noise_riser(d):
    x = rng.normal(0, 1, (int(d * SR), 2))
    t = tt(d)
    x *= ((t / d) ** 2.2)[:, None]
    return hp(sweep_lp(x, 500, 12000, 1.5), 300)


# ------------------------------------------------------------------ arrangement
CH = [[54, 57, 61, 66], [50, 54, 57, 62], [52, 57, 61, 64], [52, 56, 59, 64]]      # F#m D A E
ROOT_B = [42, 38, 45, 40]
DRUMS = np.zeros((N, 2)); PAD = np.zeros((N, 2)); BASS = np.zeros((N, 2)); LEAD = np.zeros((N, 2)); FX = np.zeros((N, 2))
KICKS = []


def section(t):
    if t < L[1] - .02:
        return "hook"
    if t < DROP:
        return "build"
    if t < LIFT:
        return "drop"
    if t < DROP2 - BAR:
        return "lift"
    if t < DROP2:
        return "build2"
    if t < END_HIT:
        return "drop2"
    return "end"


for k, t0 in bars(0, END_HIT):
    ch, rb = CH[k % 4], ROOT_B[k % 4]
    for b in range(4):
        tb = t0 + b * BEAT
        if tb < 0 or tb >= END_HIT:
            continue
        sec = section(tb)
        if sec in ("drop", "drop2", "hook") or (sec == "lift" and b in (0, 2)):
            if not (sec == "hook" and b == 3 and tb + BEAT > L[1]):
                put(DRUMS, kick(.9 if sec != "hook" else .7), tb)
                KICKS.append(tb)
        if sec in ("drop", "drop2"):
            if b in (1, 3):
                put(DRUMS, clap(), tb, .5)
            put(DRUMS, hat(True), tb + BEAT / 2, .35, .25)
            for s in range(4):
                put(DRUMS, hat(), tb + s * BEAT / 4, .22 if s % 2 else .12, -.3)
            put(BASS, bass(rb, BEAT / 2 - .03), tb + BEAT / 2, .5)
            if b == 3:
                put(BASS, bass(rb + 12, BEAT / 4 - .02), tb + 3 * BEAT / 4, .32)
        if sec == "lift":
            put(DRUMS, hat(), tb + BEAT / 2, .2, .3)
            if b == 2:
                put(DRUMS, clap(), tb, .35)
        if sec == "hook":
            put(DRUMS, hat(), tb + BEAT / 2, .14, .3)
    # pad: one chord per bar
    if t0 + BAR > 0:
        sec = section(max(0, t0) + .01)
        cut = {"hook": 900, "build": 900, "drop": 3200, "lift": 2200, "build2": 2200, "drop2": 3400}.get(sec, 2600)
        put(PAD, supersaw(ch, BAR + .05, cut), t0, .8 if sec in ("drop", "drop2") else .65)
    # lead hook: 8th-note plucks
    sec = section(max(0, t0) + .01)
    if sec in ("drop", "drop2", "lift"):
        hi = [n + 12 for n in ch]
        seq = [hi[3], hi[2], hi[1], hi[2], hi[3] + (0 if k % 2 else 2), hi[1], hi[2], hi[0] + 12]
        for i, m in enumerate(seq):
            ti = t0 + i * BEAT / 2
            if 0 <= ti < END_HIT and section(ti) in ("drop", "drop2", "lift"):
                put(LEAD, pluck(m, .42, 1.0 if section(ti) != "lift" else .7), ti, .16 if i % 2 == 0 else .11, -.45 if i % 2 else .45)

# builds: snare roll + riser + filter open + a short silence before each drop
for b0, b1 in ((L[1] - .02, DROP), (DROP2 - BAR, DROP2)):
    d = b1 - b0
    hits, t = [], b0
    while t < b1 - .12:
        p = (t - b0) / d
        step = BEAT / 2 if p < .4 else BEAT / 4 if p < .75 else BEAT / 8
        hits.append((t, .25 + .55 * p))
        t += step
    for th, g in hits:
        put(DRUMS, snare(g), th, .8)
    rise = noise_riser(d)
    put(FX, rise, b1 - d, .45)
# the half-beat gap before the first drop: cut everything for 110 ms
gap = np.ones(N)
for tg in (DROP, DROP2):
    i0, i1 = int((tg - .11) * SR), int(tg * SR)
    gap[i0:i1] = np.linspace(1, 0, i1 - i0) ** .3 * 0 + 0.0
    gap[i1 - 200:i1] = np.linspace(0, 1, 200)

# drop the filter on the hook pad (already low), open the build
build_i0, build_i1 = int((L[1] - .02) * SR), int(DROP * SR)
PAD[build_i0:build_i1] = sweep_lp(PAD[build_i0:build_i1], 700, 9000, 2.0)
hook_i1 = int((L[1] - .02) * SR)
DRUMS[:hook_i1] = lp(DRUMS[:hook_i1], 1400)

# end: one ringing chord with bells
put(PAD, supersaw(CH[0], 2.2, 2800), END_HIT, .9)
put(DRUMS, kick(1.0), END_HIT)
KICKS.append(END_HIT)
for i, m in enumerate([78, 81, 85, 90]):
    put(LEAD, bell(m, 2.0), END_HIT + .08 * i, .16, (-.4, .4)[i % 2])
put(BASS, bass(42, 1.6), END_HIT, .55)

# shimmer bells on sparkle moments
for t, ms in ((T["glow"], [85, 90, 93]), (T["biotin2"], [78, 85]), (T["nine"] + .08, [90, 97]), (T["nails"], [85, 90]),
              (T["certified"], [81, 85, 88]), (T["link"], [85, 90, 93])):
    for i, m in enumerate(ms):
        put(LEAD, bell(m, 1.4), t + .06 * i, .11, (-.5, .5)[i % 2])

# sidechain pump on pad, bass and lead from the kicks
pump = np.ones(N)
tk = np.arange(int(.32 * SR)) / SR
shape = 1 - .72 * np.exp(-tk / .09) * np.minimum(1, tk / .004 + .0001)
for t in KICKS:
    i = int(t * SR)
    n = min(len(shape), N - i)
    if n > 0:
        pump[i:i + n] = np.minimum(pump[i:i + n], shape[:n])
PAD *= pump[:, None]
BASS *= (.25 + .75 * pump)[:, None]
LEAD *= (.6 + .4 * pump)[:, None]

# reverb send
ir_t = tt(2.2)
ir = np.stack([rng.normal(0, 1, len(ir_t)), rng.normal(0, 1, len(ir_t))], -1) * np.exp(-ir_t / .55)[:, None]
ir = lp(ir, 6500) / np.sqrt(np.sum(ir ** 2) / 2)
send = PAD * .35 + LEAD * .9 + DRUMS * .06
wet = np.stack([fftconvolve(send[:, c], ir[:, c])[:N] for c in range(2)], -1) * .32
MUSIC = (DRUMS * 1.0 + PAD * 1.0 + BASS * .9 + LEAD * 1.0 + FX + wet) * gap[:, None]
MUSIC = np.tanh(MUSIC * 1.4) / 1.4

# ------------------------------------------------------------------ SFX
SFX = np.zeros((N, 2))


def crack():
    t = tt(.35)
    x = hp(rng.normal(0, 1, len(t)) * np.exp(-t * 90), 2000) * .8
    for f in (3100, 4700, 6900, 2300):
        x += np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * np.exp(-t * rng.uniform(25, 45)) * .25
    return x


def hiss(d=.6, g=1.0):
    t = tt(d)
    env = (1 - np.exp(-t * 300)) * np.exp(-t * 6)
    return hp(lp(rng.normal(0, 1, len(t)) * env, 10000), 2500) * g


def stamp():
    t = tt(.4)
    body = np.sin(2 * np.pi * np.cumsum(90 + 140 * np.exp(-t * 40)) / SR) * np.exp(-t * 12)
    return np.tanh(body * 2) * .8 + hp(rng.normal(0, 1, len(t)) * np.exp(-t * 200), 1500) * .4


def tick():
    t = tt(.04)
    return np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 160) * .6


def shimmer(d=.9):
    t = tt(d)
    x = np.zeros_like(t)
    for _ in range(14):
        f = rng.uniform(2500, 7500)
        t0 = rng.uniform(0, d * .6)
        i = int(t0 * SR)
        seg = t[:len(t) - i]
        x[i:] += np.sin(2 * np.pi * f * seg) * np.exp(-seg * 14) * .12
    return x


# hook
put(SFX, smp("impact-bass-1"), .55, .5)
for i, tp in enumerate((.15, .42, .7, 1.05, 1.4, 1.7)):
    put(SFX, smp("pop"), tp, .22, (-.6, .6)[i % 2])
put(SFX, shimmer(), T["biotin1"], .6)
for k in range(3):
    put(SFX, smp("click-soft"), T["pills"] + .09 * k, .35)
put(SFX, crack(), L[1] - .14, .9)
put(SFX, smp("whoosh-cinematic"), L[1] - .05, .45)
put(SFX, smp("sparkle"), L[1] + .02, .55)
put(SFX, shimmer(1.2), T["glow"], .8)
# reveal
put(SFX, smp("impact-bass-2"), DROP, .55)
put(SFX, smp("whoosh-short"), DROP - .05, .45)
put(SFX, smp("sparkle"), DROP + .45, .35)
put(SFX, shimmer(), T["biotin2"], .5)
# one spray
put(SFX, smp("whoosh-short"), L[3] - .08, .4)
put(SFX, smp("pop"), T["one"], .5)
put(SFX, hiss(.7, 1.0), T["spray"], .55)
put(SFX, stamp(), T["done"], .7)
# 9X roll: one tick per digit as the eased reel passes it (power3.inOut)
r0, r1 = L[4] + .25, T["nine"] + .08
ts = np.linspace(0, 1, 2000)
eased = np.where(ts < .5, 4 * ts ** 3, 1 - (-2 * ts + 2) ** 3 / 2)
for d in range(1, 9):
    t_d = r0 + ts[np.searchsorted(eased, d / 8)] * (r1 - r0)
    put(SFX, tick(), t_d - .03, .7, (-.3, .3)[d % 2])
put(SFX, smp("impact-bass-2"), r1, .55)
put(SFX, smp("chime"), r1 + .02, .3)
put(SFX, smp("whoosh-short"), T["x"] - .05, .35)
put(SFX, shimmer(), T["absorption"], .5)
# benefits
put(SFX, smp("whoosh-short"), L[5] - .08, .45)
for k in ("hair", "skin", "nails"):
    put(SFX, smp("pop"), T[k], .45)
put(SFX, smp("sparkle"), T["nails"] + .1, .35)
# flavour
put(SFX, smp("whoosh-short"), L[6] - .08, .4)
put(SFX, smp("pop"), T["lychee"], .35); put(SFX, smp("pop"), T["mint"], .35, .4)
put(SFX, smp("whoosh-short"), T["no"] - .15, .35)
put(SFX, stamp(), T["no"], .6); put(SFX, stamp(), T["sugar"] - .03, .55)
# certified
put(SFX, smp("whoosh-short"), L[7] - .05, .35)
for t in (T["fssai"], T["gmp"], T["certified"] - .05):
    put(SFX, stamp(), t, .65)
put(SFX, smp("click-soft"), T["certified"] + .05, .4)
# doctors + UK
put(SFX, smp("whoosh-short"), T["created"] - .1, .4)
for i in range(3):
    put(SFX, smp("pop"), T["three"] + .1 * i, .35)
put(SFX, smp("whoosh-short"), T["uk"] - .18, .4, .4)
put(SFX, smp("pop"), T["sublispray"], .35)
# CTA
put(SFX, smp("impact-bass-2"), DROP2, .5)
put(SFX, smp("pop"), T["comment"], .4)
for i in range(6):
    put(SFX, smp("key-press"), T["biotin3"] + .02 + .065 * i, .45)
put(SFX, smp("notification"), T["dm"], .3)
put(SFX, smp("chime"), T["link"], .3)
put(SFX, shimmer(1.4), T["link"] + .4, .6)

# ------------------------------------------------------------------ voice, ducking, master
vraw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(ROOT, "assets", "audio", "voice.wav"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                      capture_output=True, check=True).stdout
voice = np.frombuffer(vraw, np.float32).astype(np.float64)
VO = np.zeros((N, 2))
put(VO, voice, 0.0, 1.0)
env = np.convolve(np.abs(voice), np.ones(int(.05 * SR)) / int(.05 * SR), mode="same")
env = np.concatenate([env, np.zeros(max(0, N - len(env)))])[:N]
target = 1 - .55 * np.minimum(1, env / (np.percentile(env[env > 1e-4], 60) + 1e-9))
duck = np.empty(N)
a_dn, a_up = np.exp(-1 / (.025 * SR)), np.exp(-1 / (.30 * SR))
cur = 1.0
for i in range(N):
    g = target[i]
    cur = g + (cur - g) * (a_dn if g < cur else a_up)
    duck[i] = cur
MUSIC *= duck[:, None]
MIX = VO * 1.0 + MUSIC * .62 + SFX * .6
MIX = MIX[:int(DUR * SR)]
fade = int(.35 * SR)
MIX[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
MIX = MIX / (np.max(np.abs(MIX)) + 1e-9) * .9
tmp = os.path.join(ROOT, "assets", "audio", "_premaster.wav")
sf.write(tmp, MIX.astype(np.float32), SR, subtype="FLOAT")
sf.write(os.path.join(ROOT, "assets", "audio", "music.wav"), (MUSIC[:int(DUR * SR)] / (np.max(np.abs(MUSIC)) + 1e-9) * .9).astype(np.float32), SR, subtype="FLOAT")
out = os.path.join(ROOT, "assets", "audio", "mix.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(SR), "-c:a", "pcm_s16le", out], check=True)
os.remove(tmp)
print("mix.wav", subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip(), "s;",
      f"drop at {DROP:.2f}s, lift {LIFT:.2f}s, CTA drop {DROP2:.2f}s, last chord {END_HIT:.2f}s")
