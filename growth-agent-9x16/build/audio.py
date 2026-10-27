"""Music, sound design and the mastered mix for the Instagram Growth Agent reel.

python3 build/audio.py      (from the project root, after build/generate.py; needs numpy, scipy, soundfile, ffmpeg)

Music: the original score in build/score.py, composed in code to the reel's energy curve (no licence or credit needed).
SFX: recorded hits from HyperFrames' bundled library (Pixabay Content License: commercial use, no credit needed;
.claude/skills/media-use/audio/assets/sfx/CREDITS.md) plus a few synthesized here. Writes assets/audio/mix.wav,
mastered to -14 LUFS integrated, -1.5 dBTP.
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
rng = np.random.default_rng(11)
SFX = np.zeros((N, 2))
LIB = os.path.join(os.path.dirname(ROOT), ".claude", "skills", "media-use", "audio", "assets", "sfx")
_S = {}


def smp(name):
    """A bundled SFX file as mono float at 48 kHz."""
    if name not in _S:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(LIB, name + ".mp3"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                             capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.float32).astype(np.float64)
        _S[name] = x / (np.max(np.abs(x)) + 1e-9) * .5
    return _S[name]


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
    s = lambda name, d=None: smp(name)[: int(d * SR)] if d else smp(name)  # noqa: E731
    P = T["portal"]
    # HOOK: the rush down the tunnel, things whipping past, Claude ahead, the burst out through the screen
    put(rumble(P + .2), 0, .5)
    put(riser(P, .25), 0)
    for i in range(10):
        put(whoosh(.22, .55, 500 + (i % 3) * 300), .05 + i * .11, 1, (i % 2 - .5) * 1.4)
    put(s("sparkle"), T["claude"] - .02, .5)
    put(s("impact-bass-2"), P, 1.0)
    put(slam(.4), P)
    put(swell(1.4, 72), P + .05, 1.0)
    put(s("pop"), P + .35, .5)
    # FOLLOWERS: the vortex swirling, pops for the pills, the odometer ticking faster, the 6,700 hit
    put(whoosh(2.8, .7, 200), L[1] - .2, .8)
    for i in range(14):
        put(pop_(900 + (i % 5) * 90, .08), L[1] + .1 + i * .24, 1, ((i * 37) % 11 - 5) / 6)
    t, gap = T["count"] - .2, .09
    while t < T["followers"] + .05:
        put(tick(), t, .8, .2)
        t += gap
        gap = max(.035, gap * .93)
    put(s("chime"), T["followers"], .5)
    put(s("sparkle"), T["followers"] + .02, .6)
    # POST: out into bullet time (a slowed whoosh), the stamp, flung away; GROWS: the city rises
    put(s("whoosh-cinematic")[int(1.2 * SR):int(2.4 * SR)], L[2] - .2, .5)
    put(stamp(), T["post"], 1.0)
    put(s("error", .6), T["post"] + .02, .25)
    put(whoosh(.35, .9, 600), T["post"] + .3)
    put(riser(.35, .14), T["grows"] - .35)
    put(rumble(.9), T["grows"], .8)
    for i in range(9):
        put(thud(), T["grows"] - .02 + i * .05, 1.0, (i % 3 - 1) * .4)
    put(s("whoosh"), T["grows"] + .1, .45)
    put(s("chime"), T["page"], .4)
    # FIVE: the wheel spins (ticks slowing down), lands, the fifth glows; the dive
    t, gap = L[3] - .05, .05
    while t < T["last"]:
        put(click(.22), t, 1, np.sin(t * 9) * .5)
        t += gap
        gap *= 1.09
    put(thud(), T["last"], 1.0)
    put(s("glitch-1", .4), T["smartest"], .35)
    put(s("whoosh-cinematic")[int(1.6 * SR):int(2.9 * SR)], T["in0"] - .9, .8)
    put(s("impact-bass-2"), T["in0"], 1.0)
    # inside: a whoosh into every world
    for t0 in (L[5] - .14, L[6] - .14, L[7] - .14):
        put(s("whoosh-short"), t0 - .1, .6)
        put(s("impact-bass-1"), t0, .25)
    # MOVE 1: the swoop over the field, the beam's sweeps, the columns launching
    put(whoosh(1.2, 1.0, 250), T["in0"])
    put(scan(2.0), L[4] - .1, .9)
    for i in range(3):
        put(s("ping", .5), L[4] + .15 + i * .3, .3, (i - 1) * .5)
    put(riser(.35, .15), T["blowing"] - .3)
    put(s("impact-bass-1"), T["blowing"] + .05, .45)
    # MOVE 2: the corridor's frames flipping past, four snapping in, the palette
    for i in range(9):
        put(whoosh(.16, .45, 900), L[5] - .1 + i * .1, 1, (i % 2 - .5) * 1.6)
    for i in range(4):
        put(s("click", .2), T["plans"] + .18 + i * .1, .5, (i - 1.5) / 2)
    for i in range(5):
        put(pop_(1000 + i * 120, .1), T["visuals"] - .05 + i * .06, 1, (i - 2) / 3)
    # MOVE 3: the keyboard ripples, AGENT hammers, the page types, the caption pops
    for i in range(14):
        put(s("key-press", .12), L[6] - .1 + i * .11, .25, np.sin(i * 1.3) * .6)
    for i in range(5):
        put(s("key-press", .15), L[6] - .05 + i * .25, .6, (i - 2) / 4)
    put(s("typing", 1.3), L[6], .3)
    put(s("pop"), T["caption"] - .05, .45)
    # MOVE 4: the comment storm rushing past, replies firing back, three landing
    for i in range(16):
        put(whoosh(.14, .35, 700 + (i % 4) * 200), L[7] - .1 + i * .09, 1, (i % 2 - .5) * 1.6)
    for i in range(6):
        put(s("notification", .5), L[7] + i * .16, .18, (i % 2 - .5))
    for i in range(6):
        put(pop_(1300, .09), T["replies"] - .05 + i * .1, 1, .3)
    for i in range(3):
        put(thud(), T["comments"] - .2 + i * .1, .7)
    # MOVE 5: the lights go out; the spotlight; the scan; the pieces flying past; v2; the launch out of the phone
    put(sub(1.6), T["dark0"], .9)
    put(s("click"), T["five5"] - .03, .6)
    put(slam(.25), T["five5"])
    put(scan(T["rewrites"] - T["studies"]), T["studies"], 1.3)
    for i in range(10):
        put(tick(), T["studies"] + .3 + i * .17, .5, np.sin(i) * .5)
    put(s("glitch-3", .6), T["rewrites"], .5)
    put(whoosh(.4, 1.1, 300), T["rewrites"])
    for i in range(6):
        put(whoosh(.12, .5, 1200), T["rewrites"] + .08 + i * .05, 1, (i % 2 - .5) * 1.8)
    put(whoosh(.35, .7, 800), T["rewrites"] + .32)
    put(s("sparkle"), T["next"] - .02, .7)
    put(s("chime"), T["next"] + .05, .4)
    put(s("whoosh-cinematic")[int(1.8 * SR):int(2.8 * SR)], T["out1"] - .6, .7)
    put(s("impact-bass-2"), T["out1"], .9)
    # CTA: AGENT typed in, sent, the sky of comments, the DM
    for i in range(5):
        put(s("key-press", .15), T["agentcta"] - .06 + i * .075, .5, (i - 2) / 5)
    put(s("whoosh-short"), T["agentcta"] + .48, .4)
    for i in range(38):
        put(pop_(1100 + (i % 4) * 140, .05), T["agentcta"] - .1 + i * .07, 1, (i % 2 - .5) * 1.2)
    put(s("ping"), T["setup"] - .1, .55)
    put(s("sparkle"), T["end"] - 1.4, .4)


def ffmpeg(*a):
    return subprocess.run(["ffmpeg", "-y", "-hide_banner", *a], capture_output=True, text=True, check=True)


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
    fxmix = sfxb * (.05 / rms(sfxb)) * (1 - .5 * talk)[:, None]
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from score import compose
    m = compose(T, N)
    sf.write(os.path.join(ROOT, "assets", "audio", "score.wav"), m.astype(np.float32), SR, subtype="PCM_24")
    score = m * (.08 / rms(m)) * (1 - .45 * talk)[:, None] + fxmix * .8
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
    print("wrote", out, "(music: original score, build/score.py)",
          " ".join(ln.strip() for ln in summ.splitlines() if ln.strip().startswith(("I:", "Peak:"))))


if __name__ == "__main__":
    main()
