"""Pick the creator's takes for v4: faster-whisper checks the words (match >= 0.85, or the best available), then the most
expressive passing take wins: pitch movement (librosa pYIN, semitone spread) plus loudness range. Copies winners to
voice/el/<take>.wav. ~/.venvs/tts/bin/python build/pick2.py"""
import difflib, json, re, shutil
import numpy as np, soundfile as sf, librosa, torch, torchaudio.functional as AF
from faster_whisper import WhisperModel
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " ").replace("kree dum", "creedom")).split()  # noqa: E731
takes = json.load(open("voice/takes2/takes.json"))
m = WhisperModel("base.en", device="cpu", compute_type="int8")
by = {}
for key, info in sorted(takes.items()):
    a, sr = sf.read(f"voice/takes2/{key}.wav", dtype="float32")
    a16 = AF.resample(torch.from_numpy(a), sr, 16000).numpy()
    segs, _ = m.transcribe(a16, language="en", beam_size=5, initial_prompt="Creedom.")
    heard = " ".join(s.text.strip() for s in segs)
    match = difflib.SequenceMatcher(None, norm(info["text"]), norm(heard)).ratio()
    f0, vf, _ = librosa.pyin(a, fmin=70, fmax=500, sr=sr, frame_length=1024)
    f0 = f0[vf & ~np.isnan(f0)]
    spread = float(np.std(12 * np.log2(f0 / np.median(f0)))) if len(f0) > 10 else 0
    rms = librosa.feature.rms(y=a)[0]; act = rms[rms > rms.max() * .05]
    lrange = float(20 * np.log10(np.percentile(act, 95) / max(1e-6, np.percentile(act, 20))))
    score = spread + .15 * lrange
    info.update(heard=heard, match=round(match, 3), spread=round(spread, 2), lrange=round(lrange, 1), score=round(score, 2))
    by.setdefault(key.split("_")[0], []).append((key, info))
    print(f"{key} m={match:.2f} spread={spread:.2f} lr={lrange:.1f} {heard}")
for line, lst in sorted(by.items()):
    ok = [x for x in lst if x[1]["match"] >= .85] or [max(lst, key=lambda x: x[1]["match"])]
    key, info = max(ok, key=lambda x: x[1]["score"])
    shutil.copy(f"voice/takes2/{key}.wav", f"voice/el/{line}.wav"); info["picked"] = True
    print("pick", line, key, info["match"], info["score"])
json.dump(takes, open("voice/takes2/takes.json", "w"), indent=1)
