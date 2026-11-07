"""The AI Posts reel's original score, composed in code: a cozy lo-fi study beat (soft kick, brushed hats, warm plucks
and pads, a little pulse-wave melody for Hoot), tuned to the skit's beats. Nothing is sampled, so it needs no licence.

  the desk     a quiet lo-fi loop; a thud of a hit when the notes land; a lift into each STEP
  the bus      the loop filtered, as if heard through headphones
  62 / 91      a sad two-note fall on 62, a bright bell run and a crash on 91
  the bag      the beat drops out for Hoot's "No."; a soft pad under "you know every answer"
  close        the full loop back in, one last hit
"""
import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
BEAT = 60 / 84
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
    n = int(d * SR)
    return np.tanh(1.3 * np.sin(2 * np.pi * hz(m) * np.arange(n) / SR)) * env(n, .004, .3, .85, .04)


def supersaw(ms, d, cut=4000, attack=.01, release=.12, width=.6):
    n = int(d * SR)
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


def reverb(x, secs=1.6, mix=.2, seed=0):
    r = np.random.default_rng(seed)
    t = np.arange(int(secs * SR)) / SR
    ir = lp(r.standard_normal(len(t)) * np.exp(-t * 3.2), 7000)
    ir /= np.sqrt(np.sum(ir ** 2))
    return x * (1 - mix) + fftconvolve(x, ir)[: len(x)] * mix * 1.4



def snare():
    n = int(.25 * SR)
    t = np.arange(n) / SR
    return (bp(rng.standard_normal(n), 1500, 7000) * np.exp(-t * 26) * .45 + np.sin(2 * np.pi * 200 * t) * np.exp(-t * 35) * .3) * .7


def taiko(big=1.0):
    n = int(.9 * SR)
    t = np.arange(n) / SR
    f = 55 + 70 * np.exp(-t * 18)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * (4.5 / big))
    skin = bp(rng.standard_normal(n), 120, 1400) * np.exp(-t * 28) * .5
    return np.tanh((body + skin) * 1.6 * big) * .9


def chip(m, d=.12, duty=.25):
    """A pulse-wave blip, the voxel world's voice."""
    n = int(d * SR)
    t = np.arange(n) / SR
    ph = (hz(m) * t) % 1
    x = np.where(ph < duty, 1.0, -1.0) - (2 * duty - 1)
    return lp(x, 6000) * np.minimum(1, t / .002) * np.exp(-t * 9) * .35


DM, BB, FF, CC = [62, 65, 69], [58, 62, 65], [60, 65, 69], [60, 64, 67]
NIGHT, NROOT = [DM, BB, FF, CC], [38, 34, 41, 36]
F2, C2, D2, B2 = [65, 69, 72, 76], [64, 67, 72, 76], [62, 65, 69, 74], [62, 65, 70, 74]
DAY, DROOT = [F2, C2, D2, B2], [41, 36, 38, 34]
LOFI, LROOT = [[64, 67, 71, 74], [62, 65, 69, 72], [60, 64, 67, 71], [59, 62, 67, 69]], [40, 38, 36, 43]


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

    def groove(a, b, g=1.0, prog=DAY, root=DROOT, cut=2600, arp=True, clap_=True, chipy=True):
        for t, k in beats(a, b):
            c = bar(t, a)
            put(kick(), t, "drums", .7 * g); kicks.append(t)
            if k % 2 and clap_:
                put(clap(), t, "drums", .45 * g)
            put(hat(), t + BEAT / 2, "drums", .35 * g, .2)
            if k % 4 == 0:
                put(supersaw(prog[c], 4 * BEAT, cut, .05, .3, .9), t, "chords", .5 * g)
                put(sub(root[c], 4 * BEAT - .05), t, "bass", .6 * g)
            if arp:
                for s_ in range(2):
                    m = prog[c][(k * 2 + s_) % len(prog[c])] + 12
                    put(chip(m, .14) if chipy else pluck(m, .22, 1.2), t + s_ * BEAT / 2, "keys", .3 * g, (s_ - .5) * .6)

    def lofi(a, b, g=1.0, cut=2200, keys=True):
        for t, k in beats(a, b):
            c = bar(t, a)
            if k % 4 in (0, 2) or k % 8 == 7:
                put(kick(), t, "drums", .45 * g); kicks.append(t)
            if k % 4 in (1, 3):
                put(snare(), t, "drums", .25 * g)
            put(hat(), t + BEAT / 2, "drums", .18 * g, .2)
            if k % 4 == 0:
                put(supersaw(LOFI[c], 4 * BEAT, cut, .15, .4, .8), t, "chords", .38 * g)
                put(sub(LROOT[c], 4 * BEAT - .05), t, "bass", .5 * g)
            if keys and k % 2 == 0:
                put(pluck(LOFI[c][(k // 2) % 3] + 12, .5, .7), t + (BEAT / 4 if k % 4 == 2 else 0), "keys", .22 * g, (k % 3 - 1) * .4)
    cut = C["cuts"]
    L_, E_ = C["l"], C["e"]
    # the desk at dusk
    put(bell(81, 1.2), .05, "keys", .3)
    lofi(0, cut[0] - .05, .9)
    put(taiko(1.1), C["three"] + .05, "drums", .8)
    put(pluck(64, .6, .6), C["zero"], "keys", .45); put(pluck(60, .9, .6), C["zero"] + .3, "keys", .45)
    # step 1 + 2: the memo, thirty ideas
    for st in ("step1", "step2", "step3", "step4"):
        put(riser(.6, .5), C[st] - .6, "fx"); put(bell(88, 1.0), C[st], "keys", .35)
    lofi(cut[0], cut[2] - .05, .85)
    for k in range(10):
        put(chip(84 + (k % 5) * 2, .08), C["thirty7"] + k * .07, "keys", .22, (k % 2 - .5) * .6)
    for k, m in enumerate([84, 88, 91]):
        put(bell(m, 1.0), C["thirty8"] + k * .1, "keys", .35)
    # step 3 + 4: slides, a month fills in, the cheer
    lofi(cut[2], C["month"] - .3, .85)
    put(riser(C["month"] - C["schedule"] + .1, .6), C["schedule"] - .1, "fx")
    put(taiko(1.4), C["month"] - .1, "drums", 1.0); put(crash(), C["month"] - .1, "drums", .7)
    for k in range(6):
        put(bell(84 + k * 2, .9), C["month"] + k * .08, "keys", .35, (k - 2.5) * .3)
    lofi(C["month"], cut[4] - .05, 1.0, 3200)
    # the morning: brighter, a hit on eighty thousand
    lofi(cut[4], cut[5] - .05, .95, 3600)
    put(taiko(1.3), C["eighty"] - .05, "drums", .9); put(crash(), C["eighty"] - .05, "drums", .6)
    # "just be me": a sneaky pluck line, the beat drops for "No."
    for t, k in beats(cut[5], C["no"] - .15, BEAT / 2):
        put(pluck([69, 72, 71, 67][k % 4], .25, .9), t, "keys", .3, (k % 2 - .5) * .5)
        if k % 2 == 0:
            put(kick(), t, "drums", .3); kicks.append(t)
    put(sub(33, .8), C["no"], "bass", .6)
    put(bell(69, 1.6), C["why"] + .2, "keys", .3)
    # your voice is the content: a warm pad
    put(supersaw([60, 64, 67, 71], cut[7] - cut[6] + .3, 1800, .4, .6, .9), cut[6], "chords", .45)
    put(bell(84, 1.6), C["voice"], "keys", .35)
    # close
    last = int((C["end"] - .3) / BEAT) * BEAT
    lofi(cut[7], last, 1.0, 3000)
    put(taiko(1.2), last, "drums", .9); put(crash(), last, "drums", .7)
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
    gain = {"drums": .09, "bass": .07, "chords": .065, "keys": .06, "fx": .03}
    out = sum(BUS[k] * (gain[k] / rms(BUS[k])) for k in BUS)
    return np.tanh(out * 2.2) / 2.2
