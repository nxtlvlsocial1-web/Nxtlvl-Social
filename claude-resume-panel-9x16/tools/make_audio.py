"""Original music bed + synthesized SFX + final mix for the reel. Fully deterministic (seeded).

Usage (from the project root): python3 -I tools/make_audio.py
Inputs : assets/audio/vo.wav, assets/raw/{stamp1,stamp2,buzzer,chime1,chime2}.mp3 (ElevenLabs SFX)
Outputs: assets/audio/music.wav, assets/audio/sfx.wav, assets/audio/mix.wav
"""
import subprocess
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
LEN = 35.6
BPM = 120.0
BEAT = 60.0 / BPM
N = int(LEN * SR)
rng = np.random.default_rng(7)


def t_arr(d):
    return np.arange(int(d * SR)) / SR


def lp(x, f, order=2):
    return sosfilt(butter(order, f, "low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def add(buf, sig, at, gain=1.0):
    i = int(at * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * gain


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    return x / (np.max(np.abs(x)) + 1e-9) * 0.9  # peak-normalize generated SFX


def write(path, x):
    x = np.asarray(x, dtype=np.float32)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", path],
                   input=x.tobytes(), check=True)


def note(n):  # midi -> Hz
    return 440.0 * 2 ** ((n - 69) / 12)


# ---------------------------------------------------------------- instruments
def kick():
    t = t_arr(0.42)
    f = 45 + 95 * np.exp(-t / 0.045)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t / 0.16)
    click = hp(rng.standard_normal(len(t)), 2500) * np.exp(-t / 0.004) * 0.25
    return np.tanh(1.6 * (body + click))


def clap():
    t = t_arr(0.3)
    n = bp(rng.standard_normal(len(t)), 900, 4500)
    env = np.exp(-t / 0.07)
    for d in (0.0, 0.011, 0.022):  # flam
        env += 0.6 * np.exp(-np.clip(t - d, 0, None) / 0.008) * (t >= d)
    return n * env * 0.5


def hat(open_=False):
    t = t_arr(0.25 if open_ else 0.06)
    return hp(rng.standard_normal(len(t)), 7500) * np.exp(-t / (0.08 if open_ else 0.014)) * 0.35


def saw(f, d, detune=0.0):
    t = t_arr(d)
    x = 2 * ((t * f) % 1.0) - 1
    if detune:
        x = 0.5 * x + 0.5 * (2 * ((t * f * (1 + detune)) % 1.0) - 1)
    return x


def pluck(f, d=0.22):
    t = t_arr(d)
    x = saw(f, d, 0.004) + 0.5 * np.sign(np.sin(2 * np.pi * f * 2 * t))
    return lp(x, 3200) * np.exp(-t / 0.09) * 0.22


def bass(f, d):
    t = t_arr(d)
    x = lp(saw(f, d) + 0.6 * np.sin(2 * np.pi * f * t), 420)
    env = np.minimum(1, t / 0.005) * np.exp(-t / 0.35)
    return np.tanh(1.5 * x * env) * 0.55


def pad(freqs, d):
    t = t_arr(d)
    x = sum(saw(f, d, 0.006) for f in freqs) / len(freqs)
    env = np.minimum(1, t / 0.25) * np.minimum(1, (d - t) / 0.3)
    return lp(x, 1500) * env * 0.16


# A minor: Am - F - C - G, one chord per bar (2s)
CHORDS = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [55, 60, 64]), (55, [55, 59, 62])]


def section_gain(t):
    """Arrangement switches, keyed to the voiceover (see STORYBOARD)."""
    return {
        "drums": not (9.5 <= t < 11.0 or 21.0 <= t < 21.75 or 26.6 <= t < 27.9 or 28.45 <= t < 31.0),
        "bass": not (21.0 <= t < 21.75 or 26.6 <= t < 27.9 or 28.45 <= t < 31.0),
        "arp": not (26.6 <= t < 27.9) and t < 35.0,
        "pad": True,
        "hat16": 21.75 <= t < 26.6 or t >= 31.0,
    }


music = np.zeros(N)
drums = np.zeros(N)
K, C = kick(), clap()
kick_times = []
steps = int(LEN / (BEAT / 4))
for s in range(steps):
    t = s * BEAT / 4
    g = section_gain(t)
    beat_pos = s % 4  # 16th within beat
    beat_idx = s // 4
    if t >= 35.0:
        break
    if g["drums"]:
        if beat_pos == 0:
            add(drums, K, t, 0.95)
            kick_times.append(t)
            if beat_idx % 2 == 1:
                add(drums, C, t, 0.8)
        if beat_pos == 2:
            add(drums, hat(open_=(beat_idx % 4 == 3)), t, 0.8)
        elif g["hat16"]:
            add(drums, hat(), t, 0.35)
    bar = int(t // (4 * BEAT))
    root, tri = CHORDS[bar % 4]
    if g["bass"] and beat_pos in (0, 2) and not (beat_pos == 0 and beat_idx % 4 == 0 and False):
        add(music, bass(note(root - 12), BEAT / 2 * 0.95), t, 0.9)
    if g["arp"]:
        seq = [tri[0] + 12, tri[1] + 12, tri[2] + 12, tri[1] + 24]
        add(music, pluck(note(seq[s % 4])), t, 0.55 if g["drums"] else 0.4)

# pads: one per bar, always on (they carry the quiet honesty beat)
for bar in range(int(LEN // (4 * BEAT)) + 1):
    t0 = bar * 4 * BEAT
    root, tri = CHORDS[bar % 4]
    add(music, pad([note(n) for n in tri] + [note(root - 12)], 4 * BEAT), t0, 1.0)

# sidechain pump from the kicks
pump = np.ones(N)
tt = np.arange(N) / SR
for kt in kick_times:
    i = int(kt * SR)
    seg = tt[i:i + int(0.3 * SR)] - kt
    pump[i:i + len(seg)] = np.minimum(pump[i:i + len(seg)], 1 - 0.55 * np.exp(-seg / 0.09))
music *= pump

# riser into the twist, and the big hit on "zero"
def riser(d):
    t = t_arr(d)
    f = 200 * (12 ** (t / d))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.15
    n = hp(rng.standard_normal(len(t)), 1500) * 0.25
    return (tone + n) * (t / d) ** 2


def boom(d=1.6):
    t = t_arr(d)
    f = 38 + 60 * np.exp(-t / 0.08)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.5)
    n = lp(rng.standard_normal(len(t)), 900) * np.exp(-t / 0.25) * 0.4
    return np.tanh(1.4 * (x + n))


add(music, riser(0.85), 20.9, 0.9)
add(music, riser(1.3), 26.6, 0.7)
music = music + drums
music = lp(music, 14000)
music /= np.max(np.abs(music)) + 1e-9
fade = np.minimum(1, (LEN - tt) / 0.6)
music *= np.clip(fade, 0, 1)
write("assets/audio/music.wav", music * 0.9)

# ---------------------------------------------------------------- SFX
def whoosh(d=0.45, up=True):
    t = t_arr(d)
    n = rng.standard_normal(len(t))
    out = np.zeros(len(t))
    bands = 12
    for b in range(bands):
        a, z = b * len(t) // bands, (b + 1) * len(t) // bands
        frac = (b + 0.5) / bands
        fc = 400 * (10 ** (frac if up else 1 - frac))
        out[a:z] = bp(n, fc * 0.6, min(fc * 1.6, 20000))[a:z]
    env = np.sin(np.pi * t / d) ** 2
    return out * env * 0.9


def pop(f=700, d=0.09):
    t = t_arr(d)
    ff = f * (1 + 0.6 * np.exp(-t / 0.01))
    return np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-t / 0.03) * 0.7


def tick(f=2400):
    t = t_arr(0.03)
    return np.sin(2 * np.pi * f * t) * np.exp(-t / 0.006) * 0.6


def typing(d, rate=14):
    out = np.zeros(int(d * SR))
    k = 0.0
    while k < d - 0.04:
        t = t_arr(0.03)
        c = hp(rng.standard_normal(len(t)), 2000) * np.exp(-t / 0.005) * (0.35 + 0.2 * rng.random())
        add(out, c, k)
        k += (1 / rate) * (0.7 + 0.6 * rng.random())
    return out


def scribble(d):
    t = t_arr(d)
    n = bp(rng.standard_normal(len(t)), 2500, 6000)
    wob = 0.5 + 0.5 * np.sin(2 * np.pi * 9 * t) ** 2
    return n * wob * np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.05) * 0.35


def laser(d=0.7):
    t = t_arr(d)
    f = 300 + 1500 * t / d
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.18 * np.sin(np.pi * t / d)


stamp1, stamp2 = decode("assets/raw/stamp1.mp3"), decode("assets/raw/stamp2.mp3")
buzzer = decode("assets/raw/buzzer.mp3")
chime1, chime2 = decode("assets/raw/chime1.mp3"), decode("assets/raw/chime2.mp3")

sfx = np.zeros(N)
add(sfx, boom(1.2), 0.0, 0.45)                       # cold-open hit
for i in range(8):                                   # timer ticks 7.4 -> 0
    add(sfx, tick(2600 if i % 2 else 2100), 0.8 + i * 0.33, 0.8)
add(sfx, stamp1, 3.45, 1.0)                          # REJECTED stamp
for i in range(7):                                   # seven Claudes pop in
    add(sfx, pop(520 + 70 * i), 4.9 + i * 0.1, 0.55)
add(sfx, whoosh(0.4), 5.85, 0.6)                     # -> proof
add(sfx, scribble(0.9), 6.6, 0.8)                    # red pen circles
add(sfx, stamp2, 8.72, 1.0)                          # Rejected.
add(sfx, buzzer, 8.82, 0.55)
add(sfx, whoosh(0.5), 9.3, 0.6)                      # -> open loop
add(sfx, whoosh(0.35, up=False), 10.9, 0.5)
add(sfx, pop(880), 11.25, 0.6)                       # #1 badge
add(sfx, laser(0.9), 12.2, 1.0)                      # scanner sweep
add(sfx, pop(1200, 0.12), 13.8, 0.5)                 # "HUMAN?" light
add(sfx, whoosh(0.4), 13.85, 0.6)                    # -> manager
add(sfx, pop(880), 14.05, 0.6)                       # #2 badge
add(sfx, pop(660), 15.4, 0.55)                       # INTERVIEW button
add(sfx, whoosh(0.35, up=False), 16.55, 0.6)         # BIN
add(sfx, whoosh(0.4), 16.95, 0.6)                    # -> five readers
for i in range(5):
    add(sfx, pop(600 + 90 * i), 17.45 + i * 0.16, 0.55)
add(sfx, pop(1000, 0.12), 19.1, 0.55)                # rival applicant
add(sfx, pop(1100, 0.12), 21.0, 0.6)                 # CEO
add(sfx, buzzer, 21.3, 0.35)
add(sfx, boom(1.0), 21.75, 0.5)                      # THE TWIST
add(sfx, typing(1.1, 18), 23.45, 0.7)                # Claude rewrites
for i in range(4):                                   # red circles vanish
    add(sfx, pop(900 + 120 * i, 0.07), 24.8 + i * 0.3, 0.5)
for i in range(7):                                   # counter 7 -> 0
    add(sfx, tick(1800 + 100 * i), 26.62 + i * 0.18, 0.7)
add(sfx, boom(1.4), 27.9, 0.45)                       # zero.
add(sfx, chime2, 27.92, 0.9)
add(sfx, whoosh(0.6, up=False), 28.35, 0.35)         # calm beat
add(sfx, whoosh(0.4), 30.95, 0.5)                    # -> CTA
add(sfx, typing(0.6, 16), 31.35, 0.8)                # types RESUME
add(sfx, pop(760), 32.25, 0.7)                       # Post tap
add(sfx, chime1, 33.6, 0.5)
sfx /= max(1.0, np.max(np.abs(sfx)) * 1.05)
write("assets/audio/sfx.wav", sfx)

# ---------------------------------------------------------------- mix
subprocess.run([
    "ffmpeg", "-v", "error", "-y",
    "-i", "assets/audio/vo.wav", "-i", "assets/audio/music.wav", "-i", "assets/audio/sfx.wav",
    "-filter_complex",
    "[0:a]apad=whole_dur=35.6,asplit=2[vo][key];"
    "[1:a]volume=0.32[mus];"
    "[mus][key]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=250[duck];"
    "[2:a]volume=0.75[fx];"
    "[vo][duck][fx]amix=inputs=3:normalize=0:duration=first,"
    "loudnorm=I=-14:TP=-1.0:LRA=9,atrim=0:35.6[out]",
    "-map", "[out]", "-ar", str(SR), "-ac", "2", "assets/audio/mix.wav"], check=True)
print("wrote music.wav, sfx.wav, mix.wav")
