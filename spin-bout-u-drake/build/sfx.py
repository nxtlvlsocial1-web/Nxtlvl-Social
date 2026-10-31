"""Transition swooshes for the edit, synthesised from noise (ours, no third-party audio), mixed under the song.

python3 build/sfx.py      (after build/generate.py, which writes plan/sfx.json; needs numpy and scipy)

Shaped on the owner's anime-edit reference (Video-15991), measured off its audio: a whip-snap that hits on the cut
frame (energy jumps about 10x within 20 ms), sits around 5 kHz, dips then lifts in pitch and decays over about
0.2 s with a short tail, a little low body under it, and a stereo sweep. On the biggest cuts the reference drops
the music out for a split second before the hit; "drop" events do the same here.
Kinds: whip (the cut), snap (a short tick for in-scene hits), riser (a 0.3 s rise into a big cut), boom (low hit).
Writes assets/audio/sfx/<kind>.wav (one take each, for checking) and assets/audio/section_sfx.wav (song + sfx).
"""
import json
import os
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000


def stft_band(noise, centres, width_oct, n=1024, hop=256):
    """Noise filtered through a band whose centre follows centres(t) (Hz), by STFT masking."""
    win = np.hanning(n)
    out = np.zeros(len(noise) + n)
    norm = np.zeros(len(noise) + n)
    f = np.fft.rfftfreq(n, 1 / SR)
    lf = np.log2(np.maximum(f, 20))
    for i in range(0, len(noise) - n, hop):
        c = centres((i + n / 2) / SR)
        mask = np.exp(-.5 * ((lf - np.log2(c)) / width_oct) ** 2)
        seg = np.fft.irfft(np.fft.rfft(noise[i:i + n] * win) * mask)
        out[i:i + n] += seg * win
        norm[i:i + n] += win ** 2
    return out[:len(noise)] / np.maximum(norm[:len(noise)], 1e-3)


def take(kind, seed):
    g = np.random.default_rng(seed)
    if kind == "whip":
        d = .42
        t = np.arange(int(d * SR)) / SR
        hi = stft_band(g.normal(0, 1, len(t)), lambda x: 5200 * (1 - .18 * np.exp(-((x - .05) / .04) ** 2)) * (1 + .25 * max(0, x - .1)), .55)
        env = np.where(t < .012, t / .012, np.exp(-(t - .012) / .075) * .8 + .2 * np.exp(-(t - .012) / .22))
        lo = stft_band(g.normal(0, 1, len(t)), lambda x: 260, .7) * np.exp(-t / .07)
        s = hi * env + .35 * lo
        pan = np.clip(.5 + (t - .1) * 2.2, 0, 1)            # left to right
    elif kind == "snap":
        d = .2
        t = np.arange(int(d * SR)) / SR
        s = stft_band(g.normal(0, 1, len(t)), lambda x: 6500, .45) * np.where(t < .006, t / .006, np.exp(-(t - .006) / .035))
        pan = np.full_like(t, .5)
    elif kind == "riser":
        d = .34
        t = np.arange(int(d * SR)) / SR
        s = stft_band(g.normal(0, 1, len(t)), lambda x: 900 * 2 ** (x / d * 2.6), .6) * (t / d) ** 2.2
        pan = np.clip(1 - t / d, 0, 1)                      # right to left, into the cut
    else:   # boom
        d = .5
        t = np.arange(int(d * SR)) / SR
        s = np.sin(2 * np.pi * (70 - 30 * t) * t) * np.exp(-t / .13) + .3 * stft_band(g.normal(0, 1, len(t)), lambda x: 180, .8) * np.exp(-t / .06)
        pan = np.full_like(t, .5)
    s = s / (np.abs(s).max() + 1e-9)
    return np.stack([s * np.cos(pan * np.pi / 2), s * np.sin(pan * np.pi / 2)], 1) * 1.41


def read_wav(p):
    w = wave.open(p)
    sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
    x = np.frombuffer(w.readframes(n), np.int16).astype(np.float32).reshape(-1, ch) / 32768
    if ch == 1:
        x = np.repeat(x, 2, 1)
    return sr, x


def write_wav(p, sr, x):
    w = wave.open(p, "wb")
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
    w.close()


def main():
    ev = json.load(open(os.path.join(ROOT, "plan", "sfx.json")))
    sr, song = read_wav(os.path.join(ROOT, "assets", "audio", "section.wav"))
    os.makedirs(os.path.join(ROOT, "assets", "audio", "sfx"), exist_ok=True)
    cache = {}
    for kind in ("whip", "snap", "riser", "boom"):
        cache[kind] = take(kind, {"whip": 1, "snap": 2, "riser": 3, "boom": 4}[kind])
        write_wav(os.path.join(ROOT, "assets", "audio", "sfx", f"{kind}.wav"), SR, cache[kind] * .5)
    if sr != SR:
        raise SystemExit(f"section.wav is {sr} Hz, expected {SR}")
    mix = song.copy()
    gain_song = np.ones(len(song))
    for e in ev:
        if e["kind"] == "drop":          # the music drops out just before a big hit
            a, b = int((e["t"] - e.get("len", .12)) * SR), int(e["t"] * SR)
            ramp = np.ones(len(song))
            ramp[a:b] = .12
            gain_song = np.minimum(gain_song, ramp)
    mix *= gain_song[:, None]
    for k, e in enumerate(ev):
        if e["kind"] == "drop":
            continue
        s = take(e["kind"], 100 + k)       # a fresh take each time so repeats don't sound copied
        start = int((e["t"] - (s.shape[0] / SR if e["kind"] == "riser" else .004)) * SR)
        a, b = max(0, start), min(len(mix), start + len(s))
        mix[a:b] += s[a - start:b - start] * e.get("gain", .32)
    peak = np.abs(mix).max()
    if peak > .98:
        mix *= .98 / peak
    write_wav(os.path.join(ROOT, "assets", "audio", "section_sfx.wav"), SR, mix)
    print(f"{len(ev)} events, peak {peak:.2f}")


if __name__ == "__main__":
    main()
