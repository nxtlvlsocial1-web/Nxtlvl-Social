"""The ChatGPT business skit's dialogue (Marcus, a real estate agent; Byte, his AI sidekick), voiced with open-source models
only: Kokoro-82M (Apache-2.0) voice references and Chatterbox (MIT) performing every line with its own emotion setting.
Two takes per line; build/pick.py keeps the take whose words match best. Chatterbox output carries Resemble's inaudible
Perth watermark. ~/.venvs/tts/bin/python build/voices.py"""
import json
import os
import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

LINES = [
    ("01", "marcus", "Byte! Clients keep saying ChatGPT recommended Prime Nest. Not us!", .85, .45),
    ("02", "byte", "Because Prime Nest claimed their business. You didn't.", .6, .5),
    ("03", "marcus", "Wait. We can do that?", .8, .45),
    ("04", "byte", "It's free. Since November tenth. Watch.", .6, .5),
    ("05", "byte", "Step one. Log in, and open chat G P T dot com, slash business hub.", .55, .5),
    ("06", "marcus", "Do I need a paid plan?", .75, .45),
    ("07", "byte", "Nope. No ads account either.", .6, .5),
    ("08", "byte", "Step two. Search your agency. Tap Get Started.", .55, .5),
    ("09", "marcus", "What if we're not listed?", .75, .45),
    ("10", "byte", "Type it in yourself.", .6, .5),
    ("11", "byte", "Step three. Prove it's yours. Business phone, email, website, or Shopify.", .55, .5),
    ("12", "marcus", "Can I use my personal email?", .75, .45),
    ("13", "byte", "Use the one that matches your website.", .6, .5),
    ("14", "byte", "Step four. A quick I D check, and you get the blue check.", .6, .5),
    ("15", "marcus", "I look terrible in I D photos.", .85, .45),
    ("16", "byte", "It's a check. Not a headshot.", .7, .45),
    ("17", "marcus", "So now we're number one?", .8, .45),
    ("18", "byte", "It doesn't buy a ranking. It gives ChatGPT your real details.", .6, .5),
    ("19", "marcus", "Byte, you just saved me a fortune.", .85, .45),
    ("20", "byte", "I'll send you my invoice.", .7, .45),
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
