"""Music, sound design and the mastered mix for the Postclerk reel.

python3 build/audio.py      (from the project root, after build/voice.py and build/generate.py)

Music: "Thermostat" by Z Asmut (CC BY 3.0, Jamendo, found through Openverse; instrumental, checked with faster-whisper),
143 bpm electronic. Its first section runs under the pitch; on the turn ("But here's what Metricool doesn't give you") it
tape-stops into near silence, and the track's return after its break (69 s in) comes back on "It connects to your AI".
It ducks under the voice. SFX: every visual event build/generate.py logs (build/ev.json) gets a sound from HyperFrames'
bundled library (Pixabay Content License: commercial use, no credit; .claude/skills/media-use/audio/assets/sfx/CREDITS.md).
Writes assets/audio/mix.wav, mastered to -14 LUFS integrated, -1.5 dBTP.
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EV = json.load(open(os.path.join(ROOT, "build", "ev.json")))
SR = 48000
DUR = EV["end"]
N = int(DUR * SR)
LIB = os.path.join(os.path.dirname(ROOT), ".claude", "skills", "media-use", "audio", "assets", "sfx")
LN = EV["lines"]
_C = {}


def load(p):
    if p not in _C:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
        _C[p] = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
    return _C[p]


def lib(n):
    return load(os.path.join(LIB, n + ".mp3"))


def put(bus, x, t, g=1.0, a=0.0, b=None, fin=.005, fout=.04):
    x = x[int(a * SR):int(b * SR) if b else None].copy()
    if len(x) == 0:
        return
    fi, fo = min(len(x), int(fin * SR)), min(len(x), int(fout * SR))
    if fi: x[:fi] *= np.linspace(0, 1, fi)[:, None]
    if fo: x[-fo:] *= np.linspace(1, 0, fo)[:, None]
    i = int(round(t * SR))
    if i < 0:
        x, i = x[-i:], 0
    x = x[: max(0, N - i)]
    bus[i:i + len(x)] += x * g


def tapestop(x, dur=.55):
    """Slow a stereo clip to a stop over its length (pitch falls with the speed)."""
    n = int(dur * SR); x = x[:int(dur * SR * 1.6)]
    sp = np.linspace(1, 0.05, n) ** 1.4
    pos = np.cumsum(sp); pos = pos[pos < len(x) - 1]
    out = np.stack([np.interp(pos, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1)
    out *= np.linspace(1, 0, len(out))[:, None]
    return out


def music():
    m = np.zeros((N, 2))
    tr = load(os.path.join(ROOT, "assets", "music", "thermostat.mp3"))
    turn, back = LN[6][0] - .12, LN[7][0] - .14
    seg = tr[: int(turn * SR)]
    put(m, seg, 0, 1.0, fin=.01, fout=.01)                                       # the pitch
    put(m, tapestop(tr[int(turn * SR):]), turn, 1.0, fin=.001, fout=.01)       # the turn: tape stop
    lo = np.stack([sosfilt(butter(2, 300, "low", fs=SR, output="sos"), tr[int(42 * SR):int(48 * SR), c]) for c in (0, 1)], 1)
    put(m, lo * .5, turn + .5, 1.0, b=back - turn - .5, fin=.2, fout=.05)       # a low hum under the question
    put(m, tr[int(69.0 * SR):], back, 1.0, b=DUR - back, fin=.01, fout=1.2)    # the return, for the AI half
    return m


SFX = {
    "stamp": [("impact-bass-2", .9), ("glitch-3", .25)],
    "swipe": [("whoosh-short", .7)],
    "pop": [("pop", .7)],
    "boom": [("impact-bass-1", .8), ("sparkle", .5)],
    "pops": [("pop", .6, 0), ("pop", .5, .09), ("pop", .45, .18)],
    "whoosh": [("whoosh", .7)],
    "rise": [("whoosh-cinematic", .6)],
    "reveal": [("sparkle", .8), ("impact-bass-1", .45)],
    "ping": [("ping", .55)],
    "tab": [("click-soft", .8)],
    "type": [("typing", .45)],
    "drop": [("pop", .55)],
    "glitch": [("glitch-2", .8), ("impact-bass-2", .5)],
    "zap": [("whoosh-cinematic", .5), ("sparkle", .6)],
    "tick": [("click-soft", .65)],
    "typing": [("typing", .55)],
    "click": [("click", .8)],
    "chime": [("chime", .6)],
}
CUT = {"typing": .9, "type": .55, "whoosh-cinematic": 1.4, "sparkle": 1.2}


def sfx():
    s = np.zeros((N, 2))
    for t, kind, g in EV["ev"]:
        for item in SFX[kind]:
            name, gg = item[0], item[1]; off = item[2] if len(item) > 2 else 0
            b = CUT.get(name)
            put(s, lib(name), t + off, g * gg, b=b, fout=.06 if b else .04)
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
    for a, b in LN:
        talk = np.maximum(talk, np.clip((tt - (a - .15)) / .15, 0, 1) * np.clip(((b + .25) - tt) / .25, 0, 1))
    m, s = music(), sfx()
    m = m * (.12 / rms(m[: int(LN[6][0] * SR)])) * (1 - .55 * talk)[:, None]
    s = s * (.06 / rms(s))
    mix = m + s + (v * (.18 / rms(v[np.abs(v) > 1e-4])))[:, None]
    fade = np.ones(N); fade[-int(.6 * SR):] = np.linspace(1, 0, int(.6 * SR))
    mix *= fade[:, None]
    mix *= min(1, .98 / np.max(np.abs(mix)))
    raw = os.path.join(ROOT, "assets", "audio", "mix_raw.wav")
    sf.write(raw, mix.astype(np.float32), SR, subtype="FLOAT")
    o = ffmpeg("-i", raw, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-").stderr
    meas = json.loads(o[o.rindex("{"):o.rindex("}") + 1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
          f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:linear=true")
    out = os.path.join(ROOT, "assets", "audio", "mix.wav")
    ffmpeg("-i", raw, "-af", af + ",alimiter=limit=0.84:level=false:attack=1:release=60", "-ar", str(SR), "-c:a", "pcm_s24le", out)
    os.remove(raw)
    chk = ffmpeg("-i", out, "-af", "ebur128=peak=true", "-f", "null", "-").stderr
    summ = chk[chk.rindex("Summary:"):]
    print("wrote", out, " ".join(ln.strip() for ln in summ.splitlines() if ln.strip().startswith(("I:", "Peak:"))))


if __name__ == "__main__":
    main()
