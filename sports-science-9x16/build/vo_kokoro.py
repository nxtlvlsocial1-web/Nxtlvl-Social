"""Sports Science & Technology reel voice: Kokoro-82M (Apache 2.0), a measured male documentary read of the client's
master VO (plan/script.json, verbatim from the brief). VOICE/SPEED from argv for auditioning.
HF_HOME=/root/tts/hf HF_HUB_OFFLINE=1 /root/tts/.venv/bin/python build/vo_kokoro.py VOICE SPEED OUTDIR [ids]
"""
import json
import os
import sys

import numpy as np
import soundfile as sf
from kokoro import KPipeline

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIX = {}   # Kokoro's own reading of ectomorph / mesomorph / endomorph / physique checks out (whisper); overrides made it worse


def main():
    voice, speed, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
    only = set(sys.argv[4:])
    os.makedirs(out, exist_ok=True)
    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for ln in json.load(open(os.path.join(ROOT, "plan", "script.json"))):
        if only and ln["id"] not in only:
            continue
        text = ln["text"]
        for k, v in FIX.items():
            text = text.replace(k, v)
        audio = np.concatenate([np.asarray(a, dtype=np.float32) for _, _, a in pipe(text, voice=voice, speed=speed)])
        sf.write(os.path.join(out, f"{ln['id']}.wav"), audio, 24000)
        print(ln["id"], round(len(audio) / 24000, 2), flush=True)


if __name__ == "__main__":
    main()
