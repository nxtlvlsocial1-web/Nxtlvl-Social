"""Music, sound design and the mastered mix for the Vitonnix SubliSpray reel.

python3 build/audio.py      (from the project root, after build/generate.py; needs numpy, scipy, soundfile, ffmpeg)

Music: a short original bed composed in code (bright plucked arpeggio over a soft pad, 112 BPM, D major), so there is
no licence or credit to clear. SFX: hits from HyperFrames' bundled library (Pixabay Content License, commercial use,
no credit needed; .claude/skills/media-use/audio/assets/sfx/CREDITS.md) plus synthesized spray hisses.
Writes assets/audio/mix.wav, mastered to -14 LUFS integrated, -1.5 dBTP, voice on top with the music ducked under it.
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
SR = 48000
DUR = T["end"]
N = int(DUR * SR) + SR
rng = np.random.default_rng(7)
LIB = os.path.join(os.path.dirname(ROOT), ".claude", "skills", "media-use", "audio", "assets", "sfx")
_S = {}


def smp(name):
    if name not in _S:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(LIB, name + ".mp3"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                             capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.float32).astype(np.float64)
        _S[name] = x / (np.max(np.abs(x)) + 1e-9) * .5
    return _S[name]


def lp(x, fc, o=2):
    return sosfilt(butter(o, min(fc, SR / 2 - 100), "low", fs=SR, output="sos"), x, axis=0)


def hp(x, fc, o=2):
    return sosfilt(butter(o, fc, "high", fs=SR, output="sos"), x, axis=0)


def tt(d):
    return np.arange(int(d * SR)) / SR


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def put(buf, x, t, g=1.0, pan=0.0):
    i = int(t * SR)
    if i < 0:
        x = x[-i:]
        i = 0
    n = min(len(x), len(buf) - i)
    if n <= 0:
        return
    l_, r_ = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan))
    buf[i:i + n, 0] += x[:n] * g * l_ * 1.414
    buf[i:i + n, 1] += x[:n] * g * r_ * 1.414


# ---------------------------------------------------------------- music
BPM = 112
BEAT = 60 / BPM
MUSIC = np.zeros((N, 2))
# D major: progression D - A - Bm - G (I V vi IV), two beats each = one chord per bar at double speed feel
CHORDS = [[62, 66, 69, 74], [57, 61, 64, 69], [59, 62, 66, 71], [55, 59, 62, 67]]


def pluck(f, d, bright=1.0):
    t = tt(d)
    env = np.exp(-t * 7.5) * (1 - np.exp(-t * 900))
    x = np.sin(2 * np.pi * f * t) + .45 * bright * np.sin(2 * np.pi * 2 * f * t + .3) + .18 * bright * np.sin(2 * np.pi * 3 * f * t)
    return lp(x * env, 6000 * bright + 800)


def pad(notes, d):
    t = tt(d)
    x = np.zeros_like(t)
    for m in notes:
        f = hz(m)
        x += np.sin(2 * np.pi * f * t + 0.1 * np.sin(2 * np.pi * .3 * t)) + .5 * np.sin(2 * np.pi * (f * 2.003) * t)
    a = np.minimum(1, t / .6)
    r = np.minimum(1, (d - t) / .8)
    return lp(x * a * r / len(notes), 1400)


def kick(d=.3):
    t = tt(d)
    f = 150 * np.exp(-t * 18) + 48
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14)


def hat(d=.08):
    t = tt(d)
    return hp(rng.normal(0, 1, len(t)) * np.exp(-t * 80), 7000) * .6


def hiss(d=.45, g=1.0):
    """A spray: short burst of filtered noise with a fast attack and a breathy tail."""
    t = tt(d)
    env = (1 - np.exp(-t * 400)) * np.exp(-t * 9)
    x = rng.normal(0, 1, len(t)) * env
    return hp(lp(x, 9000), 1800) * g


bar = 0
t = 0.0
MUSIC_END = DUR - .2
step = 0
while t < MUSIC_END:
    ch = CHORDS[bar % 4]
    put(MUSIC, pad(ch, BEAT * 2 + .3), t, .13)
    # arpeggio: 8th notes through the chord, up then top-down
    seq = [ch[0], ch[1], ch[2], ch[3], ch[2] + 12 if bar % 2 else ch[3], ch[1] + 12 if bar % 2 else ch[2]][:4]
    for k in range(4):
        tk = t + k * BEAT / 2
        if tk < MUSIC_END:
            m = seq[k] + (12 if k in (1, 3) and bar % 4 == 2 else 0)
            put(MUSIC, pluck(hz(m), .5, 1.0), tk, .16 if k % 2 == 0 else .11, pan=(-.35 if k % 2 == 0 else .35))
    # light beat from the hero section on (after the hook)
    if t >= L[1] - .05:
        put(MUSIC, kick(), t, .55)
        put(MUSIC, kick(), t + BEAT, .4)
        for k in range(4):
            put(MUSIC, hat(), t + k * BEAT / 2 + BEAT / 4, .25 if k % 2 else .15, pan=.2)
    t += BEAT * 2
    bar += 1
# lift at the "Pick yours" scene: octave-up plucks
tL = L[5]
for k in range(8):
    tk = tL + k * BEAT / 2
    put(MUSIC, pluck(hz(CHORDS[k % 4][2] + 12), .5, 1.2), tk, .09, pan=(-.5 if k % 2 else .5))
MUSIC = lp(MUSIC, 9000)

# ---------------------------------------------------------------- SFX
SFX = np.zeros((N, 2))
put(SFX, smp("pop"), T["still"], .55); put(SFX, smp("pop"), T["swallowing"], .5); put(SFX, smp("pop"), T["your"], .5)
put(SFX, smp("impact-bass-1"), T["vitamins"], .5)                       # pill lands
put(SFX, smp("whoosh-short"), L[1] - .12, .6)                             # bottle rises
put(SFX, smp("sparkle"), T["vitonnix"], .45)
put(SFX, hiss(.5), T["sublispray"] + .05, .55)
put(SFX, smp("whoosh-short"), T["spray"] - .12, .5); put(SFX, hiss(.55, 1.2), T["spray"] + .06, .7)
put(SFX, smp("click-soft"), T["swallow"] + .18, .6)
put(SFX, hiss(.4), T["two"] + .04, .6); put(SFX, hiss(.4), T["sprays"] + .06, .6)
put(SFX, smp("pop"), T["two"] + .02, .4); put(SFX, smp("pop"), T["sprays"] + .02, .4)
put(SFX, smp("impact-bass-2"), T["done"], .6); put(SFX, smp("sparkle"), T["done"] + .05, .4)
put(SFX, smp("whoosh-cinematic"), L[4] - .2, .45)
for key, extra in (("pills", .22), ("water", .22), ("aftertaste", .12)):
    put(SFX, smp("whoosh-short"), T[key] - .1, .35)
    put(SFX, smp("click"), T[key] + extra, .7)
put(SFX, smp("whoosh-short"), L[5] - .12, .5)
for key in ("d", "b12", "biotin"):
    put(SFX, smp("pop"), T[key], .55); put(SFX, smp("sparkle"), T[key] + .18, .3)
put(SFX, smp("whoosh-short"), T["bottle"], .4)
for key in ("wherever", "day", "takes"):
    put(SFX, smp("pop"), T[key], .45)
put(SFX, smp("whoosh-short"), T["created"] - .08, .45); put(SFX, smp("whoosh-short"), T["developed"] - .08, .45)
for i in range(3):
    put(SFX, smp("click-soft"), T["three"] + .09 * i + .1, .5)
put(SFX, smp("pop"), T["uk"] + .15, .5)
put(SFX, smp("whoosh-short"), L[8] - .12, .5); put(SFX, smp("chime"), T["tata"], .35); put(SFX, hiss(.45), T["available"] + .1, .45)
put(SFX, smp("whoosh-cinematic"), L[9] - .2, .45); put(SFX, smp("pop"), T["comment"], .5)
for i in range(5):
    put(SFX, smp("key-press"), T["spraykw"] + .06 + .07 * i, .5)
put(SFX, hiss(.45), T["spraykw"] + .1, .45); put(SFX, smp("notification"), T["dm"], .35); put(SFX, smp("sparkle"), T["link"], .35)

# ---------------------------------------------------------------- voice + ducking
vraw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(ROOT, "assets", "audio", "voice.wav"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                      capture_output=True, check=True).stdout
voice = np.frombuffer(vraw, np.float32).astype(np.float64)
VO = np.zeros((N, 2))
put(VO, voice, 0.0, 1.0)
# duck music under speech: envelope from the voice itself
env = np.abs(voice)
win = int(.05 * SR)
env = np.convolve(env, np.ones(win) / win, mode="same")
env = np.concatenate([env, np.zeros(N - len(env))]) if len(env) < N else env[:N]
duck = 1 - .62 * np.minimum(1, env / (np.percentile(env[env > 0], 70) + 1e-9))
# smooth the duck (attack 30 ms, release 350 ms)
d = np.empty_like(duck)
a_up, a_dn = np.exp(-1 / (.03 * SR)), np.exp(-1 / (.35 * SR))
cur = 1.0
for i in range(N):
    tgt = duck[i]
    cur = tgt + (cur - tgt) * (a_up if tgt < cur else a_dn)
    d[i] = cur
MUSIC *= d[:, None]
MIX = VO * 1.0 + MUSIC * .55 + SFX * .7
MIX = MIX[:int(DUR * SR)]
MIX = np.clip(MIX / (np.max(np.abs(MIX)) + 1e-9) * .89, -1, 1)
tmp = os.path.join(ROOT, "assets", "audio", "_premaster.wav")
sf.write(tmp, MIX.astype(np.float32), SR, subtype="FLOAT")
out = os.path.join(ROOT, "assets", "audio", "mix.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(SR), "-c:a", "pcm_s16le", out], check=True)
os.remove(tmp)
print("mix.wav", subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip(), "s")
