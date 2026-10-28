"""Sound design and the mastered mix for the 3 AM database horror short.

python3 build/audio.py      (from the project root, after build/generate.py; needs numpy, scipy, soundfile, ffmpeg)

Music: the original score in build/score.py, composed in code (no licence or credit needed).
SFX: recorded hits from HyperFrames' bundled library (Pixabay Content License: commercial use, no credit needed;
.claude/skills/media-use/audio/assets/sfx/CREDITS.md) plus room tone, fans, clunks and buzzes synthesized here.
The two blackouts (after "...I know." and after "revoked") are true silence apart from the voice. Writes
assets/audio/mix.wav, mastered to -14 LUFS integrated, -1.5 dBTP.
"""
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
L, E = T["l"], T["e"]
SR = 48000
DUR = T["end"]
N = int(DUR * SR)
rng = np.random.default_rng(13)
SFX = np.zeros((N, 2))
BED = np.zeros((N, 2))                   # continuous beds (room tone, fans), kept out of the SFX reverb
LIB = os.path.join(os.path.dirname(ROOT), ".claude", "skills", "media-use", "audio", "assets", "sfx")
_S = {}
BLK0, EYES, CUT, CTA = E[7] + .35, T["eyes"], T["cut"], T["cta"]
SRV0, SRV1 = L[4] - .05, L[6] - .05      # the server-room shot


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


def curve(pts):
    t, g = zip(*pts)
    return np.interp(np.arange(N) / SR, t, g)


def put(x, t, g=1.0, pan=0.0, buf=None):
    buf = SFX if buf is None else buf
    i = int(round(t * SR))
    if i >= N:
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


# ---------------------------------------------------------------- sounds
def tone(f, d, dec=6):
    t = tt(d)
    return np.sin(2 * np.pi * f * t) * np.exp(-t * dec) * np.minimum(1, t / .003)


def clack():                 # the Enter key, bottoming out hard
    t = tt(.25)
    return (bp(rng.standard_normal(len(t)), 1500, 9000) * np.exp(-t * 90) * .9 + np.sin(2 * np.pi * np.cumsum(180 + 300 * np.exp(-t * 80)) / SR) * np.exp(-t * 40) * .6) * .5


def tick():                  # the wall clock
    t = tt(.05)
    return (bp(rng.standard_normal(len(t)), 2500, 7000) * np.exp(-t * 180) + tone(2900, .05, 110) * .3) * .2


def clunk():                 # a ceiling light row dying: relay clunk, a ballast pop, the hum sagging away
    t = tt(.9)
    body = np.sin(2 * np.pi * np.cumsum(70 + 90 * np.exp(-t * 35)) / SR) * np.exp(-t * 18)
    snap = bp(rng.standard_normal(len(t)), 1200, 6000) * np.exp(-t * 70) * .6
    hum = (np.sin(2 * np.pi * np.cumsum(120 * (1 - .4 * t)) / SR) + .4 * np.sin(2 * np.pi * np.cumsum(240 * (1 - .4 * t)) / SR)) * np.exp(-t * 6) * .25
    return np.tanh(1.5 * (body + snap + hum)) * .5


def power_on():              # a light row flickering back: tink-tink-hum
    t = tt(.8)
    x = sum(bp(rng.standard_normal(len(t)), 2000, 8000) * np.exp(-np.maximum(0, t - o) * 90) * (t >= o) for o in (0, .07, .16)) * .25
    hum = (np.sin(2 * np.pi * 120 * t) + .5 * np.sin(2 * np.pi * 240 * t)) * np.minimum(1, t / .2) * np.exp(-t * 3) * .12
    return x + hum


def buzz(d=.32):             # the phone vibrating on the desk
    t = tt(d)
    x = np.sign(np.sin(2 * np.pi * 165 * t)) * (np.sin(2 * np.pi * 9 * t) > -.4)
    return lp(x, 1600) * .14 * np.clip((d - t) / .04, 0, 1) * np.minimum(1, t / .01)


def beep(f=880, d=.16):      # a rack alarm, far down the corridor
    t = tt(d)
    return lp(np.sign(np.sin(2 * np.pi * f * t)), 3000) * np.minimum(1, t / .005) * np.clip((d - t) / .01, 0, 1) * .06


def zap(d):                  # the lights shorting on "revoked"
    t = tt(d)
    x = np.sign(np.sin(2 * np.pi * 120 * t)) * (rng.random(len(t)) > .3)
    return (lp(x, 4000) * (.5 + .5 * (np.sin(2 * np.pi * 13 * t) > 0)) + bp(rng.standard_normal(len(t)), 3000, 9000) * (rng.random(len(t)) > .995) * 3) * .08


def power_down(d=.7):
    t = tt(d)
    return np.sin(2 * np.pi * np.cumsum(400 * np.exp(-t * 4)) / SR) * np.exp(-t * 4) * .2 + np.sin(2 * np.pi * np.cumsum(60 * np.exp(-t * 2)) / SR) * np.exp(-t * 3) * .3


def bed():
    """Room tone (HVAC hum and air) under the office, the server room's fans and whine, both dying on cue."""
    t = np.arange(N) / SR
    air = np.stack([lp(rng.standard_normal(N), 900, 2) for _ in range(2)], 1) * .5
    hum = (np.sin(2 * np.pi * 60 * t) + .5 * np.sin(2 * np.pi * 120 * t) + .2 * np.sin(2 * np.pi * 180 * t))[:, None] * .06
    office = curve([(0, 1), (T["rows"], 1), (T["rows"] + 1, .55), (L[11] + .4, .55), (T["done"], 1), (T["revoked"], 1), (T["end"], 1)])
    inoff = 1 - curve([(SRV0 - .001, 0), (SRV0, 1), (SRV1, 1), (SRV1 + .001, 0)])
    BED[:] += (air + hum) * (office * inoff)[:, None]
    # the fans: broadband roar and a 1.1 kHz whine whose pitch falls as they die after "checked"
    dead = T["checked"] + .25
    pitch = np.where(t < dead, 1.0, np.maximum(.15, np.exp(-(t - dead) * 1.4)))
    whine = np.sin(2 * np.pi * np.cumsum(1100 * pitch) / SR) * .05 + np.sin(2 * np.pi * np.cumsum(2210 * pitch) / SR) * .02
    roar = np.stack([bp(rng.standard_normal(N), 150, 5000) for _ in range(2)], 1)
    fan = curve([(SRV0 - .001, 0), (SRV0, 1), (dead, 1), (dead + 1.2, .05), (SRV1, .05), (SRV1 + .001, 0)])
    BED[:] += (roar * 1.4 + whine[:, None]) * fan[:, None]


# ---------------------------------------------------------------- the sound design, on world.js's cue times
def sfx():
    # the wall clock: one tick a second until the blackout, then time stops
    t = .1
    while t < BLK0:
        put(tick(), t, 1, .5)
        t += 1.0
    # HOOK: the Enter key, hard and close, with a long tail; the screen floods red
    put(reverb(np.pad(clack(), (0, int(1.5 * SR))), 2.0, .45, 3), T["enter"] - .04, 1.3)
    put(smp("key-press", .2), T["enter"] - .05, .6)
    put(smp("impact-bass-2"), T["enter"], .8)
    put(smp("error", .7), T["enter"] + .05, .25)
    put(smp("glitch-1", .4), T["enter"] + .02, .3)
    # hard cuts get a CCTV tick
    for c in (L[1] - .05, L[2] - .05, L[3] - .05, L[11] - .05):
        put(smp("glitch-2", .15), c, .3)
    put(smp("whoosh-cinematic")[int(1.0 * SR):int(2.4 * SR)], SRV0 - .4, .45)
    # "One point two million rows": the lights die row by row
    for r in (3, 2, 1, 0):
        put(clunk(), T["rows"] + (3 - r) * .28, 1.0, (r - 1.5) / 2.5)
    # server room: alarms bleed in with the red on "March", die with the fans on "checked"
    for i in range(4):
        put(beep(988 if i % 2 else 740), T["march"] + .1 + i * .28, 1, -.3)
    put(smp("error", .8), T["checked"] + .2, .2)
    # the phone, filling with alerts
    for k in range(5):
        a = L[6] - .3 + k * .38
        put(buzz(), a, 1, .35)
        put(smp("notification", .5), a + .02, .1, .35)
    # the blackout is silence; the eyes open on a glitch
    put(smp("glitch-3", .5), EYES - .02, .55)
    put(smp("impact-bass-1"), EYES, .7)
    # the snapshot card slides in
    put(smp("whoosh-cinematic")[int(1.6 * SR):int(3.0 * SR)], T["snapshot"] - .5, .4)
    put(smp("sparkle"), T["snapshot"] + .1, .25)
    # the log lines on the monitor
    for k in range(5):
        put(smp("click-soft", .15), L[10] - .3 + k * .5, .35, .2)
    # "Restoring now.": ticks speeding up to 100 %, the lights coming back row by row, a chime on done
    t, gap = L[11] + .2, .12
    while t < T["done"]:
        put(tick(), t, .6, -.2)
        t += gap
        gap = max(.04, gap * .9)
    for r in range(4):
        put(power_on(), L[11] + .4 + r * ((T["done"] - L[11] - .4) / 4), .9, (r - 1.5) / 2.5)
    put(smp("chime"), T["done"], .35)
    # "revoked": the lights short out, then everything dies
    put(zap(CUT - T["revoked"] + .05), T["revoked"] - .05, 1.0)
    put(smp("glitch-1", .5), T["revoked"] - .05, .4)
    put(smp("impact-bass-2"), CUT, .9)
    put(power_down(), CUT, 1.0)
    # CTA: the eyes come back, BACKUP slams in letter by letter
    put(smp("glitch-2", .3), CTA - .02, .4)
    for i in range(6):
        put(smp("impact-bass-1", .4), T["backup"] - .08 + i * .07, .18, (i - 2.5) / 4)
    put(smp("glitch-3", .4), T["end"] - .5, .25)


def ffmpeg(*a):
    return subprocess.run(["ffmpeg", "-y", "-hide_banner", *a], capture_output=True, text=True, check=True)


def main():
    bed()
    sfx()
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
    ramp = np.convolve(on.astype(float), np.ones(3) / 3, "same")
    talk = np.clip(np.interp(np.arange(N) / hop, np.arange(len(ramp)), ramp), 0, 1)
    fx = np.stack([reverb(SFX[:, c], 1.4, .2, c + 2) for c in (0, 1)], 1)
    fx = fx * (.05 / rms(fx)) * (1 - .4 * talk)[:, None]
    bd = BED * (.012 / rms(BED))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from score import compose
    m = compose(T, N)
    sf.write(os.path.join(ROOT, "assets", "audio", "score.wav"), m.astype(np.float32), SR, subtype="PCM_24")
    music = m * (.07 / rms(m)) * (1 - .35 * talk)[:, None]
    # true silence in the blackouts (the voice stays: "production access" is spoken into the dark)
    gate = curve([(0, 1), (BLK0, 1), (BLK0 + .02, 0), (EYES - .03, 0), (EYES - .01, 1), (CUT + .7, 1), (CUT + .9, 0), (CTA - .25, 0), (CTA - .2, 1), (DUR, 1)])
    bed_gate = curve([(0, 1), (BLK0, 1), (BLK0 + .02, 0), (EYES - .03, 0), (EYES - .01, 1), (CUT, 1), (CUT + .02, 0), (CTA - .25, 0), (CTA - .2, .4), (DUR, .4)])
    score = (music + fx) * gate[:, None] + bd * bed_gate[:, None]
    fade = np.ones(N)
    fade[-int(.3 * SR):] = np.linspace(1, 0, int(.3 * SR))
    score *= fade[:, None]
    vv = reverb(v, .8, .08, 9)
    mix = score + (vv * (.15 / rms(v[v != 0])))[:, None]
    mix *= min(1, .98 / np.max(np.abs(mix)))
    raw = os.path.join(ROOT, "assets", "audio", "mix_raw.wav")
    sf.write(raw, mix.astype(np.float32), SR, subtype="FLOAT")
    o = ffmpeg("-i", raw, "-af", "loudnorm=I=-13.1:TP=-2.0:LRA=14:print_format=json", "-f", "null", "-").stderr
    meas = json.loads(o[o.rindex("{"):o.rindex("}") + 1])
    af = (f"loudnorm=I=-13.1:TP=-2.0:LRA=14:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
          f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:linear=true")
    out = os.path.join(ROOT, "assets", "audio", "mix.wav")
    ffmpeg("-i", raw, "-af", af + ",alimiter=limit=0.78:level=false:attack=1:release=60", "-ar", str(SR), "-c:a", "pcm_s24le", out)
    os.remove(raw)
    chk = ffmpeg("-i", out, "-af", "ebur128=peak=true", "-f", "null", "-").stderr
    summ = chk[chk.rindex("Summary:"):]
    print("wrote", out, " ".join(ln.strip() for ln in summ.splitlines() if ln.strip().startswith(("I:", "Peak:", "LRA:"))))


if __name__ == "__main__":
    main()
