"""Creedom CHECK reel voice: Kokoro-82M (Apache 2.0) speaking in its own natural voice
af_heart, the voice the owner approved for the Creators 100X hook reel (reel-flop-9x16 v13), at a brisk native speed,
no time-stretch. Two takes per line (two speeds); build/vo_pick.py (VO_TAKES=assets/audio/vo_takes_kokoro) picks.
HF_HOME=/root/tts/hf HF_HUB_OFFLINE=1 /root/tts/.venv/bin/python build/vo_kokoro.py
"""
import json
import os

import numpy as np
import soundfile as sf
from kokoro import KPipeline

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "audio", "vo_takes_kokoro")
VOICE = "af_heart"
SPEEDS = (1.28, 1.34)    # v6 (owner: faster pace): about 1.12x the v5 takes (1.18)


def main():
    os.makedirs(OUT, exist_ok=True)
    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for ln in json.load(open(os.path.join(ROOT, "plan", "script.json"))):
        for k, sp in enumerate(SPEEDS):
            text = ln["text"].replace("Creedom", "[Creedom](/kɹˈidəm/)")   # say CREE-dum
            audio = np.concatenate([np.asarray(a, dtype=np.float32) for _, _, a in pipe(text, voice=VOICE, speed=sp)])
            sf.write(os.path.join(OUT, f"{ln['id']}_t{k}.wav"), audio, 24000)
            print(ln["id"], k, round(len(audio) / 24000, 2), flush=True)


if __name__ == "__main__":
    main()
