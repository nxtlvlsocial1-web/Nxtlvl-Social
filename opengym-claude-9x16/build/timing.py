"""Word timings for the reel: transcribe assets/audio/voice.wav and map the script words onto them.

python opengym-claude-9x16/build/timing.py      (inside the voice venv; needs faster-whisper)
  -> build/words.json: every script word (as written in SCRIPT.md, without the non-verbals) with its start/end in s,
     and build/env.json: a 30 fps loudness envelope per speaker (drives the mouths).

Line boundaries come from voice/lines.json (assemble wrote them, so they are exact). Inside a line, each script word
takes the time of the Whisper word it aligns to; words Whisper missed are spread between their aligned neighbours.
"""
import difflib
import json
import os
import re

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
FPS = 30


def norm(w):
    w = w.lower().replace("’", "'")
    w = re.sub(r"[^a-z0-9']", "", w)
    return {"opengym": "open", "fiftysix": "fifty", "56": "fifty", "5600": "fifty", "prefilled": "pre", "cloud": "claude",
            "clawed": "claude", "clod": "claude", "jim": "gym", "gim": "gym"}.get(w, w)


def script_words(text):
    text = re.sub(r"\([^)]*\)", " ", text).replace("...", "… ").replace("…", "… ")
    return [w for w in text.split() if re.search(r"[A-Za-z0-9]", w)]


def main():
    from faster_whisper import WhisperModel
    lines = json.load(open(os.path.join(PROJ, "voice", "lines.json")))["lines"]
    m = WhisperModel("medium.en", device="cpu", compute_type="int8")
    import librosa
    audio, _ = librosa.load(os.path.join(PROJ, "assets", "audio", "voice.wav"), sr=16000)
    segs, _ = m.transcribe(audio, language="en", word_timestamps=True, beam_size=5,
                           initial_prompt="openGym. Claude. Comment GYM. I'll DM you. Dumbbells. Pre-filled.")
    heard = [(w.start, w.end, w.word.strip()) for s in segs for w in s.words]
    out = []
    for ln in lines:
        sw = script_words(ln["text"])
        hw = [h for h in heard if h[0] >= ln["start"] - .15 and h[1] <= ln["end"] + .15]
        a = [norm(w) for w in sw]
        b = [norm(h[2]) for h in hw]
        times = [None] * len(sw)
        for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
            for k in range(blk.size):
                times[blk.a + k] = (hw[blk.b + k][0], hw[blk.b + k][1])
        # fill gaps between aligned neighbours (or the line edges), weighted by word length
        i = 0
        while i < len(sw):
            if times[i] is not None:
                i += 1
                continue
            j = i
            while j < len(sw) and times[j] is None:
                j += 1
            t0 = times[i - 1][1] if i > 0 else ln["start"]
            t1 = times[j][0] if j < len(sw) else ln["end"]
            wts = [len(sw[k]) + 2 for k in range(i, j)]
            acc = t0
            for k, wgt in zip(range(i, j), wts):
                d = (t1 - t0) * wgt / sum(wts)
                times[k] = (acc, acc + d)
                acc += d
            i = j
        for w, (s, e) in zip(sw, times):
            s, e = max(ln["start"], s), min(ln["end"], e)
            out.append({"line": ln["line"], "speaker": ln["speaker"], "w": w, "s": round(s, 3), "e": round(max(e, s + .05), 3)})
        print(f"{ln['line']:2d} {ln['speaker']:5s} " + " ".join(f"{w}@{s:.2f}" for w, (s, _) in zip(sw, times)))
    json.dump(out, open(os.path.join(HERE, "words.json"), "w"), indent=0)
    # speaker envelopes for the mouths
    env = {"fps": FPS}
    for who in ("nxt", "human"):
        x, sr = sf.read(os.path.join(PROJ, "assets", "audio", f"voice_{who}.wav"))
        hop = sr // FPS
        n = len(x) // hop
        r = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1))
        r = r / (np.percentile(r[r > 1e-4], 95) + 1e-9)
        r = np.convolve(np.clip(r, 0, 1), [.25, .5, .25], "same")
        env[who] = [round(float(v), 2) for v in r]
    json.dump(env, open(os.path.join(HERE, "env.json"), "w"))
    print("wrote words.json", len(out), "words; env.json")


if __name__ == "__main__":
    main()
