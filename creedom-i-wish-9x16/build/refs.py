"""Voice reference for the creator in the Creedom "I Wish..." reel, made with Kokoro-82M (Apache-2.0): a new blend of two
stock voices (am_michael 55% + bm_fable 45%), so it matches no earlier reel. Chatterbox (MIT) then performs each line.
~/.venvs/tts/bin/python build/refs.py"""
import os
import soundfile as sf
from kokoro_onnx import Kokoro
C = os.path.expanduser("~/.cache/hyperframes/tts")
k = Kokoro(os.path.join(C, "models", "kokoro-v1.0.onnx"), os.path.join(C, "voices", "voices-v1.0.bin"))
style = .55 * k.get_voice_style("am_michael") + .45 * k.get_voice_style("bm_fable")
line = "Okay, okay, hear me out. I filmed it four times, I fixed the lighting, I wrote a whole script... and honestly? I thought this one was it."
a, sr = k.create(line, voice=style, speed=1.02, lang="en-us")
os.makedirs("voice/refs", exist_ok=True)
sf.write("voice/refs/creator.wav", a, sr)
print("creator blend", round(len(a) / sr, 2), "s")
