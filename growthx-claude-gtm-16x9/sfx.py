# Synthesizes the SFX bed from sfx.json (written by build.cjs) into assets/sfx.wav.
# Every sound is generated here, so there is nothing to license.
# Run: python3 sfx.py
import json, os, wave
import numpy as np

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(7)


def t_axis(d):
    return np.arange(int(d * SR)) / SR


def lowpass(x, cutoff):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))


def highpass(x, cutoff):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (cutoff / np.maximum(f, 1)) ** 4)
    return np.fft.irfft(X, len(x))


def sweep_noise(d, f0, f1, width=0.6):
    """Noise through a band-pass whose centre moves from f0 to f1 (log scale)."""
    n, hop, win = int(d * SR), 256, 1024
    noise = rng.standard_normal(n + win)
    out = np.zeros(n + win)
    w = np.hanning(win)
    freqs = np.fft.rfftfreq(win, 1 / SR)
    for start in range(0, n, hop):
        p = start / n
        fc = f0 * (f1 / f0) ** p
        mask = np.exp(-0.5 * (np.log2(np.maximum(freqs, 1) / fc) / width) ** 2)
        seg = np.fft.irfft(np.fft.rfft(noise[start:start + win] * w) * mask, win)
        out[start:start + win] += seg * w
    return out[:n]


def sine_sweep(d, f0, f1):
    t = t_axis(d)
    f = f0 * (f1 / f0) ** (t / d)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def norm(x, peak=1.0):
    m = np.max(np.abs(x)) or 1
    return x / m * peak


def whoosh():
    d = 0.55
    t = t_axis(d)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2 * np.exp(-((t / d - 0.55) ** 2) * 3)
    up = sweep_noise(d * 0.55, 350, 5000)
    down = sweep_noise(d * 0.45, 5000, 900)
    return norm(np.concatenate([up, down])[: len(t)] * env, 0.9)


def riser(d=0.9):
    t = t_axis(d)
    env = (t / d) ** 2.2
    x = sweep_noise(d, 300, 6000, 0.8) * 0.8 + sine_sweep(d, 160, 1100) * 0.25
    return norm(x * env, 0.8)


def impact(d=1.0, peak=1.0):
    t = t_axis(d)
    boom = sine_sweep(d, 120, 36) * np.exp(-t * 4.5)
    crack = lowpass(rng.standard_normal(len(t)), 2500) * np.exp(-t * 28)
    return norm(boom * 1.0 + norm(crack) * 0.55, peak)


def pop():
    d = 0.14
    t = t_axis(d)
    x = sine_sweep(d, 950, 260) * np.exp(-t * 38)
    return norm(x, 0.8)


def tick():
    d = 0.03
    t = t_axis(d)
    x = np.sin(2 * np.pi * 2300 * t) * np.exp(-t * 260) + highpass(rng.standard_normal(len(t)), 4000) * np.exp(-t * 500) * 0.3
    return norm(x, 0.6)


def click():
    d = 0.05
    t = t_axis(d)
    x = highpass(rng.standard_normal(len(t)), 2500) * np.exp(-t * 400) + np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 300) * 0.6
    return norm(x, 0.9)


def ding(freqs=(1568, 2349, 3136), d=1.1, peak=0.7):
    t = t_axis(d)
    x = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (3.5 + i * 2)) / (i + 1) for i, f in enumerate(freqs))
    return norm(x * np.minimum(t / 0.004, 1), peak)


def cash():
    a = ding((2093, 3136, 4186), 0.9, 0.7)
    b = ding((2637, 3951, 5274), 0.9, 0.7)
    out = np.zeros(len(a) + int(0.09 * SR))
    out[: len(a)] += a
    out[int(0.09 * SR):] += b
    return norm(out, 0.75)


def shimmer():
    notes = [1047, 1319, 1568, 2093, 2637, 3136]
    out = np.zeros(int(1.5 * SR))
    for i, f in enumerate(notes):
        n = ding((f, f * 2), 0.9, 0.5)
        s = int(i * 0.06 * SR)
        out[s:s + len(n)] += n
    return norm(out, 0.6)


BANK = {
    "whoosh": whoosh(), "riser": riser(), "impact": impact(), "impact_lite": impact(0.6, 0.6),
    "pop": pop(), "tick": tick(), "click": click(), "ding": ding(), "cash": cash(), "shimmer": shimmer(),
}


def main():
    cues = json.load(open(os.path.join(HERE, "sfx.json")))
    total = cues["duration"]
    mix = np.zeros(int(total * SR) + SR * 2)
    for c in cues["cues"]:
        s = BANK[c["type"]]
        i = int(max(c["t"], 0) * SR)
        mix[i:i + len(s)] += s[: len(mix) - i] * c.get("vol", 1.0)
    mix = mix[: int(total * SR)]
    mix = np.tanh(mix * 1.1) * 0.9  # soft-limit overlaps
    pcm = (mix * 32767).astype("<i2")
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    with wave.open(os.path.join(HERE, "assets", "sfx.wav"), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(pcm.tobytes())
    print("wrote assets/sfx.wav", len(cues["cues"]), "cues")


if __name__ == "__main__":
    main()
