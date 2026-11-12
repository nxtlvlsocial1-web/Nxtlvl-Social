"""Extra takes (t2, t3) for lines whose first two takes slipped (Whisper heard "describe again", "clock code") or had a
pitch glitch. /root/tts/.venv/bin/python build/vo_more.py g03 g09"""
import os
import sys

import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vo import LINES, OUT, REF  # noqa: E402

want = set(sys.argv[1:])
m = ChatterboxTTS.from_pretrained(device="cpu")
m.prepare_conditionals(REF, exaggeration=.6)
for lid, text, beat, ex in LINES:
    if lid not in want:
        continue
    for take, seed in ((2, 41), (3, 53)):
        torch.manual_seed(seed)
        w = m.generate(text, audio_prompt_path=REF, exaggeration=ex, cfg_weight=.4, temperature=.75)
        ta.save(os.path.join(OUT, f"{lid}_t{take}.wav"), w, m.sr)
        print(lid, take, round(w.shape[-1] / m.sr, 2), flush=True)
