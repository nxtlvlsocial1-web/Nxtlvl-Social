"""Pick the best Chatterbox take per line: faster-whisper (MIT, base.en) transcribes each take and the take whose words
match the script best wins (ties go to the calmer take 0). Copies winners to voice/el/<take>.wav for build/voice.py.
~/.venvs/tts/bin/python build/pick.py"""
import difflib
import json
import os
import re
import shutil
import soundfile as sf
import torch
import torchaudio.functional as AF
from faster_whisper import WhisperModel

norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " ")).split()  # noqa: E731
takes = json.load(open("voice/takes/takes.json"))
m = WhisperModel("base.en", device="cpu", compute_type="int8")
os.makedirs("voice/el", exist_ok=True)
best = {}
for key, info in sorted(takes.items()):
    a, sr = sf.read(f"voice/takes/{key}.wav", dtype="float32")
    a = AF.resample(torch.from_numpy(a if a.ndim == 1 else a.mean(1)), sr, 16000).numpy()
    segs, _ = m.transcribe(a, language="en", beam_size=5)
    heard = " ".join(s.text.strip() for s in segs)
    score = difflib.SequenceMatcher(None, norm(info["text"]), norm(heard)).ratio()
    info["heard"], info["match"] = heard, round(score, 3)
    line = key.split("_")[0]
    if line not in best or score > best[line][1] + .02:
        best[line] = (key, score)
    print(f"{key}  {score:.2f}  {info['seconds']:5.2f}s  heard: {heard}")
for line, (key, score) in sorted(best.items()):
    shutil.copy(f"voice/takes/{key}.wav", f"voice/el/{line}.wav")
    takes[key]["picked"] = True
    print("pick", line, key, round(score, 2))
json.dump(takes, open("voice/takes/takes.json", "w"), indent=1)
