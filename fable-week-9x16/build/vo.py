"""Fable 5.2 week reel (AI.NXTLVL): voiceover, same voice as the GTA reels (owner approved): Chatterbox (Resemble AI,
MIT) at medium emotion, its timbre from a Kokoro-82M am_puck reference (a synthetic voice, nobody real is cloned).
Lines are the approved script, spelled the way they are said ("Fable five point two", "three D", "twenty twenty-seven").
Three takes per line; build/vo_pick.py picks and joins them.
HF_HOME=/root/tts/hf /root/tts/.venv/bin/python build/vo.py
"""
import os

import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "assets", "audio", "ref_am_puck.wav")
OUT = os.path.join(ROOT, "assets", "audio", "vo_takes")
LINES = [
    ("f00", "Claude Pro users: Fable five point two costs nothing extra until Monday night. Then it eats paid credits.", .65),
    ("f01", "So don't burn the week on emails. Build these three.", .6),
    ("f02", "One: your three D twin. Answer five questions, and Fable codes a three D animal that's built like you.", .6),
    ("f03", "Two: your twenty twenty-seven. It asks the questions nobody asks you, then turns the answers into a plan, month by month.", .6),
    ("f04", "Three, the one that lasts: have Fable write its own playbook as a Skill, so cheaper models keep working like it after Monday.", .62),
    ("f05", "Comment Fable, and I'll send you all three prompts.", .65),
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


if __name__ == "__main__":
    main()
