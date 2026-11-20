"""Game-show one-shots made for the NICHE reel: buzzer (wrong), chime (right answer), quiz (three-note "question" jingle),
drumroll, slotspin (reels whirring). python3 build/synth_show.py -> assets/sfx/<name>.mp3"""
import os, subprocess
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 44100
rng = np.random.default_rng(11)


def save(name, y):
    y = y / (np.abs(y).max() + 1e-9) * .9
    raw = os.path.join(ROOT, "assets", "sfx", f"{name}.f32")
    y.astype(np.float32).tofile(raw)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", raw, "-b:a", "192k",
                    os.path.join(ROOT, "assets", "sfx", f"{name}.mp3")], check=True)
    os.remove(raw)


def t_(d):
    return np.arange(int(SR * d)) / SR


def bell(f, d, dec=6):
    t = t_(d)
    return (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 2 * t) + .15 * np.sin(2 * np.pi * f * 3.01 * t)) * np.exp(-t * dec)


# buzzer: a fat detuned square at 110 Hz
t = t_(.6)
sq = np.sign(np.sin(2 * np.pi * 110 * t)) + np.sign(np.sin(2 * np.pi * 116.5 * t))
save("buzzer", sq * np.minimum(1, t * 60) * np.exp(-np.maximum(t - .45, 0) * 30))
# chime: right answer, two rising bell notes
save("chime", np.concatenate([bell(1046.5, .12, 10), bell(1568, .7, 5)]))
# quiz: the "next question" three-note jingle
save("quiz", np.concatenate([bell(784, .14, 9), bell(988, .14, 9), bell(1318.5, .8, 4)]))
# drumroll: snare noise hits at a quickening rate, crescendo, final hit
d = 1.8
y = np.zeros(int(SR * d))
tt, rate = 0.0, 18
while tt < d - .25:
    n = int(SR * .05)
    hit = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 70) * (.35 + .65 * tt / d)
    i = int(tt * SR)
    y[i:i + n] += hit[:len(y) - i]
    tt += 1 / rate
    rate = min(rate + .25, 30)
n = int(SR * .25)
i = int((d - .25) * SR)
y[i:i + n] += 1.6 * rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 18) + bell(90, .25, 14)[:n] * 1.2
save("drumroll", y)
# slotspin: fast ratchet clicks that slow down
d = 1.2
y = np.zeros(int(SR * d))
tt, gap = 0.0, .028
while tt < d - .05:
    n = int(SR * .012)
    c = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 400) + .5 * bell(2400, .012, 300)[:n]
    i = int(tt * SR)
    y[i:i + n] += c[:len(y) - i]
    tt += gap
    gap *= 1.035
save("slotspin", y)
