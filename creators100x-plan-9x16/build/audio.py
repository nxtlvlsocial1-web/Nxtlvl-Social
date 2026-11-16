"""Music, sound effects and the mastered mix for the Creators 100X plan reel.

python3 build/audio.py      (from the project root, after build/voice.py and build/generate.py)

Music: "Positive Whistling" by Ruslan Latypov (CC BY 3.0, Jamendo, via Openverse; no words, checked with faster-whisper),
a light cozy-comedy bed, ducked under the dialogue. SFX: real recordings from Openverse only (CC0 / CC BY;
assets/sfx/CREDITS.md), placed on the picture's events, read from the same cue times the 3D shots use (build/cues.json,
build/words.json) plus the HTML layer's events (build/ev.json). Following the real-sfx method: each sound is brought to
its role's peak (hits -4, whooshes -9, pops / clicks / chimes -14 dBFS), long recordings are cut to their useful slice,
the SFX bus is ducked under the voices, and every placed sound is checked on the bus afterwards.
Writes assets/audio/mix.wav, mastered to -14 LUFS integrated, -1.5 dBTP.
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
CU = json.load(open(os.path.join(B, "cues.json")))
WORDS = json.load(open(os.path.join(B, "words.json")))
EV = json.load(open(os.path.join(B, "ev.json")))
SR = 48000
DUR = EV["end"]
N = int(DUR * SR)
LN = CU["lines"]
Ls = lambda k: LN[k][0]  # noqa: E731
Le = lambda k: LN[k][1]  # noqa: E731
_C = {}


def wd(k, txt):
    import re
    for w in WORDS:
        if w["take"] == k and re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(txt):
            return w["s"]
    return Ls(k)


def load(name):
    if name not in _C:
        p = [os.path.join(ROOT, "assets", "sfx", name + e) for e in (".mp3", ".wav") if os.path.exists(os.path.join(ROOT, "assets", "sfx", name + e))][0] if "/" not in name else name
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
        _C[name] = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
    return _C[name]


ROLE = {"hit": -4, "whoosh": -9, "pop": -14, "click": -14, "chime": -13, "foley": -10}
# name: (role, slice start, slice length or None)
SND = {"pop": ("pop", 0, None), "sparkle": ("chime", 1.25, 1.4), "whoosh": ("whoosh", 0, None), "brick": ("hit", .95, .45), "thump": ("hit", 0, .7),
       "flip": ("foley", 0, None), "plink": ("pop", 0, None), "kettle": ("foley", 4.5, 1.6), "clap": ("hit", 0, None), "typing": ("click", .1, .9),
       "click": ("click", 0, .18), "ding": ("chime", 0, .9), "ping": ("chime", 0, .6), "glock": ("chime", 0, 1.0)}
PLACED = []


def place(bus, name, t, g_db=0.0, fin=.003, fout=.05):
    role, a, ln = SND[name]
    x = load(name)[int(a * SR): int((a + ln) * SR) if ln else None].copy()
    if len(x) == 0:
        return
    pk = np.max(np.abs(x)) + 1e-9
    x *= 10 ** ((ROLE[role] + g_db) / 20) / pk
    fi, fo = min(len(x), int(fin * SR)), min(len(x), int(fout * SR))
    if fi: x[:fi] *= np.linspace(0, 1, fi)[:, None]
    if fo: x[-fo:] *= np.linspace(1, 0, fo)[:, None]
    i = int(round(t * SR))
    if i < 0 or i >= N:
        return
    x = x[: N - i]
    bus[i:i + len(x)] += x
    PLACED.append((round(t, 3), name, i, len(x)))


def sfx():
    s = np.zeros((N, 2))
    # Volt zips out of the laptop
    v0 = Ls("02") - .12
    place(s, "whoosh", v0 + .02, -2); place(s, "pop", v0 + .2); place(s, "sparkle", v0 + .15, -2)
    for i in range(3): place(s, "plink", wd("02", "thirty") + .05 + i * .07, -4)     # the board shimmers
    # step 1: the card floats up; her answers fly in; the card fills
    place(s, "whoosh", Ls("04") - .05, -6)
    for k, w in enumerate(("home", "busy", "more")):
        t = wd("05", w); place(s, "whoosh", t, -5); place(s, "flip", t + .5, -4)
    place(s, "sparkle", wd("05", "more") + .5, -3)
    # step 2: the pillars rise; the temple roof slams; the menu flips
    for w in ("teach", "story", "proof"):
        t = wd("06", w); place(s, "thump", t + .1, -8); place(s, "plink", t + .15, -2)
    rt = Ls("07") + .55
    place(s, "whoosh", rt - .15, -4); place(s, "brick", rt + .2, 0); place(s, "thump", rt + .2, -3)
    place(s, "flip", Ls("08") + .1, 0); place(s, "whoosh", Ls("08") + .1, -6); place(s, "sparkle", Ls("08") + .5, -5)
    # step 3: thirty blocks pop in a wave
    for i in range(30):
        place(s, "plink" if i % 3 else "pop", Ls("09") + .35 + i * .075, -6 + 2 * (i % 2))
    # day nine: the card flies out; the kettle whistles
    place(s, "whoosh", Ls("10") - .05, -3); place(s, "flip", Ls("10") + .5, -3)
    place(s, "kettle", Ls("10") + .6, -10, fin=.3, fout=.4)
    # batch it: the clapperboard
    place(s, "clap", wd("11", "afternoon") - .02, -2)
    # posting all week: seven pings
    for i in range(7): place(s, "ding" if i % 2 == 0 else "ping", Ls("13") + .1 + i * .12, -6)
    # the HTML layer: step chimes, the stamp, the end card
    for t, kind in EV["ev"]:
        if kind == "step": place(s, "glock", t, -2)
        elif kind == "pop": place(s, "pop", t)
        elif kind == "stamp": place(s, "thump", t, -2); place(s, "brick", t, -6)
        elif kind == "typing": place(s, "typing", t, -4, fout=.1)
        elif kind == "click": place(s, "click", t)
        elif kind == "whoosh": place(s, "whoosh", t, -5)
    return s


def ffmpeg(*a):
    return subprocess.run(["ffmpeg", "-y", "-hide_banner", *a], capture_output=True, text=True, check=True)


def main():
    voice, vsr = sf.read(os.path.join(ROOT, "assets", "audio", "voice.wav"))
    assert vsr == SR
    v = np.zeros(N); v[: min(N, len(voice))] = voice[:N]
    rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)  # noqa: E731
    tt = np.arange(N) / SR
    talk = np.zeros(N)
    for a, b in LN.values():
        talk = np.maximum(talk, np.clip((tt - (a - .12)) / .12, 0, 1) * np.clip(((b + .2) - tt) / .2, 0, 1))
    tr = load(os.path.join(ROOT, "assets", "music", "positive_whistling.mp3"))
    m = np.zeros((N, 2)); n = min(N, len(tr)); m[:n] = tr[:n]
    m[-int(1.5 * SR):] *= np.linspace(1, 0, int(1.5 * SR))[:, None]
    s = sfx()
    # check every placed sound is on the bus where it should be
    miss = [p for p in PLACED if np.max(np.abs(s[p[2]:p[2] + max(1, min(p[3], int(.05 * SR)))])) < 1e-4]
    m = m * (.11 / rms(m)) * (1 - .6 * talk)[:, None]
    s = s * (1 - .5 * talk)[:, None]                                   # SFX about 6 dB under the voices
    mix = m + s * 1.6 + (v * (.2 / rms(v[np.abs(v) > 1e-4])))[:, None]
    fade = np.ones(N); fade[-int(.6 * SR):] = np.linspace(1, 0, int(.6 * SR))
    mix *= fade[:, None]
    mix *= min(1, .98 / np.max(np.abs(mix)))
    raw = os.path.join(ROOT, "assets", "audio", "mix_raw.wav")
    sf.write(raw, mix.astype(np.float32), SR, subtype="FLOAT")
    sf.write(os.path.join(ROOT, "assets", "audio", "sfx_track.wav"), (s * 1.6).astype(np.float32), SR, subtype="FLOAT")
    o = ffmpeg("-i", raw, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-").stderr
    meas = json.loads(o[o.rindex("{"):o.rindex("}") + 1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
          f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:linear=true")
    out = os.path.join(ROOT, "assets", "audio", "mix.wav")
    ffmpeg("-i", raw, "-af", af + ",alimiter=limit=0.84:level=false:attack=1:release=60", "-ar", str(SR), "-c:a", "pcm_s24le", out)
    os.remove(raw)
    chk = ffmpeg("-i", out, "-af", "ebur128=peak=true", "-f", "null", "-").stderr
    summ = chk[chk.rindex("Summary:"):]
    print(f"{len(PLACED)} sounds placed, {len(miss)} missing on the bus")
    print("wrote", out, " ".join(ln.strip() for ln in summ.splitlines() if ln.strip().startswith(("I:", "Peak:"))))


if __name__ == "__main__":
    main()
