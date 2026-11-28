"""NXTLVLSOCIAL.AI Claude plugins reel (9:16): voiceover (Chatterbox, Resemble AI, MIT,
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
        for take, seed in enumerate((11, 29, 47, 83)):
            p = os.path.join(OUT, f"{ln['id']}_t{take}.wav")
            if os.path.exists(p):
                continue
            torch.manual_seed(seed)
            # v5 (owner: "he feels like he is just reading the script"): performed, not read. The "say" text carries the
            # phrasing (pauses before the hits); higher exaggeration and a lower cfg weight give a slower, more acted delivery
            wav = m.generate(ln.get("say", ln["text"]), exaggeration=ln["ex"], cfg_weight=ln.get("cfg", .5), temperature=.8)
            ta.save(p, wav, m.sr)
            print(ln["id"], take, round(wav.shape[-1] / m.sr, 2), flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()
