"""GTA 6 x Claude reel: voiceover (owner: "make and find the relevant voiceover which has an expressive nature").
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
REF = os.path.join(ROOT, "assets", "audio", "ref_am_michael.wav")
OUT = os.path.join(ROOT, "assets", "audio", "vo_takes")
# (id, text, beat, exaggeration)
LINES = [
    ("g00", "GTA six drops next week. I couldn't wait...", "hook 70", .8),
    ("g01", "so I made Claude build me my own.", "peak", .95),
    ("g02", "This is a free GitHub repo called Claude Code Game Studios.", "release", .6),
    ("g03", "You describe a game. Claude asks a few questions, writes the plan, and builds it.", "release", .65),
    ("g04", "I typed one prompt: a neon open-world city I can drive around.", "release", .7),
    ("g05", "This is what it made.", "peak", .9),
    ("g06", "Drifts. Combos. A rooftop ramp.", "peak", 1.0),
    ("g07", "It's not GTA. But I didn't write a single line of code...", "peak", .8),
    ("g09", "Step one: paste the repo into Claude Code. Step two: describe your game. Step three: play it.", "release", .7),
    ("g10", "Comment GAME, and I'll send you the link.", "CTA", .8),
    ("g11", "And send this to the friend who's taking November nineteenth off.", "CTA", .85),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    m = ChatterboxTTS.from_pretrained(device="cpu")
    m.prepare_conditionals(REF, exaggeration=.6)
    for lid, text, beat, ex in LINES:
        for take, seed in enumerate((11, 29)):
            if os.path.exists(os.path.join(OUT, f"{lid}_t{take}.wav")):
                continue                      # keep the takes already made
            torch.manual_seed(seed)
            w = m.generate(text, audio_prompt_path=REF, exaggeration=ex, cfg_weight=.35, temperature=.8)
            ta.save(os.path.join(OUT, f"{lid}_t{take}.wav"), w, m.sr)
            print(lid, take, round(w.shape[-1] / m.sr, 2), flush=True)
    json.dump([{"id": i, "text": t, "beat": b, "exaggeration": e} for i, t, b, e in LINES],
              open(os.path.join(ROOT, "plan", "script.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
