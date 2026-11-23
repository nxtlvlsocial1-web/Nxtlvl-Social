"""Sound effects for find-skills-9x16, synthesised here (no third-party audio, nothing to license).

python3 build/sfx.py      (from the project root, after build/voice.py; needs numpy)
Writes assets/sfx/<name>.wav (each effect once, for reuse) and assets/audio/mix.wav (48 kHz stereo), the track
index.html plays: the voiceover (assets/audio/voice.wav) with the effects under it. Cues are keyed to scene starts
and spoken words from build/timing.json (written by build/voice.py), like the animation. No music.
"""
import json
import os
import wave

import numpy as np

SR = 48000
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIMING = json.load(open(os.path.join(ROOT, "build", "timing.json")))
DUR, SC = TIMING["end"], TIMING["scenes"]
SFX_GAIN = 0.42  # effects well under the voice


def W(line, word, occ=0):
    ws = [w for w in TIMING["lines"][line]["words"] if w["w"] == word]
    return (ws[occ] if len(ws) > occ else ws[-1])["s"] if ws else TIMING["lines"][line]["start"]


def o2n(t):
    return t


rng = np.random.default_rng(1234)


def env(n, a, d):
    """attack a seconds then exponential decay d (seconds to -60 dB-ish)"""
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-4), np.exp(-(t - a) * 6.9 / d))
    return e


def biquad_bp(x, f0, q):
    """time-varying band-pass (f0 may be an array)"""
    f0 = np.broadcast_to(np.asarray(f0, dtype=float), x.shape)
    y = np.zeros_like(x)
    x1 = x2 = y1 = y2 = 0.0
    for i in range(len(x)):
        w = 2 * np.pi * f0[i] / SR
        al = np.sin(w) / (2 * q)
        b0, b2, a0, a1, a2 = al, -al, 1 + al, -2 * np.cos(w), 1 - al
        yi = (b0 * x[i] + b2 * x2 - a1 * y1 - a2 * y2) / a0
        x2, x1, y2, y1 = x1, x[i], y1, yi
        y[i] = yi
    return y


def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def norm(x, peak=0.9):
    m = np.max(np.abs(x)) or 1
    return x / m * peak


def whoosh(d=0.38, f0=500, f1=5200):
    n = int(d * SR)
    t = np.linspace(0, 1, n)
    noise = rng.standard_normal(n)
    f = f0 * (f1 / f0) ** (np.sin(np.pi * t * 0.5) ** 1.2)
    y = biquad_bp(noise, f, 1.4)
    y *= np.sin(np.pi * t) ** 1.6
    return norm(y, 0.8)


def tick(f=2600, d=0.05):
    n = int(d * SR)
    t = np.arange(n) / SR
    y = np.sin(2 * np.pi * f * t) * env(n, 0.001, d) + 0.4 * rng.standard_normal(n) * env(n, 0.0005, 0.006)
    return norm(y, 0.7)


def pop(f0=320, f1=980, d=0.12):
    n = int(d * SR)
    t = np.arange(n) / SR
    f = f0 + (f1 - f0) * (1 - np.exp(-t / 0.02))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return norm(np.sin(ph) * env(n, 0.002, d), 0.75)


def impact(d=0.9, f0=140, f1=38, big=True):
    n = int(d * SR)
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t / 0.07)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * env(n, 0.002, d)
    click = lowpass(rng.standard_normal(n), 2500) * env(n, 0.0005, 0.05) * 3
    y = np.tanh((body * (1.6 if big else 1.0) + click) * 1.8)
    return norm(y, 0.95 if big else 0.7)


def zip_(d=0.16):
    n = int(d * SR)
    t = np.linspace(0, 1, n)
    y = biquad_bp(rng.standard_normal(n), 1800 + 6000 * t, 2.5) * np.sin(np.pi * t) ** 0.7
    return norm(y, 0.7)


def ding(f=1568, d=0.5):
    n = int(d * SR)
    t = np.arange(n) / SR
    y = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.01 * t) + 0.25 * np.sin(2 * np.pi * f * 3.02 * t)) * env(n, 0.002, d)
    return norm(y, 0.5)


def key(d=0.03):
    n = int(d * SR)
    y = biquad_bp(rng.standard_normal(n), 3200, 3) * env(n, 0.0005, d)
    return norm(y, 0.6)


def drain(d=0.95):
    n = int(d * SR)
    t = np.arange(n) / SR
    f = 900 * (0.25 ** (t / d))
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = (np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.sin(np.pi * t / d) ** 0.5
    return norm(y, 0.45)


FX = {
    "whoosh": whoosh(), "whoosh_short": whoosh(0.24, 900, 6000), "whoosh_long": whoosh(0.5, 300, 4200),
    "tick": tick(), "tick_lo": tick(1700, 0.045), "pop": pop(), "pop_hi": pop(520, 1500, 0.1),
    "impact": impact(), "impact_small": impact(0.5, 180, 60, big=False), "zip": zip_(), "ding": ding(), "key": key(), "drain": drain(),
}

# (time, effect, gain dB, pan -1..1)
CUES = []
add = lambda t, n, g=0.0, p=0.0: CUES.append((t, n, g, p))
# 0: cards land on the pile, one by one (card k lands at -0.66 + k * 0.22, faster after the 8th)
for k in range(12):
    t = -0.66 + k * 0.22 * (0.8 if k > 7 else 1.0)
    if 0 <= t < SC[1]:
        add(t, "tick_lo", -12, (k % 3 - 1) * 0.4)
add(SC[1] - 0.2, "whoosh", -6, 0.2)
# 1: the galaxy and the counter
add(SC[1], "impact_small", -8)
for k in range(16):
    add(SC[1] + 0.12 + (W(1, "million") + 0.3 - SC[1] - 0.12) * (k / 16) ** 0.8, "tick", -20 + k * 0.3, (k % 2) * 0.4 - 0.2)
add(W(1, "million") + 0.3, "impact", -5)
# 2: the right four light up
add(SC[2], "whoosh_short", -11, -0.3)
for k in range(4):
    add(W(2, "right") - 0.1 + k * 0.09, "pop", -11, -0.5 + k * 0.33)
# 3: find-skills spins in
add(W(3, "find") - 0.2, "whoosh_long", -8)
add(W(3, "find") + 0.35, "impact_small", -7)
add(W(3, "vercel"), "ding", -16)
# 4: the prompt rises and types
add(SC[4], "whoosh_short", -10, 0.3)
n = 32
for k in range(0, n, 2):
    add(W(4, "tell") + (W(4, "reel") + 0.25 - W(4, "tell")) * k / n, "key", -12, 0.2)
add(W(4, "reel") + 0.45, "pop_hi", -10)
# 5: search, pick, install
add(W(5, "searches"), "whoosh_long", -8, -0.2)
for k in range(4):
    add(W(5, "picks") + k * 0.12, "whoosh_short", -15, -0.6 + k * 0.4)
for k in range(4):
    add(W(5, "installs") + k * 0.14, "ding", -14, -0.4 + k * 0.27)
# 6: leaderboard
add(SC[6], "impact_small", -8)
for k in range(4):
    add(SC[6] + 0.15 + k * 0.1, "zip", -16, -0.3 + k * 0.2)
add(W(6, "number"), "impact_small", -6)
for k in range(10):
    add(W(6, "four") - 0.1 + 0.75 * (k / 10) ** 0.8, "tick", -19)
add(W(6, "four") + 0.75, "impact", -5)
# 7: SKILLS drops in, the comment posts, the link goes out
add(SC[7], "whoosh_short", -10, -0.3)
for k in range(6):
    add(W(7, "word") - 0.05 + k * 0.07, "pop", -12, -0.5 + k * 0.2)
for k in range(6):
    add(W(7, "skills") - 0.12 + k * 0.07, "key", -10, 0.2)
add(W(7, "send"), "pop_hi", -9)
add(W(7, "link") - 0.05, "ding", -11)
# the characters
add(W(2, "this") + 0.3, "impact_small", -6, 0.4)   # the Skill Finder crash-lands (poof)
add(W(2, "this") + 0.05, "whoosh_short", -12, 0.5)
add(W(3, "find"), "pop_hi", -13, 0.4)                # it jumps on "find-skills"
add(SC[5] + 0.1, "whoosh_long", -9, 0.4)             # jetpack lifts off
add(W(5, "picks") + 0.55, "whoosh_long", -14, -0.2)  # flies back with the cards
add(W(7, "send"), "impact_small", -8)                 # high five
for k in range(6):
    add(W(6, "four") + 0.8 + k * 0.07, "ding", -20, -0.6 + 0.24 * k)  # confetti on 4.5M
add(SC[-1] - 0.25, "whoosh", -9, -0.3)  # into the loop


def write_wav(path, data):
    data = np.clip(data, -1, 1)
    pcm = (data * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2 if data.ndim == 2 else 1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def main():
    os.makedirs(os.path.join(ROOT, "assets", "sfx"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "assets", "audio"), exist_ok=True)
    for name, x in FX.items():
        write_wav(os.path.join(ROOT, "assets", "sfx", name + ".wav"), x)
    mix = np.zeros((int(DUR * SR), 2))
    for t, name, g, p in CUES:
        x = FX[name] * 10 ** (g / 20) * SFX_GAIN
        i = int(round(o2n(t) * SR))
        j = min(len(mix), i + len(x))
        l, r = np.sqrt((1 - p) / 2), np.sqrt((1 + p) / 2)
        mix[i:j, 0] += x[: j - i] * l * 1.414
        mix[i:j, 1] += x[: j - i] * r * 1.414
    with wave.open(os.path.join(ROOT, "assets", "audio", "voice.wav")) as w:  # 24 kHz mono from Kokoro
        vsr = w.getframerate()
        v = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float64) / 32768
    v = np.interp(np.arange(int(len(v) * SR / vsr)) / SR, np.arange(len(v)) / vsr, v)
    n = min(len(v), len(mix))
    mix[:n, 0] += v[:n]
    mix[:n, 1] += v[:n]
    peak = np.max(np.abs(mix))
    mix = mix / peak * 0.89 if peak > 0.89 else mix  # about -1 dBFS peaks
    write_wav(os.path.join(ROOT, "assets", "audio", "mix.wav"), mix)
    print(f"{len(CUES)} cues, peak {20 * np.log10(np.max(np.abs(mix))):.1f} dBFS")


if __name__ == "__main__":
    main()
