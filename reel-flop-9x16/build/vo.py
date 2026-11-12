"""Voiceover (owner: "a very expressive female open source voice that has emotions in every word she speaks").

Open-source models only, run locally on CPU:
  * Chatterbox (Resemble AI, MIT) speaks every line, with its emotion-exaggeration control set per line by the arc beat
    (peaks hotter, releases calmer);
  * its built-in voice is male, so the female timbre comes from a 10 s reference clip made with Kokoro-82M (hexgrad,
    Apache 2.0, voice af_heart): a synthetic voice, nobody real is cloned.
Two takes per line (different seeds) into assets/audio/vo_takes/; build/vo_pick.py checks them and joins the chosen ones.

/root/tts/.venv/bin/python build/vo.py      (HF_HOME=/root/tts/hf)
"""
import json
import os

import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "assets", "audio", "vo_test", "ref_af_heart.wav")
OUT = os.path.join(ROOT, "assets", "audio", "vo_takes")
# (id, text, beat, exaggeration)
LINES = [
    # v3 (owner: "I just wanna create a shock value in the hook", picked this cold open)
    # v11 (owner: "change the losing line - This video already lost you in first three seconds and continue with here are
    # three mistakes killing your views"): it now calls back to the skipped reel just shown; l01/l02 are cut
    ("l00", "This video already lost you in the first three seconds.", "hook 70 + first peak (callback to the skipped reel)", 1.0),
    ("l03", "Here are three mistakes killing your views.", "release", .6),
    ("l04", "One: your hook is a greeting.", "peak", .7),
    ("l05", "Nobody stays for \"Hey guys.\"", "peak", .95),
    ("l06", "Start with the result.", "release", .6),
    ("l07", "Two: your first frame is still.", "peak", .7),
    ("l08", "If nothing moves, thumbs keep scrolling.", "peak", .85),
    ("l09", "Three: you explain before you show.", "peak", .7),
    ("l10", "Show the result first, then explain how you got it.", "release", .6),
    ("l11", "Fix these three and watch your next reel.", "release", .8),
    ("l12", "Save this so you don't forget, and comment \"HOOK\" for my list of twenty hooks that work.", "CTA", .7),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    m = ChatterboxTTS.from_pretrained(device="cpu")
    m.prepare_conditionals(REF, exaggeration=.6)
    for lid, text, beat, ex in LINES:
        for take, seed in enumerate((11, 29)):
            if os.path.exists(os.path.join(OUT, f"{lid}_t{take}.wav")):
                continue                      # keep the takes already made
            torch.manual_seed(seed)
            w = m.generate(text, audio_prompt_path=REF, exaggeration=ex, cfg_weight=.35, temperature=.8)
            ta.save(os.path.join(OUT, f"{lid}_t{take}.wav"), w, m.sr)
            print(lid, take, round(w.shape[-1] / m.sr, 2), flush=True)
    json.dump([{"id": i, "text": t, "beat": b, "exaggeration": e} for i, t, b, e in LINES],
              open(os.path.join(ROOT, "plan", "script.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
