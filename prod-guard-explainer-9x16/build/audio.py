"""Music, sound design and the mastered mix for the Prod Guard explainer.

python3 build/audio.py      (from the project root, after build/generate.py; needs numpy, scipy, soundfile, ffmpeg)

Music: an original chiptune-pop bed composed here (no licence or credit needed): 104 bpm in C major (C - G - Am - F),
square-wave lead and arp, triangle bass, a soft kick and hat, in the spirit of the pixel mascot. It sits low under the
voice, drops to a dark low pulse for the twist (read-only production) and comes back brighter for the CTA.
SFX: every visual event generate.py logs (cues.json "ev") gets a sound: recorded hits from HyperFrames' bundled library
(Pixabay Content License: commercial use, no credit needed; .claude/skills/media-use/audio/assets/sfx/CREDITS.md) and
small synthesized blips. Writes assets/audio/mix.wav, mastered to -14 LUFS integrated, -1.5 dBTP.
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
SR = 48000
DUR = T["end"]
N = int(DUR * SR)
BPM = 104
BEAT = 60 / BPM
rng = np.random.default_rng(7)
LIB = os.path.join(os.path.dirname(ROOT), ".claude", "skills", "media-use", "audio", "assets", "sfx")
_S = {}
TW0, TW1 = T["scenes"][6]


def smp(name, d=None):
    if name not in _S:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(LIB, name + ".mp3"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                             capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.float32).astype(np.float64)
        _S[name] = x / (np.max(np.abs(x)) + 1e-9) * .5
    x = _S[name]
    return x[: int(d * SR)] if d else x


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


def put(buf, x, t, g=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= N or i + len(x) <= 0:
        return
    if i < 0:
        x, i = x[-i:], 0
    x = x[: N - i]
    buf[i:i + len(x), 0] += x * g * np.sqrt(.5 * (1 - pan))
    buf[i:i + len(x), 1] += x * g * np.sqrt(.5 * (1 + pan))


def reverb(x, secs=1.2, mix=.16, seed=0):
    r = np.random.default_rng(seed)
    t = np.arange(int(secs * SR)) / SR
    ir = lp(r.standard_normal(len(t)) * np.exp(-t * 6.9 / secs), 7000)
    ir /= np.sqrt(np.sum(ir ** 2))
    return x * (1 - mix) + fftconvolve(x, ir)[: len(x)] * mix * 1.4


# ---------------------------------------------------------------- instruments
def sq(f, d, duty=.5, dec=6.0, g=1.0):
    t = tt(d)
    ph = (f * t) % 1
    x = np.where(ph < duty, 1.0, -1.0)
    return lp(x, 5000) * np.exp(-t * dec) * np.minimum(1, t / .004) * np.clip((d - t) / .01, 0, 1) * g


def tri(f, d, dec=2.0):
    t = tt(d)
    x = 2 * np.abs(2 * ((f * t) % 1) - 1) - 1
    return x * np.exp(-t * dec) * np.minimum(1, t / .004) * np.clip((d - t) / .01, 0, 1)


def kick():
    t = tt(.3)
    return np.sin(2 * np.pi * np.cumsum(50 + 110 * np.exp(-t * 30)) / SR) * np.exp(-t * 12) * .9


def hat(g=.25):
    t = tt(.05)
    return hp(rng.standard_normal(len(t)), 7000) * np.exp(-t * 90) * g


def snare():
    t = tt(.18)
    return (bp(rng.standard_normal(len(t)), 1500, 7000) * np.exp(-t * 26) * .5 + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * .3)


def blip(f, d=.08, g=.25):
    t = tt(d)
    return np.sign(np.sin(2 * np.pi * f * (1 + 2 * np.exp(-t * 60)) * t)) * np.exp(-t * 40) * g


def thud(g=.4):
    t = tt(.25)
    return np.sin(2 * np.pi * np.cumsum(70 + 80 * np.exp(-t * 30)) / SR) * np.exp(-t * 20) * g


def whoosh(d=.3, g=.5, lo=400):
    t = tt(d)
    n = rng.standard_normal(len(t))
    x = np.zeros_like(t); s = len(t) // 8
    for i in range(8):
        f = lo * (8 ** (i / 8)); x[i * s:(i + 1) * s] = bp(n, f, f * 2.2)[i * s:(i + 1) * s]
    return x * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5 * .2 * g


def coin(m=84):
    return np.concatenate([sq(hz(m), .07, .25, 10, .2), sq(hz(m + 5), .25, .25, 8, .2)])


def alarm(d):
    t = tt(d)
    x = np.sign(np.sin(2 * np.pi * 1800 * t)) * (np.sin(2 * np.pi * 14 * t) > 0)
    return bp(x, 900, 6000) * .07 * np.clip((d - t) / .05, 0, 1)


def drop():
    t = tt(1.6)
    return np.tanh(2 * np.sin(2 * np.pi * np.cumsum(34 + 90 * np.exp(-t * 7)) / SR)) * np.exp(-t * 2) * .6


# ---------------------------------------------------------------- the sound design
def sfx():
    buf = np.zeros((N, 2))
    s = smp
    for t, k in T["ev"]:
        if k == "hop": put(buf, np.concatenate([blip(hz(76), .05, .12), blip(hz(83), .07, .12)]), t, .9, .2)
        elif k == "land": put(buf, thud(.25), t, 1.0)
        elif k == "pop": put(buf, s("pop", .3), t, .35)
        elif k == "accent": put(buf, s("click-soft", .2), t, .4)
        elif k == "type": put(buf, s("key-press", .1), t, .35, .3)
        elif k == "press":
            put(buf, s("key-press", .2), t - .03, .9); put(buf, s("impact-bass-2"), t, .8); put(buf, s("glitch-1", .4), t + .02, .35)
        elif k == "stamp": put(buf, thud(.6), t, 1.0); put(buf, s("click", .2), t, .5)
        elif k == "rattle":
            u, gap = t, .05
            while u < t + 1.1:
                put(buf, blip(hz(88 - (u - t) * 20), .03, .08), u, 1, .3); u += gap
        elif k == "thud": put(buf, thud(.6), t, 1.0); put(buf, s("error", .5), t, .25)
        elif k == "slide": put(buf, whoosh(.3, .8, 500), t, 1.0, .3)
        elif k == "whoosh": put(buf, s("whoosh-short"), t - .05, .4)
        elif k == "sparkle": put(buf, s("sparkle"), t, .45)
        elif k == "tick": put(buf, blip(hz(84), .06, .18), t, 1.0)
        elif k == "shutter": put(buf, s("click"), t, .7); put(buf, hp(rng.standard_normal(int(.08 * SR)), 3000) * np.exp(-tt(.08) * 40) * .3, t + .03)
        elif k == "ding": put(buf, coin(86), t, .9)
        elif k == "shield": put(buf, s("pop"), t, .5); put(buf, sq(hz(60), .3, .5, 8, .25), t)
        elif k == "clang": put(buf, sq(hz(45), .4, .3, 6, .3) + sq(hz(57), .4, .3, 6, .2), t); put(buf, thud(.4), t)
        elif k == "alarm": put(buf, alarm(T["fresh"] - t - .1), t, 1.0)
        elif k == "chime": put(buf, s("chime"), t, .45)
        elif k == "drop": put(buf, drop(), t, 1.0); put(buf, s("glitch-2", .3), t, .35)
        elif k == "lock": put(buf, s("impact-bass-1"), t, .7); put(buf, s("click"), t, .7)
        elif k == "bonk": put(buf, thud(.5), t); put(buf, blip(hz(50), .12, .15), t)
        elif k == "slam": put(buf, s("impact-bass-1"), t, .6); put(buf, s("pop"), t, .5)
        elif k == "key": put(buf, s("key-press", .12), t, .5, (rng.random() - .5) * .6)
        elif k == "send": put(buf, s("whoosh-short"), t, .5); put(buf, s("ping", .6), t + .1, .35)
        elif k == "flip": put(buf, whoosh(.4, 1.0, 300), t, 1.0)
    return buf


# ---------------------------------------------------------------- the bed: C - G - Am - F, a bar each
CHORDS = [(48, [60, 64, 67]), (43, [59, 62, 67]), (45, [60, 64, 69]), (41, [60, 65, 69])]
LEAD = [76, None, 79, 76, 74, None, 72, 74, 76, None, 72, None, 69, 72, 74, None]


def bed():
    out = np.zeros((N, 2))
    bar = 4 * BEAT
    nb = int(DUR / bar) + 2
    for b in range(nb):
        t0 = b * bar
        root, ch = CHORDS[b % 4]
        dark = TW0 - .1 <= t0 < TW1 - .2
        for q in range(4):
            tq = t0 + q * BEAT
            if TW0 <= tq < TW1:
                if q % 2 == 0:                       # the twist: only a low pulse
                    put(out, tri(hz(root - 12), BEAT * 1.6, 1.5) * .5, tq)
                continue
            put(out, kick() * .55, tq)
            if q in (1, 3):
                put(out, snare() * .35, tq)
            put(out, hat(), tq + BEAT / 2, 1, .3)
            put(out, tri(hz(root - 12 + (7 if q == 2 else 0)), BEAT * .9, 3) * .5, tq)
            for e in range(2):                       # an eighth-note arp on the chord
                m = ch[(q * 2 + e) % 3] + 12
                put(out, sq(hz(m), BEAT / 2 * .8, .25, 9, .07), tq + e * BEAT / 2, 1, -.3 if e else .3)
        if dark:
            continue
        lead_on = b % 2 == 1 or t0 > T["scenes"][7][0]
        for i, m in enumerate(LEAD if lead_on else []):
            if m is not None:
                put(out, sq(hz(m), BEAT / 4 * 1.8, .5, 5, .06), t0 + i * BEAT / 4, 1, .1)
    return np.stack([reverb(out[:, c], 1.0, .12, 3 + c) for c in (0, 1)], 1)


def ffmpeg(*a):
    return subprocess.run(["ffmpeg", "-y", "-hide_banner", *a], capture_output=True, text=True, check=True)


def main():
    voice, vsr = sf.read(os.path.join(ROOT, "assets", "audio", "voice.wav"))
    assert vsr == SR
    v = np.zeros(N)
    v[: min(N, len(voice))] = voice[:N]
    rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)  # noqa: E731
    hop = int(.01 * SR)
    fr = np.sqrt(np.mean(v[: N // hop * hop].reshape(-1, hop) ** 2, axis=1))
    on = fr > .1 * np.percentile(fr[fr > 1e-4], 90)
    k = int(.15 / .01)
    on = np.convolve(on.astype(float), np.ones(2 * k + 1), "same") > 0
    talk = np.clip(np.interp(np.arange(N) / hop, np.arange(len(on)), np.convolve(on.astype(float), np.ones(3) / 3, "same")), 0, 1)
    m = bed()
    m = m * (.05 / rms(m)) * (1 - .4 * talk)[:, None]
    fx = sfx()
    fx = np.stack([reverb(fx[:, c], .8, .1, c + 5) for c in (0, 1)], 1)
    fx = fx * (.04 / rms(fx)) * (1 - .3 * talk)[:, None]
    fade = np.ones(N)
    fade[-int(.4 * SR):] = np.linspace(1, 0, int(.4 * SR))
    mix = (m + fx) * fade[:, None] + (v * (.16 / rms(v[v != 0])))[:, None]
    mix *= min(1, .98 / np.max(np.abs(mix)))
    raw = os.path.join(ROOT, "assets", "audio", "mix_raw.wav")
    sf.write(raw, mix.astype(np.float32), SR, subtype="FLOAT")
    o = ffmpeg("-i", raw, "-af", "loudnorm=I=-13.4:TP=-2.0:LRA=11:print_format=json", "-f", "null", "-").stderr
    meas = json.loads(o[o.rindex("{"):o.rindex("}") + 1])
    af = (f"loudnorm=I=-13.4:TP=-2.0:LRA=11:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
          f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:linear=true")
    out = os.path.join(ROOT, "assets", "audio", "mix.wav")
    ffmpeg("-i", raw, "-af", af + ",alimiter=limit=0.78:level=false:attack=1:release=60", "-ar", str(SR), "-c:a", "pcm_s24le", out)
    os.remove(raw)
    chk = ffmpeg("-i", out, "-af", "ebur128=peak=true", "-f", "null", "-").stderr
    summ = chk[chk.rindex("Summary:"):]
    print("wrote", out, " ".join(ln.strip() for ln in summ.splitlines() if ln.strip().startswith(("I:", "Peak:"))))


if __name__ == "__main__":
    main()
