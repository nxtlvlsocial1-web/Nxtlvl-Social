"""Caption clock: the words of the script (plan/words_tight.json text) on the timings Whisper hears in the tight cut itself
(plan/words_check.json, from build/transcribe.py on assets/video/tight.mp4), so each caption lands as the word is spoken.
Each line's first word never starts before its line. Writes plan/words_final.json.  python3 build/words_final.py"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "plan", "words_tight.json")))
C = json.load(open(os.path.join(ROOT, "plan", "words_check.json")))
norm = lambda s: re.sub(r"[^a-z']", "", s.lower())
assert len(C) == len(T["words"]), (len(C), len(T["words"]))
out = []
for w, c in zip(T["words"], C):
    if norm(w["w"]) != norm(c["w"]):
        print("text differs:", w["w"], "/", c["w"], "(script text kept)")
    a, b = T["lines"][w["line"]]
    out.append({"line": w["line"], "text": w["w"].replace("But,", "But").replace("how,", "how"),
                "s": round(max(c["s"], a), 3), "e": round(min(max(c["e"], c["s"] + .08), b + .05), 3)})
json.dump({"dur": T["dur"], "lines": T["lines"], "words": out}, open(os.path.join(ROOT, "plan", "words_final.json"), "w"), indent=0)
print(len(out), "words")
