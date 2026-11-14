"""The Postclerk voiceover, voiced with open-source models only. A new Kokoro-82M (Apache-2.0) blend (am_eric 60% +
am_liam 40%, used on no earlier reel) reads an upbeat creator line as the voice reference; Chatterbox (MIT) then performs
each line of the owner's script, verbatim, three times (exaggeration and seed varied). build/pick.py keeps the best take.
Brand names are spelled for the ear ("Metri cool", "Post clerk"). Chatterbox output carries Resemble's inaudible Perth
watermark. ~/.venvs/tts/bin/python build/voices.py"""
import json
import os

import soundfile as sf
import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
from kokoro_onnx import Kokoro

REF = "voice/refs/host.wav"
if not os.path.exists(REF):
    C = os.path.expanduser("~/.cache/hyperframes/tts")
    k = Kokoro(os.path.join(C, "models", "kokoro-v1.0.onnx"), os.path.join(C, "voices", "voices-v1.0.bin"))
    style = .6 * k.get_voice_style("am_eric") + .4 * k.get_voice_style("am_liam")
    a, sr = k.create("Okay, this one is genuinely good. It's free, it's fast, and honestly? I switched my whole workflow over in one afternoon.", voice=style, speed=1.05, lang="en-us")
    sf.write(REF, a, sr)
LINES = [  # take, text (for the ear), exaggeration, cfg weight
    ("01", "Stop paying for Metri cool.", .75, .45),
    ("02", "This one is free, and it's open source.", .65, .5),
    ("03", "It's called Post clerk.", .7, .5),
    ("04", "Instagram, TikTok, LinkedIn, YouTube, and three more. All scheduled from one calendar.", .6, .5),
    ("05", "One composer, with a different caption for every platform.", .6, .5),
    ("06", "And a preview of your Instagram feed, before anything goes live.", .6, .5),
    ("07", "But here's what Metri cool doesn't give you.", .75, .45),
    ("08", "It connects to your AI.", .7, .5),
    ("09", "Claude Code, Cursor, or Codex draft your posts, and schedule them for you.", .6, .5),
    ("10", "I typed one sentence: plan my posts for next week. Done.", .7, .45),
    ("11", "Want your own copy? It deploys free on Cloudflare in about two minutes.", .6, .5),
    ("12", "Comment Post, and I'll send you the link.", .65, .5),
]
m = ChatterboxTTS.from_pretrained(device="cpu")
logp = "voice/takes/takes.json"
log = json.load(open(logp)) if os.path.exists(logp) else {}
for take, text, ex, cfg in LINES:
    for kk, (exk, seed) in enumerate(((ex, 7), (ex + .12, 21), (max(.4, ex - .1), 53))):
        out = f"voice/takes/{take}_{kk}.wav"
        if os.path.exists(out):
            continue
        torch.manual_seed(seed)
        w = m.generate(text, audio_prompt_path=REF, exaggeration=exk, cfg_weight=cfg)
        ta.save(out, w, m.sr)
        log[f"{take}_{kk}"] = {"text": text, "exaggeration": exk, "cfg_weight": cfg, "seconds": round(w.shape[-1] / m.sr, 2)}
        json.dump(log, open(logp, "w"), indent=1)
        print(take, kk, log[f"{take}_{kk}"]["seconds"], flush=True)
