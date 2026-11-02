"""The AI Clone reel's original score, composed in code: 112 bpm, chiptune colours over a soft electronic bed, to
match the voxel world. D minor at night, F major by day; every beat of the story gets its own turn.

build/audio.py calls compose(cues, n). Nothing is sampled, so the score needs no licence or credit.

  3 AM       a hushed pad and a clock; a square-wave arpeggio starts when the clone starts typing; a hit on "three hundred"
  day 2      a bouncy chip groove; a bell when the reply lands; a happy run when the fan laughs
  day 5      midnight: a dark pulse, a riser into the clone printing in, a tense ostinato, a hit and bells on "double"
  day 9      a warm groove; a bell for every name; a swell on "nicest creator"
  day 14     soft keys, then a drone under the voice note, a riser, a hit and a sub drop on "never spoken"
  day 30     a build into "doubled" with a crash; then a heartbeat drone under the comment and a hit on "nicer"
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

    # 1. 3 AM: a hushed pad and a clock; the clone's arpeggio; a hit on three hundred
    put(supersaw([50, 57, 62], CU[0], 700, .6, .4, .9), 0, "chords", .45)
    for t, k in beats(0, C["clone"] - .1):
        put(tick(), t, "drums", .5, .3)
        if k % 2 == 0:
            put(sub(38, .3), t, "bass", .45)
    put(bell(81, 1.4), C["asleep"], "keys", .35)
    put(bell(86, 1.2), C["clone"] - .05, "keys", .5)
    for t, k in beats(C["clone"], CU[0] - .1, BEAT / 4):
        m = NIGHT[bar(t, C["clone"])][k % 3] + 12 + (12 if k % 8 > 5 else 0)
        put(chip(m, .1), t, "keys", .32 + .12 * min(1, (t - C["clone"]) / 2), (k % 2 - .5) * .7)
        if k % 4 == 0:
            put(kick(), t, "drums", .45); kicks.append(t)
        if k % 2 == 1:
            put(hat(), t, "drums", .25, .2)
    put(taiko(1.3), C["three"], "drums", .9); put(crash(), C["three"], "drums", .5)
    put(supersaw(DM + [74], 1.2, 3500, .005, .5, 1.0), C["three"], "chords", .5)
    # 2. day 2: a bouncy chip groove; the reply lands; the laugh
    groove(CU[0], CU[1] - .05, .85, DAY, DROOT, 2400)
    for k, m in enumerate([84, 88, 91]):
        put(bell(m, 1.0), C["replies"] + .55 + k * .1, "keys", .4)
    for k in range(8):
        put(chip(79 + [0, 4, 7, 12, 7, 4, 12, 16][k], .12), C["jokes"] + .1 + k * .09, "keys", .35, (k % 2 - .5) * .6)
    # 3. day 5, midnight: a dark pulse, a riser, the print-in hit, a tense ostinato, double
    mid = C["midnight"]
    put(supersaw([38, 45, 50], mid - CU[1] + .3, 520, .4, .3, .9), CU[1], "chords", .55)
    for t, k in beats(CU[1], mid, BEAT / 2):
        put(tick(), t, "drums", .45 + .3 * (t - CU[1]) / (mid - CU[1]), .3)
        if k % 2 == 0:
            put(sub(38, .25), t, "bass", .6)
    put(riser(mid - C["dms"] + .6, .9), C["dms"] - .2, "fx")
    put(taiko(1.7), mid + .4, "drums", 1.1); put(crash(), mid + .4, "drums", .7)
    for t, k in beats(mid + .4, C["double"] - .05, BEAT / 2):
        put(chip([62, 65, 69, 70][k % 4] + 12, .12, .5), t, "keys", .35, (k % 2 - .5) * .6)
        if k % 2 == 0:
            put(kick(), t, "drums", .6); kicks.append(t)
            put(sub(38 if k % 8 < 4 else 34, .3), t, "bass", .65)
        else:
            put(hat(), t, "drums", .3)
    put(taiko(1.6), C["double"], "drums", 1.1); put(crash(), C["double"], "drums", .8)
    put(supersaw(F2, CU[2] - C["double"], 4000, .005, .6, 1.0), C["double"], "chords", .7)
    for k in range(5):
        put(bell(84 + k * 2, .9), C["double"] + .1 + k * .09, "keys", .35, (k - 2) * .3)
    # 4. day 9: a warm groove, a bell per name, a swell on nicest
    groove(CU[2], CU[3] - .05, .9, DAY, DROOT, 2800, chipy=False)
    for k, t in enumerate([C["name"], C["birthday"], C["people"] + .3]):
        put(bell(84 + k * 3, 1.0), t, "keys", .45, (k - 1) * .5)
    put(riser(C["nicest"] - C["people"] - .2, .6), C["people"] + .2, "fx")
    put(crash(), C["nicest"], "drums", .6); put(supersaw(F2 + [81], 1.6, 5000, .01, .6, 1.0), C["nicest"], "chords", .55)
    # 5. day 14: soft keys, a drone under the voice note, a hit and a sub drop on never
    nv = C["never"]
    for t, k in beats(CU[3], C["stranger"] - .1):
        c = bar(t, CU[3])
        put(pluck(DAY[c][k % 4], .5, .8), t, "keys", .35, .2)
        if k % 4 == 0:
            put(sub(DROOT[c], 4 * BEAT - .05), t, "bass", .4)
    put(supersaw([50, 57], nv - C["stranger"] + .3, 450, .8, .3, 1.0), C["stranger"], "chords", .55)
    for t, k in beats(C["thanks"], nv - .05, BEAT):
        put(heart(), t, "drums", .55)
    put(riser(nv - C["lastnight"] + .4, .9), C["lastnight"] - .4, "fx")
    put(taiko(1.9), nv, "drums", 1.2); put(crash(), nv, "drums", .8)
    put(sub(26, 1.6), nv, "bass", .9)
    put(supersaw([50, 53, 57], CU[4] - nv, 600, .3, .5, 1.0), nv + .1, "chords", .45)
    # 6. day 30: the build into doubled; then a heartbeat drone under the comment; nicer
    db = C["doubled"]
    for t, k in beats(CU[4], db - .05, BEAT / 2):
        c = bar(t, CU[4]); g = (t - CU[4]) / (db - CU[4])
        if k % 2 == 0:
            put(kick(), t, "drums", .5 + .4 * g); kicks.append(t)
        else:
            put(hat(True), t, "drums", .25 + .2 * g, .2)
        if k % 8 == 0:
            put(supersaw(DAY[c], 4 * BEAT, 1500 + 3000 * g, .03, .3, 1.0), t, "chords", .55)
            put(sub(DROOT[c], 4 * BEAT - .05), t, "bass", .6)
        put(chip(DAY[c][k % 4] + 12 + (12 if g > .5 and k % 2 else 0), .12), t, "keys", .3, (k % 2 - .5) * .6)
    put(taiko(1.5), db, "drums", 1.1); put(crash(), db, "drums", .9)
    for t, k in beats(db, C["comment"] - .2):
        c = bar(t, db)
        put(kick(), t, "drums", .8); kicks.append(t)
        if k % 2:
            put(clap(), t, "drums", .55)
        if k % 4 == 0 or t == db:
            put(supersaw(DAY[c], 4 * BEAT, 4200, .02, .2, .9), t, "chords", .7)
            put(sub(DROOT[c], 4 * BEAT - .05), t, "bass", .7)
    cm = C["comment"]
    put(downlift(1.0), cm - .1, "fx", .8)
    put(supersaw([38, 45, 50], CU[5] - cm, 420, .3, .5, 1.0), cm, "chords", .6)
    for k in range(int((CU[5] - cm) / .66)):
        put(heart(), cm + .25 + k * .66, "drums", .75)
    put(taiko(1.6), C["nicer"], "drums", 1.0)
    put(bell(74, 2.0), C["nicer"] + .05, "keys", .4)
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
        if g > .5:
            put(chip(DAY[c][(k + 2) % 4] + 24, .1), t + BEAT / 2, "keys", .22, -.3)
    put(riser(C["seven"] - C["everyone"] + .3, .7), C["everyone"] - .1, "fx")
    put(crash(), C["seven"], "drums", .55)
    put(bell(88, 1.2), C["hour"], "keys", .45)
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
