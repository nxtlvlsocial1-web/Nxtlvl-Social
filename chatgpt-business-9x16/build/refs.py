"""Narrator reference for the ChatGPT business-profile reel, made with Kokoro-82M (Apache-2.0): an upbeat, clear ~10 s
clip. Chatterbox (MIT) then speaks each line in that voice. ~/.venvs/tts/bin/python build/refs.py"""
import os
import soundfile as sf
from kokoro_onnx import Kokoro
C = os.path.expanduser("~/.cache/hyperframes/tts")
k = Kokoro(os.path.join(C, "models", "kokoro-v1.0.onnx"), os.path.join(C, "voices", "voices-v1.0.bin"))
REF = {"nar": ("af_nova", 1.05, "Okay, quick one, because this is big. If you run a business, you need to see this today. It takes five minutes, it's free, and most people have no idea it exists yet.")}
for who, (voice, speed, line) in REF.items():
    a, sr = k.create(line, voice=voice, speed=speed, lang="en-us")
    sf.write(f"voice/refs/{who}.wav", a, sr)
    print(who, voice, round(len(a) / sr, 2), "s")
