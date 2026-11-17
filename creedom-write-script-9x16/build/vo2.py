"""v2 voice (owner: "change the voiceover style, make it more expressive"): Chatterbox (Resemble AI, MIT) on CPU, its
emotion-exaggeration set per line by the arc beat, three takes per line. Timbre from a 10 s reference made with
Kokoro-82M voice af_bella (Apache 2.0; synthetic, nobody real is cloned), so it is not the af_heart voice of the CHECK
and v1 reels. build/vo_pick.py (VO_TAKES=assets/audio/v2/takes) picks the takes and writes plan/words.json.
HF_HOME=/root/tts/hf HF_HUB_OFFLINE=1 /root/tts/.venv/bin/python build/vo2.py
"""
import json
import os

import numpy as np
import soundfile as sf
import torch
import torchaudio as ta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "assets", "audio", "v2", "ref_af_bella.wav")
OUT = os.path.join(ROOT, "assets", "audio", "v2", "takes")
LINES = [
    ("m00", "I tried on forty AI scripts last week. Not one of them fit.", "hook 70", .85),
    ("m01", "They're all off the rack. Same hook. Same \"let's dive in.\" For every creator on earth.", "peak 90", 1.0),
    ("m02", "Because none of them have ever heard you talk.", "release", .6),
    ("m03", "So I opened Creedom, and typed: at write script.", "turn", .75),
    ("m04", "First, it takes your measurements. How you open. Where you pause. The words you can't stop saying.", "peak", .9),
    ("m05", "Then it cuts a script to fit you. Hook, story, call to action, stitched in your voice.", "peak (twist)", .9),
    ("m06", "It sounds like me... on a really good day.", "release (smile)", 1.0),
    ("m07", "Comment Script, and I'll send you the link.", "CTA", .75),
]


def make_ref():
    from kokoro import KPipeline
    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    text = ("Okay, so here's the thing nobody tells you about posting every day. It's not the editing. "
            "It's the blank page. And honestly? I used to stare at it for an hour.")
    a = np.concatenate([np.asarray(x, dtype=np.float32) for _, _, x in pipe(text, voice="af_bella", speed=1.05)])
    sf.write(REF, a, 24000)


def main():
    os.makedirs(OUT, exist_ok=True)
    if not os.path.exists(REF):
        make_ref()
    from chatterbox.tts import ChatterboxTTS
    m = ChatterboxTTS.from_pretrained(device="cpu")
    for lid, text, beat, ex in LINES:
        for take, (seed, dex, cfg, temp) in enumerate(((7, 0, .4, .8), (23, .15, .32, .85), (61, .25, .3, .9))):
            p = os.path.join(OUT, f"{lid}_t{take}.wav")
            if os.path.exists(p):
                continue
            torch.manual_seed(seed)
            w = m.generate(text.replace("Creedom", "Cree-dum"), audio_prompt_path=REF, exaggeration=min(1.25, ex + dex), cfg_weight=cfg, temperature=temp)
            ta.save(p, w, m.sr)
            print(lid, take, round(w.shape[-1] / m.sr, 2), flush=True)
    json.dump([{"id": i, "text": t, "beat": b, "exaggeration": e} for i, t, b, e in LINES],
              open(os.path.join(ROOT, "plan", "script.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
