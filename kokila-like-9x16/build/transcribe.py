"""Word timings of a wav with faster-whisper. python3 build/transcribe.py in.wav out.json [model]"""
import json, sys
import wave, numpy as np
from faster_whisper import WhisperModel
src, out = sys.argv[1], sys.argv[2]
m = WhisperModel(sys.argv[3] if len(sys.argv) > 3 else "medium.en", device="cpu", compute_type="int8")
w_ = wave.open(src); audio = np.frombuffer(w_.readframes(w_.getnframes()), np.int16).astype(np.float32) / 32768
segs, _ = m.transcribe(audio, word_timestamps=True, language="en", vad_filter=False, condition_on_previous_text=False)
words = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 3)}
         for s in segs for w in s.words]
json.dump(words, open(out, "w"), indent=0)
print(len(words), "words")
