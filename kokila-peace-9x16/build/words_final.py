"""Caption word timings measured on the cut itself (assets/video/tight.mp4): Whisper on the joined, sped-up take is
more accurate than raw timings mapped through 50 cuts (the raw pass misplaced "greatest" by 2 s). Each word gets the
line it falls in (plan/words_tight.json "lines"). Writes plan/words_final.json [{w, s, e, line}].
HF_HOME=/root/tts/hf HF_HUB_OFFLINE=1 /root/tts/.venv/bin/python build/words_final.py
"""
import json
import os

from faster_whisper import WhisperModel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "plan", "words_tight.json")))
m = WhisperModel("Systran/faster-whisper-small.en", device="cpu", compute_type="int8")
segs, _ = m.transcribe(os.path.join(ROOT, "assets", "video", "tight.mp4"), word_timestamps=True, language="en", beam_size=5)
out = []
for s in segs:
    for w in s.words:
        mid = (w.start + w.end) / 2
        line = next((k for k, (a, b) in T["lines"].items() if a - .3 <= mid <= b + .3), None)
        out.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "line": line})
json.dump(out, open(os.path.join(ROOT, "plan", "words_final.json"), "w"), indent=0)
print(len(out), "words")
