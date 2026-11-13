"""Voice references for the ChatGPT business skit (tutorial skit format), made with Kokoro-82M (Apache-2.0): Marcus (the
real estate agent; voice/refs/marcus.wav, am_liam, kept from the earlier cut) and Byte (his AI sidekick, dry and witty).
Chatterbox (MIT) then performs each line. ~/.venvs/tts/bin/python build/refs.py"""
import os
import soundfile as sf
from kokoro_onnx import Kokoro
C = os.path.expanduser("~/.cache/hyperframes/tts")
k = Kokoro(os.path.join(C, "models", "kokoro-v1.0.onnx"), os.path.join(C, "voices", "voices-v1.0.bin"))
REF = {"byte": ("bm_george", 1.0, "Right. I've read your emails, your calendar and your search history. I have notes. Several, actually. Shall we begin, or would you like a moment?")}
for who, (voice, speed, line) in REF.items():
    a, sr = k.create(line, voice=voice, speed=speed, lang="en-us")
    sf.write(f"voice/refs/{who}.wav", a, sr)
    print(who, voice, round(len(a) / sr, 2), "s")
