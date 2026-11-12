"""Re-voices lines 02-04 of the Copycat re-cut with clearer wording (three takes each); the picks are in voice/script.json."""
import torch, torchaudio as ta
from chatterbox.tts import ChatterboxTTS
m = ChatterboxTTS.from_pretrained(device="cpu")
R = {"02": "Then... we watch her. Legally. Public pages only. Zero dollars.",
     "03": "Clue number one. Change detection dot I O. Her prices change? You know in a minute.",
     "04": "Clue number two. R S S Hub, and Mini flux. Every post she makes, in one feed."}
for take, text in R.items():
    for j, (ex, cfg, seed) in enumerate(((.95, .45, 5), (1.0, .4, 13), (.9, .5, 29))):
        torch.manual_seed(seed); w = m.generate(text, audio_prompt_path="voice/refs/kane.wav", exaggeration=ex, cfg_weight=cfg)
        ta.save(f"voice/takes/{take}_r{j}.wav", w, m.sr); print(take, j, round(w.shape[-1] / m.sr, 2), flush=True)
