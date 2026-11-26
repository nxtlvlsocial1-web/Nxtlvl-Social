"""Klap reel v4 voice: Kokoro-82M (hexgrad, Apache 2.0, local), one voice and one setting for the whole script, so the
read flows and never switches style between lines (owner on v3: "voiceover still looks off ... better flow ... switching
styles"). Writes one take per passage to assets/audio/vo_takes/<voice>/gX_t0.wav; build/vo_pick.py trims, joins, times
the words and masters it (VO_TAKES=assets/audio/vo_takes/<voice> VO_TAG=<voice>).
HF_HOME=/root/tts/hf HF_HUB_OFFLINE=1 /root/tts/.venv/bin/python build/vo_kok.py <voice> [speed]
"""
import json
import os
import re
import sys

import numpy as np
import soundfile as sf
from kokoro import KPipeline

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE = sys.argv[1] if len(sys.argv) > 1 else "am_puck"
SPEED = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
OUT = os.path.join(ROOT, "assets", "audio", "vo_takes", VOICE)
SAY = {"MrBeast": "Mister Beast", "IShowSpeed": "I Show Speed", "GTA 6": "G T A six", "Klap": "Klap"}


def main():
    os.makedirs(OUT, exist_ok=True)
    kp = KPipeline(lang_code="a")
    for ln in json.load(open(os.path.join(ROOT, "plan", "script.json"))):
        text = ln["text"]
        for a, b in SAY.items():
            text = text.replace(a, b)
        text = text.replace("...", ",")          # Kokoro reads an ellipsis as a long stop; a comma keeps the flow
        a = np.concatenate([np.asarray(x[2]) for x in kp(text, voice=VOICE, speed=SPEED)])
        sf.write(os.path.join(OUT, f"{ln['id']}_t0.wav"), a, 24000)
        print(VOICE, ln["id"], round(len(a) / 24000, 2), flush=True)
    print("done", VOICE, flush=True)


if __name__ == "__main__":
    main()
