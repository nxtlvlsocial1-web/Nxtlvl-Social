"""Caption clock: the words as Whisper hears them in the tight cut itself (plan/words_check.json, build/transcribe.py on
assets/video/tight.mp4), each given the line it falls in (plan/words_tight.json lines). A line's first word never
starts before its line. Writes plan/words_final.json.  python3 build/words_final.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "plan", "words_tight.json")))
C = json.load(open(os.path.join(ROOT, "plan", "words_check.json")))
FIX = {}                       # word text fixes, if Whisper mishears (none needed for this take)
out = []
for c in C:
    m = (c["s"] + c["e"]) / 2
    ln = min(T["lines"], key=lambda k: 0 if T["lines"][k][0] - .05 <= m <= T["lines"][k][1] + .05 else 1 + min(abs(m - T["lines"][k][0]), abs(m - T["lines"][k][1])))
    a, b = T["lines"][ln]
    out.append({"line": ln, "text": FIX.get(c["w"], c["w"]), "s": round(max(c["s"], a), 3), "e": round(min(max(c["e"], c["s"] + .08), b + .05), 3)})
json.dump({"dur": T["dur"], "lines": T["lines"], "words": out}, open(os.path.join(ROOT, "plan", "words_final.json"), "w"), indent=0)
print(len(out), "words")
