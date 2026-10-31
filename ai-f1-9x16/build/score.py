"""The AI F1 reel's original score, composed in code: 128 bpm, A minor into C major, on the story's peaks.

build/audio.py calls compose(cues, n). Nothing is sampled, so the score needs no licence or credit.

  hook       lights out: a hit, a driving 8th-note saw bass; a hit on "pits", the floor drops on "last"
  rain       a filtered pad, thunder on "rain", drums build; a hit on every overtake
  listening  a sparse data pluck over a soft kick, a riser into the hairpin pass
  crash      ticking and a sub pulse, a riser into the contact, a boom, a heartbeat through the slow motion, a hit on P1
  final lap  the anthem builds, drops out on "the AI says...", one bell, a hit on the flag
  title      a slow, warm pad with bells, a crash on "championship"
  real world a reflective groove that builds; close: a light groove and one last hit
"""
import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
BEAT = 60 / 128
TAB = 4096
_TABLES = {}
rng = np.random.default_rng(41)


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


def snare():
    n = int(.3 * SR)
    t = np.arange(n) / SR
    return (bp(rng.standard_normal(n), 1200, 8000) * np.exp(-t * 22) * .5 + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * .5) * .8


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


def sawbass(m, d, cut=900):
    n = int(d * SR)
    x = osc(hz(m), n) * .6 + osc(hz(m - 12), n, "sq") * .5
    return lp(x, cut, 2) * env(n, .003, .12, .6, .03)


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


def lead(m, d):
    n = int(d * SR)
    x = osc(hz(m), n, "sq", vib=.004) * .55 + osc(hz(m) * 1.004, n, vib=.004) * .45
    return lp(x, 3800, 2) * env(n, .008, .15, .7, .06)


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


# ---------------------------------------------------------------- the arrangement



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


AM_, FF_, CC_, GG_ = [64, 69, 72], [65, 69, 72], [64, 67, 72], [62, 67, 71]
MINOR = [AM_, FF_, CC_, GG_]
MROOT = [45, 41, 36, 43]
CC2, GG2, AM2, FF2 = [64, 67, 72, 76], [62, 67, 71, 74], [64, 69, 72, 76], [65, 69, 72, 77]
ANTHEM = [CC2, GG2, AM2, FF2]
AROOT = [36, 43, 45, 41]


def compose(cues, n):
    L, E = cues["l"], cues["e"]
    END = cues["end"]
    CU = cues["cuts"]
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
    # 1. hook: lights out, driving saw bass, the pit call, the drop to last
    put(taiko(1.5), .02, "drums", 1.1); put(crash(), .02, "drums", .8)
    put(supersaw(AM_, 1.2, 3800, .003, .4, 1.0), .02, "chords", .8)
    for t, k in beats(0, cues["drops"] - .1, BEAT / 2):
        c = bar(t, 0)
        if k % 2 == 0:
            put(kick(), t, "drums", .8); kicks.append(t)
        else:
            put(hat(), t, "drums", .4, .2)
        if k % 4 == 2:
            put(snare(), t, "drums", .45)
        put(sawbass(MROOT[c] + (12 if k % 4 == 3 else 0), BEAT / 2 - .03, 1100), t, "bass", .75)
        if k % 8 == 0:
            put(supersaw(MINOR[c], 4 * BEAT, 1800, .05, .3, .9), t, "chords", .5)
    put(taiko(1.2), cues["pits"] - .03, "drums", .9)
    put(downlift(1.2), cues["drops"] - .1, "fx", .7)
    put(taiko(1.6), cues["last"] - .03, "drums", 1.1)
    put(supersaw([45, 52, 57], CU[0] - cues["last"] + .3, 600, .05, .5, .9), cues["last"] - .03, "chords", .55)
    # 2. rain: a filtered pad, thunder, the build, a hit on every overtake
    put(supersaw([57, 60, 64], cues["rain"] - CU[0], 700, .3, .3, .9), CU[0], "chords", .5)
    for t, k in beats(CU[0], cues["rain"]):
        put(tick(), t, "drums", .6, .3)
    put(taiko(1.8), cues["rain"] - .02, "drums", 1.2); put(crash(), cues["rain"] - .02, "drums", .8)
    six = cues["six"] - .3
    for t, k in beats(cues["rain"] + .3, six):
        c = bar(t, cues["rain"])
        g = (t - cues["rain"]) / (six - cues["rain"])
        if k % 2 == 0 or g > .5:
            put(kick(), t, "drums", .5 + .35 * g); kicks.append(t)
        put(hat(), t + BEAT / 2, "drums", .25 + .2 * g, .2)
        if k % 4 == 0:
            put(supersaw(MINOR[c], 4 * BEAT, 1200 + 1800 * g, .1, .3, .9), t, "chords", .5)
            put(sub(MROOT[c], 4 * BEAT - .05), t, "bass", .6)
    put(riser(1.2, .6), six - 1.0, "fx")
    for t, k in beats(six, CU[1] - .1, BEAT / 2):
        c = bar(t, six)
        if k % 2 == 0:
            put(kick(), t, "drums", .95); kicks.append(t)
        else:
            put(hat(True), t, "drums", .4, .2)
        if k % 4 == 2:
            put(clap(), t, "drums", .6)
        put(sawbass(AROOT[c] + (12 if k % 2 else 0), BEAT / 2 - .02, 1500), t, "bass", .7)
        if k % 8 == 0:
            put(supersaw(ANTHEM[c], 4 * BEAT, 3800, .02, .25, 1.0), t, "chords", .65)
    for tp in cues["pb"]:
        put(crash(), tp, "drums", .45); put(taiko(.8), tp, "drums", .5)
    # 3. listening: a sparse data pluck, a riser into the hairpin
    for t, k in beats(CU[1], CU[2] - .1):
        c = bar(t, CU[1])
        if k % 2 == 0:
            put(kick(), t, "drums", .5); kicks.append(t)
        put(hat(), t + BEAT / 2, "drums", .25, .2)
        if k % 4 == 0:
            put(supersaw(MINOR[c], 4 * BEAT, 1300, .15, .3, .8), t, "chords", .45)
            put(sub(MROOT[c], 4 * BEAT - .05), t, "bass", .55)
        for s_ in range(2):
            put(pluck(MINOR[c][(k * 2 + s_) % 3] + 12, .2, 1.3), t + s_ * BEAT / 2, "keys", .35, (s_ - .5) * .6)
    put(riser(cues["att"] - cues["exactly"] + .2, .7), cues["exactly"] - .2, "fx")
    put(taiko(1.4), cues["att"], "drums", 1.0); put(crash(), cues["att"], "drums", .8)
    # 4. lap 40: ticking, the riser into the crash, a boom, a heartbeat in the slow motion, a hit on P1
    tc = cues["tc"]
    put(supersaw([57, 60, 63], tc - CU[2], 900, .3, .3, .9), CU[2], "chords", .5)
    for t, k in beats(CU[2], tc - .05, BEAT / 2):
        put(tick(), t, "drums", .55 + .3 * (t - CU[2]) / (tc - CU[2]), .3)
        if k % 2 == 0:
            put(sub(33, .25), t, "bass", .7)
    put(riser(tc - cues["slows"] + .1, .9), cues["slows"] - .1, "fx")
    put(taiko(2.0), tc, "drums", 1.3); put(crash(), tc, "drums", 1.0)
    put(supersaw([45, 48, 52, 57], CU[3] - tc, 500, .05, .8, 1.0), tc, "chords", .6)
    for k in range(6):
        t = cues["slowmo"][0] + k * .55
        put(kick(True), t, "drums", .7); put(kick(), t + .16, "drums", .45)
    put(taiko(1.5), cues["through"] + .2, "drums", 1.1); put(crash(), cues["through"] + .2, "drums", .8)
    put(supersaw(CC2, 1.0, 4200, .005, .5, 1.0), cues["through"] + .2, "chords", .8)
    # 5. final lap: the anthem builds, drops out on "the AI says...", one bell, a hit on the flag
    says = cues["says"] - .9
    for t, k in beats(CU[3], says):
        c = bar(t, CU[3])
        g = (t - CU[3]) / (says - CU[3])
        put(kick(), t, "drums", .6 + .35 * g); kicks.append(t)
        if k % 2:
            put(clap(), t, "drums", .4 + .25 * g)
        put(hat(True), t + BEAT / 2, "drums", .3 + .2 * g, .2)
        if k % 4 == 0:
            put(supersaw(ANTHEM[c], 4 * BEAT, 2200 + 2000 * g, .03, .3, 1.0), t, "chords", .6)
            put(sub(AROOT[c], 4 * BEAT - .05), t, "bass", .65)
        put(pluck(ANTHEM[c][k % 4] + 12, .25, 1.1), t, "keys", .25, .3)
    put(supersaw([57, 60, 64], cues["finish"] - says, 700, .4, .4, .9), says, "chords", .4)
    put(bell(81, 1.6), cues["let"] - .02, "keys", .55)
    put(riser(cues["finish"] - cues["let"], .6), cues["let"], "fx")
    put(taiko(1.6), cues["finish"], "drums", 1.1); put(crash(), cues["finish"], "drums", .9)
    # 6. the title: a slow warm pad, bells, a crash on "championship"
    for t, k in beats(cues["finish"] + .2, CU[4] - .1, 2 * BEAT):
        c = bar(t, cues["finish"])
        put(supersaw(ANTHEM[c], 2 * BEAT + .1, 1400 if t < cues["wins"] else 3200, .25, .4, .9), t, "chords", .5)
        put(sub(AROOT[c], 2 * BEAT - .05), t, "bass", .45)
        if t > cues["wins"] - .3:
            put(kick(), t, "drums", .6); kicks.append(t)
            put(clap(), t + BEAT, "drums", .45)
    put(crash(), cues["championship"], "drums", .8); put(taiko(1.2), cues["championship"], "drums", .8)
    for k, m in enumerate([76, 79, 84, 88]):
        put(bell(m, 1.4), cues["wins"] + k * .45, "keys", .35, (k % 2 - .5) * .6)
    put(bell(91, 1.6), cues["point"], "keys", .5)
    # 7. real world: a reflective groove that builds
    S7, S8 = CU[4], L[7] - .1
    for t, k in beats(S7, S8):
        c = bar(t, S7)
        g = min(1, (t - S7) / (S8 - S7))
        if k % 2 == 0 or g > .5:
            put(kick(), t, "drums", .4 + .4 * g); kicks.append(t)
        put(hat(), t + BEAT / 2, "drums", .25 + .2 * g, .2)
        if k % 4 == 0:
            put(supersaw(ANTHEM[c], 4 * BEAT, 1500 + 2000 * g, .2, .4, .9), t, "chords", .55)
            put(sub(AROOT[c], 4 * BEAT - .05), t, "bass", .55)
        put(pluck(ANTHEM[c][k % 4] + 12, .3, 1.0), t, "keys", .3, .3)
    put(bell(88, 1.2), cues["billions"] + 1.4, "keys", .45)
    # 8. close: a light groove and one last hit
    last = int((END - .35) / BEAT) * BEAT
    for t, k in beats(S8, last):
        c = bar(t, S8)
        put(kick(), t, "drums", .8); kicks.append(t)
        if k % 2:
            put(clap(), t, "drums", .6)
        put(hat(True), t + BEAT / 2, "drums", .45, .2)
        if k % 4 == 0 or t == S8:
            put(supersaw(ANTHEM[c], 4 * BEAT, 3500, .02, .2, .9), t, "chords", .7)
            put(sub(AROOT[c], 4 * BEAT - .05), t, "bass", .7)
    put(taiko(1.3), last, "drums", 1.0)
    put(crash(), last, "drums", .9)
    put(supersaw(CC2 + [79], 1.2, 5000, .003, .3, 1.0), last, "chords", 1.0)
    # mix: sidechain, reverb, buses balanced by loudness; a breath of silence before "let him through"
    duck = np.ones(n)
    for k in kicks:
        i = int(k * SR)
        m = min(n - i, int(.3 * SR))
        duck[i:i + m] = np.minimum(duck[i:i + m], 1 - .5 * np.exp(-np.arange(m) / SR / .09))
    BUS["bass"] *= duck[:, None]
    BUS["chords"] *= (1 - (1 - duck) * .7)[:, None]
    BUS["chords"] = np.stack([reverb(BUS["chords"][:, c], 1.8, .24, c) for c in (0, 1)], 1)
    BUS["keys"] = np.stack([reverb(BUS["keys"][:, c], 2.2, .3, c + 4) for c in (0, 1)], 1)
    BUS["drums"] = np.stack([reverb(BUS["drums"][:, c], 1.1, .1, c + 8) for c in (0, 1)], 1)
    rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)  # noqa: E731
    gain = {"drums": .115, "bass": .075, "chords": .06, "keys": .045, "fx": .035}
    out = sum(BUS[k] * (gain[k] / rms(BUS[k])) for k in BUS)
    i0, i1 = int((cues["says"] - .9) * SR), int((cues["let"] - .05) * SR)
    out[i0:i1] *= np.interp(np.arange(i1 - i0), [0, (i1 - i0) * .3, i1 - i0], [1, .25, .25])[:, None]
    return np.tanh(out * 2.2) / 2.2
