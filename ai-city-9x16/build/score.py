"""The AI City reel's original score, composed in code: 116 bpm, F major / D minor, on the story's beats.

build/audio.py calls compose(cues, n). Nothing is sampled, so the score needs no licence or credit.

  hook      a soft pad, a ticking clock, a sub pulse; a bell as the orb wakes; a riser into the morning
  6 AM      a bright pluck arpeggio and a light four-on-the-floor (F - C - Am - G); a bell sweep on "syncs"
  noon      the full groove: claps, hats, bass, wide chords
  4 PM      the floor drops: a filtered minor pad, the clock ticking again, pings, a riser to a hit on "bridge"
  chaos     fast tom-and-snare drums, an alarm saw, hits on the power cut; a hard stop on "freezes"
  midnight  silence, then a warm pad swells as the AI fixes the city; a detuned glitch on "nobody can explain"
  morning   a reflective pad over a soft beat that builds
  CTA       a light groove and one last hit
"""
import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
BEAT = 60 / 116
TAB = 4096
_TABLES = {}
rng = np.random.default_rng(31)

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


FF, CC, AM, GG = [65, 69, 72], [64, 67, 72], [64, 69, 72], [62, 67, 71]
DAY = [FF, CC, AM, GG]
DROOT = [41, 36, 45, 43]                                   # F2, C2, A2, G2
DMN, BBM = [62, 65, 69], [58, 62, 65]
TENSE = [DMN, BBM, DMN, [61, 64, 69]]                      # Dm, Bb, Dm, A
TROOT = [38, 34, 38, 33]


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

    bar = lambda t: int(t // (4 * BEAT)) % 4  # noqa: E731
    S2, S3, S4, S5, S6, S7, S8 = L[1] - .1, L[2] - .1, L[3] - .1, L[4] - .1, L[5] - .1, L[6] - .1, L[7] - .1
    # 1. hook: pad, ticking clock, sub pulse, a bell as the orb wakes, a riser into the morning
    put(supersaw([53, 60, 65, 69], S2, 900, 1.2, .6, .9), 0, "chords", .5)
    put(bell(84, 2.0), .15, "keys", .7)
    put(bell(91, 2.0), .45, "keys", .4, .4)
    for t, k in beats(0, S2):
        put(tick(), t, "drums", .7, .3)
        if k % 2 == 0:
            put(sub(29, .35), t, "bass", .6)
    for key in ("mayor", "cops"):
        put(kick(True), cues[key] - .02, "drums", .9); kicks.append(cues[key] - .02)
    put(riser(1.5, .6), S2 - 1.5, "fx")
    # 2. 6 AM: pluck arpeggio, light four-on-the-floor; a bell sweep as the lights sync
    put(crash(), S2, "drums", .7)
    for t, k in beats(S2, S3):
        c = bar(t - S2)
        put(kick(), t, "drums", .75); kicks.append(t)
        put(hat(), t + BEAT / 2, "drums", .45, .25)
        if k % 4 == 0:
            put(supersaw(DAY[c], 4 * BEAT, 2200, .05, .3, .8), t, "chords", .55)
            put(sub(DROOT[c], 4 * BEAT - .05), t, "bass", .6)
        for s_ in range(2):
            put(pluck(DAY[c][(k * 2 + s_) % 3] + 12, .28, 1.2), t + s_ * BEAT / 2, "keys", .4, (s_ - .5) * .6)
    for j, m in enumerate((84, 88, 91, 96)):
        put(bell(m, 1.0), cues["syncs"] + j * .07, "keys", .45, (j - 1.5) / 2)
    # 3. noon: the full groove
    put(crash(), S3, "drums", .9)
    for t, k in beats(S3, S4):
        c = bar(t - S3)
        put(kick(), t, "drums", .9); kicks.append(t)
        if k % 2 == 1:
            put(clap(), t, "drums", .65)
        for s_ in range(2):
            put(hat(s_ == 1), t + s_ * BEAT / 2, "drums", .4, -.2)
        if k % 4 == 0:
            put(supersaw(DAY[c] + [DAY[c][0] + 12], 4 * BEAT, 3600, .02, .25, 1.0), t, "chords", .65)
        for s_ in range(2):
            put(sawbass(DROOT[c] + 12 * s_, BEAT / 2 - .02, 1200), t + s_ * BEAT / 2, "bass", .7)
        put(pluck(DAY[c][k % 3] + 24, .2, 1.4), t + BEAT * .75, "keys", .3, .4)
    # 4. 4 PM: the floor drops, ticking again, sensor pings, a riser to a hit on "bridge"
    put(downlift(1.0), S4, "fx", .6)
    put(supersaw(DMN, S5 - S4, 700, .4, .5, .9), S4, "chords", .55)
    for t, k in beats(S4, S5):
        put(tick(), t, "drums", .8, .3)
        if k % 2 == 0:
            put(sub(26, .4), t, "bass", .7)
    for j in range(3):
        put(bell(93, .6), cues["sensor"] + j * .35, "keys", .4, .5)
    put(riser(cues["bridge"] - cues["reroutes"] + .1, .8), cues["reroutes"] - .1, "fx")
    put(taiko(1.4), cues["bridge"] - .03, "drums", 1.1)
    put(crash(), cues["bridge"] - .03, "drums", .8)
    # 5. chaos: fast drums, an alarm saw, hits on the cut, a hard stop on "freezes"
    stop = cues["freezes"] + .25
    for t, k in beats(S5, stop, BEAT / 2):
        c = bar(t - S5)
        put(taiko(.9 if k % 2 == 0 else .6), t, "drums", .8); kicks.append(t)
        if k % 4 == 2:
            put(snare(), t, "drums", .7)
        if k % 8 == 0:
            put(sawbass(TROOT[c], 4 * BEAT - .05, 1600), t, "bass", .8)
            put(supersaw(TENSE[c], 4 * BEAT, 2600, .02, .1, 1.0), t, "chords", .6)
    alarm = osc(hz(81), int(2.2 * SR), "saw") * (.5 + .5 * np.sign(np.sin(2 * np.pi * 2.5 * np.arange(int(2.2 * SR)) / SR)))
    put(lp(alarm, 2400) * .35, cues["locks"], "fx")
    for key in ("cuts", "tiny"):
        put(taiko(1.5), cues[key] - .03, "drums", 1.1)
        put(crash(), cues[key] - .03, "drums", .8)
    put(taiko(1.7), cues["freezes"] - .02, "drums", 1.2)
    # 6. midnight: a warm pad swells with the fix, then a detuned glitch on "nobody"
    put(supersaw([53, 60, 64, 69], cues["nobody"] - cues["fixes"] + .4, 2400, .8, .4, 1.0), cues["fixes"] - .1, "chords", .7)
    for j, m in enumerate((72, 77, 81, 84, 89)):
        put(bell(m + 12, 1.2), cues["fixes"] + .1 + j * .22, "keys", .5, (j % 2 - .5) * .6)
    put(supersaw([62, 63, 68], S7 - cues["nobody"] + .3, 900, .3, .5, .9), cues["nobody"] - .1, "chords", .45)
    put(downlift(1.2), cues["nobody"], "fx", .5)
    # 7. morning: reflective pad over a soft beat that builds
    for t, k in beats(S7, S8):
        c = bar(t - S7)
        g = min(1, (t - S7) / (S8 - S7))
        if k % 2 == 0 or g > .5:
            put(kick(), t, "drums", .35 + .45 * g); kicks.append(t)
        put(hat(), t + BEAT / 2, "drums", .25 + .2 * g, .2)
        if k % 4 == 0:
            put(supersaw(DAY[c], 4 * BEAT, 1400 + 1800 * g, .2, .4, .9), t, "chords", .6)
            put(sub(DROOT[c], 4 * BEAT - .05), t, "bass", .55)
        put(pluck(DAY[c][k % 3] + 12, .3, .9), t, "keys", .3, .3)
    put(riser(1.2, .5), S8 - 1.2, "fx")
    # 8. CTA: a light groove and one last hit
    last = int((END - .35) / BEAT) * BEAT
    for t, k in beats(S8, last):
        c = bar(t - S8)
        put(kick(), t, "drums", .8); kicks.append(t)
        if k % 2 == 1:
            put(clap(), t, "drums", .6)
        put(hat(True), t + BEAT / 2, "drums", .45, .2)
        if k % 4 == 0 or t == S8:
            put(supersaw(DAY[c], 4 * BEAT, 3500, .02, .2, .9), t, "chords", .7)
            put(sub(DROOT[c], 4 * BEAT - .05), t, "bass", .7)
        for s_ in range(2):
            put(pluck(DAY[c][(k * 2 + s_) % 3] + 12, .3, 1.5), t + s_ * BEAT / 2, "keys", .4, (s_ - .5) * .5)
    put(taiko(1.3), last, "drums", 1.0)
    put(crash(), last, "drums", .9)
    put(supersaw(FF + [77], 1.2, 5000, .003, .3, 1.0), last, "chords", 1.0)
    # mix: sidechain, reverb, buses balanced by loudness; a breath of silence before the midnight
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
    i0, i1 = int((stop - .02) * SR), int((cues["fixes"] - .15) * SR)
    out[i0:i1] *= .06
    return np.tanh(out * 2.2) / 2.2
