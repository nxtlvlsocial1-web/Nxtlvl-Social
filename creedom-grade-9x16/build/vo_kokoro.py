"""Creedom remakes v2 voiceover (owner picked voice D): Kokoro-82M af_heart (Apache 2.0) read directly, no cloning and
no time-stretch. Three takes per line at slightly different speeds; build/vo_pick.py (VO_TAKES=assets/audio/vo_takes_d)
picks the cleanest. Shared by creedom-postmortem-9x16 and creedom-grade-9x16:
HF_HOME=/root/tts/hf /root/tts/.venv/bin/python build/vo_kokoro.py <project dir>
"""
import json
import os
import re
import sys

import numpy as np
import soundfile as sf
from kokoro import KPipeline

ROOT = os.path.abspath(sys.argv[1])
OUT = os.path.join(ROOT, "assets", "audio", "vo_takes_d")
SAY = {"Creedom": "[Creedom](/kɹˈidəm/)", "Cree,": "[Cree](/kɹˈi/),"}     # how the names are said
SPEEDS = (1.1, 1.15, 1.2)


def main():
    os.makedirs(OUT, exist_ok=True)
    kp = KPipeline(lang_code="a")
    for ln in json.load(open(os.path.join(ROOT, "plan", "script.json"))):
        text = ln["text"]
        for a, b in SAY.items():
            text = re.sub(rf"\b{re.escape(a)}", b, text)
        for k, sp in enumerate(SPEEDS):
            a = np.concatenate([np.asarray(x[2]) for x in kp(text, voice="af_heart", speed=sp)])
            sf.write(os.path.join(OUT, f"{ln['id']}_t{k}.wav"), a, 24000)
            print(ln["id"], k, round(len(a) / 24000, 2), flush=True)


if __name__ == "__main__":
    main()
