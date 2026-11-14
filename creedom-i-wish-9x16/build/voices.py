"""The creator's lines for the Creedom "I Wish..." reel, voiced with open-source models only: a Kokoro-82M (Apache-2.0)
blended voice reference, performed line by line by Chatterbox (MIT) with its own emotion setting per line (exaggeration,
cfg weight). Three takes per line; build/pick.py keeps the best. Chatterbox output carries Resemble's inaudible Perth
watermark. ~/.venvs/tts/bin/python build/voices.py"""
import json
import os
import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

LINES = [  # take, text, exaggeration, cfg weight (lower cfg = slower, more dramatic pacing)
    ("01", "My latest reel... got forty-two views.", .9, .3),
    ("02", "I used trending audio! I posted at seven A M! I even changed my hair!", 1.1, .4),
    ("03", "And still... nothing.", .85, .25),
    ("04", "I wish someone could review my reel... before I post it.", .7, .3),
    ("05", "I wish it could look at my old reels... and tell me what actually worked.", .7, .3),
    ("06", "And I wish it could just set up my D M automation for me.", .8, .35),
    ("07", "Whoa!", 1.2, .4),
    ("08", "That's... actually it.", .8, .3),
    ("09", "I forgot I even made that!", 1.0, .4),
    ("10", "Where have you been all my life?", .95, .3),
    ("11", "Comment Creedom, and I'll send you the link.", .7, .45),
]
os.makedirs("voice/takes", exist_ok=True)
m = ChatterboxTTS.from_pretrained(device="cpu")
log = {}
for take, text, ex, cfg in LINES:
    for k, (ex_k, seed) in enumerate(((ex, 7), (min(1.3, ex + .12), 21), (max(.5, ex - .12), 53))):
        out = f"voice/takes/{take}_{k}.wav"
        if os.path.exists(out):
            continue
        torch.manual_seed(seed)
        wav = m.generate(text, audio_prompt_path="voice/refs/creator.wav", exaggeration=ex_k, cfg_weight=cfg)
        ta.save(out, wav, m.sr)
        log[f"{take}_{k}"] = {"text": text, "exaggeration": ex_k, "cfg_weight": cfg, "seed": seed, "seconds": round(wav.shape[-1] / m.sr, 2)}
        print(take, k, log[f"{take}_{k}"]["seconds"], "s", flush=True)
json.dump(log, open("voice/takes/takes.json", "w"), indent=1)
