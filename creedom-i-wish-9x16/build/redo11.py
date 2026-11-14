"""Re-voice line 11 so "Creedom" is heard as cree-dom, not "create them": three spellings, two seeds each.
~/.venvs/tts/bin/python build/redo11.py"""
import json, os, torch, torchaudio as ta
from chatterbox.tts import ChatterboxTTS
m = ChatterboxTTS.from_pretrained(device="cpu")
log = json.load(open("voice/takes/takes.json"))
for j, text in enumerate(["Comment Cree-dom, and I'll send you the link.", "Comment Kree dum, and I'll send you the link.", "Comment, Creedum, and I'll send you the link."]):
    for s, seed in enumerate((7, 21)):
        key = f"11b_{j}{s}"
        torch.manual_seed(seed)
        wav = m.generate(text, audio_prompt_path="voice/refs/creator.wav", exaggeration=.75, cfg_weight=.45)
        ta.save(f"voice/takes/{key}.wav", wav, m.sr)
        log[key] = {"text": text, "exaggeration": .75, "cfg_weight": .45, "seed": seed, "seconds": round(wav.shape[-1] / m.sr, 2)}
        print(key, flush=True)
json.dump(log, open("voice/takes/takes.json", "w"), indent=1)
