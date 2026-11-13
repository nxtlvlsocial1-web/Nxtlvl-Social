"""Creators 100X STUDY reel: voiceover, same pipeline and voice as gta6-playbook-9x16 (owner: "make and find the relevant voiceover which has an expressive nature").
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
# Creators 100X "STUDY" reel: Chatterbox at medium emotion, timbre from Kokoro's am_puck (synthetic, nobody real is
# cloned), as on the GTA 6 playbook reel (owner: "Chatterbox"). Spoken spellings: "Class ten", "study" in lower case
# (capitals get read letter by letter).
LINES = [
    ("s00", "I made the hardest chapter in Class 10 Science into a manga. One prompt.", "hook 70", .65),
    ("s01", "Same chapter. Twelve pages you forget by tomorrow, or six panels you actually remember.", "peak", .6),
    ("s02", "Here are five prompts. Paste your chapter, pick one.", "release", .55),
    ("s03", "One: manga. Two: timeline. Three: mind map. Four: labelled diagram. Five: a one-page revision sheet.", "peak", .6),
    ("s04", "Number five is the one you want the night before the exam.", "peak", .6),
    ("s05", "Comment study, and I'll send you all five prompts, ready to copy.", "CTA", .65),
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
