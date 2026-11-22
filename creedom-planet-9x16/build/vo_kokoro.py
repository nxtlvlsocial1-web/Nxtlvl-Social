"""Creedom "Planet You" voice (ElevenLabs was out of credits): Kokoro-82M (Apache 2.0) in its natural voice af_heart, the Creators 100X
house voice, via kokoro-onnx (model files in /root/tts/kokoro). Script approved by the owner on 2026-11-22 (plan/script.json).
Each line is synthesised on its own and joined with short breaths; no time-stretch.
/root/tts/.venv/bin/python build/vo_kokoro.py [speed]     -> assets/audio/vo.wav, plan/line_times.json
"""
import json, os, sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEED = float(sys.argv[1]) if len(sys.argv) > 1 else 1.15
GAP = {"p0": .75, "p1": .55, "p2": .45, "p3": .5, "p4": .4, "p5": .65}      # breath after each line (s)
k = Kokoro("/root/tts/kokoro/kokoro-v1.0.onnx", "/root/tts/kokoro/voices-v1.0.bin")
LEAD = .8                                                            # a breath of space before the first line
out, times, t = [np.zeros(int(LEAD * 24000), np.float32)], {}, LEAD
for ln in json.load(open(os.path.join(ROOT, "plan", "script.json"))):
    audio, sr = k.create(ln["text"], voice="af_heart", speed=SPEED, lang="en-us")
    a = np.asarray(audio, dtype=np.float32)
    nz = np.where(np.abs(a) > .01)[0]                                # trim the model's own lead-in / tail silence
    a = a[max(nz[0] - int(.03 * sr), 0): nz[-1] + int(.08 * sr)]
    times[ln["id"]] = (round(t, 3), round(t + len(a) / sr, 3))
    out += [a, np.zeros(int(GAP.get(ln["id"], 0) * sr), np.float32)]
    t += len(a) / sr + GAP.get(ln["id"], 0)
    print(ln["id"], round(len(a) / sr, 2), flush=True)
y = np.concatenate(out)
os.makedirs(os.path.join(ROOT, "assets", "audio"), exist_ok=True)
sf.write(os.path.join(ROOT, "assets", "audio", "vo.wav"), y, sr)
json.dump(times, open(os.path.join(ROOT, "plan", "line_times.json"), "w"), indent=1)
print(f"vo.wav {len(y) / sr:.2f} s at speed {SPEED}")
