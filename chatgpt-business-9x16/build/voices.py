"""The ChatGPT business-profile reel's narration, voiced with open-source models only: Kokoro-82M (Apache-2.0) gives the
narrator's voice (voice/refs/nar.wav, from build/refs.py) and Chatterbox (MIT) speaks every line with energy. Two takes
per line; build/pick.py keeps the take whose words match best. Chatterbox output carries Resemble's inaudible Perth
watermark. ~/.venvs/tts/bin/python build/voices.py"""
import json
import os
import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

LINES = [
    ("01", "nar", "ChatGPT now recommends businesses. Is yours on it?", .75, .5),
    ("02", "nar", "Since November tenth, you can claim your business profile. For free.", .7, .5),
    ("03", "nar", "Step one. Log in, and open Business Hub: chat G P T dot com, slash business hub.", .65, .5),
    ("04", "nar", "Step two. Search your business, and tap Get Started.", .7, .5),
    ("05", "nar", "Step three. Prove it's yours, with your phone, email, website, or Shopify.", .7, .5),
    ("06", "nar", "Step four. A quick I D check, and you get the blue check.", .75, .5),
    ("07", "nar", "Then add your prices and stock, and see how often ChatGPT mentions you.", .7, .5),
    ("08", "nar", "Online businesses can claim anywhere ChatGPT works. Local shops, U S listings for now.", .65, .5),
    ("09", "nar", "Comment chat G P T, and I'll send you the full checklist. Follow next level social for more.", .7, .5),
]
os.makedirs("voice/takes", exist_ok=True)
m = ChatterboxTTS.from_pretrained(device="cpu")
log = {}
for take, who, text, ex, cfg in LINES:
    for k, (ex_k, seed) in enumerate(((ex, 7), (min(1.0, ex + .1), 21))):
        out = f"voice/takes/{take}_{k}.wav"
        if os.path.exists(out):
            continue
        torch.manual_seed(seed)
        wav = m.generate(text, audio_prompt_path=f"voice/refs/{who}.wav", exaggeration=ex_k, cfg_weight=cfg)
        ta.save(out, wav, m.sr)
        log[f"{take}_{k}"] = {"who": who, "text": text, "exaggeration": ex_k, "cfg_weight": cfg, "seed": seed, "seconds": round(wav.shape[-1] / m.sr, 2)}
        print(take, k, log[f"{take}_{k}"]["seconds"], "s", flush=True)
json.dump(log, open("voice/takes/takes.json", "w"), indent=1)
