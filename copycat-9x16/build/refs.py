"""Voice identity references for the Copycat reel, made with Kokoro-82M (Apache-2.0): one ~10 s clip per character,
read slowly and low for the noir narrator. Chatterbox (MIT) then speaks each line in that voice with the emotion we ask for.
~/.venvs/tts/bin/python build/refs.py"""
import os
import soundfile as sf
from kokoro_onnx import Kokoro
C = os.path.expanduser("~/.cache/hyperframes/tts")
k = Kokoro(os.path.join(C, "models", "kokoro-v1.0.onnx"), os.path.join(C, "voices", "voices-v1.0.bin"))
REF = {
    "kane": ("am_fenrir", .86, "The city never sleeps. Neither do I. Every case starts the same way: a knock on the door, a long night, and a cold cup of coffee nobody remembers pouring."),
    "june": ("af_bella", 1.0, "I bake everything myself, before the sun is up. Cinnamon rolls, sourdough, a new pastry every Friday. People line up outside, and I know most of them by name."),
}
for who, (voice, speed, line) in REF.items():
    a, sr = k.create(line, voice=voice, speed=speed, lang="en-us")
    sf.write(f"voice/refs/{who}.wav", a, sr)
    print(who, voice, round(len(a) / sr, 2), "s")
