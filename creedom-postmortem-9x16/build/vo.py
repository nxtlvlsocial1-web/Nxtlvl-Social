"""Creedom remake: the 304-view post-mortem (9:16): voiceover. Chatterbox (Resemble AI, MIT) with a synthetic Kokoro-82M af_bella reference (nobody real
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
    ("f00", "This reel got three hundred and four views.", 0.7),
    ("f01", "And it was a reel about why people stop watching.", 0.7),
    ("f02", "On average, people gave it five seconds.", 0.6),
    ("f03", "That's how long my first sentence took. This AI told me...", 0.65),
    ("f04", "Nobody cares about the tool. They care about their reel. Problem first, tool last.", 0.6),
    ("f05", "Like this video. Sixteen seconds in, and I still haven't named the app.", 0.65),
    ("f06", "It's Cree-dum. It shows you the exact second people leave, and why.", 0.6),
    ("f07", "Send this to the friend whose reels keep flopping. Comment Cree, and I'll send you the app.", 0.65),
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
