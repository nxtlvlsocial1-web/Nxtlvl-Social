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
    best = None
    for k in (0, 1):
        p = os.path.join(A, f"bland_t{k}.wav")
        segs, _ = m.transcribe(p, word_timestamps=True, language="en")
        ws = [w for s in segs for w in s.words]
        txt = " ".join(w.word.strip().lower() for w in ws)
        ok = "welcome back" in txt and "channel" in txt
        if ok and best is None:
            best = (k, ws)
    k, ws = best
    y, _ = librosa.load(os.path.join(A, f"bland_t{k}.wav"), sr=SR)
    lead = max(0, ws[0].start - .05)
    y = y[int(lead * SR):]
    words = [{"w": w.word.strip(), "t0": round(w.start - lead, 3), "t1": round(w.end - lead, 3)} for w in ws]
    td = next(w for w in words if w["w"].lower().startswith("today"))
    S1 = round(td["t1"] + .06, 3)                    # he gets as far as "So today..." and is swiped away
    gib = json.load(open(os.path.join(ROOT, "plan", "pixo_sylls.json")))
    G0 = round(S1 + .32, 3)
    S2 = round(G0 + gib["dur"] - .05, 3)
    T0 = round(S2 + .75, 3)
    out = np.zeros((int((T0 + .1) * SR), 2), dtype=np.float32)
    b = y[:int((S1 + .06) * SR)]
    fade = int(.06 * SR)
    b[-fade:] *= np.linspace(1, 0, fade)
    out[:len(b), 0] += b * .9
    out[:len(b), 1] += b * .9
    g, gsr = sf.read(os.path.join(A, "gibberish.wav"), dtype="float32")
    i = int(G0 * SR)
    n = min(len(g), len(out) - i)
    out[i:i + n] += g[:n] * .8
    sf.write(os.path.join(A, "intro.wav"), out, SR)
    json.dump({"take": k, "words": words, "S1": S1, "G0": G0, "S2": S2, "T0": T0}, open(os.path.join(ROOT, "plan", "intro_timing.json"), "w"), indent=0)
    print(f"take {k}; scroll to reel 2 at {S1}s, gibberish {G0}s, back at {S2}s, our video at {T0}s")


if __name__ == "__main__":
    main()
