"""SST v4 (owner: "only about the problems ... go through the article and mention the problems faced honestly"):
writes plan/edl.json, the footage cut timed to the voice (plan/words.json, sentence ids from build/relabel.py).
Every shot is a Pexels clip (licence in footage/pexels/pexels.json); one beat per problem the article reports.
python3 build/plan_v4.py && python3 build/prep_shots.py && python3 build/generate.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = json.load(open(os.path.join(ROOT, "plan", "words.json")))
S = {}
for w in W:
    S.setdefault(w["line"], []).append(w)
start = {k: v[0]["t0"] for k, v in S.items()}
end = {k: v[-1]["t1"] for k, v in S.items()}
last = sorted(S)[-1]                     # "Sports Science Technology." -> the end card
T_END = start[last] - .5

# (id, Pexels id, in point, focus, grade, extra filters, starts at, what)
PLAN = [
    ("s01", "19162466", 3.0, .5, "night", "gblur=sigma=20,eq=brightness=0.06:gamma=1.25", 0.0, "a phone in the dark, the screen unreadable"),
    ("s02", "7942762", 2.0, .45, "night", "eq=brightness=0.05:gamma=1.2", start["j01"] - .1, "a face lit by a laptop"),
    ("s03", "20563164", 1.0, .5, "night", "", start["j03"] - .1, "silhouette in a dark room"),
    ("s04", "7942761", 1.5, .5, "night", "", start["j04"] - .1, "a man lit by his phone"),
    ("s05", "19162466", 9.0, .5, "night", "gblur=sigma=14,eq=brightness=0.04:gamma=1.15", start["j10"] - .1, "the phone again: codes arriving"),
    ("s06", "7062988", 2.0, .5, "night", "", start["j11"] - .1, "at the desk, papers"),
    ("s07", "16538871", 3.0, .5, "dark", "", start["j12"] - .15, "a lone figure on a rainy street at night"),
    ("s08", "9531459", 6.0, .55, "dark", "", start["j13"] - .1, "a man watching from a parked car"),
    ("s09", "11792115", 4.0, .5, "dark", "", start["j14"] - .1, "a figure in the fog"),
    ("s10", "13891268", 2.0, .45, "dark", "", start["j15"] - .1, "a tyre in the rain"),
    ("s11", "14514406", 3.0, .4, "dark", "", (start["j15"] + end["j15"]) / 2, "a damaged wheel being changed"),
    ("s11b", "3974558", 9.0, .55, "dark", "eq=brightness=-0.09:gamma=0.85:saturation=0.8", start["j16"] - .1, "a wrecked car, the front end crushed (v6: the accidents line)"),
    ("s12", "7062984", 2.0, .55, "night", "", start["j17"] - .1, "filing papers into a box"),
    ("s13", "7062990", 1.5, .6, "night", "", start["j18"] - .2, "writing in the dark"),
    ("s14", "7062986", 1.0, .62, "turn", "", start["j19"] - .2, "hand to the head, thinking"),
    ("s15", "7062993", 2.0, .62, "turn", "", start["j20"] - .1, "stillness, hand on chin"),
]
shots = []
for k, (i, src, inn, focus, grade, extra, t, what) in enumerate(PLAN):
    t1 = PLAN[k + 1][6] if k + 1 < len(PLAN) else T_END + .5
    s = {"id": i, "src": src, "t": round(t, 3), "d": round(t1 - t, 3), "in": inn, "focus": focus, "grade": grade, "what": what}
    if extra:
        s["extra"] = extra
    if i in ("s02", "s07", "s08", "s09", "s10", "s11", "s11b"):
        s["cut"] = True                  # the problems cut hard; the quiet beats dissolve
    shots.append(s)
json.dump({"band": [1080, 1160], "handle": .6, "shots": shots, "overlays": []}, open(os.path.join(ROOT, "plan", "edl.json"), "w"), indent=1)
print(len(shots), "shots, ends", round(T_END, 2))
for s in shots:
    print(s["id"], s["src"], s["t"], s["d"], s["what"])
