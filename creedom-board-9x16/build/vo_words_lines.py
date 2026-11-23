"""Word times per line: the voice is built line by line (build/vo_kokoro.py writes plan/line_times.json), so each line is
transcribed on its own (faster-whisper small.en); when the word counts match, whisper's times are used, otherwise the line is
split by character length. Writes plan/words.json in the format build/fx.py reads.
HF_HOME=/root/tts/hf /root/tts/.venv/bin/python build/vo_words_lines.py"""
import json, os, subprocess
import numpy as np
from faster_whisper import WhisperModel
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lines = {l["id"]: l["text"].replace("Cree-dum", "Creedom") for l in json.load(open(os.path.join(ROOT, "plan", "script.json")))}
times = json.load(open(os.path.join(ROOT, "plan", "line_times.json")))
y = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(ROOT, "assets", "audio", "vo.wav"), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                 capture_output=True).stdout, np.float32)
m = WhisperModel("small.en", device="cpu", compute_type="int8")
out = []
for lid, (a, b) in times.items():
    words = lines[lid].split()
    seg = y[int(a * 16000):int(b * 16000)]
    hyp = [w for s in m.transcribe(seg, word_timestamps=True)[0] for w in s.words]
    if len(hyp) == len(words):
        ts = [(a + w.start, a + w.end) for w in hyp]
        how = "whisper"
    else:
        lens = [len(w) + 2 for w in words]
        tot, acc, ts = sum(lens), 0, []
        for L in lens:
            ts.append((a + (b - a) * acc / tot, a + (b - a) * (acc + L) / tot))
            acc += L
        how = f"split ({len(hyp)} vs {len(words)})"
    for w, (t0, t1) in zip(words, ts):
        out.append({"line": lid, "w": w, "t0": round(t0, 3), "t1": round(t1, 3)})
    print(lid, how)
json.dump(out, open(os.path.join(ROOT, "plan", "words.json"), "w"), indent=0)
