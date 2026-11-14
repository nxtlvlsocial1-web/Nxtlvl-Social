"""Word-by-word caption timing from the real voice track (the AI skits guide: Whisper for word timings): faster-whisper
(MIT, base.en) transcribes assets/audio/voice.wav with word timestamps, and each script word in build/words.json takes the
time of the matching heard word (difflib alignment inside each line; unmatched words keep their estimate).
~/.venvs/tts/bin/python build/align.py   (after build/voice.py)"""
import difflib
import json
import re
import subprocess

import numpy as np
from faster_whisper import WhisperModel

norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())  # noqa: E731
words = json.load(open("build/words.json"))
cues = json.load(open("build/cues.json"))
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "assets/audio/voice.wav", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
a = np.frombuffer(raw, np.float32)
m = WhisperModel("base.en", device="cpu", compute_type="int8")
segs, _ = m.transcribe(a, word_timestamps=True, beam_size=5, initial_prompt="Creedom. DM automation. 42 views. 7 AM.")
heard = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
moved = 0
for take, (t0, t1) in cues["lines"].items():
    mine = [w for w in words if w["take"] == take]
    hw = [h for h in heard if h[1] >= t0 - .3 and h[2] <= t1 + .3]
    sm = difflib.SequenceMatcher(None, [norm(w["w"]) for w in mine], [norm(h[0]) for h in hw])
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            w, h = mine[blk.a + k], hw[blk.b + k]
            w["s"], w["e"] = round(h[1], 3), round(h[2], 3); moved += 1
json.dump(words, open("build/words.json", "w"), indent=0)
print(f"aligned {moved} of {len(words)} words to the voice")
