"""Cue sheet for the real-sfx skill's mix.py: plan/sfx_events.json (written by build/generate.py) -> real CC0
recordings from the OpenGameArt library built for Spin Bout U (../spin-bout-u-drake/assets/sfx/oga; all CC0, no credit
needed). Openverse comes first by the house rule, but its Freesound downloads are refused from cloud sessions, so the
OGA packs are the fallback.

The ElevenLabs reference's sound grammar, rebuilt with these recordings:
- Into a split: a big whoosh with a sub hit.
- Into a full frame: a quick whoosh.
- On the colour flash: a shimmer.
- On a red key word: a punch hit.
- On the motion elements: soft UI pops and clicks (at most one per 0.7 s).
- A cash sound on the counters, a notification chime, and a stamp plus a rising hit on the CTA.
They sit under the voice.

python3 build/sfx_sheet.py VIDEO.mp4 [--out renders/cues.json]
"""
import argparse
import itertools
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = os.path.join(os.path.dirname(ROOT), "spin-bout-u-drake", "assets", "sfx", "oga")
RPG_SWING = sorted(x for x in os.listdir(os.path.join(L, "rpg-sound-pack")) if "swing" in x.lower())


def f(rel):
    p = os.path.join(L, rel)
    if not os.path.exists(p):
        raise SystemExit(f"missing sound: {rel}")
    return p


def punch(kind):
    d = os.path.join(L, "150-combat-sound-effects")
    return [os.path.join(d, x) for x in sorted(os.listdir(d)) if x.startswith(f"01_combat_melee__impact_punch_{kind}_")]


SUB = {"lowpass": 300, "max_dur": .55, "fade_out": .2}
KINDS = {   # kind: (files to rotate, role, gain_db, extra)
    "whoosh_big": ([f("wind-hit-time-morph/qubodup-megaswosh1.wav"), f("wind-hit-time-morph/60009__qubodup__swosh_22.flac"),
                    f("fantasy-sound-effects-tinysized-sfx/sfx-cc0__tube-plastic-whoosh-01.wav"), f("rpg-sound-pack/" + RPG_SWING[0])],
                   "whoosh", -6, {"max_dur": .8, "pitch": -2}),
    "boom": ([f("sci-fi-sounds/Audio__lowFrequency_explosion_000.ogg"), f("25-cc0-bang-firework-sfx/bang_03.ogg"),
              f("sci-fi-sounds/Audio__lowFrequency_explosion_001.ogg")], "hit", -9, SUB),
    "whoosh": ([f("swishes-sound-pack/swishes__swish-4.wav"), f("fantasy-sound-effects-tinysized-sfx/sfx-cc0__tube-plastic-whoosh-02.wav"),
                f("swishes-sound-pack/swishes__swish-8.wav"), f("rpg-sound-pack/" + RPG_SWING[1]),
                f("fantasy-sound-effects-tinysized-sfx/sfx-cc0__tin-whistle-whoosh-02.wav")], "whoosh", -9, {"max_dur": .6}),
    "swish": ([f("swishes-sound-pack/swishes__swish-6.wav"), f("rpg-sound-pack/" + RPG_SWING[2])], "whoosh", -11, {"max_dur": .5}),
    "shimmer": ([f("fantasy-magic-spell/fantasy_magic_button_1.mp3")], "chime", -15, {"max_dur": .7, "fade_out": .3}),
    "hit": (punch("medium"), "hit", -12, {"max_dur": .35}),
    "pop": ([f("100-cc0-sfx/plop_02.ogg"), f("interface-sounds/Audio__click_002.ogg"), f("ui-sounds/button1.ogg"),
             f("100-cc0-sfx/plop_01.ogg"), f("interface-sounds/Audio__tick_001.ogg"), f("ui-sounds/button2.ogg")], "pop", -15, {"max_dur": .3}),
    "notify": ([f("interface-sounds/Audio__confirmation_001.ogg")], "ui", -12, {}),
    "cash": ([f("coin-sounds/coinsounds011015.wav")], "coin", -13, {"max_dur": .9, "fade_out": .3}),
    "stamp": (punch("heavy"), "hit", -8, {"max_dur": .45}),
    "riser_hit": ([f("wind-hit-time-morph/qubodup-megaswosh2.wav")], "whoosh", -8, {"max_dur": .7}),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", default=os.path.join(ROOT, "renders", "cues.json"))
    a = ap.parse_args()
    ev = json.load(open(os.path.join(ROOT, "plan", "sfx_events.json")))
    trans = [e["t"] for e in ev if e["type"] in ("whoosh_big", "whoosh", "boom")]
    rot = {k: itertools.cycle(v[0]) for k, v in KINDS.items()}
    cues, uses = [], {}
    for e in ev:
        k, t = e["type"], e["t"]
        if k not in KINDS:
            continue
        if k in ("pop", "hit") and any(abs(t - x) < .25 for x in trans):
            continue                                       # a transition already carries this moment
        if k == "pop" and any(c["label"] == "pop" and t - c["t"] < .7 for c in cues):
            continue
        files, role, gain, extra = KINDS[k]
        fn = next(rot[k])
        n = uses.get(fn, 0)
        uses[fn] = n + 1
        c = {"t": max(0.0, t), "label": k, "file": fn, "role": role, "gain_db": gain} | extra
        if n and "pitch" not in extra:
            c["pitch"] = (0, -1, 1, -2, 2)[n % 5]
        cues.append(c)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump({"video": os.path.abspath(a.video), "keep_audio": "yes", "cues": cues}, open(a.out, "w"), indent=1)
    by = {}
    for c in cues:
        by[c["label"]] = by.get(c["label"], 0) + 1
    print(f"{len(cues)} cues -> {a.out}", by)


if __name__ == "__main__":
    main()
