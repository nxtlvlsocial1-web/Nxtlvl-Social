# Synthesizes the background music bed into assets/music.wav (nothing to license).
# 96 BPM, Am–F–C–G: soft pads, a plucked arpeggio and a light beat, ducked under the voiceover.
# Run after build.cjs (reads the duration from sfx.json): python3 music.py
import json, os, wave
import numpy as np

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(3)
BPM = 96
BEAT = 60 / BPM
CHORDS = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G (MIDI)


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def tone(f, d, partials=(1, .5, .25), decay=0.0):
    t = np.arange(int(d * SR)) / SR
    x = sum(a * np.sin(2 * np.pi * f * (i + 1) * t) for i, a in enumerate(partials))
    env = np.exp(-t * decay) if decay else np.ones_like(t)
    return x * env * np.minimum(t / 0.01, 1)


def add(mix, x, t, g):
    i = int(t * SR)
    if i >= len(mix):
        return
    n = min(len(x), len(mix) - i)
    mix[i:i + n] += x[:n] * g


def main():
    total = json.load(open(os.path.join(HERE, "sfx.json")))["duration"]
    mix = np.zeros(int(total * SR))
    bar = BEAT * 4
    nbars = int(total / bar) + 1
    for b in range(nbars):
        t0 = b * bar
        ch = CHORDS[b % 4]
        # pad: whole bar, slow swell
        d = bar
        tt = np.arange(int(d * SR)) / SR
        swell = np.sin(np.pi * np.clip(tt / d, 0, 1)) ** 0.6
        pad = sum(tone(hz(m), d, (1, .3, .1)) for m in ch) * swell
        add(mix, pad, t0, 0.05)
        add(mix, tone(hz(ch[0] - 24), d, (1, .4), 1.2), t0, 0.16)  # bass
        # arpeggio, 8th notes
        arp = ch + [ch[0] + 12, ch[2], ch[1], ch[0] + 12, ch[2]]
        for k in range(8):
            add(mix, tone(hz(arp[k] + 12), 0.4, (1, .2), 9), t0 + k * BEAT / 2, 0.05)
        for k in range(4):
            tb = t0 + k * BEAT
            if k in (0, 2):  # kick
                kt = np.arange(int(0.3 * SR)) / SR
                kick = np.sin(2 * np.pi * np.cumsum(50 + 90 * np.exp(-kt * 30)) / SR) * np.exp(-kt * 9)
                add(mix, kick, tb, 0.42)
            else:  # clap
                ct = np.arange(int(0.18 * SR)) / SR
                add(mix, rng.standard_normal(len(ct)) * np.exp(-ct * 22), tb, 0.08)
            for h in (0, 0.5):  # hats
                ht = np.arange(int(0.05 * SR)) / SR
                hat = np.diff(rng.standard_normal(len(ht) + 1)) * np.exp(-ht * 90)
                add(mix, hat, tb + h * BEAT, 0.03)
    # duck under the voiceover
    with wave.open(os.path.join(HERE, "assets", "voiceover.wav")) as f:
        vo = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        vsr = f.getframerate()
    hop = vsr // 100
    env = np.array([np.sqrt((vo[i:i + hop] ** 2).mean()) for i in range(0, len(vo), hop)])
    env = np.convolve(env > 0.02, np.ones(25) / 25, mode="same")  # ~250 ms smoothing
    gain = np.interp(np.arange(len(mix)) / SR, np.arange(len(env)) / 100, 1 - 0.55 * env, right=1.0)
    mix *= gain
    t = np.arange(len(mix)) / SR
    mix *= np.minimum(t / 0.6, 1) * np.clip((total - t) / 1.5, 0, 1)
    mix = np.tanh(mix * 1.2) * 0.8
    pcm = (mix * 32767).astype("<i2")
    with wave.open(os.path.join(HERE, "assets", "music.wav"), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(pcm.tobytes())
    print("wrote assets/music.wav", round(total, 2), "s")


if __name__ == "__main__":
    main()
