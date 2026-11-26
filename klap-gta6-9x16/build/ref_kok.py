"""Klap reel v2: reference voices for Chatterbox, made with Kokoro-82M (Apache 2.0): synthetic US male voices, nobody real
is cloned. An energetic reference text, because the reference's own energy sets the clone's.
HF_HOME=/root/tts/hf HF_HUB_OFFLINE=1 /root/tts/.venv/bin/python build/ref_kok.py
"""
import os

import numpy as np
import soundfile as sf
from kokoro import KPipeline

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT = ("Okay, this is actually insane. I did not expect that to work, but it did! Look at the numbers: three hundred thousand "
        "views, overnight. So here's the plan. You grab the clip, you cut it vertical, and you post it before anyone else even "
        "wakes up. That's it. That's the whole trick.")
kp = KPipeline(lang_code="a")
for v in ("am_michael", "am_fenrir"):
    a = np.concatenate([np.asarray(x[2]) for x in kp(TEXT, voice=v, speed=1.05)])
    p = os.path.join(ROOT, "assets", "audio", f"ref_{v}.wav")
    sf.write(p, a, 24000)
    print(p, round(len(a) / 24000, 1), "s")
