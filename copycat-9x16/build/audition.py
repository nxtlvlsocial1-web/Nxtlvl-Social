"""Kane voice audition for the Copycat re-cut: three open-source voices (Kokoro reference + Chatterbox), two takes each,
more expressive (exaggeration .8 to .95, normal pace, no reverb). Run from copycat-9x16: ~/.venvs/tts/bin/python build/audition.py
The best take of each is exported as voice/audition/kane_voice_*.mp3."""
import os, torch, torchaudio as ta, soundfile as sf, json
from kokoro_onnx import Kokoro
from chatterbox.tts import ChatterboxTTS
C = os.path.expanduser("~/.cache/hyperframes/tts")
k = Kokoro(os.path.join(C, "models", "kokoro-v1.0.onnx"), os.path.join(C, "voices", "voices-v1.0.bin"))
REF = {
 "A_gravel": ("am_onyx", .95, "Listen, kid. This town's got two kinds of people: the ones who make the croissants, and the ones who steal the recipe. I've seen both. Neither one tips."),
 "B_fasttalker": ("am_adam", 1.12, "Okay okay okay, here's the deal, see? You got a problem, I got a laptop, and between the two of us we're gonna crack this thing wide open before breakfast!"),
 "C_cheeky": ("am_echo", 1.02, "Oh, she copied your croissant? Your font? Your cat? Well. That's adorable. Pull up a chair, have a coffee, and let me show you a little trick."),
}
LINE = "Then we watch her. Legally. Her prices change? You know in a minute. Kid... this is gonna be fun."
m = ChatterboxTTS.from_pretrained(device="cpu")
for name, (voice, speed, text) in REF.items():
    a, sr = k.create(text, voice=voice, speed=speed, lang="en-us")
    ref = f"voice/audition/ref_{name}.wav"; sf.write(ref, a, sr)
    for j, (ex, cfg, seed) in enumerate(((.8, .5, 3), (.95, .45, 11))):
        torch.manual_seed(seed)
        w = m.generate(LINE, audio_prompt_path=ref, exaggeration=ex, cfg_weight=cfg)
        ta.save(f"voice/audition/{name}_{j}.wav", w, m.sr); print(name, j, round(w.shape[-1] / m.sr, 2), flush=True)
