"""Intro audio + timing (v9). Picks the bland take (Whisper: the script's words, no slip), cuts it where the viewer
scrolls away (just after "channel!", mid "So today..."), places Pixo's gibberish on reel 2, and works out the intro's
beats: S1 scroll to reel 2, G0 gibberish starts, S2 scroll back to reel 1, T0 our video starts.
Writes assets/audio/intro/intro.wav (0..T0) and plan/intro_timing.json.
/root/tts/.venv/bin/python build/intro_audio.py
"""
import json
import os

import librosa
import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets", "audio", "intro")
SR = 48000


def main():
    m = WhisperModel("Systran/faster-whisper-small.en", device="cpu", compute_type="int8")
    # v10: the goofy take (build/intro_vo.py, take 2: "Hey... guys, ...welcome back..."), two semitones up, sillier
    k = 2
    segs, _ = m.transcribe(os.path.join(A, f"dumb_t{k}.wav"), word_timestamps=True, language="en")
    ws = [w for s in segs for w in s.words]
    y, _ = librosa.load(os.path.join(A, f"dumb_t{k}.wav"), sr=SR)
    y = librosa.effects.pitch_shift(y, sr=SR, n_steps=2)
    lead = max(0, ws[0].start - .05)
    y = y[int(lead * SR):]
    words = [{"w": w.word.strip(), "t0": round(w.start - lead, 3), "t1": round(w.end - lead, 3)} for w in ws]
    # v11 (owner: the dull video "may not be understood by many viewers", overplay it): he drawls the whole
    # "...welcome back" (about 3 s, the "first three seconds" the voiceover then calls back to) before the swipe
    wl = next(w for w in words if w["w"].lower().startswith("back"))
    S1 = round(wl["t1"] + .05, 3)
    dance = json.load(open(os.path.join(ROOT, "plan", "dance.json")))
    G0 = round(S1 + .3, 3)                           # the mascots' song starts as reel 2 lands
    S2 = round(G0 + dance["beat"] * 4 + .05, 3)      # one bar of dancing, then back to reel 1
    T0 = round(S2 + .55, 3)
    out = np.zeros((int((T0 + .1) * SR), 2), dtype=np.float32)
    b = y[:int((S1 + .06) * SR)]
    fade = int(.06 * SR)
    b[-fade:] *= np.linspace(1, 0, fade)
    # level it with our voiceover: RMS to about -12 dBFS, then a soft limiter
    act = b[np.abs(b) > .01]
    b = np.tanh(b * (.24 / max(np.sqrt(np.mean(act ** 2)), 1e-4)) * 1.3) / 1.3
    out[:len(b), 0] += b
    out[:len(b), 1] += b
    g, gsr = sf.read(os.path.join(A, "dance.wav"), dtype="float32")
    g = g[:int((S2 - G0 + .12) * SR)]
    f2 = int(.1 * SR)
    g[-f2:] *= np.linspace(1, 0, f2)[:, None]
    i = int(G0 * SR)
    n = min(len(g), len(out) - i)
    out[i:i + n] += g[:n] * .55
    sf.write(os.path.join(A, "intro.wav"), out, SR)
    json.dump({"take": k, "words": words, "S1": S1, "G0": G0, "S2": S2, "T0": T0}, open(os.path.join(ROOT, "plan", "intro_timing.json"), "w"), indent=0)
    print(f"take {k}; scroll to reel 2 at {S1}s, gibberish {G0}s, back at {S2}s, our video at {T0}s")


if __name__ == "__main__":
    main()
