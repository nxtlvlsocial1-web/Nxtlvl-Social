"""Word times for the Empty Theater voice: faster-whisper (small.en) on assets/audio/vo.wav, matched word by word onto the script
lines (g0..g8 = the reel's scenes). Whisper writes "150,000" as one token: its span is shared across "a hundred and fifty
thousand"; "chat GPT" is joined into "ChatGPT". -> plan/words.json
HF_HOME=/root/tts/hf /root/tts/.venv/bin/python build/vo_words.py"""
import json
import os
import re
import subprocess

import numpy as np
from faster_whisper import WhisperModel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINES = [("n0", "I asked ChatGPT what I should post about. It asked me ten questions back."),
         ("n1", "Give me content ideas gets you the same ideas as everyone else."),
         ("n2", "So flip it. Ask it to interview you. Ten questions, one at a time."),
         ("n3", "About your life, your skills, what you can't stop talking about."),
         ("n4", "Then ask for three niches only you could own."),
         ("n5", "Built from your answers. Nobody else can copy that."),
         ("n6", "Comment NICHE, and I'll send you the exact prompt, plus five more to plan your first ten reels.")]
raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", os.path.join(ROOT, "assets", "audio", "vo.wav"), "-ar", "16000", "-ac", "1", "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
m = WhisperModel("small.en", device="cpu", compute_type="int8")
segs, _ = m.transcribe(np.frombuffer(raw, dtype=np.float32), word_timestamps=True, beam_size=5)
hyp = []
for s in segs:
    for w in s.words:
        t = w.word.strip()
        low = t.lower().strip(".,?!")
        if re.fullmatch(r"[\d,]+\.?", t):
            parts = ["a", "hundred", "and", "fifty", "thousand"]
            d = (w.end - w.start) / len(parts)
            hyp += [(p, w.start + d * i, w.start + d * (i + 1)) for i, p in enumerate(parts)]
        elif low == "gpt" and hyp and hyp[-1][0].lower().startswith("chat"):
            hyp[-1] = ("chatgpt", hyp[-1][1], w.end)
        else:
            hyp.append((t, w.start, w.end))


def norm(x):
    return re.sub(r"[^a-z0-9']", "", x.lower())


out, i = [], 0
for line, text in LINES:
    for sw in text.split():
        j = i
        while j < len(hyp) and norm(hyp[j][0])[:3] != norm(sw)[:3]:
            j += 1
        if j == len(hyp):          # no match (a slip such as Creedum / Credem): take the next word in order
            print("no match for", line, sw)
            j = min(i, len(hyp) - 1)
        out.append({"line": line, "w": sw, "t0": round(hyp[j][1], 3), "t1": round(hyp[j][2], 3)})
        i = j + 1
json.dump(out, open(os.path.join(ROOT, "plan", "words.json"), "w"), indent=0)
for line, _ in LINES:
    ws = [w for w in out if w["line"] == line]
    print(line, " ".join(f'{w["w"]}@{w["t0"]}' for w in ws))
