"""Original music for the Nxtlvl brand film, composed in code.

120 BPM, 4/4, A minor -> C major, 32 s exactly (16 bars). The arrangement follows STORYBOARD.md:
  bars 0-1   (0-4 s)    intro: filtered pad, ticking hats, muted pluck, riser into the drop
  bars 2-4   (4-10 s)   drop A: four-on-the-floor, sub bass, clap, bright pluck arpeggio (design)
  bars 5-7   (10-16 s)  groove B: + offbeat chord stabs, 16th hats, bell top line (reels)
  bars 8-10  (16-22 s)  lift: pads open, filter sweep, riser and snare roll into the impact (website)
  bar 11     (22-24 s)  impact on C major, half-time (automation)
  bar 12     (24-26 s)  half-time groove holds
  bars 13-15 (26-32 s)  outro: F -> C, bell at 27.5 s for the star strike, tail to silence

Usage: python3 tools/compose_music.py  ->  assets/music/nxtlvl-brand.wav, beatgrid.json
Everything is deterministic (fixed random seed), so the track re-renders identically.
"""
import json
import os

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, sosfilt

SR = 44100
BPM = 120
BEAT = 60 / BPM          # 0.5 s
BAR = 4 * BEAT           # 2 s
LENGTH = 32.0
N = int(SR * LENGTH)
rng = np.random.default_rng(7)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'assets', 'music')


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def track():
    return np.zeros((2, N))


def place(buf, sig, t, gain=1.0, pan=0.0):
    """Add a mono or stereo signal at time t (seconds) with equal-power pan."""
    i = int(round(t * SR))
    if i >= N:
        return
    if sig.ndim == 1:
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        sig = np.vstack([sig * l, sig * r]) * np.sqrt(2)
    n = min(sig.shape[1], N - i)
    buf[:, i:i + n] += sig[:, :n] * gain


def env_ar(n, a, r, sustain=1.0):
    t = np.arange(n) / SR
    e = np.minimum(1.0, t / max(a, 1e-4))
    return e * np.exp(-t / r) * sustain


def lp(x, f, order=2):
    return sosfilt(butter(order, min(f, SR * 0.45), 'low', fs=SR, output='sos'), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, 'high', fs=SR, output='sos'), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], 'band', fs=SR, output='sos'), x)


# ---------------------------------------------------------------- instruments
def kick(dur=0.45):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 54 + 120 * np.exp(-t / 0.03)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t / 0.2)
    click = hp(rng.standard_normal(n), 2500) * np.exp(-t / 0.004) * 0.35
    return np.tanh(1.6 * (body + click))


def clap():
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    noise = bp(rng.standard_normal(n), 900, 3800)
    e = np.zeros(n)
    for k, d in enumerate([0.0, 0.011, 0.022]):
        i = int(d * SR)
        e[i:] += np.exp(-(t[: n - i]) / (0.006 if k < 2 else 0.12))
    return noise * e * 0.6


def snare(gain=1.0):
    n = int(0.22 * SR)
    t = np.arange(n) / SR
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05)
    noise = hp(rng.standard_normal(n), 1800) * np.exp(-t / 0.07)
    return (0.5 * tone + 0.55 * noise) * gain


def hat(open_=False):
    n = int((0.3 if open_ else 0.06) * SR)
    t = np.arange(n) / SR
    x = hp(rng.standard_normal(n), 7500, 4)
    return x * np.exp(-t / (0.09 if open_ else 0.014)) * 0.32


def saw_additive(f, n, decay_base, decay_per_h, bright=1.0, detune_cents=(0,)):
    """Band-limited saw: harmonics decay faster the higher they are (a natural pluck)."""
    t = np.arange(n) / SR
    out = np.zeros(n)
    for dc in detune_cents:
        ff = f * 2 ** (dc / 1200)
        kmax = int((SR * 0.45) // ff)
        ph0 = rng.uniform(0, 2 * np.pi)
        for k in range(1, min(kmax, 60) + 1):
            amp = (1 / k) * np.exp(-((k - 1) / (12 * bright)) ** 1.3)
            out += amp * np.sin(2 * np.pi * k * ff * t + ph0 * k) * np.exp(-t * (decay_base + decay_per_h * k))
    return out / len(detune_cents)


def pluck(midi, dur=0.32, bright=1.0):
    n = int(dur * SR)
    x = saw_additive(hz(midi), n, 6.0, 1.6, bright, (-6, 6))
    return x * env_ar(n, 0.002, 10) * 0.5


def stab(midis, dur=0.22):
    n = int(dur * SR)
    x = sum(saw_additive(hz(m), n, 9.0, 1.2, 1.4, (-9, 0, 9)) for m in midis)
    return x * env_ar(n, 0.003, 10) * 0.28


def bell(midi, dur=2.2):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = hz(midi)
    mod = 2.2 * np.exp(-t / 0.5) * np.sin(2 * np.pi * f * 3.5 * t)
    x = np.sin(2 * np.pi * f * t + mod) * np.exp(-t / 0.9)
    x += 0.3 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t / 0.35)
    return x * env_ar(n, 0.002, 10) * 0.32


def pad(midis, dur, cutoff=2400, attack=0.35, release=0.6):
    n = int((dur + release) * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for m in midis:
        f = hz(m)
        for dc in (-14, -6, 0, 7, 15):
            ff = f * 2 ** (dc / 1200)
            kmax = int(min(cutoff * 1.6, SR * 0.45) // ff)
            ph0 = rng.uniform(0, 2 * np.pi, size=kmax + 1)
            for k in range(1, kmax + 1):
                roll = 1 / (1 + (k * ff / cutoff) ** 4)
                x += (roll / k) * np.sin(2 * np.pi * k * ff * t + ph0[k])
    x /= 5 * len(midis)
    e = np.minimum(1, t / attack) * np.where(t < dur, 1.0, np.exp(-(t - dur) / (release / 3)))
    return x * e * 0.55


def sub(midi, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = hz(midi)
    x = np.sin(2 * np.pi * f * t) + 0.18 * np.sin(4 * np.pi * f * t)
    e = np.minimum(1, t / 0.01) * np.minimum(1, (dur - t) / 0.03).clip(0, 1)
    return np.tanh(1.3 * x) * e * 0.55


def riser(dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    # time-varying one-pole lowpass: cutoff sweeps 300 Hz -> 9 kHz
    fc = 300 * (9000 / 300) ** (t / dur)
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.zeros(n)
    acc = 0.0
    for i in range(n):
        acc = a[i] * acc + (1 - a[i]) * noise[i]
        y[i] = acc
    tone = np.sin(2 * np.pi * np.cumsum(220 * 2 ** (2 * t / dur)) / SR) * 0.15
    return (hp(y, 200) * 0.9 + tone) * (t / dur) ** 2.2 * 0.55


def impact():
    n = int(2.4 * SR)
    t = np.arange(n) / SR
    f = 30 + 60 * np.exp(-t / 0.18)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.9)
    crash = hp(rng.standard_normal(n), 3500) * np.exp(-t / 0.7) * 0.22
    return np.tanh(1.4 * boom) * 0.9 + crash


# ---------------------------------------------------------------- arrangement
AM, F, C, G = 'Am', 'F', 'C', 'G'
CHORDS = {AM: (45, [57, 60, 64, 69]), F: (41, [57, 60, 65, 69]), C: (48, [55, 60, 64, 67]), G: (43, [55, 59, 62, 67])}
PROG = [AM, F, AM, F, C, G, AM, F, C, G, AM, C, C, F, C, C]   # bars 0..15

drums, bass, music, verb_send = track(), track(), track(), track()


def bar_t(b, beat=0.0):
    return b * BAR + beat * BEAT


# intro (bars 0-1): pad Am -> F filtered, ticking 8th hats, muted pluck motif
for b in (0, 1):
    root, voicing = CHORDS[PROG[b]]
    p = pad(voicing, BAR, cutoff=1250, attack=0.05 if b == 0 else 0.3)
    place(music, p, bar_t(b), 0.95, -0.1); place(verb_send, p, bar_t(b), 0.35)
    for e in range(8):
        place(drums, hat(), bar_t(b, e * 0.5), 0.85 if e % 2 else 0.55, 0.25)
    motif = [69, 72, 76, 72, 69, 72, 76, 79] if b == 0 else [69, 72, 77, 72, 69, 72, 77, 81]
    for e, m in enumerate(motif):
        place(music, pluck(m, 0.25, bright=0.45), bar_t(b, e * 0.5), 0.9, 0.2 if e % 2 else -0.2)
        place(verb_send, pluck(m, 0.25, bright=0.45), bar_t(b, e * 0.5), 0.3)
rs = riser(1.5)
place(music, rs, 2.5, 0.75); place(verb_send, rs, 2.5, 0.3)

# main body (bars 2-10): drop A (2-4), groove B (5-7), lift (8-10)
ARP = [0, 7, 12, 16, 12, 7, 19, 12]
LAST = 10
for b in range(2, LAST + 1):
    name = PROG[b]
    root, voicing = CHORDS[name]
    groove = b >= 5
    lift = b >= 8
    for beat in range(4):
        if b == LAST and beat >= 2:
            continue                              # kick drops out for the last half bar of the build
        place(drums, kick(), bar_t(b, beat), 0.72)
    for beat in (1, 3):
        if b < LAST:
            place(drums, clap(), bar_t(b, beat), 0.8, 0.05); place(verb_send, clap(), bar_t(b, beat), 0.25)
    steps = 16 if groove else 8
    for s in range(steps):
        pos = s * (4 / steps)
        if b == LAST and pos >= 2:
            continue
        is_off = (pos % 1) == 0.5
        place(drums, hat(open_=is_off and not groove), bar_t(b, pos), 0.5 if is_off else 0.32, 0.3)
    for e in range(8):
        if e % 2 == 1:
            place(bass, sub(root - 12 if root >= 45 else root, BEAT * 0.48), bar_t(b, e * 0.5), 0.95)
    bright = 1.15 if not groove else 1.3
    if lift:
        bright = 1.2 + (b - 8 + 0.5) * 0.35
    for s in range(16):
        m = voicing[0] + ARP[s % 8] + (12 if (lift and s % 4 == 3) else 0)
        place(music, pluck(m, 0.24, bright), bar_t(b, s * 0.25), 0.36, -0.35 if s % 2 else 0.35)
        place(verb_send, pluck(m, 0.24, bright), bar_t(b, s * 0.25), 0.12)
    cutoff = 1300 if not lift else 1300 + (b - 7) * 1100
    p = pad(voicing, BAR, cutoff=cutoff, attack=0.08)
    place(music, p, bar_t(b), 0.55); place(verb_send, p, bar_t(b), 0.3)
    if groove:
        for pos in (0.5, 1.5, 2.5, 3.25):
            if b == LAST and pos >= 2:
                continue
            place(music, stab(voicing), bar_t(b, pos), 0.65, 0.0); place(verb_send, stab(voicing), bar_t(b, pos), 0.25)
    if 5 <= b <= 7:
        line = {AM: [76, 79, 81], F: [77, 76, 72], C: [76, 79, 84], G: [79, 81, 83]}[name]
        for k, m in enumerate(line):
            place(music, bell(m, 1.4), bar_t(b, [0, 1.5, 3][k]), 0.42, 0.25 * (k - 1)); place(verb_send, bell(m, 1.4), bar_t(b, [0, 1.5, 3][k]), 0.4)

# lift: noise riser over the last two bars, accelerating snare roll in the last bar (20-22 s)
rs = riser(4.0)
place(music, rs, 18.0, 0.6); place(verb_send, rs, 18.0, 0.25)
roll_times = []
t = 20.0
step = BEAT / 2
while t < 22.0 - 1e-6:
    roll_times.append(t)
    if t >= 21.0:
        step = BEAT / 4
    if t >= 21.5:
        step = BEAT / 8
    t += step
for k, rt in enumerate(roll_times):
    place(drums, snare(0.35 + 0.6 * k / len(roll_times)), rt, 0.8, 0.1)

# payoff (bars 11-12, 22-26 s): impact on C, half-time kick, big open pad
place(drums, impact(), 22.0, 0.9); place(verb_send, impact(), 22.0, 0.2)
for b in (11, 12):
    root, voicing = CHORDS[C]
    for beat in (0, 2):
        place(drums, kick(), bar_t(b, beat), 0.95 if b == 11 else 0.8)
    place(drums, clap(), bar_t(b, 2), 0.7); place(verb_send, clap(), bar_t(b, 2), 0.35)
    for s in range(8):
        place(drums, hat(open_=(s % 2 == 1)), bar_t(b, s * 0.5), 0.3, 0.3)
    p = pad(voicing + [72, 76], BAR + 0.2, cutoff=5200 if b == 11 else 3800, attack=0.01 if b == 11 else 0.2)
    place(music, p, bar_t(b), 0.85 if b == 11 else 0.7); place(verb_send, p, bar_t(b), 0.45)
    place(bass, sub(36, BAR + 0.06), bar_t(b), 1.0 if b == 11 else 0.8)
    for s, m in enumerate([60, 64, 67, 72, 76, 72, 67, 64]):
        place(music, pluck(m, 0.3, 1.5), bar_t(b, s * 0.5), 0.4 if b == 11 else 0.3, -0.3 if s % 2 else 0.3); place(verb_send, pluck(m, 0.3, 1.5), bar_t(b, s * 0.5), 0.2)

# outro (bars 13-15, 26-32 s): F -> C -> C, bell for the star strike at 27.5 s, tail to silence
for b, name in ((13, F), (14, C), (15, C)):
    root, voicing = CHORDS[name]
    p = pad(voicing + ([69] if name == F else [72]), BAR, cutoff=3200 if b < 15 else 2200, attack=0.25, release=1.2)
    place(music, p, bar_t(b), 0.75 if b < 15 else 0.55); place(verb_send, p, bar_t(b), 0.5)
    place(bass, sub(root - 12 if root >= 45 else root, BAR + (0.06 if b < 15 else -0.4)), bar_t(b), 0.6 if b < 15 else 0.4)
place(drums, kick(), bar_t(13), 0.75)
place(drums, kick(), bar_t(14), 0.6)
for m, tt, g in ((84, 27.5, 0.55), (88, 27.5, 0.3), (91, 28.0, 0.25), (84, 28.5, 0.35), (79, 30.0, 0.22)):
    place(music, bell(m, 2.6), tt, g, 0.1); place(verb_send, bell(m, 2.6), tt, g * 1.1)

# ---------------------------------------------------------------- mix
t = np.arange(N) / SR
kick_times = [bar_t(b, k) for b in range(2, 11) for k in range(4) if not (b == 10 and k >= 2)] + [22.0, 23.0, 24.0, 25.0, 26.0, 28.0]
duck = np.ones(N)
for kt in kick_times:
    i = int(kt * SR)
    seg = np.arange(N - i) / SR
    n = min(len(seg), int(0.4 * SR))
    duck[i:i + n] = np.minimum(duck[i:i + n], 1 - 0.62 * np.exp(-seg[:n] / 0.11))

# synthetic stereo hall: decaying, slightly different noise per side
ir_n = int(2.2 * SR)
ir_t = np.arange(ir_n) / SR
ir = np.vstack([rng.standard_normal(ir_n), rng.standard_normal(ir_n)]) * np.exp(-ir_t / 0.55)
ir = np.vstack([lp(ir[0], 6000), lp(ir[1], 6000)])
ir[:, : int(0.012 * SR)] = 0
ir /= np.abs(ir).sum(axis=1, keepdims=True) ** 0.5 * 30
wet = np.vstack([fftconvolve(hp(verb_send[0], 250), ir[0])[:N], fftconvolve(hp(verb_send[1], 250), ir[1])[:N]])

bass = np.vstack([hp(bass[0], 32), hp(bass[1], 32)])
music = music + 0.45 * np.vstack([hp(music[0], 2200), hp(music[1], 2200)])   # presence lift on the melodic parts
bus = drums * 0.8 + (bass * duck) * 0.36 + (music * duck) * 1.5 + wet * 0.7 * duck
bus = np.vstack([hp(bus[0], 32), hp(bus[1], 32)])
# glue: gentle saturation, then a simple peak limiter and loudness target
bus = np.tanh(bus * 1.15) / np.tanh(1.15)
rms = np.sqrt(np.mean(bus ** 2))
bus *= 0.165 / rms                                   # about -14 LUFS integrated, a streaming-friendly level
peak = np.max(np.abs(bus))
if peak > 0.8:
    bus = np.tanh(bus / 0.8) * 0.8                    # soft ceiling ~ -2 dBFS, headroom for AAC
# fade the last 1.2 s so the tail lands on silence at exactly 32 s
fade = np.ones(N)
fn = int(1.2 * SR)
fade[-fn:] = np.linspace(1, 0, fn) ** 2
bus *= fade

os.makedirs(OUT, exist_ok=True)
sf.write(os.path.join(OUT, 'nxtlvl-brand.wav'), bus.T.astype(np.float32), SR, subtype='PCM_16')

grid = {
    "bpm": BPM, "beat_s": BEAT, "bar_s": BAR, "length_s": LENGTH, "key": "A minor -> C major",
    "beats": [round(i * BEAT, 3) for i in range(int(LENGTH / BEAT))],
    "bars": [round(i * BAR, 3) for i in range(int(LENGTH / BAR))],
    "sections": [
        {"name": "intro", "start": 0.0, "end": 4.0},
        {"name": "drop-a", "start": 4.0, "end": 10.0},
        {"name": "groove-b", "start": 10.0, "end": 16.0},
        {"name": "lift", "start": 16.0, "end": 22.0},
        {"name": "impact", "start": 22.0, "end": 26.0},
        {"name": "outro", "start": 26.0, "end": 32.0},
    ],
    "hits": {"drop": 4.0, "impact": 22.0, "star_bell": 27.5, "riser_into_drop": [2.5, 4.0], "riser_into_impact": [18.0, 22.0], "snare_roll": [20.0, 22.0]},
    "kicks": [round(k, 3) for k in sorted(kick_times)],
}
json.dump(grid, open(os.path.join(OUT, 'beatgrid.json'), 'w'), indent=1)
print('peak', round(float(np.max(np.abs(bus))), 3), 'rms', round(float(np.sqrt(np.mean(bus ** 2))), 3))
