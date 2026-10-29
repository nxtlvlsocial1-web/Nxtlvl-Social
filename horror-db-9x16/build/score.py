"""The short's original score, composed in code: D minor, no beat, on the scene's dread curve.

build/audio.py calls compose(cues, n). Nothing here is sampled, so the score needs no licence or credit.

  0 s         DREAD    a low drone (D, A and a rubbing Eb) is already there; Enter lands a sub boom and a string stinger,
                       then a heartbeat starts and speeds up through the server room and the phone
  blackout    SILENCE  everything stops: one beat of true silence after "...I know."
  eyes        CLAUDE   a stinger and a boom as the eyes open, then Claude's theme: a slow, detuned music-box figure over
                       a cold glass pad
  "Restoring" RELIEF   the drone sinks and a warm D major pad opens as the lights come back on, peaking on 100 %
  "One more"  TURN     the warmth drains out, the drone creeps back in
  "revoked"   STING    a low brass cluster and a screech gliss, cut dead on the blackout
  CTA         THEME    the drone and Claude's music box, one last low hit on "BACKUP"
"""
import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
rng = np.random.default_rng(31)


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def lp(x, fc, o=2):
    return sosfilt(butter(o, min(fc, SR / 2 - 200), "low", fs=SR, output="sos"), x, axis=0)


def hp(x, fc, o=2):
    return sosfilt(butter(o, fc, "high", fs=SR, output="sos"), x, axis=0)


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, min(hi, SR / 2 - 200)], "band", fs=SR, output="sos"), x, axis=0)


def saw(f, n, ph=0.0):
    """A band-limited saw (additive), f may be an array."""
    f = np.broadcast_to(np.asarray(f, float), (n,))
    p = 2 * np.pi * (ph + np.cumsum(f) / SR)
    k = max(1, min(40, int(9000 / float(np.max(f)))))
    return sum(np.sin(h * p) / h for h in range(1, k + 1)) * (2 / np.pi)


def curve(n, pts):
    """A gain curve from (time s, gain) points, linear between them."""
    t, g = zip(*pts)
    return np.interp(np.arange(n) / SR, t, g)


def reverb(x, secs=3.0, mix=.35, seed=0, damp=5000):
    r = np.random.default_rng(seed)
    t = np.arange(int(secs * SR)) / SR
    ir = lp(r.standard_normal(len(t)) * np.exp(-t * 6.9 / secs), damp)
    ir /= np.sqrt(np.sum(ir ** 2))
    return x * (1 - mix) + fftconvolve(x, ir)[: len(x)] * mix * 1.6


def place(out, x, t, g=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= len(out):
        return
    x = x[: len(out) - i]
    out[i:i + len(x), 0] += x * g * np.sqrt(.5 * (1 - pan))
    out[i:i + len(x), 1] += x * g * np.sqrt(.5 * (1 + pan))


# ---------------------------------------------------------------- voices
def drone(n):
    """D1 + A1 + Eb2 saws, detuned per side, low-passed, breathing slowly."""
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    for c, det in enumerate((-.12, .13)):
        x = (saw(hz(26) + det * .3, n, c * .3) * .7 + saw(hz(33) + det * .4, n, .2 + c * .1) * .4 + saw(hz(39) + det, n, .5) * .22
             + np.sin(2 * np.pi * hz(14) * t) * .5)
        x = lp(x, 260, 3) + lp(bp(x, 300, 900), 900) * (.3 + .3 * np.sin(2 * np.pi * .07 * t + c))
        out[:, c] = x * (.85 + .15 * np.sin(2 * np.pi * .11 * t + c * 1.7))
    return out


def heartbeat(n, a, b, bpm0, bpm1):
    out = np.zeros((n, 2))
    t, beat = a, 0
    while t < b:
        k = (t - a) / (b - a)
        for off, g in ((0, 1.0), (.17, .65)):
            d = np.arange(int(.35 * SR)) / SR
            x = np.sin(2 * np.pi * np.cumsum(42 + 38 * np.exp(-d * 30)) / SR) * np.exp(-d * 14) * np.minimum(1, d / .004)
            place(out, np.tanh(x * 1.6) * g * (.75 + .35 * k), t + off)
        t += 60 / (bpm0 + (bpm1 - bpm0) * k)
        beat += 1
    return out


def stinger(d=2.2, root=74, up=True):
    """A cluster of high detuned saws sliding up (or down), band-passed: the screech of strings."""
    n = int(d * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for k, m in enumerate((root, root + 1, root + 6, root + 7, root + 13)):
        f = hz(m) * (1 + (.06 if up else -.08) * (t / d) ** 1.5) * (1 + .004 * np.sin(2 * np.pi * (5 + k) * t))
        x += saw(f, n, k * .17)
    env = np.minimum(1, t / .03) * np.exp(-t * 1.6)
    return bp(x, 500, 7000) * env * .12


def boom(d=3.0, f0=30):
    t = np.arange(int(d * SR)) / SR
    x = np.sin(2 * np.pi * np.cumsum(f0 + 70 * np.exp(-t * 9)) / SR) * np.exp(-t * 1.4)
    return np.tanh(1.8 * x) * .9


def brass(d=.6, root=38):
    """The 'revoked' sting: a low saw cluster with a fast-opening filter, held until the cut."""
    n = int(d * SR)
    t = np.arange(n) / SR
    x = sum(saw(hz(m) * (1 + .003 * k), n, k * .2) for k, m in enumerate((root, root + 1, root + 6, root + 12, root + 13)))
    env = np.minimum(1, t / .015)
    return lp(x, 2400, 2) * env * .22


def musicbox(note_list, step):
    """Claude's theme: a slow detuned music-box figure (sine + a glassy 3rd/5th partial), each note ringing."""
    n = int((len(note_list) * step + 3) * SR)
    out = np.zeros(n)
    for i, m in enumerate(note_list):
        if m is None:
            continue
        d = np.arange(int(2.6 * SR)) / SR
        f = hz(m) * (1 + .006 * np.sin(2 * np.pi * .9 * d + i))         # a little warped, like an old box
        x = (np.sin(2 * np.pi * np.cumsum(f) / SR) + .3 * np.sin(2 * np.pi * np.cumsum(f * 3.01) / SR) * np.exp(-d * 6)
             + .12 * np.sin(2 * np.pi * np.cumsum(f * 5.4) / SR) * np.exp(-d * 12))
        x *= np.exp(-d * 2.2) * np.minimum(1, d / .002)
        i0 = int(i * step * SR)
        out[i0:i0 + len(x)] += x[: n - i0]
    return out * .12


def glass(n, notes):
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    for k, m in enumerate(notes):
        for c in (0, 1):
            out[:, c] += np.sin(2 * np.pi * hz(m) * (1 + (c - .5) * .003) * t + k) * (.6 + .4 * np.sin(2 * np.pi * (.13 + .05 * k) * t + c + k))
    return out * .05


def warm(n, notes):
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    for c, det in enumerate((-.0025, .0025)):
        x = sum(saw(hz(m) * (1 + det * (1 + k % 2)), n, k * .31 + c) for k, m in enumerate(notes))
        out[:, c] = lp(x, 1400, 2) * .12
    return out


# ---------------------------------------------------------------- the cue sheet
def compose(T, n):
    L, E = T["l"], T["e"]
    blk0, eyes, cut, cta = E[7] + .35, T["eyes"], T["cut"], T["cta"]
    out = np.zeros((n, 2))

    # the drone: there from frame 0, swelling with the dread, gone in the blackouts, sinking under the relief
    g = curve(n, [(0, .55), (T["enter"], .55), (T["enter"] + .4, 1.0), (12, .8), (20, 1.0), (blk0 - .01, 1.0), (blk0, 0),
                  (eyes - .01, 0), (eyes, .9), (30, .6), (L[11], .55), (T["done"], 0), (L[13] - .3, 0), (T["revoked"], 1.0),
                  (cut - .01, 1.0), (cut, 0), (cta - .01, 0), (cta + .5, .8), (T["end"], .8)])
    out += drone(n) * g[:, None] * .9

    # the heartbeat: starts after Enter, quickens through the server room and the phone, stops dead in the blackout
    out += heartbeat(n, T["enter"] + .9, blk0 - .3, 56, 98) * .55

    # hits
    place(out, boom(3.2), T["enter"], .9)
    place(out, stinger(2.4, 76), T["enter"] + .02, .9)
    place(out, stinger(1.6, 71, up=False), T["rows"], .5)                 # the lights die
    place(out, boom(2.0, 34), T["checked"] + .25, .55)                     # the fans die
    place(out, boom(3.4, 26), eyes, 1.0)
    place(out, stinger(2.8, 79), eyes + .01, 1.0)
    place(out, brass(cut - T["revoked"] + .05), T["revoked"] - .05, 1.0)
    place(out, stinger(cut - T["revoked"] + .05, 82), T["revoked"] - .05, .8)
    place(out, boom(1.8, 28), T["backup"] - .08, .7)

    # Claude's theme: the music box over a cold glass pad, from the eyes to the restore, and again under the CTA
    theme = [62, 65, 69, 73, 74, None, 73, 69, 70, None, 69, 65, 64, None, None, None]
    mb = musicbox(theme * 2, .58)
    a = L[8] - .3
    seg = mb[: int((L[11] - a) * SR)]
    seg[-int(.4 * SR):] *= np.linspace(1, 0, int(.4 * SR))
    place(out, seg, a, 1.0, -.2)
    place(out, musicbox(theme, .5)[: int((T["end"] - cta - .3) * SR)], cta + .3, 1.0, .2)
    gg = curve(n, [(eyes, 0), (eyes + 1.5, 1), (L[11] - .3, 1), (L[11] + .5, 0), (cta, 0), (cta + 1.2, .8), (T["end"], .8)])
    out += glass(n, [86, 89, 93, 87]) * gg[:, None]

    # the relief: a warm D major pad opening as the lights come back, peaking on 100 %, drained on "One more thing"
    gw = curve(n, [(L[11] - .1, 0), (T["done"], 1.0), (L[13] - .4, .8), (L[13] + .3, 0)])
    out += warm(n, [50, 57, 62, 66, 69, 74]) * gw[:, None] * 2.2

    out = np.stack([reverb(out[:, c], 3.2, .3, c + 5) for c in (0, 1)], 1)
    # hard silences survive the reverb tails: the blackout before the eyes, and black after the "revoked" cut
    gate = curve(n, [(0, 1), (blk0, 1), (blk0 + .02, 0), (eyes - .02, 0), (eyes, 1), (cut, 1), (cut + .02, 0), (cta - .02, 0), (cta, 1), (T["end"], 1)])
    out *= gate[:, None]
    fi = int(.6 * SR)
    out[-fi:] *= np.linspace(1, 0, fi)[:, None] ** 2
    return out / (np.max(np.abs(out)) + 1e-9) * .9
