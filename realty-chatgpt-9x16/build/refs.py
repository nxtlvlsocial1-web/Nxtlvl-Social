"""Voice references for the real estate what-if, made with Kokoro-82M (Apache-2.0): Marcus (the agent, warm and a bit
dramatic) and Lena (his junior agent, quick and sharp). Chatterbox (MIT) then performs each line. ~/.venvs/tts/bin/python build/refs.py"""
import os
import soundfile as sf
from kokoro_onnx import Kokoro
C = os.path.expanduser("~/.cache/hyperframes/tts")
k = Kokoro(os.path.join(C, "models", "kokoro-v1.0.onnx"), os.path.join(C, "voices", "voices-v1.0.bin"))
REF = {
    "marcus": ("am_liam", 1.0, "Twenty years I've been selling homes in this town. Best listings on the block, ask anybody. Come on in, sit down, let's find you a place, my friend."),
    "lena": ("af_sky", 1.06, "Okay, okay, listen to me for one second. I fixed it. I literally fixed it in like two minutes, and you're going to thank me later."),
}
for who, (voice, speed, line) in REF.items():
    a, sr = k.create(line, voice=voice, speed=speed, lang="en-us")
    sf.write(f"voice/refs/{who}.wav", a, sr)
    print(who, voice, round(len(a) / sr, 2), "s")
