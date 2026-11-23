"""Background music for find-skills-9x16, generated locally with MusicGen (no catalog track, nothing to license or credit).

<python with torch + transformers> build/music.py      (from the project root)
e.g. a venv with: pip install --index-url https://download.pytorch.org/whl/cpu torch ; pip install transformers scipy soundfile

The owner chose local generation over the HeyGen library or a Creative Commons track. Writes assets/audio/music.wav
(about 29 s, a little longer than the reel). build/sfx.py trims it to the reel, fades the ends and mixes it under the
voice with ducking. The prompt and seed are fixed, so a re-run gives the same track on the same library versions.
"""
import os
import sys

import numpy as np
import soundfile as sf
import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = "facebook/musicgen-small"
PROMPT = ("upbeat modern electronic tech promo, punchy four on the floor drums, bouncy synth bass, bright playful plucks, "
          "warm pads, energetic and fun, clean mix, 120 bpm, no vocals")
SEED, SECONDS = 7, 29

torch.manual_seed(SEED)
proc = AutoProcessor.from_pretrained(MODEL)
model = MusicgenForConditionalGeneration.from_pretrained(MODEL)
inputs = proc(text=[PROMPT], padding=True, return_tensors="pt")
tokens = int(SECONDS * model.config.audio_encoder.frame_rate)
with torch.no_grad():
    audio = model.generate(**inputs, do_sample=True, guidance_scale=3.0, max_new_tokens=tokens)
sr = model.config.audio_encoder.sampling_rate
x = audio[0, 0].cpu().numpy().astype(np.float32)
x = x / (np.max(np.abs(x)) or 1) * 0.9
out = os.path.join(ROOT, "assets", "audio", "music.wav")
sf.write(out, x, sr, subtype="PCM_16")
print(f"wrote {out}: {len(x) / sr:.1f} s at {sr} Hz", file=sys.stderr)
