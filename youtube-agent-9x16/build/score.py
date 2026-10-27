"""The reel's original score, composed in code: 120 bpm, F minor, on the reel's own energy curve.

build/audio.py calls compose(cues, n) when no licensed track has been picked (build/track.json); nothing here is sampled,
so the score needs no licence or credit.

  0 s        BAD CHAOS   no beat yet: an alarm-pulsed drone, a heartbeat sub that speeds up, ticking hats, a reverse
                         swell into Claude's burst
  burst      GROOVE      the beat lands with Claude: kick, offbeat hats, sub bass, chord stabs (Fm - Db - Ab - Eb)
  "Not one"  BREAK       the kick drops out under "Not one skill...", a riser pulls to
  "eleven"   FULL        crash, claps, 16th hats, a pluck arp; the groove runs under the five skills
  calm       CALM        the drums stop dead; a warm pad and a slow music-box line, then a riser and 60 ms of silence
  drop       GOOD CHAOS  "Virality.": a bigger kick, rolling saw bass, wide supersaw chords, the lead hook
  landing    SUNRISE     lighter and brighter (plucks, pad, claps) until "Comment YOUTUBE" brings the chords back
  end        BUTTON      one last chord hit on the final beat
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
FM, DB, AB, EB = [53, 56, 60, 63], [49, 53, 56, 60], [51, 56, 60, 63], [51, 55, 58, 62]   # Fm7, Dbmaj7, Ab/Eb, Ebmaj7
ROOTS = {0: 41, 1: 37, 2: 32, 3: 39}                                                   # F2, Db2, Ab1, Eb2
PROG = [FM, DB, AB, EB]
HOOK = [(0, 72, .5), (.5, 75, .5), (1, 77, .25), (1.25, 75, .25), (1.5, 72, .5), (2, 70, .5), (2.5, 72, 1.0),
        (4, 68, .5), (4.5, 70, .5), (5, 72, .25), (5.25, 75, .25), (5.5, 77, .5), (6, 79, .5), (6.5, 77, 1.0)]


def compose(cues, n):
    L, E = cues["l"], cues["e"]
    B0, DROP, LAND, END = L[1], L[9], L[10], cues["end"]
    CALM = E[7] + .05
    ELEVEN = B0 + round((cues["eleven"] - B0) / BEAT) * BEAT     # the nearest beat to "eleven"
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

    def beats(a, b, step=BEAT, origin=B0):
        k0 = int(np.ceil((a - origin) / step - 1e-6))
        t = origin + k0 * step
        while t < b - 1e-6:
            yield t, int(round((t - origin) / step))
            t += step

    # 1. BAD CHAOS: an alarm drone, a heartbeat that quickens, ticks, a reverse swell into the burst
    dn = int(B0 * SR)
    tt = np.arange(dn) / SR
    drone = sum(osc(hz(m) * 2 ** (c / 1200), dn, phase=rng.random()) for m in (29, 41, 48) for c in (-9, 9))
    drone = lp(drone, 700, 2) * (.55 + .45 * np.sign(np.sin(2 * np.pi * 6 * tt))) * np.minimum(1, tt / .25) * (.6 + .4 * tt / B0)
    put(drone * .5, 0, "fx")
    t, gap = .05, .55
    while t < B0 - .15:
        put(sub(29, .22) * .9, t, "bass")
        t += gap
        gap = max(.17, gap * .86)
    t, gap = 0.0, .25
    while t < B0 - .1:
        put(hat(), t, "drums", .7, np.sin(t * 9) * .5)
        t += gap
        gap = max(.08, gap * .93)
    put(riser(1.3, .5), B0 - 1.3, "fx")

    # 2. GROOVE from the burst: kick, offbeat hats, sub, chord stabs; the break under "Not one skill..."; full on "eleven"
    put(crash(), B0, "drums", .9)
    for t, k in beats(B0, CALM):
        brk = L[2] - .05 <= t < ELEVEN
        full = t >= ELEVEN
        bar, beat = (k // 4) % 4, k % 4
        if not brk:
            put(kick(), t, "drums", 1.0)
            kicks.append(t)
            put(hat(True), t + BEAT / 2, "drums", .8 if full else .6, .2)
        if full and beat in (1, 3):
            put(clap(), t, "drums", .8)
        if full:
            for s in range(4):
                put(hat(), t + s * BEAT / 4, "drums", .45 + .2 * (s % 2), -.3)
        if beat == 0:
            dur = 4 * BEAT
            put(sub(ROOTS[bar], dur - .02), t, "bass", .0 if brk else .9)
            if brk:
                put(supersaw(PROG[bar], dur, 900, .2, .4), t, "chords", .8)
        if not brk:                                       # a chord stab on every offbeat
            put(supersaw(PROG[bar], .2, 2600 if full else 1800), t + BEAT / 2, "chords", .7)
        if full:
            arp = PROG[bar] + [PROG[bar][0] + 12]
            for s in range(4):
                put(pluck(arp[(k * 4 + s) % len(arp)] + 12, .3), t + s * BEAT / 4, "keys", .45, np.sin((k * 4 + s) * 1.3) * .5)
    put(riser(ELEVEN - L[2] - .1, .45), L[2] + .1, "fx")
    put(crash(), ELEVEN, "drums", 1.0)

    # 3. CALM: the drums stop dead; a warm pad and a slow music-box line; a riser and a breath of silence before the drop
    put(downlift(1.2), CALM, "fx", .4)
    cd = DROP - CALM
    put(supersaw(DB, cd + .3, 750, .35, .6, .9), CALM, "chords", .45)
    put(sub(37, cd - .1) * .5, CALM, "bass", .18)
    for i, m in enumerate((72, 75, 77, 80, 79, 75)):
        if CALM + .25 + i * .42 < DROP - .5:
            put(bell(m + 12), CALM + .25 + i * .42, "keys", .4, (i % 2 - .5) * .6)
    put(riser(.9, .9), DROP - .96, "fx")

    # 4. GOOD CHAOS from "Virality.": a bigger kick, rolling saw bass, wide supersaws, the lead hook
    put(crash(), DROP, "drums", 1.2)
    put(kick(True) * 1.3, DROP, "drums")
    for t, k in beats(DROP, LAND, origin=DROP):
        bar, beat = (k // 4) % 4, k % 4
        put(kick(True), t, "drums", 1.05)
        kicks.append(t)
        if beat in (1, 3):
            put(clap(), t, "drums", .9)
            put(snare(), t, "drums", .5)
        put(hat(True), t + BEAT / 2, "drums", .85, .2)
        for s in range(4):
            put(hat(), t + s * BEAT / 4, "drums", .5 + .25 * (s % 2), -.3)
        for s in range(2):                                # octave-jumping eighths
            put(sawbass(ROOTS[bar] + 12 * s, BEAT / 2 - .01, 1100), t + s * BEAT / 2, "bass", .8)
        if beat == 0:
            put(sub(ROOTS[bar], 4 * BEAT - .02), t, "bass", .7)
            put(supersaw(PROG[bar], 4 * BEAT, 5200, .005, .15, .9), t, "chords", 1.0)
    for off, m, d in HOOK:
        if DROP + off * BEAT * 2 < LAND - .2:
            put(lead(m, d * BEAT * 2 - .02), DROP + off * BEAT * 2, "keys", .8)

    # 5. SUNRISE: lighter and brighter, the chords back on "Comment YOUTUBE", a button on the last beat
    put(downlift(1.0), LAND - .05, "fx", .6)
    YT = cues["youtube"]
    last = DROP + int((END - .3 - DROP) / BEAT) * BEAT
    put(crash(), YT - .05, "drums", .9)
    first = True
    for t, k in beats(LAND, last, origin=DROP):
        bar, beat = (k // 4) % 4, k % 4
        big = t >= YT - .3
        put(kick(), t, "drums", .95)
        kicks.append(t)
        if beat in (1, 3):
            put(clap(), t, "drums", .75)
        put(hat(True), t + BEAT / 2, "drums", .6, .2)
        if big:
            for s in range(2):
                put(hat(), t + BEAT / 4 + s * BEAT / 2, "drums", .5, -.3)
        if beat == 0 or first:
            first = False
            dur = 4 * BEAT - beat * BEAT
            put(sub(ROOTS[bar], dur - .02), t, "bass", .8)
            put(supersaw(PROG[bar], dur, 6000 if big else 1600, .02 if big else .15, .2, .9), t, "chords", 1.0 if big else .7)
        arp = PROG[bar] + [PROG[bar][0] + 12, PROG[bar][1] + 12]
        for s in range(4):
            put(pluck(arp[(k * 4 + s) % len(arp)] + 12, .32, 1.6), t + s * BEAT / 4, "keys", .5, np.sin((k * 4 + s) * 1.1) * .5)
    put(kick(True), last, "drums", 1.1)
    put(crash(), last, "drums", .9)
    put(supersaw(FM + [65], 1.2, 6000, .003, .3, 1.0), last, "chords", 1.2)
    put(sub(41, .9), last, "bass", .9)

    # mix: sidechain the bass and the chords to the kicks, reverb on the keys and chords, buses balanced by loudness
    t = np.arange(n) / SR
    duck = np.ones(n)
    for k in kicks:
        i = int(k * SR)
        m = min(n - i, int(.3 * SR))
        duck[i:i + m] = np.minimum(duck[i:i + m], 1 - .6 * np.exp(-np.arange(m) / SR / .09))
    BUS["bass"] *= duck[:, None]
    BUS["chords"] *= (1 - (1 - duck) * .9)[:, None]
    BUS["chords"] = np.stack([reverb(BUS["chords"][:, c], 1.8, .22, c) for c in (0, 1)], 1)
    BUS["keys"] = np.stack([reverb(BUS["keys"][:, c], 2.2, .3, c + 4) for c in (0, 1)], 1)
    rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)  # noqa: E731
    gain = {"drums": .11, "bass": .085, "chords": .055, "keys": .04, "fx": .03}
    out = sum(BUS[k] * (gain[k] / rms(BUS[k][int(B0 * SR):] if k != "fx" else BUS[k])) for k in BUS)
    out = np.tanh(out * 2.2) / 2.2                       # gentle bus glue
    i0, i1 = int((DROP - .09) * SR), int((DROP - .06) * SR)   # a breath of silence right before the drop
    out[i0:i1] *= np.linspace(1, 0, i1 - i0)[:, None]
    out[i1:int(DROP * SR)] = 0
    return out
