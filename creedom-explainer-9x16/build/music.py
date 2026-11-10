"""Original music for the Creedom explainer, synthesised from scratch (no samples, no library: ours to use).
Bright, playful tech-pop at 120 BPM in A major, built around the voiceover (plan/vo_tight.json):
  0.0  punchy start: impact + full groove (kick, offbeat hats, bass, plucked arp)  - the hook
 10.5  tension: half-time, filtered, a ticking clock (the reel being watched second by second)
 13.2  a tape-stop on "dropped", then sparse ticks, a riser into ...
 17.2  the drop: claps, chord stabs, bell lead (new hooks, fixes, the free audit)
 31.3  a one-bar break and riser ...
 32.3  the CTA: everything back with a bell melody
 35.4  the logo: a big final chord and a shimmer that fades.
Writes assets/audio/music.wav (48 kHz stereo).  python3 build/music.py
"""
import os
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
DUR = 37.6
BPM = 120.0
BEAT = 60.0 / BPM
N = int(DUR * SR)
rng = np.random.default_rng(7)
L = np.zeros(N)
Rt = np.zeros(N)


def t_(d):
    return np.arange(int(d * SR)) / SR


def add(sig, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N:
        return
    s = sig[: N - i] * gain
    L[i:i + len(s)] += s * np.sqrt(.5 * (1 - pan))
    Rt[i:i + len(s)] += s * np.sqrt(.5 * (1 + pan))


def lp(x, f, o=2):
    return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)


def hp(x, f, o=2):
    return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, hi], "band", fs=SR, output="sos"), x)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def saw(f, t, detune=0.0):
    ph = (f * (1 + detune) * t + rng.random()) % 1.0
    return 2 * ph - 1


# ---------------------------------------------------------------- instruments
def kick(gain=1.0):
    t = t_(.42)
    f = 45 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 7.5)
    s[:int(.004 * SR)] += np.linspace(.6, 0, int(.004 * SR))        # click
    return np.tanh(s * 1.6) * gain


def clap():
    t = t_(.3)
    n = rng.standard_normal(len(t))
    env = np.zeros(len(t))
    for k, d in enumerate([0, .011, .022]):
        i = int(d * SR)
        env[i:] += np.exp(-(t[: len(t) - i]) * (90 if k < 2 else 16))
    return bp(n, 900, 5200) * env * .55


def hat(open_=False):
    t = t_(.22 if open_ else .06)
    n = hp(rng.standard_normal(len(t)), 7000, 3)
    return n * np.exp(-t * (14 if open_ else 70)) * .22


def tick():
    t = t_(.05)
    return np.sin(2 * np.pi * 2600 * t) * np.exp(-t * 120) * .18 + hp(rng.standard_normal(len(t)), 5000) * np.exp(-t * 150) * .06


def bass(note, d, cutoff=900):
    t = t_(d)
    f = midi(note)
    s = .6 * saw(f, t) + .5 * np.sin(2 * np.pi * f * t) + .4 * np.sin(np.pi * f * t)
    env = np.minimum(1, t / .005) * np.exp(-t * 2.2)
    return np.tanh(lp(s, cutoff) * env * 1.4) * .5


def pluck(note, d=.32, bright=4200):
    t = t_(d)
    f = midi(note)
    s = saw(f, t) + .7 * saw(f, t, .006) + .3 * np.sin(2 * np.pi * 2 * f * t)
    env = np.minimum(1, t / .003) * np.exp(-t * 11)
    cut = lp(s, bright) * env
    return cut * .18


def pad(notes, d, cutoff=2600):
    t = t_(d)
    s = np.zeros(len(t))
    for n in notes:
        f = midi(n)
        for dt in (-.012, -.005, 0, .005, .012):
            s += saw(f, t, dt)
    s /= (len(notes) * 5)
    env = np.minimum(1, t / .25) * np.minimum(1, (d - t) / .3)
    return lp(s, cutoff) * env * .55


def stab(notes, d=.28):
    t = t_(d)
    s = np.zeros(len(t))
    for n in notes:
        f = midi(n)
        for dt in (-.008, 0, .008):
            s += saw(f, t, dt)
    s /= (len(notes) * 3)
    env = np.minimum(1, t / .004) * np.exp(-t * 9)
    return lp(s, 5200) * env * .55


def bell(note, d=1.0):
    t = t_(d)
    f = midi(note)
    mod = np.sin(2 * np.pi * f * 3.5 * t) * 2.2 * np.exp(-t * 6)
    s = np.sin(2 * np.pi * f * t + mod) * np.exp(-t * 3.2) + .25 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 5)
    return s * .2


def riser(d):
    t = t_(d)
    n = rng.standard_normal(len(t))
    out = np.zeros(len(t))
    seg = int(.02 * SR)
    for i in range(0, len(t), seg):
        x = i / len(t)
        lo = 300 + 6000 * x ** 2
        out[i:i + seg] = bp(n[i:i + seg + 400], lo, lo * 1.6)[: len(out[i:i + seg])]
    sweep = np.sin(2 * np.pi * np.cumsum(200 + 1400 * (t / d) ** 2) / SR) * .25
    return (out * .5 + sweep) * (t / d) ** 2


def impact():
    t = t_(1.6)
    f = 38 + 60 * np.exp(-t * 9)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.6)
    n = lp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 5) * .4
    return np.tanh((boom + n) * 1.3) * .9


def shimmer(d):
    t = t_(d)
    s = np.zeros(len(t))
    for n in (81, 85, 88, 93):
        s += np.sin(2 * np.pi * midi(n) * t + 3 * np.sin(2 * np.pi * 5.5 * t)) * .06
    return s * np.minimum(1, t / .4) * np.exp(-t * .9)


# ---------------------------------------------------------------- arrangement
PROG_A = [(57, [69, 73, 76]), (52, [68, 71, 76]), (54, [66, 69, 73]), (50, [66, 69, 74])]   # A E F#m D
PROG_T = [(54, [66, 69, 73]), (50, [62, 66, 69]), (54, [66, 69, 73]), (52, [64, 68, 71])]   # tension
ARP = [0, 1, 2, 1]
KICKS = []


def groove(t0, t1, prog, full=True, clapon=False, arp=True, stabs=False, cutoff=4200):
    bar = 4 * BEAT
    b = 0
    t = t0
    while t < t1 - 1e-6:
        root, ch = prog[b % len(prog)]
        for k in range(4):
            tb = t + k * BEAT
            if tb >= t1:
                break
            if full:
                add(kick(), tb, .9)
                KICKS.append(tb)
                add(hat(), tb + BEAT / 2, .9, .3)
                add(hat(), tb + BEAT / 4 * 3, .35, -.3)
                add(bass(root, BEAT * .45, 1100), tb, .9)
                add(bass(root + 12 if k == 3 else root, BEAT * .4, 1100), tb + BEAT / 2, .7)
            if clapon and k in (1, 3):
                add(clap(), tb, .8, .1)
            if stabs and k in (0, 2):
                add(stab(ch), tb + (BEAT * .5 if k == 2 else 0), .55)
        if arp:
            for s in range(16):
                ts = t + s * BEAT / 4
                if ts >= t1:
                    break
                n = ch[ARP[s % 4]] + (12 if s % 8 >= 4 else 0)
                add(pluck(n, bright=cutoff), ts, .9, .25 if s % 2 else -.25)
        b += 1
        t += bar


# 0.0 - 10.5: the hook groove
add(impact(), 0.0, .8)
add(stab([69, 73, 76, 81]), 0.0, .8)
groove(0.0, 10.5, PROG_A, full=True, arp=True)
add(pad([57, 64, 69, 73], 10.5, 2200), 0.0, .35)

# 10.5 - 16.6: tension, half-time, a ticking clock
for k in range(int((16.6 - 10.5) / BEAT)):
    tb = 10.5 + k * BEAT
    if k % 2 == 0 and tb < 13.1:
        add(kick(.7), tb, .8)
        KICKS.append(tb)
    add(tick(), tb, .9, .4)
    add(tick(), tb + BEAT / 2, .5, -.4)
groove(10.5, 13.1, PROG_T, full=False, arp=True, cutoff=1400)
add(pad([54, 61, 66, 69], 2.7, 1400), 10.5, .5)
# 13.2 "dropped": a tape-stop of a falling chord
t = t_(.8)
f = midi(57) * (1 - .7 * (t / .8) ** 1.4)
add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2) * .35 + lp(saw(110, t), 600) * np.exp(-t * 3) * .1, 13.2, 1.0)
add(pad([50, 57, 62, 66], 3.4, 900), 13.6, .5)
add(riser(1.4), 15.8, .55)

# 17.2 - 31.3: the drop
add(impact(), 17.2, .7)
groove(17.2, 31.3, PROG_A, full=True, clapon=True, arp=True, stabs=True)
LEAD = [(0, 76), (.5, 78), (1.0, 81), (1.75, 78), (2.0, 76), (2.5, 73), (3.0, 76), (4.0, 81), (4.5, 83), (5.0, 85), (5.75, 83),
        (6.0, 81), (6.5, 78), (7.0, 76)]
for rep in range(4):
    for dt, n in LEAD:
        tt = 17.2 + rep * 4.0 + dt
        if tt < 31.0:
            add(bell(n, .9), tt, .75, .15)
for s in range(int((31.3 - 24.5) / (BEAT / 4))):                     # sparkle arp for the audit
    add(pluck([81, 85, 88, 93][s % 4], .2, 7000), 24.5 + s * BEAT / 4, .35, .5 if s % 2 else -.5)

# 31.3 - 32.3: break and riser
add(pad([57, 64, 69, 73, 76], 1.2, 3000), 31.2, .45)
add(riser(1.0), 31.3, .7)

# 32.3 - 35.4: the CTA
add(impact(), 32.3, .65)
groove(32.3, 35.4, PROG_A, full=True, clapon=True, arp=True, stabs=True)
for dt, n in [(0, 81), (.5, 85), (1.0, 88), (1.5, 85), (2.0, 93), (2.5, 88)]:
    add(bell(n, 1.2), 32.3 + dt, .8, -.15)

# 35.4: the logo
add(impact(), 35.4, .6)
add(stab([57, 64, 69, 73, 76, 81], .9), 35.4, .9)
add(pad([45, 57, 64, 69, 73, 76], 2.2, 3200), 35.4, .5)
add(shimmer(2.2), 35.4, 1.0)
add(bell(93, 2.0), 35.45, .7)

# ---------------------------------------------------------------- sidechain pump, reverb, master
pump = np.ones(N)
for tk in KICKS:
    i = int(tk * SR)
    ln = int(.22 * SR)
    seg = 1 - .45 * np.exp(-np.arange(ln) / SR * 18)
    pump[i:i + ln] = np.minimum(pump[i:i + ln], seg[: len(pump[i:i + ln])])
L *= pump
Rt *= pump
ir_t = t_(1.6)
for ch, seed in ((0, 1), (1, 2)):
    r = np.random.default_rng(seed).standard_normal(len(ir_t)) * np.exp(-ir_t * 3.2)
    r = lp(r, 6000)
    r /= np.abs(r).sum() / 6
    src = L if ch == 0 else Rt
    wet = fftconvolve(hp(src, 300), r)[:N] * .18
    if ch == 0:
        L = L + wet
    else:
        Rt = Rt + wet
mix = np.stack([L, Rt], 1)
mix = hp(mix.T, 28).T
fade = np.ones(N)
fi = int((DUR - 1.4) * SR)
fade[fi:] = np.linspace(1, 0, N - fi) ** 1.5
mix *= fade[:, None]
mix = np.tanh(mix / (np.abs(mix).max() + 1e-9) * 1.4) * .89
out = (mix * 32767).astype(np.int16)
with wave.open(os.path.join(ROOT, "assets", "audio", "music.wav"), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(out.tobytes())
print(f"music.wav {DUR}s")
