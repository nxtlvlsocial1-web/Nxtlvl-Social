"""Word times for the v3 voice: faster-whisper (small.en) on assets/audio/vo.wav, matched word by word onto the script
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
LINES = [("g0", "This is the secret AI quietly growing Instagram accounts."),
         ("g1", "And no, it's not ChatGPT."),
         ("g2", "It's Creedom AI. An Instagram coach that reads your account."),
         ("g3", "It finds what's working, and what's killing your views."),
         ("g4", "It checks your reel before you post."),
         ("g5", "Tells you what to post next."),
         ("g6", "And the crazy part? It shows you if the advice actually worked."),
         ("g7", "Over a hundred and fifty thousand creators use it. Your first account read is free."),
         ("g8", "Comment GROW, and I'll send you the secret.")]
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
            j = i
        out.append({"line": line, "w": sw, "t0": round(hyp[j][1], 3), "t1": round(hyp[j][2], 3)})
        i = j + 1
json.dump(out, open(os.path.join(ROOT, "plan", "words.json"), "w"), indent=0)
for line, _ in LINES:
    ws = [w for w in out if w["line"] == line]
    print(line, " ".join(f'{w["w"]}@{w["t0"]}' for w in ws))
