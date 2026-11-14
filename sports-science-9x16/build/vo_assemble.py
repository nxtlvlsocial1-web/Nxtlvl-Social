"""Trim each VO line, lay them out with scene-aware gaps, and time every script word (faster-whisper word stamps
mapped onto the approved script words, so captions spell exactly what the brief says).
HF_HOME=/root/tts/hf HF_HUB_OFFLINE=1 /root/tts/.venv/bin/python build/vo_assemble.py
-> assets/audio/vo.wav, plan/words.json, plan/lines.json
"""
import json
import os
import re

import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 24000
LEAD = .2
GAP = {"s01": .3, "s02": .2, "s03": .3, "s04": .2, "s05": .3, "s06": .2, "s07": .3, "s08": .2, "s09": .3,
       "s10": .35, "s11": 0}


def norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())


def main():
    script = json.load(open(os.path.join(ROOT, "plan", "script.json")))
    wm = WhisperModel("Systran/faster-whisper-small.en", device="cpu", compute_type="int8")
    out, words, lines, t = [np.zeros(int(LEAD * SR), np.float32)], [], [], LEAD
    for ln in script:
        a, _ = sf.read(os.path.join(ROOT, "assets", "audio", "vo", ln["id"] + ".wav"), dtype="float32")
        e = np.abs(a) > .008
        i, j = max(0, np.argmax(e) - int(.03 * SR)), min(len(a), len(a) - np.argmax(e[::-1]) + int(.14 * SR))
        a = a[i:j]
        tmp = os.path.join(ROOT, "cache", "tmp_line.wav")
        sf.write(tmp, a, SR)
        segs, _ = wm.transcribe(tmp, word_timestamps=True, language="en", beam_size=5)
        hyp = []
        for w in (w for s in segs for w in s.words):
            if hyp and w.word.strip().startswith("-"):
                hyp[-1] = type("W", (), {"word": hyp[-1].word + w.word.strip(), "start": hyp[-1].start, "end": w.end})
            else:
                hyp.append(w)
        ref = ln["text"].split()
        # map script words onto whisper words by order (proportional fallback when counts differ)
        if len(hyp) == len(ref):
            st = [(w.start, w.end) for w in hyp]
        else:
            print("count mismatch", ln["id"], len(ref), len(hyp), " ".join(w.word for w in hyp))
            hs, he = (hyp[0].start, hyp[-1].end) if hyp else (0, len(a) / SR)
            L = sum(len(w) for w in ref)
            st, c = [], hs
            for w in ref:
                d = (he - hs) * len(w) / L
                st.append((c, c + d)); c += d
        for w, (s, e2) in zip(ref, st):
            words.append({"w": w, "s": round(t + s, 3), "e": round(t + e2, 3), "line": ln["id"]})
        lines.append({"id": ln["id"], "scene": ln["scene"], "s": round(t, 3), "e": round(t + len(a) / SR, 3),
                      "heard": " ".join(w.word.strip() for w in hyp)})
        out.append(a)
        t += len(a) / SR
        g = GAP[ln["id"]]
        out.append(np.zeros(int(g * SR), np.float32)); t += g
    vo = np.concatenate(out)
    sf.write(os.path.join(ROOT, "assets", "audio", "vo.wav"), vo, SR)
    json.dump(words, open(os.path.join(ROOT, "plan", "words.json"), "w"), indent=0)
    json.dump(lines, open(os.path.join(ROOT, "plan", "lines.json"), "w"), indent=1)
    print("duration", round(len(vo) / SR, 2))
    for l in lines:
        print(l["id"], l["s"], l["e"], "|", l["heard"])


if __name__ == "__main__":
    main()
