"""The Autopilot reel's dialogue, voiced with open-source models only.

Kokoro-82M (Apache-2.0) gives each character a voice (voice/refs/<who>.wav, from build/refs.py); Chatterbox (MIT,
Resemble AI) speaks every line in that voice, with an emotion-exaggeration setting per line. Two takes per line; the
best take is picked in build/pick.py by checking its words with faster-whisper. Chatterbox output carries Resemble's
inaudible Perth watermark.
~/.venvs/tts/bin/python build/voices.py
"""
import json
import os
import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

LINES = [
    ("01", "rosa", "Two hundred messages... I can't answer one more.", .65, .4),
    ("02", "theo", "Go to sleep. Your marketing won't.", .5, .5),
    ("03", "rosa", "Wait... who answered all of these?", .8, .35),
    ("04", "theo", "Nobody. It ran itself. For zero dollars.", .55, .45),
    ("05", "rosa", "Want the whole setup? Follow next level social, and comment autopilot.", .55, .5),
]
os.makedirs("voice/takes", exist_ok=True)
m = ChatterboxTTS.from_pretrained(device="cpu")
log = {}
for take, who, text, ex, cfg in LINES:
    for k, (ex_k, seed) in enumerate(((ex, 7), (min(1.0, ex + .15), 21))):
        out = f"voice/takes/{take}_{k}.wav"
        if os.path.exists(out):
            continue
        torch.manual_seed(seed)
        wav = m.generate(text, audio_prompt_path=f"voice/refs/{who}.wav", exaggeration=ex_k, cfg_weight=cfg)
        ta.save(out, wav, m.sr)
        log[f"{take}_{k}"] = {"who": who, "text": text, "exaggeration": ex_k, "cfg_weight": cfg, "seed": seed, "seconds": round(wav.shape[-1] / m.sr, 2)}
        print(take, k, log[f"{take}_{k}"]["seconds"], "s", flush=True)
json.dump(log, open("voice/takes/takes.json", "w"), indent=1)
