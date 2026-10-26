"""Music, sound design and the mastered mix for the YouTube Agent Skill reel.

python3 build/audio.py      (from the project root, after build/generate.py; needs numpy, scipy, soundfile, ffmpeg)

The music is a licensed track picked on the laptop with build/find_music.py (CC0, Public Domain or CC BY, credit in the
caption; it writes build/track.json). It is arranged to the reel's energy curve:
  BAD CHAOS -> ORDER (0 to the end of "plans your whole week"): a busy, steady stretch of the track, ducked under
    the voice, with the notification pings, phone buzz and the burst on top;
  CALM (to 22.3 s): the same music sinks behind a low-pass and dips, a clock ticks, a riser pulls into
  a beat of silence, then
  GOOD CHAOS ("Virality."): a hard cut to the track's highest-energy stretch on a sub drop, running to the end with a
    button on the last frame.
With no track chosen yet, the mix is the voice and the SFX only (a preview).

Every SFX is synthesized here (no samples), so nothing needs a licence. Writes assets/audio/mix.wav (mastered to
-14 LUFS integrated, -1.5 dBTP).
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, lfilter, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
L, E = T["l"], T["e"]
SR = 48000
DUR = T["end"]
N = int(DUR * SR)
DROP = L[9]
rng = np.random.default_rng(11)
SFX = np.zeros((N, 2))


def lp(x, fc, o=2):
    return sosfilt(butter(o, min(fc, SR / 2 - 100), "low", fs=SR, output="sos"), x, axis=0)


def hp(x, fc, o=2):
    return sosfilt(butter(o, fc, "high", fs=SR, output="sos"), x, axis=0)


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, min(hi, SR / 2 - 100)], "band", fs=SR, output="sos"), x, axis=0)


def tt(d):
    return np.arange(int(d * SR)) / SR


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def put(x, t, g=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= N:
        return
    if i < 0:
        x, i = x[-i:], 0
    x = x[: N - i]
    SFX[i:i + len(x), 0] += x * g * np.sqrt(.5 * (1 - pan))
    SFX[i:i + len(x), 1] += x * g * np.sqrt(.5 * (1 + pan))


# ---------------------------------------------------------------- sounds
def tone(f, d, dec=6):
    t = tt(d)
    return np.sin(2 * np.pi * f * t) * np.exp(-t * dec) * np.minimum(1, t / .003)


def ping(m):                 # a phone notification: two quick glassy notes
    return np.concatenate([tone(hz(m), .09, 18) * .6 + tone(hz(m + 12), .09, 22) * .2, tone(hz(m + 5), .35, 9) * .6 + tone(hz(m + 17), .35, 12) * .2]) * .3


def buzz(d=.45):
    t = tt(d)
    x = np.sign(np.sin(2 * np.pi * 150 * t)) * (np.sin(2 * np.pi * 11 * t) > -.2)
    return lp(x, 1800) * .09 * np.clip((d - t) / .05, 0, 1)


def glitch(d=.12):
    t = tt(d)
    return bp(np.sign(np.sin(2 * np.pi * (300 + 2000 * rng.random()) * t)) * rng.standard_normal(len(t)), 800, 6000) * .08 * np.exp(-t * 20)


def whoosh(d=.35, g=1.0, lo=300):
    t = tt(d)
    n = rng.standard_normal(len(t))
    x = np.zeros_like(t)
    s = len(t) // 10
    for i in range(10):
        f = lo * (10 ** (i / 10))
        x[i * s:(i + 1) * s] = bp(n, f, f * 2.5)[i * s:(i + 1) * s]
    return x * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5 * .16 * g


def slam(g=.6):
    t = tt(1.2)
    body = np.sin(2 * np.pi * np.cumsum(40 + 110 * np.exp(-t * 18)) / SR) * np.exp(-t * 4)
    crack = bp(rng.standard_normal(len(t)), 600, 7000) * np.exp(-t * 30)
    return np.tanh(2.2 * (body + crack * .7)) * g


def sub(d=2.0):
    t = tt(d)
    return np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(32 + 60 * np.exp(-t * 6)) / SR)) * np.exp(-t * 1.6) * .7


def riser(d=.8, g=.18):
    t = tt(d)
    f = 200 * 2 ** (t / d * 3)
    x = lp(np.sin(2 * np.pi * np.cumsum(f) / SR) + .4 * np.sin(4 * np.pi * np.cumsum(f) / SR), 5000) * (t / d)
    return (x + hp(rng.standard_normal(len(t)), 2000) * (t / d) ** 2 * .35) * g


def sparkle(n=9, d=1.2):
    t = tt(d)
    x = np.zeros_like(t)
    for k in range(n):
        y = np.pad(tone(hz(84 + [0, 3, 7, 10, 12, 15, 19][k % 7]), d - k * .04, 7), (int(k * .04 * SR), 0))[: len(t)]
        x[: len(y)] += y * .07
    return x


def pop_(f=900, g=.22):
    t = tt(.12)
    return np.sin(2 * np.pi * np.cumsum(f * (1 + 1.5 * np.exp(-t * 40))) / SR) * np.exp(-t * 35) * g


def click(g=.3):
    t = tt(.04)
    return bp(rng.standard_normal(len(t)), 2000, 8000) * np.exp(-t * 140) * g


def tick():                  # a wall clock
    t = tt(.06)
    return (bp(rng.standard_normal(len(t)), 2500, 7000) * np.exp(-t * 160) + tone(3200, .06, 90) * .3) * .22


def stamp():
    t = tt(.35)
    return np.tanh(3 * (np.sin(2 * np.pi * np.cumsum(90 + 200 * np.exp(-t * 40)) / SR) * np.exp(-t * 18) + bp(rng.standard_normal(len(t)), 1000, 5000) * np.exp(-t * 50) * .5)) * .3


def thud():
    t = tt(.2)
    return np.sin(2 * np.pi * np.cumsum(80 + 60 * np.exp(-t * 30)) / SR) * np.exp(-t * 22) * .25


def chime(root=78):
    return sum(tone(hz(m), 1.6, 2.8) * .1 for m in (root, root + 3, root + 7, root + 12))


def scan(d=1.3):
    t = tt(d)
    f = 600 + 2400 * t / d
    return bp(rng.standard_normal(len(t)), 500, 6000) * (.5 + .5 * np.sin(2 * np.pi * np.cumsum(f / 60) / SR)) * .05 * np.sin(np.pi * t / d)


def rumble(d=1.2):
    t = tt(d)
    return lp(rng.standard_normal(len(t)), 160, 4) * np.sin(np.pi * t / d) * 1.4


def swell(d=2.2, root=66):
    t = tt(d)
    x = sum(np.sin(2 * np.pi * hz(m) * t + k) for k, m in enumerate((root, root + 4, root + 7, root + 11, root + 14)))
    return lp(x, 2400) * np.minimum(1, t / .6) * np.exp(-np.maximum(0, t - .8) * 1.6) * .05


def reverb(x, secs=1.2, mix=.16, seed=0):
    r = np.random.default_rng(seed)
    t = np.arange(int(secs * SR)) / SR
    ir = lp(r.standard_normal(len(t)) * np.exp(-t * 3.8), 8000)
    ir /= np.sqrt(np.sum(ir ** 2))
    return x * (1 - mix) + fftconvolve(x, ir)[: len(x)] * mix * 1.4


# ---------------------------------------------------------------- the sound design, on world.js's cue times
def sfx():
    # BAD CHAOS: the notifications keep landing, the phone buzzes, the screen glitches
    for i in range(10):
        put(ping(76 + [0, 3, -2, 5, 1, 7, -4, 2, 6, -1][i]), .05 + i * .27, .9, [-.6, .5, -.2, .7, -.5, .3, -.7, .6, -.3, .4][i])
    for t0 in (.05, 1.15, 2.25, 3.35):
        if t0 < L[1] - .15:
            put(buzz(), t0, 1.0, .2)
    for k in range(8):
        put(glitch(), .4 + k * .41 + rng.random() * .1, .8, rng.random() - .5)
    # Claude bursts out of the monitor
    put(riser(.5, .14), L[1] - .6)
    put(whoosh(.4, 1.3, 200), L[1] - .3)
    put(slam(.55), L[1] - .06)
    put(sparkle(7, 1.0), L[1] + .05, .8)
    put(chime(81), T["free"] - .02, .8)
    put(whoosh(.35), L[2] - .1, .8)
    put(sparkle(11, 1.4), T["eleven"] - .03, 1.1)
    for i in range(11):
        put(pop_(700 + i * 60, .12), T["eleven"] + i * .025, 1, (i - 5) / 6)
    for i in range(5, 10):
        put(pop_(1300, .16), T["eleven"] + .78 + (i - 5) * .07, 1, (i - 7) / 3)
    # ORDER: a whoosh into each station, and each one's own small sounds
    for t0 in (L[3], L[4], L[5], L[6], L[7]):
        put(whoosh(.3, .9), t0 - .34)
    for k in range(9):
        put(click(.22), L[3] + .12 + k * .14, 1, -.3)
    for k in range(21):
        put(pop_(1500 + k * 25, .07), T["twentyone"] - .25 + k * .05, 1, np.sin(k) * .6)
    put(whoosh(.3, .8, 500), L[4] + .5)
    put(pop_(1100, .2), L[4] + .98)
    put(scan(1.3), L[5] + .05)
    for x in (-.5 + .9 * .14, -.5 + .9 * .45, -.5 + .9 * .62, -.5 + .9 * .82):
        put(stamp(), L[5] + .05 + (x + .5) * 1.3, .6, x)
    put(pop_(800, .2), L[5] + 1.38)
    for k in range(4):
        put(pop_(950 + k * 80, .15), L[6] - .2 + k * .08, 1, -.4)
        put(pop_(600 + k * 70, .15), L[6] + .3 + k * .17, 1, .4)
    put(stamp(), L[6] + 1.26, .7)
    for i in range(5):
        put(thud(), L[7] + .34 + i * .15, 1, (i - 2) / 4)
    put(chime(85), L[7] + .95, .6)
    for i in range(5):
        put(pop_(1600, .1), T["l"][3 + i] + .35 + 1.33, .8)
    # CALM: the clock, the riser, a breath of silence before the drop
    for k in range(int(E[7] + 1), int(DROP)):
        put(tick(), k + .0, .9, -.4)
    put(riser(.75, .2), DROP - .78)
    # GOOD CHAOS: the drop, the towers, the X-ray, the new one rising out of the voice
    put(sub(2.2), DROP, 1.0)
    put(slam(.6), DROP)
    put(sparkle(9, 1.0), DROP + .05, .7)
    put(rumble(1.2), DROP, .8)
    put(whoosh(.5, 1.0, 200), T["blowing"] - .15)
    for k in range(6):
        put(pop_(1200 + k * 90, .1), T["blowing"] - .07 + k * .12, 1, np.sin(k * 2) * .6)
    put(scan(.9), T["blowing"] + .45, 1.2)
    put(pop_(900, .18), T["blowing"] + .6)
    put(riser(T["voice"] + .25 - T["writes"], .16), T["writes"] - .15)
    put(slam(.4), T["voice"] + .2)
    put(chime(83), T["voice"] + .2, .8)
    # LANDING: sunrise, paste, send, installed
    put(whoosh(.4, 1.1, 200), L[10] - .3)
    put(swell(2.6), L[10] - .05, 1.0)
    put(pop_(700, .16), T["setup"] - .2)
    put(click(.4), T["paste"] - .02)
    put(click(.3), T["paste"] + .06)
    put(whoosh(.25, .8, 800), T["link"] + .02)
    put(chime(85), T["link"] + .28, .8)
    # CTA: confetti, the keyword typed in, the DM landing
    put(sparkle(11, 1.6), T["youtube"] - .05, 1.0)
    put(whoosh(.3, .7, 600), T["youtube"] - .05)
    a = T["youtube"] - .12
    for i in range(7):
        put(click(.3), a + .1 + i * .07, 1, (i - 3) / 5)
    put(ping(83), E[11] + .1, 1.0)
    put(pop_(1400, .2), E[11] + .45)


def ffmpeg(*a):
    return subprocess.run(["ffmpeg", "-y", "-hide_banner", *a], capture_output=True, text=True, check=True)


def music():
    """The licensed track (build/track.json) arranged to the energy curve; None when none has been chosen."""
    meta = os.path.join(ROOT, "build", "track.json")
    if not os.path.exists(meta):
        return None, None
    tr = json.load(open(meta))
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(ROOT, tr["track"]), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
    blk = SR // 2
    p = (x ** 2).mean(1)
    e = np.sqrt(p[: len(p) // blk * blk].reshape(-1, blk).mean(1))         # energy per 0.5 s
    n1, n2 = int(np.ceil(DROP * 2)), int(np.ceil((DUR - DROP) * 2))
    skip = min(16, max(0, len(e) - n1))
    # part 1: the steadiest busy stretch (the 20th percentile of its energy, highest); part 2: the loudest stretch after it
    c1 = [(np.percentile(e[i:i + n1], 20), i) for i in range(skip, max(skip + 1, len(e) - n1))]
    s1 = tr.get("start", max(c1)[1] * .5 if c1 else 0)
    c2 = [(np.mean(e[i:i + n2]), i) for i in range(0, max(1, len(e) - n2))]
    s2 = tr.get("drop", max(c2)[1] * .5 if c2 else 0)

    def seg(st, n):
        i = int(st * SR)
        y = x[i:i + n]
        while len(y) < n:
            y = np.concatenate([y, x[: n - len(y)]])
        return y.copy()
    a = seg(s1, int(DROP * SR))
    b = seg(s2, N - int(DROP * SR))
    # the calm: a low-pass that closes from the end of line 8 and a dip; silence for the last 60 ms before the drop
    t = np.arange(len(a)) / SR
    k = np.clip((t - (E[7] - .1)) / .8, 0, 1)[:, None]
    a = a * (1 - k) + lp(a, 520, 4) * k * .55
    a *= np.clip((DROP - .06 - t) / .25, 0, 1)[:, None]
    fi = int(.01 * SR)
    b[:fi] *= np.linspace(0, 1, fi)[:, None]
    print(f"music: {tr['title']} by {tr['creator']} ({tr['license']}); chaos from {s1:.1f} s, drop from {s2:.1f} s")
    return np.concatenate([a, b]), tr


def main():
    sfx()
    voice, vsr = sf.read(os.path.join(ROOT, "assets", "audio", "voice.wav"))
    assert vsr == SR
    v = np.zeros(N)
    v[: min(N, len(voice))] = voice[:N]
    rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)  # noqa: E731
    # speech gate: on within 30 ms of a word, held 150 ms past it; music and SFX duck on it so the voice stays on top
    hop = int(.01 * SR)
    fr = np.sqrt(np.mean(v[: N // hop * hop].reshape(-1, hop) ** 2, axis=1))
    on = fr > .1 * np.percentile(fr[fr > 1e-4], 90)
    k = int(.15 / .01)
    on = np.convolve(on.astype(float), np.ones(2 * k + 1), "same") > 0
    ramp = np.convolve(on.astype(float), np.ones(3) / 3, "same")
    talk = np.clip(np.interp(np.arange(N) / hop, np.arange(len(ramp)), ramp), 0, 1)
    sfxb = np.stack([reverb(SFX[:, c], 1.0, .15, c + 2) for c in (0, 1)], 1)
    score = sfxb * (.05 / rms(sfxb)) * (1 - .6 * talk)[:, None]
    m, tr = music()
    if m is not None:
        score = m * (.075 / rms(m[int(DROP * SR):])) * (1 - .5 * talk)[:, None] + score * .8
    fade = np.ones(N)
    fade[-int(.2 * SR):] = np.linspace(1, 0, int(.2 * SR))
    score *= fade[:, None]
    mix = score + (v * (.16 / rms(v[v != 0])))[:, None]
    mix *= min(1, .98 / np.max(np.abs(mix)))
    raw = os.path.join(ROOT, "assets", "audio", "mix_raw.wav")
    sf.write(raw, mix.astype(np.float32), SR, subtype="FLOAT")
    # master: two-pass loudnorm to -14 LUFS, -1.5 dBTP after the AAC encode (the WAV aims at -2.0 dBTP)
    o = ffmpeg("-i", raw, "-af", "loudnorm=I=-13.7:TP=-2.0:LRA=11:print_format=json", "-f", "null", "-").stderr
    meas = json.loads(o[o.rindex("{"):o.rindex("}") + 1])
    af = (f"loudnorm=I=-13.7:TP=-2.0:LRA=11:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
          f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:linear=true")
    out = os.path.join(ROOT, "assets", "audio", "mix.wav")
    ffmpeg("-i", raw, "-af", af + ",alimiter=limit=0.78:level=false:attack=1:release=60", "-ar", str(SR), "-c:a", "pcm_s24le", out)
    os.remove(raw)
    chk = ffmpeg("-i", out, "-af", "ebur128=peak=true", "-f", "null", "-").stderr
    summ = chk[chk.rindex("Summary:"):]
    print("wrote", out, "(music: " + (tr["credit"] if tr else "none yet, voice + SFX preview") + ")",
          " ".join(ln.strip() for ln in summ.splitlines() if ln.strip().startswith(("I:", "Peak:"))))


if __name__ == "__main__":
    main()
