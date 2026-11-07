"""Cue sheet for the real-sfx skill's mix.py: plan/sfx_events.json (written by build/generate.py) -> real CC0 recordings.

House rule: Openverse first. Every Openverse sound for these cues is a Freesound file, and Freesound refuses downloads
from cloud sessions (403), so the CC0 OpenGameArt library built for Spin Bout U is used instead
(../spin-bout-u-drake/assets/sfx/oga; all CC0, no credit needed). No music; the effects sit well under the voice.

python3 build/sfx_sheet.py VIDEO.mp4 [--out renders/cues.json]
"""
import argparse
import itertools
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = os.path.join(os.path.dirname(ROOT), "spin-bout-u-drake", "assets", "sfx", "oga")
TS = "fantasy-sound-effects-tinysized-sfx/sfx-cc0__"


def f(rel):
    p = os.path.join(L, rel)
    if not os.path.exists(p):
        raise SystemExit(f"missing sound: {rel}")
    return p


KINDS = {   # kind: (files to rotate, role, gain_db, extra)
    "paper": ([f("100-cc0-sfx/paper_01.ogg"), f("100-cc0-sfx/paper_02.ogg")], "foley", -16, {"max_dur": .45}),
    "tear": ([f(TS + "cover-paper-tear-01.wav"), f(TS + "cover-paper-tear-02.wav")], "foley", -15, {"max_dur": .6, "fade_out": .2, "anchor": "end"}),
    "tear_big": ([f(TS + "cover-paper-tear-02.wav"), f(TS + "cover-paper-tear-01.wav")], "foley", -13, {"max_dur": .75, "fade_out": .2}),
    "whoosh": ([f("swishes-sound-pack/swishes__swish-4.wav"), f(TS + "tube-plastic-whoosh-02.wav"), f("swishes-sound-pack/swishes__swish-8.wav")],
               "whoosh", -15, {"max_dur": .5}),
    "zoom": ([f("wind-hit-time-morph/qubodup-megaswosh2.wav")], "whoosh", -17, {"reverse": True, "max_dur": .45, "anchor": "end"}),
    "swish": ([f("swishes-sound-pack/swishes__swish-6.wav")], "whoosh", -18, {"max_dur": .4}),
    "pop": ([f("100-cc0-sfx/plop_01.ogg"), f("100-cc0-sfx/plop_02.ogg"), f("interface-sounds/Audio__click_002.ogg")], "pop", -18, {"max_dur": .3}),
    "tick": ([f("interface-sounds/Audio__confirmation_001.ogg")], "ui", -17, {"max_dur": .5}),
    "marker": ([f("202-more-sound-effects/Paper _ Stationery__Stationery_42.wav")], "foley", -19, {"max_dur": .5, "fade_out": .15}),
    "chime": ([f("bell-dingschimes/bell_ding2.wav"), f("bell-dingschimes/bell_ding1.wav")], "chime", -21, {"max_dur": 1.0, "fade_out": .4}),
    "shimmer": ([f("fantasy-magic-spell/fantasy_magic_button_1.mp3")], "chime", -20, {"max_dur": .7, "fade_out": .3}),
    "firework": ([f("25-cc0-bang-firework-sfx/bang_09.ogg"), f("25-cc0-bang-firework-sfx/bang_04.ogg"), f("25-cc0-bang-firework-sfx/bang_02.ogg")],
                 "ambience", -21, {"max_dur": .9, "fade_out": .3}),
    "rocket": ([f(TS + "tin-whistle-whoosh-01.wav"), f(TS + "tin-whistle-whoosh-02.wav")], "whoosh", -20, {"max_dur": .5}),
    "coin": ([f(TS + "coin-spin-fall-01.wav")], "coin", -19, {"max_dur": 1.0, "fade_out": .3}),
    "stamp": ([f("150-combat-sound-effects/" + sorted(x for x in os.listdir(os.path.join(L, "150-combat-sound-effects"))
                                                    if x.startswith("01_combat_melee__impact_punch_medium_"))[0])], "hit", -17, {"max_dur": .35}),
    "hit": ([f("100-cc0-sfx/hit_01.ogg")], "hit", -17, {"max_dur": .35}),
    "thud": ([f("75-cc0-breaking-falling-hit-sfx/bfh1_hit_02.ogg")], "foley", -18, {"max_dur": .4}),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", default=os.path.join(ROOT, "renders", "cues.json"))
    a = ap.parse_args()
    ev = json.load(open(os.path.join(ROOT, "plan", "sfx_events.json")))
    rot = {k: itertools.cycle(v[0]) for k, v in KINDS.items()}
    cues, uses, last = [], {}, {}
    for e in ev:
        k, t = e["type"], e["t"]
        if k not in KINDS:
            continue
        if t - last.get(k, -9) < .25:          # the same sound twice in a quarter second reads as a stutter
            continue
        last[k] = t
        files, role, gain, extra = KINDS[k]
        fn = next(rot[k])
        n = uses.get(fn, 0)
        uses[fn] = n + 1
        c = {"t": max(0.0, t), "label": k, "file": fn, "role": role, "gain_db": gain} | extra
        if n:
            c["pitch"] = (0, -1, 1, -2, 2)[n % 5]
        cues.append(c)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump({"video": os.path.abspath(a.video), "keep_audio": "yes", "cues": cues}, open(a.out, "w"), indent=1)
    print(f"{len(cues)} cues -> {a.out}")


if __name__ == "__main__":
    main()
