"""Sports Science Technology reel, v2 voice (owner: "a different voiceover who is a little more expressive"):
Chatterbox (Resemble AI, MIT) with its timbre from a Kokoro-82M am_puck reference (a synthetic voice, nobody real is
cloned; the owner-approved expressive male voice of the GTA reels), at medium-high emotion. The brief's master script,
verbatim (plan/script.json). Two takes per line; build/vo_pick.py picks.
HF_HOME=/root/tts/hf /root/tts/.venv/bin/python build/vo_chatterbox.py
"""
import json
import os

import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "assets", "audio", "ref_am_puck.wav")
OUT = os.path.join(ROOT, "assets", "audio", "vo_takes")
EX = {"s01": .7, "s03": .65, "s05": .65, "s10": .7, "s11": .6}      # the rest .6


def main():
    os.makedirs(OUT, exist_ok=True)
    m = ChatterboxTTS.from_pretrained(device="cpu")
    for ln in json.load(open(os.path.join(ROOT, "plan", "script.json"))):
        ex = EX.get(ln["id"], .6)
        m.prepare_conditionals(REF, exaggeration=ex)
        for take, seed in enumerate((11, 29)):
            p = os.path.join(OUT, f"{ln['id']}_t{take}.wav")
            if os.path.exists(p):
                continue
            torch.manual_seed(seed)
            wav = m.generate(ln["text"], exaggeration=ex, cfg_weight=.5)
            ta.save(p, wav, m.sr)
            print(ln["id"], take, round(wav.shape[-1] / m.sr, 2), flush=True)
    print("VO DONE", flush=True)


if __name__ == "__main__":
    main()
