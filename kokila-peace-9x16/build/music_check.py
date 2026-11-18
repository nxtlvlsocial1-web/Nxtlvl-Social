"""Vocal check of the music candidates (no singing under the voice): each is split with Demucs (htdemucs, MIT, local),
and its vocal stem measured against the whole mix over 60 s; also tempo and brightness. Writes sfx/music/check.json.
HF_HOME=/root/tts/hf /root/tts/.venv/bin/python build/music_check.py FILE...
"""
import json
import os
import subprocess
import sys

import librosa
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, "cache", "demucs")
res = {}
for f in sys.argv[1:]:
    name = os.path.splitext(os.path.basename(f))[0]
    clip = os.path.join(WORK, name + "_60.wav")
    os.makedirs(WORK, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "20", "-t", "60", "-i", f, "-ac", "2", "-ar", "44100", clip], check=True)
    subprocess.run([sys.executable, "-m", "demucs", "--two-stems", "vocals", "-n", "htdemucs", "-o", WORK, clip], check=True, capture_output=True)
    st = os.path.join(WORK, "htdemucs", name + "_60")
    mix, _ = librosa.load(clip, sr=22050)
    voc, _ = librosa.load(os.path.join(st, "vocals.wav"), sr=22050)
    db = 20 * np.log10(np.sqrt(np.mean(voc ** 2)) / max(np.sqrt(np.mean(mix ** 2)), 1e-9))
    tempo = float(np.atleast_1d(librosa.beat.beat_track(y=mix, sr=22050)[0])[0])
    cent = float(np.median(librosa.feature.spectral_centroid(y=mix, sr=22050)))
    res[name] = {"vocal_db_below_mix": round(float(db), 1), "tempo": round(tempo, 1), "centroid_hz": round(cent)}
    print(name, res[name], flush=True)
json.dump(res, open(os.path.join(ROOT, "sfx", "music", "check.json"), "w"), indent=1)
