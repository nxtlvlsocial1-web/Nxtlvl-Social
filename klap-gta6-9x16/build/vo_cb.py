"""Klap reel v2: the voiceover, directed. Chatterbox (Resemble AI, MIT) on CPU, timbre from a synthetic Kokoro reference
(build/ref_kok.py; nobody real is cloned). The script is read in passages (plan/script.json), so the intonation flows
across sentences; each passage carries its own intensity ("ex") and pacing ("cfg": lower = slower, more deliberate).
Three takes per passage per reference voice, into assets/audio/vo_takes/<ref>/; build/vo_pick.py picks.
HF_HOME=/root/tts/hf /root/tts/.venv/bin/python build/vo_cb.py <ref>      (ref: am_michael | am_fenrir)
"""
import json
import os
import sys

import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFV = sys.argv[1] if len(sys.argv) > 1 else "am_michael"
REF = os.path.join(ROOT, "assets", "audio", f"ref_{REFV}.wav")
OUT = os.path.join(ROOT, "assets", "audio", "vo_takes", REFV)
SEEDS = (7, 23, 61)


def main():
    os.makedirs(OUT, exist_ok=True)
    lines = json.load(open(os.path.join(ROOT, "plan", "script.json")))
    m = ChatterboxTTS.from_pretrained(device="cpu")
    m.prepare_conditionals(REF, exaggeration=.6)
    for ln in lines:
        for take, seed in enumerate(SEEDS):
            p = os.path.join(OUT, f"{ln['id']}_t{take}.wav")
            if os.path.exists(p):
                continue
            torch.manual_seed(seed)
            wav = m.generate(ln["text"], audio_prompt_path=REF, exaggeration=ln["ex"], cfg_weight=ln["cfg"], temperature=.8)
            ta.save(p, wav, m.sr)
            print(REFV, ln["id"], take, round(wav.shape[-1] / m.sr, 2), flush=True)
    print("done", REFV, flush=True)


if __name__ == "__main__":
    main()
