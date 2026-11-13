"""The real estate what-if's dialogue, voiced with open-source models only: Kokoro-82M (Apache-2.0) gives each character a
voice (voice/refs/<who>.wav) and Chatterbox (MIT) performs every line with its own emotion setting. Two takes per line;
build/pick.py keeps the take whose words match best. Chatterbox output carries Resemble's inaudible Perth watermark.
~/.venvs/tts/bin/python build/voices.py"""
import json
import os
import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

LINES = [
    ("01", "marcus", "Monday. Nine A M. Everyone in town is looking for a house... and my phone is dead silent.", .7, .45),
    ("02", "lena", "Marcus, they're all asking ChatGPT. And it keeps saying Prime Nest.", .8, .45),
    ("03", "marcus", "Prime Nest? They spelled kitchen wrong on their last listing!", .95, .4),
    ("04", "lena", "They claimed their business on ChatGPT. We didn't. Watch.", .75, .45),
    ("05", "lena", "Business Hub. Search Keystone Realty. Get Started. Verify with our office phone. Quick I D check...", .7, .5),
    ("06", "marcus", "Wait. Is that a blue check? On our sign?", .95, .4),
    ("07", "lena", "It launched November tenth, and it's free. Most agencies still haven't done it.", .75, .5),
    ("08", "marcus", "Okay... who's buying a house today?", .85, .4),
    ("09", "lena", "Want the checklist? Follow next level social, and comment chat G P T.", .7, .5),
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
