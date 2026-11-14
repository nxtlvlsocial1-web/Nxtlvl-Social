"""Cut Cree's chirp library out of real bird recordings (CC0 / CC BY, via Openverse and media-use).

Each source is high-passed, split into single chirps where the loudness dips, and every chirp from 45 to 260 ms that
stands well clear of its background is kept, trimmed, faded and normalised. Writes assets/sfx/cree/syl/*.wav and
assets/sfx/cree/syllables.json (file, source, length, dominant frequency, brightness, clarity).
python3 build/cree_syllables.py
"""
import json
import os
import subprocess

import librosa
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfiltfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "assets", "sfx", "cree")
SR = 48000
SOURCES = ["src_001", "src_002", "src_003", "src_005", "src_006"]


def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def main():
    out = os.path.join(D, "syl"); os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        os.remove(os.path.join(out, f))
    lib = []
    for src in SOURCES:
        x = load(os.path.join(D, src + ".mp3"))
        x = sosfiltfilt(butter(4, 1100, "high", fs=SR, output="sos"), x)
        bg = np.percentile(np.abs(x), 30) + 1e-7
        for a, b in librosa.effects.split(x, top_db=40, frame_length=1024, hop_length=128):
            seg = x[a:b]
            for c, d in librosa.effects.split(seg, top_db=14, frame_length=512, hop_length=96):  # single chirps inside a phrase
                s = seg[max(0, c - 96):d + 96]
                L = len(s) / SR
                if not (.045 <= L <= .26):
                    continue
                pk = np.max(np.abs(s)); clar = 20 * np.log10(pk / bg)
                if clar < 30:
                    continue
                spec = np.abs(np.fft.rfft(s * np.hanning(len(s)))); fr = np.fft.rfftfreq(len(s), 1 / SR)
                dom = float(fr[np.argmax(spec)]); cen = float(np.sum(fr * spec) / np.sum(spec))
                fi, fo = int(.004 * SR), int(.012 * SR)
                s = s.copy(); s[:fi] *= np.linspace(0, 1, fi); s[-fo:] *= np.linspace(1, 0, fo)
                s = s / np.max(np.abs(s)) * .9
                name = f"{src[4:]}_{len(lib):03d}.wav"
                sf.write(os.path.join(out, name), s.astype(np.float32), SR)
                lib.append({"file": name, "src": src, "len": round(L, 3), "dom": round(dom), "cen": round(cen), "clar": round(clar, 1)})
    json.dump(lib, open(os.path.join(D, "syllables.json"), "w"), indent=0)
    print(len(lib), "chirps;", {s: sum(1 for r in lib if r["src"] == s) for s in SOURCES})


if __name__ == "__main__":
    main()
