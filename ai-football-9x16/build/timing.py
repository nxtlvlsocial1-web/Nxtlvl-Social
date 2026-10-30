"""Word timings for the reel's captions, from ElevenLabs Scribe (voice/scribe_words.json) and voice/lines.json.

python3 build/timing.py      (from the project root, after build/voice.py and a Scribe transcription of
                              assets/audio/voice.wav saved as voice/scribe_words.json)
  -> build/words.json: every caption word, spelled as in the script, with its start/end in s

Scribe hears "30,000" where the script says "Thirty thousand", so the two are aligned letter by letter: every script
letter that matches a Scribe letter takes its time (each Scribe word's time spread over its letters), and the letters
in between (numbers written out, hyphens) are interpolated between the matched ones.
"""
import difflib
import json
import os
import re

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())  # noqa: E731


def main():
    lines = json.load(open(os.path.join(ROOT, "voice", "lines.json")))["lines"]
    sw = [w for w in json.load(open(os.path.join(ROOT, "voice", "scribe_words.json")))["words"] if w.get("type", "word") == "word"]
    # Scribe letters with times
    sc, st = [], []
    for w in sw:
        n = norm(w["text"])
        for k, ch in enumerate(n):
            sc.append(ch); st.append(w["start"] + (w["end"] - w["start"]) * (k + .5) / len(n))
    # script words and letters
    words = []
    for ln in lines:
        for w in ln["text"].replace("...", "… ").split():
            words.append((ln["line"], ln["speaker"], w))
    pc, owner = [], []
    for i, (_, _, w) in enumerate(words):
        for ch in norm(w):
            pc.append(ch); owner.append(i)
    t = np.full(len(pc), np.nan)
    for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, pc, sc, autojunk=False).get_opcodes():
        if op == "equal":
            t[a1:a2] = st[b1:b2]
        elif op == "replace":                   # "thirtythousand" said as "30000": spread over the heard span
            t[a1:a2] = np.linspace(st[b1], st[b2 - 1], a2 - a1)
    ok = ~np.isnan(t)
    t = np.interp(np.arange(len(pc)), np.flatnonzero(ok), t[ok])
    out = []
    for i, (line, who, w) in enumerate(words):
        idx = [k for k, o in enumerate(owner) if o == i]
        s, e = float(t[idx[0]]) - .05, float(t[idx[-1]]) + .05
        out.append({"line": line, "speaker": who, "w": w, "s": round(s, 3), "e": round(max(e, s + .08), 3)})
    # keep words inside their line
    for ln in lines:
        ws = [w for w in out if w["line"] == ln["line"]]
        for w in ws:
            w["s"] = max(w["s"], ln["start"]); w["e"] = min(w["e"], ln["end"] + .1)
        print(f"{ln['line']:2d} " + " ".join(f"{w['w']}@{w['s']:.2f}" for w in ws))
    json.dump(out, open(os.path.join(HERE, "words.json"), "w"), indent=0)
    print("wrote words.json", len(out), "words")


if __name__ == "__main__":
    main()
