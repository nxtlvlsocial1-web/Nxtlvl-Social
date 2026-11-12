"""The Copycat reel's dialogue, voiced with open-source models only.

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
    ("01", "june", "She copied my croissant. My font. Even my cat!", .9, .45),
    ("02", "kane", "Then we watch her. Legally. Public pages only. Zero dollars.", .9, .45),
    ("03", "kane", "Clue one: changedetection dot io. Her prices change? You know in a minute.", .85, .45),
    ("04", "kane", "Clue two: R S S Hub and Mini flux. Every post she makes, in one feed.", .85, .45),
    ("05", "kane", "Clue three: Ollama. An AI on your own laptop reads it all... and writes your briefing.", .85, .45),
    ("06", "june", "A lavender croissant... on Friday?", .9, .4),
    ("07", "kane", "She launches Friday. You launch Thursday.", .9, .4),
    ("08", "june", "A year of copying me... and now she's a day behind!", .9, .45),
    ("09", "kane", "Case closed, kid.", .95, .4),
    ("10", "june", "Want the whole kit? Follow next level social, and comment spy.", .7, .5),
]
os.makedirs("voice/takes", exist_ok=True)
m = ChatterboxTTS.from_pretrained(device="cpu")
log = {}
for take, who, text, ex, cfg in LINES:
    for k, (ex_k, seed) in enumerate(((ex, 7), (min(1.0, ex + .08), 21))):
        out = f"voice/takes/{take}_{k}.wav"
        if os.path.exists(out):
            continue
        torch.manual_seed(seed)
        wav = m.generate(text, audio_prompt_path=f"voice/refs/{who}.wav", exaggeration=ex_k, cfg_weight=cfg)
        ta.save(out, wav, m.sr)
        log[f"{take}_{k}"] = {"who": who, "text": text, "exaggeration": ex_k, "cfg_weight": cfg, "seed": seed, "seconds": round(wav.shape[-1] / m.sr, 2)}
        print(take, k, log[f"{take}_{k}"]["seconds"], "s", flush=True)
json.dump(log, open("voice/takes/takes.json", "w"), indent=1)
