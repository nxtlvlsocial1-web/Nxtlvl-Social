"""Voices for the Creators 100X "30 days in 1 prompt" reel, open-source models only. Two new Kokoro-82M (Apache-2.0)
blends, used on no earlier reel: Jules (the creator) = af_jessica 60% + af_nova 40%, Volt (the AI sidekick) = bm_daniel
50% + am_echo 50%. Each reads a reference line in character; Chatterbox (MIT) then performs every line from that
reference, three takes per line (exaggeration and seed varied). build/voice.py picks and lays them out.
~/.venvs/tts/bin/python build/voices.py"""
import json
import os

import soundfile as sf
import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
from kokoro_onnx import Kokoro

C = os.path.expanduser("~/.cache/hyperframes/tts")
REFS = {
    "jules": ("voice/refs/jules.wav", {"af_jessica": .6, "af_nova": .4}, "Okay, I'm being honest with you. I sat down to film three times this week, and every single time, my mind went completely blank."),
    "volt": ("voice/refs/volt.wav", {"bm_daniel": .5, "am_echo": .5}, "Good news! This is exactly what I'm built for. Give me one minute, and I'll have your whole month sorted."),
}
k = None
for who, (path, mix, line) in REFS.items():
    if os.path.exists(path):
        continue
    k = k or Kokoro(os.path.join(C, "models", "kokoro-v1.0.onnx"), os.path.join(C, "voices", "voices-v1.0.bin"))
    style = sum(w * k.get_voice_style(v) for v, w in mix.items())
    a, sr = k.create(line, voice=style, speed=1.04, lang="en-us" if who == "jules" else "en-gb")
    sf.write(path, a, sr)

LINES = [  # take, speaker, text (for the ear), exaggeration, cfg weight
    ("01", "jules", "Two weeks without posting. Every morning I open my phone... and I've got nothing.", .75, .4),
    ("02", "volt", "What if one prompt planned your next thirty days?", .7, .45),
    ("03", "jules", "Thirty?! I can't even plan lunch.", .9, .45),
    ("04", "volt", "Step one. Tell me your niche, who it's for, and your goal.", .6, .5),
    ("05", "jules", "Home workouts. Busy moms. More clients.", .6, .5),
    ("06", "volt", "Step two. I split it into three pillars: teach, story, proof.", .6, .5),
    ("07", "jules", "Pillars? Like... a temple?", .85, .45),
    ("08", "volt", "Like a menu. You never run out of dishes.", .65, .5),
    ("09", "volt", "Step three. Thirty days, each with a hook and a format.", .65, .5),
    ("10", "jules", "Day nine: the four-minute workout while the kettle boils? I'd watch that!", .9, .45),
    ("11", "volt", "One rule: film the whole week in one afternoon.", .65, .5),
    ("12", "jules", "So I'm busy for one afternoon...", .7, .45),
    ("13", "volt", "...and posting all week.", .75, .5),
    ("14", "jules", "Send this to a friend who never knows what to post.", .7, .5),
    ("15", "volt", "Comment Plan, and I'll send you the prompt.", .65, .5),
]
m = ChatterboxTTS.from_pretrained(device="cpu")
logp = "voice/takes/takes.json"
log = json.load(open(logp)) if os.path.exists(logp) else {}
for take, who, text, ex, cfg in LINES:
    for kk, (exk, seed) in enumerate(((ex, 7), (ex + .15, 21), (max(.4, ex - .1), 53))):
        out = f"voice/takes/{take}_{kk}.wav"
        if os.path.exists(out):
            continue
        torch.manual_seed(seed)
        w = m.generate(text, audio_prompt_path=REFS[who][0], exaggeration=exk, cfg_weight=cfg)
        ta.save(out, w, m.sr)
        log[f"{take}_{kk}"] = {"speaker": who, "text": text, "exaggeration": exk, "cfg_weight": cfg, "seconds": round(w.shape[-1] / m.sr, 2)}
        json.dump(log, open(logp, "w"), indent=1)
        print(take, kk, log[f"{take}_{kk}"]["seconds"], flush=True)
