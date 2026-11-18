"""Word timings for the raw take (footage/face_1080.mp4): faster-whisper small.en, local, word timestamps.
Writes plan/words_raw.json [{w, s, e, p}] (s/e in seconds of the raw file, p = Whisper's confidence).
HF_HOME=/root/tts/hf HF_HUB_OFFLINE=1 /root/tts/.venv/bin/python build/words.py
"""
import json
import os
import subprocess

from faster_whisper import WhisperModel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
wav = os.path.join(ROOT, "cache", "raw16k.wav")
os.makedirs(os.path.dirname(wav), exist_ok=True)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(ROOT, "footage", "face_1080.mp4"), "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
m = WhisperModel("Systran/faster-whisper-small.en", device="cpu", compute_type="int8")
segs, _ = m.transcribe(wav, word_timestamps=True, language="en", beam_size=5, vad_filter=False)
out = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 3)} for s in segs for w in s.words]
json.dump(out, open(os.path.join(ROOT, "plan", "words_raw.json"), "w"), indent=0)
print(len(out), "words")
