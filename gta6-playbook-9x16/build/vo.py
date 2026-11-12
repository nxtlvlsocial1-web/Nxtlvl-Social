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
REF = os.path.join(ROOT, "assets", "audio", "ref_am_michael.wav")
OUT = os.path.join(ROOT, "assets", "audio", "vo_takes")
# (id, text, beat, exaggeration)
# v2 (owner: "highly expressive and emotional, not like he's just reading the script"): each line carries its beat's
# emotion through punctuation (the pauses and lifts Chatterbox follows) and a much higher exaggeration; three takes each
LINES = [
    ("p00", "GTA six drops on the nineteenth! So save this... it's the only creator video you'll need.", "hook 70: urgent, hyped", 1.15),
    ("p01", "The biggest GTA RP clip pages grew exactly like this... one police chase. One streamer losing it. Clipped in minutes.",
     "peak: storytelling, building", 1.1),
    ("p02", "Millions. Of. Views.", "peak: amazed, big", 1.3),
    ("p03", "Step one: an AI tool that turns any eight-hour stream into ten ready-to-post clips!", "release: excited reveal", 1.05),
    ("p04", "Step two: one game setting that decides if you get paid... or get claimed.", "peak: serious warning, drop on claimed", 1.2),
    ("p05", "Then the music rule... and the keyword trick most GTA pages will miss.", "peak: secretive, teasing", 1.15),
    ("p06", "Comment GTA six, and I'll send you all of it. And follow, so you're early!", "CTA: warm, energetic", 1.2),
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
            w = m.generate(text, audio_prompt_path=REF, exaggeration=ex, cfg_weight=.3, temperature=.85)
            ta.save(os.path.join(OUT, f"{lid}_t{take}.wav"), w, m.sr)
            print(lid, take, round(w.shape[-1] / m.sr, 2), flush=True)
    json.dump([{"id": i, "text": t, "beat": b, "exaggeration": e} for i, t, b, e in LINES],
              open(os.path.join(ROOT, "plan", "script.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
