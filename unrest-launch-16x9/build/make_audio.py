"""Generate the Unrest launch music bed and SFX track (fully synthesized, no samples).

120 BPM, A minor. Every section cut in the brief lands on a beat:
  0.0-2.0 hook (intro + riser), 2.0 drop, groove to 12.875, gap, 13.0 reveal impact, pad to 15.0.
Outputs (48 kHz, 16-bit stereo WAV): assets/audio/music.wav, assets/audio/sfx.wav

Run: python3 build/make_audio.py   (needs numpy)
"""
import os
import wave

import numpy as np

SR = 48000
DUR = 15.0
N = int(SR * DUR)
BPM = 120
BEAT = 60 / BPM
DROP = 2.0
GROOVE_END = 12.875
REVEAL = 13.0
rng = np.random.default_rng(1129)  # seeded: identical output every run

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "audio")


def buf():
    return np.zeros((N, 2))


def t_axis(d):
    return np.arange(int(SR * d)) / SR


def place(dst, sig, t0, gain=1.0, pan=0.0):
    """Mix mono or stereo `sig` into stereo `dst` at t0 seconds."""
    i = int(round(t0 * SR))
    if i >= N:
        return
    if sig.ndim == 1:
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        sig = np.stack([sig * l * 1.414, sig * r * 1.414], 1)
    j = min(N, i + len(sig))
    dst[i:j] += sig[: j - i] * gain


def onepole_lp(x, fc):
    """Time-varying one-pole lowpass; fc may be scalar or per-sample array."""
    fc = np.broadcast_to(np.asarray(fc, float), x.shape)
    a = 1 - np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x)
    s = 0.0
    for n in range(len(x)):
        s += a[n] * (x[n] - s)
        y[n] = s
    return y


def fft_filter(x, lo=None, hi=None):
    """Static zero-phase band filter via FFT (fast)."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.ones_like(f)
    if lo:
        m *= 1 / (1 + (lo / np.maximum(f, 1)) ** 4)
    if hi:
        m *= 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * m, len(x))


def noise(d):
    return rng.standard_normal(int(SR * d))


def env_exp(d, tau, attack=0.002):
    t = t_axis(d)
    return np.minimum(1, t / attack) * np.exp(-t / tau)


def note(n):  # MIDI note -> Hz
    return 440 * 2 ** ((n - 69) / 12)


def saw(freq, d, detune=0.0):
    t = t_axis(d)
    ph = (t * freq * (1 + detune)) % 1
    return 2 * ph - 1


# ---------------------------------------------------------------- instruments

def kick(hard=1.0):
    d = 0.45
    t = t_axis(d)
    f = 45 + 110 * np.exp(-t / 0.035)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(d, 0.16)
    click = fft_filter(noise(d), lo=2500) * env_exp(d, 0.004) * 0.5
    return np.tanh((body + click) * 1.6 * hard)


def clap():
    d = 0.3
    n = fft_filter(noise(d), lo=900, hi=4500)
    e = np.zeros(int(SR * d))
    for k, off in enumerate([0, 0.011, 0.022]):
        e += np.roll(env_exp(d, 0.006), int(off * SR)) * (0.8 + 0.1 * k)
    e += np.roll(env_exp(d, 0.09), int(0.026 * SR)) * 0.7
    return n * e * 0.5


def hat(open_=False):
    d = 0.25 if open_ else 0.06
    return fft_filter(noise(d), lo=7000) * env_exp(d, 0.07 if open_ else 0.012) * 0.35


def bass(n, d=0.22):
    f = note(n)
    s = 0.6 * saw(f, d) + 0.4 * np.sin(2 * np.pi * f * t_axis(d))
    s = onepole_lp(s, 380 + 900 * np.exp(-t_axis(d) / 0.04))
    return np.tanh(s * 2.2) * env_exp(d, 0.12, 0.003) * 0.55


def stab(notes, d=0.32, bright=2600):
    s = sum(saw(note(n), d, dt) for n in notes for dt in (-0.006, 0.006))
    s = onepole_lp(s / (2 * len(notes)), bright * np.exp(-t_axis(d) / 0.09) + 300)
    return s * env_exp(d, 0.13, 0.002) * 0.9


def pad(notes, d, tau=1.4):
    t = t_axis(d)
    s = sum(np.sin(2 * np.pi * note(n) * t) + 0.3 * np.sin(2 * np.pi * note(n) * 2.003 * t) for n in notes)
    e = np.minimum(1, t / 0.03) * np.exp(-t / tau)
    return s / len(notes) * e * 0.5


def boom(d=1.6, f0=70, f1=32):
    t = t_axis(d)
    f = f1 + (f0 - f1) * np.exp(-t / 0.25)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(d, 0.55, 0.003)
    hit = fft_filter(noise(d), hi=2500) * env_exp(d, 0.08) * 0.6
    return np.tanh((body + hit) * 1.8) * 0.9


def crash(d=1.4):
    return fft_filter(noise(d), lo=4000) * env_exp(d, 0.45, 0.001) * 0.35


def riser(d, f0=300, f1=7000, rise=2.2):
    t = t_axis(d)
    x = t / d
    fc = f0 * (f1 / f0) ** x
    n = onepole_lp(noise(d), fc) - onepole_lp(noise(d), fc * 0.35)
    tone = saw(1, d) * 0  # placeholder for shape below
    ph = np.cumsum(note(57) * (1 + 3 * x ** rise)) / SR
    tone = (2 * (ph % 1) - 1) * 0.12
    amp = x ** 1.6
    return (n * 0.9 + onepole_lp(tone, 1800)) * amp


def whoosh(d=0.45, f0=500, f1=5000, peak=0.5):
    t = t_axis(d)
    x = t / d
    fc = f0 * (f1 / f0) ** x
    n = onepole_lp(noise(d), fc) - onepole_lp(noise(d), fc * 0.25)
    amp = np.where(x < peak, (x / peak) ** 2, ((1 - x) / (1 - peak)) ** 1.5)
    return n * amp * 1.2


def pop(f0=1100, f1=320, d=0.09):
    t = t_axis(d)
    f = f1 + (f0 - f1) * np.exp(-t / 0.018)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(d, 0.03, 0.001) * 0.6


def click(bright=3500):
    d = 0.03
    return (fft_filter(noise(d), lo=bright) * env_exp(d, 0.003, 0.0005)
            + np.sin(2 * np.pi * 2200 * t_axis(d)) * env_exp(d, 0.004, 0.0005) * 0.4) * 0.7


def thud(d=0.35):
    t = t_axis(d)
    f = 48 + 70 * np.exp(-t / 0.03)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(d, 0.09, 0.001)
    return np.tanh((body + fft_filter(noise(d), hi=1800) * env_exp(d, 0.025) * 0.8) * 1.5) * 0.9


def tick():
    d = 0.02
    return fft_filter(noise(d), lo=5000) * env_exp(d, 0.002, 0.0003) * 0.5


# ---------------------------------------------------------------- music

music = buf()
duck = np.ones(N)  # sidechain envelope from the kick

# intro: dot pulse, ring, word ticks, riser into the "boring?" hit
place(music, boom(0.9, 90, 40) * 0.55, 0.0)
place(music, riser(1.45, 250, 5000, 2.0) * 0.55, 0.05, pan=0.0)
for i, w in enumerate([0.40, 0.58, 0.76, 0.98, 1.18]):
    place(music, kick(0.5) * 0.35, w)
place(music, boom(1.2, 80, 30), 1.5)
place(music, crash(1.0) * 0.6, 1.5)
place(music, pad([45, 52, 57, 60], 0.5, 0.25) * 0.5, 1.5)

# groove
beats = np.arange(DROP, GROOVE_END - 1e-6, BEAT)
progression = [  # per bar (2 s): bass root, stab chord
    (45, [57, 60, 64]),  # Am
    (41, [57, 60, 65]),  # F
    (43, [55, 59, 62]),  # G
    (40, [55, 59, 64]),  # Em
]
for k, b in enumerate(beats):
    place(music, kick(1.15 if k == 0 else 1.0) * 0.9, b)
    t = np.arange(N) / SR
    i0 = int(b * SR)
    seg = slice(i0, min(N, i0 + int(0.3 * SR)))
    duck[seg] = np.minimum(duck[seg], 1 - 0.65 * np.exp(-(t[seg] - b) / 0.11))
    bar = int((b - DROP) // (4 * BEAT))
    root, chord = progression[bar % 4]
    beat_in_bar = int(round((b - DROP) / BEAT)) % 4
    if beat_in_bar in (1, 3):
        place(music, clap() * 0.8, b, pan=0.05)
    place(music, hat(True) * 0.55, b + BEAT / 2, pan=0.25)
    for s in range(4):
        place(music, hat() * (0.5 if s % 2 else 0.3), b + s * BEAT / 4, pan=-0.3)
    place(music, bass(root + (12 if beat_in_bar == 3 else 0)), b + BEAT / 2)
    place(music, bass(root, 0.12) * 0.6, b + BEAT * 0.75)
    if beat_in_bar == 0:
        place(music, stab(chord) * 0.6, b, pan=-0.15)
        place(music, stab(chord) * 0.45, b + 0.012, pan=0.15)
    if beat_in_bar == 2 and bar % 2 == 1:
        place(music, stab(chord, 0.2) * 0.4, b + BEAT * 0.5)

place(music, crash(1.6) * 0.8, DROP)
place(music, boom(1.4, 85, 35) * 0.8, DROP)

# build into the reveal: clap roll + riser
roll = list(np.arange(11.0, 12.0, BEAT / 2)) + list(np.arange(12.0, GROOVE_END - 1e-6, BEAT / 4))
for i, r in enumerate(roll):
    place(music, clap() * (0.25 + 0.5 * i / len(roll)), r, pan=(-0.2 if i % 2 else 0.2))
place(music, riser(1.85, 400, 9000, 1.8) * 0.75, 11.0)

# hard gap 12.875-13.0, then the reveal
music[int(GROOVE_END * SR):int(REVEAL * SR)] *= np.linspace(1, 0, int(REVEAL * SR) - int(GROOVE_END * SR))[:, None] ** 3
place(music, boom(2.0, 75, 30) * 1.1, REVEAL)
place(music, crash(2.0) * 0.7, REVEAL)
place(music, pad([45, 52, 57, 59, 64], 2.0, 1.6) * 0.9, REVEAL)
place(music, pad([69, 76], 2.0, 1.0) * 0.25, REVEAL + 0.02, pan=0.3)
place(music, kick(0.8) * 0.7, 14.5)
place(music, pad([57, 64, 69], 0.5, 0.35) * 0.35, 14.5)

# sidechain pump on the tonal layers is approximated by ducking the whole groove bus lightly
music *= (0.55 + 0.45 * duck)[:, None]

# ---------------------------------------------------------------- sfx

sfx = buf()
# hook
place(sfx, pop(1500, 600, 0.12) * 0.7, 0.05)                     # dot pulse
place(sfx, whoosh(0.4, 600, 6000, 0.35) * 0.5, 0.2)              # ring expands
for w in [0.40, 0.58, 0.76, 0.98, 1.18]:
    place(sfx, click(3000) * 0.9, w)                               # word slams
place(sfx, thud(0.45) * 0.9, 1.5)                                 # "boring?" lands
for f in [1.70, 1.80]:
    place(sfx, tick() * 1.2, f)                                    # solid/outline flicker
place(sfx, whoosh(0.3, 3000, 400, 0.8) * 0.5, 1.72)               # suck-in before the drop
# discover: icon pops and morphs
for k, b in enumerate([2.0, 2.5, 3.0, 3.5]):
    place(sfx, pop(1300 - 120 * k, 380, 0.1) * 0.75, b, pan=-0.1 + 0.07 * k)
    place(sfx, whoosh(0.22, 2500, 900, 0.4) * 0.25, b + 0.3)
place(sfx, tick() * 1.3, 4.0)                                      # outline flip
place(sfx, whoosh(0.35, 400, 5000, 0.85) * 0.6, 4.68)             # out to connect
# connect: dots pop, lines tick, collapse, bubbles, doors
for i in range(12):
    place(sfx, pop(2400 + 90 * (i % 5), 1300, 0.04) * 0.3, 5.0 + i * 0.025, pan=((i * 37) % 11 - 5) / 6)
for i in range(16):
    place(sfx, tick() * 0.8, 5.30 + i * 0.045, pan=((i * 53) % 9 - 4) / 5)
place(sfx, whoosh(0.3, 4000, 500, 0.7) * 0.6, 5.95)               # network collapses
place(sfx, pop(900, 300, 0.12) * 0.8, 6.25, pan=-0.4)
place(sfx, pop(1100, 350, 0.12) * 0.8, 6.30, pan=0.4)
place(sfx, thud(0.25) * 0.7, 6.5)                                  # doors shut
place(sfx, whoosh(0.4, 300, 3000, 0.25) * 0.7, 6.75)              # doors slide open
# experience
for i in range(8):
    place(sfx, pop(700 + 40 * i, 250, 0.06) * 0.35, 8.0 + i * 0.05, pan=(i - 3.5) / 4)
place(sfx, whoosh(0.4, 300, 2500, 0.5) * 0.5, 8.45)               # stage rises
place(sfx, boom(0.9, 110, 45) * 0.6, 9.0)                          # burst
place(sfx, whoosh(0.5, 800, 9000, 0.15) * 0.6, 9.0)
place(sfx, thud(0.4) * 1.0, 10.0)                                   # ticket stamp
place(sfx, click(1500) * 0.8, 10.0)
place(sfx, tick() * 1.2, 10.5)
# recap slams
for k, b in enumerate([11.0, 11.5, 12.0, 12.5]):
    place(sfx, thud(0.3) * 0.85, b)
    place(sfx, click(2500) * 0.8, b)
    place(sfx, tick() * 1.1, b + 0.25)
place(sfx, whoosh(0.4, 7000, 300, 0.9) * 0.8, 12.6)               # everything collapses to the dot
# reveal
place(sfx, pop(1800, 700, 0.12) * 0.6, 13.0)
for i in range(18):                                                 # tagline types
    place(sfx, click(4000 + 200 * (i % 4)) * 0.45, 13.40 + i * 0.025, pan=((i * 29) % 7 - 3) / 6)
place(sfx, pop(1400, 500, 0.08) * 0.5, 13.5)                        # url line
place(sfx, whoosh(0.3, 500, 2000, 0.3) * 0.25, 14.4)                # logo pulse

# ---------------------------------------------------------------- master + write


def master(x, peak_db=-1.0):
    x = np.tanh(x * 1.1)
    fade = int(0.12 * SR)
    x[-fade:] *= np.linspace(1, 0, fade)[:, None]
    x[:int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))[:, None]
    return x / np.max(np.abs(x)) * 10 ** (peak_db / 20)


def write(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


os.makedirs(OUT, exist_ok=True)
write(os.path.join(OUT, "music.wav"), master(music, -1.5))
write(os.path.join(OUT, "sfx.wav"), master(sfx, -2.0))
print("wrote", OUT)
