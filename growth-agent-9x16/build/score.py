"""The reel's original score, composed in code: 120 bpm, Ab major / F minor (Db - Ab - Eb - Fm), on the reel's energy curve.

build/audio.py calls compose(cues, n). Nothing here is sampled, so the score needs no licence or credit. It never dips:
every stretch either drives or builds toward the next hit.

  0 s        HOOK      no intro: the downbeat hits with the phone landing; kick, offbeat hats, sub, chord stabs from bar 1,
                       claps and a pluck arp join as the count starts, a riser into the 2,400 hit on "followers"
  "post."    STOP      the beat cuts out under "It doesn't just post." (filtered chords only), then slams back on "grows"
  "Five"     BUILD     claps, a snare roll that speeds up and a riser into the dive through the screen
  dive       MOVES     the drop: a bigger kick, rolling saw bass, wide supersaws, the lead hook; a crash on every move
  "And five?" BREAK    dead stop: a sub boom and a breath of near-silence
  dark lab   HALF-TIME a deep pulse at half time, a minor pad, a ticking arp that builds into "rewrites", then double time
  bonus      DROP      the brightest section: full drums, open supersaws, the hook an octave up
  CTA        GROOVE    the groove holds under the CTA and ends on one last chord hit
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
DBM, ABM, EBM, FMI = [49, 53, 56, 60], [51, 56, 60, 63], [51, 55, 58, 63], [53, 56, 60, 63]   # Dbmaj7, Ab/Eb, Eb, Fm7
PROG = [DBM, ABM, EBM, FMI]
ROOTS = {0: 37, 1: 32, 2: 39, 3: 41}                                                        # Db2, Ab1, Eb2, F2
DARK = [[41, 44, 48, 51], [37, 41, 44, 48], [39, 43, 46, 51], [36, 39, 43, 48]]             # Fm7, Db, Eb, Cm (low)
DROOTS = [29, 25, 27, 24]
HOOK = [(0, 75, .5), (.5, 72, .25), (.75, 75, .25), (1, 77, .5), (1.5, 80, .5), (2, 79, .5), (2.5, 75, .5), (3, 77, 1.0),
        (4, 75, .5), (4.5, 72, .25), (4.75, 75, .25), (5, 77, .5), (5.5, 80, .5), (6, 82, .5), (6.5, 80, 1.0)]


def compose(cues, n):
    L, E = cues["l"], cues["e"]
    END = cues["end"]
    STOP0, GROW = cues["post"] - .5, cues["grows"] - .02
    BUILD = L[3] - .05
    DIVE = cues["in0"]
    BRK = cues["dark0"]
    HALF = L[9] - .05
    RW = cues["rewrites"]
    BON = cues["out1"] + .04
    CTA = L[11] - .1
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

    def beats(a, b, step=BEAT, origin=0.0):
        k0 = int(np.ceil((a - origin) / step - 1e-6))
        t = origin + k0 * step
        while t < b - 1e-6:
            yield t, int(round((t - origin) / step))
            t += step

    def groove(a, b, origin, big=False, claps=True, hats16=False, arp=False, chords="stab", cut=2600, bass="sub", bright=1.0):
        for t, k in beats(a, b, origin=origin):
            bar, beat = (k // 4) % 4, k % 4
            put(kick(big), t, "drums", 1.05 if big else 1.0)
            kicks.append(t)
            put(hat(True), t + BEAT / 2, "drums", .75, .2)
            if claps and beat in (1, 3):
                put(clap(), t, "drums", .85)
                if big:
                    put(snare(), t, "drums", .45)
            if hats16:
                for s in range(4):
                    put(hat(), t + s * BEAT / 4, "drums", .42 + .2 * (s % 2), -.3)
            if beat == 0 or t == a:
                dur = (4 - beat) * BEAT
                put(sub(ROOTS[bar], dur - .02), t, "bass", .85)
                if chords == "pad":
                    put(supersaw(PROG[bar], dur, cut, .01, .15, .9), t, "chords", 1.0)
            if bass == "saw":
                for s in range(2):
                    put(sawbass(ROOTS[bar] + 12 * s, BEAT / 2 - .01, 1100), t + s * BEAT / 2, "bass", .75)
            if chords == "stab":
                put(supersaw(PROG[bar], .2, cut), t + BEAT / 2, "chords", .75)
            if arp:
                notes = PROG[bar] + [PROG[bar][0] + 12, PROG[bar][1] + 12]
                for s in range(4):
                    put(pluck(notes[(k * 4 + s) % len(notes)] + 12, .3, bright), t + s * BEAT / 4, "keys", .45, np.sin((k * 4 + s) * 1.3) * .5)

    # 1. HOOK from frame 0: the downbeat lands with the phone (.38 s), the count builds, 2,400 hits on "followers"
    put(crash(), .38, "drums", 1.0)
    put(kick(True) * 1.2, .38, "drums")
    put(riser(.38, .4), 0, "fx")
    COUNT = L[1] - .1
    groove(.38, COUNT, .38, claps=False, cut=2000)
    groove(COUNT, STOP0, .38, claps=True, hats16=True, arp=True, cut=2800)
    put(riser(cues["followers"] - cues["three"], .5), cues["three"], "fx")
    put(crash(), cues["followers"], "drums", 1.0)
    # 2. STOP: under "It doesn't just post." only a filtered chord; slams back on "grows"
    put(downlift(.8), STOP0, "fx", .5)
    put(supersaw(DBM, GROW - STOP0 + .1, 700, .05, .2, .9), STOP0, "chords", .7)
    put(riser(GROW - STOP0 - .05, .55), STOP0, "fx")
    put(crash(), GROW, "drums", 1.1)
    put(kick(True) * 1.3, GROW, "drums")
    groove(GROW, BUILD, GROW, claps=True, hats16=True, arp=True, cut=3200)
    # 3. BUILD: the snare roll speeds up into the dive
    groove(BUILD, DIVE - .02, BUILD, claps=True, hats16=False, chords="stab", cut=2400)
    t, gap = BUILD + .9, BEAT / 2
    while t < DIVE - .05:
        put(snare(), t, "drums", .35 + .5 * (t - BUILD) / (DIVE - BUILD))
        t += gap
        gap = max(BEAT / 8, gap * .8)
    put(riser(DIVE - BUILD - .3, .9), BUILD + .3, "fx")
    # 4. MOVES: the drop through the screen; a crash on every move
    put(crash(), DIVE, "drums", 1.25)
    put(kick(True) * 1.4, DIVE, "drums")
    groove(DIVE, BRK - .06, DIVE, big=True, hats16=True, arp=True, chords="pad", cut=5200, bass="saw")
    for off, m, d in HOOK:
        if DIVE + off * BEAT < BRK - .2:
            put(lead(m, d * BEAT - .02), DIVE + off * BEAT, "keys", .75)
    for k in (5, 6, 7):
        put(crash(), L[k] - .14, "drums", .7)
        put(riser(.4, .3), L[k] - .54, "fx")
    # 5. BREAK: dead stop on "And five?"
    put(sub(24, 1.0) * 1.2, BRK + .02, "bass", 1.0)
    put(downlift(1.0), BRK, "fx", .7)
    put(bell(84, 1.2), cues["five5"], "keys", .5)
    # 6. HALF-TIME in the dark lab, building into "rewrites", then double time to the bonus
    dark_bar = 4 * BEAT * 2
    for t, k in beats(HALF, RW - .02, step=BEAT * 2, origin=HALF):
        bar = (k // 2) % 4
        put(kick(True), t, "drums", .95)
        kicks.append(t)
        if k % 2:
            put(clap(), t, "drums", .7)
            put(snare(), t, "drums", .4)
        if k % 2 == 0:
            put(sub(DROOTS[bar], dark_bar / 2 - .02), t, "bass", .9)
            put(supersaw([m + 12 for m in DARK[bar]], dark_bar / 2, 900, .2, .4, .9), t, "chords", .8)
    for t, k in beats(HALF, RW - .02, step=BEAT / 4, origin=HALF):
        prog = (t - HALF) / (RW - HALF)
        put(pluck(DARK[(k // 16) % 4][k % 4] + 24, .22, .7 + prog), t, "keys", .2 + .35 * prog, np.sin(k * 1.7) * .6)
    put(riser(RW - HALF - .4, .8), HALF + .4, "fx")
    put(crash(), RW, "drums", 1.1)
    put(kick(True) * 1.3, RW, "drums")
    groove(RW, BON - .06, RW, big=True, hats16=True, arp=True, chords="stab", cut=3600, bass="saw")
    put(riser(BON - RW - .1, .9), RW + .1, "fx")
    # 7. BONUS: the brightest drop
    put(crash(), BON, "drums", 1.3)
    put(kick(True) * 1.4, BON, "drums")
    groove(BON, CTA, BON, big=True, hats16=True, arp=True, chords="pad", cut=7000, bass="saw", bright=1.6)
    for off, m, d in HOOK:
        if BON + off * BEAT < CTA - .2:
            put(lead(m + 12, d * BEAT - .02), BON + off * BEAT, "keys", .6)
    # 8. CTA: the groove holds, then the button on the last beat
    last = CTA + int((END - .35 - CTA) / BEAT) * BEAT
    put(crash(), CTA, "drums", .8)
    groove(CTA, last, BON, claps=True, hats16=False, arp=True, chords="stab", cut=4200, bright=1.4)
    put(kick(True), last, "drums", 1.1)
    put(crash(), last, "drums", .9)
    put(supersaw(ABM + [68], 1.2, 6000, .003, .3, 1.0), last, "chords", 1.2)
    put(sub(32, .9), last, "bass", .9)

    # mix: sidechain the bass and the chords to the kicks, reverb on the keys and chords, buses balanced by loudness
    duck = np.ones(n)
    for k in kicks:
        i = int(k * SR)
        m = min(n - i, int(.3 * SR))
        if m > 0:
            duck[i:i + m] = np.minimum(duck[i:i + m], 1 - .6 * np.exp(-np.arange(m) / SR / .09))
    BUS["bass"] *= duck[:, None]
    BUS["chords"] *= (1 - (1 - duck) * .9)[:, None]
    BUS["chords"] = np.stack([reverb(BUS["chords"][:, c], 1.8, .22, c) for c in (0, 1)], 1)
    BUS["keys"] = np.stack([reverb(BUS["keys"][:, c], 2.2, .3, c + 4) for c in (0, 1)], 1)
    rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)  # noqa: E731
    gain = {"drums": .11, "bass": .085, "chords": .055, "keys": .04, "fx": .03}
    out = sum(BUS[k] * (gain[k] / rms(BUS[k])) for k in BUS)
    out = np.tanh(out * 2.2) / 2.2                       # gentle bus glue
    i0, i1 = int((BRK + .25) * SR), int((HALF - .02) * SR)   # the break stays almost silent until move five starts
    out[i0:i1] *= .35
    return out
