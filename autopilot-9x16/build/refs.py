"""Voice identity references for the Autopilot reel, made with Kokoro-82M (Apache-2.0): one ~10 s neutral clip per
character. Chatterbox (MIT) then speaks each line in that voice with the emotion we ask for.
~/.venvs/tts/bin/python build/refs.py"""
import os
import soundfile as sf
from kokoro_onnx import Kokoro
C = os.path.expanduser("~/.cache/hyperframes/tts")
k = Kokoro(os.path.join(C, "models", "kokoro-v1.0.onnx"), os.path.join(C, "voices", "voices-v1.0.bin"))
REF = {
    "rosa": ("af_jessica", "I open the café at six every morning. The first coffee is always mine, and the regulars know their orders by heart. It is a small place, but it is mine."),
    "theo": ("am_eric", "I build little tools for people who are too busy to build them. Most problems are simpler than they look. You just have to connect the right pieces."),
}
for who, (voice, line) in REF.items():
    a, sr = k.create(line, voice=voice, speed=1.0, lang="en-us")
    sf.write(f"voice/refs/{who}.wav", a, sr)
    print(who, voice, round(len(a) / sr, 2), "s")
