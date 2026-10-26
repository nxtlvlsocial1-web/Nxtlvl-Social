"""Check every take in voice/lines/ and pick the most expressive clean one per line.

python opengym-claude-9x16/voice/qa_takes.py            (inside the voice venv; needs faster-whisper and librosa)
  -> voice/qa.json and a table: per take the transcript, word accuracy against the script, duration, the longest
     internal pause, peak level and pitch movement. Prints a ready `assemble --pick ...` line.

A take is "clean" when Whisper hears the script words (accuracy >= .85), there is no internal pause over .7 s,
nothing clips hard (the takes are float WAVs, so a peak just over 1.0 is fine before the loudness match), and it is not far longer than its siblings (a stall or a doubled word). Among the clean takes the
one with the most pitch movement (semitone spread) wins, the expressiveness proxy; ties go to the shorter take.
"""
import glob
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make_voices import LINES  # noqa: E402

# Whisper writes numbers and brand words its own way; fold them before comparing
FOLD = {"opengym": "open gym", "56": "fifty six", "5600": "fifty six hundred", "5,600": "fifty six hundred",
        "dm": "d m", "pre-filled": "prefilled", "pre filled": "prefilled", "claude's": "claude", "clod": "claude",
        "cloud": "claude", "clawed": "claude", "gim": "gym", "jim": "gym", "4": "four"}


def norm(t):
    t = t.lower().replace("-", " ").replace("…", " ")
    t = re.sub(r"[^a-z0-9' ]", " ", t)
    t = " ".join(t.split())
    for k, v in FOLD.items():
        t = re.sub(rf"\b{re.escape(k)}\b", v, t)
    t = t.replace("pre filled", "prefilled")
    return t.split()


def accuracy(ref, hyp):
    """1 - word error rate (Levenshtein over words), floored at 0."""
    r, h = ref, hyp
    d = np.zeros((len(r) + 1, len(h) + 1), int)
    d[:, 0] = range(len(r) + 1)
    d[0, :] = range(len(h) + 1)
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + (r[i - 1] != h[j - 1]))
    return max(0.0, 1 - d[-1, -1] / max(1, len(r)))


def main():
    import librosa
    from faster_whisper import WhisperModel
    m = WhisperModel("small.en", device="cpu", compute_type="int8")
    rows = []
    for i, (who, text, *_rest) in enumerate(LINES, 1):
        # the non-verbal sounds are not words to check
        ref = norm(re.sub(r"\([^)]*\)", "", text))
        for p in sorted(glob.glob(os.path.join(HERE, "lines", f"{i:02d}_{who}_t*.wav"))):
            y, sr = librosa.load(p, sr=16000)
            segs, _ = m.transcribe(y, language="en", word_timestamps=True, beam_size=5,
                                   initial_prompt="openGym, Claude, GYM, DM, dumbbells, pre-filled.")
            ws = [w for s in segs for w in s.words]
            hyp_text = " ".join(w.word.strip() for w in ws)
            hyp = norm(hyp_text)
            # drop leading non-verbal words Chatterbox speaks for (sighs)/(gasps)/(laughs)
            while hyp and hyp[0] in ("hhh", "hh", "h", "oh", "haha", "ha", "huh", "ah", "uh"):
                hyp = hyp[1:]
            gaps = [b.start - a.end for a, b in zip(ws, ws[1:])] or [0]
            f0, _, _ = librosa.pyin(y, fmin=60, fmax=400, sr=sr)
            f0 = f0[~np.isnan(f0)]
            spread = float(np.percentile(12 * np.log2(f0 / np.median(f0)), [5, 95]) @ [-1, 1]) if len(f0) > 10 else 0
            rows.append(dict(line=i, who=who, take=int(p[-5]), file=os.path.basename(p), dur=round(len(y) / sr, 2),
                             heard=hyp_text, acc=round(accuracy(ref, hyp), 2), max_gap=round(max(gaps), 2),
                             peak=round(float(np.max(np.abs(y))), 3), spread=round(spread, 1)))
            r = rows[-1]
            print(f"{r['file']:18s} {r['dur']:5.2f}s acc {r['acc']:.2f} gap {r['max_gap']:.2f} pk {r['peak']:.2f} "
                  f"st {r['spread']:4.1f} | {hyp_text}", flush=True)
    picks = {}
    for i in range(1, len(LINES) + 1):
        takes = [r for r in rows if r["line"] == i]
        if not takes:
            continue
        med = float(np.median([r["dur"] for r in takes]))
        for r in takes:
            r["clean"] = bool(r["acc"] >= .85 and r["max_gap"] <= .7 and r["peak"] < 1.1 and r["dur"] <= med * 1.3)
        pool = [r for r in takes if r["clean"]] or sorted(takes, key=lambda r: -r["acc"])[:1]
        best = max(pool, key=lambda r: (r["spread"], -r["dur"]))
        picks[i] = best["take"]
        best["picked"] = True
    json.dump({"takes": rows, "picks": picks}, open(os.path.join(HERE, "qa.json"), "w"), indent=1)
    flagged = sorted({r["line"] for r in rows if r["line"] in picks and not any(t["clean"] for t in rows if t["line"] == r["line"])})
    print("\nno clean take:", flagged or "none")
    print("assemble --pick " + " ".join(f"{i:02d}={k}" for i, k in picks.items()))


if __name__ == "__main__":
    main()
