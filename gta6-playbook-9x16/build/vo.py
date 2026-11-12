"""GTA 6 creator playbook reel (AI.NXTLVL): voiceover, same pipeline and voice as gta6-claude-9x16 (owner: "make and find the relevant voiceover which has an expressive nature").
Open-source models only, run locally on CPU: Chatterbox (Resemble AI, MIT) speaks every line with its emotion set by the
line's beat; the voice's timbre comes from a 11 s reference made with Kokoro-82M (hexgrad, Apache 2.0, voice am_michael,
a synthetic US male voice: nobody real is cloned). Script: the client's brief, word for word ("GTA 6" written "GTA six"
so it is read the way people say it). Two takes per line; build/vo_pick.py picks and joins them.
/root/tts/.venv/bin/python build/vo.py      (HF_HOME=/root/tts/hf)
"""
import json
import os

import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "assets", "audio", "ref_am_puck.wav")
OUT = os.path.join(ROOT, "assets", "audio", "vo_takes")
# (id, text, beat, exaggeration)
# v4 (owner picked the "chatterbox" sample): Chatterbox with a medium emotion setting (0.6, the sample's), its timbre
# from Kokoro's am_puck (a synthetic voice, nobody real is cloned), normal punctuation, and NO time-stretch afterwards:
# v2's weirdness came from exaggeration 1.1-1.6 plus a 30 % atempo.
LINES = [
    ("p00", "GTA six drops on the nineteenth. Save this, it's the only creator video you'll need.", "hook 70", .65),
    ("p01", "The biggest GTA RP clip pages grew exactly like this: one police chase, one streamer losing it, clipped in minutes.", "peak", .6),
    ("p02", "Millions of views.", "peak", .65),
    ("p03", "Step one: an AI tool that turns any eight hour stream into ten ready-to-post clips.", "release", .55),
    ("p04", "Step two: one game setting that decides if you get paid, or get claimed.", "peak", .6),
    ("p05", "Then the music rule, and the keyword trick most GTA pages will miss.", "peak", .6),
    ("p06", "Comment GTA six, and I'll send you all of it. And follow, so you're early!", "CTA", .65),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    m = ChatterboxTTS.from_pretrained(device="cpu")
    m.prepare_conditionals(REF, exaggeration=.6)
    for lid, text, beat, ex in LINES:
        for take, seed in enumerate((11, 29, 47)):
            if os.path.exists(os.path.join(OUT, f"{lid}_t{take}.wav")):
                continue                      # keep the takes already made
            torch.manual_seed(seed)
            w = m.generate(text, audio_prompt_path=REF, exaggeration=ex, cfg_weight=.5, temperature=.8)
            ta.save(os.path.join(OUT, f"{lid}_t{take}.wav"), w, m.sr)
            print(lid, take, round(w.shape[-1] / m.sr, 2), flush=True)
    json.dump([{"id": i, "text": t, "beat": b, "exaggeration": e} for i, t, b, e in LINES],
              open(os.path.join(ROOT, "plan", "script.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
