"""samarpit.ai "Framework in 30: Funnel vs flywheel" (9:16): voiceover. Chatterbox (Resemble AI, MIT) with a synthetic
Kokoro-82M am_puck reference (nobody real is cloned), the same voice set-up as the AI.NXTLVL reels. Lines are the owner's
script word for word ("day 3" spoken as "day three"). Three takes per line; build/vo_pick.py picks and joins them.
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
    ("f00", "Why do customers buy once, and vanish?", .7),
    ("f01", "Because you built a funnel. Ads. Visit. Buy. Then... nothing.", .65),
    ("f02", "A flywheel puts them back in. Attract. Sell. Delight. Refer.", .65),
    ("f03", "One. Message every buyer on day three.", .6),
    ("f04", "Two. Ask the happy ones for a review.", .6),
    ("f05", "Three. Give them a reason to bring a friend.", .62),
    ("f06", "Stop refilling the funnel. Spin the wheel.", .7),
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
