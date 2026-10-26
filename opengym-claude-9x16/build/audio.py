"""Music, sound design and the mastered mix for the openGym x Claude reel.

The music bed is a licensed track picked with build/find_music.py (build/track.json; CC0 / CC BY, credit in the
caption) when one is chosen; otherwise the original score synthesized below.

python opengym-claude-9x16/build/audio.py      (inside the voice venv: numpy, scipy, soundfile; needs ffmpeg)

A 120 bpm gym track in F# minor (four-on-the-floor kick, claps, hats, a pumping saw bass, supersaw stabs, a pluck arp):
filtered and sparse under the paywall hook, a full drop on NXT's slam, a filter dip into the muscle-map tease, back in
on "Worked", and a button ending on the last word. It is sidechain-ducked under the voice. SFX per scene: phone buzz,
error ding, slam, power-up riser, glass burst, record scratch, stamps, key click, pops, rep thuds, counter ticks, plate
clank, three rising tones, a comic boing, a laugh sting, the power-down puff and a chime.
Writes assets/audio/music.wav (score + sfx) and assets/audio/mix.wav (voice + score, mastered to -14 LUFS, -1.5 dBTP).
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
L, E = T["l"], T["e"]
SR = 48000
DUR = T["end"]
N = int(DUR * SR)
BPM = 120
BEAT = 60 / BPM
rng = np.random.default_rng(7)


def lp(x, fc, o=2):
    return sosfilt(butter(o, min(fc, SR / 2 - 100), "low", fs=SR, output="sos"), x)


def hp(x, fc, o=2):
    return sosfilt(butter(o, fc, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, min(hi, SR / 2 - 100)], "band", fs=SR, output="sos"), x)


def tt(d):
    return np.arange(int(d * SR)) / SR


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


BUS = {k: np.zeros((N, 2)) for k in ("drums", "bass", "synth", "sfx")}


def put(x, t, g=1.0, pan=0.0, bus="sfx"):
    i = int(round(t * SR))
    if i >= N:
        return
    if i < 0:
        x, i = x[-i:], 0
    x = x[: N - i]
    BUS[bus][i:i + len(x), 0] += x * g * np.sqrt(.5 * (1 - pan))
    BUS[bus][i:i + len(x), 1] += x * g * np.sqrt(.5 * (1 + pan))


# ---------------------------------------------------------------- instruments
def kick(d=.42):
    t = tt(d)
    f = 48 + 150 * np.exp(-t * 32)
    return np.tanh(2.6 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5)) * .55


def clap(d=.3):
    t = tt(d)
    n = bp(rng.standard_normal(len(t)), 900, 6000)
    env = sum(np.exp(-np.clip(t - k * .011, 0, None) * 60) * (t >= k * .011) for k in range(3)) * .5 + np.exp(-t * 14) * .5
    return n * env * .3


def hat(d=.05, open_=False):
    t = tt(d if not open_ else .2)
    return hp(rng.standard_normal(len(t)), 8500) * np.exp(-t * (70 if not open_ else 18)) * (.07 if not open_ else .06)


def saw(f, t, det=(0,)):
    x = np.zeros_like(t)
    for c in det:
        ph = (f * (1 + c / 100) * t + rng.random()) % 1
        x += 2 * ph - 1
    return x / len(det)


def bass(m, d):
    t = tt(d)
    x = saw(hz(m), t, (-6, 6)) * .7 + np.sin(2 * np.pi * hz(m - 12) * t) * .6
    return lp(x, 900) * np.clip(t / .004, 0, 1) * np.clip((d - t) / .02, 0, 1) * .22


def stab(ms, d=.45, cut=4200):
    t = tt(d)
    x = sum(saw(hz(m), t, (-14, -5, 0, 5, 14)) for m in ms) / len(ms)
    return lp(x, cut) * np.exp(-t * 5) * np.minimum(1, t / .006) * .16


def pad(ms, d, cut=1600):
    t = tt(d)
    x = sum(saw(hz(m), t, (-10, -3, 3, 10)) for m in ms) / len(ms)
    env = np.minimum(1, t / .4) * np.clip((d - t) / .4, 0, 1)
    return lp(x, cut) * env * .07


def pluck(m, d=.2):
    t = tt(d)
    x = saw(hz(m), t, (-4, 4))
    return (lp(x, 1800) + hp(lp(x, 6000), 1800) * np.exp(-t * 30)) * np.exp(-t * 16) * .09


# ---------------------------------------------------------------- arrangement
PROG = [(54, [66, 69, 73]), (50, [62, 66, 69]), (57, [64, 69, 73]), (52, [64, 68, 71])]   # F#m  D  A  E (bass, chord)


def arrange():
    drop, dip, back, stop = L[1] - .12, L[8] - .1, T["worked"] - .02, E[11] + .05
    nbeats = int(DUR / BEAT) + 1
    for b in range(nbeats):
        t = b * BEAT
        bar = b // 4
        root, chord = PROG[bar % 4]
        if t >= stop:
            break
        full = (drop <= t < dip) or (back <= t < stop)
        intro = t < drop
        hush = dip <= t < back
        if full:
            put(kick(), t, 1.0, bus="drums")
            if b % 2 == 1:
                put(clap(), t, .9, .05, bus="drums")
            put(hat(open_=True), t + BEAT / 2, .9, .2, bus="drums")
            for k in range(4):
                put(hat(), t + k * BEAT / 4, .7 if k % 2 else .45, -.2, bus="drums")
            for k in range(2):           # off-beat pumping bass
                put(bass(root - 12, BEAT / 2 - .02), t + BEAT / 2 * k + (BEAT / 4 if k == 0 else 0), .9, bus="bass")
            if b % 4 == 0:
                put(stab(chord), t, .9, -.1, bus="synth")
            if b % 4 == 2:
                put(stab(chord, .3), t + BEAT / 2, .6, .15, bus="synth")
            for k in range(4):
                put(pluck(chord[(b * 4 + k) % 3] + 12), t + k * BEAT / 4, .8, (-.3, .3)[k % 2], bus="synth")
        elif intro:
            for k in range(2):
                put(hat(), t + k * BEAT / 2, .5, -.2, bus="drums")
            if b % 4 == 0:
                put(pad([m - 12 for m in chord] + chord, BEAT * 4 + .2, 900), t, 1.0, bus="synth")
            if b % 2 == 0:
                put(lp(kick(), 300), t, .45, bus="drums")
        elif hush:
            if b % 4 == 0:
                put(pad(chord + [chord[0] + 12], BEAT * 4 + .2, 700), t, 1.0, bus="synth")
            put(lp(kick(), 180), t, .5 if b % 2 == 0 else .25, bus="drums")
            put(hat(), t + BEAT / 2, .35, .2, bus="drums")
    # riser into the drop and into "Worked"
    for a, z, g in ((drop - 1.2, drop, 1.0), (back - 1.0, back, .8)):
        d = z - a
        t = tt(d)
        n = rng.standard_normal(len(t))
        x = np.zeros_like(t)
        seg = len(t) // 12
        for i in range(12):
            lo = 400 * (12 ** (i / 12))
            x[i * seg:(i + 1) * seg] = bp(n, lo, lo * 2.2)[i * seg:(i + 1) * seg]
        put(x * (t / d) ** 2 * .22 * g, a, 1.0, bus="synth")
    # button ending: one big stab + kick on the last word, then a ring-out
    put(kick(.8), stop, 1.2, bus="drums")
    put(stab(PROG[0][1] + [78], 1.6, 3000), stop, 1.3, bus="synth")
    put(pad(PROG[0][1], 1.4, 1200), stop, .8, bus="synth")


# ---------------------------------------------------------------- sfx
def tone(f, d, dec=6, kind="sin"):
    t = tt(d)
    x = np.sin(2 * np.pi * f * t) if kind == "sin" else saw(f, t)
    return x * np.exp(-t * dec) * np.minimum(1, t / .003)


def buzz(d=.6):
    t = tt(d)
    x = np.sign(np.sin(2 * np.pi * 150 * t)) * (np.sin(2 * np.pi * 9 * t) > -.2)
    return lp(x, 1800) * .08 * np.clip((d - t) / .05, 0, 1)


def ding_err():
    return tone(880, .5, 7) * .3 + tone(660, .5, 7) * .25


def whoosh(d=.35, g=1.0):
    t = tt(d)
    n = rng.standard_normal(len(t))
    x = np.zeros_like(t)
    s = len(t) // 10
    for i in range(10):
        lo = 300 * (10 ** (i / 10))
        x[i * s:(i + 1) * s] = bp(n, lo, lo * 2.5)[i * s:(i + 1) * s]
    return x * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5 * .16 * g


def slam():
    t = tt(1.2)
    body = np.sin(2 * np.pi * np.cumsum(40 + 110 * np.exp(-t * 18)) / SR) * np.exp(-t * 4)
    crack = bp(rng.standard_normal(len(t)), 600, 7000) * np.exp(-t * 30)
    return np.tanh(2.2 * (body + crack * .7)) * .6


def riser_up(d=.8):
    t = tt(d)
    f = 200 * 2 ** (t / d * 3)
    return lp(np.sin(2 * np.pi * np.cumsum(f) / SR) + .4 * np.sin(4 * np.pi * np.cumsum(f) / SR), 5000) * (t / d) * .18


def glass(d=1.0):
    t = tt(d)
    x = hp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 7) * .3
    for k in range(14):
        x += tone(2000 + rng.random() * 6000, d, 9 + rng.random() * 8) * .05 * (t > rng.random() * .15)
    return x


def scratch():
    t = tt(.28)
    f = 300 + 900 * np.abs(np.sin(t * 22))
    return bp(np.sin(2 * np.pi * np.cumsum(f) / SR) + rng.standard_normal(len(t)) * .4, 300, 4000) * .16 * np.sin(np.pi * t / .28)


def stamp():
    t = tt(.35)
    return np.tanh(3 * (np.sin(2 * np.pi * np.cumsum(90 + 200 * np.exp(-t * 40)) / SR) * np.exp(-t * 18) + bp(rng.standard_normal(len(t)), 1000, 5000) * np.exp(-t * 50) * .5)) * .35


def pop_(f=900):
    t = tt(.12)
    return np.sin(2 * np.pi * np.cumsum(f * (1 + 1.5 * np.exp(-t * 40))) / SR) * np.exp(-t * 35) * .22


def click():
    t = tt(.05)
    return bp(rng.standard_normal(len(t)), 2000, 8000) * np.exp(-t * 120) * .3


def thud():
    t = tt(.2)
    return np.sin(2 * np.pi * np.cumsum(80 + 60 * np.exp(-t * 30)) / SR) * np.exp(-t * 22) * .25


def clank():
    t = tt(.9)
    x = sum(tone(f, .9, d) * a for f, a, d in [(520, .5, 5), (1310, .35, 7), (2240, .25, 9), (3170, .15, 12)])
    return x * .5 + bp(rng.standard_normal(len(t)), 2000, 8000) * np.exp(-t * 60) * .3


def boing():
    t = tt(.6)
    f = 180 + 120 * np.sin(2 * np.pi * 7 * t) * np.exp(-t * 3) + 160 * np.exp(-t * 6)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4) * .32


def chime():
    return sum(tone(hz(m), 1.8, 2.5) * .12 for m in (78, 81, 85, 90))


def puff():
    t = tt(.6)
    return lp(rng.standard_normal(len(t)), 1800) * np.exp(-t * 7) * .35


def sfx():
    put(buzz(.6), .02, 1.0); put(buzz(.4), 1.1, .9)
    put(ding_err(), .32, .8)
    land = L[1] - .12
    put(whoosh(.45, 1.4), land - .45, 1.0)
    put(slam(), land, 1.0)
    put(riser_up(.7), land + .1, 1.0)
    put(pop_(400), land + .55, 1.2)
    put(glass(), T["free"] - .02, 1.1)
    put(slam() * .6, T["free"] - .02, .7)
    put(whoosh(.3), T["claude"] - .2, .7)
    put(scratch(), L[2] - .05, 1.0)
    put(whoosh(.35), L[3] - .2, .9)
    for t in T["x"]:
        put(stamp(), t, .9)
    put(click(), L[4] + .85, 1.2); put(pop_(1300), L[4] + .87, .9)
    for t in T["g"]:
        put(pop_(1100), t, .9)
    for i in range(4):
        put(pop_(700 + i * 120), L[6] + .5 + i * .22, .8)
    put(stamp(), T["approve"], 1.2)
    put(chime() * .5, T["approve"] + .05, 1.0)
    b = 0
    while L[7] + .2 + b * .5 < L[8]:
        put(thud(), L[7] + .2 + b * .5, .6); b += 1
    for i in range(8):
        put(click(), T["demos"] + i * .07, .5)
    put(whoosh(.25), T["ready"] - .3, .7)
    put(clank(), T["ready"] + .08, 1.0)
    put(whoosh(.5, 1.1), L[8] - .25, 1.0)
    for t, m in ((T["worked"], 76), (T["recovering"], 80), (T["untrained"], 83)):
        put(tone(hz(m), .7, 4) * .25 + tone(hz(m + 12), .7, 6) * .1, t, 1.0)
    put(boing(), T["legs"] + .4, 1.0)
    put(sum(tone(hz(m), .5, 6) * .15 for m in (72, 76, 79)), L[10] + .1, 1.0)
    put(whoosh(.3), L[10] - .15, .8)
    put(whoosh(.3), T["gym"] - .2, .7); put(pop_(1500), T["gym"], 1.0)
    put(puff(), T["end"] - 1.15, 1.0)
    put(chime(), T["end"] - 1.0, 1.0)


def reverb(x, secs=1.4, mix=.18, seed=0):
    r = np.random.default_rng(seed)
    t = np.arange(int(secs * SR)) / SR
    ir = lp(r.standard_normal(len(t)) * np.exp(-t * 3.8), 8000)
    ir /= np.sqrt(np.sum(ir ** 2))
    return x * (1 - mix) + fftconvolve(x, ir)[: len(x)] * mix * 1.4


def ffmpeg(*a):
    return subprocess.run(["ffmpeg", "-y", "-hide_banner", *a], capture_output=True, text=True, check=True)


def track_bed():
    """The licensed track from build/find_music.py (build/track.json), cut to the reel: the loudest steady stretch
    past the intro, so the hook starts on full energy. None when no track has been chosen."""
    meta = os.path.join(ROOT, "build", "track.json")
    if not os.path.exists(meta):
        return None
    t = json.load(open(meta))
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(ROOT, t["track"]), "-f", "f32le", "-ac", "2",
                          "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
    if "start" in t:
        st = int(t["start"] * SR)
    else:
        win = int(SR / 2)
        e = np.sqrt(np.convolve((x ** 2).mean(1), np.ones(win) / win, "valid")[::win])   # energy per 0.5 s
        need = int(np.ceil(DUR * 2))
        skip = min(16, max(0, len(e) - need))                     # skip up to 8 s of intro
        cand = [(np.percentile(e[i:i + need], 20), i) for i in range(skip, max(skip + 1, len(e) - need))]
        st = max(cand)[1] * win if cand else 0
    seg = x[st:st + N]
    while len(seg) < N:                                           # short track: loop it
        seg = np.concatenate([seg, x[: N - len(seg)]])
    fi = int(.02 * SR)
    seg[:fi] *= np.linspace(0, 1, fi)[:, None]
    print(f"music bed: {t['title']} by {t['creator']} ({t['license']}), from {st / SR:.1f} s")
    return seg


def main():
    arrange()
    sfx()
    voice, vsr = sf.read(os.path.join(ROOT, "assets", "audio", "voice.wav"))
    assert vsr == SR
    v = np.zeros(N)
    v[: min(N, len(voice))] = voice[:N]
    # sidechain: duck the score under the voice (180 ms release)
    env = np.abs(v)
    r_ = np.exp(-1 / (.18 * SR))
    from scipy.signal import lfilter
    env = lfilter([1 - r_], [1, -r_], env)
    env = np.clip(env / (np.percentile(env[env > 1e-4], 90) + 1e-9), 0, 1)
    duck = 1 - .5 * env
    synth = np.stack([reverb(BUS["synth"][:, c], 1.8, .25, c) for c in (0, 1)], 1)
    sfxb = np.stack([reverb(BUS["sfx"][:, c], 1.0, .15, c + 2) for c in (0, 1)], 1)
    rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)
    bed = track_bed()
    if bed is not None:
        # a real track sits on a single bus: duck it deeper under the voice, keep the SFX a little lower
        music = bed * (.07 / rms(bed)) * (1 - .62 * env)[:, None]
        score = music + sfxb * (.035 / rms(sfxb))
    else:
        music = BUS["drums"] * (.05 / rms(BUS["drums"])) + BUS["bass"] * (.035 / rms(BUS["bass"])) + synth * (.03 / rms(synth))
        music *= duck[:, None]
        score = music + sfxb * (.05 / rms(sfxb))
    fade = np.ones(N); fade[-int(.25 * SR):] = np.linspace(1, 0, int(.25 * SR))
    score *= fade[:, None]
    vg = .16 / rms(v[v != 0]) if np.any(v) else 1
    mix = score + (v * vg)[:, None]
    pk = np.max(np.abs(mix))
    if pk > .98:
        mix *= .98 / pk
        score *= .98 / pk
    out_m = os.path.join(ROOT, "assets", "audio", "music.wav")
    sf.write(out_m, score.astype(np.float32), SR, subtype="PCM_24")
    raw = os.path.join(ROOT, "assets", "audio", "mix_raw.wav")
    sf.write(raw, mix.astype(np.float32), SR, subtype="FLOAT")
    # master: two-pass loudnorm to -14 LUFS integrated, -1.5 dBTP
    o = ffmpeg("-i", raw, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-").stderr
    meas = json.loads(o[o.rindex("{"):o.rindex("}") + 1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
          f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:linear=true")
    out = os.path.join(ROOT, "assets", "audio", "mix.wav")
    ffmpeg("-i", raw, "-af", af + ",alimiter=limit=0.82:level=false:attack=1:release=60", "-ar", str(SR), "-c:a", "pcm_s24le", out)
    os.remove(raw)
    chk = ffmpeg("-i", out, "-af", "ebur128=peak=true", "-f", "null", "-").stderr
    summ = chk[chk.rindex("Summary:"):]
    print("wrote", out, " ".join(l.strip() for l in summ.splitlines() if l.strip().startswith(("I:", "Peak:"))))


if __name__ == "__main__":
    main()
