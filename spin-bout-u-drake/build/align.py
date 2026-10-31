"""Align the owner's lyrics (plan/lyrics.md) to the Scribe word timings: writes plan/lines.json.

python3 build/align.py      (from the project root)

Each lyric word gets the start/end of the transcript word it matches (difflib on normalized spellings); words the
transcript heard differently ("assholes" for "ass hoes", "it" for "you") take the timing of their counterpart, and any
leftovers are spread between their neighbours. Times are in edit seconds: song time minus EDIT_START.
"""
import difflib
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIBE_OFFSET = 125.0          # the transcribed clip started at song 2:05
EDIT_START = 133.0             # the edit starts on the bass drop at 2:13.0


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower().replace("'", ""))


def main():
    raw = json.load(open(os.path.join(ROOT, "plan", "words_scribe_raw.json")))["words"]
    sw = [w for w in raw if w.get("type", "word") == "word"]
    first = next(i for i, w in enumerate(sw) if norm(w["text"]) == "jealous")
    sw = sw[first:]                    # the owner's lyrics start at "Jealous"
    body = open(os.path.join(ROOT, "plan", "lyrics.md")).read().split("\n\n", 2)[2]   # after the title and notes
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    lw = [(li, w) for li, l in enumerate(lines) for w in re.findall(r"[\w'&]+", l)]   # "Jealous-ass" -> two words
    a = [norm(w) for _, w in lw]
    b = [norm(w["text"]) for w in sw]
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    t = [None] * len(lw)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1):
                t[i1 + k] = (sw[j1 + k]["start"], sw[j1 + k]["end"])
        elif tag == "replace":
            s0, e0 = sw[j1]["start"], sw[j2 - 1]["end"]
            n = i2 - i1
            for k in range(n):
                t[i1 + k] = (s0 + (e0 - s0) * k / n, s0 + (e0 - s0) * (k + 1) / n)
    for i in range(len(t)):            # leftovers: between neighbours
        if t[i] is None:
            p = next((t[j] for j in range(i - 1, -1, -1) if t[j]), (0, 0))
            q = next((t[j] for j in range(i + 1, len(t)) if t[j]), (p[1] + .3, p[1] + .5))
            t[i] = (p[1], max(p[1] + .05, min(q[0], p[1] + .25)))
    out = []
    for li, l in enumerate(lines):
        ws = [(w, round(s + SCRIBE_OFFSET - EDIT_START, 3), round(e + SCRIBE_OFFSET - EDIT_START, 3))
              for (lj, w), (s, e) in zip(lw, t) if lj == li]
        out.append({"text": l, "words": ws, "start": ws[0][1], "end": ws[-1][2]})
    json.dump(out, open(os.path.join(ROOT, "plan", "lines.json"), "w"), indent=1, ensure_ascii=False)
    for o in out:
        print(f"{o['start']:6.2f}-{o['end']:6.2f}  {o['text']}")


if __name__ == "__main__":
    main()
