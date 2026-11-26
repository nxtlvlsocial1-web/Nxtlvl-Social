"""SST Journey v2: the voice is recorded as whole passages (g1..g9, plan/script.json) for a natural read; the composition
times everything per sentence (j00..j16, the brief's master script lines). This splits plan/words.json back into
sentences in script order, keeps the script's spelling (aligned word by word when Whisper splits or merges a word), and
writes plan/words.json (sentence ids) + plan/sentences.json (id -> text). The passage-level file is kept as
plan/words_passages.json.
python3 build/relabel.py
"""
import difflib
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "plan")
script = json.load(open(os.path.join(P, "script.json")))
src = os.path.join(P, "words_passages.json")
if not os.path.exists(src):
    os.replace(os.path.join(P, "words.json"), src)
W = json.load(open(src))


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


out, sentences, n = [], {}, 0
for ln in script:
    heard = [w for w in W if w["line"] == ln["id"]]
    sents = [s for s in re.split(r"(?<=[.?!])\s+", ln["text"]) if s]
    # script words, with the sentence each belongs to
    sw = [(word, k) for k, s in enumerate(sents) for word in s.split()]
    a, b = [norm(x[0]) for x in sw], [norm(h["w"]) for h in heard]
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    m = {}                                           # script word index -> heard word index
    for blk in sm.get_matching_blocks():
        for i in range(blk.size):
            m[blk.a + i] = blk.b + i
    for k, s in enumerate(sents):
        sid = f"j{n:02d}"
        sentences[sid] = s
        idx = [i for i, (_, kk) in enumerate(sw) if kk == k]
        for i in idx:
            if i in m:
                h = heard[m[i]]
                t0, t1 = h["t0"], h["t1"]
            else:                                    # an unmatched word: borrow the neighbours' times
                prev = max((m[j] for j in m if j < i), default=0)
                nxt = min((m[j] for j in m if j > i), default=len(heard) - 1)
                t0, t1 = heard[prev]["t1"], heard[nxt]["t0"]
            out.append({"line": sid, "w": sw[i][0], "t0": round(t0, 3), "t1": round(max(t1, t0 + .05), 3)})
        n += 1
json.dump(out, open(os.path.join(P, "words.json"), "w"), indent=0)
json.dump(sentences, open(os.path.join(P, "sentences.json"), "w"), indent=1)
for sid, s in sentences.items():
    ws = [w for w in out if w["line"] == sid]
    print(sid, ws[0]["t0"], ws[-1]["t1"], s)
