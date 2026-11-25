"""samarpit.ai "System Build: lead auto-reply" (9:16): voiceover. Same voice as the series (Chatterbox, Resemble AI, MIT,
with a synthetic Kokoro-82M am_puck reference: nobody real is cloned). Lines come from plan/script.json. Three takes per
line; build/vo_pick.py picks and joins them.
HF_HOME=/root/tts/hf /root/tts/.venv/bin/python build/vo.py
"""
import json
import os

import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "assets", "audio", "ref_am_puck.wav")
OUT = os.path.join(ROOT, "assets", "audio", "vo_takes")


def main():
    os.makedirs(OUT, exist_ok=True)
    lines = json.load(open(os.path.join(ROOT, "plan", "script.json")))
    m = ChatterboxTTS.from_pretrained(device="cpu")
    for ln in lines:
        m.prepare_conditionals(REF, exaggeration=ln["ex"])
        for take, seed in enumerate((11, 29, 47)):
            p = os.path.join(OUT, f"{ln['id']}_t{take}.wav")
            if os.path.exists(p):
                continue
            torch.manual_seed(seed)
            wav = m.generate(ln["text"], exaggeration=ln["ex"], cfg_weight=.5)
            ta.save(p, wav, m.sr)
            print(ln["id"], take, round(wav.shape[-1] / m.sr, 2), flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()
