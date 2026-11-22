"""AI.NXTLVL "6 free GitHub projects you can turn into businesses" (9:16): voiceover. Chatterbox (Resemble AI, MIT) with a synthetic
Kokoro-82M am_puck reference (nobody real is cloned), the same voice set-up as the AI.NXTLVL reels. Lines spelled as said ("Mu Mu A I Novel", "Red Note"). Three takes per line; build/vo_pick.py picks and joins them.
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
    ("f00", "These six free GitHub projects could each be a business.", 0.65),
    ("f01", "One. AutoClip cuts long videos into short clips. Sell clipping to podcasters and streamers.", 0.6),
    ("f02", "Two. Remotion makes videos with code. Run a video factory for agencies.", 0.6),
    ("f03", "Three. OpenHands is an AI agent that writes code. Build small apps for local businesses.", 0.6),
    ("f04", "Four. PersonaLive turns one photo into a live AI avatar. Launch a virtual influencer.", 0.6),
    ("f05", "Five. RedInk writes a full Red Note post, text and images, from one prompt. Sell it to brands.", 0.6),
    ("f06", "Six. Moo Moo A I Novel plans and drafts novels with AI. Start a publishing studio.", 0.6),
    ("f07", "The code is free. The money is in packaging it for one customer.", 0.65),
    ("f08", "Comment repos, and I'll send you all six links.", 0.65),
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
