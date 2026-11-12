"""Voiceover v3 (owner: "the voiceover feels very weird... his expressive voice feels very bad, go with a natural tone,
just a little expressive"). v2 pushed Chatterbox (cloning a synthetic reference) to high emotion and then sped it up
30 % with atempo: that chain sounded off. v3 speaks the script with Kokoro-82M (hexgrad, Apache 2.0) directly, in its own
natural US male voice am_michael, at a brisk native speed (no time-stretch afterwards), the way the reel-flop VO was
fixed. Two takes per line (two speeds); build/vo_pick.py (VO_TAKES=assets/audio/vo_takes_kokoro, TEMPO 1.0) picks.

HF_HOME=/root/tts/hf HF_HUB_OFFLINE=1 /root/tts/.venv/bin/python build/vo_kokoro.py
"""
import json
import os

import numpy as np
import soundfile as sf
from kokoro import KPipeline

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "audio", "vo_takes_kokoro")
VOICE = "am_michael"
SPEEDS = (1.25, 1.32)   # the reel has to land at 25-30 s
# the approved script, natural punctuation only (a little lift on the hook, the number and the CTA)
LINES = [
    ("p00", "GTA six drops on the nineteenth. Save this, it's the only creator video you'll need.", "hook 70"),
    ("p01", "The biggest GTA RP clip pages grew exactly like this: one police chase, one streamer losing it, clipped in minutes.", "peak"),
    ("p02", "Millions of views.", "peak"),
    ("p03", "Step one: an AI tool that turns any eight hour stream into ten ready-to-post clips.", "release"),
    ("p04", "Step two: one game setting that decides if you get paid, or get claimed.", "peak"),
    ("p05", "Then the music rule, and the keyword trick most GTA pages will miss.", "peak"),
    ("p06", "Comment GTA six, and I'll send you all of it. And follow, so you're early!", "CTA"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    json.dump([{"id": i, "text": t, "beat": b, "exaggeration": 0} for i, t, b in LINES],
              open(os.path.join(ROOT, "plan", "script.json"), "w"), indent=1)
    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    only = set(__import__('sys').argv[1:])
    for lid, text, _ in LINES:
        if only and lid not in only:
            continue
        for k, sp in enumerate(SPEEDS):
            audio = np.concatenate([np.asarray(a, dtype=np.float32) for _, _, a in pipe(text, voice=VOICE, speed=sp)])
            sf.write(os.path.join(OUT, f"{lid}_t{k}.wav"), audio, 24000)
            print(lid, k, round(len(audio) / 24000, 2), flush=True)


if __name__ == "__main__":
    main()
