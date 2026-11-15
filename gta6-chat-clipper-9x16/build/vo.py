"""GTA 6 chat-clipper reel (AI.NXTLVL): voiceover in the page's voice: Chatterbox (Resemble AI, MIT) with its timbre
from a Kokoro-82M am_puck reference (a synthetic voice, nobody real is cloned), medium emotion, as the earlier GTA and
Fable reels. Lines from plan/script.json ("say" = spelled the way it is said: "Klawd", "G T A six").
Three takes per line; build/vo_pick.py picks.
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
EX = {"g00": .68, "g01": .66, "g02": .65, "g05": .64, "g06": .66, "g07": .64}   # v2: the 30 s script


def main():
    os.makedirs(OUT, exist_ok=True)
    m = ChatterboxTTS.from_pretrained(device="cpu")
    for ln in json.load(open(os.path.join(ROOT, "plan", "script.json"))):
        ex = EX.get(ln["id"], .6)
        m.prepare_conditionals(REF, exaggeration=ex)
        for take, seed in enumerate((11, 29, 47)):
            p = os.path.join(OUT, f"{ln['id']}_t{take}.wav")
            if os.path.exists(p):
                continue
            torch.manual_seed(seed)
            wav = m.generate(ln["say"], exaggeration=ex, cfg_weight=.5)
            ta.save(p, wav, m.sr)
            print(ln["id"], take, round(wav.shape[-1] / m.sr, 2), flush=True)
    print("VO DONE", flush=True)


if __name__ == "__main__":
    main()
