"""Original score and sound design for the Sucsess Maperrs ad, synthesized here so there are no rights issues.

python3 -I build/audio.py      (run from the project root, after build/generate.py; needs numpy, scipy, ffmpeg)

Score: a warm, hopeful 84 bpm bed in D major (D - A - Bm - G): felt-piano arpeggios and a soft pad from the first frame,
a low pulse and light percussion from the brand reveal, a lift into the free scan and the offer, percussion out under the
disclaimer, and a resolving final chord under the end card. Sound design: every visual event generate.py logs
(build/sfx_events.json) gets a matching sound: soft whooshes on framing moves, pops and pings for cards, a coin shimmer,
stamps, ticks, a reveal swell for the logo, a count roll for the price, a glassy shimmer with every light sweep, UI taps
and scroll ticks on the app screens, a ticking timer, and sub-boom impacts on the hook, the reveal, the offer and the CTA.

Mix: the bed is ducked by the voice (envelope follower) and carved: its 1-4 kHz band drops further while she speaks, so
the words stay clear. Writes assets/audio/music.wav (bed + SFX) and assets/audio/voice.wav (her voice, cleaned and mastered).
"""
import json
import os
import subprocess
import sys
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate as G  # noqa: E402

SR = 48000
DUR = G.DUR
N = int(DUR * SR)
L = G.L
BPM = 84
BEAT = 60 / BPM
BAR = 4 * BEAT
rng = np.random.default_rng(11)


def lp(x, fc, o=2):
    return sosfilt(butter(o, fc, "low", fs=SR, output="sos"), x)


def hp(x, fc, o=2):
    return sosfilt(butter(o, fc, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, hi], "band", fs=SR, output="sos"), x)


def tt(d):
    return np.arange(int(d * SR)) / SR


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


BUS = {k: (np.zeros(N), np.zeros(N)) for k in ("music", "sfx")}


def put(x, t, g=1.0, pan=0.0, bus="music"):
    i = int(t * SR)
    if i >= N or i < 0:
        return
    x = x[: N - i]
    l, r = BUS[bus]
    l[i:i + len(x)] += x * g * np.sqrt(.5 * (1 - pan))
    r[i:i + len(x)] += x * g * np.sqrt(.5 * (1 + pan))


# ------------------------------------------------------------------ instruments
def piano(m, d=1.6, v=1.0):
    t = tt(d)
    f = hz(m)
    x = sum(a * np.sin(2 * np.pi * f * k * t * (1 + .0004 * k)) * np.exp(-t * (2.2 + k * 1.4)) for k, a in
            ((1, 1), (2, .45), (3, .22), (4, .1)))
    x += .2 * bp(rng.standard_normal(len(t)), 800, 3000) * np.exp(-t * 90)            # felt hammer
    return lp(x, 3800) * np.minimum(1, t / .004) * .07 * v


def pad(ms, d):
    t = tt(d)
    x = np.zeros_like(t)
    for m in ms:
        for det in (-.12, .12):
            ph = (hz(m) * (1 + det / 100) * t) % 1
            x += 2 * ph - 1
    env = np.minimum(1, t / 1.2) * np.clip((d - t) / 1.0, 0, 1)
    return lp(x, 1400) * env * .018


def sub(m, d):
    t = tt(d)
    return np.sin(2 * np.pi * hz(m) * t) * np.minimum(1, t / .02) * np.clip((d - t) / .2, 0, 1) * .16


def kick(d=.4):
    t = tt(d)
    f = 48 + 90 * np.exp(-t * 32)
    return np.tanh(1.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)) * .38


def snap(d=.2):
    t = tt(d)
    return bp(rng.standard_normal(len(t)), 1800, 6000) * np.exp(-t * 55) * .09


def shaker(d=.07):
    t = tt(d)
    return hp(rng.standard_normal(len(t)), 7000) * np.exp(-t * 70) * np.minimum(1, t / .008) * .035


def riser(d=1.6):
    t = tt(d)
    n = rng.standard_normal(len(t))
    seg, s = 16, len(t) // 16
    x = np.zeros_like(t)
    for i in range(seg):
        lo = 300 * (12 ** (i / seg))
        x[i * s:(i + 1) * s] = bp(n, lo, min(lo * 2.2, 18000))[i * s:(i + 1) * s]
    return x * (t / d) ** 2 * .1


# ------------------------------------------------------------------ sound design
def whoosh(d=.45, g=1.0):
    t = tt(d)
    n = rng.standard_normal(len(t))
    seg, s = 10, len(t) // 10
    x = np.zeros_like(t)
    for i in range(seg):
        lo = 250 * (8 ** (i / seg))
        x[i * s:(i + 1) * s] = bp(n, lo, min(lo * 2.4, 16000))[i * s:(i + 1) * s]
    return x * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.6 * .1 * g


def pop(f0=900, d=.12):
    t = tt(d)
    f = f0 * (1 + 1.4 * np.exp(-t * 55))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 38) * .14


def ping(m=86, d=.9):
    t = tt(d)
    return (np.sin(2 * np.pi * hz(m) * t) + .35 * np.sin(2 * np.pi * hz(m + 12) * t) * np.exp(-t * 6)) * np.exp(-t * 5) * .05


def chime(d=1.4):
    t = tt(d)
    x = np.zeros_like(t)
    for j, m in enumerate((86, 90, 93, 98)):
        o = j * .07
        tj = np.clip(t - o, 0, None)
        x += np.where(t >= o, np.sin(2 * np.pi * hz(m) * tj) * np.exp(-tj * 4.5), 0)
    return x * .04


def coins(d=1.6):
    out_ = np.zeros(int(d * SR))
    for k in range(14):
        tk = k * .1 + rng.uniform(0, .05)
        x = ping(int(rng.choice([91, 93, 95, 98])), .4) * .8
        i = int(tk * SR)
        out_[i:i + len(x)] += x[: len(out_) - i]
    return out_


def stamp(d=.5):
    t = tt(d)
    body = np.sin(2 * np.pi * np.cumsum(60 + 80 * np.exp(-t * 30)) / SR) * np.exp(-t * 14)
    return np.tanh(1.8 * (body + .4 * bp(rng.standard_normal(len(t)), 300, 2500) * np.exp(-t * 40))) * .3


def tick(d=.05):
    t = tt(d)
    return np.sin(2 * np.pi * 2600 * t) * np.exp(-t * 140) * .1


def thud(d=1.0):
    t = tt(d)
    return np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(40 + 50 * np.exp(-t * 9)) / SR) * np.exp(-t * 4)) * .3


def rattle(d, rate=20):
    out_ = np.zeros(int(d * SR))
    for k in range(int(d * rate)):
        x = tick(.03) * .7
        i = int(k / rate * SR)
        out_[i:i + len(x)] += x[: len(out_) - i]
    return out_


def swell(d=1.6):
    t = tt(d)
    x = sum(np.sin(2 * np.pi * hz(m) * t) for m in (62, 69, 74, 78))
    return lp(x, 2400) * (t / d) ** 1.5 * np.clip((d + .3 - t) / .3, 0, 1) * .03


def shimmer(d=.7):
    """The light sweep: a bright airy whoosh with a glassy top."""
    t = tt(d)
    x = hp(rng.standard_normal(len(t)), 5000) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2 * .05
    return x + sum(np.sin(2 * np.pi * hz(m) * t) * np.exp(-t * 5) for m in (93, 98)) * .012


def click(d=.06):
    t = tt(d)
    return (bp(rng.standard_normal(len(t)), 2000, 7000) * np.exp(-t * 160) * .2 + np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 90) * .08)


def scroll(d=1.0):
    out_ = np.zeros(int(d * SR))
    for k in range(9):
        x = click(.03) * .35
        i = int((k * .1 + k * k * .004) * SR)
        out_[i:i + len(x)] += x[: len(out_) - i]
    return out_


def clock(d=.12):
    t = tt(d)
    return np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 120) * .12 + bp(rng.standard_normal(len(t)), 1500, 5000) * np.exp(-t * 200) * .08


def boom(d=2.2):
    t = tt(d)
    x = np.sin(2 * np.pi * np.cumsum(32 + 46 * np.exp(-t * 7)) / SR) * np.exp(-t * 2.2)
    x += .25 * lp(rng.standard_normal(len(t)), 300) * np.exp(-t * 5)
    return np.tanh(1.6 * x) * .45


# ------------------------------------------------------------------ arrangement
PROG = [(62, 66, 69), (57, 61, 64), (59, 62, 66), (55, 59, 62)]     # D, A, Bm, G
ROOTS = [38, 33, 35, 31]
REVEAL, DISC, OFFER_LIFT, END_CTA = L[5][0], (L[7][0], L[8][1]), L[11][0], L[15][0]


def arrange():
    nbeats = int(DUR / BEAT) + 2
    for b in range(nbeats):
        t = b * BEAT
        if t > DUR - 2.2:
            break
        bar, beat = b // 4, b % 4
        ci = bar % 4
        chord = PROG[ci]
        if beat == 0:
            put(pad([m + 12 for m in chord], BAR + .4), t, 1.0)
            if t >= REVEAL - .1:
                put(sub(ROOTS[ci], BAR * .95), t, 1.0)
        # felt-piano arpeggio: 8ths, up the chord
        for k in range(2):
            tk = t + k * BEAT / 2
            m = (chord + tuple(c + 12 for c in chord))[(beat * 2 + k) % 6] + 12
            put(piano(m, 1.4, .85 if k else 1.0), tk, 1.0, pan=-.15 + .1 * k)
        disc = DISC[0] - .1 <= t < DISC[1] - .1
        if t >= REVEAL - .05 and not disc:
            if beat in (0, 2):
                put(kick(), t, .9 if t < OFFER_LIFT else 1.05)
            if beat in (1, 3):
                put(snap(), t, .9, pan=.1)
            for k in range(2):
                put(shaker(), t + k * BEAT / 2, 1.0 if k else .6, pan=-.25)
    put(riser(1.8), REVEAL - 1.75, 1.0)
    put(riser(1.4), OFFER_LIFT - 1.4, .8)
    # resolving end chord under the CTA
    t = END_CTA + .2
    for j, m in enumerate((62, 66, 69, 74, 78)):
        put(piano(m + 12, 3.5, .9), t + j * .08, 1.0)
    put(pad([74, 78, 81], DUR - t), t, 1.3)


def sfx():
    evs = json.load(open(os.path.join(ROOT, "build", "sfx_events.json")))
    for t, kind, d in evs:
        pan = float(rng.uniform(-.3, .3))
        if kind == "whoosh":
            put(whoosh(.5, 1.0), t - .05, .8, pan, "sfx")
        elif kind == "pop":
            put(pop(float(rng.uniform(760, 1100))), t, .7, pan, "sfx")
        elif kind == "ping":
            put(ping(int(rng.choice([86, 88, 91]))), t, 1.0, pan, "sfx")
            put(pop(1300, .07), t, .35, pan, "sfx")
        elif kind == "rise":
            put(whoosh(.35, .7), t, .6, 0, "sfx")
        elif kind == "coins":
            put(coins(), t, 1.0, .2, "sfx")
        elif kind == "stamp":
            put(stamp(), t, 1.0, 0, "sfx")
        elif kind == "thud":
            put(thud(), t, .8, 0, "sfx")
        elif kind == "tick":
            put(tick(), t, 1.4, pan, "sfx")
            put(ping(93, .5), t, .5, pan, "sfx")
        elif kind == "swish":
            put(whoosh(.25, .8), t - .05, .6, pan, "sfx")
        elif kind == "reveal":
            put(chime(), t, 1.0, 0, "sfx")
            put(swell(1.4), t - .9, 1.0, 0, "sfx")
        elif kind == "swell":
            put(swell(1.3), t, 1.0, 0, "sfx")
        elif kind == "count":
            put(rattle(max(.3, d), 22), t, .8, pan, "sfx")
        elif kind == "dice":
            for k in range(4):
                put(stamp(.2) * .4, t + k * .12, .7, -.4 + .25 * k, "sfx")
        elif kind == "sweep":
            put(shimmer(), t, .9, 0, "sfx")
        elif kind == "click":
            put(click(), t, 1.2, pan, "sfx")
        elif kind == "scroll":
            put(scroll(), t, 1.0, pan, "sfx")
        elif kind == "clock":
            put(clock(), t, 1.2, 0, "sfx")
        elif kind == "boom":
            put(boom(), t, 1.0, 0, "sfx")
        elif kind == "glint":
            put(chime(.8), t, .7, pan, "sfx")


def reverb(x, secs=2.2, mix=.25, seed=0):
    r = np.random.default_rng(seed)
    t = np.arange(int(secs * SR)) / SR
    ir = lp(r.standard_normal(len(t)) * np.exp(-t * 3), 6500)
    ir /= np.sqrt(np.sum(ir ** 2))
    return x * (1 - mix) + fftconvolve(x, ir)[: len(x)] * mix * 1.4


def rms(x):
    return np.sqrt(np.mean(x ** 2) + 1e-12)


def voice_env():
    """0..1 speech activity from voice.wav: rectified, smoothed with a fast attack and slow release."""
    w = wave.open(os.path.join(ROOT, "assets", "audio", "voice.wav"))
    a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, w.getnchannels()).mean(1) / 32768
    a = np.pad(a, (0, max(0, N - len(a))))[:N]
    hop = 480
    frames = np.sqrt(np.convolve(a[: len(a) // hop * hop].reshape(-1, hop).__pow__(2).mean(1), np.ones(3) / 3, "same"))
    act = np.clip((20 * np.log10(frames + 1e-6) + 46) / 14, 0, 1)
    sm = np.zeros_like(act)
    for i in range(1, len(act)):
        k = .5 if act[i] > sm[i - 1] else .04            # attack ~20 ms, release ~250 ms per 10 ms hop
        sm[i] = sm[i - 1] + (act[i] - sm[i - 1]) * k
    env = np.repeat(sm, hop)
    return np.pad(env, (0, max(0, N - len(env))))[:N]


def make_voice():
    """Her voice from the cut master: rumble cut, light denoise, gentle compression, mastered to about -14.5 LUFS."""
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(ROOT, "assets", "video", "talk.mp4"), "-vn", "-af",
                    "highpass=f=75,afftdn=nf=-30,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3,"
                    "loudnorm=I=-14.5:TP=-1.5:LRA=9", "-ar", str(SR), "-ac", "2", os.path.join(ROOT, "assets", "audio", "voice.wav")],
                   check=True)


def main():
    make_voice()
    arrange()
    sfx()
    ml, mr = reverb(BUS["music"][0], seed=1), reverb(BUS["music"][1], seed=2)
    sl, sr_ = reverb(BUS["sfx"][0], 1.0, .15, 3), reverb(BUS["sfx"][1], 1.0, .15, 4)
    env = voice_env()
    duck = 1 - .42 * env                                     # about -5 dB under speech
    carve = 1 - .55 * env                                    # the 1-4 kHz band drops a further ~3 dB
    out_ch = []
    for m in (ml, mr):
        mid = bp(m, 1000, 4000)
        m = (m - mid + mid * carve) * duck
        out_ch.append(m)
    gm = .03 / rms(out_ch[0] + out_ch[1])
    gs = .05 / rms(sl + sr_)
    left, right = out_ch[0] * gm + sl * gs, out_ch[1] * gm + sr_ * gs
    fade = np.ones(N)
    fade[-int(1.2 * SR):] = np.linspace(1, 0, int(1.2 * SR)) ** 1.5
    st = np.stack([left * fade, right * fade], 1) * 1.9
    pk = np.max(np.abs(st))
    if pk > .95:
        st *= .95 / pk
    path = os.path.join(ROOT, "assets", "audio", "music.wav")
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())
    voice = os.path.join(ROOT, "assets", "audio", "voice.wav")
    o = subprocess.run(["ffmpeg", "-i", voice, "-i", path, "-filter_complex", "amix=inputs=2:normalize=0,ebur128", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    o2 = subprocess.run(["ffmpeg", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    pick = lambda s: [ln.strip() for ln in s.splitlines() if ln.strip().startswith("I:")][-1:]   # noqa: E731
    print("wrote", path, "| mix", pick(o), "| bed+sfx alone", pick(o2))


if __name__ == "__main__":
    main()
