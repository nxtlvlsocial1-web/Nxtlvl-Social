"""Pick one Chatterbox take per line (assets/audio/vo_takes/<id>_t<k>.wav): fewest word errors against the script
(faster-whisper small.en), then the one closer to the line's median pace. Writes assets/audio/vo/<id>.wav (24 kHz) for
build/vo_assemble.py, and plan/vo_pick.json.
HF_HOME=/root/tts/hf HF_HUB_OFFLINE=1 /root/tts/.venv/bin/python build/vo_pick.py
"""
import glob
import json
import os
import re

import numpy as np
import soundfile as sf
import librosa
from faster_whisper import WhisperModel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def words(t):
    return re.sub(r"[^a-z0-9' ]", " ", t.lower().replace("-", " ")).split()


def wer(ref, hyp):
    d = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        prev, d[0] = d[0], i
        for j, h in enumerate(hyp, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (r != h))
    return d[-1]


def main():
    wm = WhisperModel("Systran/faster-whisper-small.en", device="cpu", compute_type="int8")
    out = os.path.join(ROOT, "assets", "audio", "vo")
    os.makedirs(out, exist_ok=True)
    log = {}
    for ln in json.load(open(os.path.join(ROOT, "plan", "script.json"))):
        best = None
        for p in sorted(glob.glob(os.path.join(ROOT, "assets", "audio", "vo_takes", f"{ln['id']}_t*.wav"))):
            y, sr = librosa.load(p, sr=24000)
            segs, _ = wm.transcribe(p, language="en", beam_size=5)
            heard = " ".join(s.text for s in segs)
            e = wer(words(ln["text"]), words(heard))
            cand = (e, len(y) / sr, p, heard, y)
            print(ln["id"], os.path.basename(p), "errors", e, round(len(y) / sr, 2), "|", heard.strip(), flush=True)
            if best is None or cand[:2] < best[:2]:
                best = cand
        sf.write(os.path.join(out, ln["id"] + ".wav"), best[4].astype(np.float32), 24000)
        log[ln["id"]] = {"take": os.path.basename(best[2]), "errors": best[0], "heard": best[3].strip()}
    json.dump(log, open(os.path.join(ROOT, "plan", "vo_pick.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
