"""The AI Closer reel's original score, composed in code: 112 bpm, chiptune colours over a soft electronic bed (the voxel
world's sound), D minor at night, F major by day; every beat of the story gets its own turn.

build/audio.py calls compose(cues, n). Nothing is sampled, so the score needs no licence or credit.

  3 AM       a hushed pad and a clock; a cash-register run of bells on "seven sales"
  day 1      a bouncy chip groove; a whoosh-riser while the robot flies over; bells when the DM lands
  day 4      warm keys; a pause on "too expensive"; a lift on the story and a hit on "she buys"
  day 10     a groove that ticks forward (a day passing), bells for the ones who come back
  day 18     midnight: a dark pulse and a riser into "no", then near-silence under "not the right fit"
  day 30     the full groove and a crash on 212; a warm swell as she comes back with her friends
  real world a reflective groove that builds; close: the full groove and one last hit
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


DM, BB, FF, CC = [62, 65, 69], [58, 62, 65], [60, 65, 69], [60, 64, 67]
NIGHT, NROOT = [DM, BB, FF, CC], [38, 34, 41, 36]
F2, C2, D2, B2 = [65, 69, 72, 76], [64, 67, 72, 76], [62, 65, 69, 74], [62, 65, 70, 74]
DAY, DROOT = [F2, C2, D2, B2], [41, 36, 38, 34]


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

    # 1. 3 AM: hushed pad and clock; the sales come in
    put(supersaw([50, 57, 62], CU[0], 700, .6, .4, .9), 0, "chords", .45)
    for t, k in beats(0, C["seven"] - .1):
        put(tick(), t, "drums", .5, .3)
        if k % 2 == 0:
            put(sub(38, .3), t, "bass", .45)
    for k in range(7):
        put(bell(84 + [0, 4, 7, 12, 7, 12, 16][k], .9), C["buzzing"] - .2 + k * .27, "keys", .35, (k % 2 - .5) * .6)
    put(taiko(1.3), C["seven"], "drums", .9); put(crash(), C["seven"], "drums", .5)
    put(supersaw(F2, CU[0] - C["seven"], 2600, .01, .5, 1.0), C["seven"], "chords", .5)
    for t, k in beats(C["seven"], CU[0] - .1, BEAT / 2):
        put(chip(DAY[bar(t, C["seven"])][k % 4] + 12, .1), t, "keys", .25, (k % 2 - .5) * .6)
    # 2. day 1: the chip groove, the flight, the DM
    groove(CU[0], CU[1] - .05, .85, DAY, DROOT, 2400)
    put(riser(C["scroll"] + .6 - C["price"], .7), C["price"], "fx")
    for k, m in enumerate([84, 88, 91]):
        put(bell(m, 1.0), C["already"] + .3 + k * .1, "keys", .4)
    # 3. day 4: warm keys, the objection, the story, the sale
    for t, k in beats(CU[1], C["buys"] - .1):
        c = bar(t, CU[1])
        put(pluck(DAY[c][k % 4], .5, .8), t, "keys", .35, .2)
        if k % 4 == 0:
            put(sub(DROOT[c], 4 * BEAT - .05), t, "bass", .45)
            put(supersaw(DAY[c], 4 * BEAT, 1400 if t < C["story"] else 2600, .2, .4, .9), t, "chords", .4)
        if t > C["story"]:
            put(kick(), t, "drums", .5); kicks.append(t)
    put(riser(C["buys"] - C["student"] + .2, .6), C["student"] - .2, "fx")
    put(taiko(1.4), C["buys"], "drums", 1.0); put(crash(), C["buys"], "drums", .6)
    for k in range(5):
        put(bell(84 + k * 2, .9), C["buys"] + .1 + k * .09, "keys", .35, (k - 2) * .3)
    groove(C["buys"] + .1, CU[2] - .05, .7, DAY, DROOT, 3000)
    # 4. day 10: ticking forward; the ones who come back
    for t, k in beats(CU[2], C["half"] - .05, BEAT / 2):
        put(tick(), t, "drums", .4 + .3 * (t - CU[2]) / (C["half"] - CU[2]), .3)
        if k % 4 == 0:
            put(sub(DROOT[bar(t, CU[2])], 2 * BEAT), t, "bass", .5)
    put(supersaw([53, 57, 60], C["half"] - CU[2], 900, .3, .3, .9), CU[2], "chords", .45)
    put(riser(C["half"] - C["later"] + .1, .6), C["later"] - .1, "fx")
    put(taiko(1.3), C["half"], "drums", 1.0)
    groove(C["half"], CU[3] - .05, .9, DAY, DROOT, 3200)
    for k, m in enumerate([86, 91]):
        put(bell(m, 1.0), C["half"] + .1 + k * .15, "keys", .45)
    # 5. day 18, midnight: a dark pulse, a riser into no, near-silence
    no_ = C["no"]
    put(supersaw([38, 45, 50], no_ - CU[3] + .3, 520, .4, .3, .9), CU[3], "chords", .55)
    for t, k in beats(CU[3], no_ - .1, BEAT / 2):
        put(tick(), t, "drums", .45 + .3 * (t - CU[3]) / (no_ - CU[3]), .3)
        if k % 2 == 0:
            put(sub(38, .25), t, "bass", .6)
    for k in range(int((no_ - C["pay"]) / .66)):
        put(heart(), C["pay"] + .1 + k * .66, "drums", .6)
    put(riser(no_ - C["says"] + .5, .9), C["says"] - .4, "fx")
    put(taiko(1.8), no_, "drums", 1.1)
    put(sub(26, 1.6), no_, "bass", .8)
    put(supersaw([50, 53, 57], CU[4] - no_ - .2, 600, .4, .6, 1.0), no_ + .2, "chords", .35)
    put(bell(74, 2.0), C["fit"] + .4, "keys", .35)
    # 6. day 30: the full groove and a crash on 212; the return
    put(taiko(1.5), C["two"], "drums", 1.1); put(crash(), C["two"], "drums", .9)
    for t, k in beats(CU[4], C["woman"] - .2):
        c = bar(t, CU[4])
        put(kick(), t, "drums", .8); kicks.append(t)
        if k % 2:
            put(clap(), t, "drums", .55)
        if k % 4 == 0 or t == CU[4]:
            put(supersaw(DAY[c], 4 * BEAT, 4200, .02, .2, .9), t, "chords", .7)
            put(sub(DROOT[c], 4 * BEAT - .05), t, "bass", .7)
        put(chip(DAY[c][k % 4] + 12, .12), t + BEAT / 2, "keys", .25, .3)
    put(downlift(1.0), C["woman"] - .2, "fx", .6)
    put(supersaw([53, 57, 60, 64], C["she"] - C["woman"] + .2, 1100, .4, .3, 1.0), C["woman"] - .1, "chords", .5)
    put(riser(C["she"] - C["turned"] + .1, .6), C["turned"] - .1, "fx")
    put(crash(), C["she"], "drums", .6); put(supersaw(F2 + [81], CU[5] - C["she"], 4800, .01, .6, 1.0), C["she"], "chords", .6)
    for k, m in enumerate([84, 88, 91, 96]):
        put(bell(m, 1.0), C["friends"] - .1 + k * .1, "keys", .4, (k - 1.5) * .4)
    # 7. real world: a reflective groove that builds
    S7, S8 = CU[5], CU[6]
    for t, k in beats(S7, S8 - .05):
        c = bar(t, S7)
        g = min(1, (t - S7) / (S8 - S7))
        if k % 2 == 0 or g > .45:
            put(kick(), t, "drums", .4 + .4 * g); kicks.append(t)
        put(hat(), t + BEAT / 2, "drums", .25 + .2 * g, .2)
        if k % 4 == 0:
            put(supersaw(DAY[c], 4 * BEAT, 1500 + 2500 * g, .2, .4, .9), t, "chords", .55)
            put(sub(DROOT[c], 4 * BEAT - .05), t, "bass", .55)
        put(pluck(DAY[c][k % 4] + 12, .3, 1.0), t, "keys", .3, .3)
    put(crash(), C["every"], "drums", .5)
    put(bell(88, 1.2), C["week"], "keys", .45)
    # 8. close
    last = int((END - .35) / BEAT) * BEAT
    for t, k in beats(S8, last):
        c = bar(t, S8)
        put(kick(), t, "drums", .8); kicks.append(t)
        if k % 2:
            put(clap(), t, "drums", .6)
        put(hat(True), t + BEAT / 2, "drums", .45, .2)
        if k % 4 == 0 or t == S8:
            put(supersaw(DAY[c], 4 * BEAT, 3600, .02, .2, .9), t, "chords", .7)
            put(sub(DROOT[c], 4 * BEAT - .05), t, "bass", .7)
        for s_ in range(2):
            put(chip(DAY[c][(k * 2 + s_) % 4] + 12, .12), t + s_ * BEAT / 2, "keys", .25, (s_ - .5) * .6)
    put(taiko(1.3), last, "drums", 1.0); put(crash(), last, "drums", .9)
    put(supersaw(F2 + [81], 1.2, 5000, .003, .3, 1.0), last, "chords", 1.0)
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
