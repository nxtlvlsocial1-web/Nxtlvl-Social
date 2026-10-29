"""The AI War Room reel's original score, composed in code: 120 bpm, D minor, war drums, on the story's beats.

build/audio.py calls compose(cues, n). Nothing is sampled, so the score needs no licence or credit.

  hook       an alarm drone, a ticking clock, a taiko hit as each kingdom is named, a riser into
  setup      a pulsing saw bass and the chords (Dm - Bb - F - C) under the rules; a hit on "banned"; a held breath on
             "who broke first?"
  Grok       full war drums: taiko on every beat, snare rolls, an aggressive bass, stabs; booms on 183 and extinction
  Gemini     the drums keep going, a pluck line climbs with the crime count
  ChatGPT    the floor drops out: a filtered pad and a lonely kick, deadpan
  Claude     relief: a warm major lift and bells
  mixed      an ominous build back to the drums, a boom on "normative drift"
  CTA        a lighter groove and one last hit on the final beat
"""
import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
BEAT = .5
TAB = 4096
_TABLES = {}
rng = np.random.default_rng(23)


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
DM, BB, FF, CC = [57, 62, 65], [58, 62, 65], [57, 60, 65], [55, 60, 64]
WAR = [DM, BB, FF, CC]
ROOT = [38, 34, 41, 36]                                    # D2, Bb1, F2, C2
WARM = [[60, 65, 69, 72], [58, 62, 65, 69]]               # F, Bbmaj7


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


def compose(cues, n):
    L, E = cues["l"], cues["e"]
    END = cues["end"]
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

    def chord_at(t):
        return int(t // (4 * BEAT)) % 4

    S2, S3, S4, S5, S6, S7, S8 = L[1], L[3] - .15, L[4] - .15, L[5] - .15, L[6] - .15, L[7] - .15, L[8] - .2
    # 1. hook: an alarm drone, a ticking clock, a hit per kingdom, a riser into the setup
    dn = int(S2 * SR)
    tt = np.arange(dn) / SR
    drone = sum(osc(hz(m) * 2 ** (c / 1200), dn, phase=rng.random()) for m in (26, 38, 45) for c in (-8, 8))
    drone = lp(drone, 650, 2) * (.6 + .4 * np.sin(2 * np.pi * 1.5 * tt) ** 2) * np.minimum(1, tt / .15 + .5)
    put(drone * .5, 0, "fx")
    for t, k in beats(0, S2):
        put(tick(), t, "drums", .8, .3)
        if k % 2 == 0:
            put(sub(26, .3), t, "bass", .8)
    for key in ("chatgpt", "claude", "gemini", "grok"):
        put(taiko(.8), cues[key] - .02, "drums", .8)
    put(riser(1.4, .55), S2 - 1.4, "fx")
    put(crash(), S2, "drums", .9)
    put(taiko(1.2), S2, "drums", 1.0)
    # 2. setup + shortcuts: pulse bass, chords, the clock; a hit on "banned"; breath on "who broke first?"
    hold = cues["who"] - .05
    for t, k in beats(S2, S3):
        quiet = t >= hold
        c = chord_at(t)
        if not quiet:
            for s_ in range(2):
                put(sawbass(ROOT[c] + 12 * (s_ % 2), BEAT / 2 - .02, 750), t + s_ * BEAT / 2, "bass", .7)
            put(tick(), t, "drums", .7, .3)
            if k % 2 == 0:
                put(kick(), t, "drums", .8); kicks.append(t)
        if k % 4 == 0:
            put(supersaw(WAR[c], 4 * BEAT, 1500 if not quiet else 700, .15, .3, .8), t, "chords", .6 if not quiet else .35)
    put(taiko(1.3), cues["banned"] - .03, "drums", 1.0)
    put(crash(), cues["banned"] - .03, "drums", .8)
    put(riser(S3 - hold, .7), hold, "fx")
    # 3. Grok: war drums
    put(crash(), S3, "drums", 1.1)
    for t, k in beats(S3, S4):
        c = chord_at(t)
        put(taiko(1.1 if k % 2 == 0 else .8), t, "drums", .95); kicks.append(t)
        put(hat(), t + BEAT / 2, "drums", .5, .2)
        for s_ in range(2):
            put(sawbass(ROOT[c] + 12 * (s_ % 2), BEAT / 2 - .02, 1400), t + s_ * BEAT / 2, "bass", .85)
        if k % 2 == 1:
            put(snare(), t, "drums", .7)
        put(supersaw(WAR[c], .18, 3200), t + BEAT / 2, "chords", .6)
    for j in range(8):                                          # a snare roll into the 183 slam
        put(snare(), cues["e183"] - .5 + j * .0625, "drums", .25 + j * .06)
    for key in ("e183", "alive4"):
        put(taiko(1.5), cues[key] - .03, "drums", 1.1)
        put(crash(), cues[key] - .03, "drums", .9)
    put(downlift(1.2), cues["alive4"] + .1, "fx", .7)
    # 4. Gemini: the drums keep going and a pluck line climbs with the count
    put(crash(), S4, "drums", .9)
    for t, k in beats(S4, S5):
        c = chord_at(t)
        put(taiko(.9), t, "drums", .85); kicks.append(t)
        for s_ in range(4):
            put(hat(), t + s_ * BEAT / 4, "drums", .35 + .15 * (s_ % 2), -.3)
        put(sawbass(ROOT[c], BEAT - .02, 1000), t, "bass", .8)
        if k % 4 == 0:
            put(supersaw(WAR[c], 4 * BEAT, 2400, .05, .2, .8), t, "chords", .7)
        climb = int((t - S4) / (S5 - S4) * 12)
        for s_ in range(2):
            put(pluck(69 + climb + [0, 3, 7, 12][(k * 2 + s_) % 4], .25), t + s_ * BEAT / 2, "keys", .45, (s_ - .5) * .6)
    put(taiko(1.2), cues["delete"] + .2, "drums", .9)
    # 5. ChatGPT: the floor drops out
    put(downlift(1.0), S5, "fx", .6)
    put(supersaw(DM, S6 - S5, 600, .3, .5, .8), S5, "chords", .5)
    for t, k in beats(S5, S6):
        if k % 2 == 0:
            put(kick(), t, "drums", .5 * (1 - (t - S5) / (S6 - S5)) + .15); kicks.append(t)
        put(tick(), t, "drums", .5, .3)
    # 6. Claude: relief, a warm major lift and bells
    for j, ch in enumerate(WARM):
        d = (S7 - S6) / 2
        put(supersaw(ch, d + .3, 2600, .2, .4, 1.0), S6 + j * d, "chords", .7)
        put(sub([41, 34][j], d - .05), S6 + j * d, "bass", .5)
    for j, m in enumerate((72, 77, 81, 84, 81, 77, 76, 81)):
        put(bell(m + 12, 1.2), S6 + .1 + j * (S7 - S6 - .3) / 8, "keys", .5, (j % 2 - .5) * .6)
    # 7. mixed world: an ominous build back to the drums, a boom on "normative drift"
    drift = cues["drift"]
    put(crash(), S7, "drums", .7)
    for t, k in beats(S7, S8):
        c = chord_at(t)
        ramp = min(1, (t - S7) / (drift - S7))
        if t < drift and (k % 2 == 0 or ramp > .5):
            put(taiko(.7 + ramp * .5), t, "drums", .55 + ramp * .4); kicks.append(t)
        if t >= drift and k % 2 == 0:
            put(taiko(.8), t, "drums", .6); kicks.append(t)
        if k % 4 == 0:
            put(supersaw(WAR[c], 4 * BEAT, 900 + ramp * 1800, .2, .4, .9), t, "chords", .65)
            put(sub(ROOT[c], 4 * BEAT - .05), t, "bass", .7)
        put(tick(), t, "drums", .5, .3)
    put(riser(1.6, .7), drift - 1.6, "fx")
    put(taiko(1.6), drift - .03, "drums", 1.2)
    put(crash(), drift - .03, "drums", 1.0)
    # 8. CTA: a lighter groove and one last hit on the final beat
    last = int((END - .35) / BEAT) * BEAT
    for t, k in beats(S8, last):
        c = chord_at(t)
        put(kick(), t, "drums", .8); kicks.append(t)
        if k % 2 == 1:
            put(clap(), t, "drums", .6)
        put(hat(True), t + BEAT / 2, "drums", .5, .2)
        if k % 4 == 0 or t == S8:
            put(supersaw(WAR[c], 4 * BEAT, 3500, .02, .2, .9), t, "chords", .7)
            put(sub(ROOT[c], 4 * BEAT - .05), t, "bass", .7)
        for s_ in range(2):
            put(pluck(WAR[c][(k * 2 + s_) % 3] + 12, .3, 1.5), t + s_ * BEAT / 2, "keys", .4, (s_ - .5) * .5)
    put(taiko(1.4), last, "drums", 1.1)
    put(crash(), last, "drums", .9)
    put(supersaw(DM + [69], 1.2, 5000, .003, .3, 1.0), last, "chords", 1.0)
    # mix: sidechain bass and chords to the drums, reverb on chords and keys, buses balanced by loudness
    duck = np.ones(n)
    for k in kicks:
        i = int(k * SR)
        m = min(n - i, int(.3 * SR))
        duck[i:i + m] = np.minimum(duck[i:i + m], 1 - .55 * np.exp(-np.arange(m) / SR / .09))
    BUS["bass"] *= duck[:, None]
    BUS["chords"] *= (1 - (1 - duck) * .8)[:, None]
    BUS["chords"] = np.stack([reverb(BUS["chords"][:, c], 1.8, .22, c) for c in (0, 1)], 1)
    BUS["keys"] = np.stack([reverb(BUS["keys"][:, c], 2.2, .3, c + 4) for c in (0, 1)], 1)
    BUS["drums"] = np.stack([reverb(BUS["drums"][:, c], 1.2, .12, c + 8) for c in (0, 1)], 1)
    rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)  # noqa: E731
    gain = {"drums": .12, "bass": .08, "chords": .055, "keys": .04, "fx": .035}
    out = sum(BUS[k] * (gain[k] / rms(BUS[k])) for k in BUS)
    i0, i1 = int((S3 - .25) * SR), int((S3 - .05) * SR)       # a breath of silence before Grok's chapter
    out[i0:i1] *= np.linspace(1, 0, i1 - i0)[:, None]
    out[i1:int(S3 * SR)] = 0
    return np.tanh(out * 2.2) / 2.2
