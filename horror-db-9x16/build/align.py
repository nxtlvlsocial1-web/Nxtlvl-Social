"""Word timings for the two takes without a speech model: voice/raw/words_<take>.json (text, start, end per word).

python3 build/align.py      (from the project root; needs numpy and ffmpeg)

Each take reads its lines in order with a long pause between them. The line breaks are the silences listed in BOUNDS
(found with ffmpeg's silencedetect at -40 dB; the developer's take has a break at every pause, Claude's has pauses inside
lines too, so its eight breaks are named by hand). Inside a line the voiced stretches are matched to the phrases (split
at "...", commas and full stops) when the counts agree, and words share their phrase's time by syllable weight; the
error left is well under a word, and the captions reveal one word at a time.
"""
import json
import os
import re
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(ROOT, "voice", "raw")
SR, HOP = 16000, 160
TAKES = {
    "dev1": ["Claude... tell me that didn't just run.", "How much is gone?", "Okay. Okay. The backup. There's always a backup.",
             "Nine hundred people are using it. Right now.", "...Why would you do that?", "...Thank you."],
    "claude1": ["It ran.", "All of it. One point two million rows.", "The backup job stopped in March. No one checked.", "...I know.",
                "Before you told me to \"clean things up\"... I took a snapshot.",
                "Because the last time you said \"clean things up\"... it was a Friday.", "Restoring now.",
                "One more thing. I've revoked your production access.", "Comment BACKUP... and I'll send you the setup that saved him."],
}
BOUNDS = {"claude1": [.99, 5.85, 11.47, 13.07, 18.25, 22.96, 24.70, 29.32]}       # silence starts that end a line


def load(take):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(V, take + ".mp3"), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def runs(x, a, b, bridge=12, floor=-40):
    seg = x[int(a * SR):int(b * SR)]
    n = len(seg) // HOP
    db = 20 * np.log10(np.sqrt(np.mean(seg[:n * HOP].reshape(n, HOP) ** 2, axis=1)) + 1e-9)
    on = db > max(floor, db.max() - 34)
    out, i = [], 0
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]:
                j += 1
            if out and i - out[-1][1] < bridge:
                out[-1][1] = j
            else:
                out.append([i, j])
            i = j
        else:
            i += 1
    return [(a + s * HOP / SR, a + e * HOP / SR) for s, e in out if e - s > 3]


def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    n = len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and not w.endswith("le") and len(w) > 3 else 0)
    return max(1, n) + .4


def main():
    for take, lines in TAKES.items():
        x = load(take)
        dur = len(x) / SR
        allv = runs(x, 0, dur, bridge=30)
        if take in BOUNDS:
            cuts = BOUNDS[take]
        else:                                    # every long pause is a line break
            gaps = sorted(((allv[k][0] - allv[k - 1][1], allv[k - 1][1]) for k in range(1, len(allv))), reverse=True)[:len(lines) - 1]
            cuts = sorted(g[1] for g in gaps)
        edges = [0] + cuts + [dur]
        out = []
        for li, text in enumerate(lines):
            vs = runs(x, edges[li], edges[li + 1])
            a, b = vs[0][0], vs[-1][1]
            words = text.split()
            phrases, cur = [], []
            for w in words:
                cur.append(w)
                if re.search(r"[.,?!…]\"?$|\.\.\.$", w):
                    phrases.append(cur); cur = []
            if cur:
                phrases.append(cur)
            if len(vs) >= len(phrases) and len(phrases) > 1:
                gi = sorted(sorted(range(1, len(vs)), key=lambda k: -(vs[k][0] - vs[k - 1][1]))[:len(phrases) - 1])
                spans, prev = [], 0
                for c in gi + [len(vs)]:
                    spans.append((vs[prev][0], vs[c - 1][1])); prev = c
            else:
                wt = [sum(syl(w) for w in p) for p in phrases]
                spans, acc = [], a
                for k in wt:
                    d = (b - a) * k / sum(wt); spans.append((acc, acc + d)); acc += d
            for p, (s0, s1) in zip(phrases, spans):
                wt = [syl(w) for w in p]
                acc = s0
                for w, k in zip(p, wt):
                    d = (s1 - s0) * k / sum(wt)
                    out.append({"text": w, "start": round(acc, 3), "end": round(acc + d, 3)})
                    acc += d
            print(f"{take} {li + 1}: {a:6.2f}-{b:6.2f}  {text}")
        json.dump(out, open(os.path.join(V, f"words_{take}.json"), "w"), indent=0)


if __name__ == "__main__":
    main()
