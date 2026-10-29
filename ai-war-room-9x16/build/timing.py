"""Word timings and mouth envelopes for the reel, from assets/audio/voice.wav and voice/lines.json (no speech model).

python3 build/timing.py      (from the project root, after build/voice.py; needs numpy and ffmpeg)
  -> build/words.json: every caption word with its start/end in s
  -> build/env.json: a 30 fps loudness envelope per speaker (drives the mouths)

Line boundaries are exact (voice.py wrote them). Inside a line, the voiced stretches are found from the loudness, and
the script's phrases (split at "...", commas and full stops) are matched to the pauses between them when the counts
agree; words then share their phrase's time by syllable weight. Captions show 2-3 words at a time, so the error left
(well under a word) doesn't show.
"""
import json
import os
import re
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SR, FPS, HOP = 16000, 30, 160            # 10 ms analysis frames


def load():
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(ROOT, "assets", "audio", "voice.wav"), "-f", "s16le",
                          "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    n = len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and not w.endswith("le") and len(w) > 3 else 0)
    return max(1, n) + .4


def voiced(x, a, b):
    """Voiced stretches in [a, b] s as (start, end), pauses shorter than 120 ms bridged."""
    seg = x[int(a * SR):int(b * SR)]
    n = len(seg) // HOP
    db = 20 * np.log10(np.sqrt(np.mean(seg[:n * HOP].reshape(n, HOP) ** 2, axis=1)) + 1e-9)
    on = db > max(-42, db.max() - 32)
    runs, i = [], 0
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]:
                j += 1
            runs.append([i, j]); i = j
        else:
            i += 1
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] < 12:
            merged[-1][1] = r[1]
        else:
            merged.append(r)
    return [(a + s * HOP / SR, a + e * HOP / SR) for s, e in merged if e - s > 3]


def main():
    x = load()
    lines = json.load(open(os.path.join(ROOT, "voice", "lines.json")))["lines"]
    out = []
    for ln in lines:
        words = ln["text"].replace("...", "… ").split()
        phrases, cur = [], []
        for w in words:
            cur.append(w)
            if re.search(r"[.,?!…]$", w):
                phrases.append(cur); cur = []
        if cur:
            phrases.append(cur)
        vs = voiced(x, ln["start"], ln["end"])
        # split voiced runs at the widest gaps until there is one run per phrase (if there are enough gaps)
        if len(vs) >= len(phrases):
            gaps = sorted(range(1, len(vs)), key=lambda k: -(vs[k][0] - vs[k - 1][1]))[:len(phrases) - 1]
            cuts = sorted(gaps)
            spans, prev = [], 0
            for c in cuts + [len(vs)]:
                spans.append((vs[prev][0], vs[c - 1][1])); prev = c
        else:                                   # not enough pauses: share the whole voiced line by weight
            a, b = (vs[0][0], vs[-1][1]) if vs else (ln["start"], ln["end"])
            wt = [sum(syl(w) for w in p) for p in phrases]
            spans, acc = [], a
            for k in wt:
                d = (b - a) * k / sum(wt); spans.append((acc, acc + d)); acc += d
        for p, (a, b) in zip(phrases, spans):
            wt = [syl(w) for w in p]
            acc = a
            for w, k in zip(p, wt):
                d = (b - a) * k / sum(wt)
                out.append({"line": ln["line"], "speaker": ln["speaker"], "w": w, "s": round(acc, 3), "e": round(acc + d, 3)})
                acc += d
        print(f"{ln['line']:2d} " + " ".join(f"{w['w']}@{w['s']:.2f}" for w in out if w["line"] == ln["line"]))
    json.dump(out, open(os.path.join(HERE, "words.json"), "w"), indent=0)
    # speaker envelopes: the voice track's loudness, given to whoever speaks that line
    hop = SR // FPS
    n = len(x) // hop
    r = np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, axis=1))
    r = np.clip(r / (np.percentile(r[r > 1e-4], 95) + 1e-9), 0, 1)
    r = np.convolve(r, [.25, .5, .25], "same")
    env = {"fps": FPS}
    for who in ("claude", "creator"):
        m = np.zeros(n)
        for ln in lines:
            if ln["speaker"] == who:
                m[int(ln["start"] * FPS):int(ln["end"] * FPS) + 1] = 1
        env[who] = [round(float(v), 2) for v in r * m]
    json.dump(env, open(os.path.join(HERE, "env.json"), "w"), separators=(",", ":"))
    print("wrote words.json", len(out), "words; env.json")


if __name__ == "__main__":
    main()
