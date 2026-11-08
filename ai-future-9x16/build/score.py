"""The AI Future reel's original score, composed in code: 100 bpm, A minor, a ticking clock as the motif (the phone
sees the clock run ahead), chip and bell colours for the voxel world; every beat of the story gets its own turn.

build/audio.py calls compose(cues, n). Nothing is sampled, so the score needs no licence or credit.

  title, NY   a wide pad and a clock tick; a hit and bells when the coffee falls on 9:14
  Las Vegas   a low groove with slot-machine chips; a riser into black 17; a crash and a shower of bells
  Miami       a dark pulse and a heartbeat; a riser into the fall; a big hit, then a held, relieved chord
  day 21      near-silence, a low drone; a sting on "don't open the door"; the music stops for the knock
  day 30      the clock ticks again and stops dead on "the screen is black"
  real world  a reflective groove that builds
  end         the theme, softly, and one last hit
"""
import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
BEAT = 60 / 112
TAB = 4096
_TABLES = {}
rng = np.random.default_rng(57)


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def lp(x, fc, o=2):
    return sosfilt(butter(o, min(fc, SR / 2 - 200), "low", fs=SR, output="sos"), x, axis=0)


def hp(x, fc, o=2):
    return sosfilt(butter(o, fc, "high", fs=SR, output="sos"), x, axis=0)


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, min(hi, SR / 2 - 200)], "band", fs=SR, output="sos"), x, axis=0)


# ---------------------------------------------------------------- band-limited oscillators (wavetables, no aliasing)
def table(kind, k):
    key = (kind, k)
    if key not in _TABLES:
        ph = np.arange(TAB) / TAB * 2 * np.pi
        h = np.arange(1, k + 1)
        if kind == "sq":
            h = h[h % 2 == 1]
        _TABLES[key] = (np.sin(np.outer(h, ph)) / h[:, None]).sum(0) * (2 / np.pi)
    return _TABLES[key]


def osc(f, n, kind="saw", phase=0.0, vib=0.0):
    k = max(1, min(400, int(15000 / f)))
    tb = table(kind, k)
    fr = f * (1 + vib * np.sin(2 * np.pi * 5.2 * np.arange(n) / SR)) if vib else f
    ph = (phase + np.cumsum(np.full(n, 1.0) * fr) / SR) % 1 * TAB
    i = ph.astype(int)
    a = ph - i
    return tb[i] * (1 - a) + tb[(i + 1) % TAB] * a


def env(n, a=.005, d=.1, s=.7, r=.05, hold=None):
    """ADSR over n samples; the release starts at `hold` s (default: n minus the release)."""
    t = np.arange(n) / SR
    hold = (n / SR - r) if hold is None else hold
    e = np.where(t < a, t / max(a, 1e-4), s + (1 - s) * np.exp(-(t - a) / max(d, 1e-4)))
    return e * np.clip((n / SR - t) / max(r, 1e-4), 0, 1) * np.where(t > hold, np.exp(-(t - hold) / max(r, 1e-4) * 3), 1)


# ---------------------------------------------------------------- instruments
def kick(big=False):
    n = int(.5 * SR)
    t = np.arange(n) / SR
    f = 46 + (150 if big else 120) * np.exp(-t * 30)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * (6 if big else 8))
    click = hp(rng.standard_normal(n), 3000) * np.exp(-t * 400) * .35
    return np.tanh((body + click) * (1.8 if big else 1.4)) * .9


def clap():
    n = int(.35 * SR)
    t = np.arange(n) / SR
    nz = bp(rng.standard_normal(n), 900, 4500)
    e = sum(np.exp(-np.maximum(0, t - d) * 140) * (t >= d) for d in (0, .011, .022)) * .5 + np.exp(-t * 16) * (t >= .03) * .6
    return nz * e * .7


def hat(open_=False):
    n = int((.32 if open_ else .06) * SR)
    t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 7500, 4) * np.exp(-t * (9 if open_ else 70)) * (.22 if open_ else .2)


def crash():
    n = int(2.2 * SR)
    t = np.arange(n) / SR
    x = hp(rng.standard_normal(n), 4500, 2) * np.exp(-t * 2.0) * .32
    for f in (3150, 4720, 6380, 8110):
        x += np.sin(2 * np.pi * f * t + rng.random() * 6) * np.exp(-t * 3) * .02
    return x


def sub(m, d):
    n = int(max(d, .05) * SR)
    return np.tanh(1.3 * np.sin(2 * np.pi * hz(m) * np.arange(n) / SR)) * env(n, .004, .3, .85, .04)


def supersaw(ms, d, cut=4000, attack=.01, release=.12, width=.6):
    n = int(max(d, .05) * SR)
    L_ = np.zeros(n)
    R_ = np.zeros(n)
    for m in ms:
        for v, cents in enumerate((-18, -11, -5, 0, 5, 11, 18)):
            x = osc(hz(m) * 2 ** (cents / 1200), n, phase=rng.random())
            pan = (v - 3) / 3 * width
            L_ += x * np.sqrt(.5 * (1 - pan))
            R_ += x * np.sqrt(.5 * (1 + pan))
    e = env(n, attack, .25, .8, release)
    st = np.stack([L_, R_], 1) * e[:, None] / (len(ms) * 7) * 2.2
    return lp(st, cut, 2)


def pluck(m, d=.35, bright=1.0):
    n = int(d * SR)
    t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * hz(m) * k * t) / k * np.exp(-t * (5 + k * 3.5 / bright)) for k in range(1, 10))
    return x * np.minimum(1, t / .002) * .5


def bell(m, d=1.4):
    n = int(d * SR)
    t = np.arange(n) / SR
    f = hz(m)
    return (np.sin(2 * np.pi * f * t) * np.exp(-t * 2.4) + np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 5) * .35
            + np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 9) * .12) * np.minimum(1, t / .002) * .5


def riser(d, g=1.0):
    d = max(d, .2)
    n = int(d * SR)
    t = np.arange(n) / SR
    k = t / d
    nz = rng.standard_normal(n)
    x = np.zeros(n)
    seg = max(1, n // 24)
    for i in range(24):                                   # a band of noise sweeping up
        lo = 400 * 2 ** (i / 24 * 4.5)
        x[i * seg:(i + 1) * seg] = bp(nz, lo, lo * 3)[i * seg:(i + 1) * seg]
    f = 110 * 2 ** (k * 3)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return (x * .6 + tone * .25) * k ** 2 * g


def downlift(d=1.0):
    n = int(d * SR)
    t = np.arange(n) / SR
    return lp(rng.standard_normal(n), 3000) * np.exp(-t * 3) * .3


def reverb(x, secs=1.6, mix=.2, seed=0):
    r = np.random.default_rng(seed)
    t = np.arange(int(secs * SR)) / SR
    ir = lp(r.standard_normal(len(t)) * np.exp(-t * 3.2), 7000)
    ir /= np.sqrt(np.sum(ir ** 2))
    return x * (1 - mix) + fftconvolve(x, ir)[: len(x)] * mix * 1.4



def taiko(big=1.0):
    n = int(.9 * SR)
    t = np.arange(n) / SR
    f = 55 + 70 * np.exp(-t * 18)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * (4.5 / big))
    skin = bp(rng.standard_normal(n), 120, 1400) * np.exp(-t * 28) * .5
    return np.tanh((body + skin) * 1.6 * big) * .9


def tick():
    n = int(.05 * SR)
    t = np.arange(n) / SR
    return (bp(rng.standard_normal(n), 2500, 7000) * np.exp(-t * 160) + np.sin(2 * np.pi * 3400 * t) * np.exp(-t * 90) * .3) * .5


def chip(m, d=.12, duty=.25):
    """A pulse-wave blip, the voxel world's voice."""
    n = int(d * SR)
    t = np.arange(n) / SR
    ph = (hz(m) * t) % 1
    x = np.where(ph < duty, 1.0, -1.0) - (2 * duty - 1)
    return lp(x, 6000) * np.minimum(1, t / .002) * np.exp(-t * 9) * .35


def heart():
    n = int(.5 * SR)
    t = np.arange(n) / SR
    b = lambda t0, f, g: np.where(t >= t0, np.sin(2 * np.pi * f * (t - t0)) * np.exp(-np.maximum(0, t - t0) * 18), 0) * g  # noqa: E731
    return lp(b(0, 55, 1.0) + b(.17, 48, .7), 220) * .9


AM, FM, CM, GM = [69, 72, 76], [65, 69, 72], [64, 67, 72], [62, 67, 71]
MIN, MROOT = [AM, FM, CM, GM], [45, 41, 48, 43]
DK, DKR = [[57, 60, 64], [53, 57, 60], [52, 55, 59], [53, 57, 62]], [33, 29, 28, 29]
BEAT = 60 / 100


def compose(cues, n):
    C = cues
    CU, END = C["cuts"], C["end"]
    BUS = {k: np.zeros((n, 2)) for k in ("drums", "bass", "chords", "keys", "fx")}
    kicks = []

    def put(x, t, bus, g=1.0, pan=0.0):
        i = int(round(t * SR))
        if i >= n or g == 0:
            return
        if x.ndim == 1:
            x = np.stack([x * np.sqrt(.5 * (1 - pan)), x * np.sqrt(.5 * (1 + pan))], 1)
        if i < 0:
            x, i = x[-i:], 0
        x = x[: n - i]
        BUS[bus][i:i + len(x)] += x * g

    def beats(a, b, step=BEAT):
        k = int(np.ceil(a / step - 1e-6))
        while k * step < b - 1e-6:
            yield k * step, k
            k += 1

    bar = lambda t, s: int((t - s) // (4 * BEAT)) % 4  # noqa: E731

    def pads(a, b, prog, roots, cut, g=1.0, sub_g=.5):
        for t, k in beats(a, b, 4 * BEAT):
            c = bar(t, a)
            d = min(4 * BEAT, b - t)
            if d > .2:
                put(supersaw(prog[c], d, cut, .3, .4, .9), t, "chords", .45 * g)
                put(sub(roots[c], d - .05), t, "bass", sub_g * g)

    # 1. title and New York: a wide pad, the clock; a hit on 9:14
    pads(0, CU[0], MIN, MROOT, 1100, .9)
    for t, k in beats(0, C["does"] - .1):
        put(tick(), t, "drums", .55, .3)
        if t > C["day1"] and k % 2 == 0:
            put(kick(), t, "drums", .35); kicks.append(t)
    for t, k in beats(C["day1"], C["does"] - .1, BEAT / 2):
        put(chip(MIN[bar(t, C["day1"])][k % 3] + 12, .1), t, "keys", .16, (k % 2 - .5) * .6)
    put(riser(C["does"] - C["at3"] + .1, .6), C["at3"] - .1, "fx")
    put(taiko(1.4), C["does"], "drums", 1.0); put(crash(), C["does"], "drums", .5)
    for k, m in enumerate([81, 84, 88]):
        put(bell(m, 1.0), C["does"] + .05 + k * .1, "keys", .4, (k - 1) * .4)
    # 2. Las Vegas: a low groove with slot chips, a riser into black 17, the win
    tl = C["seventeen"]
    for t, k in beats(CU[0], tl - .1):
        c = bar(t, CU[0])
        put(kick(), t, "drums", .6); kicks.append(t)
        put(hat(), t + BEAT / 2, "drums", .3, .2)
        if k % 4 == 0:
            put(supersaw(MIN[c], 4 * BEAT, 1600, .05, .3, .9), t, "chords", .45)
            put(sub(MROOT[c], 4 * BEAT - .05), t, "bass", .6)
        for s_ in range(2):
            put(chip(MIN[c][(k * 2 + s_) % 3] + 24, .09, .125), t + s_ * BEAT / 2, "keys", .16, (s_ - .5) * .7)
    put(riser(tl - C["black5"] + 1.0, .8), C["black5"] - 1.0, "fx")
    put(taiko(1.6), tl, "drums", 1.1); put(crash(), tl, "drums", .8)
    for k in range(8):
        put(bell(84 + [0, 4, 7, 12, 7, 12, 16, 19][k], .9), tl + .1 + k * .1, "keys", .35, (k % 2 - .5) * .6)
    for t, k in beats(tl + .05, CU[1] - .05):
        c = bar(t, tl)
        put(kick(), t, "drums", .8); kicks.append(t)
        if k % 2:
            put(clap(), t, "drums", .5)
        put(hat(True), t + BEAT / 2, "drums", .35, .2)
        if k % 4 == 0 or t < tl + BEAT:
            put(supersaw([72, 76, 79], 4 * BEAT, 4200, .02, .3, 1.0), t, "chords", .6)
            put(sub(48, 4 * BEAT - .05), t, "bass", .7)
        put(chip([72, 76, 79, 84][k % 4] + 12, .12), t + BEAT / 2, "keys", .22, .3)
    # 3. Miami: a dark pulse and a heartbeat; a riser into the fall; then a held, relieved chord
    dn = C["down"]
    pads(CU[1], dn - .1, DK, DKR, 700, 1.0, .6)
    for t, k in beats(CU[1], dn - .2, BEAT / 2):
        put(tick(), t, "drums", .3 + .35 * (t - CU[1]) / (dn - CU[1]), .3)
    for k in range(int((dn - C["block"]) / .62)):
        put(heart(), C["block"] + k * .62, "drums", .55)
    put(riser(dn - C["noon9"] + .5, .9), C["noon9"] - .5, "fx")
    put(taiko(1.9), dn, "drums", 1.2); put(sub(26, 1.8), dn, "bass", .8); put(crash(), dn, "drums", .7)
    put(supersaw([60, 64, 67, 71], CU[2] - C["nobody"], 1500, .5, .6, 1.0), C["nobody"], "chords", .5)
    put(bell(76, 2.0), C["nobody"] + .3, "keys", .3)
    # 4. home, day 21: near-silence, a sting, the music stops for the knock
    kn = C["knocks"]
    put(supersaw([45, 52, 57], kn - .35 - CU[2], 420, .8, .3, .9), CU[2], "chords", .5)
    put(sub(33, kn - .35 - CU[2]), CU[2], "bass", .35)
    put(bell(69, 2.0), C["open"], "keys", .4); put(bell(68, 2.0), C["open"] + .02, "keys", .25)
    put(downlift(1.2), C["door"], "fx", .5)
    put(supersaw([44, 51, 56], CU[3] - kn - .8, 380, .6, .4, .9), kn + .8, "chords", .4)
    # 5. home, day 30: the clock again, stopping dead on black
    bk = C["black"]
    for t, k in beats(CU[3], bk - .05, BEAT / 2):
        put(tick(), t, "drums", .55, .3)
        if k % 2 == 0:
            put(sub(33, .3), t, "bass", .4)
    put(supersaw([57, 60, 64], bk - CU[3], 650, .3, .1, .9), CU[3], "chords", .45)
    put(sub(21, 1.6), bk, "bass", .7)
    # 6. the real part: a reflective groove that builds
    S5, S6 = CU[4], CU[5]
    for t, k in beats(S5, S6 - .05):
        c = bar(t, S5)
        g = min(1, (t - S5) / (S6 - S5))
        if k % 2 == 0 or g > .5:
            put(kick(), t, "drums", .35 + .4 * g); kicks.append(t)
        put(hat(), t + BEAT / 2, "drums", .22 + .2 * g, .2)
        if k % 4 == 0:
            put(supersaw(MIN[c], 4 * BEAT, 1500 + 2500 * g, .2, .4, .9), t, "chords", .55)
            put(sub(MROOT[c], 4 * BEAT - .05), t, "bass", .55)
        put(pluck(MIN[c][k % 3] + 12, .3, 1.0), t, "keys", .3, .3)
    put(crash(), C["ten"], "drums", .45)
    # 7. the end: the theme, softly, and one last hit
    last = S6 + int((END - .6 - S6) / BEAT) * BEAT
    for t, k in beats(S6, last):
        c = bar(t, S6)
        put(kick(), t, "drums", .6); kicks.append(t)
        if k % 2:
            put(clap(), t, "drums", .4)
        put(tick(), t + BEAT / 2, "drums", .4, .3)
        if k % 4 == 0 or t == S6:
            put(supersaw(MIN[c], 4 * BEAT, 2600, .1, .3, 1.0), t, "chords", .6)
            put(sub(MROOT[c], 4 * BEAT - .05), t, "bass", .6)
        put(chip(MIN[c][k % 3] + 12, .12), t + BEAT / 2, "keys", .2, .3)
    put(taiko(1.3), last, "drums", 1.0); put(crash(), last, "drums", .8)
    put(supersaw(AM + [81], 1.4, 4000, .003, .4, 1.0), last, "chords", .9)
    # mix
    duck = np.ones(n)
    for k in kicks:
        i = int(k * SR)
        m = min(n - i, int(.3 * SR))
        if m > 0:
            duck[i:i + m] = np.minimum(duck[i:i + m], 1 - .5 * np.exp(-np.arange(m) / SR / .09))
    BUS["bass"] *= duck[:, None]
    BUS["chords"] *= (1 - (1 - duck) * .7)[:, None]
    BUS["chords"] = np.stack([reverb(BUS["chords"][:, c], 1.8, .24, c) for c in (0, 1)], 1)
    BUS["keys"] = np.stack([reverb(BUS["keys"][:, c], 2.2, .3, c + 4) for c in (0, 1)], 1)
    BUS["drums"] = np.stack([reverb(BUS["drums"][:, c], 1.1, .1, c + 8) for c in (0, 1)], 1)
    rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)  # noqa: E731
    gain = {"drums": .11, "bass": .07, "chords": .06, "keys": .055, "fx": .035}
    out = sum(BUS[k] * (gain[k] / rms(BUS[k])) for k in BUS)
    return np.tanh(out * 2.2) / 2.2
