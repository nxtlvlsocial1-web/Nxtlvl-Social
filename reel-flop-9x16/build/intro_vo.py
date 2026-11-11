"""Intro (v9, owner's idea): reel 1 is an average, skippable hook. Its voice is Chatterbox's own default voice (open
source, MIT; no reference clip, nobody cloned) at low emotion, so it sounds flat. Two takes; build/intro.py uses take 0
unless Whisper finds a slip.
/root/tts/.venv/bin/python build/intro_vo.py
"""
import os

import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "audio", "intro")
# v10 (owner: "make the hey guys person's voice intentionally dumber and funny"): a clueless, goofy delivery
TEXT = "Heyyy guyyys! Uhhh... welcome back to my... channel?"

m = ChatterboxTTS.from_pretrained(device="cpu")
for k, seed in enumerate((3, 17, 29)):
    torch.manual_seed(seed)
    w = m.generate(TEXT, exaggeration=1.1, cfg_weight=.3, temperature=.95)
    ta.save(os.path.join(OUT, f"dumb_t{k}.wav"), w, m.sr)
    print(k, round(w.shape[-1] / m.sr, 2), flush=True)
