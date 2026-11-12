"""Voiceover v13 (owner: "the voiceover feels weird, fix that, make it natural; use VoiceStudio if needed").

v4-v12 spoke every line with Chatterbox cloning a synthetic reference, pushed to high emotion, then sped up 15 % with
atempo: that chain is what sounded off. v13 speaks the script with Kokoro-82M (hexgrad, Apache 2.0) directly, in its
own natural voice af_heart, at a slightly brisk native speed (no time-stretch afterwards). Kokoro is one of the TTS
engines the VoiceStudio app bundles; the app itself is a desktop GUI, so the engine is run here on its own.
Two takes per line (two speaking speeds); build/vo_pick.py (VO_TAKES=assets/audio/vo_takes_kokoro) picks and joins.

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
SPEEDS = (1.06, 1.14)
# what Kokoro is given to say, where the on-screen spelling would read badly aloud (the script keeps its spelling)
SAY = {"l12": 'Save this so you don\'t forget, and comment "hook" for my list of twenty hooks that work.'}


def main():
    os.makedirs(OUT, exist_ok=True)
    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for ln in json.load(open(os.path.join(ROOT, "plan", "script.json"))):
        text = SAY.get(ln["id"], ln["text"])
        for k, sp in enumerate(SPEEDS):
            audio = np.concatenate([np.asarray(a, dtype=np.float32) for _, _, a in pipe(text, voice=VOICE, speed=sp)])
            sf.write(os.path.join(OUT, f"{ln['id']}_t{k}.wav"), audio, 24000)
            print(ln["id"], k, round(len(audio) / 24000, 2), flush=True)


if __name__ == "__main__":
    main()
