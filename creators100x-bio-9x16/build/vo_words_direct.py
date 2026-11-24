"""Word times straight from faster-whisper on the trimmed voice (vo_words.py's line matcher tripped on "12 views. 19. 23."):
the transcript's words are matched to the script's words in order (difflib), then written as plan/words.json.
HF_HOME=/root/tts/hf /root/tts/.venv/bin/python build/vo_words_direct.py"""
import difflib, json, os, re, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "build"))
src = open(os.path.join(ROOT, "build", "vo_words.py")).read()
LINES = eval(src[src.index("LINES = [") + 8:src.index("]", src.index("LINES = [")) + 1])
norm = lambda w: re.sub(r"[^a-z0-9']", "", w.lower()).replace("creedum", "creedom")
script = [(lid, w) for lid, text in LINES for w in text.split()]
y = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(ROOT, "assets", "audio", "vo.wav"), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                 capture_output=True).stdout, np.float32)
hyp = [w for s in WhisperModel("small.en", device="cpu", compute_type="int8").transcribe(y, word_timestamps=True)[0] for w in s.words]
sm = difflib.SequenceMatcher(a=[norm(w) for _, w in script], b=[norm(w.word) for w in hyp], autojunk=False)
t_of = {}
for a, b, n in sm.get_matching_blocks():
    for k in range(n):
        t_of[a + k] = (hyp[b + k].start, hyp[b + k].end)
out, last = [], 0.0
for i, (lid, w) in enumerate(script):
    if i in t_of:
        t0, t1 = t_of[i]
    else:                                   # unmatched: the next matched word's start, or just after the last one
        nxt = next((t_of[j][0] for j in range(i + 1, len(script)) if j in t_of), last + .2)
        t0 = t1 = max(last, nxt - .15)
    out.append({"line": lid, "w": w, "t0": round(t0, 3), "t1": round(t1, 3)})
    last = t1
json.dump(out, open(os.path.join(ROOT, "plan", "words.json"), "w"), indent=0)
print(f"{len(t_of)}/{len(script)} words matched")
