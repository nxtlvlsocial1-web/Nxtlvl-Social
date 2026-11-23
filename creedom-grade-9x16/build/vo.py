"""Creedom remake: graded before anyone saw it (9:16): voiceover. Chatterbox (Resemble AI, MIT) with a synthetic Kokoro-82M af_bella reference (nobody real
is cloned), the same voice set-up as the Creedom @write-script reel v2. Three takes per line; build/vo_pick.py picks.
HF_HOME=/root/tts/hf /root/tts/.venv/bin/python build/vo.py
"""
import os

import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "assets", "audio", "ref_af_bella.wav")
OUT = os.path.join(ROOT, "assets", "audio", "vo_takes")
LINES = [
    ("f00", "This reel scored two point nine out of five. Before anyone saw it.", 0.7),
    ("f01", "Harsh. But look where it lost points.", 0.7),
    ("f02", "Second one, the hook is too slow. Second seven, a claim with no proof. Second fourteen, it loses trust.", 0.6),
    ("f03", "Fix just those three seconds, and it scores four point four.", 0.7),
    ("f04", "That's Cree-dum. Upload your reel before you post, and it shows you the exact second, and the fix.", 0.6),
    ("f05", "Send this to the friend who posts and prays. Comment Check, and I'll send you the link.", 0.65),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    m = ChatterboxTTS.from_pretrained(device="cpu")
    for lid, text, ex in LINES:
        m.prepare_conditionals(REF, exaggeration=ex)
        for take, seed in enumerate((11, 29, 47)):
            p = os.path.join(OUT, f"{lid}_t{take}.wav")
            if os.path.exists(p):
                continue
            torch.manual_seed(seed)
            wav = m.generate(text, exaggeration=ex, cfg_weight=.5)
            ta.save(p, wav, m.sr)
            print(lid, take, round(wav.shape[-1] / m.sr, 2), flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()
