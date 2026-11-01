"""Cue sheet for the real-sfx skill's mix.py (v10): plan/sfx_events_1x1.json (or sfx_events.json for 9:16), written by
build/generate.py, -> exact real recordings from the CC0 OpenGameArt library that the Spin Bout U edit built
(../spin-bout-u-drake/assets/sfx/oga, credits in ../spin-bout-u-drake/plan/sfx_credits_oga.json; all CC0, no credit
needed). Openverse comes first by the house rule; its Freesound downloads are refused from cloud sessions, so these
packs are the fallback.

The owner's rules for this edit: sound effects from 3 s on only (generate.py SFX_FROM), the song untouched. Under a
full song the effects stay a layer: no typing or star ticks, one camera click per 2.6 s, label pops thinned, a paper
slap at most once (the owner disliked repeated slaps on Spin Bout U), bass-weighted cut whooshes with a low sub layer.

python3 build/sfx_sheet.py RENDER.mp4 [--events plan/sfx_events_1x1.json] [--out cache/sfx/cues.json]
"""
import argparse
import itertools
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = os.path.join(os.path.dirname(ROOT), "spin-bout-u-drake", "assets", "sfx", "oga")
RPG_SWING = sorted(x for x in os.listdir(os.path.join(L, "rpg-sound-pack")) if "swing" in x.lower())
R8P = ("512-sound-effects-8-bit-style/The Essential Retro Video Game Sound Effects Collection _512 sounds_ By Juhani Junkala__"
       "Movement__Portals and Transitions__")
PUNCH = "150-combat-sound-effects/01_combat_melee__impact_punch_"
SFX_FROM = 3.0


def f(rel):
    p = os.path.join(L, rel)
    if not os.path.exists(p):
        raise SystemExit(f"missing sound: {rel}")
    return p


def punch(kind):
    d = os.path.join(L, "150-combat-sound-effects")
    return [os.path.join(d, x) for x in sorted(os.listdir(d)) if x.startswith(f"01_combat_melee__impact_punch_{kind}_")]


# kind: (files to rotate through, role, gain_db, extra cue fields)
KINDS = {
    "whoosh": ([f("rpg-sound-pack/" + RPG_SWING[0]), f("wind-hit-time-morph/60009__qubodup__swosh_22.flac"),
                f("swishes-sound-pack/swishes__swish-9.wav"), f("wierd-whooshes/weird_whoosh_sounds_-_whoosh_12_0.mp3"),
                f(R8P + "sfx_movement_portal5.wav"), f("rpg-sound-pack/" + RPG_SWING[1])], "whoosh", -4, {"max_dur": 1.0}),
    "swish": ([f("swishes-sound-pack/swishes__swish-4.wav"), f("wind-hit-time-morph/qubodup-megaswosh2.wav"),
               f("fantasy-sound-effects-tinysized-sfx/sfx-cc0__cloth-pouch-shake-01.wav"), f("rpg-sound-pack/" + RPG_SWING[2]),
               f("swishes-sound-pack/swishes__swish-6.wav")], "whoosh", -6, {"max_dur": .8}),
    "whoosh_big": ([f("wind-hit-time-morph/qubodup-megaswosh1.wav"), f("wind-hit-time-morph/60009__qubodup__swosh_22.flac"),
                    f("wind-hit-time-morph/qubodup-megaswosh2.wav"), f("rpg-sound-pack/" + RPG_SWING[0])], "whoosh", -2, {"max_dur": .9}),
    "glitch": ([f(p_) for k in range(4) for p_ in (f"interface-sounds/Audio__glitch_00{k + 1}.ogg",
                                                     f"sci-fi-sounds/Audio__computerNoise_00{k}.ogg")], "glitch", -8, {"max_dur": .3}),
    "hit": ([f("100-cc0-sfx-2/sfx100v2_hit_01.ogg"), f("75-cc0-breaking-falling-hit-sfx/bfh1_hit_02.ogg"),
             f("100-cc0-sfx-2/sfx100v2_hit_03.ogg")], "hit", -5, {}),
    "slam": (punch("heavy"), "hit", -5, {"max_dur": .5}),
    "stamp": (punch("medium"), "hit", -6, {"max_dur": .4}),
    "keyword": ([f("100-cc0-sfx-2/sfx100v2_hit_01.ogg"), f("100-cc0-sfx-2/sfx100v2_hit_03.ogg")], "hit", -5,
                {"layers": [{"dt": 0.0, "file": f("sci-fi-sounds/Audio__lowFrequency_explosion_001.ogg"), "role": "hit", "gain_db": -5,
                             "lowpass": 300, "max_dur": .5, "fade_out": .2}]}),
    "camera": ([f("camera/photo.ogg"), f("202-more-sound-effects/Camera__Camera_01.wav"), f("camerashudder/camera_0.ogg"),
                f("202-more-sound-effects/Camera__Camera_03.wav")], "camera", -10, {}),
    "paper": ([f("202-more-sound-effects/Paper _ Stationery__Stationery_01.wav")], "paper", -11, {"max_dur": .45, "slice": "first"}),
    "pop": ([f(f"interface-sounds/Audio__drop_00{k}.ogg") for k in (1, 2, 3)], "pop", -9, {}),
    "tear": ([f("fantasy-sound-effects-tinysized-sfx/sfx-cc0__cover-paper-tear-01.wav"),
              f("fantasy-sound-effects-tinysized-sfx/sfx-cc0__cover-paper-tear-02.wav")], "paper", -6, {"anchor": "start", "max_dur": .6}),
}
# every cut whoosh is pitched down with a low impact under it (the owner wanted bassier transitions on Spin Bout U)
SUBS = ["sci-fi-sounds/Audio__lowFrequency_explosion_000.ogg", "25-cc0-bang-firework-sfx/bang_03.ogg",
        "sci-fi-sounds/Audio__lowFrequency_explosion_001.ogg", "75-cc0-breaking-falling-hit-sfx/bfh1_falling_02.ogg",
        "100-cc0-sfx/explosion.ogg", "25-cc0-bang-firework-sfx/bang_07.ogg"]
WEIGHT = {"whoosh": (-3, -5), "swish": (-2, -8), "whoosh_big": (-4, -2)}   # (pitch semitones, sub layer gain)
LIFT = 2.0
CUT = ("whoosh", "swish", "whoosh_big")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--events", default=os.path.join(ROOT, "plan", "sfx_events_1x1.json"))
    ap.add_argument("--out", default=os.path.join(ROOT, "cache", "sfx", "cues.json"))
    a = ap.parse_args()
    ev = [e for e in json.load(open(a.events)) if e["t"] >= SFX_FROM - 1e-6]
    cuts = [e["t"] for e in ev if e["type"] in CUT]
    rot = {k: itertools.cycle(v[0]) for k, v in KINDS.items()}
    cues, uses, seen = [], {}, set()
    for e in ev:
        k, t = e["type"], e["t"]
        if k not in KINDS or (k, round(t, 2)) in seen:
            continue
        seen.add((k, round(t, 2)))
        near_cut = any(abs(t - c) < .2 for c in cuts)
        if k in ("glitch", "hit", "paper", "pop", "camera") and near_cut:
            continue                                       # a cut already carries its whoosh and sub
        if k == "camera" and any(c["label"] == "camera" and t - c["t"] < 2.6 for c in cues):
            continue
        if k == "pop" and any(c["label"] in ("pop", "slam", "stamp", "keyword") and abs(t - c["t"]) < .45 for c in cues):
            continue
        if k == "paper" and any(c["label"] == "paper" for c in cues):
            continue                                       # one paper slap in the whole edit
        if k in ("slam", "stamp") and any(c["label"] in ("slam", "stamp", "keyword") and abs(t - c["t"]) < .25 for c in cues):
            continue
        files, role, gain, extra = KINDS[k]
        fn = next(rot[k])
        n = uses.get(fn, 0)
        uses[fn] = n + 1
        c = {"t": t, "label": k, "file": fn, "role": role, "gain_db": gain + LIFT} | extra
        if n:
            c["pitch"] = (0, -1, 1, -2, 2)[n % 5]          # a repeat is a new take, not the same file twice
        if fn.endswith("weird_whoosh_sounds_-_whoosh_12_0.mp3"):
            c["slice"] = [.25, .85]                        # its first sweep only (no double whoosh)
        if k in WEIGHT:
            pt, sub_gain = WEIGHT[k]
            c["pitch"] = max(-12, c.get("pitch", 0) + pt)
            sub = SUBS[sum(1 for x in cues if x.get("layers") and x["label"] in CUT) % len(SUBS)]
            c["layers"] = [{"dt": 0.0, "file": f(sub), "role": "hit", "gain_db": sub_gain + LIFT,
                            "lowpass": 320, "max_dur": .55, "fade_out": .2}]
        cues.append(c)
    assert all(c["t"] >= SFX_FROM - 1e-6 for c in cues)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump({"video": os.path.abspath(a.video), "keep_audio": "yes", "cues": cues}, open(a.out, "w"), indent=1)
    by = {}
    for c in cues:
        by[c["label"]] = by.get(c["label"], 0) + 1
    print(f"{len(cues)} cues from {min(c['t'] for c in cues):.2f} s -> {a.out}", by)


if __name__ == "__main__":
    main()
